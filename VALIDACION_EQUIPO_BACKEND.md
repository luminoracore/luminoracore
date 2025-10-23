# 📋 VALIDACIÓN PARA EL EQUIPO DE BACKEND - LuminoraCore v1.1

## 🎯 **OBJETIVO**
Este documento explica **exactamente** qué debe revisar el equipo de backend para verificar que la versión de LuminoraCore v1.1 tiene los fixes aplicados y funciona correctamente.

---

## 📁 **PASO 1: REVISAR ARCHIVOS EN EL CÓDIGO FUENTE**

### **1.1 Archivo Principal a Revisar:**
```
luminoracore-sdk-python/luminoracore_sdk/session/storage_dynamodb_flexible.py
```

### **1.2 Líneas Específicas a Verificar:**

#### **✅ LÍNEA 363 (Búsqueda con categoría):**
```python
# DEBE tener esto (CORREGIDO):
FilterExpression=f'user_id = :user_id AND #category = :category AND begins_with({self.range_key_name}, :fact_prefix)'

# NO debe tener esto (ROTO):
FilterExpression='user_id = :user_id AND #category = :category AND begins_with(#range_key, :fact_prefix)'
```

#### **✅ LÍNEA 378 (Búsqueda sin categoría):**
```python
# DEBE tener esto (CORREGIDO):
FilterExpression=f'user_id = :user_id AND begins_with({self.range_key_name}, :fact_prefix)'

# NO debe tener esto (ROTO):
FilterExpression='user_id = :user_id AND begins_with(#range_key, :fact_prefix)'
```

#### **✅ LÍNEA 517 (get_episodes):**
```python
# DEBE tener esto (CORREGIDO):
FilterExpression=f'user_id = :user_id AND begins_with({self.range_key_name}, :episode_prefix)'

# NO debe tener esto (ROTO):
FilterExpression='user_id = :user_id AND begins_with(#range_key, :episode_prefix)'
```

#### **✅ LÍNEA 637 (get_moods):**
```python
# DEBE tener esto (CORREGIDO):
FilterExpression=f'user_id = :user_id AND begins_with({self.range_key_name}, :mood_prefix)'

# NO debe tener esto (ROTO):
FilterExpression='user_id = :user_id AND begins_with(#range_key, :mood_prefix)'
```

### **1.3 Verificar que NO tenga ExpressionAttributeNames para range_key:**
```python
# NO debe tener esto en ninguna parte:
ExpressionAttributeNames={
    '#range_key': self.range_key_name
}
```

---

## 📦 **PASO 2: VALIDAR LA VERSIÓN DESCARGADA**

### **2.1 Verificar que el paquete se construyó correctamente:**
```bash
# En el directorio del proyecto
cd luminoracore-sdk-python
python setup.py sdist bdist_wheel
```

### **2.2 Verificar que el archivo .whl contiene los fixes:**
```bash
# Extraer el .whl y verificar el contenido
unzip -q luminoracore_sdk-*.whl
cat luminoracore_sdk/session/storage_dynamodb_flexible.py | grep -A 2 -B 2 "FilterExpression.*begins_with"
```

### **2.3 Verificar que __init__.py exporta setup_logging:**
```bash
# Verificar que el archivo __init__.py tiene:
cat luminoracore_sdk/__init__.py | grep "setup_logging"
```

**DEBE mostrar:**
```python
from .logging_config import setup_logging, auto_configure, get_logger
__all__ = [..., 'setup_logging', 'auto_configure', 'get_logger']
```

---

## 🚀 **PASO 3: VALIDAR UNA VEZ CREADA LA CAPA**

### **3.1 Verificar que la capa se creó correctamente:**
```bash
# Verificar que la capa existe
aws lambda list-layers --region eu-west-1
```

### **3.2 Verificar que la función Lambda usa la capa:**
```bash
# Verificar que la función tiene la capa asignada
aws lambda get-function --function-name tu-funcion --region eu-west-1
```

### **3.3 Verificar que el código de la función puede importar:**
```python
# En tu función Lambda, verificar que esto funciona:
from luminoracore_sdk import setup_logging, LuminoraCoreClientV11
from luminoracore_sdk.session import FlexibleDynamoDBStorageV11

# Esto NO debe dar error:
setup_logging(level="DEBUG", format_type="lambda")
```

---

## 🧪 **PASO 4: VALIDACIÓN FUNCIONAL COMPLETA**

### **4.1 Test de Importación:**
```python
# Ejecutar en tu función Lambda:
try:
    from luminoracore_sdk import setup_logging, LuminoraCoreClientV11
    from luminoracore_sdk.session import FlexibleDynamoDBStorageV11
    print("✅ Importaciones exitosas")
except Exception as e:
    print(f"❌ Error de importación: {e}")
```

### **4.2 Test de Configuración:**
```python
# Ejecutar en tu función Lambda:
try:
    setup_logging(level="DEBUG", format_type="lambda")
    print("✅ Logging configurado correctamente")
except Exception as e:
    print(f"❌ Error de logging: {e}")
```

### **4.3 Test de Storage:**
```python
# Ejecutar en tu función Lambda:
try:
    storage = FlexibleDynamoDBStorageV11(
        table_name="luminora-sessions-v1-1",
        region_name="eu-west-1"
    )
    print("✅ Storage inicializado correctamente")
except Exception as e:
    print(f"❌ Error de storage: {e}")
```

### **4.4 Test de Cliente:**
```python
# Ejecutar en tu función Lambda:
try:
    client = LuminoraCoreClientV11(base_client=None, storage_v11=storage)
    print("✅ Cliente inicializado correctamente")
except Exception as e:
    print(f"❌ Error de cliente: {e}")
```

### **4.5 Test de Memoria:**
```python
# Ejecutar en tu función Lambda:
try:
    facts = await client.get_facts("test_user")
    print(f"✅ get_facts() funciona - retornó {len(facts)} facts")
    if len(facts) > 0:
        print("✅ La memoria funciona correctamente")
    else:
        print("⚠️ No hay facts, pero el método funciona")
except Exception as e:
    print(f"❌ Error de memoria: {e}")
```

---

## 🔍 **PASO 5: VALIDACIÓN DE LOGS**

### **5.1 Verificar que los logs aparecen en CloudWatch:**
```python
# En tu función Lambda, verificar que esto aparece en los logs:
logger.info("DEBUG get_facts() - user_id: test_user")
logger.info("DEBUG get_facts() - table_name: luminora-sessions-v1-1")
logger.info("DEBUG get_facts() - range_key_name: timestamp")
```

### **5.2 Verificar que no hay errores de FilterExpression:**
```python
# En los logs NO debe aparecer:
# ❌ "Invalid FilterExpression"
# ❌ "ExpressionAttributeNames error"
# ❌ "begins_with function error"
```

---

## 📊 **PASO 6: VALIDACIÓN FINAL**

### **6.1 Test End-to-End:**
```python
# Ejecutar este test completo en tu función Lambda:
async def test_complete():
    try:
        # 1. Configurar logging
        setup_logging(level="DEBUG", format_type="lambda")
        
        # 2. Crear storage
        storage = FlexibleDynamoDBStorageV11(
            table_name="luminora-sessions-v1-1",
            region_name="eu-west-1"
        )
        
        # 3. Crear cliente
        client = LuminoraCoreClientV11(base_client=None, storage_v11=storage)
        
        # 4. Guardar un fact
        await client.save_fact(
            user_id="test_user",
            category="test_info",
            key="name",
            value="TestUser"
        )
        
        # 5. Recuperar facts
        facts = await client.get_facts("test_user")
        
        # 6. Verificar resultado
        if len(facts) > 0:
            print("✅ TEST COMPLETO EXITOSO - La memoria funciona")
            return True
        else:
            print("❌ TEST COMPLETO FALLIDO - La memoria no funciona")
            return False
            
    except Exception as e:
        print(f"❌ Error en test completo: {e}")
        return False

# Ejecutar test
result = await test_complete()
```

---

## 🚨 **SEÑALES DE ALERTA**

### **❌ Si ves esto, el fix NO está aplicado:**
```python
# En storage_dynamodb_flexible.py:
FilterExpression='begins_with(#range_key, :fact_prefix)'
ExpressionAttributeNames={'#range_key': self.range_key_name}
```

### **❌ Si ves este error:**
```python
# En runtime:
Runtime.ImportModuleError: cannot import name 'setup_logging' from 'luminoracore_sdk'
```

### **❌ Si get_facts() siempre retorna []:**
```python
facts = await client.get_facts("user123")
print(len(facts))  # Siempre 0
```

---

## ✅ **SEÑALES DE ÉXITO**

### **✅ Si ves esto, el fix SÍ está aplicado:**
```python
# En storage_dynamodb_flexible.py:
FilterExpression=f'begins_with({self.range_key_name}, :fact_prefix)'
# Sin ExpressionAttributeNames para range_key
```

### **✅ Si ves esto:**
```python
# En runtime:
from luminoracore_sdk import setup_logging  # No da error
```

### **✅ Si get_facts() retorna datos:**
```python
facts = await client.get_facts("user123")
print(len(facts))  # > 0 si hay datos
```

---

## 📞 **SOPORTE**

### **Si algo falla:**
1. **Revisar los archivos** según el Paso 1
2. **Verificar la distribución** según el Paso 2
3. **Validar la capa** según el Paso 3
4. **Ejecutar tests** según el Paso 4
5. **Revisar logs** según el Paso 5

### **Contactar al equipo de infraestructura si:**
- Los archivos no tienen los fixes aplicados
- La distribución no incluye los fixes
- Los tests fallan después de seguir todos los pasos

---

**Fecha:** 2025-10-23  
**Versión:** LuminoraCore v1.1  
**Estado:** Fix aplicado - Validación requerida
