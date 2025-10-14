# Technical Architecture - LuminoraCore v1.1

**Detailed implementation design: classes, modules, APIs, and database schemas**

---

## ⚠️ IMPORTANT DISCLAIMER

**Python code examples in this document show values like `affinity_range=(0, 20)` in code.**

**THIS DOES NOT MEAN THEY ARE HARDCODED.**

These values are **example defaults** that the code uses **ONLY IF the JSON doesn't specify them**.

**IN PRODUCTION:**
- All values are read from the personality JSON
- Code only has fallback defaults
- See [INTEGRATION_WITH_CURRENT_SYSTEM.md](./INTEGRATION_WITH_CURRENT_SYSTEM.md) for complete clarification
- See [PERSONALITY_JSON_EXAMPLES.md](./PERSONALITY_JSON_EXAMPLES.md) for real JSON templates

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Module Structure](#module-structure)
3. [Database Schemas](#database-schemas)
4. [APIs and Interfaces](#apis-and-interfaces)
5. [Data Flows](#data-flows)
6. [Configuration](#configuration)
7. [Integration with v1.0](#integration-with-v10)

---

## Architecture Overview

### 🏗️ Component Responsibilities

**CRITICAL:** Understand the division of responsibilities:

| Component | What it HAS | What it DOES NOT have |
|-----------|-------------|----------------------|
| **luminoracore (Core)** | ✅ Personality classes<br>✅ Compilers<br>✅ Memory classes<br>✅ Relationship classes<br>✅ Validators<br>✅ Schemas | ❌ NO providers (in SDK)<br>❌ NO storage (in SDK)<br>❌ NO session management (in SDK)<br>❌ NO API calls |
| **luminoracore-sdk** | ✅ LLM providers (10 already exist)<br>✅ Embedding providers<br>✅ Storage (SQLite, PostgreSQL)<br>✅ Session management<br>✅ Memory manager<br>✅ Client API | ❌ NO personality definitions<br>❌ NO compilers |
| **luminoracore-cli** | ✅ Terminal commands (11 exist)<br>✅ Interactive wizards<br>✅ Configuration | ❌ NO business logic<br>❌ NO providers |

**v1.1 Implementation Strategy:**
- **Core:** CREATE new personality/memory classes
- **SDK:** EXTEND existing storage/memory classes
- **CLI:** ADD 3 new commands to existing 11

---

### 💡 How It's Really Used (Complete Example)

```python
# ============================================
# REAL EXAMPLE: From JSON to Execution
# ============================================

# 1. Developer creates personality in JSON
# alicia.json contains:
# {
#   "persona": {...},
#   "hierarchical_config": {
#     "enabled": true,
#     "relationship_levels": [
#       {"name": "stranger", "affinity_range": [0, 20], "modifiers": {...}},
#       {"name": "friend", "affinity_range": [41, 60], "modifiers": {...}}
#     ]
#   }
# }

# 2. System loads JSON
personality_json = load_json("alicia.json")

# 3. Create PersonalityTree FROM JSON (not hardcoded)
tree = PersonalityTree.from_json(personality_json)  # ← Reads values from JSON

# 4. User talks
affinity = await db.get_affinity(session_id)  # Ex: 45 (from DB)
mood = await db.get_mood(session_id)          # Ex: "shy" (from DB)

# 5. Compile dynamically
compiled = tree.compile(affinity=45, mood="shy")
# Applies modifiers that are in the JSON

# 6. Generate response
response = await llm.generate(compiled + message)
```

**Values are NOT in code, they're in JSON.**

---

## Database Schemas

### PostgreSQL Schema

```sql
-- ============================================================================
-- FACTS TABLE
-- ============================================================================

CREATE TABLE user_facts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    session_id VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,  -- personal_info, preferences, etc.
    key VARCHAR(255) NOT NULL,
    value JSONB NOT NULL,  -- Supports strings, numbers, objects
    confidence FLOAT DEFAULT 1.0,  -- 0.0 - 1.0
    source_message_id VARCHAR(255),
    first_mentioned TIMESTAMP DEFAULT NOW(),
    last_updated TIMESTAMP DEFAULT NOW(),
    mention_count INTEGER DEFAULT 1,
    tags TEXT[],
    context TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    CONSTRAINT unique_user_fact UNIQUE(user_id, category, key)
);

CREATE INDEX idx_user_facts_user_id ON user_facts(user_id);
CREATE INDEX idx_user_facts_category ON user_facts(category);
CREATE INDEX idx_user_facts_tags ON user_facts USING GIN(tags);

-- ============================================================================
-- EPISODES TABLE
-- ============================================================================

CREATE TABLE episodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    session_id VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,  -- emotional_moment, milestone, etc.
    title VARCHAR(500) NOT NULL,
    summary TEXT NOT NULL,
    importance FLOAT NOT NULL,  -- 0-10
    sentiment VARCHAR(50) NOT NULL,  -- very_positive, positive, etc.
    tags TEXT[],
    context_messages TEXT[],  -- Array of message IDs
    timestamp TIMESTAMP NOT NULL,
    temporal_decay FLOAT DEFAULT 1.0,
    related_facts UUID[],
    related_episodes UUID[],
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_episodes_user_id ON episodes(user_id);
CREATE INDEX idx_episodes_importance ON episodes(importance);
CREATE INDEX idx_episodes_timestamp ON episodes(timestamp);
CREATE INDEX idx_episodes_type ON episodes(type);
CREATE INDEX idx_episodes_tags ON episodes USING GIN(tags);

-- ============================================================================
-- VECTOR EMBEDDINGS (pgvector)
-- ============================================================================

-- Requires pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE message_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    session_id VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI text-embedding-3-small
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_message_embeddings_user_id ON message_embeddings(user_id);
CREATE INDEX idx_message_embeddings_embedding ON message_embeddings 
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ============================================================================
-- AFFINITY TABLE
-- ============================================================================

CREATE TABLE user_affinity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    personality_name VARCHAR(255) NOT NULL,
    affinity_points INTEGER DEFAULT 0,  -- 0-100
    current_level VARCHAR(50) DEFAULT 'stranger',  -- stranger, friend, etc.
    total_messages INTEGER DEFAULT 0,
    positive_interactions INTEGER DEFAULT 0,
    negative_interactions INTEGER DEFAULT 0,
    last_interaction TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    CONSTRAINT unique_user_personality UNIQUE(user_id, personality_name)
);

CREATE INDEX idx_affinity_user_id ON user_affinity(user_id);

-- ============================================================================
-- SESSION MOOD STATE
-- ============================================================================

CREATE TABLE session_moods (
    session_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    current_mood VARCHAR(50) DEFAULT 'neutral',
    mood_intensity FLOAT DEFAULT 1.0,
    mood_started_at TIMESTAMP DEFAULT NOW(),
    mood_history JSONB DEFAULT '[]'::jsonb,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_session_moods_user_id ON session_moods(user_id);
```

---

## APIs and Interfaces

### 🔌 Provider Architecture (SDK)

**IMPORTANT:** Providers **ALREADY EXIST** in SDK. We do NOT create them.

**Existing providers in SDK:**

```
luminoracore-sdk-python/luminoracore_sdk/providers/
├── base.py                  # ✅ EXISTS v1.0
├── anthropic.py             # ✅ EXISTS v1.0 (Claude)
├── deepseek.py              # ✅ EXISTS v1.0
├── google.py                # ✅ EXISTS v1.0 (Gemini)
├── groq.py                  # ✅ EXISTS v1.0
├── huggingface.py           # ✅ EXISTS v1.0
├── mistral.py               # ✅ EXISTS v1.0
├── ollama.py                # ✅ EXISTS v1.0
├── openai.py                # ✅ EXISTS v1.0
└── replicate.py             # ✅ EXISTS v1.0
```

**Usage example:**

```python
# Core uses SDK providers for LLM calls
from luminoracore_sdk.providers import DeepSeekProvider

# Fact extraction uses LLM provider
provider = DeepSeekProvider(api_key=config.api_key)
facts = await fact_extractor.extract_facts(
    message=message,
    llm_provider=provider  # ← Uses SDK provider
)
```

**v1.1 does NOT create new providers.** ✅

---

### 🗄️ Storage Architecture (SDK)

**IMPORTANT:** Storage **ALREADY EXISTS** in SDK. We do NOT create it.

**Existing storage in SDK:**

```
luminoracore-sdk-python/luminoracore_sdk/session/
├── storage.py               # ✅ EXISTS v1.0 (StorageProvider class)
├── manager.py               # ✅ EXISTS v1.0 (Session management)
├── memory.py                # ✅ EXISTS v1.0 (Memory manager)
└── state.py                 # ✅ EXISTS v1.0 (State management)
```

**v1.1 EXTENDS storage.py:**

```python
# EXTEND existing StorageProvider class
class StorageProvider:
    # ✅ v1.0 methods (EXIST, no changes)
    async def save_message(self, ...)
    async def get_history(self, ...)
    async def save_state(self, ...)
    
    # 🆕 NEW v1.1 methods (ADD, don't replace)
    async def save_fact(self, ...)        # NEW
    async def save_episode(self, ...)     # NEW
    async def get_affinity(self, ...)     # NEW
    async def update_affinity(self, ...)  # NEW
```

**v1.1 does NOT create new storage infrastructure.** ✅

---

### Client API (Python SDK)

```python
"""
luminoracore_sdk/client.py

Client API with new v1.1 features
"""

from typing import List, Optional, Dict

class LuminoraCoreClient:
    """Enhanced v1.1 client"""
    
    # ========================================================================
    # MEMORY (NEW in v1.1)
    # ========================================================================
    
    async def search_memories(
        self,
        session_id: str,
        query: str,
        top_k: int = 10
    ) -> List[MemorySearchResult]:
        """Semantic search in memory"""
        pass
    
    async def get_episodes(
        self,
        session_id: str,
        min_importance: float = 5.0
    ) -> List[Episode]:
        """Get memorable episodes"""
        pass
    
    async def get_facts(
        self,
        session_id: str,
        category: Optional[str] = None
    ) -> List[Fact]:
        """Get user facts"""
        pass
    
    # ========================================================================
    # AFFINITY (NEW in v1.1)
    # ========================================================================
    
    async def get_affinity(
        self,
        session_id: str
    ) -> AffinityInfo:
        """Get affinity information"""
        pass
    
    # ========================================================================
    # SNAPSHOTS (NEW in v1.1)
    # ========================================================================
    
    async def export_snapshot(
        self,
        session_id: str,
        include_options: Optional[dict] = None
    ) -> dict:
        """Export complete snapshot"""
        pass
    
    async def import_snapshot(
        self,
        snapshot_file: str,
        user_id: str
    ) -> str:
        """Import snapshot (returns session_id)"""
        pass
```

---

## Integration with v1.0

### Backward Compatibility

```python
"""
Guarantee compatibility with existing v1.0 code
"""

# v1.0 code keeps working
client = LuminoraCoreClient()  # Without new configs
session_id = await client.create_session(...)
response = await client.send_message(session_id, "Hello")

# But v1.1 features are disabled by default
# To enable, use explicit configs:

client = LuminoraCoreClient(
    memory_config=MemoryConfig(
        enable_episodic_memory=True,  # Opt-in
        enable_semantic_search=True,
        enable_fact_extraction=True
    ),
    personality_config=PersonalityConfig(
        enable_hierarchical=True,  # Opt-in
        enable_moods=True
    )
)
```

---

<div align="center">

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

