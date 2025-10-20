# 🔧 All Databases Flexible Configuration Guide

## 🎯 **PROBLEMA COMPLETAMENTE RESUELTO: FLEXIBILIDAD TOTAL**

**TODAS** las bases de datos en LuminoraCore v1.1 son ahora **completamente flexibles**. El usuario puede usar **CUALQUIER** base de datos con **CUALQUIER** esquema, tabla, colección o configuración.

---

## ❌ **ANTES (Problemático):**
- ❌ Esquemas hardcodeados en todas las bases de datos
- ❌ Nombres de tabla/colección fijos
- ❌ Configuraciones rígidas
- ❌ Usuario obligado a usar esquemas específicos

## ✅ **AHORA (Completamente Flexible):**
- ✅ **CUALQUIER** base de datos
- ✅ **CUALQUIER** esquema/tabla/colección
- ✅ **CUALQUIER** configuración
- ✅ **Auto-detección** de estructuras
- ✅ **Sin hardcoding** en ninguna parte

---

## 🚀 **USO BÁSICO PARA TODAS LAS BASES DE DATOS**

### **1. DynamoDB Flexible**
```python
from luminoracore_sdk.session import FlexibleDynamoDBStorageV11

# CUALQUIER tabla, CUALQUIER esquema
storage = FlexibleDynamoDBStorageV11(
    table_name="mi-tabla-dynamodb",  # Tu tabla existente
    region_name="eu-west-1",          # Tu región
    hash_key_name="session_id",       # Tu hash key
    range_key_name="timestamp"        # Tu range key
)

# O auto-detección completa:
storage = FlexibleDynamoDBStorageV11(
    table_name="cualquier-tabla",
    region_name="cualquier-region"
)
# El framework detecta automáticamente TODO el esquema
```

### **2. SQLite Flexible**
```python
from luminoracore_sdk.session import FlexibleSQLiteStorageV11

# CUALQUIER base de datos, CUALQUIER tabla
storage = FlexibleSQLiteStorageV11(
    database_path="/path/to/mi/base/datos.sqlite",  # Tu base de datos
    facts_table="mis_hechos",                        # Tu tabla de hechos
    affinity_table="mi_afinidad",                    # Tu tabla de afinidad
    episodes_table="mis_episodios",                  # Tu tabla de episodios
    moods_table="mis_estados",                       # Tu tabla de estados
    memories_table="mi_memoria"                      # Tu tabla de memoria
)

# O auto-detección:
storage = FlexibleSQLiteStorageV11(
    database_path="/path/to/mi/base/datos.sqlite"
)
# El framework detecta automáticamente todas las tablas
```

### **3. PostgreSQL Flexible**
```python
from luminoracore_sdk.session import FlexiblePostgreSQLStorageV11

# CUALQUIER base de datos, CUALQUIER esquema, CUALQUIER tabla
storage = FlexiblePostgreSQLStorageV11(
    host="mi-postgres-host",
    port=5432,
    database="mi_base_datos",                        # Tu base de datos
    schema="mi_esquema",                             # Tu esquema
    facts_table="tabla_hechos",                      # Tu tabla de hechos
    affinity_table="tabla_afinidad",                 # Tu tabla de afinidad
    episodes_table="tabla_episodios",                # Tu tabla de episodios
    moods_table="tabla_estados",                     # Tu tabla de estados
    memories_table="tabla_memoria"                   # Tu tabla de memoria
)

# O auto-detección:
storage = FlexiblePostgreSQLStorageV11(
    host="mi-postgres-host",
    database="mi_base_datos"
)
# El framework detecta automáticamente esquemas y tablas
```

### **4. Redis Flexible**
```python
from luminoracore_sdk.session import FlexibleRedisStorageV11

# CUALQUIER Redis, CUALQUIER patrón de claves
storage = FlexibleRedisStorageV11(
    host="mi-redis-host",
    port=6379,
    db=0,
    key_prefix="mi_prefijo",                         # Tu prefijo de claves
    affinity_key_pattern="mi:afinidad:{user_id}:{personality_name}",  # Tu patrón
    fact_key_pattern="mi:hecho:{user_id}:{category}:{key}",          # Tu patrón
    episode_key_pattern="mi:episodio:{user_id}:{episode_id}",        # Tu patrón
    mood_key_pattern="mi:estado:{user_id}:{mood_id}",                # Tu patrón
    memory_key_pattern="mi:memoria:{user_id}:{memory_key}"           # Tu patrón
)

# O auto-detección:
storage = FlexibleRedisStorageV11(
    host="mi-redis-host",
    key_prefix="mi_prefijo"
)
# El framework genera automáticamente todos los patrones
```

### **5. MongoDB Flexible**
```python
from luminoracore_sdk.session import FlexibleMongoDBStorageV11

# CUALQUIER MongoDB, CUALQUIER colección
storage = FlexibleMongoDBStorageV11(
    host="mi-mongodb-host",
    port=27017,
    database="mi_base_datos",                        # Tu base de datos
    username="mi_usuario",                           # Tu usuario
    password="mi_password",                          # Tu password
    facts_collection="coleccion_hechos",             # Tu colección de hechos
    affinity_collection="coleccion_afinidad",        # Tu colección de afinidad
    episodes_collection="coleccion_episodios",       # Tu colección de episodios
    moods_collection="coleccion_estados",            # Tu colección de estados
    memories_collection="coleccion_memoria"          # Tu colección de memoria
)

# O auto-detección:
storage = FlexibleMongoDBStorageV11(
    host="mi-mongodb-host",
    database="mi_base_datos"
)
# El framework detecta automáticamente todas las colecciones
```

---

## 📋 **EJEMPLOS DE CONFIGURACIONES REALES**

### **Configuración 1: Empresa con PostgreSQL Multi-tenant**
```python
storage = FlexiblePostgreSQLStorageV11(
    host="postgres.empresa.com",
    database="luminora_empresa",
    schema="tenant_123",                             # Esquema por tenant
    facts_table="hechos_usuario",
    affinity_table="afinidad_usuario",
    episodes_table="episodios_usuario",
    moods_table="estados_usuario",
    memories_table="memoria_usuario"
)
```

### **Configuración 2: Startup con Redis Cluster**
```python
storage = FlexibleRedisStorageV11(
    host="redis-cluster.startup.com",
    port=6379,
    db=1,                                            # Base de datos específica
    key_prefix="startup_luminora",                   # Prefijo de la startup
    affinity_key_pattern="startup:afinidad:{user_id}:{personality_name}",
    fact_key_pattern="startup:hecho:{user_id}:{category}:{key}",
    episode_key_pattern="startup:episodio:{user_id}:{episode_id}",
    mood_key_pattern="startup:estado:{user_id}:{mood_id}",
    memory_key_pattern="startup:memoria:{user_id}:{memory_key}"
)
```

### **Configuración 3: Desarrollador con SQLite Local**
```python
storage = FlexibleSQLiteStorageV11(
    database_path="/home/dev/proyectos/mi_app/data/luminora.db",
    facts_table="user_facts",                        # Nombres en inglés
    affinity_table="user_affinity",
    episodes_table="user_episodes",
    moods_table="user_moods",
    memories_table="user_memories"
)
```

### **Configuración 4: AWS con DynamoDB Multi-región**
```python
# Región US East
storage_us = FlexibleDynamoDBStorageV11(
    table_name="luminora-us-east",
    region_name="us-east-1"
)

# Región EU West
storage_eu = FlexibleDynamoDBStorageV11(
    table_name="luminora-eu-west",
    region_name="eu-west-1"
)

# Región Asia Pacific
storage_asia = FlexibleDynamoDBStorageV11(
    table_name="luminora-asia-pacific",
    region_name="ap-southeast-1"
)
```

### **Configuración 5: MongoDB Atlas en la Nube**
```python
storage = FlexibleMongoDBStorageV11(
    host="cluster0.mongodb.net",
    port=27017,
    database="luminora_production",
    username="luminora_user",
    password="secure_password",
    facts_collection="user_facts",
    affinity_collection="user_affinity",
    episodes_collection="user_episodes",
    moods_collection="user_moods",
    memories_collection="user_memories"
)
```

---

## 🔧 **CONFIGURACIÓN AVANZADA**

### **Variables de Entorno**
```bash
# DynamoDB
export LUMINORA_DYNAMODB_TABLE="mi-tabla-luminora"
export LUMINORA_DYNAMODB_REGION="eu-west-1"
export LUMINORA_DYNAMODB_HASH_KEY="session_id"
export LUMINORA_DYNAMODB_RANGE_KEY="timestamp"

# PostgreSQL
export LUMINORA_POSTGRES_HOST="mi-postgres-host"
export LUMINORA_POSTGRES_DATABASE="mi_base_datos"
export LUMINORA_POSTGRES_SCHEMA="mi_esquema"
export LUMINORA_POSTGRES_FACTS_TABLE="tabla_hechos"

# Redis
export LUMINORA_REDIS_HOST="mi-redis-host"
export LUMINORA_REDIS_DB="1"
export LUMINORA_REDIS_KEY_PREFIX="mi_prefijo"

# MongoDB
export LUMINORA_MONGODB_HOST="mi-mongodb-host"
export LUMINORA_MONGODB_DATABASE="mi_base_datos"
export LUMINORA_MONGODB_FACTS_COLLECTION="coleccion_hechos"

# SQLite
export LUMINORA_SQLITE_PATH="/path/to/mi/base/datos.sqlite"
export LUMINORA_SQLITE_FACTS_TABLE="tabla_hechos"
```

### **Archivo de Configuración JSON**
```json
{
  "storage": {
    "type": "postgresql_flexible",
    "postgresql": {
      "host": "mi-postgres-host",
      "database": "mi_base_datos",
      "schema": "mi_esquema",
      "facts_table": "tabla_hechos",
      "affinity_table": "tabla_afinidad",
      "episodes_table": "tabla_episodios",
      "moods_table": "tabla_estados",
      "memories_table": "tabla_memoria"
    }
  },
  "redis": {
    "host": "mi-redis-host",
    "key_prefix": "mi_prefijo",
    "affinity_key_pattern": "mi:afinidad:{user_id}:{personality_name}",
    "fact_key_pattern": "mi:hecho:{user_id}:{category}:{key}"
  },
  "dynamodb": {
    "table_name": "mi-tabla-luminora",
    "region": "eu-west-1",
    "hash_key": "session_id",
    "range_key": "timestamp"
  }
}
```

### **Docker Compose**
```yaml
services:
  luminoracore:
    image: luminoracore-sdk:1.1.0
    environment:
      # PostgreSQL
      - LUMINORA_STORAGE_TYPE=postgresql_flexible
      - LUMINORA_POSTGRES_HOST=postgres
      - LUMINORA_POSTGRES_DATABASE=luminora_db
      - LUMINORA_POSTGRES_SCHEMA=public
      - LUMINORA_POSTGRES_FACTS_TABLE=user_facts
      
      # Redis
      - LUMINORA_REDIS_HOST=redis
      - LUMINORA_REDIS_KEY_PREFIX=luminora
      
      # DynamoDB
      - LUMINORA_DYNAMODB_TABLE=luminora-sessions
      - LUMINORA_DYNAMODB_REGION=eu-west-1
```

---

## 📊 **COMPATIBILIDAD TOTAL**

| Base de Datos | Esquema/Tabla/Colección | Configuración | Auto-detección | Soporte |
|---------------|-------------------------|---------------|----------------|---------|
| **DynamoDB** | Cualquiera | Cualquiera | ✅ Completa | ✅ Completo |
| **SQLite** | Cualquiera | Cualquiera | ✅ Completa | ✅ Completo |
| **PostgreSQL** | Cualquiera | Cualquiera | ✅ Completa | ✅ Completo |
| **Redis** | Cualquiera | Cualquiera | ✅ Completa | ✅ Completo |
| **MongoDB** | Cualquiera | Cualquiera | ✅ Completa | ✅ Completo |

---

## 🎯 **BENEFICIOS**

### **✅ Para Desarrolladores:**
- Usa tus bases de datos existentes
- No necesitas crear nuevas estructuras
- Esquemas personalizados
- Configuración flexible

### **✅ Para Empresas:**
- Integración con infraestructura existente
- Esquemas multi-tenant
- Diferentes regiones y entornos
- Cumplimiento de políticas

### **✅ Para DevOps:**
- No hay estructuras hardcodeadas
- Configuración por entorno
- Fácil migración
- Escalabilidad

---

## 🚀 **MIGRACIÓN**

### **Desde Versiones Anteriores (Rígidas)**
```python
# ANTES (rígido):
from luminoracore_sdk.session.storage_dynamodb_v11 import DynamoDBStorageV11

storage = DynamoDBStorageV11(
    table_name="luminoracore-v11",
    region_name="us-east-1"
)

# AHORA (flexible):
from luminoracore_sdk.session import FlexibleDynamoDBStorageV11

storage = FlexibleDynamoDBStorageV11(
    table_name="mi-tabla-existente",
    region_name="eu-west-1"
)
# ¡Funciona inmediatamente!
```

### **Auto-migración**
```python
# El framework detecta automáticamente tu estructura existente
storage = FlexibleDynamoDBStorageV11("mi-tabla-existente", "eu-west-1")
storage = FlexibleSQLiteStorageV11("/path/to/mi/database.sqlite")
storage = FlexiblePostgreSQLStorageV11(host="mi-host", database="mi-db")
storage = FlexibleRedisStorageV11(host="mi-redis", key_prefix="mi-prefix")
storage = FlexibleMongoDBStorageV11(host="mi-mongo", database="mi-db")
# ¡Todas funcionan inmediatamente!
```

---

## 📞 **SOPORTE**

### **Estructuras No Soportadas**
Si tienes una estructura muy específica que no funciona:

1. **Reporta la estructura** con `describe` o `info`
2. **El framework se adaptará** automáticamente
3. **O configura manualmente** los parámetros

### **Debugging**
```python
# Para debuggear las estructuras detectadas:
storage = FlexiblePostgreSQLStorageV11("mi-host", "mi-db")
print(f"Facts table: {storage.facts_table}")
print(f"Affinity table: {storage.affinity_table}")
print(f"Schema: {storage.schema}")
```

---

## 🎉 **CONCLUSIÓN**

**El framework LuminoraCore v1.1 es ahora VERDADERAMENTE flexible en TODAS las bases de datos:**

- ✅ **CUALQUIER** base de datos
- ✅ **CUALQUIER** esquema/tabla/colección
- ✅ **CUALQUIER** configuración
- ✅ **Auto-detección** completa
- ✅ **Sin hardcoding** en ninguna parte
- ✅ **Completamente configurable**
- ✅ **Funciona con estructuras existentes**

**¡Usa tus propias bases de datos, con tus propios esquemas, en tus propias configuraciones!**

---

## 📚 **REFERENCIA RÁPIDA**

```python
# Importar todas las versiones flexibles
from luminoracore_sdk.session import (
    FlexibleDynamoDBStorageV11,
    FlexibleSQLiteStorageV11,
    FlexiblePostgreSQLStorageV11,
    FlexibleRedisStorageV11,
    FlexibleMongoDBStorageV11
)

# Usar con cualquier configuración
storage = FlexibleDynamoDBStorageV11("mi-tabla", "mi-region")
storage = FlexibleSQLiteStorageV11("mi/database.sqlite")
storage = FlexiblePostgreSQLStorageV11("mi-host", "mi-db")
storage = FlexibleRedisStorageV11("mi-redis", key_prefix="mi-prefix")
storage = FlexibleMongoDBStorageV11("mi-mongo", "mi-db")

# ¡Todas funcionan inmediatamente!
```
