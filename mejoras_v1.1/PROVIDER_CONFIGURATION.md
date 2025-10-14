# Provider Configuration - LuminoraCore v1.1

**Completely agnostic system: EVERYTHING configurable, NOTHING hardcoded**

---

## ⚠️ FUNDAMENTAL PRINCIPLE

**If you use DeepSeek → EVERYTHING uses DeepSeek**
**If you use Claude → EVERYTHING uses Claude**
**If you use PostgreSQL → EVERYTHING uses PostgreSQL**

**NOTHING can be hardcoded to a specific provider.**

---

## 🎯 Abstracted Provider Architecture

### Concept: Complete Abstraction

```
┌─────────────────────────────────────────┐
│      LUMINORACORE CORE                  │
│      (Provider-agnostic)                │
│                                         │
│  - Personality System                   │
│  - Memory System                        │
│  - Relationship System                  │
│                                         │
│  Does NOT know which specific LLM/DB    │
└────────────┬────────────────────────────┘
             │
             │ Uses abstract interfaces
             ▼
┌─────────────────────────────────────────┐
│      PROVIDER LAYER (Adapters)          │
│                                         │
│  LLMProvider (abstract)                 │
│  ├─ DeepSeekProvider                    │
│  ├─ OpenAIProvider                      │
│  ├─ ClaudeProvider                      │
│  ├─ MistralProvider                     │
│  └─ CohereProvider                      │
│                                         │
│  EmbeddingProvider (abstract)           │
│  ├─ DeepSeekEmbeddings                  │
│  ├─ OpenAIEmbeddings                    │
│  ├─ CohereEmbeddings                    │
│  └─ LocalEmbeddings (sentence-trans)    │
│                                         │
│  StorageProvider (abstract)             │
│  ├─ PostgreSQLProvider                  │
│  ├─ SQLiteProvider                      │
│  ├─ DynamoDBProvider                    │
│  └─ MongoDBProvider                     │
│                                         │
│  VectorStoreProvider (abstract)         │
│  ├─ PgVectorProvider (PostgreSQL)       │
│  ├─ PineconeProvider                    │
│  ├─ WeaviateProvider                    │
│  └─ ChromaDBProvider (local)            │
└─────────────────────────────────────────┘
```

---

## 📝 Complete Configuration in JSON

### Example: DeepSeek + PostgreSQL + pgvector

```json
// config/luminora_config.json
{
  // ════════════════════════════════════════════════════
  // LLM PROVIDER (EVERYTHING uses the same)
  // ════════════════════════════════════════════════════
  
  "llm_provider": {
    "name": "deepseek",  // ← This defines EVERYTHING
    "config": {
      "api_base": "https://api.deepseek.com/v1",
      "api_key_env": "DEEPSEEK_API_KEY",  // Environment variable
      
      // Specific models for each task
      "models": {
        "main": "deepseek-chat",           // Main conversation
        "processing": "deepseek-chat",     // Background processing
        "embeddings": "deepseek-jina-embeddings-v3"  // ← DeepSeek has embeddings!
      },
      
      // Configuration per task
      "task_configs": {
        "conversation": {
          "model": "deepseek-chat",
          "max_tokens": 2000,
          "temperature": 0.8
        },
        "mood_detection": {
          "model": "deepseek-chat",
          "max_tokens": 50,
          "temperature": 0.3
        },
        "fact_extraction": {
          "model": "deepseek-chat",
          "max_tokens": 200,
          "temperature": 0.1
        }
      }
    }
  },
  
  // ════════════════════════════════════════════════════
  // STORAGE PROVIDER (Relational DB)
  // ════════════════════════════════════════════════════
  
  "storage_provider": {
    "name": "postgresql",  // ← This defines which DB
    "config": {
      "connection": {
        "host": "localhost",
        "port": 5432,
        "database": "luminora",
        "user": "luminora_user",
        "password_env": "DB_PASSWORD"  // Environment variable
      },
      
      "pool": {
        "min_connections": 2,
        "max_connections": 20
      },
      
      "migrations": {
        "auto_migrate": true,  // Create tables automatically
        "scripts_path": "luminoracore/storage/postgresql/migrations/"
      }
    }
  },
  
  // ════════════════════════════════════════════════════
  // VECTOR STORE PROVIDER (Semantic search)
  // ════════════════════════════════════════════════════
  
  "vector_store_provider": {
    "name": "pgvector",  // Uses PostgreSQL extension
    "config": {
      "connection": "use_storage_provider",  // Same connection
      "dimension": 1024,  // DeepSeek embedding dimension
      "index_type": "ivfflat",
      "lists": 100
    }
  }
}
```

---

## 🔌 Provider Adapters (Abstract Interfaces)

### LLM Provider Interface

```python
# luminoracore/providers/llm/base.py

from abc import ABC, abstractmethod
from typing import List, Dict

class LLMProvider(ABC):
    """Abstract interface for ANY LLM provider"""
    
    @abstractmethod
    async def generate(
        self,
        messages: List[Dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """Generate response (ANY LLM must implement this)"""
        pass

# ════════════════════════════════════════════════════════
# SPECIFIC IMPLEMENTATIONS
# ════════════════════════════════════════════════════════

# luminoracore/providers/llm/deepseek.py
class DeepSeekProvider(LLMProvider):
    """Provider for DeepSeek"""
    
    def __init__(self, config: dict):
        self.api_base = config["api_base"]
        self.api_key = os.getenv(config["api_key_env"])
        self.client = OpenAI(  # DeepSeek uses OpenAI-compatible API
            api_key=self.api_key,
            base_url=self.api_base
        )
    
    async def generate(self, messages, model, **kwargs):
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content


# luminoracore/providers/llm/claude.py
class ClaudeProvider(LLMProvider):
    """Provider for Claude (Anthropic)"""
    
    def __init__(self, config: dict):
        self.api_key = os.getenv(config["api_key_env"])
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    async def generate(self, messages, model, **kwargs):
        response = await self.client.messages.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response.content[0].text


# ════════════════════════════════════════════════════════
# FACTORY (Creates the correct provider based on config)
# ════════════════════════════════════════════════════════

def create_llm_provider(config: dict) -> LLMProvider:
    """Factory that creates the correct provider"""
    
    provider_name = config["name"]  # From JSON!
    
    providers = {
        "deepseek": DeepSeekProvider,
        "openai": OpenAIProvider,
        "claude": ClaudeProvider,
        "mistral": MistralProvider,
        "ollama": OllamaProvider  # Local
    }
    
    if provider_name not in providers:
        raise ValueError(f"Unknown provider: {provider_name}")
    
    return providers[provider_name](config["config"])
```

---

## 🛠️ CLI for Setup

### Interactive Command

```bash
# ════════════════════════════════════════════════════════
# INTERACTIVE SETUP WITH CLI
# ════════════════════════════════════════════════════════

$ luminora-cli init

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  LuminoraCore v1.1 - Setup Wizard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/5] LLM Provider Configuration

? Select your LLM provider: 
  > DeepSeek
    OpenAI
    Claude
    Mistral
    Ollama (Local)

✓ Selected: DeepSeek

? DeepSeek API Key (or env var): 
> DEEPSEEK_API_KEY

? Use same provider for background processing? (Y/n)
> Y

✓ LLM Provider configured: DeepSeek

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[2/5] Embedding Provider Configuration

? Use DeepSeek for embeddings too? (Y/n)
> Y

? Enable batch processing? (Y/n)
> Y

✓ Embedding Provider configured: DeepSeek (batch=10)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[3/5] Storage Provider Configuration

? Select your database:
  SQLite (Simple, for development)
  > PostgreSQL (Recommended for production)
    MySQL
    DynamoDB

✓ Selected: PostgreSQL

? Test connection now? (Y/n)
> Y

⏳ Testing connection...
✓ Connection successful!

? Create tables automatically? (Y/n)
> Y

⏳ Running migrations...
  ✓ 001_initial_schema.sql
  ✓ 002_add_affinity_tables.sql
  ✓ 003_add_memory_tables.sql
  
✓ Database initialized!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Setup Complete!

Your Configuration:
  LLM:        DeepSeek (all tasks)
  Embeddings: DeepSeek Jina (1024 dims, batch=10)
  Storage:    PostgreSQL (luminora@localhost)
  Vectors:    pgvector (1024 dims)

Ready to use! Run:
  python your_app.py
```

---

## 🎯 FINAL SUMMARY

### Everything is Configurable ✅

| Component | Configuration | Location |
|-----------|---------------|----------|
| **Main LLM** | config.llm_provider | JSON |
| **Processing LLM** | config.llm_provider.models.processing | JSON |
| **Embeddings** | config.embedding_provider | JSON |
| **Batch size** | config.embedding_provider.batch_size | JSON |
| **Storage** | config.storage_provider | JSON |
| **Vector store** | config.vector_store_provider | JSON |

**NOTHING hardcoded** ✅

---

<div align="center">

**✅ EVERYTHING CONFIGURABLE. NOTHING HARDCODED. PROVIDERS ABSTRACTED.**

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

