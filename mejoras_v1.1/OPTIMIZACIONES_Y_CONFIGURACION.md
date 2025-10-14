# Optimizaciones y Configuración - LuminoraCore v1.1

**Cómo optimizar costes, rendimiento, y configurar TODO el sistema**

---

## ⚡ TUS PREGUNTAS RESPONDIDAS

### 1. ✅ Batch Processing de Embeddings

**SÍ, es MEJOR y DEBE ser configurable.**

```python
# ════════════════════════════════════════════════════════
# CONFIGURACIÓN (TODO en JSON o config)
# ════════════════════════════════════════════════════════

embedding_config = {
    "provider": "openai",  # openai, cohere, deepseek, local
    "model": "text-embedding-3-small",
    "batch_size": 10,  # ← CONFIGURABLE
    "batch_timeout": 30,  # segundos (o procesar antes si llega a batch_size)
    "enabled": True
}

# ════════════════════════════════════════════════════════
# IMPLEMENTACIÓN
# ════════════════════════════════════════════════════════

class EmbeddingBatcher:
    """Acumula mensajes y procesa en batch"""
    
    def __init__(self, config: dict):
        self.batch_size = config.get("batch_size", 10)
        self.batch_timeout = config.get("batch_timeout", 30)
        self.provider = config.get("provider", "openai")
        self.queue = []
        self.last_flush = datetime.now()
    
    async def add_message(self, message: str, message_id: str):
        """Agrega mensaje a la cola"""
        self.queue.append({
            "id": message_id,
            "content": message,
            "timestamp": datetime.now()
        })
        
        # Procesar si:
        # - Queue llega a batch_size
        # - O pasó el timeout
        if len(self.queue) >= self.batch_size:
            await self.flush()
        elif (datetime.now() - self.last_flush).seconds >= self.batch_timeout:
            await self.flush()
    
    async def flush(self):
        """Procesa batch de embeddings"""
        if not self.queue:
            return
        
        # Crear embeddings en BATCH (1 sola llamada API)
        texts = [item["content"] for item in self.queue]
        
        embeddings = await openai.embeddings.create(
            model="text-embedding-3-small",
            input=texts  # ← Array de textos
        )
        
        # Guardar en BBDD en batch
        await db.insert_many(
            "message_embeddings",
            [
                {
                    "message_id": item["id"],
                    "embedding": emb.embedding,
                    "created_at": datetime.now()
                }
                for item, emb in zip(self.queue, embeddings.data)
            ]
        )
        
        # Limpiar queue
        self.queue = []
        self.last_flush = datetime.now()

# ════════════════════════════════════════════════════════
# AHORRO DE COSTES
# ════════════════════════════════════════════════════════

# Sin batch (1 llamada por mensaje):
# 100 mensajes × $0.0001 × 1 llamada = $0.01
# Tiempo: 100 × 100ms = 10,000ms (10 segundos)

# Con batch de 10:
# 100 mensajes ÷ 10 batch × $0.0001 = $0.001
# Tiempo: 10 batch × 150ms = 1,500ms (1.5 segundos)

# AHORRO: 90% costes, 85% tiempo ✅
```

---

### 2. ✅ Configurabilidad del Embedding Provider

**SÍ, debe poder elegirse según lo compilado.**

```json
// En alicia.json (Template)
{
  "persona": {...},
  
  "memory_config": {
    "semantic_search": {
      "enabled": true,
      "embedding_provider": "openai",  // ← CONFIGURABLE
      "embedding_model": "text-embedding-3-small",
      "batch_processing": {
        "enabled": true,
        "batch_size": 10,  // ← CONFIGURABLE
        "batch_timeout_seconds": 30
      }
    }
  }
}
```

```python
# Al cargar personalidad, se configura automáticamente
personality = Personality.load("alicia.json")

# Embedding provider según config del JSON
embedding_provider = create_embedding_provider(
    provider=personality.memory_config["embedding_provider"],  # Del JSON!
    model=personality.memory_config["embedding_model"]
)

# Batch size según config del JSON
batch_size = personality.memory_config["batch_processing"]["batch_size"]  # Del JSON!
```

**TODO configurable en JSON Template ✅**

---

### 3. ✅ Dónde se Guardan Embeddings y Sentiment

**En BBDD, NO en JSON Template.**

```sql
-- Tabla de embeddings
CREATE TABLE message_embeddings (
    id UUID PRIMARY KEY,
    message_id VARCHAR(255),
    user_id VARCHAR(255),
    session_id VARCHAR(255),
    embedding vector(1536),  -- pgvector
    created_at TIMESTAMP
);

-- Tabla de análisis sentimental
CREATE TABLE sentiment_analysis (
    id UUID PRIMARY KEY,
    message_id VARCHAR(255),
    sentiment VARCHAR(50),  -- positive, negative, neutral
    intensity FLOAT,  -- 0-1
    emotions JSONB,  -- ["joy", "affection", ...]
    created_at TIMESTAMP
);

-- Tabla de moods (estado actual)
CREATE TABLE session_moods (
    session_id VARCHAR(255) PRIMARY KEY,
    current_mood VARCHAR(50),  -- happy, shy, sad, etc.
    mood_intensity FLOAT,
    mood_started_at TIMESTAMP
);
```

**Los datos se guardan en BBDD, NO en el JSON Template (que es inmutable).**

---

### 4. ✅ Exportación (Snapshots) - MUY IMPORTANTE

**SÍ, cuando exportas, se incluye TODA la evolución de BBDD.**

```python
# ════════════════════════════════════════════════════════
# EXPORTAR SNAPSHOT (Template + Estado de BBDD → JSON)
# ════════════════════════════════════════════════════════

snapshot = await client.export_snapshot(
    session_id="session_123",
    include_options={
        "conversation_history": True,  # Mensajes
        "facts": True,                 # Facts aprendidos (de BBDD)
        "episodes": True,              # Episodios (de BBDD)
        "affinity_progression": True,  # Historia de affinity (de BBDD)
        "mood_history": True,          # Historia de moods (de BBDD)
        "embeddings": False,           # ⚠️ MUY pesado, mejor no
        "sentiment_data": True         # Análisis sentimental (de BBDD)
    }
)

# ════════════════════════════════════════════════════════
# SNAPSHOT JSON (Exportado)
# ════════════════════════════════════════════════════════

{
  "_snapshot_info": {
    "created_at": "2025-10-14T20:00:00Z",
    "template_name": "alicia_base",
    "user_id": "diego",
    "total_messages": 150
  },
  
  // ──────────────────────────────────────────────
  // TEMPLATE BASE (del JSON original, inmutable)
  // ──────────────────────────────────────────────
  "template": {
    "$ref": "alicia_base.json",
    // O copia completa del template
    "persona": {...},
    "hierarchical_config": {...},
    "mood_config": {...}
  },
  
  // ──────────────────────────────────────────────
  // ESTADO EVOLUCIONADO (de BBDD) ✅
  // ──────────────────────────────────────────────
  "state": {
    "affinity": {
      "current": 47,  // ← De BBDD (evolucionó)
      "level": "friend",
      "progression_history": [  // ← De BBDD
        {"date": "2025-09-14", "points": 0},
        {"date": "2025-10-01", "points": 25},
        {"date": "2025-10-14", "points": 47}
      ]
    },
    
    "mood": {
      "current": "shy",  // ← De BBDD (último mood)
      "intensity": 0.9,
      "history": [  // ← De BBDD
        {"mood": "neutral", "duration": "15m"},
        {"mood": "happy", "duration": "5m"},
        {"mood": "shy", "duration": "current"}
      ]
    },
    
    "learned_facts": [  // ← De BBDD
      {
        "category": "personal_info",
        "key": "name",
        "value": "Diego",
        "confidence": 0.99,
        "first_mentioned": "2025-09-14"
      },
      {
        "category": "preferences",
        "key": "favorite_anime",
        "value": "Naruto",
        "confidence": 0.90
      }
      // ... todos los facts de BBDD
    ],
    
    "episodes": [  // ← De BBDD
      {
        "type": "emotional_moment",
        "title": "Pérdida de Max",
        "summary": "...",
        "importance": 9.5,
        "sentiment": "very_sad",  // ← Del análisis sentimental
        "date": "2025-10-01"
      }
      // ... todos los episodios de BBDD
    ],
    
    "sentiment_summary": {  // ← De BBDD (agregado)
      "overall": "positive",
      "distribution": {
        "positive": 68,
        "neutral": 25,
        "negative": 7
      }
    }
    
    // Embeddings NO se exportan (muy pesados)
    // Pero se pueden regenerar si importas en otro sistema
  },
  
  // ──────────────────────────────────────────────
  // CONVERSACIÓN (opcional, de BBDD)
  // ──────────────────────────────────────────────
  "conversation_history": [  // ← De BBDD
    {
      "speaker": "user",
      "content": "Hola, soy Diego",
      "timestamp": "2025-09-14T10:00:00Z"
    },
    {
      "speaker": "assistant",
      "content": "Hola Diego!",
      "timestamp": "2025-09-14T10:00:05Z"
    }
    // ... todos los mensajes de BBDD
  ]
}
```

**Este JSON Snapshot es PORTABLE:**
- ✅ Puedes importarlo en otra app
- ✅ Puedes compartirlo
- ✅ Puedes migrarlo a otro LLM
- ✅ Contiene TODA la evolución

---

### 5. ✅ Persistencia del Estado Evolucionado

**SÍ, todo persiste en BBDD. Snapshot es solo EXPORTACIÓN.**

```
┌─────────────────────────────────────────┐
│ BBDD (PostgreSQL/SQLite)                │
│ ════════════════════════════════════════│
│                                         │
│ - user_affinity (affinity evolucionada) │
│ - session_moods (moods históricos)      │
│ - user_facts (facts aprendidos)         │
│ - episodes (episodios creados)          │
│ - message_embeddings (vectores)         │
│ - sentiment_analysis (sentimientos)     │
│                                         │
│ TODO PERSISTE AQUÍ ✅                   │
│ No se pierde nunca                      │
└─────────────────────────────────────────┘
         │
         │ Usuario quiere backup o migración
         ▼
┌─────────────────────────────────────────┐
│ SNAPSHOT JSON (Exportado)               │
│ ════════════════════════════════════════│
│                                         │
│ - Template base (ref)                   │
│ - Estado completo (de BBDD)             │
│ - Facts (de BBDD)                       │
│ - Episodios (de BBDD)                   │
│ - Moods (de BBDD)                       │
│ - Affinity (de BBDD)                    │
│                                         │
│ Portable, compartible ✅                │
└─────────────────────────────────────────┘
```

**Flujo:**
1. Template JSON (inmutable) → Define comportamientos posibles
2. BBDD (mutable) → Estado evoluciona con cada conversación
3. Snapshot JSON (exportado) → Template + Estado en un solo JSON portable

---

### 6. ✅ Usar Tu Propio Modelo (DeepSeek Self-Hosted)

**SÍ, puedes usar tu endpoint propio (MUY recomendado).**

```json
// Config en JSON Template
{
  "persona": {...},
  
  "processing_config": {
    // ════════════════════════════════════════
    // LLM PRINCIPAL (Conversación)
    // ════════════════════════════════════════
    "main_llm": {
      "provider": "deepseek",
      "model": "deepseek-chat",
      "endpoint": "https://api.deepseek.com/v1",  // Cloud
      "api_key_env": "DEEPSEEK_API_KEY"
    },
    
    // ════════════════════════════════════════
    // LLM PARA PROCESAMIENTO (Background)
    // ════════════════════════════════════════
    "processing_llm": {
      "provider": "deepseek-local",  // ← TU PROPIO ENDPOINT
      "model": "deepseek-r1-distill-llama-8b",
      "endpoint": "http://localhost:8000/v1",  // ← TU SERVIDOR
      "api_key_env": null,  // No necesitas API key
      
      "tasks": [
        "mood_detection",      // Usar para detectar moods
        "fact_extraction",     // Usar para extraer facts
        "sentiment_analysis",  // Usar para sentimiento
        "episode_detection"    // Usar para detectar episodios
      ]
    },
    
    // ════════════════════════════════════════
    // EMBEDDING PROVIDER
    // ════════════════════════════════════════
    "embedding_provider": {
      "provider": "openai",  // openai, cohere, local, deepseek
      "model": "text-embedding-3-small",
      "endpoint": "https://api.openai.com/v1",  // O tu propio endpoint
      "batch_processing": {
        "enabled": true,
        "batch_size": 10,  // ← CONFIGURABLE
        "batch_timeout": 30,
        "max_queue_size": 100
      }
    }
  }
}
```

**Ventajas de tu propio endpoint:**
- ✅ **Gratis** (sin API costs)
- ✅ **Rápido** (latencia local)
- ✅ **Privacidad** (datos no salen)
- ✅ **Control total**

---

## 💰 Comparación de Costes

### Opción A: Todo Cloud APIs (❌ Caro)

```python
# Por cada mensaje:
# - LLM principal (DeepSeek cloud): $0.014 / mensaje
# - Mood detection (DeepSeek cloud): $0.002 / mensaje
# - Fact extraction (DeepSeek cloud): $0.003 / mensaje
# - Sentiment (DeepSeek cloud): $0.001 / mensaje
# - Embeddings (OpenAI): $0.0001 / mensaje

# TOTAL: $0.0201 / mensaje

# 1000 mensajes/día:
# $0.0201 × 1000 = $20.10 / día
# $20.10 × 30 = $603 / mes ❌ CARO
```

---

### Opción B: Cloud Principal + Local Processing (✅ Mejor)

```python
# Por cada mensaje:
# - LLM principal (DeepSeek cloud): $0.014 / mensaje
# - Mood detection (TU SERVER): $0 / mensaje ✅
# - Fact extraction (TU SERVER): $0 / mensaje ✅
# - Sentiment (TU SERVER): $0 / mensaje ✅
# - Embeddings (OpenAI batch): $0.00001 / mensaje ✅

# TOTAL: $0.01401 / mensaje

# 1000 mensajes/día:
# $0.01401 × 1000 = $14.01 / día
# $14.01 × 30 = $420 / mes

# AHORRO: $603 - $420 = $183/mes (30% ahorro) ✅
```

---

### Opción C: Todo Local (✅✅ Más Barato, pero requiere GPU)

```python
# Por cada mensaje:
# - LLM principal (TU SERVER DeepSeek): $0 / mensaje ✅
# - Mood detection (TU SERVER): $0 / mensaje ✅
# - Fact extraction (TU SERVER): $0 / mensaje ✅
# - Sentiment (TU SERVER): $0 / mensaje ✅
# - Embeddings (Local sentence-transformers): $0 / mensaje ✅

# TOTAL: $0 / mensaje ✅✅✅

# 1000 mensajes/día: $0 / día

# AHORRO: $603/mes (100% ahorro) ✅✅✅

# PERO:
# - Requiere GPU (NVIDIA RTX 4090 o similar)
# - Costo servidor: ~$200-300/mes (GPU cloud)
# - O hardware propio: ~$2000 one-time

# Net savings: $603 - $250 = $353/mes
```

---

## ⚡ Performance: Optimizaciones Avanzadas

### 1. Batch Processing Inteligente

```python
class SmartBatcher:
    """Batcher inteligente con priorización"""
    
    def __init__(self, config):
        self.high_priority_queue = []  # Procesar rápido
        self.normal_queue = []         # Procesar en batch
        self.batch_size = config["batch_size"]
    
    async def add_message(self, message, priority="normal"):
        """Agrega mensaje con prioridad"""
        
        if priority == "high":
            # Procesar inmediatamente (no esperar batch)
            await self.process_immediate([message])
        else:
            # Agregar a queue normal
            self.normal_queue.append(message)
            
            # Procesar si llegamos a batch size
            if len(self.normal_queue) >= self.batch_size:
                await self.process_batch(self.normal_queue)
                self.normal_queue = []
    
    async def process_batch(self, messages):
        """Procesa batch de mensajes"""
        # 1 llamada para N mensajes
        embeddings = await create_embeddings_batch(
            [m.content for m in messages]
        )
        # Ahorro: 80-90%
```

**Configuración:**

```json
{
  "batch_processing": {
    "enabled": true,
    "strategies": {
      "normal": {
        "batch_size": 10,
        "timeout": 30
      },
      "high_priority": {
        "batch_size": 1,  // Inmediato
        "timeout": 0
      }
    }
  }
}
```

---

### 2. Procesamiento Selectivo

```python
# NO procesar TODO cada mensaje

async def process_background(message):
    """Procesamiento selectivo"""
    
    # ─────────────────────────────────────────
    # 1. Mood: Solo si hay trigger aparente
    # ─────────────────────────────────────────
    if has_mood_trigger(message):
        # "Eres linda" → tiene trigger (cumplido)
        mood = await detect_mood(message)  # 200ms
    else:
        # "Hola" → no tiene trigger
        mood = None  # No procesamos (ahorro: 200ms)
    
    # ─────────────────────────────────────────
    # 2. Facts: Solo si parece haber facts
    # ─────────────────────────────────────────
    if looks_like_fact(message):
        # "Soy Diego, 28 años" → parece fact
        facts = await extract_facts(message)  # 300ms
    else:
        # "Eres linda" → no parece fact
        facts = []  # No procesamos (ahorro: 300ms)
    
    # ─────────────────────────────────────────
    # 3. Episodio: Solo cada N mensajes
    # ─────────────────────────────────────────
    message_count = await db.count_messages(session_id)
    
    if message_count % 5 == 0:
        # Cada 5 mensajes, verificar
        episode = await detect_episode(...)  # 400ms
    else:
        episode = None  # No verificamos (ahorro: 400ms)
    
    # ─────────────────────────────────────────
    # 4. Embeddings: SIEMPRE (pero en batch)
    # ─────────────────────────────────────────
    await batcher.add_message(message)  # Agrega a queue
    # Procesará cuando llegue a batch_size


# ═══════════════════════════════════════════════════
# AHORRO REAL
# ═══════════════════════════════════════════════════

# Mensaje promedio (sin facts, sin triggers especiales):
# - Mood: 0ms (no detectado)
# - Facts: 0ms (no extraídos)
# - Episode: 0ms (no cada mensaje)
# - Embeddings: 0ms (en queue, batch después)
# TOTAL: ~0ms background ✅

# Solo cuando REALMENTE hay algo que procesar
```

**Configuración:**

```json
{
  "selective_processing": {
    "mood_detection": {
      "strategy": "trigger_based",  // "always", "trigger_based", "manual"
      "triggers_regex": ["linda", "guapo", "hermosa", "amor", ...]
    },
    "fact_extraction": {
      "strategy": "heuristic",  // "always", "heuristic", "manual"
      "min_message_length": 10  // No procesar mensajes muy cortos
    },
    "episode_detection": {
      "strategy": "periodic",  // "always", "periodic", "importance_based"
      "check_every_n_messages": 5  // ← CONFIGURABLE
    }
  }
}
```

---

## 🚀 Tu Propio Endpoint DeepSeek

### Setup Recomendado

```bash
# ════════════════════════════════════════════════════════
# OPCIÓN 1: DeepSeek Local (Tu Servidor)
# ════════════════════════════════════════════════════════

# 1. Instalar vLLM (servidor de inferencia)
pip install vllm

# 2. Descargar modelo DeepSeek
huggingface-cli download deepseek-ai/DeepSeek-R1-Distill-Llama-8B

# 3. Levantar servidor
vllm serve deepseek-ai/DeepSeek-R1-Distill-Llama-8B \
    --host 0.0.0.0 \
    --port 8000 \
    --gpu-memory-utilization 0.9

# 4. Usar en LuminoraCore
```

```python
# Config
processing_llm = {
    "provider": "openai-compatible",  # vLLM es compatible con API de OpenAI
    "endpoint": "http://localhost:8000/v1",
    "model": "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
    "api_key": "dummy"  # No se usa
}

# Usar
async def detect_mood_local(message):
    """Detectar mood con tu servidor local"""
    response = await httpx.post(
        "http://localhost:8000/v1/chat/completions",
        json={
            "model": "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
            "messages": [{
                "role": "user",
                "content": f"Detecta mood de: {message}"
            }]
        }
    )
    # Tiempo: ~100ms (local, muy rápido)
    # Costo: $0 ✅
    return response.json()
```

**Performance:**
- Latencia: 100-200ms (vs 500ms cloud)
- Costo: $0 (vs $0.002 cloud)
- Throughput: Ilimitado (tu hardware)

---

### Hardware Recomendado

```
GPU Recomendada: NVIDIA RTX 4090 (24GB VRAM)
- Puede correr DeepSeek-8B (~8-10 req/s)
- Costo: ~$1600 one-time

Alternativa Cloud:
- RunPod GPU (RTX 4090): $0.69/hora
- 24/7: $0.69 × 24 × 30 = $497/mes
- Still más barato que APIs ($603/mes)

Alternativa Barata:
- RTX 3090 (24GB): $800 one-time
- Puede correr DeepSeek-8B (~6 req/s)
```

---

## 📊 Configuración Completa Recomendada

```json
// alicia_optimized.json
{
  "persona": {...},
  "core_traits": {...},
  "advanced_parameters": {...},
  
  // ════════════════════════════════════════════════════
  // CONFIGURACIÓN DE PROCESAMIENTO (TODO CONFIGURABLE)
  // ════════════════════════════════════════════════════
  
  "processing_config": {
    
    // ────────────────────────────────────────
    // LLM Principal (Conversación)
    // ────────────────────────────────────────
    "main_llm": {
      "provider": "deepseek",
      "model": "deepseek-chat",
      "endpoint": "https://api.deepseek.com/v1",
      "max_tokens": 2000,
      "temperature": 0.8
    },
    
    // ────────────────────────────────────────
    // LLM Background (Procesamiento)
    // ────────────────────────────────────────
    "processing_llm": {
      "provider": "deepseek-local",  // ← TU SERVIDOR
      "model": "deepseek-r1-distill-llama-8b",
      "endpoint": "http://localhost:8000/v1",
      "tasks": {
        "mood_detection": {
          "enabled": true,
          "max_tokens": 50,
          "temperature": 0.3
        },
        "fact_extraction": {
          "enabled": true,
          "max_tokens": 200,
          "temperature": 0.1
        },
        "sentiment_analysis": {
          "enabled": true,
          "max_tokens": 100,
          "temperature": 0.2
        },
        "episode_detection": {
          "enabled": true,
          "max_tokens": 300,
          "temperature": 0.3,
          "check_every_n_messages": 5  // ← CONFIGURABLE
        }
      }
    },
    
    // ────────────────────────────────────────
    // Embeddings
    // ────────────────────────────────────────
    "embedding_provider": {
      "provider": "openai",  // O "local" para sentence-transformers
      "model": "text-embedding-3-small",
      "batch_processing": {
        "enabled": true,
        "batch_size": 10,  // ← CONFIGURABLE
        "batch_timeout_seconds": 30,
        "strategy": "smart"  // "immediate", "batch", "smart"
      }
    },
    
    // ────────────────────────────────────────
    // Optimizaciones
    // ────────────────────────────────────────
    "optimizations": {
      "selective_processing": {
        "enabled": true,
        "mood_detection": "trigger_based",  // Solo si hay trigger
        "fact_extraction": "heuristic",     // Solo si parece fact
        "episode_detection": "periodic"     // Solo cada N mensajes
      },
      
      "caching": {
        "enabled": true,
        "personality_ttl": 3600,  // Cache personality 1 hora
        "context_ttl": 300,       // Cache context 5 min
        "embeddings_ttl": 86400   // Cache embeddings 24 horas
      },
      
      "rate_limiting": {
        "enabled": true,
        "max_llm_calls_per_minute": 60,
        "max_embedding_calls_per_minute": 100
      }
    }
  }
}
```

---

## 🔄 Flujo Optimizado Completo

```python
# ════════════════════════════════════════════════════════
# CONFIGURACIÓN INICIAL (Al cargar personalidad)
# ════════════════════════════════════════════════════════

personality = Personality.load("alicia_optimized.json")

# Crear providers según config del JSON
main_llm = create_llm_provider(
    personality.processing_config["main_llm"]
)

processing_llm = create_llm_provider(
    personality.processing_config["processing_llm"]
    # ↑ TU SERVIDOR LOCAL
)

embedding_provider = create_embedding_provider(
    personality.processing_config["embedding_provider"]
)

# Crear batcher
batcher = EmbeddingBatcher(
    batch_size=personality.processing_config["embedding_provider"]["batch_size"]
    # ↑ Del JSON, CONFIGURABLE
)

# ════════════════════════════════════════════════════════
# POR CADA MENSAJE
# ════════════════════════════════════════════════════════

async def send_message(session_id, message):
    # ──────────────────────────────────────────
    # FOREGROUND (usuario espera)
    # ──────────────────────────────────────────
    
    # Cargar contexto (con caché)
    context = await load_context_cached(session_id)
    
    # Compilar
    compiled = compile_dynamic(context)
    
    # Generar respuesta (LLM principal - cloud o local según config)
    response = await main_llm.generate(compiled + message)
    
    # Retornar
    return response  # Usuario ve ✅
    
    # ──────────────────────────────────────────
    # BACKGROUND (usuario NO espera)
    # ──────────────────────────────────────────
    
    asyncio.create_task(
        process_background_optimized(session_id, message, response)
    )


async def process_background_optimized(session_id, message, response):
    """Background optimizado"""
    
    # ─────────────────────────────────────────
    # Procesamiento SELECTIVO
    # ─────────────────────────────────────────
    
    tasks = []
    
    # Mood: Solo si tiene trigger
    if has_mood_trigger(message.content):
        tasks.append(
            processing_llm.detect_mood(message)  # ← TU SERVIDOR
        )
    
    # Facts: Solo si parece tener facts
    if looks_like_fact(message.content):
        tasks.append(
            processing_llm.extract_facts(message)  # ← TU SERVIDOR
        )
    
    # Sentiment: Solo si es importante
    if is_important_message(message):
        tasks.append(
            processing_llm.analyze_sentiment(message)  # ← TU SERVIDOR
        )
    
    # Embeddings: SIEMPRE pero en batch
    await batcher.add_message(message)  # Queue, procesa después
    
    # Episodio: Solo cada 5 mensajes
    msg_count = await db.get_message_count(session_id)
    if msg_count % 5 == 0:
        tasks.append(
            processing_llm.detect_episode(session_id)  # ← TU SERVIDOR
        )
    
    # ─────────────────────────────────────────
    # Ejecutar tareas en paralelo
    # ─────────────────────────────────────────
    
    if tasks:
        results = await asyncio.gather(*tasks)
        await save_results_to_db(results)
    
    # TIEMPO PROMEDIO: ~100ms (porque es selectivo)
    # Sin procesamiento innecesario ✅
```

---

## 📊 Performance Comparado

### Sin Optimizaciones (Naive)

```
Mensaje → Respuesta
├─ LLM generate: 1500ms
└─ Background:
   ├─ Mood (SIEMPRE): 200ms
   ├─ Facts (SIEMPRE): 300ms
   ├─ Sentiment (SIEMPRE): 150ms
   ├─ Embeddings (INDIVIDUAL): 100ms
   └─ Episode (SIEMPRE): 400ms
   
TOTAL background: 1150ms
Costo: $0.0201/mensaje
```

---

### Con Optimizaciones (Smart)

```
Mensaje → Respuesta
├─ LLM generate: 1500ms
└─ Background:
   ├─ Mood (SI trigger): 100ms (local) o 0ms
   ├─ Facts (SI parece fact): 150ms (local) o 0ms
   ├─ Sentiment (SI importante): 100ms (local) o 0ms
   ├─ Embeddings (BATCH): 15ms promedio
   └─ Episode (CADA 5 msg): 80ms promedio (local) o 0ms
   
TOTAL background promedio: ~150ms
Costo: $0.014/mensaje (solo LLM principal)

AHORRO: 87% tiempo, 30% costos ✅
```

---

## 🎯 Respuestas Finales a tus Preguntas

### 1. "¿Mejor batch embeddings?"

**SÍ, 100%:**
- Ahorro: 80-90% tiempo y costos
- Configurable: batch_size, timeout
- Smart: puede ser inmediato si es urgente

---

### 2. "¿Debe ser configurable?"

**SÍ, TODO configurable en JSON:**
- Batch size
- Timeout
- Provider (OpenAI, Cohere, local)
- Modelo
- Strategy (immediate, batch, smart)

---

### 3. "¿Embeddings van a BBDD?"

**SÍ:**
```sql
CREATE TABLE message_embeddings (
    message_id VARCHAR,
    embedding vector(1536),
    created_at TIMESTAMP
);
```

**NO van al JSON Template (inmutable)**
**SÍ van al Snapshot (cuando exportas)**

---

### 4. "¿JSON exportado incluye evolución de BBDD?"

**SÍ, Snapshot = Template + Todo de BBDD:**
- ✅ Facts aprendidos (de BBDD)
- ✅ Episodios (de BBDD)
- ✅ Affinity progression (de BBDD)
- ✅ Mood history (de BBDD)
- ✅ Sentiment data (de BBDD)
- ⚠️ Embeddings NO (muy pesados, se regeneran)

---

### 5. "¿Debe ser persistente?"

**SÍ, TODO persiste en BBDD:**

```
Conversación Día 1:
- Affinity: 0 → 5 (guardado en BBDD)
- Facts: 3 facts (guardados en BBDD)

Usuario cierra app
════════════════════════════

Conversación Día 2:
- Sistema carga de BBDD: affinity=5, facts=3
- Usuario continúa donde lo dejó ✅

Usuario exporta snapshot
════════════════════════════

Snapshot incluye:
- Template base (alicia.json)
- Affinity: 5 (de BBDD)
- Facts: 3 (de BBDD)
- Todo portable ✅
```

---

### 6. "¿Propio modelo DeepSeek para procesamiento?"

**SÍ, MUY RECOMENDADO:**

**Ventajas:**
- ✅ Gratis (sin API costs de processing)
- ✅ Rápido (latencia local ~100ms)
- ✅ Privacidad total
- ✅ Control completo
- ✅ Ahorro: ~$183/mes

**Desventajas:**
- ⚠️ Requiere GPU (RTX 3090/4090)
- ⚠️ Setup inicial (~1 día)
- ⚠️ Mantenimiento

**Configuración:**

```json
{
  "processing_llm": {
    "provider": "deepseek-local",
    "endpoint": "http://localhost:8000/v1",  // ← TU SERVIDOR
    "model": "deepseek-r1-distill-llama-8b",
    "timeout": 5000,
    "max_retries": 3
  }
}
```

---

### 7. "¿Preocupación por velocidad?"

**Con las optimizaciones, NO hay problema:**

```
Usuario envía mensaje
    ↓
1555ms: Ve respuesta ✅ (igual que v1.0)
    ↓
[Background, usuario NO espera]
    ↓
~150ms: Procesamiento optimizado
    - Selectivo (no procesa innecesario)
    - Local (tu servidor, rápido)
    - Batch (embeddings eficientes)
    ↓
TOTAL: 1555ms visible + 150ms invisible
    
Overhead real: 0ms (usuario no lo nota)
```

**Velocidad para usuario: IDÉNTICA a v1.0** ✅

---

## 🎯 RECOMENDACIÓN FINAL

### Setup Óptimo para Ti

```json
{
  "processing_config": {
    // LLM principal: DeepSeek Cloud (conversaciones)
    "main_llm": {
      "provider": "deepseek",
      "endpoint": "https://api.deepseek.com/v1",
      "model": "deepseek-chat"
    },
    
    // LLM procesamiento: TU SERVIDOR LOCAL ✅
    "processing_llm": {
      "provider": "deepseek-local",
      "endpoint": "http://localhost:8000/v1",
      "model": "deepseek-r1-distill-llama-8b"
    },
    
    // Embeddings: Batch con OpenAI ✅
    "embedding_provider": {
      "provider": "openai",
      "model": "text-embedding-3-small",
      "batch_processing": {
        "enabled": true,
        "batch_size": 10,
        "batch_timeout": 30
      }
    },
    
    // Optimizaciones ✅
    "optimizations": {
      "selective_processing": true,
      "caching": true,
      "batch_processing": true
    }
  }
}
```

**Costos:**
- Main LLM (cloud): $14/día
- Processing LLM (local): $0/día ✅
- Embeddings (batch): $0.10/día ✅
- **Total: ~$420/mes** (vs $603 sin optimizar)

**Performance:**
- Usuario: 1555ms (idéntico a v1.0)
- Background: 150ms promedio
- Total: Sin impacto visible ✅

---

## ✅ Resumen de tus Preguntas

| Pregunta | Respuesta |
|----------|-----------|
| ¿Batch embeddings? | ✅ SÍ, ahorra 80% |
| ¿Configurable? | ✅ SÍ, batch_size en JSON |
| ¿Embedding según compilado? | ✅ SÍ, provider en JSON |
| ¿Embeddings a BBDD? | ✅ SÍ, tabla message_embeddings |
| ¿Sentiment a BBDD? | ✅ SÍ, tabla sentiment_analysis |
| ¿Snapshot incluye BBDD? | ✅ SÍ, Template + Estado de BBDD |
| ¿Es persistente? | ✅ SÍ, BBDD persiste siempre |
| ¿Propio modelo DeepSeek? | ✅ SÍ, muy recomendado |
| ¿Velocidad? | ✅ Sin impacto (background) |

---

<div align="center">

**TODO es configurable. TODO es optimizable. Velocidad NO es problema.**

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

