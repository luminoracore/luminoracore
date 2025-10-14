# Advanced Memory System - LuminoraCore v1.1

**Complete design of episodic memory system, intelligent classification, and contextual retrieval**

---

## ⚠️ IMPORTANT NOTE

This document describes the **memory system** of LuminoraCore v1.1.

**Conceptual Model (Templates/Instances/Snapshots):**
- **Templates (JSON)** define which memory is enabled (configuration)
- **Instances (DB)** store the actual data (facts, episodes, messages)
- **Snapshots (JSON)** export the complete state including memory

**See:** [CONCEPTUAL_MODEL_REVISED.md](./CONCEPTUAL_MODEL_REVISED.md) to understand how memory integrates with the complete model.

**Memory Data:**
- ✅ Facts → Saved in **DB** (NOT in JSON Template)
- ✅ Episodes → Saved in **DB** (NOT in JSON Template)
- ✅ Embeddings → Saved in **Vector Store** (NOT in JSON Template)
- ✅ The JSON Template only defines memory **configuration** (which features are enabled)

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Memory Architecture](#memory-architecture)
3. [Memory Types](#memory-types)
4. [Episodic Memory](#episodic-memory)
5. [Semantic Search (Vector Search)](#semantic-search)
6. [Intelligent Classification](#intelligent-classification)
7. [Automatic Fact Extraction](#automatic-fact-extraction)
8. [Long-term Storage](#long-term-storage)
9. [Contextual Retrieval](#contextual-retrieval)
10. [Optimization and Performance](#optimization-and-performance)

---

## Overview

### 🎯 Objective

**Create a memory system that allows personalities to remember conversations in a human way:**
- Remember important moments (episodic memory)
- Search by meaning, not just exact words (vector search)
- Automatically classify information (facts, episodes, events)
- Automatically retrieve relevant context

### ❌ Current Problems (v1.0)

```python
# v1.0 - Basic memory
await client.store_memory(session_id, "favorite_anime", "Naruto")  # Manual
await client.get_memory(session_id, "favorite_anime")  # Only key-value

# Problems:
# 1. ❌ Manual fact extraction
# 2. ❌ Doesn't differentiate important from trivial information
# 3. ❌ Can't search "remember when we talked about my dog?"
# 4. ❌ Doesn't save "special moments" automatically
# 5. ❌ Storage without prioritization
```

### ✅ Proposed Solution (v1.1)

```python
# v1.1 - Intelligent memory
client = LuminoraCoreClient(
    memory_config=MemoryConfig(
        enable_episodic_memory=True,       # ← Automatic episodes
        enable_fact_extraction=True,        # ← Automatic extraction
        enable_semantic_search=True,        # ← Search by meaning
        memory_classification="automatic"   # ← AI classification
    )
)

# Everything is automatic
response = await client.send_message(
    session_id,
    "My dog Max died yesterday, I'm devastated"
)

# System automatically:
# 1. ✅ Extracts facts: pet_name="Max", pet_status="deceased"
# 2. ✅ Detects importance: 9/10 (critical emotional moment)
# 3. ✅ Creates episode: type="loss", tags=["sad", "pet", "grief"]
# 4. ✅ Generates embedding for semantic search
# 5. ✅ Stores with high priority
```

---

## Memory Architecture

### 🏗️ System Layers

```
┌────────────────────────────────────────────────────────────┐
│                    CONVERSATION (LLM)                      │
│  "Remember when we talked about my dog?"                   │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│              INTELLIGENT RETRIEVAL LAYER                   │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Vector Search│  │ Episodic     │  │ Fact Retrieval  │  │
│  │ (Semantic)   │  │ Memory Query │  │ (Key-Value)     │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│            CLASSIFICATION AND PROCESSING LAYER             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Importance   │  │ Category     │  │ Sentiment       │  │
│  │ Scoring      │  │ Classification│  │ Analysis        │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│                 EXTRACTION LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Fact         │  │ Episode      │  │ Entity          │  │
│  │ Extraction   │  │ Detection    │  │ Recognition     │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│                STORAGE LAYER                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Short-term Memory (Redis)          │ Rolling window  │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ Long-term Memory (PostgreSQL)      │ Facts + Episodes│  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ Vector Store (Pinecone/pgvector)   │ Embeddings     │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

---

## Memory Types

### 1. **Short-term Memory (Working Memory)**

**Duration:** Current session (until close)  
**Storage:** Redis / Memory  
**Content:** Last N messages of conversation

```python
# Configuration
working_memory_config = {
    "max_messages": 50,              # Last 50 messages
    "max_tokens": 4000,              # Or 4000 tokens (whichever comes first)
    "compression": "automatic",      # Compress automatically if exceeds
    "backend": "redis"               # Redis for speed
}
```

**Use:**
- Immediate conversation context
- Reference to recent messages
- No search required, always available

---

### 2. **Semantic Memory (Facts)**

**Duration:** Permanent (until updated)  
**Storage:** PostgreSQL / MongoDB  
**Content:** Factual information about the user

```python
# Structure of a Fact
{
    "id": "fact_123",
    "user_id": "user_456",
    "session_id": "session_789",
    "category": "personal_info",        # personal_info, preferences, relationships, etc.
    "key": "favorite_anime",
    "value": "Naruto",
    "confidence": 0.95,                 # How certain the system is
    "source_message_id": "msg_555",
    "first_mentioned": "2025-10-14T10:30:00Z",
    "last_updated": "2025-10-14T10:30:00Z",
    "mention_count": 1,
    "tags": ["anime", "entertainment", "preference"],
    "context": "User mentioned they love Naruto"
}
```

**Fact Categories:**
- `personal_info`: Name, age, profession, location
- `preferences`: Likes, dislikes, favorites
- `relationships`: Family, friends, partners, pets
- `hobbies`: Activities, interests
- `goals`: Objectives, aspirations
- `health`: Physical, mental health
- `work`: Job, studies, career
- `events`: Important past events

---

### 3. **Episodic Memory (Episodes)**

**Duration:** Permanent  
**Storage:** PostgreSQL / MongoDB  
**Content:** Important moments in the relationship

```python
# Structure of an Episode
{
    "id": "episode_123",
    "user_id": "user_456",
    "session_id": "session_789",
    "type": "emotional_moment",      # emotional_moment, milestone, confession, conflict, achievement
    "title": "Loss of pet Max",
    "summary": "User shared the sad news that their dog Max passed away yesterday. They're very emotionally affected.",
    "importance": 9.5,               # 0-10 (10 = most important)
    "sentiment": "very_sad",         # very_happy, happy, neutral, sad, very_sad, angry
    "tags": ["sad", "loss", "pet", "grief", "max"],
    "participants": ["user_456", "personality_alicia"],
    "context_messages": [            # Messages that form the episode
        "msg_100",
        "msg_101",
        "msg_102"
    ],
    "timestamp": "2025-10-14T10:30:00Z",
    "temporal_decay": 1.0,          # Starts at 1.0, decays over time
    "related_facts": ["fact_pet_max", "fact_pet_status"],
    "related_episodes": [],
    "embedding": [0.234, -0.567, ...] # For semantic search
}
```

**Episode Types:**

| Type | Description | Base Importance | Examples |
|------|-------------|-----------------|----------|
| `emotional_moment` | Moments of high emotional charge | 7-10 | Losses, breakups, confessions |
| `milestone` | Milestones in relationship | 6-9 | First conversation, anniversaries |
| `confession` | User shares something personal | 6-8 | Secrets, fears, dreams |
| `conflict` | Disagreements or tensions | 5-7 | Arguments, misunderstandings |
| `achievement` | User accomplishments | 5-8 | Promotion, graduation, success |
| `bonding` | Special connection moments | 6-8 | Shared laughter, mutual support |
| `routine` | Everyday conversations | 1-3 | Greetings, weather, small talk |

---

### 4. **Vector Memory (Semantic Memory)**

**Duration:** Permanent  
**Storage:** Pinecone / Weaviate / PostgreSQL pgvector  
**Content:** Message embeddings for semantic search

```python
# Each message becomes a vector
{
    "id": "vec_msg_123",
    "message_id": "msg_123",
    "user_id": "user_456",
    "session_id": "session_789",
    "content": "My dog Max died yesterday",
    "embedding": [0.234, -0.567, 0.123, ...],  # 1536 dimensions (OpenAI)
    "metadata": {
        "timestamp": "2025-10-14T10:30:00Z",
        "speaker": "user",
        "sentiment": "very_sad",
        "importance": 9.5,
        "tags": ["pet", "loss", "sad"]
    }
}
```

**Semantic Search:**
```python
# Query: "Remember when we talked about my dog?"
query_embedding = create_embedding("Remember when we talked about my dog?")

# Search by cosine similarity
results = vector_store.query(
    vector=query_embedding,
    top_k=5,
    filter={"user_id": "user_456"}
)

# Semantically similar results:
# 1. "My dog Max died yesterday" (similarity: 0.92)
# 2. "Max was my best friend" (similarity: 0.87)
# 3. "I really miss my puppy" (similarity: 0.84)
```

---

## Episodic Memory

### 🎯 Concept

**Inspired by human memory:**  
Humans don't remember every conversation word for word, but we do remember **special moments**.

**Examples:**
- "I remember when you told me your dog died"
- "That time you were so happy about your promotion"
- "When you confessed your fears about your relationship"

### 🏗️ Implementation

```python
# luminoracore/core/memory/episodic.py

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import numpy as np

@dataclass
class Episode:
    """Represents a memorable episode in conversation"""
    
    id: str
    user_id: str
    session_id: str
    type: str  # emotional_moment, milestone, confession, etc.
    title: str
    summary: str
    importance: float  # 0-10
    sentiment: str
    tags: List[str]
    context_messages: List[str]  # Message IDs
    timestamp: datetime
    temporal_decay: float = 1.0
    related_facts: List[str] = None
    related_episodes: List[str] = None
    embedding: np.ndarray = None
    
    def get_current_importance(self) -> float:
        """Current importance considering temporal decay"""
        return self.importance * self.temporal_decay
    
    def update_decay(self, days_passed: int):
        """Update temporal decay (memories fade over time)"""
        # Logarithmic decay: recent events decay slowly
        decay_rate = 0.1
        self.temporal_decay = 1.0 / (1.0 + decay_rate * np.log(days_passed + 1))
```

---

## Semantic Search

### 🔍 Vector Search

**Problem:** Exact search doesn't work for conversational memory

```python
# ❌ Exact search
user: "when we talked about my dog"
system.search("dog")  # Only finds messages with word "dog"

user: "that time I told you about my pet"
system.search("pet")  # Finds nothing if you said "dog" before
```

**Solution:** Semantic search with embeddings

```python
# ✅ Semantic search
user: "when we talked about my dog"
embedding = create_embedding("when we talked about my dog")
results = vector_search(embedding)
# → Finds: "my dog Max", "my pet", "my puppy", etc.

user: "that time I told you about my pet"
embedding = create_embedding("that time I told you about my pet")
results = vector_search(embedding)
# → Finds conversations about dogs, cats, pets in general
```

---

## Intelligent Classification

### 📊 Multi-dimensional Classification System

**Each memory is classified by:**

1. **Category** (what type of information)
2. **Importance** (how relevant)
3. **Sentiment** (what emotion)
4. **Temporality** (when it occurred / temporal validity)
5. **Privacy** (how sensitive)

```python
# luminoracore/core/memory/classifier.py

from enum import Enum
from dataclasses import dataclass

class MemoryCategory(Enum):
    PERSONAL_INFO = "personal_info"      # Name, age, profession
    PREFERENCES = "preferences"          # Likes, dislikes
    RELATIONSHIPS = "relationships"      # Family, friends, partner
    HOBBIES = "hobbies"                 # Activities, interests
    GOALS = "goals"                     # Objectives, aspirations
    HEALTH = "health"                   # Physical, mental health
    WORK = "work"                       # Job, studies
    EVENTS = "events"                   # Past events
    ROUTINE = "routine"                 # Habits, routines
    OTHER = "other"

class ImportanceLevel(Enum):
    CRITICAL = "9-10"      # Life-changing events
    HIGH = "7-8"           # Very important
    MEDIUM = "5-6"         # Moderately important
    LOW = "3-4"            # Not very important
    TRIVIAL = "0-2"        # Irrelevant
```

---

## Automatic Fact Extraction

### 🤖 NLP-Based Fact Extraction

```python
# luminoracore/core/memory/fact_extractor.py

class FactExtractor:
    """Extracts facts automatically from conversations"""
    
    def __init__(self, llm_provider, confidence_threshold: float = 0.7):
        self.llm = llm_provider
        self.confidence_threshold = confidence_threshold
    
    async def extract_from_message(
        self,
        message: str,
        context: Optional[List[Message]] = None
    ) -> List[Fact]:
        """
        Extracts facts from a message
        
        Args:
            message: User message
            context: Previous messages for context
        
        Returns:
            List of extracted facts
        """
        prompt = f"""
        Extract factual information about the user from the following message.
        
        User message: "{message}"
        
        Respond with JSON:
        {{
            "facts": [
                {{
                    "category": "personal_info | preferences | relationships | hobbies | goals | health | work",
                    "key": "descriptive_fact_name",
                    "value": "extracted_value",
                    "confidence": 0-1,
                    "reasoning": "why you extracted this fact"
                }}
            ]
        }}
        
        Rules:
        - Only extract EXPLICIT facts, don't infer
        - High confidence (>0.9) only if direct statement
        - Key should be descriptive (e.g. "favorite_anime", "pet_name", "age")
        - If no facts, return empty array
        
        Examples:
        
        Input: "I'm Diego, I'm 28 and work in IT"
        Output:
        {{
            "facts": [
                {{"category": "personal_info", "key": "name", "value": "Diego", "confidence": 0.99}},
                {{"category": "personal_info", "key": "age", "value": 28, "confidence": 0.99}},
                {{"category": "work", "key": "profession", "value": "IT", "confidence": 0.95}}
            ]
        }}
        """
        
        result = await self.llm.complete(
            prompt,
            response_format="json_object",
            temperature=0.1
        )
        
        # Filter by confidence threshold
        facts = [
            Fact(**f)
            for f in result["facts"]
            if f["confidence"] >= self.confidence_threshold
        ]
        
        return facts
```

---

<div align="center">

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

