# Hierarchical Personality System - LuminoraCore v1.1

**Complete design of adaptive personality system with tree-based structure**

---

## ⚠️ IMPORTANT NOTE

This document describes the **hierarchical personality system** of LuminoraCore v1.1.

**Conceptual Model (Templates/Instances/Snapshots):**
- **Templates (JSON)** define possible levels, possible moods, and base configuration
- **Instances (DB)** store current state (current affinity, current mood)
- **Snapshots (JSON)** export complete personality state

**See:** [CONCEPTUAL_MODEL_REVISED.md](./CONCEPTUAL_MODEL_REVISED.md) for the complete model.

**Personality State:**
- ✅ **Possible** relationship levels → Defined in **JSON Template**
- ✅ User's **current** level → Saved in **DB** (affinity points)
- ✅ **Possible** moods → Defined in **JSON Template**
- ✅ Session's **current** mood → Saved in **DB**

**Code examples in this document:**
- Show the **implementation logic** (Python classes)
- **Values** (affinity ranges, modifiers) are read from **JSON Template**
- See [INTEGRATION_WITH_CURRENT_SYSTEM.md](./INTEGRATION_WITH_CURRENT_SYSTEM.md) for how it's configured in JSON

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Tree-Based Architecture](#tree-based-architecture)
3. [Emotional States (Moods)](#emotional-states-moods)
4. [Intensity Levels](#intensity-levels)
5. [Contextual Adaptation](#contextual-adaptation)
6. [Smooth Transitions](#smooth-transitions)
7. [Affinity Integration](#affinity-integration)
8. [Practical Examples](#practical-examples)

---

## Overview

### 🎯 Central Concept

**Real people don't always behave the same:**
- React differently depending on context
- Have emotional states that change
- Adjust their intensity based on situation
- Progress in relationships (stranger → friend → partner)

**Real Example:**

```
Situation 1: A stranger tells you "you're pretty"
Reaction: "Uh... thanks?" (discomfort, distant)

Situation 2: Your best friend tells you "you're pretty"
Reaction: "Aw, thanks! 😊" (joy, warm)

Situation 3: Your partner tells you "you're pretty"
Reaction: "You make me nervous when you say that 😳💕" (shyness, intimate)
```

**Same person, same input, different output depending on:**
- Relationship level (affinity)
- Emotional state (mood)
- Conversation context
- Recent history

---

### ❌ Current Problem (v1.0)

```python
# v1.0 - Static personality
personality = load_personality("alicia.json")

# Always responds the same
user: "You're pretty"
alicia: "Thanks! 😊"  # Same response regardless of context

user: [says something sad]
alicia: [responds equally energetic]  # Doesn't adapt mood

user: [after 100 conversations]
alicia: [behaves like a stranger]  # No relationship progression
```

### ✅ Proposed Solution (v1.1)

```python
# v1.1 - Hierarchical adaptive personality
personality_tree = PersonalityTree(
    base_personality="alicia_base.json",
    relationship_levels={
        "stranger": "alicia_stranger.json",
        "acquaintance": "alicia_acquaintance.json",
        "friend": "alicia_friend.json",
        "close_friend": "alicia_close_friend.json",
        "soulmate": "alicia_soulmate.json"
    },
    moods={
        "happy": {"empathy": +0.1, "humor": +0.2},
        "shy": {"formality": +0.2, "directness": -0.3},
        "sad": {"empathy": +0.3, "humor": -0.2},
        "excited": {"verbosity": +0.2, "creativity": +0.2}
    },
    adaptation_enabled=True
)

# Automatic adaptation
user: "You're pretty" + context(affinity=10, mood="neutral")
alicia: "Uh... thanks, I guess 😅"  # Stranger + neutral

user: "You're pretty" + context(affinity=80, mood="shy")
alicia: "Oh! 😳 You make me nervous... 💕"  # Close friend + shy

user: [says something sad] + context(...)
alicia: [automatically changes to "concerned" mood, more empathetic]
```

---

## Tree-Based Architecture

### 🌳 Personality Tree Structure

```
                    ┌─────────────────────┐
                    │   BASE PERSONALITY  │
                    │   (Alicia Core)     │
                    │                     │
                    │  Core traits that   │
                    │  NEVER change:      │
                    │  - archetype        │
                    │  - values           │
                    │  - core identity    │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
       ┌────────────┐  ┌────────────┐  ┌────────────┐
       │ STRANGER   │  │   FRIEND   │  │  SOULMATE  │
       │  LEVEL     │  │   LEVEL    │  │   LEVEL    │
       │            │  │            │  │            │
       │ Modifiers: │  │ Modifiers: │  │ Modifiers: │
       │ +distant   │  │ +warm      │  │ +intimate  │
       │ +formal    │  │ +playful   │  │ +devoted   │
       └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
             │               │               │
    ┌────────┴────────┐     │      ┌────────┴────────┐
    │                 │     │      │                 │
    ▼                 ▼     ▼      ▼                 ▼
┌────────┐        ┌────────┐  ┌────────┐        ┌────────┐
│ Happy  │        │  Shy   │  │  Sad   │        │Excited │
│ Mood   │        │  Mood  │  │  Mood  │        │ Mood   │
│        │        │        │  │        │        │        │
│+humor  │        │+formal │  │+empathy│        │+energy │
│+energy │        │-direct │  │-humor  │        │+creative│
└────────┘        └────────┘  └────────┘        └────────┘
```

---

<div align="center">

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

