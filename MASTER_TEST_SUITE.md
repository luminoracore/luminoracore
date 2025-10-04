# 🧪 MASTER TEST SUITE - LuminoraCore

## 🎯 Objetivo

**Probar CADA funcionalidad prometida antes de lanzar.**

> "No lanzaremos nada que sea una mierda. Se probarán todas las características exhaustivamente."  
> — Decisión del equipo, 2025-01-04

---

## 📊 SCOPE COMPLETO

### ✅ Áreas a Probar

1. **Motor Base (luminoracore)**
   - Carga de personalidades (JSON, dict)
   - Validación (schema, errores)
   - Compilación para 7 LLMs
   - PersonaBlend (mezcla de personalidades)
   - Manejo de errores

2. **CLI (luminoracore-cli)**
   - Todos los comandos
   - Wizard interactivo
   - Servidor web local
   - Validación de archivos
   - Compilación por línea de comandos

3. **SDK (luminoracore-sdk-python)**
   - Inicialización de cliente
   - Gestión de sesiones
   - Envío de mensajes
   - 7 LLM Providers
   - 6 Storage Types
   - Manejo de errores
   - Performance

---

## 🔬 TEST SUITE 1: MOTOR BASE

### Script: `test_1_motor_base.py`

**Pruebas:**

1. **Carga de Personalidades**
   - ✅ Cargar desde archivo JSON válido
   - ✅ Cargar desde diccionario Python
   - ✅ Manejo de archivo inexistente
   - ✅ Manejo de JSON inválido
   - ✅ Manejo de schema incorrecto

2. **Validación**
   - ✅ Personalidad válida (sin errores)
   - ✅ Personalidad con warnings
   - ✅ Personalidad inválida (errores)
   - ✅ Validación estricta vs permisiva
   - ✅ Mensajes de error claros

3. **Compilación**
   - ✅ Compilar para OpenAI
   - ✅ Compilar para Anthropic
   - ✅ Compilar para DeepSeek
   - ✅ Compilar para Mistral
   - ✅ Compilar para Cohere
   - ✅ Compilar para Google
   - ✅ Compilar para Llama
   - ✅ Token counting correcto
   - ✅ Optimización por provider

4. **PersonaBlend**
   - ✅ Mezclar 2 personalidades (50/50)
   - ✅ Mezclar 2 personalidades (70/30)
   - ✅ Mezclar 3+ personalidades
   - ✅ Estrategias de mezcla
   - ✅ Validar personalidad mezclada

5. **Performance**
   - ✅ Carga < 100ms
   - ✅ Validación < 50ms
   - ✅ Compilación < 200ms
   - ✅ No memory leaks

**Estimado**: 30 test cases, ~15 minutos

---

## 🔬 TEST SUITE 2: CLI

### Script: `test_2_cli.py`

**Pruebas:**

1. **Comando: list**
   - ✅ `luminoracore list`
   - ✅ `luminoracore list --detailed`
   - ✅ Directorio vacío
   - ✅ Directorio con personalidades

2. **Comando: validate**
   - ✅ `luminoracore validate <file.json>`
   - ✅ Archivo válido
   - ✅ Archivo inválido
   - ✅ Archivo inexistente
   - ✅ `--strict` mode

3. **Comando: compile**
   - ✅ `luminoracore compile <file.json> --provider openai`
   - ✅ Todos los 7 providers
   - ✅ `--output <file>` guarda resultado
   - ✅ Manejo de errores

4. **Comando: create**
   - ✅ `luminoracore create <name>` (no interactivo)
   - ✅ Template generado es válido
   - ✅ Archivo creado correctamente

5. **Comando: blend**
   - ✅ `luminoracore blend <file1:0.5> <file2:0.5>`
   - ✅ `--output` guarda resultado
   - ✅ Resultado es válido

6. **Comando: info**
   - ✅ `luminoracore info <file.json>`
   - ✅ Muestra metadata correcta
   - ✅ Token counts por provider

7. **Comando: serve**
   - ⚠️ Manual test (requiere navegador)
   - Puerto configurable
   - Interfaz web accesible

8. **Comando: init**
   - ✅ `luminoracore init`
   - ✅ Crea estructura de proyecto
   - ✅ Config files correctos

**Estimado**: 25 test cases, ~10 minutos

---

## 🔬 TEST SUITE 3: SDK - PROVIDERS

### Script: `test_3_providers.py`

**Pruebas por cada provider:**

1. **OpenAI** (gpt-3.5-turbo)
   - ✅ Conexión exitosa
   - ✅ Envío de mensaje
   - ✅ Respuesta correcta
   - ✅ Token counting
   - ✅ Manejo de rate limits
   - ✅ Manejo de API key inválida
   - ✅ Manejo de red caída

2. **Anthropic** (claude-3-haiku)
   - [Mismas pruebas que OpenAI]

3. **DeepSeek** (deepseek-chat)
   - [Mismas pruebas que OpenAI]

4. **Mistral** (mistral-tiny)
   - [Mismas pruebas que OpenAI]

5. **Cohere** (command)
   - [Mismas pruebas que OpenAI]

6. **Google** (gemini-pro)
   - [Mismas pruebas que OpenAI]

7. **Llama** (llama-2-7b via Replicate)
   - [Mismas pruebas que OpenAI]

**Estimado**: 49 test cases (7 providers × 7 tests), ~20 minutos

---

## 🔬 TEST SUITE 4: SDK - STORAGE TYPES

### Script: `test_4_storage.py`

**Pruebas por cada storage:**

1. **Memory (RAM)**
   - ✅ Crear sesión
   - ✅ Guardar mensajes
   - ✅ Recuperar historial
   - ✅ Limpiar conversación
   - ✅ Se pierde al cerrar (esperado)

2. **JSON File**
   - ✅ Crear sesión
   - ✅ Guardar mensajes
   - ✅ Recuperar historial
   - ✅ Persistencia entre reinicios
   - ✅ Archivo JSON válido
   - ✅ Manejo de archivo corrupto

3. **SQLite**
   - ✅ Crear sesión
   - ✅ Guardar mensajes
   - ✅ Recuperar historial
   - ✅ Persistencia entre reinicios
   - ✅ Database schema correcto
   - ✅ Concurrent access

4. **Redis**
   - ✅ Conexión exitosa
   - ✅ Crear sesión
   - ✅ Guardar mensajes
   - ✅ Recuperar historial
   - ✅ TTL/expiration
   - ✅ Manejo de Redis caído

5. **PostgreSQL**
   - ✅ Conexión exitosa
   - ✅ Crear sesión
   - ✅ Guardar mensajes
   - ✅ Recuperar historial
   - ✅ Transactions
   - ✅ Manejo de DB caída

6. **MongoDB**
   - ✅ Conexión exitosa
   - ✅ Crear sesión
   - ✅ Guardar mensajes
   - ✅ Recuperar historial
   - ✅ Document schema
   - ✅ Manejo de Mongo caído

**Estimado**: 36 test cases (6 storage × 6 tests), ~15 minutos

---

## 🔬 TEST SUITE 5: SDK - SESSION MANAGEMENT

### Script: `test_5_sessions.py`

**Pruebas:**

1. **Ciclo de Vida de Sesión**
   - ✅ Crear sesión
   - ✅ Obtener info de sesión
   - ✅ Listar sesiones activas
   - ✅ Actualizar configuración
   - ✅ Eliminar sesión
   - ✅ Session ID único

2. **Conversación**
   - ✅ Enviar mensaje
   - ✅ Múltiples mensajes en secuencia
   - ✅ Obtener historial completo
   - ✅ Obtener últimos N mensajes
   - ✅ Limpiar conversación
   - ✅ Context window management

3. **Memoria de Usuario**
   - ✅ Guardar memoria (`store_memory`)
   - ✅ Recuperar memoria (`get_memory`)
   - ✅ Actualizar memoria
   - ✅ Eliminar memoria
   - ✅ Persistencia según storage type

4. **Personality Management**
   - ✅ Cargar personalidad
   - ✅ Cambiar personalidad mid-session
   - ✅ Validar personalidad antes de usar
   - ✅ PersonaBlend en sesión

5. **Error Handling**
   - ✅ Sesión inexistente
   - ✅ Provider timeout
   - ✅ API key inválida
   - ✅ Rate limit exceeded
   - ✅ Network error
   - ✅ Storage error

**Estimado**: 25 test cases, ~10 minutos

---

## 🔬 TEST SUITE 6: INTEGRATION & E2E

### Script: `test_6_integration.py`

**Escenarios Reales:**

1. **Chatbot Simple**
   - Usuario envía 10 mensajes
   - Assistant responde coherentemente
   - Historial se mantiene
   - Memoria funciona

2. **Multi-Session**
   - 5 sesiones simultáneas
   - Diferentes personalidades
   - Sin cross-contamination
   - Performance estable

3. **Personality Switching**
   - Empezar con personalidad A
   - Cambiar a personalidad B
   - Comportamiento cambia
   - Historial se mantiene

4. **Blended Personality**
   - Crear blend 50/50
   - Usar en sesión
   - Comportamiento mezclado observable

5. **Long Conversation**
   - 50+ mensajes
   - Context window handling
   - Performance estable
   - Memoria no crece descontroladamente

6. **Storage Migration**
   - Empezar con memory
   - Migrar a JSON
   - Migrar a SQLite
   - Data integrity

7. **Provider Fallback**
   - Provider primario falla
   - Fallback a secundario
   - Usuario no nota interrupción

8. **Stress Test**
   - 100 mensajes en 1 minuto
   - 10 sesiones paralelas
   - No memory leaks
   - No crashes

**Estimado**: 8 scenarios, ~30 minutos

---

## 🔬 TEST SUITE 7: INSTALLATION & DOCS

### Manual Testing

**Instalación:**

1. **Windows 10/11**
   - [ ] VM limpia
   - [ ] Seguir GUIA_INSTALACION_USO.md
   - [ ] `verificar_instalacion.py` todo verde
   - [ ] Quick starts funcionan
   - [ ] Tiempo < 15 minutos

2. **Ubuntu 22.04**
   - [ ] Docker limpio
   - [ ] Seguir guía
   - [ ] Verificación OK
   - [ ] Quick starts OK

3. **macOS Ventura/Sonoma**
   - [ ] Mac limpia
   - [ ] Seguir guía
   - [ ] Verificación OK
   - [ ] Quick starts OK

**Documentación:**

1. **Ejemplos de Código**
   - [ ] Copiar/pegar cada ejemplo de docs
   - [ ] Ejecutar sin modificación
   - [ ] Produce resultado esperado

2. **Links**
   - [ ] Revisar todos los links (automated)
   - [ ] 0 links rotos

3. **Screenshots**
   - [ ] Actualizados
   - [ ] Correspondientes al código actual

**Estimado**: 2 horas (manual)

---

## 📊 RESUMEN DE COBERTURA

| Test Suite | Test Cases | Tiempo Estimado | Prioridad |
|------------|------------|-----------------|-----------|
| 1. Motor Base | 30 | 15 min | 🔴 CRÍTICO |
| 2. CLI | 25 | 10 min | 🟡 ALTO |
| 3. Providers | 49 | 20 min | 🔴 CRÍTICO |
| 4. Storage | 36 | 15 min | 🔴 CRÍTICO |
| 5. Sessions | 25 | 10 min | 🟡 ALTO |
| 6. Integration | 8 | 30 min | 🔴 CRÍTICO |
| 7. Installation | Manual | 2 horas | 🟡 ALTO |
| **TOTAL** | **173** | **~3.5 horas** | |

---

## 🎯 CRITERIOS DE ÉXITO

### Para Lanzar v1.0, TODOS deben pasar:

- ✅ **Motor Base**: 30/30 tests passing
- ✅ **CLI**: 25/25 tests passing
- ✅ **Providers**: 49/49 tests passing (o 7/7 providers funcionando)
- ✅ **Storage**: 36/36 tests passing (o 6/6 storage types funcionando)
- ✅ **Sessions**: 25/25 tests passing
- ✅ **Integration**: 8/8 scenarios passing
- ✅ **Installation**: 3/3 OS instalaciones exitosas
- ✅ **Docs**: 0 links rotos, todos los ejemplos funcionan

**NO SE LANZA SI:**
- ❌ Cualquier test crítico falla
- ❌ Más de 2 providers no funcionan
- ❌ Cualquier storage type no funciona
- ❌ Instalación falla en cualquier OS principal
- ❌ Ejemplos de docs no funcionan

---

## 🚀 PLAN DE EJECUCIÓN

### Semana 1: Test Suites Automáticos

**Día 1**: Motor Base
- Crear `test_1_motor_base.py`
- Ejecutar y arreglar errores
- 30/30 passing

**Día 2**: CLI
- Crear `test_2_cli.py`
- Ejecutar y arreglar errores
- 25/25 passing

**Día 3**: Providers
- Crear `test_3_providers.py`
- Configurar todas las API keys
- Ejecutar y arreglar errores
- 49/49 passing (o documentar providers que fallan)

**Día 4**: Storage
- Crear `test_4_storage.py`
- Setup Redis, PostgreSQL, MongoDB (Docker)
- Ejecutar y arreglar errores
- 36/36 passing

**Día 5**: Sessions & Integration
- Crear `test_5_sessions.py`
- Crear `test_6_integration.py`
- Ejecutar y arreglar errores
- 33/33 passing

### Semana 2: Testing Manual & Docs

**Día 1**: Windows Testing
- VM limpia
- Instalación completa
- Documentar problemas
- Arreglar

**Día 2**: Linux Testing
- Docker Ubuntu
- Instalación completa
- Arreglar

**Día 3**: macOS Testing
- Mac limpia
- Instalación completa
- Arreglar

**Día 4**: Documentación
- Probar cada ejemplo
- Verificar links
- Actualizar screenshots
- Corregir

**Día 5**: Buffer/Fixes
- Arreglar issues encontrados
- Re-test críticos

### Semana 3: Beta Testing & Final Validation

**Día 1-3**: Beta Testing Externo
- 5-10 usuarios externos
- Observar instalación
- Recolectar feedback
- Bugs críticos

**Día 4**: Final Test Run
- Ejecutar TODA la suite completa
- Verificar 173/173 passing
- Decisión GO/NO-GO

**Día 5**: Release Preparation
- Changelog
- Release notes
- Tag v1.0.0
- Publicar

---

## 📝 TRACKING

### Estado Actual: 🔴 PRE-ALPHA

- ✅ DeepSeek provider validado (1/7)
- ⚠️ Arquitectura corregida
- ⚠️ Instalación funciona en Windows
- ❌ 0/173 tests automáticos existentes
- ❌ 6/7 providers sin probar
- ❌ 6/6 storage types sin probar
- ❌ CLI sin validación exhaustiva
- ❌ Motor Base sin test suite

### Próximo Hito: 🟡 ALPHA

**Objetivo**: Core funcionalidad validada

**Requisitos**:
- ✅ Test Suite 1 (Motor Base): 30/30
- ✅ Test Suite 3 (Providers): 21/49 (3 providers funcionando)
- ✅ Test Suite 4 (Storage): 12/36 (memory, json, sqlite)
- ✅ Instalación Windows: OK

**ETA**: 1 semana

### Hito Final: 🟢 v1.0 PRODUCTION

**Objetivo**: TODO validado

**Requisitos**: TODOS los criterios de éxito

**ETA**: 3 semanas

---

## 🔧 HERRAMIENTAS

### Test Framework

```python
# pytest para tests automáticos
pip install pytest pytest-asyncio pytest-cov

# Ejecución
pytest test_1_motor_base.py -v
pytest test_2_cli.py -v
pytest test_3_providers.py -v
pytest test_4_storage.py -v
pytest test_5_sessions.py -v
pytest test_6_integration.py -v

# Coverage
pytest --cov=luminoracore --cov-report=html

# Todos los tests
pytest tests/ -v --cov
```

### CI/CD

```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python: ['3.9', '3.10', '3.11']
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python }}
      - run: pip install -e .[all]
      - run: pytest tests/ -v
```

---

## 📞 RESPONSABILIDADES

**Test Suite Owner**: Asegurar que los tests se ejecutan y pasan

**Provider Integration**: Configurar y validar cada provider

**Storage Integration**: Setup de DBs y validación

**Documentation**: Verificar ejemplos y links

**CI/CD**: Mantener pipeline funcionando

---

**Última actualización**: 2025-01-04  
**Estado**: 🔴 Iniciando validación exhaustiva  
**Decisión**: NO LANZAR hasta pasar todos los tests

