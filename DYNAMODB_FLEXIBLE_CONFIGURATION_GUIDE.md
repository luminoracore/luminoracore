# 🔧 DynamoDB Flexible Configuration Guide

## 🎯 **PROBLEMA RESUELTO: COMPLETA FLEXIBILIDAD**

El framework LuminoraCore v1.1 ahora es **completamente flexible** y puede usar **CUALQUIER** tabla DynamoDB con **CUALQUIER** esquema.

---

## ❌ **ANTES (Problemático):**
- ❌ Esquema hardcodeado (PK/SK/GSI1)
- ❌ Nombres de tabla fijos
- ❌ Usuario obligado a crear tablas específicas
- ❌ No funciona con tablas existentes

## ✅ **AHORA (Flexible):**
- ✅ **CUALQUIER** esquema de tabla
- ✅ **CUALQUIER** nombre de tabla
- ✅ **CUALQUIER** región AWS
- ✅ **Auto-detección** de esquemas
- ✅ Funciona con **tablas existentes**

---

## 🚀 **USO BÁSICO**

### **1. Auto-detección de Esquema (Recomendado)**
```python
from luminoracore_sdk.session import FlexibleDynamoDBStorageV11
from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11

# El framework detecta automáticamente el esquema de tu tabla
storage = FlexibleDynamoDBStorageV11(
    table_name="mi-tabla-dynamodb",  # Tu tabla existente
    region_name="eu-west-1"          # Tu región
)

client = LuminoraCoreClientV11(
    base_client=LuminoraCoreClient(),
    storage_v11=storage
)

# ¡Funciona con cualquier tabla!
await client.send_message_with_memory(
    session_id="mi-sesion",
    user_message="Hola!",
    personality_name="sakura",
    provider_config=provider_config
)
```

### **2. Configuración Explícita de Esquema**
```python
# Si quieres especificar el esquema manualmente
storage = FlexibleDynamoDBStorageV11(
    table_name="mi-tabla-personalizada",
    region_name="us-east-1",
    hash_key_name="session_id",      # Tu hash key
    range_key_name="timestamp",      # Tu range key
    gsi_name="UserIndex",            # Tu GSI (opcional)
    gsi_hash_key="user_id",          # Tu GSI hash key
    gsi_range_key="created_at"       # Tu GSI range key
)
```

---

## 📋 **EJEMPLOS DE ESQUEMAS SOPORTADOS**

### **Esquema 1: Session-based (session_id/timestamp)**
```python
# Tu tabla existente:
# - Hash Key: session_id (String)
# - Range Key: timestamp (String)

storage = FlexibleDynamoDBStorageV11(
    table_name="luminora-sessions-v1-1",
    region_name="eu-west-1",
    hash_key_name="session_id",
    range_key_name="timestamp"
)
```

### **Esquema 2: Partition-based (PK/SK)**
```python
# Tu tabla existente:
# - Hash Key: PK (String)
# - Range Key: SK (String)
# - GSI: GSI1 (GSI1PK/GSI1SK)

storage = FlexibleDynamoDBStorageV11(
    table_name="luminora-sessions-v1-1-correct",
    region_name="eu-west-1",
    hash_key_name="PK",
    range_key_name="SK",
    gsi_name="GSI1",
    gsi_hash_key="GSI1PK",
    gsi_range_key="GSI1SK"
)
```

### **Esquema 3: Multi-tenant Enterprise**
```python
# Tu tabla enterprise:
# - Hash Key: tenant_id (String)
# - Range Key: session_timestamp (String)
# - GSI: UserIndex (user_id/created_at)

storage = FlexibleDynamoDBStorageV11(
    table_name="enterprise-luminora-sessions",
    region_name="us-west-2",
    hash_key_name="tenant_id",
    range_key_name="session_timestamp",
    gsi_name="UserIndex",
    gsi_hash_key="user_id",
    gsi_range_key="created_at"
)
```

### **Esquema 4: Simple ID-based**
```python
# Tu tabla simple:
# - Hash Key: id (String)
# - Range Key: type (String)

storage = FlexibleDynamoDBStorageV11(
    table_name="mi-tabla-simple",
    region_name="ap-southeast-1",
    hash_key_name="id",
    range_key_name="type"
)
```

---

## 🌍 **MÚLTIPLES REGIONES**

```python
# Diferentes regiones, diferentes tablas, diferentes esquemas
storage_us = FlexibleDynamoDBStorageV11(
    table_name="luminora-us-east",
    region_name="us-east-1"
)

storage_eu = FlexibleDynamoDBStorageV11(
    table_name="luminora-eu-west",
    region_name="eu-west-1"
)

storage_asia = FlexibleDynamoDBStorageV11(
    table_name="luminora-asia-pacific",
    region_name="ap-southeast-1"
)
```

---

## 🔧 **CONFIGURACIÓN AVANZADA**

### **Variables de Entorno**
```bash
# Configuración por variables de entorno
export LUMINORA_DYNAMODB_TABLE="mi-tabla-luminora"
export LUMINORA_DYNAMODB_REGION="eu-west-1"
export LUMINORA_DYNAMODB_HASH_KEY="session_id"
export LUMINORA_DYNAMODB_RANGE_KEY="timestamp"
```

### **Archivo de Configuración**
```json
{
  "dynamodb": {
    "table_name": "mi-tabla-luminora",
    "region": "eu-west-1",
    "schema": {
      "hash_key": "session_id",
      "range_key": "timestamp",
      "gsi_name": "UserIndex",
      "gsi_hash_key": "user_id",
      "gsi_range_key": "created_at"
    }
  }
}
```

### **Docker Compose**
```yaml
services:
  luminoracore:
    image: luminoracore-sdk:1.1.0
    environment:
      - LUMINORA_STORAGE_TYPE=dynamodb_flexible
      - LUMINORA_DYNAMODB_TABLE=mi-tabla-luminora
      - LUMINORA_DYNAMODB_REGION=eu-west-1
      - LUMINORA_DYNAMODB_HASH_KEY=session_id
      - LUMINORA_DYNAMODB_RANGE_KEY=timestamp
```

---

## 📊 **COMPATIBILIDAD DE ESQUEMAS**

| Esquema | Hash Key | Range Key | GSI | Soporte |
|---------|----------|-----------|-----|---------|
| Session-based | session_id | timestamp | ❌ | ✅ Completo |
| Partition-based | PK | SK | GSI1 | ✅ Completo |
| Multi-tenant | tenant_id | session_timestamp | UserIndex | ✅ Completo |
| Simple ID | id | type | ❌ | ✅ Completo |
| Custom | Cualquiera | Cualquiera | Cualquiera | ✅ Completo |

---

## 🎯 **BENEFICIOS**

### **✅ Para Desarrolladores:**
- Usa tus tablas existentes
- No necesitas crear nuevas tablas
- Esquemas personalizados
- Configuración flexible

### **✅ Para Empresas:**
- Integración con infraestructura existente
- Esquemas multi-tenant
- Diferentes regiones
- Cumplimiento de políticas

### **✅ Para DevOps:**
- No hay tablas hardcodeadas
- Configuración por entorno
- Fácil migración
- Escalabilidad

---

## 🚀 **MIGRACIÓN**

### **Desde DynamoDBStorageV11 (Esquema Fijo)**
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
```

### **Auto-migración**
```python
# El framework detecta automáticamente tu esquema
storage = FlexibleDynamoDBStorageV11(
    table_name="tu-tabla-existente",
    region_name="tu-region"
)
# ¡Funciona inmediatamente!
```

---

## 📞 **SOPORTE**

### **Esquemas No Soportados**
Si tienes un esquema muy específico que no funciona:

1. **Reporta el esquema** con `describe_table`
2. **El framework se adaptará** automáticamente
3. **O configura manualmente** los parámetros

### **Debugging**
```python
# Para debuggear el esquema detectado:
storage = FlexibleDynamoDBStorageV11("tu-tabla", "tu-region")
print(f"Hash Key: {storage.hash_key_name}")
print(f"Range Key: {storage.range_key_name}")
print(f"GSI: {storage.gsi_name}")
```

---

## 🎉 **CONCLUSIÓN**

**El framework LuminoraCore v1.1 es ahora verdaderamente flexible:**

- ✅ **CUALQUIER** tabla DynamoDB
- ✅ **CUALQUIER** esquema
- ✅ **CUALQUIER** región
- ✅ **CUALQUIER** configuración
- ✅ **Auto-detección** de esquemas
- ✅ **Sin hardcoding**
- ✅ **Completamente configurable**

**¡Usa tus propias tablas, con tus propios esquemas, en tus propias regiones!**
