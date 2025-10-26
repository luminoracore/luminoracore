# Guía de Creación de Capas Docker para AWS Lambda
## Nueva Arquitectura LuminoraCore - Impacto en Capas

**Fecha**: 2025-01-25  
**Estado**: ✅ ARQUITECTURA ACTUALIZADA - GUÍA ACTUALIZADA  
**Compatibilidad**: 100% MANTENIDA

---

## 🎯 **Respuesta Directa a tu Pregunta**

### **✅ El proceso de creación de capas Docker NO ha cambiado**
### **✅ Pueden usar el mismo Dockerfile que tenían**
### **✅ Solo necesitan actualizar la ruta del SDK**

---

## 📋 **Dockerfile Actualizado para la Nueva Arquitectura**

### **Opción 1: Usar Solo el Core (Recomendado para Nuevos Proyectos)**
```dockerfile
FROM public.ecr.aws/lambda/python:3.11

# Copiar solo el core (más ligero)
COPY luminoracore /tmp/luminoracore

# Instalar dependencias del core
RUN pip install --upgrade pip
RUN pip install -t /asset/python /tmp/luminoracore --no-cache-dir

# Limpiar archivos temporales
RUN rm -rf /tmp/luminoracore /usr/local/lib/python3.11/site-packages/*

# Configurar variables de entorno
ENV PYTHONPATH=/asset/python
```

### **Opción 2: Usar SDK Completo (Recomendado para Compatibilidad)**
```dockerfile
FROM public.ecr.aws/lambda/python:3.11

# Copiar SDK completo (incluye core)
COPY luminoracore-sdk-python /tmp/luminoracore-sdk-python

# Instalar dependencias del SDK
RUN pip install --upgrade pip
RUN pip install -t /asset/python /tmp/luminoracore-sdk-python --no-cache-dir

# Limpiar archivos temporales
RUN rm -rf /tmp/luminoracore-sdk-python /usr/local/lib/python3.11/site-packages/*

# Configurar variables de entorno
ENV PYTHONPATH=/asset/python
```

### **Opción 3: Usar Ambos (Core + SDK) - Para Máxima Flexibilidad**
```dockerfile
FROM public.ecr.aws/lambda/python:3.11

# Copiar core
COPY luminoracore /tmp/luminoracore

# Copiar SDK
COPY luminoracore-sdk-python /tmp/luminoracore-sdk-python

# Instalar core primero
RUN pip install --upgrade pip
RUN pip install -t /asset/python /tmp/luminoracore --no-cache-dir

# Instalar SDK (depende del core)
RUN pip install -t /asset/python /tmp/luminoracore-sdk-python --no-cache-dir

# Limpiar archivos temporales
RUN rm -rf /tmp/luminoracore /tmp/luminoracore-sdk-python /usr/local/lib/python3.11/site-packages/*

# Configurar variables de entorno
ENV PYTHONPATH=/asset/python
```

---

## 🔄 **Comparación: Antes vs Después**

### **ANTES (Arquitectura Incorrecta):**
```dockerfile
# ❌ Arquitectura incorrecta - SDK dependía de sí mismo
FROM public.ecr.aws/lambda/python:3.11
COPY luminoracore-sdk-python /tmp/luminoracore-sdk-python
RUN pip install -t /asset/python /tmp/luminoracore-sdk-python --no-cache-dir
```

### **DESPUÉS (Arquitectura Correcta):**
```dockerfile
# ✅ Arquitectura correcta - SDK usa core independiente
FROM public.ecr.aws/lambda/python:3.11
COPY luminoracore-sdk-python /tmp/luminoracore-sdk-python
RUN pip install -t /asset/python /tmp/luminoracore-sdk-python --no-cache-dir
```

**¡El Dockerfile es exactamente el mismo!** La diferencia está en la arquitectura interna, no en cómo se instala.

---

## 📊 **Análisis de Dependencias**

### **Core (luminoracore/) - Dependencias Mínimas:**
```txt
# Solo dependencias esenciales
jsonschema>=4.17.2
pydantic>=2.0.0
pyyaml>=6.0

# Dependencias opcionales (solo si se usan)
# psycopg2-binary>=2.9.0  # PostgreSQL
# boto3>=1.26.0          # DynamoDB
# redis>=4.5.0           # Redis
# pymongo>=4.3.0        # MongoDB
```

### **SDK (luminoracore-sdk-python/) - Dependencias:**
```txt
# Depende del core
luminoracore>=1.0.0,<2.0.0

# Dependencias del SDK
pydantic>=2.0.0,<3.0.0
httpx>=0.24.0,<1.0.0
aiofiles>=23.0.0,<24.0.0
typing-extensions>=4.5.0; python_version<"3.11"
tenacity>=8.2.0,<9.0.0
structlog>=23.1.0,<24.0.0
opentelemetry-api>=1.18.0,<2.0.0
opentelemetry-sdk>=1.18.0,<2.0.0
```

---

## 🚀 **Recomendaciones por Caso de Uso**

### **Para APIs Simples (Solo Core):**
```dockerfile
# Usar solo core - más ligero
FROM public.ecr.aws/lambda/python:3.11
COPY luminoracore /tmp/luminoracore
RUN pip install -t /asset/python /tmp/luminoracore --no-cache-dir
```

**Ventajas:**
- ✅ **Más ligero** (menos dependencias)
- ✅ **Mejor rendimiento** (menos overhead)
- ✅ **Más rápido** (menos código para cargar)

### **Para APIs Complejas (SDK Completo):**
```dockerfile
# Usar SDK completo - más funcionalidades
FROM public.ecr.aws/lambda/python:3.11
COPY luminoracore-sdk-python /tmp/luminoracore-sdk-python
RUN pip install -t /asset/python /tmp/luminoracore-sdk-python --no-cache-dir
```

**Ventajas:**
- ✅ **Más funcionalidades** (cliente completo)
- ✅ **Mejor compatibilidad** (APIs existentes)
- ✅ **Más fácil de usar** (interfaz simplificada)

### **Para Migración Gradual (Híbrido):**
```dockerfile
# Usar ambos - máxima flexibilidad
FROM public.ecr.aws/lambda/python:3.11
COPY luminoracore /tmp/luminoracore
COPY luminoracore-sdk-python /tmp/luminoracore-sdk-python
RUN pip install -t /asset/python /tmp/luminoracore --no-cache-dir
RUN pip install -t /asset/python /tmp/luminoracore-sdk-python --no-cache-dir
```

**Ventajas:**
- ✅ **Máxima flexibilidad** (pueden usar ambos)
- ✅ **Migración gradual** (pueden cambiar gradualmente)
- ✅ **Futuro-proof** (preparado para cambios futuros)

---

## 📋 **Scripts de Construcción de Capas**

### **Script para Core Solo:**
```bash
#!/bin/bash
# build-core-layer.sh

echo "Building LuminoraCore layer (core only)..."

# Crear directorio temporal
mkdir -p temp-layer
cd temp-layer

# Copiar core
cp -r ../luminoracore .

# Crear Dockerfile
cat > Dockerfile << EOF
FROM public.ecr.aws/lambda/python:3.11
COPY luminoracore /tmp/luminoracore
RUN pip install --upgrade pip
RUN pip install -t /asset/python /tmp/luminoracore --no-cache-dir
RUN rm -rf /tmp/luminoracore /usr/local/lib/python3.11/site-packages/*
ENV PYTHONPATH=/asset/python
EOF

# Construir imagen
docker build -t luminoracore-core-layer .

# Extraer capa
docker run --rm -v $(pwd):/output luminoracore-core-layer cp -r /asset /output/

echo "Core layer built successfully!"
```

### **Script para SDK Completo:**
```bash
#!/bin/bash
# build-sdk-layer.sh

echo "Building LuminoraCore layer (SDK complete)..."

# Crear directorio temporal
mkdir -p temp-layer
cd temp-layer

# Copiar SDK
cp -r ../luminoracore-sdk-python .

# Crear Dockerfile
cat > Dockerfile << EOF
FROM public.ecr.aws/lambda/python:3.11
COPY luminoracore-sdk-python /tmp/luminoracore-sdk-python
RUN pip install --upgrade pip
RUN pip install -t /asset/python /tmp/luminoracore-sdk-python --no-cache-dir
RUN rm -rf /tmp/luminoracore-sdk-python /usr/local/lib/python3.11/site-packages/*
ENV PYTHONPATH=/asset/python
EOF

# Construir imagen
docker build -t luminoracore-sdk-layer .

# Extraer capa
docker run --rm -v $(pwd):/output luminoracore-sdk-layer cp -r /asset /output/

echo "SDK layer built successfully!"
```

---

## 🔧 **Configuración en AWS Lambda**

### **Variables de Entorno:**
```bash
# Configurar PYTHONPATH
PYTHONPATH=/opt/python

# Configurar logging (opcional)
LUMINORACORE_LOG_LEVEL=INFO
LUMINORACORE_LOG_FORMAT=json
```

### **Configuración de IAM:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteItem",
                "dynamodb:Query",
                "dynamodb:Scan"
            ],
            "Resource": "arn:aws:dynamodb:*:*:table/luminoracore-*"
        }
    ]
}
```

---

## 📊 **Comparación de Tamaños de Capa**

| Opción | Tamaño Estimado | Dependencias | Rendimiento |
|--------|----------------|--------------|-------------|
| **Core Solo** | ~15-20 MB | Mínimas | ⚡⚡⚡ Excelente |
| **SDK Completo** | ~25-30 MB | Completas | ⚡⚡ Muy Bueno |
| **Híbrido** | ~30-35 MB | Completas | ⚡⚡ Muy Bueno |

---

## 🎯 **Recomendación Final**

### **Para el Equipo de Backend:**

1. **Usar el mismo Dockerfile** que tenían antes
2. **Solo cambiar la ruta** del SDK (si es necesario)
3. **El proceso es idéntico** - no hay cambios en la metodología
4. **La arquitectura interna** es mejor, pero transparente para ellos

### **Dockerfile Recomendado:**
```dockerfile
FROM public.ecr.aws/lambda/python:3.11
COPY luminoracore-sdk-python /tmp/luminoracore-sdk-python
RUN pip install --upgrade pip
RUN pip install -t /asset/python /tmp/luminoracore-sdk-python --no-cache-dir
RUN rm -rf /tmp/luminoracore-sdk-python /usr/local/lib/python3.11/site-packages/*
ENV PYTHONPATH=/asset/python
```

**¡Es exactamente el mismo Dockerfile que tenían antes!**

---

## ✅ **Conclusión**

**El proceso de creación de capas Docker NO ha cambiado.** La nueva arquitectura es interna y transparente para el equipo de backend. Pueden usar exactamente el mismo proceso que tenían antes.

**La única diferencia es que ahora la arquitectura es correcta internamente, lo que proporciona mejor rendimiento y estabilidad.**

---

*Guía actualizada para la nueva arquitectura LuminoraCore - 2025-01-25*
