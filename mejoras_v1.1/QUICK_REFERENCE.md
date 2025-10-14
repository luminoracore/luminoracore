# Quick Reference - LuminoraCore v1.1

**Quick answers to the most common questions**

---

## 🎯 Model in One Sentence

> **LuminoraCore defines JSON Templates (shareable standard), runs Instances (state in DB), and exports Snapshots (JSON backup).**

---

## ❓ Frequently Asked Questions

### 1. Does personality JSON get updated?

**NO.** The template JSON is **immutable**.

```
Template (alicia.json)  → NEVER changes
State (PostgreSQL)      → YES, changes constantly
Snapshot (backup.json)  → Photo of state, doesn't change after export
```

---

### 2. Where does state persist?

**In DB** (your choice: SQLite, PostgreSQL, MongoDB, etc.)

```sql
-- Diego's state with Alicia
SELECT * FROM user_affinity WHERE user_id='diego';
→ affinity: 45, level: "friend"

SELECT * FROM session_moods WHERE session_id='session_123';
→ mood: "shy", intensity: 0.7

SELECT * FROM user_facts WHERE user_id='diego';
→ name: "Diego", favorite_anime: "Naruto"
```

---

### 3. Recompile with each message?

**YES, but takes only 5ms** (LLM takes 1500ms, compilation is irrelevant).

```
Compile: 5ms (0.3% of time)
LLM: 1500ms (99.7% of time)
```

---

### 4. Is it slower than v1.0?

**NO.** Only ~55ms overhead (3.5%), and heavy processing goes in background.

```
v1.0: 1500ms (only LLM)
v1.1: 1555ms (LLM + compilation + cache)
      + 400ms background (doesn't block)

User sees response just as fast
```

---

### 5. What happens to my current DBs?

**They keep working.** Only new tables are added.

```
Before (v1.0):
- sessions
- messages

After (v1.1):
- sessions ← No changes
- messages ← No changes
- user_affinity ← NEW
- user_facts ← NEW
- episodes ← NEW
- (optional: message_embeddings, session_moods)
```

---

### 6. Does vector DB replace SQLite/JSON?

**NO.** It's **additional** (only for semantic search).

```
SQLite/PostgreSQL → Stores messages, facts, episodes (ALWAYS)
pgvector/Pinecone → Only for semantic search (OPTIONAL)
```

You can use v1.1 without vector search ✅

---

### 7. How does it retrieve memories?

**Multi-source** (combines multiple sources):

```python
# User asks: "Remember when we talked about my dog?"

# System searches in parallel:
1. Recent messages (last 10) ← Always
2. User facts (pet_name="Max") ← If they exist
3. Episodes (search by tags) ← If they exist
4. Vector search (semantic similarity) ← If enabled

# Combines everything and sends to LLM
```

---

### 8. LLM memory or LuminoraCore memory?

**Both complement each other:**

```
LLM Context Window (short-term):
- Last 10-20 messages
- Fast, always available
- Limited to recent window

LuminoraCore Memory (long-term):
- All messages (unlimited)
- Facts, episodes, embeddings
- Search when needed

TOGETHER:
LLM receives: recent messages + relevant memory from LuminoraCore
```

---

### 9. How to export state?

**Snapshots** (exported JSON):

```python
# Export complete state
snapshot = await client.export_snapshot(session_id)

# Save
save_json("backup.json", snapshot)

# Import
new_session = await client.import_snapshot("backup.json")
# Restores exactly the saved state
```

---

### 10. Fits original value proposition?

**YES.** The JSON standard now covers:

1. **Templates** (v1.0) - How to define personalities
2. **Snapshots** (v1.1 new) - How to export states
3. **Instances** (v1.1 new) - How to execute personalities

**JSON is still the heart of the system.**

---

## 📊 Three Layers (Summary)

| | Template | Instance | Snapshot |
|---|----------|----------|----------|
| **What is it** | Blueprint | Live state | State photo |
| **Format** | JSON | DB | JSON |
| **Mutable** | ❌ | ✅ | ❌ |
| **Shareable** | ✅ | ❌ | ✅ |
| **Example** | alicia_base.json | affinity=45 in PostgreSQL | diego_backup.json |

---

## ✅ To Remember

### Template JSON Does NOT Update

```python
# ❌ NEVER
personality_json["affinity"] = 45
save(personality_json)

# ✅ ALWAYS
await db.update_affinity(session_id, 45)
```

### Compilation is Fast

```
Compile: 5ms ≈ Irrelevant
LLM: 1500ms ≈ 99% of time
```

### Background Tasks Don't Block

```python
# Foreground (blocks)
response = await llm.generate()  # 1500ms
return response  # User sees here ✅

# Background (doesn't block)
asyncio.create_task(extract_facts())  # 300ms async
# User does NOT wait for this
```

### Everything is Optional

```python
# You can enable only what you need
enable_moods = True              # ✅
enable_hierarchical = True       # ✅
enable_semantic_search = False   # ❌ Disabled
enable_episodic_memory = True    # ✅
```

---

## 🎯 Next Steps

1. **If you have conceptual doubts:** Read [`CONCEPTUAL_MODEL_REVISED.md`](./CONCEPTUAL_MODEL_REVISED.md)
2. **If you have performance doubts:** Read [`DATA_FLOW_AND_PERSISTENCE.md`](./DATA_FLOW_AND_PERSISTENCE.md)
3. **If you want to see code:** Read [`PERSONALITY_JSON_EXAMPLES.md`](./PERSONALITY_JSON_EXAMPLES.md)
4. **If you want to implement:** Read [`IMPLEMENTATION_PLAN.md`](./IMPLEMENTATION_PLAN.md)

---

<div align="center">

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

