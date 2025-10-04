# 🧪 ESTRATEGIA DE TESTS - 2 NIVELES

**Fecha**: 4 de Octubre de 2025  
**Aprobado por**: Usuario

---

## 📊 VISIÓN GENERAL

LuminoraCore utiliza una **estrategia de 2 niveles** para tests:

```
┌─────────────────────────────────────────────────────────────┐
│  NIVEL 1: TESTS DE DESARROLLO (Rápidos, cada componente)   │
│                                                             │
│  luminoracore/tests/        → Motor Base                   │
│  luminoracore-cli/tests/    → CLI                          │
│  luminoracore-sdk-python/tests/ → SDK                      │
│                                                             │
│  • Ejecutar durante desarrollo diario                      │
│  • Feedback rápido                                          │
│  • Tests unitarios básicos                                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  NIVEL 2: SUITE DE VALIDACIÓN (Exhaustivos, pre-lanzar)    │
│                                                             │
│  tests/                     → 173 tests completos          │
│                                                             │
│  • Ejecutar ANTES de lanzamiento v1.0                      │
│  • Tests exhaustivos de TODO                                │
│  • APIs reales, DBs reales                                  │
│  • Escenarios end-to-end                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 NIVEL 1: TESTS DE DESARROLLO

### Propósito
Tests **rápidos** para desarrollo diario de cada componente.

### Ubicación y Ejecución

#### Motor Base
```bash
cd luminoracore
pytest tests/ -v

# Archivos:
# - test_personality.py (12 tests)
# - test_validator.py (13 tests)
```

#### CLI
```bash
cd luminoracore-cli
pytest tests/ -v

# Archivos:
# - test_config.py
# - test_validate.py
# - conftest.py (fixtures)
```

#### SDK
```bash
cd luminoracore-sdk-python
pytest tests/ -v

# Archivos:
# - unit/test_client.py
# - integration/test_full_session.py
```

### Características
- ✅ **Rápidos**: < 30 segundos
- ✅ **Mocks**: Usan mocks en lugar de APIs/DBs reales
- ✅ **Unitarios**: Un componente a la vez
- ✅ **Feedback inmediato**: Para desarrollo diario

### Cuándo Ejecutar
- ✅ Después de cada cambio en el código
- ✅ Antes de cada commit
- ✅ Durante desarrollo activo
- ✅ Para debugging rápido

---

## 🏆 NIVEL 2: SUITE DE VALIDACIÓN

### Propósito
Tests **exhaustivos** para validación completa antes del lanzamiento.

### Ubicación y Ejecución

```bash
# Desde la raíz del proyecto
pytest tests/ -v

# O ejecutar suites específicas
pytest tests/test_1_motor_base.py -v
pytest tests/test_2_cli.py -v
pytest tests/test_3_providers.py -v
pytest tests/test_4_storage.py -v
pytest tests/test_5_sessions.py -v
pytest tests/test_6_integration.py -v
```

### Estructura

| Suite | Archivo | Tests | Descripción |
|-------|---------|-------|-------------|
| 1 | `test_1_motor_base.py` | 30 | Motor Base: carga, validación, compilación, blend |
| 2 | `test_2_cli.py` | 25 | CLI: todos los comandos (validate, compile, create, etc.) |
| 3 | `test_3_providers.py` | 49 | Providers: 7 LLMs con APIs **REALES** |
| 4 | `test_4_storage.py` | 36 | Storage: 6 tipos (memory, json, sqlite, redis, pg, mongo) |
| 5 | `test_5_sessions.py` | 25 | Sessions: crear, mensajes, historial, memoria |
| 6 | `test_6_integration.py` | 8 | Integración: escenarios end-to-end completos |
| **TOTAL** | | **173** | |

### Características
- ✅ **Exhaustivos**: Cubren TODAS las características
- ✅ **Reales**: APIs reales, databases reales (no mocks)
- ✅ **Integración**: Tests end-to-end completos
- ✅ **Validación**: Criterios de aceptación para v1.0

### Cuándo Ejecutar
- 🎯 **ANTES del lanzamiento v1.0** (obligatorio)
- 🎯 Antes de merge a `main`
- 🎯 En CI/CD (GitHub Actions)
- 🎯 Para validación de release
- 🎯 Después de cambios arquitectónicos

### Requisitos

```bash
# Dependencias
pip install pytest pytest-asyncio pytest-cov pytest-benchmark

# API Keys (para test_3_providers.py)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="sk-..."
export MISTRAL_API_KEY="..."
export COHERE_API_KEY="..."
export GOOGLE_API_KEY="..."

# Databases (para test_4_storage.py)
docker-compose -f tests/docker-compose.yml up -d
```

---

## ✅ CRITERIOS DE ACEPTACIÓN v1.0

Para lanzar v1.0, la **Suite de Validación** debe cumplir:

### Mínimo Obligatorio
- ✅ **Test Suite 1** (Motor Base): 100% passing
- ✅ **Test Suite 2** (CLI): 100% passing
- ✅ **Test Suite 3** (Providers): ≥ 5/7 providers funcionando
- ✅ **Test Suite 4** (Storage): ≥ 3/6 storage types funcionando (memory, json, sqlite)
- ✅ **Test Suite 5** (Sessions): 100% passing
- ✅ **Test Suite 6** (Integration): ≥ 6/8 escenarios passing

### Ideal
- 🏆 **173/173 tests passing** (100%)
- 🏆 **7/7 providers funcionando**
- 🏆 **6/6 storage types funcionando**
- 🏆 **8/8 escenarios end-to-end**

### Métricas de Calidad
- ✅ **Coverage**: ≥ 70% (ideal 85%+)
- ✅ **Flaky tests**: 0 (tests que fallan intermitentemente)
- ✅ **Tiempo de ejecución**: < 10 minutos (sin APIs reales)
- ✅ **Documentación**: README.md en `tests/` actualizado

---

## 🚀 FLUJO DE TRABAJO

### Durante Desarrollo Diario

```bash
# 1. Trabajas en el Motor Base
cd luminoracore
# ... haces cambios ...

# 2. Ejecutas tests rápidos (Nivel 1)
pytest tests/ -v

# 3. Si pasan, commiteas
git add .
git commit -m "feat: nueva funcionalidad"
```

### Antes de Lanzamiento

```bash
# 1. Asegúrate de estar en la raíz
cd /ruta/a/LuminoraCoreBase

# 2. Ejecuta Suite de Validación completa (Nivel 2)
pytest tests/ -v --cov

# 3. Verifica que TODOS pasen
# Expected: 173 passed in X.XXs

# 4. Si pasan, estás listo para lanzar v1.0
git tag v1.0.0
git push origin v1.0.0
```

---

## 📋 CHECKLIST PRE-LANZAMIENTO

```markdown
- [ ] Tests de Desarrollo (Nivel 1) - Todos passing
  - [ ] luminoracore/tests/ (25 tests)
  - [ ] luminoracore-cli/tests/ (15 tests)
  - [ ] luminoracore-sdk-python/tests/ (27 tests)

- [ ] Suite de Validación (Nivel 2) - Criterios cumplidos
  - [ ] Test Suite 1: Motor Base (30 tests)
  - [ ] Test Suite 2: CLI (25 tests)
  - [ ] Test Suite 3: Providers (≥35/49 tests)
  - [ ] Test Suite 4: Storage (≥18/36 tests)
  - [ ] Test Suite 5: Sessions (25 tests)
  - [ ] Test Suite 6: Integration (≥6/8 tests)

- [ ] Documentación
  - [ ] tests/README.md actualizado
  - [ ] CHANGELOG.md actualizado
  - [ ] README.md con badge de tests

- [ ] CI/CD
  - [ ] GitHub Actions configurado
  - [ ] Tests ejecutándose en 3 OS (Windows, Linux, macOS)
  - [ ] Coverage report generado

- [ ] Manual
  - [ ] Instalación validada en 3 OS
  - [ ] Ejemplos ejecutados manualmente
  - [ ] Documentación revisada
```

---

## 🔧 MANTENIMIENTO

### Agregar Nuevo Test de Desarrollo (Nivel 1)

1. Identifica el componente (motor, CLI, SDK)
2. Ve al directorio de tests apropiado
3. Agrega el test en el archivo existente
4. Ejecuta: `pytest tests/ -v`

### Agregar Nuevo Test de Validación (Nivel 2)

1. Identifica la suite correcta (1-6)
2. Agrega el test en `tests/test_X_nombre.py`
3. Actualiza el contador en `tests/README.md`
4. Ejecuta: `pytest tests/test_X_nombre.py -v`

### Actualizar Criterios de Aceptación

1. Edita este archivo (`ESTRATEGIA_TESTS.md`)
2. Comunica los cambios al equipo
3. Actualiza `tests/README.md` si es necesario

---

## 🎓 FILOSOFÍA

> **"No lanzaremos nada que sea una mierda."**
> 
> Los tests no son solo código que valida código.
> Son nuestra **garantía de calidad** y **promesa al usuario**.
> 
> - **Nivel 1**: Velocidad para iterar rápido
> - **Nivel 2**: Confianza para lanzar sin miedo

**Ambos niveles son igualmente importantes.**

---

## 📞 CONTACTO

**Preguntas sobre tests**: Ver `tests/README.md`

**Issues con tests**: GitHub Issues con label "tests"

**Proponer nuevos tests**: Pull Request con actualización de esta estrategia

---

**Última actualización**: 2025-01-04  
**Versión**: 1.0  
**Estado**: ✅ Aprobado e implementado

