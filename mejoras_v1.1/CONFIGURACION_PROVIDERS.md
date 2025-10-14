# Configuración de Providers - LuminoraCore v1.1

**Sistema completamente agnóstico: TODO configurable, NADA hardcoded**

---

## ⚠️ PRINCIPIO FUNDAMENTAL

**Si usas DeepSeek → TODO usa DeepSeek**
**Si usas Claude → TODO usa Claude**
**Si usas PostgreSQL → TODO usa PostgreSQL**

**NADA puede estar hardcoded a un provider específico.**

---

## 🎯 Arquitectura de Providers Abstraídos

### Concepto: Abstracción Completa

```
┌─────────────────────────────────────────┐
│      LUMINORACORE CORE                  │
│      (Provider-agnostic)                │
│                                         │
│  - Personality System                   │
│  - Memory System                        │
│  - Relationship System                  │
│                                         │
│  NO sabe qué LLM/BBDD específico usa    │
└────────────┬────────────────────────────┘
             │
             │ Usa interfaces abstractas
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
│  ├─ VoyageEmbeddings                    │
│  └─ LocalEmbeddings (sentence-trans)    │
│                                         │
│  StorageProvider (abstract)             │
│  ├─ PostgreSQLProvider                  │
│  ├─ SQLiteProvider                      │
│  ├─ DynamoDBProvider                    │
│  ├─ MongoDBProvider                     │
│  └─ RedisProvider                       │
│                                         │
│  VectorStoreProvider (abstract)         │
│  ├─ PgVectorProvider (PostgreSQL)       │
│  ├─ PineconeProvider                    │
│  ├─ WeaviateProvider                    │
│  ├─ QdrantProvider                      │
│  └─ ChromaDBProvider (local)            │
└─────────────────────────────────────────┘
```

---

## 📝 Configuración Completa en JSON

### Ejemplo: DeepSeek + PostgreSQL + pgvector

```json
// config/luminora_config.json (O en alicia.json directamente)
{
  // ════════════════════════════════════════════════════
  // LLM PROVIDER (TODO usa el mismo)
  // ════════════════════════════════════════════════════
  
  "llm_provider": {
    "name": "deepseek",  // ← Esto define TODO
    "config": {
      "api_base": "https://api.deepseek.com/v1",
      "api_key_env": "DEEPSEEK_API_KEY",  // Variable de entorno
      
      // Modelos específicos para cada tarea
      "models": {
        "main": "deepseek-chat",           // Conversación principal
        "processing": "deepseek-chat",     // Background processing
        "embeddings": "deepseek-jina-embeddings-v3"  // ← DeepSeek tiene embeddings!
      },
      
      // Configuración por tarea
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
        },
        "sentiment_analysis": {
          "model": "deepseek-chat",
          "max_tokens": 100,
          "temperature": 0.2
        }
      }
    }
  },
  
  // ════════════════════════════════════════════════════
  // STORAGE PROVIDER (BBDD relacional)
  // ════════════════════════════════════════════════════
  
  "storage_provider": {
    "name": "postgresql",  // ← Esto define qué BBDD
    "config": {
      "connection": {
        "host": "localhost",
        "port": 5432,
        "database": "luminora",
        "user": "luminora_user",
        "password_env": "DB_PASSWORD"  // Variable de entorno
      },
      
      "pool": {
        "min_connections": 2,
        "max_connections": 20
      },
      
      "migrations": {
        "auto_migrate": true,  // Crear tablas automáticamente
        "scripts_path": "luminoracore/storage/postgresql/migrations/"
      }
    }
  },
  
  // ════════════════════════════════════════════════════
  // VECTOR STORE PROVIDER (Búsqueda semántica)
  // ════════════════════════════════════════════════════
  
  "vector_store_provider": {
    "name": "pgvector",  // Usa extensión de PostgreSQL
    "config": {
      "connection": "use_storage_provider",  // Misma conexión
      "dimension": 1024,  // Dimensión de embeddings de DeepSeek
      "index_type": "ivfflat",
      "lists": 100
    }
  },
  
  // ════════════════════════════════════════════════════
  // OPTIMIZACIONES
  // ════════════════════════════════════════════════════
  
  "optimizations": {
    "batch_processing": {
      "embeddings": {
        "enabled": true,
        "batch_size": 10,
        "timeout_seconds": 30
      }
    },
    "selective_processing": {
      "enabled": true,
      "episode_check_frequency": 5
    },
    "caching": {
      "enabled": true,
      "backend": "redis",
      "redis_url_env": "REDIS_URL"
    }
  }
}
```

---

## 🔌 Provider Adapters (Interfaces Abstractas)

### LLM Provider Interface

```python
# luminoracore/providers/llm/base.py

from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class LLMProvider(ABC):
    """Interfaz abstracta para ANY LLM provider"""
    
    @abstractmethod
    async def generate(
        self,
        messages: List[Dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """Genera respuesta (CUALQUIER LLM debe implementar esto)"""
        pass
    
    @abstractmethod
    async def generate_json(
        self,
        messages: List[Dict],
        model: str,
        **kwargs
    ) -> dict:
        """Genera respuesta en formato JSON"""
        pass


# ════════════════════════════════════════════════════════
# IMPLEMENTACIONES ESPECÍFICAS
# ════════════════════════════════════════════════════════

# luminoracore/providers/llm/deepseek.py
class DeepSeekProvider(LLMProvider):
    """Provider para DeepSeek"""
    
    def __init__(self, config: dict):
        self.api_base = config["api_base"]
        self.api_key = os.getenv(config["api_key_env"])
        self.client = OpenAI(  # DeepSeek usa API compatible con OpenAI
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
    """Provider para Claude (Anthropic)"""
    
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


# luminoracore/providers/llm/openai.py
class OpenAIProvider(LLMProvider):
    """Provider para OpenAI"""
    
    def __init__(self, config: dict):
        self.api_key = os.getenv(config["api_key_env"])
        self.client = OpenAI(api_key=self.api_key)
    
    async def generate(self, messages, model, **kwargs):
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content


# ════════════════════════════════════════════════════════
# FACTORY (Crea el provider correcto según config)
# ════════════════════════════════════════════════════════

def create_llm_provider(config: dict) -> LLMProvider:
    """Factory que crea el provider correcto"""
    
    provider_name = config["name"]  # Del JSON!
    
    providers = {
        "deepseek": DeepSeekProvider,
        "openai": OpenAIProvider,
        "claude": ClaudeProvider,
        "mistral": MistralProvider,
        "cohere": CohereProvider,
        "groq": GroqProvider,
        "ollama": OllamaProvider  # Local
    }
    
    if provider_name not in providers:
        raise ValueError(f"Unknown provider: {provider_name}")
    
    return providers[provider_name](config["config"])
```

---

## 🔍 Embedding Provider Interface

```python
# luminoracore/providers/embeddings/base.py

class EmbeddingProvider(ABC):
    """Interfaz abstracta para ANY embedding provider"""
    
    @abstractmethod
    async def create_embedding(self, text: str) -> List[float]:
        """Crea embedding para un texto"""
        pass
    
    @abstractmethod
    async def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Crea embeddings en batch (más eficiente)"""
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """Dimensión del embedding (ej: 1536, 1024, etc.)"""
        pass


# ════════════════════════════════════════════════════════
# IMPLEMENTACIONES
# ════════════════════════════════════════════════════════

# DeepSeek (usa Jina embeddings)
class DeepSeekEmbeddingProvider(EmbeddingProvider):
    def __init__(self, config: dict):
        self.api_base = config["api_base"]
        self.api_key = os.getenv(config["api_key_env"])
        self.model = config["models"]["embeddings"]  # deepseek-jina-embeddings-v3
        self.dimension = 1024  # DeepSeek Jina: 1024 dims
    
    async def create_embeddings_batch(self, texts: List[str]):
        response = await httpx.post(
            f"{self.api_base}/embeddings",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "input": texts  # ← Batch
            }
        )
        return [item["embedding"] for item in response.json()["data"]]
    
    def get_dimension(self) -> int:
        return 1024  # DeepSeek


# OpenAI
class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, config: dict):
        self.client = OpenAI(api_key=os.getenv(config["api_key_env"]))
        self.model = config["models"]["embeddings"]
        self.dimension = 1536  # OpenAI
    
    async def create_embeddings_batch(self, texts: List[str]):
        response = await self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]
    
    def get_dimension(self) -> int:
        return 1536  # OpenAI


# Cohere
class CohereEmbeddingProvider(EmbeddingProvider):
    def __init__(self, config: dict):
        self.client = cohere.Client(os.getenv(config["api_key_env"]))
        self.model = config["models"]["embeddings"]
        self.dimension = 1024  # Cohere embed-v3
    
    async def create_embeddings_batch(self, texts: List[str]):
        response = await self.client.embed(
            texts=texts,
            model=self.model,
            input_type="search_document"
        )
        return response.embeddings
    
    def get_dimension(self) -> int:
        return 1024


# Local (Sentence Transformers)
class LocalEmbeddingProvider(EmbeddingProvider):
    def __init__(self, config: dict):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(config["model"])
        self.dimension = self.model.get_sentence_embedding_dimension()
    
    async def create_embeddings_batch(self, texts: List[str]):
        # Local, muy rápido, GRATIS
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
    
    def get_dimension(self) -> int:
        return self.dimension  # Depende del modelo (384, 768, 1024)
```

---

## 💾 Storage Provider Interface

```python
# luminoracore/storage/base.py

class StorageProvider(ABC):
    """Interfaz abstracta para ANY database"""
    
    @abstractmethod
    async def connect(self):
        """Conectar a BBDD"""
        pass
    
    @abstractmethod
    async def initialize_schema(self):
        """Crear tablas (ejecutar migrations)"""
        pass
    
    @abstractmethod
    async def save_message(self, session_id: str, message: dict):
        """Guardar mensaje"""
        pass
    
    @abstractmethod
    async def get_affinity(self, user_id: str, personality: str) -> int:
        """Obtener affinity"""
        pass
    
    # ... etc para cada operación


# ════════════════════════════════════════════════════════
# IMPLEMENTACIONES
# ════════════════════════════════════════════════════════

# PostgreSQL
class PostgreSQLProvider(StorageProvider):
    def __init__(self, config: dict):
        self.config = config
        self.pool = None
    
    async def connect(self):
        self.pool = await asyncpg.create_pool(
            host=self.config["host"],
            port=self.config["port"],
            database=self.config["database"],
            user=self.config["user"],
            password=os.getenv(self.config["password_env"])
        )
    
    async def initialize_schema(self):
        """Ejecuta migrations de PostgreSQL"""
        migrations = load_sql_files(
            "luminoracore/storage/postgresql/migrations/"
        )
        for migration in migrations:
            await self.pool.execute(migration)
    
    async def save_message(self, session_id, message):
        await self.pool.execute(
            """
            INSERT INTO messages (session_id, speaker, content, timestamp)
            VALUES ($1, $2, $3, $4)
            """,
            session_id, message["speaker"], message["content"], datetime.now()
        )


# SQLite
class SQLiteProvider(StorageProvider):
    def __init__(self, config: dict):
        self.db_path = config["database_path"]
        self.conn = None
    
    async def connect(self):
        self.conn = await aiosqlite.connect(self.db_path)
    
    async def initialize_schema(self):
        """Ejecuta migrations de SQLite"""
        migrations = load_sql_files(
            "luminoracore/storage/sqlite/migrations/"
        )
        for migration in migrations:
            await self.conn.execute(migration)
    
    async def save_message(self, session_id, message):
        await self.conn.execute(
            """
            INSERT INTO messages (session_id, speaker, content, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (session_id, message["speaker"], message["content"], datetime.now())
        )


# DynamoDB
class DynamoDBProvider(StorageProvider):
    def __init__(self, config: dict):
        self.client = boto3.client(
            'dynamodb',
            region_name=config["region"],
            aws_access_key_id=os.getenv(config["access_key_env"]),
            aws_secret_access_key=os.getenv(config["secret_key_env"])
        )
        self.table_prefix = config.get("table_prefix", "luminora_")
    
    async def connect(self):
        # Verificar conexión
        await self.client.list_tables()
    
    async def initialize_schema(self):
        """Crea tablas en DynamoDB"""
        tables = [
            {
                "TableName": f"{self.table_prefix}messages",
                "KeySchema": [...],
                "AttributeDefinitions": [...],
                "BillingMode": "PAY_PER_REQUEST"
            },
            # ... otras tablas
        ]
        
        for table_def in tables:
            try:
                await self.client.create_table(**table_def)
            except self.client.exceptions.ResourceInUseException:
                # Tabla ya existe
                pass
    
    async def save_message(self, session_id, message):
        await self.client.put_item(
            TableName=f"{self.table_prefix}messages",
            Item={
                "session_id": {"S": session_id},
                "message_id": {"S": message["id"]},
                "content": {"S": message["content"]},
                "timestamp": {"N": str(int(time.time()))}
            }
        )
```

---

## 📁 Estructura de Migrations (Scripts SQL)

### Organización por BBDD

```
luminoracore/
└── storage/
    ├── postgresql/
    │   └── migrations/
    │       ├── 001_initial_schema.sql
    │       ├── 002_add_affinity_tables.sql
    │       ├── 003_add_memory_tables.sql
    │       ├── 004_add_pgvector_extension.sql
    │       └── 005_add_indexes.sql
    │
    ├── sqlite/
    │   └── migrations/
    │       ├── 001_initial_schema.sql
    │       ├── 002_add_affinity_tables.sql
    │       ├── 003_add_memory_tables.sql
    │       └── 004_add_indexes.sql
    │
    ├── mysql/
    │   └── migrations/
    │       ├── 001_initial_schema.sql
    │       └── ...
    │
    └── dynamodb/
        └── schemas/
            ├── messages_table.json
            ├── user_affinity_table.json
            └── ...
```

---

### Ejemplo: PostgreSQL Migration

```sql
-- luminoracore/storage/postgresql/migrations/001_initial_schema.sql

-- ════════════════════════════════════════════════════════
-- TABLAS BÁSICAS (v1.0 + v1.1)
-- ════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    personality_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_activity TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES sessions(session_id),
    speaker VARCHAR(50) NOT NULL,  -- 'user' | 'assistant'
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS user_affinity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    personality_name VARCHAR(255) NOT NULL,
    affinity_points INTEGER DEFAULT 0,
    current_level VARCHAR(50) DEFAULT 'stranger',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, personality_name)
);

CREATE TABLE IF NOT EXISTS user_facts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    key VARCHAR(255) NOT NULL,
    value JSONB NOT NULL,
    confidence FLOAT DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, category, key)
);

CREATE TABLE IF NOT EXISTS episodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    session_id UUID REFERENCES sessions(session_id),
    type VARCHAR(50) NOT NULL,
    title VARCHAR(500) NOT NULL,
    summary TEXT NOT NULL,
    importance FLOAT NOT NULL,
    sentiment VARCHAR(50) NOT NULL,
    tags TEXT[],
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_messages_session ON messages(session_id);
CREATE INDEX idx_affinity_user ON user_affinity(user_id);
CREATE INDEX idx_facts_user ON user_facts(user_id);
CREATE INDEX idx_episodes_user ON episodes(user_id);
```

---

### Ejemplo: SQLite Migration

```sql
-- luminoracore/storage/sqlite/migrations/001_initial_schema.sql

-- ════════════════════════════════════════════════════════
-- SQLite Version (Sintaxis ligeramente diferente)
-- ════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    personality_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    speaker TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

CREATE TABLE IF NOT EXISTS user_affinity (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    personality_name TEXT NOT NULL,
    affinity_points INTEGER DEFAULT 0,
    current_level TEXT DEFAULT 'stranger',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, personality_name)
);

-- ... más tablas con sintaxis SQLite
```

---

### Ejemplo: pgvector Migration

```sql
-- luminoracore/storage/postgresql/migrations/004_add_pgvector_extension.sql

-- ════════════════════════════════════════════════════════
-- EXTENSIÓN PGVECTOR (Solo PostgreSQL)
-- ════════════════════════════════════════════════════════

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS message_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID NOT NULL REFERENCES messages(id),
    embedding vector(1024),  -- ← Dimensión según provider (DeepSeek=1024, OpenAI=1536)
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índice para búsqueda vectorial
CREATE INDEX IF NOT EXISTS idx_message_embeddings_vector 
ON message_embeddings 
USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 100);
```

---

## 🛠️ CLI para Setup

### Comando Interactivo

```bash
# ════════════════════════════════════════════════════════
# SETUP INTERACTIVO CON CLI
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
    Cohere
    Groq
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

? Batch size (5-20 recommended):
> 10

? Batch timeout (seconds):
> 30

✓ Embedding Provider configured: DeepSeek (batch=10)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[3/5] Storage Provider Configuration

? Select your database:
  SQLite (Simple, for development)
  > PostgreSQL (Recommended for production)
    MySQL
    MongoDB
    DynamoDB

✓ Selected: PostgreSQL

? PostgreSQL connection details:
  Host: localhost
  Port: 5432
  Database: luminora
  User: luminora_user
  Password (env var): DB_PASSWORD

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

[4/5] Vector Store Configuration

? Enable semantic search? (Y/n)
> Y

? Select vector store:
  > pgvector (Use PostgreSQL extension)
    Pinecone (Cloud)
    Weaviate (Self-hosted)
    Qdrant (Self-hosted)
    ChromaDB (Local)

✓ Selected: pgvector

? Install pgvector extension now? (Y/n)
> Y

⏳ Installing pgvector extension...
✓ Extension installed!

⏳ Creating vector tables...
✓ message_embeddings table created!
✓ Vector index created!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[5/5] Cache Configuration (Optional)

? Enable caching for performance? (Y/n)
> Y

? Select cache backend:
  > Redis
    Memcached
    Memory (No external cache)

✓ Selected: Redis

? Redis URL (env var):
> REDIS_URL

? Test connection? (Y/n)
> Y

⏳ Testing Redis connection...
✓ Redis connected!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Setup Complete!

Configuration saved to: config/luminora.json

┌─────────────────────────────────────────────────┐
│ Your Configuration:                             │
│                                                 │
│ LLM:        DeepSeek (all tasks)                │
│ Embeddings: DeepSeek Jina (batch=10)            │
│ Database:   PostgreSQL (localhost)              │
│ Vector DB:  pgvector                            │
│ Cache:      Redis                               │
└─────────────────────────────────────────────────┘

Next steps:
  1. Set environment variables:
     export DEEPSEEK_API_KEY="your-key"
     export DB_PASSWORD="your-password"
     export REDIS_URL="redis://localhost:6379"
  
  2. Test the setup:
     luminora-cli test-connection
  
  3. Load a personality:
     luminora-cli load-personality alicia.json
  
  4. Start coding! 🚀
```

---

## 🔧 Archivo de Configuración Generado

```json
// config/luminora.json (Generado por CLI)
{
  "version": "1.1.0",
  "created_at": "2025-10-14T20:00:00Z",
  
  // ════════════════════════════════════════════════════
  // LLM PROVIDER (TODO DeepSeek)
  // ════════════════════════════════════════════════════
  
  "llm_provider": {
    "name": "deepseek",
    "config": {
      "api_base": "https://api.deepseek.com/v1",
      "api_key_env": "DEEPSEEK_API_KEY",
      "models": {
        "main": "deepseek-chat",
        "processing": "deepseek-chat",
        "embeddings": "deepseek-jina-embeddings-v3"
      }
    }
  },
  
  // ════════════════════════════════════════════════════
  // EMBEDDING PROVIDER (DeepSeek)
  // ════════════════════════════════════════════════════
  
  "embedding_provider": {
    "name": "deepseek",
    "dimension": 1024,  // ← Auto-detectado
    "batch_processing": {
      "enabled": true,
      "batch_size": 10,
      "timeout_seconds": 30
    }
  },
  
  // ════════════════════════════════════════════════════
  // STORAGE PROVIDER (PostgreSQL)
  // ════════════════════════════════════════════════════
  
  "storage_provider": {
    "name": "postgresql",
    "config": {
      "host": "localhost",
      "port": 5432,
      "database": "luminora",
      "user": "luminora_user",
      "password_env": "DB_PASSWORD"
    },
    "migrations": {
      "auto_migrate": true,
      "path": "luminoracore/storage/postgresql/migrations/"
    }
  },
  
  // ════════════════════════════════════════════════════
  // VECTOR STORE (pgvector)
  // ════════════════════════════════════════════════════
  
  "vector_store_provider": {
    "name": "pgvector",
    "config": {
      "use_storage_connection": true,  // Usa misma conexión PostgreSQL
      "dimension": 1024,  // Según embedding provider
      "index_type": "ivfflat"
    }
  },
  
  // ════════════════════════════════════════════════════
  // CACHE (Redis)
  // ════════════════════════════════════════════════════
  
  "cache_provider": {
    "name": "redis",
    "config": {
      "url_env": "REDIS_URL",
      "ttl_defaults": {
        "personality": 3600,
        "context": 300,
        "embeddings": 86400
      }
    }
  }
}
```

---

## ✅ Testing de Conexiones

### CLI Testing Command

```bash
# ════════════════════════════════════════════════════════
# PROBAR TODAS LAS CONEXIONES
# ════════════════════════════════════════════════════════

$ luminora-cli test-connection

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Testing Connections
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/5] Testing LLM Provider (DeepSeek)
⏳ Connecting to https://api.deepseek.com/v1...
⏳ Sending test request...
✓ DeepSeek API working! (latency: 245ms)

[2/5] Testing Embedding Provider (DeepSeek)
⏳ Creating test embedding...
✓ Embeddings working! (dimension: 1024, latency: 89ms)

[3/5] Testing Database (PostgreSQL)
⏳ Connecting to localhost:5432...
✓ Connection established!
⏳ Checking tables...
✓ All tables present!
⏳ Running test query...
✓ Database working!

[4/5] Testing Vector Store (pgvector)
⏳ Checking pgvector extension...
✓ Extension installed!
⏳ Testing vector search...
✓ Vector search working!

[5/5] Testing Cache (Redis)
⏳ Connecting to Redis...
✓ Redis connected!
⏳ Testing read/write...
✓ Cache working!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ All Connections Working!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Performance Summary:
  LLM latency:        245ms
  Embedding latency:  89ms
  Database latency:   12ms
  Cache latency:      2ms

Your setup is ready! 🚀
```

---

## 🎯 Ejemplo: Setup para DeepSeek + PostgreSQL

### Paso 1: Crear Config

```bash
$ luminora-cli init --interactive

# O manual:
$ cat > config/luminora.json << EOF
{
  "llm_provider": {"name": "deepseek", ...},
  "storage_provider": {"name": "postgresql", ...}
}
EOF
```

### Paso 2: Configurar Variables de Entorno

```bash
# .env
DEEPSEEK_API_KEY=sk-your-key-here
DB_PASSWORD=your-db-password
REDIS_URL=redis://localhost:6379
```

### Paso 3: Inicializar BBDD

```bash
# Crear BBDD
$ createdb luminora

# Ejecutar migrations
$ luminora-cli migrate --database postgresql

⏳ Running PostgreSQL migrations...
  ✓ 001_initial_schema.sql
  ✓ 002_add_affinity_tables.sql
  ✓ 003_add_memory_tables.sql
  ✓ 004_add_pgvector_extension.sql
  ✓ 005_add_indexes.sql

✓ Database initialized!
```

### Paso 4: Probar

```bash
$ luminora-cli test-connection

✓ All connections working!
```

### Paso 5: Usar

```python
from luminoracore import LuminoraCoreClient

# Carga config automáticamente desde config/luminora.json
client = LuminoraCoreClient.from_config("config/luminora.json")

# TODO está configurado según el JSON:
# - DeepSeek para LLM
# - DeepSeek para embeddings
# - PostgreSQL para storage
# - pgvector para vector search

session = await client.create_session(
    personality="alicia.json",
    user_id="diego"
)

response = await client.send_message(session, "Hola")
# ✓ Funciona!
```

---

## 📊 Comparación de Setups

### Setup A: DeepSeek + PostgreSQL + pgvector

```json
{
  "llm_provider": {"name": "deepseek"},
  "embedding_provider": {"name": "deepseek"},  // Usa Jina embeddings
  "storage_provider": {"name": "postgresql"},
  "vector_store_provider": {"name": "pgvector"}
}
```

**Ventajas:**
- ✅ Todo DeepSeek (consistente)
- ✅ Embeddings 1024-dim
- ✅ pgvector integrado en PostgreSQL
- ✅ Performance excelente

**Costos:**
- DeepSeek API: ~$420/mes
- PostgreSQL: $0 (local) o $50-150/mes (cloud)

---

### Setup B: DeepSeek + SQLite (Mobile)

```json
{
  "llm_provider": {"name": "deepseek"},
  "embedding_provider": {"name": "local"},  // Sentence transformers
  "storage_provider": {"name": "sqlite"},
  "vector_store_provider": {"name": "chromadb"}  // Vector DB local
}
```

**Ventajas:**
- ✅ Todo local (app móvil)
- ✅ Sin servidores externos
- ✅ Offline-capable (excepto LLM)

**Costos:**
- DeepSeek API: ~$420/mes
- Storage: $0 (local)

---

### Setup C: Claude + DynamoDB (AWS)

```json
{
  "llm_provider": {"name": "claude"},
  "embedding_provider": {"name": "voyage"},  // Voyage AI (embeddings)
  "storage_provider": {"name": "dynamodb"},
  "vector_store_provider": {"name": "pinecone"}
}
```

**Ventajas:**
- ✅ Todo en cloud (AWS ecosystem)
- ✅ Escalable
- ✅ Serverless

**Costos:**
- Claude API: ~$800/mes
- DynamoDB: Pay-per-request
- Pinecone: $70/mes

---

## 🎯 Sistema de Dimensiones Dinámicas

### Problema: Cada provider tiene dimensiones diferentes

```
OpenAI text-embedding-3-small: 1536 dims
DeepSeek Jina v3: 1024 dims
Cohere embed-v3: 1024 dims
Voyage AI: 1024 dims
Local (all-MiniLM): 384 dims
```

### Solución: Auto-detect y adaptar

```python
# luminoracore/providers/embeddings/manager.py

class EmbeddingManager:
    """Gestiona embeddings con auto-detección de dimensiones"""
    
    def __init__(self, config: dict):
        # Crear provider según config
        self.provider = create_embedding_provider(config)
        
        # Auto-detectar dimensión
        self.dimension = self.provider.get_dimension()
        
        print(f"✓ Embedding provider: {config['name']}")
        print(f"✓ Dimension: {self.dimension}")
    
    async def initialize_vector_store(self, storage_config):
        """Inicializa vector store con dimensión correcta"""
        
        # Verificar si tabla existe
        table_exists = await check_table_exists("message_embeddings")
        
        if not table_exists:
            # Crear tabla con dimensión correcta
            await create_vector_table(
                table_name="message_embeddings",
                dimension=self.dimension  # ← Auto-detectado
            )
        else:
            # Verificar dimensión de tabla existente
            existing_dim = await get_table_dimension("message_embeddings")
            
            if existing_dim != self.dimension:
                raise ValueError(
                    f"Dimension mismatch! "
                    f"Table has {existing_dim} dims, "
                    f"but provider uses {self.dimension} dims. "
                    f"Either change provider or recreate table."
                )

# ════════════════════════════════════════════════════════
# USO
# ════════════════════════════════════════════════════════

# Config para DeepSeek (1024 dims)
manager = EmbeddingManager({"name": "deepseek", ...})
# → Crea tabla: vector(1024)

# Config para OpenAI (1536 dims)
manager = EmbeddingManager({"name": "openai", ...})
# → Crea tabla: vector(1536)
```

---

## 🗄️ Scripts SQL Dinámicos

### Migration con Placeholders

```sql
-- luminoracore/storage/postgresql/migrations/004_add_pgvector.sql.template

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS message_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID NOT NULL REFERENCES messages(id),
    embedding vector({{EMBEDDING_DIMENSION}}),  -- ← Placeholder
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_message_embeddings_vector 
ON message_embeddings 
USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 100);
```

```python
# Al ejecutar migration, reemplazar placeholder
def execute_migration(sql_template: str, config: dict):
    """Ejecuta migration con config"""
    
    # Obtener dimensión del embedding provider
    dimension = get_embedding_dimension(config["embedding_provider"])
    
    # Reemplazar placeholder
    sql = sql_template.replace("{{EMBEDDING_DIMENSION}}", str(dimension))
    
    # Ejecutar
    await db.execute(sql)

# Resultado:
# - Si DeepSeek: CREATE TABLE ... vector(1024)
# - Si OpenAI: CREATE TABLE ... vector(1536)
```

---

## ✅ Validación y Testing Automático

### Health Check Completo

```python
# luminoracore/core/health.py

class HealthChecker:
    """Verifica que TODO esté configurado correctamente"""
    
    async def check_all(self, config: dict) -> dict:
        """Chequeo completo de salud del sistema"""
        
        results = {
            "llm_provider": await self.check_llm(config),
            "embedding_provider": await self.check_embeddings(config),
            "storage_provider": await self.check_storage(config),
            "vector_store": await self.check_vector_store(config),
            "cache": await self.check_cache(config)
        }
        
        return results
    
    async def check_llm(self, config: dict) -> dict:
        """Verifica LLM provider"""
        try:
            provider = create_llm_provider(config["llm_provider"])
            
            # Test request
            response = await provider.generate(
                messages=[{"role": "user", "content": "test"}],
                model=config["llm_provider"]["config"]["models"]["main"],
                max_tokens=5
            )
            
            return {
                "status": "ok",
                "provider": config["llm_provider"]["name"],
                "latency_ms": ...,
                "model": ...
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def check_embeddings(self, config: dict) -> dict:
        """Verifica embedding provider"""
        try:
            provider = create_embedding_provider(config["embedding_provider"])
            
            # Test embedding
            start = time.time()
            embedding = await provider.create_embedding("test")
            latency = (time.time() - start) * 1000
            
            return {
                "status": "ok",
                "provider": config["embedding_provider"]["name"],
                "dimension": len(embedding),
                "latency_ms": latency
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def check_storage(self, config: dict) -> dict:
        """Verifica storage provider"""
        try:
            provider = create_storage_provider(config["storage_provider"])
            
            # Test connection
            await provider.connect()
            
            # Test query
            await provider.execute("SELECT 1")
            
            # Verificar tablas
            tables = await provider.list_tables()
            required_tables = [
                "sessions", "messages", "user_affinity",
                "user_facts", "episodes", "message_embeddings"
            ]
            missing = [t for t in required_tables if t not in tables]
            
            return {
                "status": "ok" if not missing else "warning",
                "provider": config["storage_provider"]["name"],
                "tables_found": len(tables),
                "missing_tables": missing
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
```

---

## 🎯 Respuestas a tus Preguntas Específicas

### 1. "Si uso DeepSeek, TODO debe usar DeepSeek"

**✅ CORRECTO. El sistema se configura así:**

```json
{
  "llm_provider": {"name": "deepseek"},
  "embedding_provider": {"name": "deepseek"}  // ← Mismo provider
}
```

**El código NUNCA hardcodea OpenAI:**

```python
# ❌ NUNCA hacemos:
embeddings = await openai.embeddings.create(...)  # Hardcoded!

# ✅ SIEMPRE hacemos:
embeddings = await self.embedding_provider.create(...)  # Abstracción!
# ↑ Puede ser DeepSeek, OpenAI, Cohere, lo que configuraste
```

---

### 2. "Embeddings deben usar mismo LLM configurado"

**✅ SÍ, y es automático:**

```python
# Si configuraste DeepSeek:
config = load_config("luminora.json")

# Crea providers según config (NO hardcoded)
llm = create_llm_provider(config["llm_provider"])  # DeepSeek
embeddings = create_embedding_provider(config["embedding_provider"])  # DeepSeek Jina

# Ambos usan mismo API base si es el mismo provider
```

---

### 3. "BBDD debe ser configurable (PostgreSQL, SQLite, DynamoDB)"

**✅ SÍ, y hay migrations para cada una:**

```
luminoracore/storage/
├── postgresql/migrations/*.sql      ← Scripts PostgreSQL
├── sqlite/migrations/*.sql          ← Scripts SQLite
├── mysql/migrations/*.sql           ← Scripts MySQL
├── dynamodb/schemas/*.json          ← Schemas DynamoDB
└── mongodb/schemas/*.json           ← Schemas MongoDB
```

**Al ejecutar `luminora-cli migrate`, usa los scripts correctos:**

```bash
# Detecta qué BBDD usas (del config) y ejecuta migrations apropiadas
$ luminora-cli migrate

Reading config: config/luminora.json
Database: postgresql
⏳ Running PostgreSQL migrations...
  ✓ 001_initial_schema.sql
  ✓ 002_add_affinity_tables.sql
  ...
```

---

### 4. "Vector BBDD también configurable"

**✅ SÍ:**

```json
{
  "vector_store_provider": {
    "name": "pgvector",  // O "pinecone", "weaviate", "qdrant", "chromadb"
    "config": {...}
  }
}
```

**Cada uno tiene su adapter:**
- pgvector → PostgreSQL extension
- Pinecone → Cloud service
- Weaviate → Self-hosted o cloud
- ChromaDB → Local (perfecto para móvil)

---

### 5. "CLI para hacer setup paso a paso"

**✅ SÍ, el CLI guía todo el proceso:**

```bash
# Setup completo interactivo
$ luminora-cli init

# O paso a paso:
$ luminora-cli config llm --provider deepseek
$ luminora-cli config storage --provider postgresql
$ luminora-cli config embeddings --provider deepseek
$ luminora-cli migrate  # Crea tablas
$ luminora-cli test-connection  # Prueba todo
```

---

### 6. "Probar conexiones antes de usar"

**✅ SÍ, health checks integrados:**

```python
# El cliente verifica al inicializar
client = LuminoraCoreClient.from_config("config/luminora.json")

# Automáticamente:
# 1. Carga config
# 2. Crea providers
# 3. Prueba conexiones
# 4. Si algo falla → Error claro con instrucciones

# Health check manual:
health = await client.health_check()
if health["status"] == "ok":
    # Todo bien ✅
    pass
else:
    # Ver qué falló
    print(health["errors"])
```

---

## 🎯 Ejemplo Real: Tu Setup

### Tu Configuración (DeepSeek + PostgreSQL)

```json
// config/luminora.json
{
  "llm_provider": {
    "name": "deepseek",
    "config": {
      "api_base": "https://api.deepseek.com/v1",
      "api_key_env": "DEEPSEEK_API_KEY",
      "models": {
        "main": "deepseek-chat",
        "processing": "deepseek-chat",
        "embeddings": "deepseek-jina-embeddings-v3"  // ← Todo DeepSeek
      }
    }
  },
  
  "embedding_provider": {
    "name": "deepseek",  // ← Mismo que LLM
    "dimension": 1024,  // Auto-detectado
    "batch_processing": {
      "enabled": true,
      "batch_size": 10,
      "timeout_seconds": 30
    }
  },
  
  "storage_provider": {
    "name": "postgresql",  // ← Tu elección
    "config": {
      "host": "localhost",
      "port": 5432,
      "database": "luminora",
      "user": "luminora_user",
      "password_env": "DB_PASSWORD"
    }
  },
  
  "vector_store_provider": {
    "name": "pgvector",  // ← Integrado con PostgreSQL
    "config": {
      "dimension": 1024  // Según DeepSeek embeddings
    }
  }
}
```

---

### Qué Pasa Cuando Ejecutas

```bash
# 1. Inicializar
$ luminora-cli init --config config/luminora.json

Reading configuration...
  ✓ LLM Provider: deepseek
  ✓ Embedding Provider: deepseek (dim=1024)
  ✓ Storage: postgresql
  ✓ Vector Store: pgvector

# 2. Probar conexiones
Testing connections...
  ⏳ Testing DeepSeek API...
     ✓ Main LLM: OK (latency: 230ms)
     ✓ Embeddings: OK (dim: 1024, latency: 85ms)
  
  ⏳ Testing PostgreSQL...
     ✓ Connection: OK
     ⚠️ Tables not found
  
  ⏳ Testing pgvector...
     ⚠️ Extension not installed

# 3. Instalar extensión
? pgvector extension not found. Install now? (Y/n)
> Y

⏳ Installing pgvector...
  $ CREATE EXTENSION vector;
✓ pgvector installed!

# 4. Crear tablas
? Create database tables? (Y/n)
> Y

⏳ Running migrations for PostgreSQL...
  ✓ 001_initial_schema.sql
  ✓ 002_add_affinity_tables.sql
  ✓ 003_add_memory_tables.sql
  ✓ 004_add_pgvector_extension.sql (dimension=1024)
  ✓ 005_add_indexes.sql

✓ Database initialized!

# 5. Verificación final
⏳ Final health check...
  ✓ All systems operational!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ LuminoraCore Ready!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your Configuration:
  LLM:        DeepSeek (deepseek-chat)
  Embeddings: DeepSeek Jina (1024 dims, batch=10)
  Storage:    PostgreSQL (luminora@localhost)
  Vectors:    pgvector (1024 dims)

Ready to use! Run:
  python your_app.py
```

---

## 🎯 Configuraciones Diferentes

### Config 1: DeepSeek + SQLite (Simple)

```json
{
  "llm_provider": {"name": "deepseek"},
  "embedding_provider": {"name": "deepseek"},
  "storage_provider": {
    "name": "sqlite",
    "config": {"database_path": "./luminora.db"}
  },
  "vector_store_provider": {
    "name": "chromadb",  // Vector DB local
    "config": {"persist_directory": "./chroma_data"}
  }
}
```

**Migrations automáticas:**
- Usa scripts de `storage/sqlite/migrations/`
- Crea `luminora.db` con tablas SQLite
- Crea vector store local con ChromaDB

---

### Config 2: Claude + PostgreSQL

```json
{
  "llm_provider": {"name": "claude"},
  "embedding_provider": {"name": "voyage"},  // Voyage AI
  "storage_provider": {"name": "postgresql"},
  "vector_store_provider": {"name": "pgvector"}
}
```

**Migrations automáticas:**
- Usa scripts de `storage/postgresql/migrations/`
- Embeddings dimension = 1024 (Voyage)
- pgvector usa vector(1024)

---

### Config 3: Ollama Local (Todo Gratis)

```json
{
  "llm_provider": {
    "name": "ollama",
    "config": {
      "api_base": "http://localhost:11434",
      "models": {
        "main": "llama3.1",
        "processing": "llama3.1",
        "embeddings": "nomic-embed-text"
      }
    }
  },
  "embedding_provider": {
    "name": "ollama",
    "dimension": 768  // nomic-embed-text
  },
  "storage_provider": {"name": "sqlite"},
  "vector_store_provider": {"name": "chromadb"}
}
```

**TODO local, TODO gratis ✅**

---

## 📊 Tabla de Compatibilidad

### LLM Providers Soportados

| Provider | Main LLM | Embeddings | Dimension | Costo/1M tokens |
|----------|----------|------------|-----------|-----------------|
| **DeepSeek** | ✅ deepseek-chat | ✅ jina-v3 | 1024 | $0.14 |
| **OpenAI** | ✅ gpt-4 | ✅ text-emb-3 | 1536 | $15.00 |
| **Claude** | ✅ claude-3.5 | ❌ (usa Voyage) | - | $15.00 |
| **Mistral** | ✅ mistral-large | ✅ mistral-embed | 1024 | $2.00 |
| **Cohere** | ✅ command-r | ✅ embed-v3 | 1024 | $0.50 |
| **Groq** | ✅ llama3-70b | ❌ (usa otra) | - | $0.59 |
| **Ollama** | ✅ llama3.1 | ✅ nomic-embed | 768 | $0 (local) |

---

### Storage Providers Soportados

| Provider | Tipo | Vector Support | Migrations | Uso |
|----------|------|----------------|------------|-----|
| **PostgreSQL** | Relacional | ✅ pgvector | ✅ SQL | Production |
| **SQLite** | Relacional | ⚠️ Limitado | ✅ SQL | Development, Mobile |
| **MySQL** | Relacional | ⚠️ Limitado | ✅ SQL | Legacy systems |
| **DynamoDB** | NoSQL | ❌ | ✅ JSON | AWS Serverless |
| **MongoDB** | NoSQL | ✅ Atlas Vector | ✅ JSON | Flexible schema |

---

### Vector Store Providers

| Provider | Type | Hosted | Dimension Limit | Costo |
|----------|------|--------|-----------------|-------|
| **pgvector** | PostgreSQL ext | Self | 2000 | $0 (con PostgreSQL) |
| **Pinecone** | Cloud | Managed | 2000 | $70/mes |
| **Weaviate** | Self-hosted/Cloud | Both | 65536 | $0 o $25+/mes |
| **Qdrant** | Self-hosted/Cloud | Both | 65536 | $0 o $25+/mes |
| **ChromaDB** | Local | Self | Sin límite | $0 |

---

## 🛠️ CLI Commands Completos

### Setup Inicial

```bash
# Wizard completo
$ luminora-cli init

# Manual
$ luminora-cli config llm --provider deepseek --api-key-env DEEPSEEK_API_KEY
$ luminora-cli config storage --provider postgresql --host localhost --database luminora
$ luminora-cli config embeddings --provider deepseek --batch-size 10
$ luminora-cli config vector-store --provider pgvector
```

---

### Migrations

```bash
# Auto-migración
$ luminora-cli migrate

# Dry-run (solo mostrar, no ejecutar)
$ luminora-cli migrate --dry-run

# Migración específica
$ luminora-cli migrate --database postgresql --version 003

# Rollback
$ luminora-cli migrate --rollback --version 002
```

---

### Testing

```bash
# Health check completo
$ luminora-cli health

# Test específico
$ luminora-cli test llm
$ luminora-cli test storage
$ luminora-cli test embeddings
$ luminora-cli test vector-store

# Benchmark
$ luminora-cli benchmark --messages 100
```

---

### Info

```bash
# Ver configuración actual
$ luminora-cli config show

# Ver dimensión de embeddings
$ luminora-cli info embeddings

# Ver tablas en BBDD
$ luminora-cli info tables

# Ver estadísticas
$ luminora-cli stats
```

---

## 🎯 RESUMEN FINAL

### TODO es Configurable ✅

| Componente | Configuración | Ubicación |
|------------|---------------|-----------|
| **LLM principal** | config.llm_provider | JSON |
| **LLM processing** | config.llm_provider.models.processing | JSON |
| **Embeddings** | config.embedding_provider | JSON |
| **Batch size** | config.embedding_provider.batch_size | JSON |
| **Storage** | config.storage_provider | JSON |
| **Vector store** | config.vector_store_provider | JSON |
| **Cache** | config.cache_provider | JSON |

**NADA hardcoded** ✅

---

### Migrations Automáticas ✅

| BBDD | Scripts | Auto-detect Dimension | CLI |
|------|---------|----------------------|-----|
| **PostgreSQL** | ✅ SQL files | ✅ | ✅ |
| **SQLite** | ✅ SQL files | ✅ | ✅ |
| **MySQL** | ✅ SQL files | ✅ | ✅ |
| **DynamoDB** | ✅ JSON schemas | ✅ | ✅ |
| **MongoDB** | ✅ JSON schemas | ✅ | ✅ |

---

### Testing Integrado ✅

```bash
$ luminora-cli test-connection

✓ LLM: DeepSeek (230ms)
✓ Embeddings: DeepSeek Jina (85ms, dim=1024)
✓ Storage: PostgreSQL (12ms)
✓ Vector: pgvector (vector(1024) ready)
✓ Cache: Redis (2ms)

✅ All systems operational!
```

---

## 💡 Tu Flujo de Trabajo

```bash
# 1. Crear config
$ luminora-cli init --interactive
# → Elige DeepSeek, PostgreSQL, etc.
# → Genera config/luminora.json

# 2. Configurar variables
$ cat > .env << EOF
DEEPSEEK_API_KEY=sk-...
DB_PASSWORD=...
EOF

# 3. Crear BBDD
$ createdb luminora

# 4. Migrar tablas
$ luminora-cli migrate
# → Detecta PostgreSQL
# → Ejecuta scripts de storage/postgresql/migrations/
# → Crea tablas con dimension=1024 (según DeepSeek)

# 5. Probar
$ luminora-cli test-connection
# → ✅ Todo funciona

# 6. Usar
$ python your_app.py
```

---

<div align="center">

**✅ TODO CONFIGURABLE. NADA HARDCODED. PROVIDERS ABSTRAÍDOS.**

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

