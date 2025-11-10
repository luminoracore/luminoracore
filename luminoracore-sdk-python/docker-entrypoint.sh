#!/bin/bash
# LuminoraCore v1.1 - Docker Entrypoint Script
# Handles v1.1 initialization and migrations

set -e

echo "🚀 LuminoraCore v1.1 - Starting..."
echo "Version: ${LUMINORA_VERSION:-1.1.0}"

# ========================================
# 1. VERIFICAR FEATURE FLAGS
# ========================================
echo ""
echo "📋 Feature Flags Configuration:"
echo "   Config file: ${LUMINORA_FEATURES_CONFIG:-config/features_production_safe.json}"

if [ -n "$LUMINORA_FEATURE_AFFINITY" ]; then
    echo "   ✓ Affinity system: ${LUMINORA_FEATURE_AFFINITY}"
fi
if [ -n "$LUMINORA_FEATURE_FACTS" ]; then
    echo "   ✓ Fact extraction: ${LUMINORA_FEATURE_FACTS}"
fi
if [ -n "$LUMINORA_FEATURE_EPISODES" ]; then
    echo "   ✓ Episodic memory: ${LUMINORA_FEATURE_EPISODES}"
fi

# ========================================
# 2. ESPERAR POR BASE DE DATOS
# ========================================
echo ""
echo "🗄️  Waiting for database services..."

# Wait for PostgreSQL
if [ -n "$POSTGRES_URL" ]; then
    echo "   Waiting for PostgreSQL..."
    until python -c "import psycopg2; psycopg2.connect('$POSTGRES_URL')" 2>/dev/null; do
        echo "   ⏳ PostgreSQL is unavailable - sleeping"
        sleep 2
    done
    echo "   ✓ PostgreSQL is ready"
fi

# Wait for Redis
if [ -n "$REDIS_URL" ]; then
    echo "   Waiting for Redis..."
    until python -c "import redis; redis.from_url('$REDIS_URL').ping()" 2>/dev/null; do
        echo "   ⏳ Redis is unavailable - sleeping"
        sleep 2
    done
    echo "   ✓ Redis is ready"
fi

# Wait for MongoDB
if [ -n "$MONGODB_URL" ]; then
    echo "   Waiting for MongoDB..."
    until python -c "from pymongo import MongoClient; MongoClient('$MONGODB_URL').admin.command('ping')" 2>/dev/null; do
        echo "   ⏳ MongoDB is unavailable - sleeping"
        sleep 2
    done
    echo "   ✓ MongoDB is ready"
fi

# ========================================
# 3. EJECUTAR MIGRACIONES (si está habilitado)
# ========================================
if [ "$LUMINORA_AUTO_MIGRATE" = "true" ]; then
    echo ""
    echo "🔄 Running v1.1 database migrations..."
    
    # Verificar si el comando existe
    if command -v luminora-cli &> /dev/null; then
        echo "   Checking migration status..."
        luminora-cli migrate --status || true
        
        echo "   Applying pending migrations..."
        luminora-cli migrate up || {
            echo "   ⚠️  Migration failed, but continuing startup"
            echo "   Run migrations manually: luminora-cli migrate up"
        }
        
        echo "   ✓ Migrations completed"
    else
        echo "   ⚠️  luminora-cli not found, skipping migrations"
        echo "   Install: pip install luminoracore-cli"
    fi
else
    echo ""
    echo "⏭️  Auto-migrate disabled (LUMINORA_AUTO_MIGRATE=${LUMINORA_AUTO_MIGRATE})"
    echo "   Run migrations manually: luminora-cli migrate up"
fi

# ========================================
# 4. VERIFICAR CONFIGURACIÓN
# ========================================
echo ""
echo "⚙️  Configuration:"
echo "   Storage: ${LUMINORA_STORAGE_TYPE:-memory}"
echo "   Cache size: ${LUMINORA_CACHE_SIZE:-1000}"
echo "   Max facts/user: ${LUMINORA_MAX_FACTS_PER_USER:-500}"
echo "   Max episodes/user: ${LUMINORA_MAX_EPISODES_PER_USER:-100}"

# ========================================
# 5. INICIAR APLICACIÓN
# ========================================
echo ""
echo "✅ LuminoraCore v1.1 ready!"
echo "🚀 Starting application..."
echo ""

# Ejecutar el comando pasado al container
exec "$@"

