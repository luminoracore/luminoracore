# LuminoraCore SDK - Tests

Suite de tests completa para validar funcionalidad del SDK.

---

## 📋 Estructura de Tests

### Tests Unitarios (`unit/`)

#### `test_client.py`
**Propósito:** Tests unitarios del cliente principal.

**Cobertura:**
- ✅ Inicialización del cliente
- ✅ Gestión de sesiones
- ✅ Gestión de personalidades
- ✅ Manejo de errores

---

### Tests de Integración (`integration/`)

#### `test_sdk_core_e2e.py`
**Propósito:** Tests end-to-end que validan SDK + Core.

**Cobertura:**
- ✅ Integration con Core optimizer
- ✅ Integration con Core PersonaBlend
- ✅ Integration con Core MemorySystem
- ✅ Storage con optimization
- ✅ Backward compatibility

**Requisitos:**
- `luminoracore>=1.2.0` (Core package)
- Se salta automáticamente si Core no está disponible

#### `test_full_session.py`
**Propósito:** Tests de sesiones completas.

**Cobertura:**
- ✅ Creación de sesiones
- ✅ Envío de mensajes
- ✅ Gestión de conversaciones
- ✅ Gestión de memoria

---

### Tests de Features

#### `test_personality_adapter.py`
**Propósito:** Tests para PersonaBlendAdapter.

**Cobertura:**
- ✅ Inicialización del adapter
- ✅ Conversión SDK → Core
- ✅ Conversión Core → SDK
- ✅ Blending de personalidades
- ✅ Validación de inputs
- ✅ Roundtrip conversion

**Requisitos:**
- `luminoracore>=1.2.0` (Core package)
- Se salta automáticamente si Core no está disponible

#### `test_personality_blender.py`
**Propósito:** Tests para PersonalityBlender.

**Cobertura:**
- ✅ Uso del adapter internamente
- ✅ Delegación al adapter
- ✅ Fallback si adapter no disponible
- ✅ Cache de blends
- ✅ Backward compatibility

#### `test_optimization_integration.py`
**Propósito:** Tests de integración con Core optimizer.

**Cobertura:**
- ✅ Client con optimization config
- ✅ Client sin optimization (backward compat)
- ✅ Storage wrapped con optimizer
- ✅ Optimization stats
- ✅ OptimizedStorageWrapper

**Requisitos:**
- `luminoracore>=1.2.0` (Core package)
- Se salta automáticamente si Core no está disponible

#### `test_backward_compatibility.py`
**Propósito:** Tests de backward compatibility.

**Cobertura:**
- ✅ Código v1.0/v1.1 sigue funcionando
- ✅ API pública idéntica
- ✅ Comportamiento consistente
- ✅ Sin breaking changes

**Importante:** Estos tests son CRÍTICOS. Si alguno falla, se rompió backward compatibility.

#### `test_memory_manager.py`
**Propósito:** Tests para MemoryManager.

**Cobertura:**
- ✅ Integration con Core MemorySystem
- ✅ Store/retrieve memories
- ✅ Clear memory
- ✅ Get stats
- ✅ Fallback si Core no disponible

#### `test_memory_with_optimization.py`
**Propósito:** Tests de memoria con optimization.

**Cobertura:**
- ✅ Memory con optimization enabled
- ✅ Compression/expansion transparente
- ✅ Stats con optimization
- ✅ Cache hits/misses

**Requisitos:**
- `luminoracore>=1.2.0` (Core package)

---

### Tests v1.1

#### `test_step_8_storage_v1_1.py`
**Propósito:** Tests para storage v1.1.

**Cobertura:**
- ✅ InMemoryStorageV11
- ✅ Operaciones de storage v1.1

#### `test_step_9_types.py`
**Propósito:** Tests para tipos v1.1.

**Cobertura:**
- ✅ Memory types
- ✅ Relationship types
- ✅ Snapshot types

#### `test_step_10_memory_v1_1.py`
**Propósito:** Tests para memory v1.1.

**Cobertura:**
- ✅ MemoryManagerV11
- ✅ Operaciones de memoria v1.1

#### `test_step_11_client_v1_1.py`
**Propósito:** Tests para client v1.1.

**Cobertura:**
- ✅ LuminoraCoreClientV11
- ✅ Features v1.1 completas

#### `test_complete_memory_operations.py`
**Propósito:** Tests completos de operaciones de memoria.

**Cobertura:**
- ✅ WRITE operations (save facts/episodes)
- ✅ READ operations (get facts/episodes)
- ✅ DELETE operations
- ✅ SEARCH operations
- ✅ ANALYTICS

---

## 🧪 Ejecutar Tests

### Todos los tests

```bash
# Desde directorio del SDK
cd luminoracore-sdk-python

# Ejecutar todos los tests
pytest tests/

# Con coverage
pytest tests/ --cov=luminoracore_sdk --cov-report=html

# Con verbose
pytest tests/ -v
```

### Tests específicos

```bash
# Tests de integración
pytest tests/integration/

# Tests unitarios
pytest tests/unit/

# Test específico
pytest tests/test_personality_adapter.py

# Test específico con verbose
pytest tests/test_backward_compatibility.py -v
```

### Con markers

```bash
# Solo tests que requieren Core
pytest tests/ -m "core"

# Solo tests que no requieren Core
pytest tests/ -m "not core"

# Tests asyncio
pytest tests/ -m "asyncio"
```

---

## 📊 Cobertura de Tests

### Cobertura por Módulo

| Módulo | Cobertura | Tests |
|--------|-----------|-------|
| **Client** | ✅ Alta | `test_client.py`, `test_sdk_core_e2e.py` |
| **Personality** | ✅ Alta | `test_personality_adapter.py`, `test_personality_blender.py` |
| **Memory** | ✅ Alta | `test_memory_manager.py`, `test_memory_with_optimization.py` |
| **Storage** | ✅ Media | `test_optimization_integration.py`, `test_step_8_storage_v1_1.py` |
| **Session** | ✅ Media | `test_full_session.py` |
| **Optimization** | ✅ Alta | `test_optimization_integration.py`, `test_memory_with_optimization.py` |
| **Backward Compat** | ✅ Crítica | `test_backward_compatibility.py` |

---

## 🎯 Tests Críticos

### Tests que DEBEN pasar siempre

1. **`test_backward_compatibility.py`**
   - ✅ CRÍTICO: Si falla, rompimos backward compatibility
   - ✅ Valida código v1.0/v1.1 sigue funcionando

2. **`test_personality_adapter.py`**
   - ✅ CRÍTICO: Valida adapter funciona con Core
   - ✅ Valida conversiones SDK ↔ Core

3. **`test_optimization_integration.py`**
   - ✅ CRÍTICO: Valida optimization funciona
   - ✅ Valida storage wrapping

4. **`test_sdk_core_e2e.py`**
   - ✅ CRÍTICO: Valida toda la stack funciona junta
   - ✅ Valida Core integration completa

---

## 🔧 Configuración

### Requisitos

```bash
# Instalar dependencias de tests
pip install pytest pytest-asyncio pytest-cov

# Para tests de integration con Core
pip install -e ../luminoracore/
```

### pytest.ini

```ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    asyncio: marks tests as async
    core: marks tests that require Core package
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

---

## 🐛 Troubleshooting

### Error: "luminoracore not available"

**Causa:** Core package no está instalado.

**Solución:**
```bash
# Instalar Core
cd ../luminoracore
pip install -e .
```

**Nota:** Algunos tests se saltan automáticamente si Core no está disponible.

### Error: "Module not found: luminoracore_sdk"

**Solución:**
```bash
# Instalar SDK
cd luminoracore-sdk-python
pip install -e .
```

### Error: "pytest not found"

**Solución:**
```bash
pip install pytest pytest-asyncio pytest-cov
```

### Error: "asyncio mode not set"

**Solución:** Asegúrate de tener `pytest-asyncio` instalado y `pytest.ini` configurado.

---

## 📈 Estadísticas

### Total de Tests

- **Unit Tests:** ~52 tests
- **Integration Tests:** ~12 tests
- **Backward Compatibility:** ~10 tests
- **Total:** ~74 tests

### Cobertura

- **Cobertura objetivo:** ≥90%
- **Cobertura actual:** ~85-90% (varía según módulo)

---

## 📚 Más Información

- **SDK Documentation:** `../README.md`
- **API Reference:** `../docs/api_reference.md`
- **Architecture:** `../../ARCHITECTURE.md`
- **Migration Guide:** `../../MIGRATION_1.1_to_1.2.md`

---

**Última Actualización:** 2025-11-21  
**Versión SDK:** 1.2.0  
**Estado:** ✅ Suite de tests completa y funcionando

