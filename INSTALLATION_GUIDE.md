# LuminoraCore v1.2.0 Installation Guide

Complete installation guide for all LuminoraCore components.

**Last Updated:** November 21, 2025  
**Version:** 1.2.0

> **🆕 What's New in v1.2.0:**  
> - Unified 3-layer architecture (Core, SDK, CLI)  
> - Core Integration: SDK now uses Core internally  
> - Optimization Module: 25-45% token reduction  
> - 100% Backward Compatible with v1.1  
> 
> See [`MIGRATION_1.1_to_1.2.md`](MIGRATION_1.1_to_1.2.md) for migration details.

## Prerequisites

- Python 3.9 or higher (3.11 recommended)
- pip package manager
- Git (optional, for cloning the repo)

## Quick Installation

### 1. Clone Repository (optional)

```bash
git clone https://github.com/luminoracore/luminoracore.git
cd luminoracore
```

### 2. Install Components (per folder)

**Important:** Install in order due to dependencies:

```bash
# 1. Core (required for SDK and CLI)
cd luminoracore && pip install . && cd ..

# 2. SDK (optional, requires Core)
cd luminoracore-sdk-python && pip install . && cd ..

# 3. CLI (optional, requires Core >= 1.2.0)
cd luminoracore-cli && pip install . && cd ..
```

**Note (Windows):** Install Core without editable mode (`-e`) to avoid namespace issues.

**Dependencies:**
- **SDK** requires `luminoracore>=1.2.0`
- **CLI** requires `luminoracore>=1.2.0` (NEW in v1.2.0)

### 3. Verify Installation

```bash
# Test Core
python -c "from luminoracore import Personality; print('✅ Core OK')"

# Test SDK (v1.2.0 - new client)
python -c "from luminoracore_sdk import LuminoraCoreClient; print('✅ SDK v1.2 OK')"

# Test SDK (v1.1 - backward compatibility)
python -c "from luminoracore_sdk import LuminoraCoreClientV11; print('✅ SDK v1.1 OK')"

# Test CLI
luminoracore --version
```

**Note:** `LuminoraCoreClient` is the new v1.2.0 client. `LuminoraCoreClientV11` is available for backward compatibility.

## Detailed Installation

### Core Framework

```bash
cd luminoracore/
pip install .
```

**Features:**
- Personality engine (PersonaBlend, PersonalityValidator)
- Memory system (MemorySystem)
- Storage backends (SQLite, Redis, PostgreSQL, MongoDB, DynamoDB)
- Optimization module (key mapping, compact format, deduplication, cache)
- Migration system

### SDK Python

```bash
cd luminoracore-sdk-python/
pip install .
```

**Features:**
- Client library (LuminoraCoreClient)
- LLM provider integration (OpenAI, Anthropic, DeepSeek, Mistral, Cohere, Google, Llama)
- Storage management (with optimization support)
- Memory operations (uses Core MemorySystem when available)
- Session management
- **NEW in v1.2.0:** Core integration via adapters

### CLI Tools

```bash
cd luminoracore-cli/
pip install .
```

**Features:**
- Memory management (uses Core MemorySystem)
- Database migrations (uses Core MigrationManager)
- Storage configuration
- Validation tools (uses Core PersonalityValidator)
- **NEW in v1.2.0:** Requires `luminoracore>=1.2.0` as dependency

## Storage Configuration

### Using v1.2.0 Client (Recommended)

```python
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.session import StorageConfig, StorageType
from luminoracore.optimization import OptimizationConfig

# With optimization (NEW in v1.2.0)
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type=StorageType.MEMORY  # or SQLITE, REDIS, etc.
    ),
    optimization_config=OptimizationConfig(
        key_abbreviation=True,
        cache_enabled=True
    )
)
await client.initialize()
```

### Using v1.1 Storage Classes (Backward Compatibility)

For backward compatibility, v1.1 storage classes are still available:

```python
from luminoracore_sdk import FlexibleSQLiteStorageV11

storage = FlexibleSQLiteStorageV11(
    database_path="luminora.db",
    facts_table="facts",
    affinity_table="affinity"
)
```

### PostgreSQL

```python
from luminoracore_sdk import FlexiblePostgreSQLStorageV11

storage = FlexiblePostgreSQLStorageV11(
    host="localhost",
    port=5432,
    database="luminora",
    username="user",
    password="password",
    facts_table="facts",
    affinity_table="affinity"
)
```

### DynamoDB

```python
from luminoracore_sdk import FlexibleDynamoDBStorageV11

storage = FlexibleDynamoDBStorageV11(
    table_name="luminora-table",
    region_name="us-east-1",
    hash_key_name="PK",
    range_key_name="SK"
)
```

### Redis

```python
from luminoracore_sdk import FlexibleRedisStorageV11

storage = FlexibleRedisStorageV11(
    host="localhost",
    port=6379,
    db=0,
    key_prefix="luminora:"
)
```

### MongoDB

```python
from luminoracore_sdk import FlexibleMongoDBStorageV11

storage = FlexibleMongoDBStorageV11(
    host="localhost",
    port=27017,
    database="luminora",
    facts_collection="facts",
    affinity_collection="affinity"
)
```

## Environment Configuration

### Environment Variables

```bash
# SQLite
export SQLITE_DATABASE_PATH="luminora.db"

# PostgreSQL
export POSTGRES_URL="postgresql://user:password@localhost:5432/luminora"

# DynamoDB
export DYNAMODB_TABLE="luminora-table"
export AWS_REGION="us-east-1"

# Redis
export REDIS_URL="redis://localhost:6379/0"

# MongoDB
export MONGODB_URL="mongodb://localhost:27017/luminora"
```

### Configuration File

Create `luminora_config.json`:

```json
{
  "storage": {
    "type": "sqlite",
    "sqlite": {
      "database_path": "luminora.db",
      "facts_table": "facts",
      "affinity_table": "affinity"
    }
  },
  "memory": {
    "max_entries": 1000,
    "decay_factor": 0.1
  }
}
```

## Docker Installation

### Docker Compose

```yaml
version: '3.8'
services:
  luminora:
    build: .
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_URL=postgresql://user:password@db:5432/luminora
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: luminora
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

## Development Installation

### Prerequisites

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
# Core tests
cd luminoracore/
pytest tests/ -v

# SDK tests  
cd luminoracore-sdk-python/
pytest tests/ -v

# CLI tests
cd luminoracore-cli/
pytest tests/ -v
```

### Build Packages

```bash
# Build all packages
./build_all_packages.sh

# Windows
./build_all_packages.ps1
```

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure packages are installed
cd luminoracore && pip install . && cd ..
cd luminoracore-sdk-python && pip install . && cd ..
cd luminoracore-cli && pip install . && cd ..
```

**Storage Connection Issues:**
```bash
# Test storage connection (v1.2.0)
python -c "
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.session import StorageConfig, StorageType
import asyncio

async def test():
    client = LuminoraCoreClient(
        storage_config=StorageConfig(storage_type=StorageType.MEMORY)
    )
    await client.initialize()
    print('✅ Storage OK (v1.2.0)')

asyncio.run(test())
"

# Test storage connection (v1.1 - backward compatibility)
python -c "
from luminoracore_sdk import FlexibleSQLiteStorageV11
storage = FlexibleSQLiteStorageV11(':memory:')
print('✅ Storage OK (v1.1)')
"
```

**CLI Not Found:**
```bash
# Ensure CLI is installed
cd luminoracore-cli && pip install . && cd ..
which luminoracore
```

### Platform-Specific Notes

**Windows:**
- Use PowerShell for scripts
- Set PYTHONPATH if needed
- Use Windows paths for database files

**macOS:**
- May need Xcode command line tools
- Use Homebrew for dependencies

**Linux:**
- Install build essentials
- Use system package manager for dependencies

## Architecture Overview (v1.2.0)

LuminoraCore uses a **3-layer architecture**:

1. **Core** (`luminoracore/`) - Pure business logic
2. **SDK** (`luminoracore-sdk-python/`) - Client layer with LLM integration
3. **CLI** (`luminoracore-cli/`) - User interface

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for complete documentation.

## Next Steps

1. **Read Documentation**: 
   - [`ARCHITECTURE.md`](ARCHITECTURE.md) - Architecture overview
   - [`MIGRATION_1.1_to_1.2.md`](MIGRATION_1.1_to_1.2.md) - Migration guide
   - Component-specific docs in each folder
2. **Run Examples**: Try the example scripts
3. **Configure Storage**: Set up your preferred database
4. **Enable Optimization** (Optional): Reduce tokens by 25-45%
5. **Create Personalities**: Build your first AI personality
6. **Integrate**: Use the SDK in your application

## Support

- **Documentation**: Check component docs directories
- **Examples**: See examples/ directory
- **Issues**: GitHub Issues
- **Community**: Discord/Forum links