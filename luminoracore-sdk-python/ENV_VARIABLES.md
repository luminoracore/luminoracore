# 🔧 LuminoraCore v1.1 - Environment Variables Guide

Complete guide to environment variables for configuring LuminoraCore v1.1.

---

## 📋 v1.1 Environment Variables

### 🗄️ Database Configuration

```env
# PostgreSQL (primary storage for v1.1)
DB_PASSWORD=your_secure_password_here
POSTGRES_URL=postgresql://luminoracore:password@postgres:5432/luminoracore

# Redis (caching and sessions)
REDIS_URL=redis://redis:6379/0

# MongoDB (optional - document storage)
MONGODB_URL=mongodb://mongodb:27017/luminoracore
```

---

### ⚙️ v1.1 Core Configuration

```env
# Version tracking
LUMINORA_VERSION=1.1.0

# Feature flags configuration file
LUMINORA_FEATURES_CONFIG=/app/config/features_production_safe.json

# Auto-run migrations on startup
LUMINORA_AUTO_MIGRATE=true

# Storage backend (memory|redis|postgres|mongodb|sqlite)
LUMINORA_STORAGE_TYPE=postgres
```

**LUMINORA_STORAGE_TYPE options:**
- `memory` - In-memory (development/testing)
- `redis` - Redis (production, high speed)
- `postgres` - PostgreSQL (production, complete)
- `mongodb` - MongoDB (documents)
- `sqlite` - SQLite (mobile, single-user)

---

### 🚩 Feature Flags (v1.1)

```env
# Core memory features
LUMINORA_FEATURE_AFFINITY=true          # Affinity system
LUMINORA_FEATURE_FACTS=true             # Fact extraction
LUMINORA_FEATURE_EPISODES=true          # Episodic memory
LUMINORA_FEATURE_HIERARCHICAL=true      # Hierarchical personalities

# Analytics and export
LUMINORA_FEATURE_ANALYTICS=true         # Session analytics
LUMINORA_FEATURE_SNAPSHOTS=true         # State export/import

# Experimental (disabled by default)
LUMINORA_FEATURE_SEMANTIC_SEARCH=false  # Semantic search (requires vector store)
LUMINORA_FEATURE_MOOD_SYSTEM=false      # Mood states system
```

**Recommendations:**
- **Development:** All set to `true` for testing
- **Production:** Only stable features set to `true`
- **Testing:** All set to `false` for basic tests

---

### ⚡ Performance Tuning

```env
# Cache configuration
LUMINORA_CACHE_SIZE=1000                # In-memory cache size
LUMINORA_CACHE_TTL=3600                 # TTL in seconds (1 hour)

# Memory limits per user
LUMINORA_MAX_FACTS_PER_USER=500         # Maximum facts per user
LUMINORA_MAX_EPISODES_PER_USER=100      # Maximum episodes per user

# Thresholds
LUMINORA_FACT_CONFIDENCE_THRESHOLD=0.75      # Minimum confidence to save
LUMINORA_EPISODE_IMPORTANCE_THRESHOLD=6.0    # Minimum importance to save

# Cleanup intervals
LUMINORA_CLEANUP_INTERVAL=86400         # Cleanup every 24 hours
LUMINORA_MEMORY_RETENTION_DAYS=90       # Retain memory for 90 days
```

**Adjust based on:**
- **High traffic:** Increase CACHE_SIZE, reduce TTL
- **Memory constrained:** Reduce MAX_FACTS/EPISODES
- **Quality focused:** Increase THRESHOLDS
- **Long-term memory:** Increase RETENTION_DAYS

---

### 🔑 LLM Provider API Keys

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DEEPSEEK_API_KEY=...
MISTRAL_API_KEY=...
COHERE_API_KEY=...
GOOGLE_API_KEY=...
```

**Security:**
- ✅ Never commit keys to git
- ✅ Use secrets in production
- ✅ Rotate keys regularly
- ✅ Limit key permissions

---

### 📊 Monitoring & Observability

```env
# Metrics
LUMINORA_METRICS_ENABLED=true
LUMINORA_LOG_LEVEL=INFO                 # DEBUG|INFO|WARNING|ERROR
LUMINORA_PROMETHEUS_PORT=9091

# Grafana
GRAFANA_PASSWORD=admin
```

**Log Levels:**
- `DEBUG` - Development (very verbose)
- `INFO` - Standard production
- `WARNING` - Warnings only
- `ERROR` - Critical errors only

---

### 🔐 Security

```env
# API authentication
LUMINORA_API_KEY=your_secure_api_key_here

# CORS configuration
LUMINORA_CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Rate limiting
LUMINORA_RATE_LIMIT_ENABLED=true
LUMINORA_RATE_LIMIT_PER_MINUTE=60
```

---

### 🌐 Application Settings

```env
# Server configuration
LUMINORA_HOST=0.0.0.0
LUMINORA_PORT=8000
LUMINORA_WORKERS=4

# Timeouts
LUMINORA_REQUEST_TIMEOUT=30             # General timeout (seconds)
LUMINORA_LLM_TIMEOUT=60                 # Timeout for LLM calls
LUMINORA_DB_TIMEOUT=10                  # Timeout for DB queries
```

---

## 🎯 Configuration by Environment

### Development

```env
LUMINORA_VERSION=1.1.0
LUMINORA_FEATURES_CONFIG=config/features_development.json
LUMINORA_AUTO_MIGRATE=true
LUMINORA_STORAGE_TYPE=postgres
LUMINORA_LOG_LEVEL=DEBUG

# All features enabled
LUMINORA_FEATURE_AFFINITY=true
LUMINORA_FEATURE_FACTS=true
LUMINORA_FEATURE_EPISODES=true
LUMINORA_FEATURE_HIERARCHICAL=true
LUMINORA_FEATURE_ANALYTICS=true
LUMINORA_FEATURE_SNAPSHOTS=true
LUMINORA_FEATURE_SEMANTIC_SEARCH=true
LUMINORA_FEATURE_MOOD_SYSTEM=true
```

### Staging

```env
LUMINORA_VERSION=1.1.0
LUMINORA_FEATURES_CONFIG=config/features_production_safe.json
LUMINORA_AUTO_MIGRATE=true
LUMINORA_STORAGE_TYPE=postgres
LUMINORA_LOG_LEVEL=INFO

# Stable features only
LUMINORA_FEATURE_AFFINITY=true
LUMINORA_FEATURE_FACTS=true
LUMINORA_FEATURE_EPISODES=true
LUMINORA_FEATURE_HIERARCHICAL=true
LUMINORA_FEATURE_ANALYTICS=true
LUMINORA_FEATURE_SNAPSHOTS=true
LUMINORA_FEATURE_SEMANTIC_SEARCH=false
LUMINORA_FEATURE_MOOD_SYSTEM=false

# Conservative performance
LUMINORA_CACHE_SIZE=1000
LUMINORA_MAX_FACTS_PER_USER=500
```

### Production

```env
LUMINORA_VERSION=1.1.0
LUMINORA_FEATURES_CONFIG=config/features_production_safe.json
LUMINORA_AUTO_MIGRATE=false  # Manual migrations
LUMINORA_STORAGE_TYPE=postgres
LUMINORA_LOG_LEVEL=WARNING

# Only battle-tested features
LUMINORA_FEATURE_AFFINITY=true
LUMINORA_FEATURE_FACTS=true
LUMINORA_FEATURE_EPISODES=true
LUMINORA_FEATURE_HIERARCHICAL=true
LUMINORA_FEATURE_ANALYTICS=true
LUMINORA_FEATURE_SNAPSHOTS=true
LUMINORA_FEATURE_SEMANTIC_SEARCH=false
LUMINORA_FEATURE_MOOD_SYSTEM=false

# Optimized performance
LUMINORA_CACHE_SIZE=2000
LUMINORA_MAX_FACTS_PER_USER=1000
LUMINORA_RATE_LIMIT_PER_MINUTE=120

# Security
LUMINORA_API_KEY=${SECRET_API_KEY}
```

---

## 📖 Usage Examples

### Example 1: Full Development

```bash
# .env
LUMINORA_VERSION=1.1.0
LUMINORA_STORAGE_TYPE=postgres
LUMINORA_LOG_LEVEL=DEBUG
LUMINORA_FEATURE_AFFINITY=true
LUMINORA_FEATURE_FACTS=true
LUMINORA_FEATURE_EPISODES=true

# Start
docker-compose up -d

# View logs
docker-compose logs -f
```

### Example 2: Minimal Production

```bash
# .env
LUMINORA_VERSION=1.1.0
LUMINORA_STORAGE_TYPE=redis
LUMINORA_LOG_LEVEL=INFO
LUMINORA_FEATURES_CONFIG=config/features_minimal.json

# Start
docker-compose -f docker-compose.production.yml up -d
```

### Example 3: Testing Without Features

```bash
# .env
LUMINORA_VERSION=1.1.0
LUMINORA_STORAGE_TYPE=memory
LUMINORA_FEATURE_AFFINITY=false
LUMINORA_FEATURE_FACTS=false
LUMINORA_FEATURE_EPISODES=false

# Start
docker-compose up -d luminoracore
```

---

## 🔍 Debugging

### View Current Configuration

```bash
# Inside container
docker-compose exec luminoracore env | grep LUMINORA

# Specific variables
docker-compose exec luminoracore printenv LUMINORA_VERSION
docker-compose exec luminoracore printenv LUMINORA_FEATURE_AFFINITY
```

### Verify Active Features

```bash
docker-compose exec luminoracore python -c "
from luminoracore.core.config import get_features, is_enabled
print('Affinity:', is_enabled('affinity_system'))
print('Facts:', is_enabled('fact_extraction'))
"
```

---

## 📚 References

- **Docker Compose:** `docker-compose.yml` (development)
- **Production:** `docker-compose.production.yml`
- **Dockerfile:** `Dockerfile`
- **Entrypoint:** `docker-entrypoint.sh`
- **Documentation:** `DOCKER.md`

---

**Version:** 1.1.0  
**Last updated:** October 2025  
**Status:** ✅ Production Ready
