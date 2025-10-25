# ⚠️ ERROR DEL BACKEND: Módulo 'requests' Faltante

**Fecha:** 2025-01-27  
**Prioridad:** 🔴 ALTA  
**Estado:** ⚠️ ERROR EN EL BACKEND  
**Responsable:** Equipo Backend API

---

## 📋 **RESUMEN EJECUTIVO**

El error **NO es del framework**. Es un **error de configuración del backend** que está intentando usar el módulo `requests` que no está disponible en el Lambda Layer.

### **Error en CloudWatch:**
```
Runtime.ImportModuleError: Unable to import module 'src.handlers.simulate': No module named 'requests'
```

### **Causa Raíz:**
El handler `src.handlers.simulate` está intentando importar la librería `requests`, pero esta librería **NO está incluida en el Lambda Layer**.

---

## 🐛 **EL PROBLEMA**

### **Error en CloudWatch:**
```
[ERROR] Runtime.ImportModuleError: Unable to import module 'src.handlers.simulate': No module named 'requests'
```

### **Handler Afectado:**
```
src/handlers/simulate.py
```

### **Dependencia Faltante:**
```
requests
```

---

## 🔍 **¿POR QUÉ NO ES DEL FRAMEWORK?**

### **1. El framework NO usa `requests`:**

El SDK de LuminoraCore **NO depende de `requests`**. El error está en el código del backend, específicamente en:

```
src/handlers/simulate.py
```

### **2. El error es de importación:**

El backend está haciendo algo como:

```python
# En src/handlers/simulate.py
import requests  # ❌ Esta librería no está en el Lambda Layer

# ... resto del código
```

---

## 🔧 **SOLUCIÓN PARA EL EQUIPO BACKEND**

### **Opción 1: Agregar `requests` al Lambda Layer (RECOMENDADO)**

**Paso 1:** Agregar `requests` a los requirements del Lambda Layer:

```txt
# En el Lambda Layer
requests==2.31.0
```

**Paso 2:** Reconstruir el Lambda Layer:

```bash
# Reinstalar dependencias
pip install -r requirements.txt -t python/

# Crear el zip del layer
zip -r layer.zip python/

# Actualizar el layer en AWS
aws lambda publish-layer-version \
    --layer-name luminoracore-layer \
    --zip-file fileb://layer.zip \
    --compatible-runtimes python3.11
```

**Paso 3:** Actualizar las funciones Lambda para usar el layer actualizado

---

### **Opción 2: Usar `urllib` (Librería estándar de Python)**

Si solo necesitan hacer peticiones HTTP simples, pueden usar `urllib` que ya viene con Python:

```python
# En lugar de:
import requests

response = requests.get(url)

# Usar:
from urllib.request import urlopen
import json

response = urlopen(url)
data = json.loads(response.read().decode())
```

---

### **Opción 3: Usar `httpx` (Si ya lo tienen)**

Si ya tienen `httpx` en el Lambda Layer (es parte del SDK):

```python
# En lugar de:
import requests

response = requests.get(url)

# Usar:
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get(url)
```

---

## 📁 **ARCHIVO A REVISAR EN EL BACKEND**

El equipo backend debe revisar y corregir este archivo:

```
src/handlers/simulate.py
```

Buscar líneas como:

```python
import requests
from requests import ...
```

---

## 🧪 **VERIFICACIÓN**

### **Cómo verificar que el fix está correcto:**

**Opción 1 - Agregar requests:**
```bash
# Verificar que requests está en el layer
pip list | grep requests

# Debe mostrar:
# requests 2.31.0 (o similar)
```

**Opción 2 - Usar urllib:**
```python
# Este código debe funcionar sin requests
from urllib.request import urlopen

response = urlopen("https://example.com")
print(response.status)
```

---

## 📝 **RESUMEN PARA EL EQUIPO BACKEND**

### **Acción Requerida:**

1. ⚠️ **Identificar** dónde se usa `requests` en el código
2. ✅ **Elegir** una de las tres soluciones:
   - Agregar `requests` al Lambda Layer (más fácil)
   - Usar `urllib` (sin dependencias adicionales)
   - Usar `httpx` (si ya lo tienen)
3. ✅ **Modificar** el código para usar la solución elegida
4. ✅ **Probar** que el error desaparece

### **Archivos a Revisar:**

- `src/handlers/simulate.py` - Archivo principal afectado
- Cualquier otro handler que use `requests`

### **Comando de Búsqueda:**

```bash
# Buscar todos los archivos que usan requests
grep -r "import requests" src/
grep -r "from requests" src/
```

---

## 🎯 **CONCLUSIÓN**

**Problema:** El backend está intentando usar `requests` pero no está en el Lambda Layer  
**Solución:** Agregar `requests` al Lambda Layer o cambiar el código para no usarlo  
**Responsable:** Equipo Backend API  
**Tipo de Error:** Error de configuración/importación, NO es un bug del framework  

---

**Fecha de Identificación:** 2025-01-27  
**Por:** Cursor AI Assistant  
**Revisado por:** [Pendiente]
