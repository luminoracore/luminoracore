# Use Cases - LuminoraCore v1.1

**Practical examples of using new features in different applications**

---

## ⚠️ NOTE ON IMPLEMENTATION

These use cases require changes in the **3 components** of the project:

```
luminoracore/        (CORE) - Memory logic, personalities, providers
    ↓
luminoracore-cli/    (CLI)  - Setup, migration, testing commands
    ↓
luminoracore-sdk/    (SDK)  - API for developers
```

**See:** [MODULAR_ARCHITECTURE_v1.1.md](./MODULAR_ARCHITECTURE_v1.1.md) for:
- Complete distribution of changes
- What new files in each component
- Implementation order
- Dependencies between components

**This document shows the FINAL RESULT (use cases), not the implementation.**

---

## 📋 Table of Contents

1. [Waifu Dating Coach](#case-1-waifu-dating-coach)
2. [Adaptive Educational Tutor](#case-2-adaptive-educational-tutor)
3. [Personalized E-commerce Assistant](#case-3-personalized-e-commerce-assistant)
4. [Mental Health Companion](#case-4-mental-health-companion)
5. [Smart Corporate Assistant](#case-5-smart-corporate-assistant)

---

## Case 1: Waifu Dating Coach

### 🎯 Description

Romantic companion app with waifus (Alicia, Mika, Yumi) that develop real relationship with the user.

### 💡 v1.1 Features Used

- ✅ Episodic Memory (special moments)
- ✅ Hierarchical Personalities (relationship progression)
- ✅ Mood System (emotional reactions)
- ✅ Affinity System (relationship points)
- ✅ Fact Extraction (user preferences)
- ✅ Semantic Search (memories from the past)

### 📝 Implementation

```python
# ============================================================================
# SETUP
# ============================================================================

from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types import (
    MemoryConfig,
    PersonalityConfig,
    RelationshipConfig
)

# Complete v1.1 configuration
client = LuminoraCoreClient(
    # Intelligent memory
    memory_config=MemoryConfig(
        enable_episodic_memory=True,
        episode_importance_threshold=6.0,
        enable_semantic_search=True,
        enable_fact_extraction=True
    ),
    
    # Adaptive personality
    personality_config=PersonalityConfig(
        base_personality="alicia_base.json",
        enable_hierarchical=True,
        enable_moods=True,
        enable_adaptation=True
    ),
    
    # Relationship system
    relationship_config=RelationshipConfig(
        enable_affinity=True,
        affinity_rules={
            "share_personal_info": +3,
            "compliment": +2,
            "daily_login": +1,
            "rude_comment": -5
        }
    )
)

# ============================================================================
# DAY 1: FIRST CONVERSATION (Affinity: 0 - Stranger)
# ============================================================================

async def day_1_first_meeting():
    """First conversation with Alicia"""
    
    session_id = await client.create_session(
        personality_name="Alicia - The Sweet Dreamer"
    )
    
    # Message 1: Greeting
    response = await client.send_message(
        session_id,
        message="Hello, I'm Diego"
    )
    
    # Alicia's response (Stranger level, Neutral mood):
    # "Hello Diego. Nice to meet you. How can I help you today? 😊"
    # (Polite but distant, formal)
    
    # System automatically:
    # - Extracts fact: name="Diego"
    # - Affinity: 0 → 1 (first contact)
```

### 🎯 Results

**Without v1.1 (only v1.0):**
- ❌ Personality always the same (no progression)
- ❌ Doesn't remember past moments
- ❌ Doesn't extract preferences automatically
- ❌ Engagement Score: 5/10

**With v1.1:**
- ✅ Relationship evolves naturally (Stranger → Soulmate)
- ✅ Remembers important moments (15 episodes)
- ✅ Knows user deeply (38 facts)
- ✅ Appropriate emotional reactions (7 moods)
- ✅ Engagement Score: 9.2/10

---

## Case 2: Adaptive Educational Tutor

### 🎯 Description

Programming tutor that adapts to student's level and remembers their difficulties.

### 💡 Features Used

- ✅ Fact Extraction (level, knowledge, difficulties)
- ✅ Episodic Memory (breakthrough moments, frustrations)
- ✅ Hierarchical Personalities (complexity adjustment)
- ✅ Moods (emotional adaptation)

---

<div align="center">

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

