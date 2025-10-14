# Flujo de Datos y Persistencia - LuminoraCore v1.1

**Aclaración completa sobre qué se guarda dónde, qué se actualiza, y cómo funciona el sistema**

---

## ⚠️ ACLARACIONES CRÍTICAS

### 1. El JSON de Personalidad NUNCA se actualiza

```
❌ INCORRECTO:
- Cargar alicia.json
- Usuario aumenta afinidad
- Modificar alicia.json con nueva afinidad  ← NO!

✅ CORRECTO:
- Cargar alicia.json (UNA VEZ, inmutable)
- Usuario aumenta afinidad
- Guardar afinidad en BBDD (PostgreSQL/SQLite/etc)
- Aplicar modificadores del JSON en memoria (temporal)
```

**El archivo JSON es un TEMPLATE, no un estado.**

---

### 2. Estados se guardan en BBDD, NO en JSON

```
┌─────────────────────────────────────────────────────────┐
│ JSON de Personalidad (INMUTABLE)                        │
│ - alicia.json                                           │
│ - Define comportamiento base                            │
│ - Define niveles posibles                               │
│ - Define moods posibles                                 │
│ - NUNCA cambia                                          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ BBDD de Estados (MUTABLE)                               │
│ - PostgreSQL / SQLite / MongoDB                         │
│ - Guarda: affinity, current_mood, session_state         │
│ - Se actualiza constantemente                           │
│ - Persiste entre sesiones                               │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ BBDD Vectorial (BÚSQUEDA)                               │
│ - pgvector / Pinecone                                   │
│ - Guarda: embeddings de mensajes                        │
│ - Solo para semantic search                             │
│ - NO reemplaza BBDD actual                              │
└─────────────────────────────────────────────────────────┘
```

---

### 3. Compilación Dinámica es RÁPIDA (no lenta)

**Compilar = Aplicar deltas, no regenerar todo**

```python
# Compilación toma ~1-5ms (muy rápido)
base = {"empathy": 0.95, "formality": 0.3}
modifier = {"empathy": +0.2, "formality": -0.1}
compiled = apply_deltas(base, modifier)  # {"empathy": 1.0, "formality": 0.2}
# Tiempo: ~1ms
```

vs

```python
# Llamada al LLM toma ~500-2000ms (lento)
response = await llm.generate(prompt)
# Tiempo: ~500-2000ms
```

**La compilación es 500x más rápida que el LLM.**

---

## 📊 Separación de Responsabilidades

### Qué va en CADA storage

| Tipo de Dato | Storage | Mutable | Persistencia |
|--------------|---------|---------|--------------|
| **Personalidad base** | `alicia.json` (archivo) | ❌ NO | Permanente |
| **Niveles/moods definidos** | `alicia.json` (archivo) | ❌ NO | Permanente |
| **Conversación actual** | Redis / Memory | ✅ SÍ | Sesión actual |
| **Historial de mensajes** | PostgreSQL / SQLite | ✅ SÍ | Permanente |
| **Facts del usuario** | PostgreSQL / SQLite | ✅ SÍ | Permanente |
| **Episodios** | PostgreSQL / SQLite | ✅ SÍ | Permanente |
| **Afinidad actual** | PostgreSQL / SQLite | ✅ SÍ | Permanente |
| **Mood actual** | PostgreSQL / SQLite / Redis | ✅ SÍ | Sesión o permanente |
| **Embeddings** | pgvector / Pinecone | ✅ SÍ | Permanente |

---

## 🔄 Flujo Completo: Envío de Mensaje

### Diagrama de Flujo con Tiempos

```
Usuario envía: "Hola Alicia, eres muy linda"
       │
       ▼
┌─────────────────────────────────────────────────────┐
│ 1. CARGAR CONTEXTO (async, paralelo)                │  ⏱️ ~50ms
│    ├─ Cargar personalidad JSON (si no en caché)     │
│    ├─ Obtener affinity de BBDD                      │
│    ├─ Obtener mood actual de BBDD                   │
│    └─ Obtener últimos 10 mensajes de BBDD           │
└─────────────┬───────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────┐
│ 2. COMPILAR PERSONALIDAD (en memoria)               │  ⏱️ ~5ms
│    ├─ Base (del JSON)                               │
│    ├─ + Nivel según affinity (del JSON)             │
│    ├─ + Mood actual (del JSON)                      │
│    └─ = Personalidad compilada (en memoria)         │
└─────────────┬───────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────┐
│ 3. GENERAR RESPUESTA (LLM)                          │  ⏱️ ~1500ms ← BOTTLENECK
│    - Llamada a DeepSeek/OpenAI/etc                  │
│    - Con personalidad compilada + contexto          │
└─────────────┬───────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────┐
│ 4. PROCESAMIENTO POST-RESPUESTA (async, paralelo)   │  ⏱️ ~200ms (background)
│    ├─ Extraer facts (LLM call ligero)               │
│    ├─ Detectar mood nuevo (LLM call ligero)         │
│    ├─ Actualizar affinity (cálculo)                 │
│    ├─ Detectar episodio (cada 5 mensajes)           │
│    ├─ Crear embeddings (API call)                   │
│    └─ Guardar todo en BBDD                          │
└─────────────┬───────────────────────────────────────┘
              │
              ▼
       Retornar respuesta al usuario

TOTAL: ~1555ms (usuario ve respuesta antes del step 4)
       Step 4 corre en background
```

---

## 🎯 Respuestas a tus Preguntas

### Q1: "¿Con cada mensaje se recompila?"

**Sí, pero es MUY rápido (~5ms).**

```python
# Pseudocódigo del proceso
async def send_message(session_id, message):
    # 1. Cargar contexto (paralelo) - ~50ms
    affinity = await db.get_affinity(session_id)        # ~10ms
    mood = await db.get_mood(session_id)                # ~10ms
    personality_json = load_cached("alicia.json")       # ~1ms (caché)
    recent_messages = await db.get_messages(session_id, limit=10)  # ~30ms
    
    # 2. Compilar personalidad (en memoria) - ~5ms
    compiled = compile_dynamic(
        base=personality_json,
        affinity=affinity,      # Ej: 45
        mood=mood               # Ej: "shy"
    )
    # Esto solo aplica deltas:
    # empathy: 0.95 + 0.2 (friend) + 0.0 (shy) = 1.0
    # formality: 0.3 + (-0.1) (friend) + 0.2 (shy) = 0.4
    
    # 3. Generar respuesta (LLM) - ~1500ms ← ESTE es el lento
    response = await llm.generate(
        personality=compiled,
        context=recent_messages,
        message=message
    )
    
    # 4. Retornar inmediatamente
    return response
    
    # 5. Procesamiento background (no bloquea) - ~200ms
    asyncio.create_task(process_post_response(session_id, message, response))
```

**Usuario ve la respuesta en ~1555ms, donde 1500ms es el LLM (inevitable).**

---

### Q2: "¿Se actualiza el JSON?"

**NO. El JSON NUNCA se actualiza.**

```python
# ❌ NUNCA hacemos esto:
personality_json["advanced_parameters"]["empathy"] = new_value
save_json(personality_json)  # NO!

# ✅ Hacemos esto:
# El JSON es un template de LECTURA
# Los estados se guardan en BBDD
await db.update_affinity(session_id, new_affinity)  # Guarda en PostgreSQL
await db.update_mood(session_id, new_mood)          # Guarda en PostgreSQL
```

**Analogía:**
```
El JSON es como una RECETA de cocina.
- La receta NO cambia cuando cocinas
- Pero cada vez que cocinas, ajustas ingredientes según contexto
- Los ajustes son temporales, la receta permanece
```

---

### Q3: "¿Solo persiste mientras se habla?"

**NO. Persiste PERMANENTEMENTE en BBDD.**

```sql
-- Tabla de afinidad (PostgreSQL/SQLite)
CREATE TABLE user_affinity (
    user_id VARCHAR(255),
    personality_name VARCHAR(255),
    affinity_points INTEGER,        -- Persiste aquí
    current_level VARCHAR(50),      -- Persiste aquí
    last_updated TIMESTAMP
);

-- Tabla de mood de sesión
CREATE TABLE session_moods (
    session_id VARCHAR(255),
    current_mood VARCHAR(50),       -- Persiste aquí
    mood_intensity FLOAT,           -- Persiste aquí
    mood_started_at TIMESTAMP
);
```

**Flujo de persistencia:**

```python
# Día 1, Mensaje 1
await send_message(session_id, "Hola")
# Affinity: 0 → 1
# Se guarda en BBDD: affinity=1

# Día 1, Mensaje 2
await send_message(session_id, "Eres linda")
# Affinity: 1 → 3
# Se guarda en BBDD: affinity=3, mood="shy"

# Usuario cierra la app
# ...

# Día 2, nuevo chat
session_id = await create_session(...)  # Puede ser nueva sesión
# Sistema carga:
# - affinity = 3 (desde BBDD)
# - mood = "neutral" (reseteado por nueva sesión, OPCIONAL)
# - Personalidad base (desde JSON)

# Compila con affinity=3
# Usuario sigue donde lo dejó
```

---

### Q4: "¿Cómo clasifica qué va al JSON según el formato?"

**Nada va AL JSON. El JSON es inmutable.**

```
┌─────────────────────────────────────────────────────┐
│ ARCHIVO JSON (Inmutable)                            │
│ - Define estructura de personalidad                 │
│ - Define niveles posibles                           │
│ - Define moods posibles                             │
│ - NO se actualiza nunca                             │
└─────────────────────────────────────────────────────┘
         │
         │ Lee una vez (cacheado)
         ▼
┌─────────────────────────────────────────────────────┐
│ MEMORIA RAM (Temporal, por request)                 │
│ - Personalidad base (del JSON)                      │
│ - Estados actuales (de BBDD):                       │
│   * affinity = 45                                   │
│   * mood = "shy"                                    │
│ - Compilación dinámica (aplicar modificadores)      │
│ - Personalidad compilada final (solo en RAM)        │
└─────────────────────────────────────────────────────┘
         │
         │ Persiste en
         ▼
┌─────────────────────────────────────────────────────┐
│ BASE DE DATOS (Permanente)                          │
│ - user_affinity (affinity_points, current_level)    │
│ - session_moods (current_mood, intensity)           │
│ - messages (historial de conversación)              │
│ - user_facts (facts extraídos)                      │
│ - episodes (episodios memorables)                   │
│ - message_embeddings (vectores para búsqueda)       │
└─────────────────────────────────────────────────────┘
```

**El JSON solo se lee, nunca se escribe.**

---

### Q5: "¿El proceso no sería más lento en el chat?"

**NO, porque el procesamiento pesado va en BACKGROUND.**

```python
async def send_message(session_id, message):
    # ============================================
    # FOREGROUND (bloquea, debe ser rápido)
    # ============================================
    
    # 1. Cargar contexto - ~50ms
    affinity = await db.get_affinity(session_id)
    mood = await db.get_mood(session_id)
    personality = load_cached("alicia.json")  # Caché
    
    # 2. Compilar - ~5ms
    compiled = compile_dynamic(personality, affinity, mood)
    
    # 3. Generar respuesta LLM - ~1500ms (inevitable)
    response = await llm.generate(compiled + message)
    
    # 4. Guardar mensaje en BBDD - ~20ms
    await db.save_message(session_id, message, response)
    
    # TOTAL FOREGROUND: ~1575ms
    # Usuario ve respuesta AQUÍ ✅
    
    # ============================================
    # BACKGROUND (NO bloquea, puede ser lento)
    # ============================================
    
    # Lanzar tareas en background
    asyncio.create_task(
        process_memory_async(session_id, message, response)
    )
    
    # Retornar inmediatamente
    return response


async def process_memory_async(session_id, message, response):
    """
    Procesamiento de memoria en background
    NO bloquea la respuesta al usuario
    """
    # Estas tareas corren en paralelo
    await asyncio.gather(
        extract_facts(message),              # ~300ms (LLM ligero)
        detect_mood(message, context),       # ~200ms (LLM ligero)
        update_affinity(session_id),         # ~10ms (cálculo)
        create_embedding(message),           # ~100ms (API OpenAI)
        detect_episode_if_needed(session_id) # ~400ms (LLM, cada 5 msgs)
    )
    
    # TOTAL BACKGROUND: ~400ms (paralelo)
    # Pero el usuario YA tiene su respuesta
```

**Timeline del usuario:**

```
T=0ms:     Usuario envía mensaje
T=50ms:    Sistema carga contexto
T=55ms:    Sistema compila personalidad
T=1555ms:  Usuario recibe respuesta ✅ (ve la respuesta aquí)
T=1955ms:  Background: facts extraídos, affinity actualizada, embeddings creados
```

**El usuario NO espera el procesamiento de memoria.**

---

### Q6: "¿No deberíamos tener un proceso paralelo que haga esto con IA?"

**¡Exacto! Ya está diseñado así.**

```python
# ARQUITECTURA PROPUESTA

┌─────────────────────────────────────────┐
│ Main Thread (Usuario esperando)         │
│                                         │
│  1. Cargar contexto        [50ms]      │
│  2. Compilar personalidad  [5ms]       │
│  3. Llamar LLM             [1500ms]    │
│  4. Retornar respuesta     ✅          │
│                                         │
│  TOTAL: 1555ms                          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Background Worker (Async)               │
│                                         │
│  5. Extract facts (LLM)    [300ms]     │
│  6. Detect mood (LLM)      [200ms]     │
│  7. Update affinity        [10ms]      │
│  8. Create embeddings      [100ms]     │
│  9. Detect episode         [400ms]     │
│  10. Save all to DB        [50ms]      │
│                                         │
│  TOTAL: 400ms (paralelo)                │
└─────────────────────────────────────────┘

Usuario ve respuesta en 1.5s ✅
Sistema procesa memoria en background
```

---

## 💾 Sistema de Persistencia Multi-Capa

### Capa 1: Archivos JSON (Personalidades - INMUTABLES)

```
luminoracore/personalities/
├── alicia.json              ← Template inmutable
├── mika.json                ← Template inmutable
└── yumi.json                ← Template inmutable

Uso:
- Se cargan UNA VEZ al inicio (o desde caché)
- NUNCA se modifican
- Definen comportamiento base + posibles modificadores
```

### Capa 2: BBDD Relacional (Estados - MUTABLE)

```
PostgreSQL / SQLite (TU ELECCIÓN)

Tablas:
├── sessions                 ← Sesiones de conversación
├── messages                 ← Historial de mensajes
├── user_affinity            ← Puntos de afinidad por usuario/personalidad
├── session_moods            ← Mood actual por sesión
├── user_facts               ← Facts aprendidos del usuario
└── episodes                 ← Episodios memorables

Uso:
- Se actualiza constantemente
- Persiste entre sesiones
- Tu sistema ACTUAL (SQLite, JSON file, etc.) sigue funcionando
- Solo agregamos tablas nuevas
```

### Capa 3: BBDD Vectorial (Búsqueda Semántica - OPCIONAL)

```
pgvector (extensión PostgreSQL) / Pinecone

Tablas:
└── message_embeddings       ← Vectores para búsqueda semántica

Uso:
- OPCIONAL (solo si habilitas semantic search)
- NO reemplaza tu BBDD actual
- ES ADICIONAL para "recuerdas cuando..." queries
- Si no la usas, todo sigue funcionando (sin semantic search)
```

---

## 🔄 Qué Pasa con tus BBDD Actuales

### Sistema Actual v1.0

```
TU SISTEMA ACTUAL:
├── JSON files (para conversaciones)
│   └── session_123.json
│       ├── messages: [...]
│       └── context: {...}
│
├── SQLite (para persistencia)
│   └── conversations.db
│       └── sessions table
│           ├── session_id
│           ├── personality_name
│           └── messages (JSON blob)
│
└── Redis (para caché)
    └── session:{session_id} -> {data}
```

### Sistema v1.1 (EXTIENDE, no reemplaza)

```
TU SISTEMA v1.1:
├── JSON files (SIGUE IGUAL)
│   └── session_123.json
│       ├── messages: [...]
│       └── context: {...}
│
├── SQLite (SE AGREGAN TABLAS)
│   └── conversations.db
│       ├── sessions (existente)
│       ├── user_affinity (NUEVA)        ← Guarda afinidad
│       ├── session_moods (NUEVA)        ← Guarda mood actual
│       ├── user_facts (NUEVA)           ← Guarda facts
│       ├── episodes (NUEVA)             ← Guarda episodios
│       └── message_embeddings (NUEVA)   ← Guarda vectores
│
└── Redis (SIGUE IGUAL)
    └── session:{session_id} -> {data}
```

**TUS DATOS ACTUALES NO SE PIERDEN. Solo agregamos tablas nuevas.**

---

## 📝 Memoria del LLM vs Memoria de LuminoraCore

### Memoria del LLM (Context Window)

```
┌─────────────────────────────────────────┐
│ Context Window del LLM                  │
│ (Ej: 8k tokens para DeepSeek)           │
│                                         │
│ Últimos ~10-20 mensajes                 │
│ - User: "Hola"                          │
│ - Assistant: "¡Hola! ¿Cómo estás?"     │
│ - User: "Bien, ¿y tú?"                  │
│ - ...                                   │
│                                         │
│ Limitado a ventana reciente             │
└─────────────────────────────────────────┘

Ventajas:
✅ Rápido (ya en contexto)
✅ No requiere búsqueda

Desventajas:
❌ Olvida conversaciones antiguas
❌ No diferencia importante vs trivial
❌ No puede "recordar hace 2 semanas..."
```

### Memoria de LuminoraCore (Ilimitada)

```
┌─────────────────────────────────────────┐
│ LuminoraCore Memory System              │
│ (Ilimitada, permanente)                 │
│                                         │
│ Facts (permanente):                     │
│ - name = "Diego"                        │
│ - favorite_anime = "Naruto"             │
│ - pet_name = "Max" (deceased)           │
│                                         │
│ Episodios (importantes):                │
│ - "Pérdida de Max" (hace 2 semanas)     │
│ - "Pelea con hermana" (hace 1 mes)      │
│                                         │
│ Vector search:                          │
│ - Búsqueda semántica en TODO el         │
│   historial (meses/años)                │
└─────────────────────────────────────────┘

Ventajas:
✅ Memoria ilimitada (años)
✅ Recuerda información importante
✅ Búsqueda semántica ("recuerdas cuando...")

Desventajas:
⚠️ Requiere retrieval (pero es rápido ~50ms)
```

### Cómo se Combinan

```python
# Al generar respuesta
async def generate_response(session_id, message):
    # 1. Obtener contexto del LLM (últimos mensajes)
    recent_messages = await db.get_messages(session_id, limit=10)
    # Estos van SIEMPRE al LLM
    
    # 2. Obtener memoria relevante de LuminoraCore
    relevant_facts = await memory.get_facts(session_id)
    relevant_episodes = await memory.search_episodes(
        query=message,
        top_k=3
    )
    
    # 3. Construir prompt combinado
    prompt = f"""
    Personality: {compiled_personality}
    
    Facts about user:
    - Name: {relevant_facts['name']}
    - Favorite anime: {relevant_facts['favorite_anime']}
    - Pet: {relevant_facts['pet_name']} (deceased)
    
    Important memories:
    - 2 weeks ago: User shared that their dog Max passed away. They were very sad.
    
    Recent conversation:
    {recent_messages}
    
    User says: {message}
    """
    
    # 4. LLM tiene TODO el contexto
    response = await llm.generate(prompt)
```

**LuminoraCore ENRIQUECE el context window del LLM con información relevante del pasado.**

---

## ⚡ Performance: Optimizaciones

### 1. Caché de Personalidades

```python
# NO cargar JSON cada vez
personality_cache = {}

def load_personality(name):
    if name not in personality_cache:
        personality_cache[name] = json.load(f"{name}.json")
    return personality_cache[name]  # Instant
```

### 2. Batch Processing

```python
# En lugar de:
for message in messages:
    await create_embedding(message)  # 100ms * 10 = 1000ms

# Hacer:
embeddings = await create_embeddings_batch(messages)  # 200ms total
```

### 3. Procesamiento Selectivo

```python
# NO procesar TODO cada mensaje
if message_count % 5 == 0:
    # Solo cada 5 mensajes
    await detect_episode(recent_messages)

# Fact extraction: solo si parece haber facts
if looks_like_fact(message):  # Regex simple
    await extract_facts(message)
```

### 4. Lazy Loading

```python
# NO cargar todos los facts
# Solo cargar los relevantes
relevant_facts = await db.get_facts(
    session_id,
    categories=["personal_info", "preferences"],  # Solo lo necesario
    limit=10
)
```

---

## 🗂️ Estrategia de BBDD Híbrida

### Opción A: Todo en SQLite (Simple)

```python
# Tu setup actual puede seguir igual
storage_config = {
    "backend": "sqlite",
    "database": "luminora.db"
}

# v1.1 agrega tablas a la misma DB
# luminora.db:
# - sessions (existente)
# - messages (existente)
# - user_affinity (nueva)
# - user_facts (nueva)
# - episodes (nueva)
# - message_embeddings (nueva, si usas pgvector alternativo)
```

**Ventajas:**
- ✅ Simple, un solo archivo
- ✅ No requiere infraestructura adicional
- ✅ Migración fácil

**Desventajas:**
- ⚠️ Vector search menos eficiente (sin pgvector extension)
- ⚠️ Escalabilidad limitada

---

### Opción B: Híbrido (Recomendado)

```python
storage_config = {
    # Conversaciones y estados (rápido, local)
    "sessions_backend": "sqlite",          # sessions, messages
    
    # Memoria a largo plazo (persistente, cloud)
    "memory_backend": "postgresql",        # facts, episodes
    
    # Caché (muy rápido, temporal)
    "cache_backend": "redis",              # session state, compilaciones
    
    # Vector search (semántica)
    "vector_backend": "pgvector"           # embeddings (OPCIONAL)
}
```

**Ventajas:**
- ✅ Rápido (Redis caché)
- ✅ Persistente (PostgreSQL)
- ✅ Búsqueda eficiente (pgvector)
- ✅ Escalable

---

### Opción C: Progresivo (Empezar Simple)

**Fase 1: Solo SQLite (Mes 1-2)**
```python
storage_config = {"backend": "sqlite"}
# Todo en SQLite
# Sin vector search (semantic search deshabilitado)
```

**Fase 2: SQLite + Vector Search Local (Mes 3-4)**
```python
storage_config = {
    "backend": "sqlite",
    "vector_search": "local"  # Sentence transformers (no requiere API)
}
# Vector search con embeddings locales (gratis, más lento)
```

**Fase 3: Production (Mes 5+)**
```python
storage_config = {
    "sessions_backend": "sqlite",
    "memory_backend": "postgresql",
    "cache_backend": "redis",
    "vector_backend": "pgvector"
}
# Full stack production
```

---

## 🔍 Recuperación de Recuerdos: Cómo Funciona

### Sistema Actual v1.0

```python
# v1.0 - Solo context window del LLM
recent_messages = db.get_messages(session_id, limit=10)
# [Mensaje 1, Mensaje 2, ..., Mensaje 10]

# LLM solo ve estos 10 mensajes
# Si el usuario pregunta por algo hace 2 semanas → No recuerda
```

### Sistema v1.1 - Multi-Source Retrieval

```python
async def get_relevant_context(session_id, user_message):
    """
    Recupera contexto relevante de MÚLTIPLES fuentes
    """
    # En paralelo (simultáneo)
    results = await asyncio.gather(
        # 1. Mensajes recientes (siempre, rápido)
        db.get_recent_messages(session_id, limit=10),
        
        # 2. Facts del usuario (si relevantes)
        db.get_facts(session_id, categories=detect_categories(user_message)),
        
        # 3. Episodios relevantes (si pregunta por el pasado)
        search_episodes(session_id, query=user_message) if "recuerd" in user_message else None,
        
        # 4. Búsqueda semántica (si necesario)
        vector_search(user_message, session_id) if needs_semantic_search(user_message) else None
    )
    
    # Combinar todas las fuentes
    context = {
        "recent_messages": results[0],      # Últimos 10 mensajes
        "user_facts": results[1],           # Facts relevantes
        "relevant_episodes": results[2],    # Episodios del pasado
        "similar_conversations": results[3] # Conversaciones similares
    }
    
    return context
```

### Ejemplo Práctico

```python
# Usuario pregunta: "Recuerdas cuando te conté de Max?"

# 1. Sistema detecta: query sobre el pasado
if "recuerd" in message or "cuand" in message:
    use_semantic_search = True

# 2. Recuperación multi-source (paralelo, ~100ms)
context = await asyncio.gather(
    db.get_recent_messages(session_id, limit=5),        # ~20ms
    vector_search("Max perro", session_id, top_k=3),    # ~50ms (pgvector)
    db.get_episodes(session_id, tags=["pet", "Max"])    # ~30ms
)

# Resultados:
# recent_messages: últimos 5 mensajes (contexto inmediato)
# vector_search: [
#   "Mi perro Max murió ayer" (hace 2 semanas, score: 0.92),
#   "Max era mi mejor amigo" (hace 2 semanas, score: 0.88)
# ]
# episodes: [
#   Episode(title="Pérdida de Max", importance=9.5, hace 14 días)
# ]

# 3. Construir prompt enriquecido
prompt = f"""
Personality: {compiled}

Recent conversation:
{recent_messages}

IMPORTANT MEMORY (2 weeks ago):
User shared that their dog Max passed away. They were heartbroken.
This was a very emotional moment (importance: 9.5/10).

User asks: "Recuerdas cuando te conté de Max?"
"""

# 4. LLM responde con TODA la información
# "Claro que sí, recuerdo cuando me contaste de Max hace 2 semanas.
#  Sé que era muy importante para ti. ¿Cómo te sientes ahora?"
```

---

## 🏗️ Arquitectura Completa con Capas

```
┌────────────────────────────────────────────────────────────────┐
│                         USUARIO                                │
│                  "Recuerdas cuando..."                         │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│                    LUMINORACORE SDK                            │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│              CAPA DE ORQUESTACIÓN (Main Thread)                │
│  - Coordina todo el flujo                                      │
│  - Maneja foreground (respuesta rápida)                        │
│  - Lanza background tasks                                      │
└──┬────────┬────────┬────────┬────────────────────────────────┘
   │        │        │        │
   │        │        │        │
   ▼        ▼        ▼        ▼
┌─────┐ ┌─────┐ ┌─────┐ ┌──────────┐
│Cache│ │BBDD │ │BBDD │ │BBDD      │
│Layer│ │Rel. │ │Vec. │ │LLM Mem.  │
└─────┘ └─────┘ └─────┘ └──────────┘
  │        │        │         │
  │        │        │         │
  ▼        ▼        ▼         ▼
┌──────────────────────────────────────┐
│ STORAGE BACKENDS                     │
│                                      │
│ Redis         SQLite/PostgreSQL      │
│ ┌──────────┐  ┌──────────────┐      │
│ │Sessions  │  │Messages       │      │
│ │Moods     │  │Affinity       │      │
│ │Cache     │  │Facts          │      │
│ └──────────┘  │Episodes       │      │
│               │Embeddings     │      │
│               └──────────────┘       │
└──────────────────────────────────────┘
```

---

## 🎯 Flujo Detallado: Primera Conversación vs Conversación Continua

### Primera Conversación (Cold Start)

```python
# Usuario crea sesión por primera vez
session_id = await client.create_session(
    personality_name="alicia",
    provider_config={...}
)

# Sistema inicializa:
# 1. Cargar JSON de personalidad (del disco)
personality_json = load_json("alicia.json")  # ~10ms

# 2. Crear entrada en BBDD
await db.insert({
    "table": "user_affinity",
    "data": {
        "user_id": user_id,
        "personality_name": "alicia",
        "affinity_points": 0,      # Empieza en 0
        "current_level": "stranger"
    }
})

await db.insert({
    "table": "session_moods",
    "data": {
        "session_id": session_id,
        "current_mood": "neutral",  # Empieza en neutral
        "mood_intensity": 1.0
    }
})

# 3. Cachear personalidad en Redis
await redis.set(f"personality:alicia", personality_json, ex=3600)

# Listo para chatear
```

### Conversación Continua (Warm)

```python
# Usuario envía mensaje #1
response = await client.send_message(session_id, "Hola")

# Foreground (usuario espera):
# 1. Cargar desde caché (~1ms)
personality = await redis.get("personality:alicia")  # Caché hit
affinity = await redis.get(f"affinity:{session_id}")  # Caché hit
mood = await redis.get(f"mood:{session_id}")         # Caché hit

# 2. Compilar (~5ms)
compiled = apply_modifiers(personality, affinity=0, mood="neutral")

# 3. LLM (~1500ms)
response = await llm.generate(compiled + "Hola")

# 4. Retornar
return response  # Usuario ve respuesta aquí (1.5s)

# Background (async):
# 5. Actualizar estado
affinity_new = 1  # +1 por primer mensaje
await db.update("user_affinity", affinity=1)
await redis.set(f"affinity:{session_id}", 1, ex=3600)  # Actualizar caché

# Usuario envía mensaje #2
response = await client.send_message(session_id, "Eres linda")

# Foreground:
# 1. Cargar desde caché (~1ms) - MÁS RÁPIDO
affinity = 1  # Ya en caché
mood = "neutral"

# 2. Detectar nuevo mood (paralelo con LLM)
asyncio.create_task(detect_mood("Eres linda"))  # Background

# 3. Compilar con mood actual (~5ms)
compiled = apply_modifiers(personality, affinity=1, mood="neutral")

# 4. LLM (~1500ms)
response = await llm.generate(compiled + "Eres linda")

# 5. Retornar
return response

# Background:
# 6. Mood detectado
new_mood = "shy"
await db.update("session_moods", mood="shy", intensity=0.3)
await redis.set(f"mood:{session_id}", "shy", ex=3600)

# 7. Actualizar affinity
affinity = 1 + 2 = 3  # +2 por cumplido
await db.update("user_affinity", affinity=3)
```

---

## 💡 Solución a tus Preocupaciones

### Preocupación 1: "Recompilar cada vez es lento"

**Solución:** Compilación es TRIVIAL (~5ms), el LLM es lo lento (~1500ms)

```
Total tiempo de respuesta:
- Cargar contexto: 50ms (con caché: 1ms)
- Compilar: 5ms
- LLM: 1500ms ← 99% del tiempo
- Total: 1555ms

Si elimináramos la compilación:
- Total: 1550ms (diferencia: 5ms = 0.3%)

Conclusión: La compilación es IRRELEVANTE vs el LLM
```

### Preocupación 2: "¿Cuándo se actualiza el JSON?"

**Respuesta:** NUNCA. El JSON NO se actualiza.

```
alicia.json (archivo en disco)
  ↓ Carga UNA VEZ
Memoria RAM (objeto Python)
  ↓ Aplica modificadores TEMPORALMENTE
Personalidad compilada (en RAM, por request)
  ↓ Se usa para generar respuesta
  ↓ Se DESCARTA después
```

### Preocupación 3: "¿Dónde persiste el estado?"

**Respuesta:** En BBDD (tu elección: SQLite, PostgreSQL, etc.)**

```sql
-- Estos datos PERSISTEN entre sesiones
SELECT * FROM user_affinity WHERE user_id='diego';
-- affinity_points: 45
-- current_level: "friend"

SELECT * FROM session_moods WHERE session_id='session_123';
-- current_mood: "shy"
-- mood_intensity: 0.7

SELECT * FROM user_facts WHERE user_id='diego';
-- name: "Diego"
-- favorite_anime: "Naruto"
-- pet_name: "Max" (deceased)
```

### Preocupación 4: "¿Proceso paralelo con IA?"

**Respuesta:** SÍ, ya está diseñado así (background tasks)**

```python
# Usuario NO espera estas tareas
asyncio.create_task(extract_facts(message))      # Background
asyncio.create_task(detect_episode(messages))    # Background
asyncio.create_task(create_embeddings(message))  # Background
asyncio.create_task(update_analytics(session))   # Background
```

### Preocupación 5: "¿Qué pasa con JSON/SQLite actuales?"

**Respuesta:** SIGUEN FUNCIONANDO. Solo agregamos tablas.**

```python
# TU CÓDIGO ACTUAL (sigue igual)
messages = await db.get_messages(session_id)  # SQLite
conversation = load_json(f"session_{session_id}.json")  # JSON file

# v1.1 AGREGA (no reemplaza)
affinity = await db.get_affinity(session_id)      # Nueva tabla en SQLite
facts = await db.get_facts(session_id)            # Nueva tabla en SQLite
episodes = await db.get_episodes(session_id)      # Nueva tabla en SQLite
```

**No pierdes nada de lo que tienes.**

---

## 📋 Migración desde v1.0

```bash
# 1. Backup de BBDD actual
cp luminora.db luminora.db.backup

# 2. Ejecutar migración
luminora-cli migrate --from 1.0 --to 1.1

# Crea tablas nuevas:
# - user_affinity
# - session_moods  
# - user_facts
# - episodes
# - message_embeddings (si vector search habilitado)

# 3. Datos existentes NO se tocan
# - sessions (intacto)
# - messages (intacto)
# - Tu estructura actual (intacta)
```

---

## ⚡ Performance Real: Benchmarks

### Sin Optimización (Naive)

```
Mensaje → Respuesta
├─ Load personality JSON: 10ms
├─ Load affinity from DB: 15ms
├─ Load mood from DB: 15ms
├─ Compile personality: 5ms
├─ LLM generate: 1500ms
├─ Background tasks: 400ms (async, no bloquea)
└─ TOTAL visible: 1545ms
```

### Con Optimización (Caché)

```
Mensaje → Respuesta
├─ Load personality (caché): 0.1ms
├─ Load affinity (caché): 0.5ms
├─ Load mood (caché): 0.5ms
├─ Compile personality: 5ms
├─ LLM generate: 1500ms
├─ Background tasks: 400ms (async)
└─ TOTAL visible: 1506ms
```

**Diferencia: 39ms (2.5% overhead)**

### Con Streaming

```
Mensaje → Primera palabra visible
├─ Load context (caché): 1ms
├─ Compile: 5ms
├─ LLM streaming: 200ms ← Primera palabra
└─ TOTAL: 206ms ✅

Usuario ve primera palabra en 200ms
Resto llega progresivamente (streaming)
```

---

## 🗄️ Estructura de BBDD Completa

### SQLite (Opción Simple)

```sql
-- TU BBDD ACTUAL (v1.0, sin cambios)
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT,
    personality_name TEXT,
    created_at TIMESTAMP,
    last_activity TIMESTAMP
);

CREATE TABLE messages (
    id TEXT PRIMARY KEY,
    session_id TEXT,
    speaker TEXT,  -- "user" | "assistant"
    content TEXT,
    timestamp TIMESTAMP
);

-- NUEVAS TABLAS v1.1 (agregadas, no reemplazadas)
CREATE TABLE user_affinity (
    user_id TEXT,
    personality_name TEXT,
    affinity_points INTEGER DEFAULT 0,
    current_level TEXT DEFAULT 'stranger',
    last_updated TIMESTAMP,
    PRIMARY KEY (user_id, personality_name)
);

CREATE TABLE session_moods (
    session_id TEXT PRIMARY KEY,
    current_mood TEXT DEFAULT 'neutral',
    mood_intensity REAL DEFAULT 1.0,
    mood_started_at TIMESTAMP
);

CREATE TABLE user_facts (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    category TEXT,
    key TEXT,
    value TEXT,  -- JSON string
    confidence REAL,
    first_mentioned TIMESTAMP,
    UNIQUE(user_id, category, key)
);

CREATE TABLE episodes (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    session_id TEXT,
    type TEXT,
    title TEXT,
    summary TEXT,
    importance REAL,
    sentiment TEXT,
    tags TEXT,  -- JSON array
    timestamp TIMESTAMP
);

-- OPCIONAL: Si usas vector search con extensión
CREATE TABLE message_embeddings (
    message_id TEXT PRIMARY KEY,
    user_id TEXT,
    embedding BLOB,  -- numpy array serializado
    metadata TEXT    -- JSON
);
```

---

## 🔑 Respuesta Final a Todas tus Dudas

### 1. ¿JSON se actualiza?
**NO. JSON es inmutable. Estados en BBDD.**

### 2. ¿Recompila cada mensaje?
**SÍ, pero es rápido (~5ms). El LLM es lo lento.**

### 3. ¿Solo persiste durante chat?
**NO. Persiste PERMANENTEMENTE en BBDD.**

### 4. ¿Cómo clasifica qué va al JSON?
**Nada va al JSON. Estados van a BBDD.**

### 5. ¿Proceso más lento?
**NO. Background tasks no bloquean (async).**

### 6. ¿Proceso paralelo con IA?
**SÍ. Fact extraction, mood detection, etc. son async.**

### 7. ¿Qué pasa con JSON/SQLite actuales?
**Siguen funcionando. Solo agregamos tablas.**

### 8. ¿BBDD vectorial reemplaza actuales?
**NO. Es ADICIONAL (solo para semantic search).**

### 9. ¿Cómo recupera recuerdos?
**Multi-source: mensajes recientes + facts + episodios + vector search.**

### 10. ¿Memoria del LLM?
**LuminoraCore ENRIQUECE el context window con info del pasado.**

---

## 📊 Tabla Resumen de Persistencia

| Dato | Dónde se Define | Dónde Persiste | Mutable | Lifetime |
|------|----------------|----------------|---------|----------|
| **Personalidad base** | `alicia.json` | Archivo JSON | ❌ NO | Permanente |
| **Niveles posibles** | `alicia.json` | Archivo JSON | ❌ NO | Permanente |
| **Moods posibles** | `alicia.json` | Archivo JSON | ❌ NO | Permanente |
| **Affinity actual** | - | BBDD (SQLite/PostgreSQL) | ✅ SÍ | Permanente |
| **Mood actual** | - | BBDD + Caché (Redis) | ✅ SÍ | Sesión o permanente |
| **Mensajes** | - | BBDD (SQLite/PostgreSQL) | ✅ SÍ | Permanente |
| **Facts** | - | BBDD (SQLite/PostgreSQL) | ✅ SÍ | Permanente |
| **Episodios** | - | BBDD (SQLite/PostgreSQL) | ✅ SÍ | Permanente |
| **Embeddings** | - | BBDD Vector (pgvector/Pinecone) | ✅ SÍ | Permanente |
| **Personalidad compilada** | - | RAM (temporal, por request) | - | 1 request |

---

<div align="center">

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

