# 🔧 PLAN DE REFACTORING: Separación de Namespaces

## 🎯 Objetivo

Separar correctamente el Motor Base y el SDK en namespaces independientes para eliminar conflictos.

**Decisión**: OPCIÓN A - SDK con namespace diferente
**Fecha**: 2025-01-04
**Estado**: 🟡 EN PROGRESO

---

## 📊 CAMBIOS REQUERIDOS

### 1. Renombrar Namespace del SDK

**ANTES**:
```
luminoracore-sdk-python/
└── luminoracore/          ← Conflicto con motor base
    ├── __init__.py
    ├── client.py
    ├── providers/
    ├── session/
    ├── types/
    └── utils/
```

**DESPUÉS**:
```
luminoracore-sdk-python/
└── luminoracore_sdk/      ← Namespace único
    ├── __init__.py
    ├── client.py
    ├── providers/
    ├── session/
    ├── types/
    └── utils/
```

### 2. Actualizar setup.py del SDK

**ANTES**:
```python
setup(
    name="luminoracore-sdk",
    packages=find_packages(),
    # No depende del motor base
)
```

**DESPUÉS**:
```python
setup(
    name="luminoracore-sdk",
    packages=find_packages(),
    install_requires=[
        'luminoracore>=0.1.0',  # ← Dependencia explícita
        'httpx>=0.24.0',
        # ...
    ]
)
```

### 3. Actualizar Imports en SDK

**Archivos a modificar**: ~50 archivos

**Pattern de cambio**:
```python
# ANTES
from luminoracore.providers import BaseProvider
from luminoracore.types import ProviderConfig

# DESPUÉS  
from luminoracore_sdk.providers import BaseProvider
from luminoracore_sdk.types import ProviderConfig
```

**Archivos críticos**:
- `luminoracore_sdk/__init__.py`
- `luminoracore_sdk/client.py`
- `luminoracore_sdk/providers/*.py` (9 archivos)
- `luminoracore_sdk/session/*.py` (5 archivos)
- `luminoracore_sdk/types/*.py` (6 archivos)
- `luminoracore_sdk/utils/*.py` (7 archivos)

### 4. Actualizar Documentación

**Archivos a modificar**:
- `GUIA_INSTALACION_USO.md`
- `README.md`
- `INICIO_RAPIDO.md`
- `docs/api_reference.md`
- `luminoracore-sdk-python/README.md`

**Cambios en ejemplos**:
```python
# ANTES
from luminoracore import LuminoraCoreClient

# DESPUÉS
from luminoracore import Personality  # Motor base
from luminoracore_sdk import LuminoraCoreClient  # SDK
```

### 5. Actualizar Tests

**Archivos a modificar**:
- `tests/test_1_motor_base.py` - NO cambia (solo usa motor base)
- `tests/test_3_providers.py` - Actualizar imports del SDK
- `tests/test_4_storage.py` - Actualizar imports del SDK
- `tests/test_5_sessions.py` - Actualizar imports del SDK
- `tests/test_6_integration.py` - Actualizar ambos imports
- `test_all_providers.py` - Actualizar imports del SDK
- `test_real.py` - Actualizar imports del SDK

### 6. Actualizar Scripts de Ejemplo

**Archivos a modificar**:
- `ejemplo_quick_start_sdk.py`
- `ejemplo_quick_start_cli.py` (si usa SDK)

---

## 📝 CHECKLIST DE IMPLEMENTACIÓN

### Fase 1: Renombrar y Reorganizar (2 horas)

- [ ] Renombrar `luminoracore-sdk-python/luminoracore/` → `luminoracore_sdk/`
- [ ] Actualizar `setup.py` con dependencia del motor base
- [ ] Actualizar `luminoracore_sdk/__init__.py`
- [ ] Verificar que no queden referencias al namespace viejo

### Fase 2: Actualizar Imports Internos del SDK (3 horas)

- [ ] `luminoracore_sdk/client.py`
- [ ] `luminoracore_sdk/providers/` (9 archivos)
- [ ] `luminoracore_sdk/session/` (5 archivos)
- [ ] `luminoracore_sdk/types/` (6 archivos)
- [ ] `luminoracore_sdk/utils/` (7 archivos)
- [ ] `luminoracore_sdk/monitoring/` (4 archivos)
- [ ] `luminoracore_sdk/personality/` (4 archivos)

### Fase 3: Actualizar Tests (1 hora)

- [ ] `test_all_providers.py`
- [ ] `test_real.py`
- [ ] `tests/test_3_providers.py`
- [ ] `tests/test_4_storage.py`
- [ ] `tests/test_5_sessions.py`
- [ ] `tests/test_6_integration.py`

### Fase 4: Actualizar Documentación (2 horas)

- [ ] `GUIA_INSTALACION_USO.md`
- [ ] `README.md`
- [ ] `INICIO_RAPIDO.md`
- [ ] `luminoracore-sdk-python/README.md`
- [ ] `docs/api_reference.md`

### Fase 5: Actualizar Scripts de Ejemplo (1 hora)

- [ ] `ejemplo_quick_start_sdk.py`
- [ ] `verificar_instalacion.py`

### Fase 6: Testing y Validación (2 horas)

- [ ] Desinstalar todo: `pip uninstall luminoracore luminoracore-sdk -y`
- [ ] Instalar motor base: `pip install -e luminoracore/`
- [ ] Instalar SDK: `pip install -e luminoracore-sdk-python/`
- [ ] Verificar instalación: `python verificar_instalacion.py`
- [ ] Ejecutar tests: `python run_tests.py --suite 1`
- [ ] Probar ejemplo real: `python test_real.py`
- [ ] Probar todos los providers: `python test_all_providers.py`

---

## 🎯 RESULTADO ESPERADO

### Instalación Final

```bash
# Motor Base (independiente)
pip install luminoracore

# SDK (depende del motor base)
pip install luminoracore-sdk

# O ambos en desarrollo
pip install -e luminoracore/
pip install -e luminoracore-sdk-python/
```

### Imports Finales

```python
# Motor Base
from luminoracore import (
    Personality,
    PersonalityValidator,
    PersonalityCompiler,
    LLMProvider,
    PersonaBlend
)

# SDK
from luminoracore_sdk import (
    LuminoraCoreClient,
    ProviderConfig,
    StorageConfig,
    SessionConfig
)

# Uso combinado
personality = Personality("my_bot.json")  # Motor base
client = LuminoraCoreClient()  # SDK
session = client.create_session(...)  # SDK usa personalidad del motor base
```

---

## ⚠️ BREAKING CHANGES

### Para Usuarios Existentes

**ANTES (v0.x)**:
```python
from luminoracore import LuminoraCoreClient  # ❌ Ya no funciona
```

**DESPUÉS (v1.0)**:
```python
from luminoracore_sdk import LuminoraCoreClient  # ✅ Correcto
```

### Migration Guide

```python
# Actualizar imports
# Buscar y reemplazar en tu código:

# Motor Base - NO cambia
from luminoracore import Personality  # ✅ Sigue igual

# SDK - SÍ cambia
# ANTES:
from luminoracore import LuminoraCoreClient
from luminoracore.types import ProviderConfig

# DESPUÉS:
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types import ProviderConfig
```

---

## 📊 ESTIMACIÓN DE TIEMPO

| Fase | Tiempo | Prioridad |
|------|--------|-----------|
| 1. Renombrar | 2h | 🔴 CRÍTICO |
| 2. Imports SDK | 3h | 🔴 CRÍTICO |
| 3. Tests | 1h | 🟡 ALTO |
| 4. Docs | 2h | 🟡 ALTO |
| 5. Ejemplos | 1h | 🟡 ALTO |
| 6. Validación | 2h | 🔴 CRÍTICO |
| **TOTAL** | **11h** | |

**ETA**: 1.5 días de trabajo concentrado

---

## 🚀 SIGUIENTE ACCIÓN

**AHORA**: Iniciar Fase 1 - Renombrar namespace del SDK

```bash
cd luminoracore-sdk-python
mv luminoracore luminoracore_sdk
# Actualizar setup.py
# Actualizar __init__.py
```

---

## 📝 LOG DE PROGRESO

### 2025-01-04 23:30 - Inicio
- ✅ Plan de refactoring creado
- ✅ Decisión aprobada por el equipo
- ⏳ Fase 1 iniciando...

---

**Última actualización**: 2025-01-04 23:30  
**Estado**: 🟡 EN PROGRESO - Fase 1  
**Responsable**: Core Team  
**Review**: Requerido antes de merge a main

