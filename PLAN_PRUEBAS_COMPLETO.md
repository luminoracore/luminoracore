# 🧪 PLAN DE PRUEBAS COMPLETO - LUMINORACORE

**Fecha**: 4 de Octubre de 2025  
**Objetivo**: Validar TODAS las características del proyecto antes del lanzamiento  
**Criterio**: "No vamos a lanzar nada que sea una mierda" - Usuario

---

## 📋 ÍNDICE DE PRUEBAS

1. [Motor Base (Core)](#1-motor-base-core)
2. [CLI (Línea de Comandos)](#2-cli-línea-de-comandos)
3. [SDK (Python)](#3-sdk-python)
4. [Providers LLM (7 proveedores)](#4-providers-llm-7-proveedores)
5. [Storage/Memoria (6 opciones)](#5-storagememoria-6-opciones)
6. [Instalación (3 sistemas operativos)](#6-instalación-3-sistemas-operativos)
7. [Documentación](#7-documentación)
8. [Integración End-to-End](#8-integración-end-to-end)

---

## 1. MOTOR BASE (CORE)

### 1.1 Carga de Personalidades ✅
- [ ] Cargar desde archivo JSON válido
- [ ] Cargar desde diccionario Python
- [ ] Cargar desde string JSON
- [ ] Error con archivo inexistente
- [ ] Error con JSON malformado
- [ ] Error con esquema inválido

### 1.2 Validación ✅
- [ ] Validar personalidad completa y válida
- [ ] Validar personalidad mínima válida
- [ ] Detectar campos faltantes requeridos
- [ ] Detectar tipos de datos incorrectos
- [ ] Detectar valores fuera de rango
- [ ] Warnings para campos opcionales vacíos
- [ ] Modo estricto vs. modo permisivo

### 1.3 Compilación para LLMs ✅
- [ ] Compilar para OpenAI (gpt-3.5-turbo, gpt-4)
- [ ] Compilar para Anthropic (claude-3-sonnet, claude-3-opus)
- [ ] Compilar para DeepSeek (deepseek-chat, deepseek-coder)
- [ ] Compilar para Mistral (mistral-tiny, mistral-medium)
- [ ] Compilar para Cohere (command, command-light)
- [ ] Compilar para Google (gemini-pro)
- [ ] Compilar para Llama (llama-2-7b-chat, llama-2-13b)
- [ ] Optimización específica por proveedor
- [ ] Token counting razonable (<5000 tokens para prompts)

### 1.4 PersonaBlend (Mezcla de Personalidades) ✅
- [ ] Mezclar 2 personalidades 50/50
- [ ] Mezclar 2 personalidades 70/30
- [ ] Mezclar 3+ personalidades con pesos personalizados
- [ ] Estrategia de mezcla: average
- [ ] Estrategia de mezcla: dominant
- [ ] Estrategia de mezcla: merge
- [ ] Validar que personalidad mezclada es válida
- [ ] Preservar coherencia semántica

### 1.5 Performance ✅
- [ ] Cargar 10 personalidades en <1 segundo
- [ ] Validar 100 personalidades en <5 segundos
- [ ] Compilar 100 prompts en <10 segundos
- [ ] Sin memory leaks (crear 1000 objetos)

---

## 2. CLI (LÍNEA DE COMANDOS)

### 2.1 Comandos Básicos
- [ ] `luminoracore --version` - Mostrar versión
- [ ] `luminoracore --help` - Ayuda general
- [ ] `luminoracore <comando> --help` - Ayuda por comando

### 2.2 Comando: validate
- [ ] `luminoracore validate <archivo>.json` - Validar archivo
- [ ] `luminoracore validate --strict <archivo>.json` - Modo estricto
- [ ] `luminoracore validate <directorio>/*.json` - Múltiples archivos
- [ ] Salida exitosa con personalidad válida
- [ ] Error claro con personalidad inválida
- [ ] Warnings para campos opcionales

### 2.3 Comando: compile
- [ ] `luminoracore compile <archivo>.json --provider openai`
- [ ] `luminoracore compile <archivo>.json --provider anthropic`
- [ ] `luminoracore compile <archivo>.json --provider deepseek`
- [ ] `luminoracore compile <archivo>.json --provider mistral`
- [ ] `luminoracore compile <archivo>.json --provider cohere`
- [ ] `luminoracore compile <archivo>.json --provider google`
- [ ] `luminoracore compile <archivo>.json --provider llama`
- [ ] `luminoracore compile --output <archivo>.txt`
- [ ] Optimización por proveedor funciona

### 2.4 Comando: create (Wizard Interactivo)
- [ ] `luminoracore create` - Iniciar wizard
- [ ] `luminoracore create --interactive` - Modo interactivo
- [ ] Solicitar todos los campos requeridos
- [ ] Validar entrada del usuario en tiempo real
- [ ] Guardar personalidad generada correctamente
- [ ] Formato JSON válido del archivo generado

### 2.5 Comando: blend
- [ ] `luminoracore blend <file1>.json <file2>.json --ratio 50:50`
- [ ] `luminoracore blend <file1>.json <file2>.json --ratio 70:30`
- [ ] `luminoracore blend <file1>.json <file2>.json <file3>.json`
- [ ] `luminoracore blend --strategy average`
- [ ] `luminoracore blend --strategy dominant`
- [ ] `luminoracore blend --output blended.json`

### 2.6 Comando: serve (Servidor Web Local)
- [ ] `luminoracore serve` - Iniciar servidor (puerto 8080)
- [ ] `luminoracore serve --port 3000` - Puerto personalizado
- [ ] `luminoracore serve --host 0.0.0.0` - Acceso externo
- [ ] Interfaz web accesible en navegador
- [ ] Validación en tiempo real en UI
- [ ] Compilación desde UI
- [ ] Hot-reload funciona

### 2.7 Otros Comandos
- [ ] `luminoracore list` - Listar personalidades instaladas
- [ ] `luminoracore info <archivo>.json` - Mostrar información
- [ ] `luminoracore update <archivo>.json` - Actualizar campos
- [ ] `luminoracore test --provider <provider>` - Test real con API

---

## 3. SDK (PYTHON)

### 3.1 Inicialización del Cliente
- [ ] `LuminoraCoreClient()` - Sin parámetros (defaults)
- [ ] `LuminoraCoreClient(storage_type="memory")` - In-memory
- [ ] `LuminoraCoreClient(storage_type="json")` - JSON file
- [ ] `LuminoraCoreClient(storage_type="sqlite")` - SQLite
- [ ] `LuminoraCoreClient(storage_type="redis")` - Redis
- [ ] `LuminoraCoreClient(storage_type="postgresql")` - PostgreSQL
- [ ] `LuminoraCoreClient(storage_type="mongodb")` - MongoDB
- [ ] Error con storage_type inválido

### 3.2 Gestión de Sesiones
- [ ] `create_session()` - Crear nueva sesión
- [ ] `create_session(session_id="custom")` - ID personalizado
- [ ] `get_session(session_id)` - Obtener sesión existente
- [ ] `delete_session(session_id)` - Eliminar sesión
- [ ] `list_sessions()` - Listar todas las sesiones
- [ ] Error con sesión inexistente

### 3.3 Envío de Mensajes (Sin Memoria)
- [ ] `send_message()` con OpenAI
- [ ] `send_message()` con Anthropic
- [ ] `send_message()` con DeepSeek
- [ ] `send_message()` con Mistral
- [ ] `send_message()` con Cohere
- [ ] `send_message()` con Google
- [ ] `send_message()` con Llama
- [ ] Respuesta en formato `ChatResponse`
- [ ] Manejo de errores de API

### 3.4 Envío de Mensajes (Con Memoria)
- [ ] `send_message()` mantiene contexto en memoria
- [ ] Contexto persiste entre mensajes
- [ ] Contexto se guarda en storage configurado
- [ ] Contexto se recupera al reiniciar

### 3.5 Gestión de Memoria Personalizada
- [ ] `store_memory(key, value)` - Guardar dato
- [ ] `get_memory(key)` - Obtener dato
- [ ] `delete_memory(key)` - Eliminar dato
- [ ] `list_memories()` - Listar todas
- [ ] Memoria persiste en storage configurado

### 3.6 PersonaBlend en Tiempo Real
- [ ] `blend_personalities()` con 2 personalidades
- [ ] `blend_personalities()` con 3+ personalidades
- [ ] `blend_personalities()` con pesos personalizados
- [ ] Cambiar blend dinámicamente durante conversación

### 3.7 Monitoring y Analytics
- [ ] `get_metrics()` - Obtener métricas
- [ ] `get_usage_stats()` - Estadísticas de uso
- [ ] Track de tokens consumidos
- [ ] Track de llamadas por proveedor
- [ ] Track de errores

### 3.8 Async/Await
- [ ] Todas las operaciones asíncronas funcionan
- [ ] `await send_message()` no bloquea
- [ ] Múltiples llamadas concurrentes
- [ ] Manejo correcto de errores async

---

## 4. PROVIDERS LLM (7 PROVEEDORES)

### 4.1 OpenAI
- [ ] Conexión exitosa con API key válida
- [ ] Error claro con API key inválida
- [ ] Modelo: gpt-3.5-turbo funciona
- [ ] Modelo: gpt-4 funciona
- [ ] Streaming funciona
- [ ] Manejo de rate limits
- [ ] Manejo de errores 500

### 4.2 Anthropic (Claude)
- [ ] Conexión exitosa con API key válida
- [ ] Error claro con API key inválida
- [ ] Modelo: claude-3-sonnet funciona
- [ ] Modelo: claude-3-opus funciona
- [ ] Streaming funciona
- [ ] Manejo de rate limits

### 4.3 DeepSeek (IMPORTANTE - Económico)
- [ ] Conexión exitosa con API key válida
- [ ] Error claro con API key inválida
- [ ] Modelo: deepseek-chat funciona
- [ ] Modelo: deepseek-coder funciona
- [ ] Streaming funciona
- [ ] Base URL configurable (`provider_urls.json`)
- [ ] Respuestas en español correctas

### 4.4 Mistral
- [ ] Conexión exitosa con API key válida
- [ ] Modelo: mistral-tiny funciona
- [ ] Modelo: mistral-medium funciona
- [ ] Base URL configurable

### 4.5 Cohere
- [ ] Conexión exitosa con API key válida
- [ ] Modelo: command funciona
- [ ] Modelo: command-light funciona
- [ ] Base URL configurable

### 4.6 Google Gemini
- [ ] Conexión exitosa con API key válida
- [ ] Modelo: gemini-pro funciona
- [ ] Base URL configurable

### 4.7 Llama (vía Replicate)
- [ ] Conexión exitosa con API key de Replicate
- [ ] Modelo: llama-2-7b-chat funciona
- [ ] Modelo: llama-2-13b-chat funciona
- [ ] Base URL configurable

### 4.8 Configuración de URLs (`provider_urls.json`)
- [ ] Archivo `provider_urls.json` existe
- [ ] Todas las URLs de proveedores son válidas
- [ ] Se pueden modificar URLs sin cambiar código
- [ ] Soporta URLs personalizadas (Ollama local, Azure OpenAI)
- [ ] Soporta proxies corporativos

---

## 5. STORAGE/MEMORIA (6 OPCIONES)

### 5.1 Memory (RAM - Sin Persistencia)
- [ ] Crear sesión en memoria
- [ ] Almacenar mensajes en memoria
- [ ] Recuperar historial de mensajes
- [ ] Memoria se pierde al reiniciar
- [ ] Performance: <5ms por operación

### 5.2 JSON File (Simple y Portátil)
- [ ] Crear archivo `sessions.json`
- [ ] Almacenar sesiones en JSON
- [ ] Recuperar sesiones de JSON
- [ ] Persistencia entre reinicios
- [ ] Compresión opcional
- [ ] Performance: <50ms por operación
- [ ] Múltiples clientes: file locking funciona

### 5.3 SQLite (Perfecto para Móviles)
- [ ] Crear base de datos `luminoracore.db`
- [ ] Almacenar sesiones en SQLite
- [ ] Recuperar sesiones de SQLite
- [ ] Persistencia entre reinicios
- [ ] Performance: <20ms por operación
- [ ] Múltiples clientes: locking funciona
- [ ] Portabilidad: archivo único

### 5.4 Redis (Alto Rendimiento)
- [ ] Conexión a Redis local (localhost:6379)
- [ ] Conexión a Redis remoto (con host/port)
- [ ] Almacenar sesiones con TTL
- [ ] Recuperar sesiones
- [ ] Expiración automática
- [ ] Performance: <10ms por operación
- [ ] Múltiples clientes: concurrencia funciona

### 5.5 PostgreSQL (Producción Robusta)
- [ ] Conexión a PostgreSQL local
- [ ] Conexión a PostgreSQL remoto
- [ ] Crear tablas automáticamente
- [ ] Almacenar sesiones
- [ ] Recuperar sesiones
- [ ] Búsqueda por filtros
- [ ] Performance: <30ms por operación
- [ ] Transacciones ACID funcionan

### 5.6 MongoDB (Flexibilidad NoSQL)
- [ ] Conexión a MongoDB local
- [ ] Conexión a MongoDB Atlas
- [ ] Crear colecciones automáticamente
- [ ] Almacenar sesiones
- [ ] Recuperar sesiones
- [ ] Búsqueda por queries complejos
- [ ] Performance: <25ms por operación

---

## 6. INSTALACIÓN (3 SISTEMAS OPERATIVOS)

### 6.1 Windows 10/11
- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado
- [ ] Motor Base: `pip install .` (modo normal)
- [ ] CLI: `pip install -e .` funciona
- [ ] SDK: `pip install ".[all]"` funciona
- [ ] Imports funcionan: `from luminoracore import Personality`
- [ ] Imports funcionan: `from luminoracore_sdk import LuminoraCoreClient`
- [ ] CLI en PATH: `luminoracore --version`
- [ ] Sin conflictos de namespace

### 6.2 Linux (Ubuntu 22.04)
- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado
- [ ] Motor Base: `pip install -e .` funciona
- [ ] CLI: `pip install -e .` funciona
- [ ] SDK: `pip install -e ".[all]"` funciona
- [ ] Imports funcionan correctamente
- [ ] CLI en PATH

### 6.3 macOS (Monterey+)
- [ ] Python 3.8+ instalado (vía Homebrew)
- [ ] Entorno virtual creado
- [ ] Motor Base: `pip install -e .` funciona
- [ ] CLI: `pip install -e .` funciona
- [ ] SDK: `pip install -e ".[all]"` funciona
- [ ] Imports funcionan correctamente
- [ ] CLI en PATH

### 6.4 Scripts de Instalación Automática
- [ ] `instalar_todo.ps1` (Windows) funciona
- [ ] `instalar_todo.sh` (Linux/Mac) funciona
- [ ] `verificar_instalacion.py` funciona
- [ ] Todos los componentes se instalan correctamente

---

## 7. DOCUMENTACIÓN

### 7.1 Guías de Instalación
- [ ] `GUIA_INSTALACION_USO.md` - Completa y clara
- [ ] Instrucciones específicas para Windows
- [ ] Instrucciones específicas para Linux/Mac
- [ ] Troubleshooting detallado
- [ ] Todos los ejemplos funcionan

### 7.2 Guías de Uso
- [ ] `GUIA_CREAR_PERSONALIDADES.md` - Completa
- [ ] `GUIA_VERIFICACION_INSTALACION.md` - Útil
- [ ] `README.md` - Claro y accesible
- [ ] Todos los enlaces funcionan

### 7.3 Documentación Técnica
- [ ] `docs/api_reference.md` - Completa
- [ ] `docs/personality_format.md` - Detallada
- [ ] `docs/best_practices.md` - Útil
- [ ] JSON Schema documentado

### 7.4 Ejemplos de Código
- [ ] `ejemplo_quick_start_core.py` funciona
- [ ] `ejemplo_quick_start_cli.py` funciona
- [ ] `ejemplo_quick_start_sdk.py` funciona
- [ ] `examples/basic_usage.py` funciona
- [ ] `examples/blending_demo.py` funciona
- [ ] Todos los ejemplos tienen comentarios claros

---

## 8. INTEGRACIÓN END-TO-END

### 8.1 Escenario 1: Chatbot Simple (Sin Memoria)
- [ ] Instalar todo desde cero
- [ ] Crear personalidad desde wizard
- [ ] Validar con CLI
- [ ] Compilar para OpenAI
- [ ] SDK: crear sesión
- [ ] SDK: enviar mensaje y recibir respuesta
- [ ] Todo funciona sin errores

### 8.2 Escenario 2: Chatbot con Memoria JSON
- [ ] Configurar storage_type="json"
- [ ] Crear sesión
- [ ] Enviar múltiples mensajes
- [ ] Verificar contexto se mantiene
- [ ] Reiniciar cliente
- [ ] Recuperar sesión
- [ ] Contexto persiste

### 8.3 Escenario 3: App Móvil con SQLite
- [ ] Configurar storage_type="sqlite"
- [ ] Crear múltiples sesiones
- [ ] Enviar mensajes en cada sesión
- [ ] Verificar aislamiento entre sesiones
- [ ] Archivo `.db` se crea correctamente
- [ ] Performance aceptable

### 8.4 Escenario 4: App Web con Redis
- [ ] Configurar storage_type="redis"
- [ ] Múltiples clientes concurrentes
- [ ] Crear sesiones desde distintos clientes
- [ ] Compartir sesión entre clientes
- [ ] Performance bajo carga

### 8.5 Escenario 5: Producción con PostgreSQL
- [ ] Configurar storage_type="postgresql"
- [ ] Migraciones automáticas funcionan
- [ ] Alta carga: 100+ sesiones
- [ ] Backup y restore funciona

### 8.6 Escenario 6: PersonaBlend en Producción
- [ ] Cargar 2 personalidades
- [ ] Mezclar con blend_personalities()
- [ ] Usar personalidad mezclada en conversación
- [ ] Cambiar pesos dinámicamente
- [ ] Respuestas coherentes

### 8.7 Escenario 7: Multi-Provider
- [ ] Configurar 3 proveedores (OpenAI, DeepSeek, Anthropic)
- [ ] Usar cada proveedor en sesiones distintas
- [ ] Comparar respuestas
- [ ] Todos funcionan correctamente

### 8.8 Escenario 8: Producción Real (1 día)
- [ ] Desplegar en servidor
- [ ] 1000+ mensajes procesados
- [ ] Sin errores críticos
- [ ] Performance estable
- [ ] Logs completos

---

## ✅ CRITERIOS DE ACEPTACIÓN

### Mínimo para v1.0:
- ✅ **100% de tests del Motor Base passing**
- ✅ **100% de tests del CLI passing**
- ✅ **100% de tests del SDK passing**
- ✅ **Todos los 7 providers funcionando** (con API keys de prueba)
- ✅ **4 storage types validados**: memory, json, sqlite, redis
- ✅ **Instalación exitosa en Windows y Linux**
- ✅ **Documentación completa y sin errores**
- ✅ **2 escenarios end-to-end exitosos**

### Recomendado para v1.0:
- ✅ **Instalación en macOS validada**
- ✅ **PostgreSQL y MongoDB validados**
- ✅ **6 escenarios end-to-end exitosos**
- ✅ **1 semana de uso en producción sin incidentes**

---

## 📊 TRACKING DE PROGRESO

| Área | Tests Totales | Completados | Fallidos | % Completado |
|------|--------------|-------------|----------|--------------|
| Motor Base | 30 | 0 | 0 | 0% |
| CLI | 40 | 0 | 0 | 0% |
| SDK | 50 | 0 | 0 | 0% |
| Providers | 35 | 1 (DeepSeek) | 0 | 3% |
| Storage | 30 | 0 | 0 | 0% |
| Instalación | 20 | 5 (Windows) | 0 | 25% |
| Documentación | 15 | 10 | 0 | 67% |
| End-to-End | 8 | 0 | 0 | 0% |
| **TOTAL** | **228** | **16** | **0** | **7%** |

---

## 🚀 SIGUIENTE PASO INMEDIATO

1. **Arreglar datos de prueba en `test_1_motor_base.py`** para que cumplan con JSON Schema
2. **Ejecutar Test Suite 1 completo** (Motor Base)
3. **Crear Test Suite 2** (CLI)
4. **Ejecutar tests uno por uno** hasta completar todas las áreas

**Objetivo:** No lanzar nada hasta que **TODOS los tests pasen** y **TODAS las características funcionen**.

---

**Creado por**: AI Assistant  
**Fecha**: 4 de Octubre de 2025  
**Estado**: EN PROGRESO (7% completado)

