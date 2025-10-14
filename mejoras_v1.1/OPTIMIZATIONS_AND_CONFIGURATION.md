# Optimizations and Configuration - LuminoraCore v1.1

**How to optimize costs, performance, and configure the ENTIRE system**

---

## ⚡ YOUR QUESTIONS ANSWERED

### 1. ✅ Batch Processing of Embeddings

**YES, it's BETTER and MUST be configurable.**

```python
# ════════════════════════════════════════════════════════
# CONFIGURATION (EVERYTHING in JSON or config)
# ════════════════════════════════════════════════════════

embedding_config = {
    "provider": "openai",  # openai, cohere, deepseek, local
    "model": "text-embedding-3-small",
    "batch_size": 10,  # ← CONFIGURABLE
    "batch_timeout": 30,  # seconds
    "enabled": True
}

# ════════════════════════════════════════════════════════
# SAVINGS
# ════════════════════════════════════════════════════════

# Without batch (1 call per message):
# 100 messages × $0.0001 × 1 call = $0.01
# Time: 100 × 100ms = 10,000ms (10 seconds)

# With batch of 10:
# 100 messages ÷ 10 batch × $0.0001 = $0.001
# Time: 10 batch × 150ms = 1,500ms (1.5 seconds)

# SAVINGS: 90% costs, 85% time ✅
```

---

### 2. ✅ Embedding Provider Configurability

**YES, it should be selectable based on what's compiled.**

```json
// In alicia.json (Template)
{
  "persona": {...},
  
  "memory_config": {
    "semantic_search": {
      "enabled": true,
      "embedding_provider": "openai",  // ← CONFIGURABLE
      "embedding_model": "text-embedding-3-small",
      "batch_processing": {
        "enabled": true,
        "batch_size": 10,  // ← CONFIGURABLE
        "batch_timeout_seconds": 30
      }
    }
  }
}
```

---

### 3. ✅ Where Embeddings and Sentiment are Saved

**In DB, NOT in JSON Template.**

```sql
-- Embeddings table
CREATE TABLE message_embeddings (
    id UUID PRIMARY KEY,
    message_id VARCHAR(255),
    embedding vector(1536),  -- pgvector
    created_at TIMESTAMP
);

-- Sentiment analysis table
CREATE TABLE sentiment_analysis (
    id UUID PRIMARY KEY,
    message_id VARCHAR(255),
    sentiment VARCHAR(50),  -- positive, negative, neutral
    intensity FLOAT,  -- 0-1
    emotions JSONB,  -- ["joy", "affection", ...]
    created_at TIMESTAMP
);
```

**Data is saved in DB, NOT in the JSON Template (which is immutable).**

---

### 4. ✅ Export (Snapshots) - VERY IMPORTANT

**YES, when you export, it includes ALL evolution from DB.**

```python
# ════════════════════════════════════════════════════════
# EXPORT SNAPSHOT (Template + DB State → JSON)
# ════════════════════════════════════════════════════════

snapshot = await client.export_snapshot(
    session_id="session_123",
    include_options={
        "conversation_history": True,  # Messages
        "facts": True,                 # Learned facts (from DB)
        "episodes": True,              # Episodes (from DB)
        "affinity_progression": True,  # Affinity history (from DB)
        "mood_history": True,          # Mood history (from DB)
        "embeddings": False,           # ⚠️ VERY heavy, better not
        "sentiment_data": True         # Sentiment analysis (from DB)
    }
)
```

**This Snapshot JSON is PORTABLE:**
- ✅ You can import it into another app
- ✅ You can share it
- ✅ You can migrate it to another LLM
- ✅ Contains ALL evolution

---

## 💰 Cost Comparison

### Option A: All Cloud APIs (❌ Expensive)

```python
# Per message:
# - Main LLM (DeepSeek cloud): $0.014 / message
# - Mood detection (DeepSeek cloud): $0.002 / message
# - Fact extraction (DeepSeek cloud): $0.003 / message
# - Sentiment (DeepSeek cloud): $0.001 / message
# - Embeddings (OpenAI): $0.0001 / message

# TOTAL: $0.0201 / message

# 1000 messages/day:
# $0.0201 × 1000 = $20.10 / day
# $20.10 × 30 = $603 / month ❌ EXPENSIVE
```

---

### Option B: Cloud Main + Local Processing (✅ Better)

```python
# Per message:
# - Main LLM (DeepSeek cloud): $0.014 / message
# - Mood detection (YOUR SERVER): $0 / message ✅
# - Fact extraction (YOUR SERVER): $0 / message ✅
# - Sentiment (YOUR SERVER): $0 / message ✅
# - Embeddings (OpenAI batch): $0.00001 / message ✅

# TOTAL: $0.01401 / message

# 1000 messages/day:
# $0.01401 × 1000 = $14.01 / day
# $14.01 × 30 = $420 / month

# SAVINGS: $603 - $420 = $183/month (30% savings) ✅
```

---

## 🎯 FINAL RECOMMENDATION

### Optimal Setup for You

```json
{
  "processing_config": {
    // Main LLM: DeepSeek Cloud (conversations)
    "main_llm": {
      "provider": "deepseek",
      "endpoint": "https://api.deepseek.com/v1",
      "model": "deepseek-chat"
    },
    
    // Processing LLM: YOUR LOCAL SERVER ✅
    "processing_llm": {
      "provider": "deepseek-local",
      "endpoint": "http://localhost:8000/v1",
      "model": "deepseek-r1-distill-llama-8b"
    },
    
    // Embeddings: Batch with OpenAI ✅
    "embedding_provider": {
      "provider": "openai",
      "model": "text-embedding-3-small",
      "batch_processing": {
        "enabled": true,
        "batch_size": 10,
        "batch_timeout": 30
      }
    }
  }
}
```

**Costs:**
- Main LLM (cloud): $14/day
- Processing LLM (local): $0/day ✅
- Embeddings (batch): $0.10/day ✅
- **Total: ~$420/month** (vs $603 without optimization)

**Performance:**
- User: 1555ms (identical to v1.0)
- Background: 150ms average
- Total: No visible impact ✅

---

<div align="center">

**Everything is configurable. Everything is optimizable. Speed is NOT a problem.**

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

