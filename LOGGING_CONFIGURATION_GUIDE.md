# 🔧 GUÍA DE CONFIGURACIÓN DE LOGGING - LUMINORACORE

Esta guía explica cómo configurar el logging profesional en LuminoraCore para que todos los logs sean visibles en AWS Lambda y otros entornos de producción.

## 📋 RESUMEN

LuminoraCore ahora incluye configuración de logging profesional integrada. Ya no necesitas archivos "fix" cutres - todo está integrado directamente en el framework.

## 🚀 USO RÁPIDO

### Para AWS Lambda (Recomendado)

```python
from luminoracore_sdk import setup_logging, LuminoraCoreClientV11
from luminoracore_sdk.session import FlexibleDynamoDBStorageV11

# ⭐ UNA LÍNEA - Configurar logging
setup_logging(level="DEBUG", format_type="lambda")

async def lambda_handler(event, context):
    # Ahora TODOS los logs son visibles en CloudWatch
    storage = FlexibleDynamoDBStorageV11(
        table_name="luminoracore-sessions",
        region_name="eu-west-1"
    )
    
    client = LuminoraCoreClientV11(base_client=None, storage_v11=storage)
    facts = await client.get_facts("user123")
    
    # Logs que ahora SÍ aparecen:
    # DEBUG - luminoracore_sdk.client_v1_1 - Getting facts for user=user123
    # DEBUG - luminoracore_sdk.session.memory_v1_1 - Querying memory...
    # DEBUG - luminoracore_sdk.session.storage_dynamodb_flexible - DynamoDB query...
    # INFO - luminoracore_sdk - Retrieved 0 facts
    
    return {"statusCode": 200, "body": "Success"}
```

### Para Desarrollo Local

```python
from luminoracore_sdk import setup_logging, get_logger

# Configurar logging para desarrollo
setup_logging(level="DEBUG", format_type="text")

# Obtener logger
logger = get_logger(__name__)

logger.info("🚀 Aplicación iniciada")
logger.debug("Debug information visible")
```

### Para Producción

```python
from luminoracore_sdk import setup_logging

# Configurar logging estructurado para producción
setup_logging(level="INFO", format_type="json")

# Todos los logs serán en formato JSON estructurado
```

## 🔧 OPCIONES DE CONFIGURACIÓN

### Niveles de Logging

- `DEBUG`: Información detallada para debugging
- `INFO`: Información general (recomendado para producción)
- `WARNING`: Solo mensajes de advertencia
- `ERROR`: Solo mensajes de error
- `CRITICAL`: Solo errores críticos

### Tipos de Formato

- `lambda`: Optimizado para AWS Lambda/CloudWatch
- `json`: Formato JSON estructurado (mejor para producción)
- `text`: Formato de texto simple (mejor para desarrollo)
- `detailed`: Formato detallado con contexto completo

### Variables de Entorno

```bash
# Sobrescribir nivel de logging
export LUMINORACORE_LOG_LEVEL=DEBUG

# Sobrescribir formato
export LUMINORACORE_LOG_FORMAT=json

# Auto-detección
export AWS_LAMBDA_FUNCTION_NAME=my-function  # Auto-usa formato lambda
export DEBUG=1  # Auto-usa nivel DEBUG
```

## 📝 EJEMPLOS COMPLETOS

### 1. Lambda Handler Completo

```python
import json
import logging
from luminoracore_sdk import (
    LuminoraCoreClientV11,
    setup_logging
)
from luminoracore_sdk.session import FlexibleDynamoDBStorageV11

# ⭐ Configurar logging ANTES de importar otros módulos
setup_logging(level="DEBUG", format_type="lambda")

logger = logging.getLogger(__name__)

async def lambda_handler(event, context):
    logger.info("🚀 Handler iniciado")
    
    try:
        body = json.loads(event.get('body', '{}'))
        session_id = body.get('session_id')
        message = body.get('message')
        
        # Inicializar storage
        storage = FlexibleDynamoDBStorageV11(
            table_name="luminoracore-sessions",
            region_name="eu-west-1"
        )
        
        # Inicializar cliente
        client = LuminoraCoreClientV11(
            base_client=None,
            storage_v11=storage
        )
        
        # ⭐ AHORA TODOS LOS LOGS SON VISIBLES
        user_facts = await client.get_facts(session_id)
        logger.info(f"✓ Facts: {len(user_facts)}")
        
        result = await client.send_message_with_memory(
            session_id=session_id,
            message=message,
            personality="Sakura"
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### 2. Desarrollo Local con Debugging

```python
from luminoracore_sdk import setup_logging, LuminoraCoreClientV11
from luminoracore_sdk.session import InMemoryStorageV11
import asyncio

# Configurar logging para desarrollo
setup_logging(level="DEBUG", format_type="text")

async def main():
    storage = InMemoryStorageV11()
    client = LuminoraCoreClientV11(base_client=None, storage_v11=storage)
    
    # Test operations
    facts = await client.get_facts("test_user")
    print(f"✓ Facts retrieved: {len(facts)}")
    
    # Deberías ver logs como:
    # DEBUG - luminoracore_sdk.client_v1_1 - Getting facts for user: test_user
    # DEBUG - luminoracore_sdk.session.memory_v1_1 - Querying memory for facts
    # INFO - luminoracore_sdk - Retrieved 0 facts

asyncio.run(main())
```

### 3. Producción con Logging Estructurado

```python
from luminoracore_sdk import setup_logging, LuminoraCoreClientV11
from luminoracore_sdk.session import FlexiblePostgreSQLStorageV11

# Configurar para producción
setup_logging(level="INFO", format_type="json")

# Todos los logs serán en formato JSON estructurado
# Fácil de parsear con herramientas de agregación de logs
```

### 4. Auto-configuración

```python
from luminoracore_sdk import auto_configure, LuminoraCoreClientV11

# Auto-configurar basado en el entorno
auto_configure()

# Detecta automáticamente:
# - AWS Lambda: usa formato "lambda" con nivel INFO
# - Desarrollo (DEBUG=1): usa formato "text" con nivel DEBUG
# - Producción: usa formato "json" con nivel INFO
```

## 🔧 TROUBLESHOOTING

### Los logs no aparecen en Lambda

1. **Asegúrate de llamar `setup_logging()` ANTES de importar el SDK**
2. **Usa `format_type="lambda"`**
3. **Verifica el grupo de logs de CloudWatch para tu Lambda**

### Demasiados logs de boto3

```python
setup_logging(level="INFO", include_boto=True)
# Esto configura boto3/botocore al nivel WARNING
```

### Quieres diferentes niveles para diferentes módulos

```python
import logging
from luminoracore_sdk import setup_logging

# Configurar SDK
setup_logging(level="INFO")

# Sobrescribir módulo específico
logging.getLogger("luminoracore_sdk.session").setLevel(logging.DEBUG)
```

## 🎯 BENEFICIOS

| Aspecto | Antes | Después |
|---------|-------|---------|
| **Configuración** | Archivos `*_fix.py` cutres | Integrado profesionalmente |
| **Importación** | `import luminoracore_sdk_logging_fix` | `from luminoracore_sdk import setup_logging` |
| **Uso** | `configure_luminoracore_logging(...)` | `setup_logging(...)` |
| **Visibilidad** | Logs perdidos en Lambda | Logs visibles en CloudWatch |
| **Mantenimiento** | Difícil | Fácil y sostenible |
| **Documentación** | Ninguna | Completa y clara |

## ✅ VERIFICACIÓN

Para verificar que todo funciona correctamente:

```bash
# Ejecutar script de validación
python validate_framework.py

# Debe mostrar:
# ✅ ALL CHECKS PASSED! Framework is professional and clean.
```

## 📞 SOPORTE

Si tienes problemas:

1. **Revisa esta guía**
2. **Ejecuta `python validate_framework.py`**
3. **Verifica logs con `level="DEBUG"`**
4. **Contacta al equipo de infraestructura**

---

**¡El framework ahora es 100% profesional y todos los logs son visibles! 🚀**
