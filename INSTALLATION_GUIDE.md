# LuminoraCore v1.1 Installation Guide

Complete installation guide for all LuminoraCore components.

## Prerequisites

- Python 3.9 or higher
- pip package manager
- Git (for development)

## Quick Installation

### 1. Clone Repository

```bash
git clone https://github.com/luminoracore/luminoracore.git
cd luminoracore
```

### 2. Install All Components

```bash
# Install Core framework
pip install -e luminoracore/

# Install SDK
pip install -e luminoracore-sdk-python/

# Install CLI
pip install -e luminoracore-cli/
```

### 3. Verify Installation

```bash
# Test Core
python -c "from luminoracore import Personality; print('Core OK')"

# Test SDK
python -c "from luminoracore_sdk import LuminoraCoreClientV11; print('SDK OK')"

# Test CLI
luminoracore --version
```

## Detailed Installation

### Core Framework

```bash
cd luminoracore/
pip install -e .
```

**Features:**
- Personality engine
- Memory system
- Storage backends
- Evolution algorithms

### SDK Python

```bash
cd luminoracore-sdk-python/
pip install -e .
```

**Features:**
- Client library
- Storage management
- Memory operations
- Context API

### CLI Tools

```bash
cd luminoracore-cli/
pip install -e .
```

**Features:**
- Memory management
- Database migrations
- Storage configuration
- Validation tools

## Storage Configuration

### SQLite (Default)

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
# Ensure packages are installed in development mode
pip install -e luminoracore/
pip install -e luminoracore-sdk-python/
pip install -e luminoracore-cli/
```

**Storage Connection Issues:**
```bash
# Test storage connection
python -c "
from luminoracore_sdk import FlexibleSQLiteStorageV11
storage = FlexibleSQLiteStorageV11(':memory:')
print('Storage OK')
"
```

**CLI Not Found:**
```bash
# Ensure CLI is installed
pip install -e luminoracore-cli/
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

## Next Steps

1. **Read Documentation**: Check component-specific docs
2. **Run Examples**: Try the example scripts
3. **Configure Storage**: Set up your preferred database
4. **Create Personalities**: Build your first AI personality
5. **Integrate**: Use the SDK in your application

## Support

- **Documentation**: Check component docs directories
- **Examples**: See examples/ directory
- **Issues**: GitHub Issues
- **Community**: Discord/Forum links