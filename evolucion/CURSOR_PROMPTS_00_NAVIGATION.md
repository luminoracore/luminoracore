# 🤖 CURSOR AI - Sistema de Prompts LuminoraCore

**Framework:** LuminoraCore v1.1 → v2.0  
**Timeline Total:** 20-22 meses (8 fases)  
**Versión Documentación:** 1.0  
**Fecha:** 18 de Noviembre, 2025

---

## ⚠️ LEE ESTO PRIMERO - INSTRUCCIONES CRÍTICAS

### Para Cursor AI: REGLAS DE ORO

```
┌─────────────────────────────────────────────────────────────┐
│                    REGLAS INQUEBRANTABLES                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. NO ALUCINES                                              │
│     → Si algo no está claro, DETENTE y pregunta            │
│                                                              │
│  2. NO ASUMAS                                                │
│     → Usa exactamente los nombres especificados             │
│     → Usa exactamente las rutas especificadas               │
│     → Usa exactamente las estructuras especificadas         │
│                                                              │
│  3. NO CAMBIES ARQUITECTURA                                  │
│     → Sigue la estructura exacta del proyecto               │
│     → No reorganices archivos sin permiso                   │
│                                                              │
│  4. SÍ VALIDA TODO                                           │
│     → Ejecuta tests después de cada cambio                  │
│     → Verifica sintaxis antes de continuar                  │
│     → Ejecuta el código de prueba incluido                  │
│                                                              │
│  5. SÍ PREGUNTA                                              │
│     → Si hay conflicto con código existente                 │
│     → Si algo parece ambiguo                                │
│     → Si los tests fallan inesperadamente                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Cómo Usar Este Sistema

```
ESTRUCTURA DE DOCUMENTOS:

/
├── CURSOR_PROMPTS_00_NAVIGATION.md       ◄── ESTÁS AQUÍ
├── CURSOR_PROMPTS_01_PHASE_1.md          ◄── Semanas 1-4
├── CURSOR_PROMPTS_02_PHASE_2.md          ◄── Semanas 5-16
├── CURSOR_PROMPTS_03_PHASE_3.md          ◄── Semanas 17-28
├── CURSOR_PROMPTS_04_PHASE_4.md          ◄── Semanas 29-40
└── CURSOR_PROMPTS_05_PHASES_5_8.md       ◄── Semanas 41-88

CADA DOCUMENTO CONTIENE:
✅ Contexto de la fase
✅ Objetivos claros
✅ Prompts paso a paso
✅ Código completo para cada archivo
✅ Validaciones obligatorias
✅ Criterios de éxito
✅ Solución de problemas
```

---

## 📂 ESTRUCTURA DEL PROYECTO LUMINORACORE

### Estructura Actual (v1.1 - EXISTENTE)

```
luminoracore/
├── luminoracore/                    # Core framework
│   ├── __init__.py
│   ├── core.py                      # PersonalityCore, PersonaBlend
│   ├── sdk.py                       # SDK con LLM providers
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── fact_extractor.py       # Extracción de facts
│   │   └── storage/
│   │       ├── __init__.py
│   │       ├── base.py              # Base storage interface
│   │       ├── memory_storage.py   # In-memory
│   │       ├── json_storage.py     # JSON files
│   │       ├── sqlite_storage.py   # SQLite
│   │       ├── postgres_storage.py # PostgreSQL
│   │       ├── redis_storage.py    # Redis
│   │       └── mongodb_storage.py  # MongoDB
│   ├── affinity/
│   │   ├── __init__.py
│   │   └── tracker.py               # Affinity tracking
│   └── types/
│       ├── __init__.py
│       └── models.py                # Data models
├── tests/
│   ├── test_core.py
│   ├── test_sdk.py
│   ├── test_memory/
│   ├── test_affinity/
│   └── conftest.py
├── examples/
│   ├── basic_usage.py
│   └── advanced_personablend.py
├── docs/
│   └── API.md
├── pyproject.toml
├── requirements.txt
└── README.md
```

### Estructura Nueva (Fase 1 en adelante)

```
luminoracore/
├── luminoracore/
│   ├── optimization/                # ← FASE 1 (NUEVO)
│   │   ├── __init__.py
│   │   ├── key_mapping.py           # Semana 1
│   │   ├── minifier.py              # Semana 1
│   │   ├── compact_format.py        # Semana 2
│   │   ├── deduplicator.py          # Semana 3
│   │   └── cache.py                 # Semana 3
│   ├── search/                      # ← FASE 2 (NUEVO)
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── semantic_search.py
│   ├── graph/                       # ← FASE 3 (NUEVO)
│   │   ├── __init__.py
│   │   ├── entity_extractor.py
│   │   └── graph_builder.py
│   └── compression/                 # ← FASE 4 (NUEVO)
│       ├── __init__.py
│       ├── tiered_memory.py
│       └── llm_compression.py
├── tests/
│   ├── test_optimization/           # ← FASE 1 (NUEVO)
│   │   ├── __init__.py
│   │   ├── test_key_mapping.py
│   │   ├── test_minifier.py
│   │   ├── test_compact_format.py
│   │   ├── test_deduplicator.py
│   │   └── test_cache.py
│   ├── test_search/                 # ← FASE 2 (NUEVO)
│   ├── test_graph/                  # ← FASE 3 (NUEVO)
│   └── test_compression/            # ← FASE 4 (NUEVO)
└── docs/
    ├── optimization/                # ← FASE 1 (NUEVO)
    │   └── MIGRATION_GUIDE.md
    ├── search/                      # ← FASE 2 (NUEVO)
    └── graph/                       # ← FASE 3 (NUEVO)
```

---

## 🔄 FLUJO DE TRABAJO POR FASE

### Proceso General para Cada Fase

```
┌─────────────────────────────────────────────────────────────┐
│                    WORKFLOW POR FASE                         │
└─────────────────────────────────────────────────────────────┘

PASO 1: PREPARACIÓN
├─ Lee el documento completo de la fase
├─ Entiende los objetivos
├─ Verifica dependencies cumplidas
└─ Verifica que tests actuales pasan (100%)

PASO 2: IMPLEMENTACIÓN SEMANAL
├─ Sigue los prompts semana por semana
├─ NO te saltes pasos
├─ NO combines semanas
└─ Implementa cada archivo según especificación

PASO 3: VALIDACIÓN CONTINUA
├─ Después de cada archivo: verificar sintaxis
├─ Después de cada módulo: ejecutar tests
├─ Después de cada semana: validación completa
└─ Mantén 100% tests passing

PASO 4: DOCUMENTACIÓN
├─ Actualiza docstrings
├─ Actualiza README si necesario
├─ Crea migration guides si necesario
└─ Actualiza changelog

PASO 5: INTEGRACIÓN
├─ Integra con código existente
├─ Valida backward compatibility
├─ Ejecuta suite completa de tests
└─ Performance benchmarks
```

---

## 🎯 ORDEN DE EJECUCIÓN - MAPA DE DEPENDENCIAS

```
┌─────────────────────────────────────────────────────────────┐
│              DEPENDENCIAS ENTRE FASES                        │
└─────────────────────────────────────────────────────────────┘

v1.1 (ACTUAL - 85% Complete)
    │
    │ READY ✅
    │
    ├──► FASE 1: Quick Wins (4 semanas)
    │      └─ Independiente, sin dependencies
    │         └─ OUTPUT: 25-45% token reduction
    │
    ├──► FASE 2: Semantic Search (12 semanas)
    │      └─ REQUIERE: Fase 1 completa
    │         └─ OUTPUT: Natural language queries
    │
    ├──► FASE 3: Knowledge Graphs (12 semanas)
    │      └─ REQUIERE: Fase 2 completa
    │         └─ OUTPUT: Relationship detection
    │
    ├──► FASE 4: Compression (12 semanas) ⚠️ CRÍTICA
    │      └─ REQUIERE: Fase 1, 2, 3 completas
    │         └─ OUTPUT: 75-80% token reduction
    │
    ├──► FASE 5: Micro-Personalities (12 semanas)
    │      └─ REQUIERE: Fase 4 completa
    │
    ├──► FASE 6: Auto-Learning (12 semanas)
    │      └─ REQUIERE: Fase 5 completa
    │
    ├──► FASE 7: Production Optimization (12 semanas)
    │      └─ REQUIERE: Fase 6 completa
    │
    └──► FASE 8: API SaaS Launch (12 semanas)
           └─ REQUIERE: Fase 7 completa
              └─ OUTPUT: v2.0 API Production Ready
```

---

## 📋 CHECKLIST ANTES DE EMPEZAR CUALQUIER FASE

```
ANTES DE ABRIR EL DOCUMENTO DE UNA FASE, VERIFICA:

Setup Inicial:
  ☐ Python 3.11+ instalado
  ☐ Git configurado
  ☐ Virtual environment creado y activado
  ☐ Requirements instalados: pip install -r requirements.txt
  ☐ Tests actuales pasan: pytest tests/ -v

Código Base:
  ☐ Repositorio clonado
  ☐ Branch creado para la fase: git checkout -b phase-X-nombre
  ☐ Código limpio (no uncommitted changes)
  ☐ Backup realizado (por si acaso)

Tools:
  ☐ Editor configurado (VS Code / Cursor)
  ☐ pytest instalado
  ☐ pytest-cov instalado (coverage)
  ☐ mypy instalado (type checking - opcional)

Documentación:
  ☐ Leído README.md del proyecto
  ☐ Leído EXECUTIVE-SUMMARY.md del roadmap
  ☐ Leído 00-PROJECT-MANAGER-INDEX.md
  ☐ Entendido estructura del proyecto

Conocimiento:
  ☐ Entiendes qué es LuminoraCore
  ☐ Entiendes los objetivos de la fase
  ☐ Tienes claro qué se va a implementar
  ☐ Sabes qué archivos se van a crear/modificar

SI TODOS LOS CHECKBOXES ESTÁN MARCADOS:
  → PROCEDE a abrir el documento de la fase
  
SI ALGUNO NO ESTÁ MARCADO:
  → DETENTE y completa lo que falta
```

---

## 🚀 COMENZAR IMPLEMENTACIÓN

### Fase Actual: FASE 1 - Quick Wins

```
STATUS: 🟡 READY TO START
DOCUMENTO: CURSOR_PROMPTS_01_PHASE_1.md

ANTES DE ABRIR ESE DOCUMENTO:
1. ☐ Verifica checklist arriba está completa
2. ☐ Crea branch: git checkout -b phase-1-quick-wins
3. ☐ Lee objetivos de Fase 1:
      - Token reduction 25-45%
      - Sin breaking changes
      - 4 semanas de trabajo
4. ☐ Prepara tiempo: 4 semanas de implementación
5. ☐ Confirma que v1.1 está funcionando (pytest tests/)

CUANDO TODO ESTÉ LISTO:
→ ABRE: CURSOR_PROMPTS_01_PHASE_1.md
→ SIGUE: Los prompts en orden exacto
```

---

## 📊 SISTEMA DE VALIDACIÓN

### Comandos de Validación por Nivel

```bash
# NIVEL 1: Verificación de Sintaxis (Después de crear archivo)
python -m py_compile path/to/file.py

# NIVEL 2: Tests Unitarios (Después de completar módulo)
pytest tests/test_modulo/test_file.py -v

# NIVEL 3: Tests de Integración (Después de completar semana)
pytest tests/test_modulo/ -v

# NIVEL 4: Suite Completa (Después de completar fase)
pytest tests/ -v

# NIVEL 5: Coverage (Para verificar calidad)
pytest --cov=luminoracore tests/ --cov-report=term-missing

# NIVEL 6: Type Checking (Opcional pero recomendado)
mypy luminoracore/ --ignore-missing-imports
```

### Criterios de Éxito Universales

```
PARA CONSIDERAR UNA TAREA COMPLETADA:

Código:
  ☐ Sintaxis correcta (py_compile sin errores)
  ☐ No hay imports faltantes
  ☐ Docstrings completos
  ☐ Type hints incluidos
  ☐ Código sigue PEP 8

Tests:
  ☐ 100% tests pasan
  ☐ Coverage ≥ 90%
  ☐ Edge cases cubiertos
  ☐ Integration tests incluidos

Funcionalidad:
  ☐ Cumple especificación exacta
  ☐ Backward compatible (si aplica)
  ☐ Performance aceptable
  ☐ No hay regressions

Documentación:
  ☐ Docstrings completos
  ☐ Examples funcionan
  ☐ README actualizado (si aplica)
```

---

## 🔧 TROUBLESHOOTING GENERAL

### Problemas Comunes y Soluciones

```
PROBLEMA: ImportError - No module named 'luminoracore.optimization'
SOLUCIÓN:
  1. Verifica que existe luminoracore/optimization/__init__.py
  2. Verifica que __init__.py exporta las funciones
  3. Reinstala en modo editable: pip install -e .

PROBLEMA: Tests fallan con "fixture not found"
SOLUCIÓN:
  1. Verifica que tests/conftest.py existe
  2. Verifica imports en el test file
  3. Ejecuta pytest con -v para más detalles

PROBLEMA: "File already exists"
SOLUCIÓN:
  1. Si es intencional: rm archivo_existente
  2. Si no es intencional: verifica que estás siguiendo orden correcto

PROBLEMA: Syntax errors después de copiar código
SOLUCIÓN:
  1. Verifica indentación (usa espacios, no tabs)
  2. Verifica comillas (no uses smart quotes del procesador)
  3. Ejecuta: python -m py_compile archivo.py

PROBLEMA: Tests pasan localmente pero fallan en CI
SOLUCIÓN:
  1. Verifica dependencies en requirements.txt
  2. Verifica paths relativos vs absolutos
  3. Verifica que no dependes de archivos locales
```

### Comandos de Emergencia

```bash
# REVERTIR CAMBIOS
git checkout -- archivo.py  # Revertir un archivo
git reset --hard HEAD       # Revertir todos los cambios (¡cuidado!)

# REEJECUTAR TESTS LIMPIOS
pytest --cache-clear tests/ -v

# VER QUÉ TESTS FALLAN
pytest tests/ -v --tb=short  # Traceback corto
pytest tests/ -v --tb=long   # Traceback completo

# DEBUG DE UN TEST ESPECÍFICO
pytest tests/test_file.py::test_function -v -s  # -s muestra prints

# VERIFICAR COVERAGE DE UN MÓDULO
pytest --cov=luminoracore.optimization tests/test_optimization/ -v

# LIMPIAR CACHE DE PYTHON
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

---

## 📝 FORMATO DE COMMIT MESSAGES

### Convención de Commits

```
FORMATO: <tipo>(<scope>): <descripción>

TIPOS:
  feat:     Nueva funcionalidad
  fix:      Bug fix
  docs:     Cambios en documentación
  test:     Añadir/modificar tests
  refactor: Refactoring sin cambiar funcionalidad
  perf:     Mejoras de performance
  chore:    Tareas de mantenimiento

EJEMPLOS:
  feat(optimization): implementar key_mapping.py
  test(optimization): añadir tests para key_mapping
  docs(optimization): actualizar README con ejemplos
  fix(optimization): corregir bug en compress_keys
  refactor(optimization): mejorar performance de minifier

COMMITS PROHIBIDOS:
  ❌ "Update"
  ❌ "Fix stuff"
  ❌ "WIP"
  ❌ "asdfasdf"
```

---

## 🎓 RECURSOS ADICIONALES

### Documentación del Proyecto

```
ANTES DE IMPLEMENTAR, LEE:
  ├─ README.md (del proyecto LuminoraCore)
  ├─ docs/API.md
  └─ Roadmap documents:
      ├─ EXECUTIVE-SUMMARY.md
      ├─ 00-PROJECT-MANAGER-INDEX.md
      └─ 01-08-PHASE-*.md (según fase)

DURANTE IMPLEMENTACIÓN:
  ├─ Python docs: https://docs.python.org/3/
  ├─ pytest docs: https://docs.pytest.org/
  └─ Type hints: https://mypy.readthedocs.io/

PARA DUDAS ESPECÍFICAS:
  ├─ LLM APIs: docs de OpenAI, Anthropic, etc.
  ├─ Storage: docs de SQLite, PostgreSQL, Redis, MongoDB
  └─ Vector DBs (Fase 2+): docs de Pinecone, Weaviate, etc.
```

---

## 🚦 SIGUIENTE PASO

```
┌─────────────────────────────────────────────────────────────┐
│                    AHORA PROCEDE A:                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📄 CURSOR_PROMPTS_01_PHASE_1.md                            │
│                                                              │
│  CONTIENE:                                                   │
│    ✅ 4 semanas de prompts detallados                       │
│    ✅ Código completo para cada archivo                     │
│    ✅ Validaciones paso a paso                              │
│    ✅ Criterios de éxito claros                             │
│                                                              │
│  EMPEZARÁS CON:                                              │
│    → Semana 1: key_mapping.py + minifier.py                 │
│    → Objetivo: 15-20% token reduction                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘

🚀 LISTO PARA COMENZAR?
   → Abre CURSOR_PROMPTS_01_PHASE_1.md
   → Sigue Prompt 1.1
   → Implementa paso a paso
```

---

**Versión:** 1.0  
**Última Actualización:** 18 de Noviembre, 2025  
**Mantenido Por:** LuminoraCore Team  
**Contacto:** https://github.com/luminoracore (cuando esté público)

---

