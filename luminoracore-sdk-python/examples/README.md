# LuminoraCore SDK Examples

Ejemplos de uso del SDK de LuminoraCore organizados por versión y funcionalidad.

---

## 📋 Índice

### Ejemplos Básicos (v1.0+)
- [`basic_usage.py`](#basic_usagepy) - Uso básico del SDK
- [`simple_usage.py`](#simple_usagepy) - Ejemplo simple paso a paso
- [`personality_blending.py`](#personality_blendingpy) - Mezcla de personalidades

### Ejemplos v1.1 (Legacy - Backward Compatible)
- [`v1_1_sdk_usage.py`](#v1_1_sdk_usagepy) - Todas las features de v1.1
- [`v1_1_complete_memory_example.py`](#v1_1_complete_memory_examplepy) - Sistema de memoria completo
- [`v1_1_complete_real_implementation.py`](#v1_1_complete_real_implementationpy) - Implementación real
- [`v1_1_all_storage_options.py`](#v1_1_all_storage_optionspy) - Todas las opciones de storage

### Ejemplos v1.2.0 (Nuevo)
- [`v1_2_optimization_example.py`](#v1_2_optimization_examplepy) - 🆕 Features de optimización

### Ejemplos Avanzados
- [`voice_bot_dynamic_personality.py`](#voice_bot_dynamic_personalitypy) - Bot de voz con personalidad dinámica

### Integraciones
- [`integrations/fastapi_integration.py`](#integrationsfastapi_integrationpy) - Integración con FastAPI
- [`integrations/streamlit_app.py`](#integrationsstreamlit_apppy) - App Streamlit

---

## 🚀 Ejemplos Básicos

### `basic_usage.py`

**Versión:** v1.0+ (Compatible con v1.2.0)

**Descripción:** Ejemplo básico de uso del SDK.

**Características:**
- ✅ Inicialización del cliente
- ✅ Carga de personalidad
- ✅ Creación de sesión
- ✅ Gestión de memoria
- ✅ Conversación

**Uso:**
```bash
cd luminoracore-sdk-python
python examples/basic_usage.py
```

**Nota:** Este ejemplo funciona con todas las versiones (v1.0, v1.1, v1.2.0).

---

### `simple_usage.py`

**Versión:** v1.0+ (Compatible con v1.2.0)

**Descripción:** Ejemplo simple paso a paso con validación.

**Características:**
- ✅ Inicialización con validación
- ✅ Gestión de personalidades
- ✅ Creación de sesiones
- ✅ Gestión de memoria
- ✅ Mezcla de personalidades

**Uso:**
```bash
python examples/simple_usage.py
```

---

### `personality_blending.py`

**Versión:** v1.0+ (Compatible con v1.2.0)

**Descripción:** Demuestra cómo mezclar múltiples personalidades.

**Características:**
- ✅ Carga de múltiples personalidades
- ✅ Mezcla con pesos personalizados
- ✅ Creación de sesión con personalidad mezclada

**Uso:**
```bash
python examples/personality_blending.py
```

---

## 📦 Ejemplos v1.1 (Legacy)

> **Nota:** Estos ejemplos usan `LuminoraCoreClientV11` y son para backward compatibility.
> En v1.2.0, `LuminoraCoreClient` es la clase principal, pero `LuminoraCoreClientV11` sigue disponible.

### `v1_1_sdk_usage.py`

**Versión:** v1.1 (Compatible con v1.2.0)

**Descripción:** Demuestra todas las features de v1.1.

**Características:**
- ✅ Affinity management
- ✅ Fact management
- ✅ Episode management
- ✅ Sentiment analysis
- ✅ Personality evolution

**Uso:**
```bash
python examples/v1_1_sdk_usage.py
```

---

### `v1_1_complete_memory_example.py`

**Versión:** v1.1 (Compatible con v1.2.0)

**Descripción:** Sistema de memoria completo con todas las operaciones.

**Características:**
- ✅ Save facts (write operations)
- ✅ Retrieve facts (read operations)
- ✅ Delete facts
- ✅ Memory statistics
- ✅ Affinity relationships

**Uso:**
```bash
python examples/v1_1_complete_memory_example.py
```

---

### `v1_1_all_storage_options.py`

**Versión:** v1.1 (Compatible con v1.2.0)

**Descripción:** Demuestra todas las opciones de storage disponibles.

**Storage Options:**
- ✅ SQLite (local file)
- ✅ PostgreSQL (relational)
- ✅ MySQL (relational)
- ✅ MongoDB (document)
- ✅ Redis (key-value)
- ✅ DynamoDB (cloud NoSQL)

**Uso:**
```bash
python examples/v1_1_all_storage_options.py
```

**Nota:** Requiere configurar conexiones para cada storage.

---

## 🆕 Ejemplos v1.2.0

### `v1_2_optimization_example.py`

**Versión:** v1.2.0 (NUEVO)

**Descripción:** Demuestra las nuevas features de optimización.

**Características:**
- ✅ Token reduction (25-45%)
- ✅ Key mapping (abbreviated keys)
- ✅ Compact format (array-based)
- ✅ Deduplication (merge duplicates)
- ✅ Caching (LRU with TTL)

**Requisitos:**
- `luminoracore>=1.2.0` (Core package)
- `luminoracore-sdk>=1.2.0`

**Uso:**
```bash
# Primero instalar Core
cd ../luminoracore
pip install -e .

# Luego ejecutar ejemplo
cd ../luminoracore-sdk-python
python examples/v1_2_optimization_example.py
```

**Código Clave:**
```python
from luminoracore.optimization import OptimizationConfig

opt_config = OptimizationConfig(
    key_abbreviation=True,
    compact_format=True,
    deduplication=True,
    cache_enabled=True
)

client = LuminoraCoreClient(
    storage_config=StorageConfig(storage_type="memory"),
    optimization_config=opt_config  # 🆕 NEW
)
```

---

## 🎯 Ejemplos Avanzados

### `voice_bot_dynamic_personality.py`

**Versión:** v1.0+ (Compatible con v1.2.0)

**Descripción:** Bot de voz con personalidad dinámica usando formato oficial de LuminoraCore.

**Características:**
- ✅ Formato oficial de personalidad
- ✅ Múltiples personalidades
- ✅ Cambio dinámico de personalidad
- ✅ Optimizado para voz

**Uso:**
```bash
python examples/voice_bot_dynamic_personality.py
```

---

## 🔌 Integraciones

### `integrations/fastapi_integration.py`

**Versión:** v1.0+ (Compatible con v1.2.0)

**Descripción:** Integración con FastAPI para crear una API REST.

**Características:**
- ✅ Endpoints REST
- ✅ Gestión de sesiones
- ✅ Chat con personalidades
- ✅ Gestión de memoria

**Uso:**
```bash
python examples/integrations/fastapi_integration.py
```

---

### `integrations/streamlit_app.py`

**Versión:** v1.0+ (Compatible con v1.2.0)

**Descripción:** Aplicación Streamlit para interactuar con personalidades.

**Características:**
- ✅ Interfaz web interactiva
- ✅ Selección de personalidad
- ✅ Chat en tiempo real
- ✅ Visualización de memoria

**Uso:**
```bash
streamlit run examples/integrations/streamlit_app.py
```

---

## 📊 Matriz de Compatibilidad

| Ejemplo | v1.0 | v1.1 | v1.2.0 | Notas |
|---------|------|------|--------|-------|
| `basic_usage.py` | ✅ | ✅ | ✅ | Funciona en todas las versiones |
| `simple_usage.py` | ✅ | ✅ | ✅ | Funciona en todas las versiones |
| `personality_blending.py` | ✅ | ✅ | ✅ | Funciona en todas las versiones |
| `v1_1_*.py` | ⚠️ | ✅ | ✅ | Requiere `LuminoraCoreClientV11` |
| `v1_2_optimization_example.py` | ❌ | ❌ | ✅ | Requiere Core v1.2.0+ |
| `voice_bot_*.py` | ✅ | ✅ | ✅ | Funciona en todas las versiones |
| `integrations/*.py` | ✅ | ✅ | ✅ | Funciona en todas las versiones |

**Leyenda:**
- ✅ Compatible
- ⚠️ Requiere ajustes menores
- ❌ No compatible

---

## 🔧 Configuración

### Requisitos Generales

```bash
# Instalar SDK
cd luminoracore-sdk-python
pip install -e .

# Para ejemplos v1.2.0 (optimization)
cd ../luminoracore
pip install -e .
```

### Variables de Entorno

```bash
# Para ejemplos que usan LLM providers reales
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
# etc.
```

---

## 📝 Notas Importantes

### v1.2.0 Changes

1. **Optimization es opcional:** Los ejemplos básicos funcionan sin optimization.
2. **Backward Compatible:** Código v1.1 funciona sin modificaciones.
3. **Nuevo parámetro:** `optimization_config` en `LuminoraCoreClient` (opcional).

### v1.1 Legacy

1. **`LuminoraCoreClientV11`:** Disponible para backward compatibility.
2. **Storage v1.1:** `InMemoryStorageV11`, `FlexibleSQLiteStorageV11`, etc.
3. **Features v1.1:** Affinity, Facts, Episodes, etc.

---

## 🐛 Troubleshooting

### Error: "luminoracore.optimization not available"

**Solución:**
```bash
cd ../luminoracore
pip install -e .
```

### Error: "LuminoraCoreClientV11 not found"

**Solución:** Este es un ejemplo v1.1. Asegúrate de usar SDK v1.1+ o v1.2.0.

### Error: "Module not found: luminoracore_sdk"

**Solución:**
```bash
cd luminoracore-sdk-python
pip install -e .
```

---

## 📚 Más Información

- **Documentación Principal:** `../README.md`
- **Changelog:** `../CHANGELOG.md`
- **Migration Guide:** `../../MIGRATION_1.1_to_1.2.md`
- **Architecture:** `../../ARCHITECTURE.md`

---

**Última Actualización:** 2025-11-21  
**Versión SDK:** 1.2.0  
**Estado:** ✅ Todos los ejemplos revisados y funcionando

