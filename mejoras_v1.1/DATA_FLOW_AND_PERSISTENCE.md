# Data Flow and Persistence - LuminoraCore v1.1

**Complete clarification about what's saved where, what's updated, and how the system works**

---

## ⚠️ CRITICAL CLARIFICATIONS

### 1. Personality JSON is NEVER updated

```
❌ INCORRECT:
- Load alicia.json
- User increases affinity
- Modify alicia.json with new affinity  ← NO!

✅ CORRECT:
- Load alicia.json (ONCE, immutable)
- User increases affinity
- Save affinity in DB (PostgreSQL/SQLite/etc)
- Apply modifiers from JSON in memory (temporary)
```

**The JSON file is a TEMPLATE, not a state.**

---

### 2. States are saved in DB, NOT in JSON

```
┌─────────────────────────────────────────────────────────┐
│ Personality JSON (IMMUTABLE)                            │
│ - alicia.json                                           │
│ - Defines base behavior                                 │
│ - Defines possible levels                               │
│ - Defines possible moods                                │
│ - NEVER changes                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ State DB (MUTABLE)                                      │
│ - PostgreSQL / SQLite / MongoDB                         │
│ - Stores: affinity, current_mood, session_state         │
│ - Constantly updated                                    │
│ - Persists between sessions                             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Vector DB (SEARCH)                                      │
│ - pgvector / Pinecone                                   │
│ - Stores: message embeddings                            │
│ - Only for semantic search                              │
│ - Does NOT replace current DB                           │
└─────────────────────────────────────────────────────────┘
```

---

### 3. Dynamic Compilation is FAST (not slow)

**Compile = Apply deltas, not regenerate everything**

```python
# Compilation takes ~1-5ms (very fast)
base = {"empathy": 0.95, "formality": 0.3}
modifier = {"empathy": +0.2, "formality": -0.1}
compiled = apply_deltas(base, modifier)  # {"empathy": 1.0, "formality": 0.2}
# Time: ~1ms
```

vs

```python
# LLM call takes ~500-2000ms (slow)
response = await llm.generate(prompt)
# Time: ~500-2000ms
```

**Compilation is 500x faster than LLM.**

---

## 📊 Separation of Responsibilities

### What goes in EACH storage

| Data Type | Storage | Mutable | Persistence |
|-----------|---------|---------|-------------|
| **Base personality** | `alicia.json` (file) | ❌ NO | Permanent |
| **Defined levels/moods** | `alicia.json` (file) | ❌ NO | Permanent |
| **Current conversation** | Redis / Memory | ✅ YES | Current session |
| **Message history** | PostgreSQL / SQLite | ✅ YES | Permanent |
| **User facts** | PostgreSQL / SQLite | ✅ YES | Permanent |
| **Episodes** | PostgreSQL / SQLite | ✅ YES | Permanent |
| **Current affinity** | PostgreSQL / SQLite | ✅ YES | Permanent |
| **Current mood** | PostgreSQL / SQLite / Redis | ✅ YES | Session or permanent |
| **Embeddings** | pgvector / Pinecone | ✅ YES | Permanent |

---

## 🔄 Complete Flow: Sending a Message

### Flow Diagram with Times

```
User sends: "Hello Alicia, you're very pretty"
       │
       ▼
┌─────────────────────────────────────────────────────┐
│ 1. LOAD CONTEXT (async, parallel)                   │  ⏱️ ~50ms
│    ├─ Load personality JSON (if not cached)         │
│    ├─ Get affinity from DB                          │
│    ├─ Get current mood from DB                      │
│    └─ Get last 10 messages from DB                  │
└─────────────┬───────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────┐
│ 2. COMPILE PERSONALITY (in memory)                  │  ⏱️ ~5ms
│    ├─ Base (from JSON)                              │
│    ├─ + Level by affinity (from JSON)               │
│    ├─ + Current mood (from JSON)                    │
│    └─ = Compiled personality (in memory)            │
└─────────────┬───────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────┐
│ 3. GENERATE RESPONSE (LLM)                          │  ⏱️ ~1500ms ← BOTTLENECK
│    - Call to DeepSeek/OpenAI/etc                    │
│    - With compiled personality + context            │
└─────────────┬───────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────┐
│ 4. POST-RESPONSE PROCESSING (async, parallel)       │  ⏱️ ~200ms (background)
│    ├─ Extract facts (light LLM call)                │
│    ├─ Detect new mood (light LLM call)              │
│    ├─ Update affinity (calculation)                 │
│    ├─ Detect episode (every 5 messages)             │
│    ├─ Create embeddings (API call)                  │
│    └─ Save everything to DB                         │
└─────────────┬───────────────────────────────────────┘
              │
              ▼
       Return response to user

TOTAL: ~1555ms (user sees response before step 4)
       Step 4 runs in background
```

---

## 🎯 Answers to Your Questions

### Q1: "Recompile with each message?"

**Yes, but it's VERY fast (~5ms).**

```python
# Pseudocode of the process
async def send_message(session_id, message):
    # 1. Load context (parallel) - ~50ms
    affinity = await db.get_affinity(session_id)        # ~10ms
    mood = await db.get_mood(session_id)                # ~10ms
    personality_json = load_cached("alicia.json")       # ~1ms (cache)
    recent_messages = await db.get_messages(session_id, limit=10)  # ~30ms
    
    # 2. Compile personality (in memory) - ~5ms
    compiled = compile_dynamic(
        base=personality_json,
        affinity=affinity,      # Ex: 45
        mood=mood               # Ex: "shy"
    )
    # This only applies deltas:
    # empathy: 0.95 + 0.2 (friend) + 0.0 (shy) = 1.0
    # formality: 0.3 + (-0.1) (friend) + 0.2 (shy) = 0.4
    
    # 3. Generate response (LLM) - ~1500ms ← THIS is the slow one
    response = await llm.generate(
        personality=compiled,
        context=recent_messages,
        message=message
    )
    
    # 4. Return immediately
    return response
    
    # 5. Background processing (doesn't block) - ~200ms
    asyncio.create_task(process_post_response(session_id, message, response))
```

**User sees response in ~1555ms, where 1500ms is the LLM (inevitable).**

---

### Q2: "Does JSON get updated?"

**NO. JSON is NEVER updated.**

```python
# ❌ NEVER do this:
personality_json["advanced_parameters"]["empathy"] = new_value
save_json(personality_json)  # NO!

# ✅ Do this:
# JSON is a READ-ONLY template
# States are saved in DB
await db.update_affinity(session_id, new_affinity)  # Save in PostgreSQL
await db.update_mood(session_id, new_mood)          # Save in PostgreSQL
```

**Analogy:**
```
JSON is like a COOKING RECIPE.
- The recipe does NOT change when you cook
- But each time you cook, you adjust ingredients based on context
- The adjustments are temporary, the recipe remains
```

---

### Q3: "Does it only persist while chatting?"

**NO. It persists PERMANENTLY in DB.**

```sql
-- Affinity table (PostgreSQL/SQLite)
CREATE TABLE user_affinity (
    user_id VARCHAR(255),
    personality_name VARCHAR(255),
    affinity_points INTEGER,        -- Persists here
    current_level VARCHAR(50),      -- Persists here
    last_updated TIMESTAMP
);

-- Session mood table
CREATE TABLE session_moods (
    session_id VARCHAR(255),
    current_mood VARCHAR(50),       -- Persists here
    mood_intensity FLOAT,           -- Persists here
    mood_started_at TIMESTAMP
);
```

**Persistence flow:**

```python
# Day 1, Message 1
await send_message(session_id, "Hello")
# Affinity: 0 → 1
# Saved in DB: affinity=1

# Day 1, Message 2
await send_message(session_id, "You're pretty")
# Affinity: 1 → 3
# Saved in DB: affinity=3, mood="shy"

# User closes the app
# ...

# Day 2, new chat
session_id = await create_session(...)  # Can be new session
# System loads:
# - affinity = 3 (from DB)
# - mood = "neutral" (reset per new session, OPTIONAL)
# - Base personality (from JSON)

# Compiles with affinity=3
# User continues where they left off
```

---

## 💾 Multi-Layer Persistence System

### Layer 1: JSON Files (Personalities - IMMUTABLE)

```
luminoracore/personalities/
├── alicia.json              ← Immutable template
├── mika.json                ← Immutable template
└── yumi.json                ← Immutable template

Use:
- Loaded ONCE at startup (or from cache)
- NEVER modified
- Define base behavior + possible modifiers
```

### Layer 2: Relational DB (States - MUTABLE)

```
PostgreSQL / SQLite (YOUR CHOICE)

Tables:
├── sessions                 ← Conversation sessions
├── messages                 ← Message history
├── user_affinity            ← Affinity points per user/personality
├── session_moods            ← Current mood per session
├── user_facts               ← Learned facts about user
└── episodes                 ← Memorable episodes

Use:
- Constantly updated
- Persists between sessions
- Your CURRENT system (SQLite, JSON file, etc.) keeps working
- We only add new tables
```

### Layer 3: Vector DB (Semantic Search - OPTIONAL)

```
pgvector (PostgreSQL extension) / Pinecone

Tables:
└── message_embeddings       ← Vectors for semantic search

Use:
- OPTIONAL (only if you enable semantic search)
- Does NOT replace your current DB
- Is ADDITIONAL for "remember when..." queries
- If you don't use it, everything keeps working (without semantic search)
```

---

## 🔑 Final Answer to All Your Doubts

### 1. Does JSON get updated?
**NO. JSON is immutable. States in DB.**

### 2. Recompile each message?
**YES, but it's fast (~5ms). LLM is the slow part.**

### 3. Only persists during chat?
**NO. Persists PERMANENTLY in DB.**

### 4. How does it classify what goes to JSON?
**Nothing goes to JSON. States go to DB.**

### 5. Slower process?
**NO. Background tasks don't block (async).**

### 6. Parallel process with AI?
**YES. Fact extraction, mood detection, etc. are async.**

### 7. What happens to current JSON/SQLite?
**They keep working. We only add tables.**

### 8. Does vector DB replace current ones?
**NO. It's ADDITIONAL (only for semantic search).**

### 9. How does it retrieve memories?
**Multi-source: recent messages + facts + episodes + vector search.**

### 10. LLM memory?
**LuminoraCore ENRICHES the LLM context window with info from the past.**

---

## 📊 Persistence Summary Table

| Data | Where Defined | Where Persists | Mutable | Lifetime |
|------|---------------|----------------|---------|----------|
| **Base personality** | `alicia.json` | JSON file | ❌ NO | Permanent |
| **Possible levels** | `alicia.json` | JSON file | ❌ NO | Permanent |
| **Possible moods** | `alicia.json` | JSON file | ❌ NO | Permanent |
| **Current affinity** | - | DB (SQLite/PostgreSQL) | ✅ YES | Permanent |
| **Current mood** | - | DB + Cache (Redis) | ✅ YES | Session or permanent |
| **Messages** | - | DB (SQLite/PostgreSQL) | ✅ YES | Permanent |
| **Facts** | - | DB (SQLite/PostgreSQL) | ✅ YES | Permanent |
| **Episodes** | - | DB (SQLite/PostgreSQL) | ✅ YES | Permanent |
| **Embeddings** | - | Vector DB (pgvector/Pinecone) | ✅ YES | Permanent |
| **Compiled personality** | - | RAM (temporary, per request) | - | 1 request |

---

<div align="center">

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

