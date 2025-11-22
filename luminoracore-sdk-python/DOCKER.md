# 🐳 LuminoraCore SDK - Docker Guide

This guide explains how to use LuminoraCore v1.1 with Docker and Docker Compose.

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# 1. Copy example configuration
cp .env.example .env

# 2. Edit .env with your values
nano .env  # or vim, code, etc.

# 3. Start all services
docker-compose up -d

# 4. Check logs
docker-compose logs -f luminoracore
```

**Access:**
- API: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

---

## 📋 Available Configurations

### 1. Development (docker-compose.yml)

**For:** Complete local development

```bash
docker-compose up -d
```

**Includes:**
- ✅ LuminoraCore SDK
- ✅ Redis (cache)
- ✅ PostgreSQL (storage)
- ✅ MongoDB (optional)
- ✅ Prometheus (metrics)
- ✅ Grafana (dashboards)

**v1.1 Features:**
- ✅ All features enabled
- ✅ Auto-migrate activated
- ✅ Detailed logs

---

### 2. Production (docker-compose.production.yml)

**For:** Production deployment

```bash
docker-compose -f docker-compose.production.yml up -d
```

**Differences from development:**
- ✅ Resource limits (CPU/Memory)
- ✅ Health checks configured
- ✅ Experimental features disabled
- ✅ Security configuration
- ✅ Read-only volumes where applicable

**Optional profiles:**
```bash
# Without MongoDB
docker-compose -f docker-compose.production.yml up -d

# With monitoring
docker-compose -f docker-compose.production.yml --profile monitoring up -d

# With MongoDB
docker-compose -f docker-compose.production.yml --profile with-mongodb up -d
```

---

## 🔧 v1.1 Environment Variables

### Core Configuration

```env
# Version
LUMINORA_VERSION=1.1.0

# Feature flags
LUMINORA_FEATURES_CONFIG=/app/config/features_production_safe.json
LUMINORA_AUTO_MIGRATE=true
LUMINORA_STORAGE_TYPE=postgres
```

### Feature Flags

```env
# Memory features
LUMINORA_FEATURE_AFFINITY=true
LUMINORA_FEATURE_FACTS=true
LUMINORA_FEATURE_EPISODES=true
LUMINORA_FEATURE_HIERARCHICAL=true

# Advanced features
LUMINORA_FEATURE_ANALYTICS=true
LUMINORA_FEATURE_SNAPSHOTS=true
LUMINORA_FEATURE_SEMANTIC_SEARCH=false  # Requires vector store
LUMINORA_FEATURE_MOOD_SYSTEM=false      # Experimental
```

### Performance

```env
LUMINORA_CACHE_SIZE=1000
LUMINORA_MAX_FACTS_PER_USER=500
LUMINORA_MAX_EPISODES_PER_USER=100
LUMINORA_FACT_CONFIDENCE_THRESHOLD=0.75
LUMINORA_EPISODE_IMPORTANCE_THRESHOLD=6.0
```

**See `.env.example` for all options.**

---

## 🗄️ Database

### PostgreSQL (Recommended for v1.1)

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U luminoracore

# View v1.1 tables
\dt

# Check migrations
SELECT * FROM schema_migrations;

# View data
SELECT * FROM user_affinity LIMIT 10;
SELECT * FROM user_facts LIMIT 10;
SELECT * FROM episodes LIMIT 10;
```

### Redis (Cache and Sessions)

```bash
# Connect to Redis
docker-compose exec redis redis-cli

# View keys
KEYS *

# View stats
INFO stats
```

### MongoDB (Optional)

```bash
# Connect to MongoDB
docker-compose exec mongodb mongosh

# View collections
show collections

# Query
db.sessions.find().limit(5)
```

---

## 🔄 Migrations

### Automatic (on startup)

If `LUMINORA_AUTO_MIGRATE=true`:
```bash
docker-compose up -d  # Runs migrations automatically
docker-compose logs luminoracore | grep migration
```

### Manual

```bash
# Status
docker-compose exec luminoracore luminora-cli migrate --status

# Apply
docker-compose exec luminoracore luminora-cli migrate up

# Rollback
docker-compose exec luminoracore luminora-cli migrate down

# View history
docker-compose exec luminoracore luminora-cli migrate --history
```

---

## 📊 Monitoring (Optional)

### Start with monitoring

```bash
docker-compose --profile monitoring up -d
```

**Additional services:**
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000

### Dashboards

Grafana includes pre-configured dashboards:
1. **LuminoraCore Overview** - General metrics
2. **v1.1 Memory System** - Facts, Episodes, Affinity
3. **Performance** - Latency, cache, DB queries

**Login:** admin / admin (change in production)

---

## 🛠️ Useful Commands

### Service Management

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart specific service
docker-compose restart luminoracore

# View logs
docker-compose logs -f luminoracore

# View resources
docker stats
```

### Maintenance

```bash
# Execute command in container
docker-compose exec luminoracore bash

# PostgreSQL backup
docker-compose exec postgres pg_dump -U luminoracore > backup_$(date +%Y%m%d).sql

# Restore backup
cat backup.sql | docker-compose exec -T postgres psql -U luminoracore

# Clean volumes (⚠️ CAREFUL)
docker-compose down -v
```

### v1.1 Specific

```bash
# Query memory
docker-compose exec luminoracore luminora-cli memory facts --session-id user123

# Query episodes
docker-compose exec luminoracore luminora-cli memory episodes --session-id user123

# Create snapshot
docker-compose exec luminoracore luminora-cli snapshot create --session-id user123
```

---

## 🔒 Production Security

### 1. Change Passwords

```env
# .env
DB_PASSWORD=strong_random_password_here
GRAFANA_PASSWORD=another_strong_password
LUMINORA_API_KEY=secure_api_key_here
```

### 2. Configure CORS

```env
LUMINORA_CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### 3. Use Secrets

In production, use Docker secrets:

```yaml
services:
  luminoracore:
    secrets:
      - db_password
      - api_key

secrets:
  db_password:
    external: true
  api_key:
    external: true
```

### 4. Network Security

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access
```

---

## 📈 Scaling

### Horizontal Scaling

```bash
# Scale main service
docker-compose up -d --scale luminoracore=3
```

**Requires:**
- Load balancer (nginx/traefik)
- Redis for shared sessions
- PostgreSQL with connection pooling

### Vertical Scaling

```yaml
# docker-compose.production.yml
deploy:
  resources:
    limits:
      cpus: '4'      # Increase CPUs
      memory: 4G     # Increase RAM
```

---

## 🐛 Troubleshooting

### Problem: Migrations fail

```bash
# View detailed logs
docker-compose logs luminoracore | grep migration

# Run manually
docker-compose exec luminoracore luminora-cli migrate up --verbose

# Dry-run for debugging
docker-compose exec luminoracore luminora-cli migrate up --dry-run
```

### Problem: Connection refused

```bash
# Verify services
docker-compose ps

# Check health
docker-compose exec postgres pg_isready
docker-compose exec redis redis-cli ping

# Restart services
docker-compose restart postgres redis
```

### Problem: Out of memory

```bash
# View usage
docker stats

# Increase limits
# Edit docker-compose.yml → deploy.resources.limits.memory

# Clear cache
docker-compose exec redis redis-cli FLUSHALL
```

---

## 📦 Build and Publish

### Build Image

```bash
# Build image
docker build -t luminoracore-sdk:1.1.0 .

# Tag for registry
docker tag luminoracore-sdk:1.1.0 yourregistry/luminoracore-sdk:1.1.0

# Push
docker push yourregistry/luminoracore-sdk:1.1.0
```

### Multi-platform Build

```bash
# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 \
  -t luminoracore-sdk:1.1.0 \
  --push .
```

---

## 🎯 Use Cases

### Local Development

```bash
# Everything in one
docker-compose up -d

# Only necessary services
docker-compose up -d redis postgres luminoracore
```

### Testing

```bash
# Isolated environment
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

### Staging

```bash
# Staging configuration
docker-compose -f docker-compose.production.yml --env-file .env.staging up -d
```

### Production

```bash
# With monitoring
docker-compose -f docker-compose.production.yml --profile monitoring up -d

# Verify health
curl http://localhost:8000/health
```

---

## 📚 Configuration Files

```
luminoracore-sdk-python/
├── Dockerfile                         # v1.1 base image
├── docker-compose.yml                 # Development
├── docker-compose.production.yml      # Production
├── docker-entrypoint.sh              # v1.1 startup script
├── .env.example                      # Environment variables
├── config/
│   ├── features_minimal.json        # Minimal features
│   ├── features_development.json    # Full features
│   └── features_production_safe.json # Stable features
└── monitoring/
    ├── prometheus.yml
    └── grafana/
```

---

## ✅ Verification

### 1. Services Running

```bash
docker-compose ps

# Expected:
# luminoracore    running (healthy)
# postgres        running (healthy)
# redis           running (healthy)
```

### 2. Health Checks

```bash
# API health
curl http://localhost:8000/health

# Expected:
# {"status": "healthy", "version": "1.1.0"}
```

### 3. v1.1 Features

```bash
# Verify features
docker-compose exec luminoracore python -c "
from luminoracore.core.config import get_features
print(get_features())
"
```

### 4. Migrations

```bash
# Status
docker-compose exec luminoracore luminora-cli migrate --status

# Expected:
# ✅ 001_initial
# ✅ 002_affinity
# ✅ 003_facts
# ✅ 004_episodes
# ✅ 005_moods
```

---

## 🎉 Summary

**Docker setup for v1.1:**
- ✅ Dockerfile updated with v1.1
- ✅ docker-compose.yml with all features
- ✅ docker-compose.production.yml optimized
- ✅ docker-entrypoint.sh with auto-migrate
- ✅ .env.example with all variables
- ✅ Optional monitoring stack
- ✅ Complete documentation

**To get started:**
```bash
cp .env.example .env
# Edit .env
docker-compose up -d
```

**For production:**
```bash
docker-compose -f docker-compose.production.yml --profile monitoring up -d
```

---

**Version:** 1.1.0  
**Last updated:** October 2025  
**Status:** ✅ Production Ready
