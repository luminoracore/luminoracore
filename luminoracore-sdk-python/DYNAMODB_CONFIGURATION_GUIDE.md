# 🎯 GUÍA COMPLETA DE CONFIGURACIÓN DE DYNAMODB PARA LUMINORACORE SDK

## PROBLEMA RESUELTO

**PROBLEMA ORIGINAL:**
La documentación del framework NO explica claramente cómo configurar `FlexibleDynamoDBStorageV11` para trabajar con tablas existentes que tienen esquemas diferentes.

**SOLUCIÓN:**
Esta guía proporciona documentación completa y ejemplos prácticos para configurar DynamoDB con cualquier esquema de tabla.

---

## 📋 ÍNDICE

1. [Configuración Básica](#configuración-básica)
2. [Esquemas de Tabla Soportados](#esquemas-de-tabla-soportados)
3. [Ejemplos Prácticos](#ejemplos-prácticos)
4. [Validación y Troubleshooting](#validación-y-troubleshooting)
5. [Mejores Prácticas](#mejores-prácticas)

---

## 🔧 CONFIGURACIÓN BÁSICA

### 1. Configuración Mínima

```python
from luminoracore_sdk.session.storage_dynamodb_flexible import FlexibleDynamoDBStorageV11

# Configuración básica - el framework auto-detecta el esquema
storage_v11 = FlexibleDynamoDBStorageV11(
    table_name="luminoracore-sessions",
    region_name="eu-west-1"
)
```

### 2. Configuración con Esquema Específico

```python
# Si tu tabla tiene un esquema específico, puedes especificarlo
storage_v11 = FlexibleDynamoDBStorageV11(
    table_name="mi-tabla-personalizada",
    region_name="eu-west-1",
    hash_key_name="PK",           # Nombre de tu hash key
    range_key_name="SK",          # Nombre de tu range key
    gsi_name="GSI1",              # Nombre de tu GSI (opcional)
    gsi_hash_key="GSI1PK",        # Hash key del GSI (opcional)
    gsi_range_key="GSI1SK"        # Range key del GSI (opcional)
)
```

---

## 🗃️ ESQUEMAS DE TABLA SOPORTADOS

### Esquema 1: Session-Based (Recomendado)

```yaml
Tabla: luminoracore-sessions
Hash Key: session_id (String)
Range Key: timestamp (String)

Ejemplo de items:
- session_id: "user123_session_001", timestamp: "2024-01-01T10:00:00Z"
- session_id: "user123_session_001", timestamp: "2024-01-01T10:01:00Z"
```

**Configuración:**
```python
storage_v11 = FlexibleDynamoDBStorageV11(
    table_name="luminoracore-sessions",
    region_name="eu-west-1"
    # Auto-detecta: hash_key_name="session_id", range_key_name="timestamp"
)
```

### Esquema 2: Partition Key Schema

```yaml
Tabla: mi-tabla-datos
Hash Key: PK (String)
Range Key: SK (String)

Ejemplo de items:
- PK: "USER#user123", SK: "FACT#personal_info#name"
- PK: "USER#user123", SK: "FACT#personal_info#age"
```

**Configuración:**
```python
storage_v11 = FlexibleDynamoDBStorageV11(
    table_name="mi-tabla-datos",
    region_name="eu-west-1",
    hash_key_name="PK",
    range_key_name="SK"
)
```

### Esquema 3: Simple ID Schema

```yaml
Tabla: conversaciones
Hash Key: id (String)
Range Key: created_at (String)

Ejemplo de items:
- id: "user123", created_at: "2024-01-01T10:00:00Z"
- id: "user123", created_at: "2024-01-01T10:01:00Z"
```

**Configuración:**
```python
storage_v11 = FlexibleDynamoDBStorageV11(
    table_name="conversaciones",
    region_name="eu-west-1",
    hash_key_name="id",
    range_key_name="created_at"
)
```

### Esquema 4: Con GSI (Global Secondary Index)

```yaml
Tabla: datos-usuarios
Hash Key: user_id (String)
Range Key: data_type (String)
GSI1: GSI1PK (String), GSI1SK (String)

Ejemplo de items:
- user_id: "user123", data_type: "FACT#personal_info#name"
- GSI1PK: "USER#user123", GSI1SK: "CATEGORY#personal_info"
```

**Configuración:**
```python
storage_v11 = FlexibleDynamoDBStorageV11(
    table_name="datos-usuarios",
    region_name="eu-west-1",
    hash_key_name="user_id",
    range_key_name="data_type",
    gsi_name="GSI1",
    gsi_hash_key="GSI1PK",
    gsi_range_key="GSI1SK"
)
```

---

## 💡 EJEMPLOS PRÁCTICOS

### Ejemplo 1: Tu Tabla Actual

Si tu tabla actual tiene el esquema:
- **Hash Key:** `session_id`
- **Range Key:** `timestamp`

```python
# Tu configuración actual (CORRECTA)
storage_v11 = FlexibleDynamoDBStorageV11(
    table_name="luminoracore-sessions",
    region_name="eu-west-1"
)

# El framework auto-detecta el esquema y funciona correctamente
```

### Ejemplo 2: Migración a Nueva Tabla

Si quieres usar una tabla con esquema diferente:

```python
# Nueva tabla con esquema PK/SK
storage_v11 = FlexibleDynamoDBStorageV11(
    table_name="nueva-tabla-luminoracore",
    region_name="eu-west-1",
    hash_key_name="PK",
    range_key_name="SK"
)
```

### Ejemplo 3: Tabla Existente con Datos

Si tienes una tabla existente con datos:

```python
# 1. Verificar esquema de tu tabla
import boto3

dynamodb = boto3.client('dynamodb', region_name='eu-west-1')
response = dynamodb.describe_table(TableName='tu-tabla-existente')

# 2. Configurar con el esquema detectado
hash_key = response['Table']['KeySchema'][0]['AttributeName']
range_key = response['Table']['KeySchema'][1]['AttributeName'] if len(response['Table']['KeySchema']) > 1 else None

storage_v11 = FlexibleDynamoDBStorageV11(
    table_name="tu-tabla-existente",
    region_name="eu-west-1",
    hash_key_name=hash_key,
    range_key_name=range_key
)
```

---

## 🔍 VALIDACIÓN Y TROUBLESHOOTING

### 1. Verificar Configuración

```python
from luminoracore_sdk_validation_fix import validation_manager

# Validar configuración
try:
    validation_manager.validate_storage_configuration(storage_v11)
    print("✅ Configuración válida")
except Exception as e:
    print(f"❌ Error de configuración: {e}")
```

### 2. Test de Conexión

```python
# Test básico de conexión
try:
    # Intentar obtener facts (debería funcionar incluso si no hay datos)
    facts = await storage_v11.get_facts("test_user")
    print(f"✅ Conexión exitosa, {len(facts)} facts encontrados")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
```

### 3. Debug de Esquema

```python
# Habilitar debug para ver detalles del esquema
from luminoracore_sdk_validation_fix import configure_validation
configure_validation(debug_mode=True)

# Ahora las operaciones mostrarán información detallada del esquema
facts = await storage_v11.get_facts("test_user")
```

### 4. Problemas Comunes

#### Problema: "Tabla no encontrada"
```python
# Solución: Verificar nombre de tabla y región
import boto3

dynamodb = boto3.client('dynamodb', region_name='eu-west-1')
try:
    response = dynamodb.describe_table(TableName='luminoracore-sessions')
    print(f"✅ Tabla encontrada: {response['Table']['TableStatus']}")
except Exception as e:
    print(f"❌ Tabla no encontrada: {e}")
```

#### Problema: "Credenciales AWS no válidas"
```python
# Solución: Verificar credenciales
import boto3

try:
    sts = boto3.client('sts')
    response = sts.get_caller_identity()
    print(f"✅ Credenciales válidas: {response['Arn']}")
except Exception as e:
    print(f"❌ Error de credenciales: {e}")
```

#### Problema: "get_facts() devuelve []"
```python
# Solución: Verificar datos en la tabla
import boto3

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('luminoracore-sessions')

# Escanear tabla para ver qué datos existen
response = table.scan(Limit=5)
print(f"Datos en tabla: {response['Items']}")
```

---

## 🚀 MEJORES PRÁCTICAS

### 1. Configuración Recomendada

```python
# Usar variables de entorno
import os

storage_v11 = FlexibleDynamoDBStorageV11(
    table_name=os.getenv("DYNAMODB_TABLE_NAME", "luminoracore-sessions"),
    region_name=os.getenv("AWS_REGION", "eu-west-1")
)
```

### 2. Manejo de Errores

```python
# Usar versión mejorada con validación
from luminoracore_sdk_improved_methods import create_improved_storage

storage_v11 = create_improved_storage(
    table_name="luminoracore-sessions",
    region_name="eu-west-1"
)

# Ahora get_facts() devuelve información detallada de errores
result = await storage_v11.get_facts("user123")
if isinstance(result, dict) and not result.get("success", True):
    print(f"Error: {result['error']}")
    print(f"Tipo: {result['error_type']}")
    print(f"Debug: {result['debug_info']}")
```

### 3. Configuración de Logging

```python
# Configurar logging antes de usar el SDK
from luminoracore_sdk_logging_fix import configure_luminoracore_logging

configure_luminoracore_logging(level="DEBUG")

# Ahora verás todos los logs del framework
```

### 4. Validación de Esquema

```python
# Validar esquema antes de usar
def validate_table_schema(table_name: str, region_name: str):
    import boto3
    
    dynamodb = boto3.client('dynamodb', region_name=region_name)
    response = dynamodb.describe_table(TableName=table_name)
    
    key_schema = response['Table']['KeySchema']
    hash_key = key_schema[0]['AttributeName']
    range_key = key_schema[1]['AttributeName'] if len(key_schema) > 1 else None
    
    print(f"Esquema detectado: {hash_key}/{range_key}")
    return hash_key, range_key

# Usar antes de crear storage
hash_key, range_key = validate_table_schema("luminoracore-sessions", "eu-west-1")
```

---

## 📝 EJEMPLO COMPLETO

```python
import asyncio
from luminoracore_sdk.session.storage_dynamodb_flexible import FlexibleDynamoDBStorageV11
from luminoracore_sdk_logging_fix import configure_luminoracore_logging
from luminoracore_sdk_validation_fix import configure_validation

async def main():
    # 1. Configurar logging
    configure_luminoracore_logging(level="DEBUG")
    
    # 2. Configurar validación
    configure_validation(debug_mode=True)
    
    # 3. Crear storage
    storage_v11 = FlexibleDynamoDBStorageV11(
        table_name="luminoracore-sessions",
        region_name="eu-west-1"
    )
    
    # 4. Test de operación
    try:
        facts = await storage_v11.get_facts("test_user")
        print(f"✅ get_facts() exitoso: {len(facts)} facts encontrados")
        
        # Test con categoría
        facts_category = await storage_v11.get_facts("test_user", category="personal_info")
        print(f"✅ get_facts() con categoría exitoso: {len(facts_category)} facts encontrados")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🆘 SOPORTE

Si tienes problemas con la configuración:

1. **Habilitar debug mode** para ver logs detallados
2. **Verificar credenciales AWS** y permisos de DynamoDB
3. **Validar esquema de tabla** con los ejemplos de arriba
4. **Usar versión mejorada** con manejo de errores detallado

**Logs de debug mostrarán:**
- Esquema de tabla detectado
- Parámetros de consulta
- Respuestas de DynamoDB
- Errores detallados con stack trace
