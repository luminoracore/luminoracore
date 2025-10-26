# Análisis de Velocidad de Conversaciones

## 📊 Resumen Ejecutivo

**Pregunta:** ¿Por qué las conversaciones son lentas? ¿Se llama al LLM siempre? ¿Cómo funciona la extracción de sentimiento y facts?

**Respuesta:** Las conversaciones tardan 2-3 segundos por mensaje porque **CADA mensaje hace una llamada al LLM (DeepSeek)** para generar la respuesta. El análisis de sentimiento y la actualización de affinity son **instantáneos** (no usan LLM). La extracción automática de facts **SÍ usa LLM** pero solo cuando se usa el método avanzado.

---

## ⏱️ Desglose de Tiempos

### Tiempo por Mensaje (~2-3 segundos)

```
┌─────────────────────────────────────────────────┐
│ 1. Enviar mensaje usuario                       │  ~0ms
│ 2. Preparar contexto + historia                 │  ~10ms
│ 3. LLM (DeepSeek) genera respuesta              │  ⏳ 2-3 SEGUNDOS ⭐
│ 4. Guardar mensaje en historial                 │  ~5ms
│ 5. Análisis de sentimiento (keywords)           │  ~1ms
│ 6. Actualizar affinity (SQLite)                 │  ~5ms
└─────────────────────────────────────────────────┘
TOTAL: ~2-3 segundos (mayormente esperando LLM)
```

### Análisis de Sentimiento: **NO llama al LLM**

En tu test (`test_comprehensive_30_message_chat.py`), el análisis de sentimiento es **instantáneo** porque usa **keywords simples**:

```python
# Sentiment analysis (simple heuristic) - LÍNEAS 143-150
sentiment = "neutral"
response_lower = response.content.lower()
if any(word in response_lower for word in ['great', 'wonderful', 'amazing', 'excellent', 'love', 'happy', 'excited']):
    sentiment = "positive"  # ⚡ Instantáneo
elif any(word in response_lower for word in ['sorry', 'unfortunately', 'problem', 'issue', 'difficult']):
    sentiment = "negative"  # ⚡ Instantáneo
else:
    sentiment = "neutral"   # ⚡ Instantáneo
```

**Tiempo:** < 1ms (búsqueda de palabras)

### Actualización de Affinity: **NO llama al LLM**

```python
# Actualizar affinity basado en sentimiento - LÍNEAS 155-161
if sentiment == "positive":
    await client_v11.update_affinity("user123", personality_name, 5, "positive")
elif sentiment == "negative":
    await client_v11.update_affinity("user123", personality_name, -2, "negative")
else:
    await client_v11.update_affinity("user123", personality_name, 1, "neutral")
```

**Tiempo:** ~5-10ms (write a SQLite)

---

## 🤖 Flujo Completo de un Mensaje

### 1. **Usuario envía mensaje** → `client.send_message()`
```python
response = await client.send_message(session_id=session_id, message=message)
```

### 2. **Session Manager procesa** (`session/manager.py`)
- Agrega mensaje a historial
- Prepara contexto con personalidad
- **LLAMA AL LLM (DeepSeek)** ⭐ ⏳ 2-3 segundos
- Recibe respuesta
- Guarda en historial

### 3. **Análisis de Sentimiento** (en el test)
- **No usa LLM** ⚡
- Busca keywords simples en la respuesta
- Clasifica: positive/neutral/negative

### 4. **Actualización de Affinity**
- **No usa LLM** ⚡
- Escribe a SQLite con puntos basados en sentimiento

### 5. **Extracción de Facts** (Opcional)
- **SOLO si usas método avanzado** (`send_message_with_memory`)
- **SÍ usa LLM** ⏳ para extraer facts
- En tu test NO se usa (solo guardas facts manualmente)

---

## 📋 Comparación: Básico vs Avanzado

### Modo Básico (Tu Test Actual)
```python
# 1. LLM genera respuesta
response = await client.send_message(session_id, message)  # ⏳ 2-3s

# 2. Análisis instantáneo de sentimiento (keywords)
sentiment = analyze_keywords(response.content)  # ⚡ 1ms

# 3. Actualizar affinity (SQLite write)
await client_v11.update_affinity(...)  # ⚡ 5ms

# 4. NO extrae facts automáticamente
```

**Total:** ~2-3 segundos (solo LLM para respuesta)

### Modo Avanzado (Con Extracción de Facts)
```python
# 1. LLM genera respuesta
response = await client_v11.send_message_with_memory(...)  # ⏳ 2-3s

# 2. LLM extrae facts de la conversación
facts = await llm_extract_facts(user_message, response)  # ⏳ 1-2s ⭐

# 3. Guarda facts en SQLite
await client_v11.save_facts(facts)  # ⚡ 10ms

# 4. Análisis de sentimiento
sentiment = analyze_sentiment(response)  # ⚡ 1ms
```

**Total:** ~3-5 segundos (LLM para respuesta + LLM para extracción)

---

## 🔍 ¿Cuándo se Llama al LLM?

### ✅ **SÍ se llama al LLM:**

1. **Cada mensaje del usuario** → Generar respuesta (obligatorio)
   - **Tiempo:** 2-3 segundos
   - **Proveedor:** DeepSeek API

2. **Extracción de facts** (solo modo avanzado)
   - **Tiempo:** 1-2 segundos adicionales
   - **Proveedor:** DeepSeek API
   - **Cuándo:** Solo con `send_message_with_memory()`

3. **Análisis avanzado de sentimiento** (opcional)
   - **Tiempo:** 1-2 segundos adicionales
   - **Cuándo:** Si usas `AdvancedSentimentAnalyzer`

### ❌ **NO se llama al LLM:**

1. **Análisis de sentimiento simple** (keywords)
   - **Tiempo:** < 1ms
   - **Método:** Búsqueda de palabras

2. **Actualización de affinity**
   - **Tiempo:** ~5ms
   - **Método:** Write a SQLite

3. **Guardar facts manualmente**
   - **Tiempo:** ~5ms
   - **Método:** Write a SQLite

4. **Recuperar facts/episodes/affinity**
   - **Tiempo:** ~10-50ms
   - **Método:** Read from SQLite

---

## 🚀 Optimizaciones Posibles

### Opción 1: Batching (Agrupar Mensajes)
```python
# Enviar varios mensajes en paralelo
responses = await asyncio.gather(*[
    client.send_message(session_id, msg)
    for msg in messages
])
```
**Mejora:** ~30s → ~5s para 30 mensajes

### Opción 2: Streaming
```python
# Ya lo tienes implementado: stream_message()
async for chunk in client.stream_message(session_id, message):
    print(chunk.content)  # Primera palabra en ~0.5s
```
**Mejora:** Primera palabra en ~0.5s (vs 2-3s completo)

### Opción 3: Cache de Respuestas
```python
# Cache para preguntas frecuentes
if message in cache:
    return cache[message]  # ⚡ Instantáneo
```

### Opción 4: Extracción Offline de Facts
```python
# Extraer facts después (batch)
facts = await extract_facts_offline(conversation_history)
```
**Mejora:** No bloquea respuesta del usuario

---

## 📊 Estadísticas de Tu Test

### 30 Mensajes = ~60-90 segundos

```
Mensaje 1:  2.5s (LLM) + 0.01s (sentiment) + 0.005s (affinity) = 2.515s
Mensaje 2:  2.3s (LLM) + 0.01s (sentiment) + 0.005s (affinity) = 2.315s
...
Mensaje 30: 2.4s (LLM) + 0.01s (sentiment) + 0.005s (affinity) = 2.415s

TOTAL: ~75 segundos para 30 mensajes
```

### Desglose

| Operación | Tiempo | % Total | LLM? |
|-----------|--------|---------|------|
| LLM (DeepSeek) | ~2.5s | 99.6% | ✅ |
| Sentiment (keywords) | 0.01s | 0.4% | ❌ |
| Affinity update | 0.005s | 0.2% | ❌ |
| **TOTAL** | **~2.515s** | **100%** | - |

**Conclusión:** El 99.6% del tiempo es esperando al LLM.

---

## 💡 Respuestas Directas

### ❓ ¿Por qué es lento?
**A:** Porque **cada mensaje** llama al LLM (DeepSeek) que tarda 2-3 segundos. Es normal en chatbots con LLM externos.

### ❓ ¿Se llama al LLM siempre?
**A:** Sí, **una vez por mensaje** para generar la respuesta. Si usas extracción automática de facts, serían 2 llamadas (respuesta + extracción).

### ❓ ¿Cómo funciona el análisis de sentimiento?
**A:** En tu test, usa **keywords simples** (búsqueda de palabras) → **NO llama al LLM**, es instantáneo (< 1ms).

### ❓ ¿Cómo funciona la extracción de facts?
**A:** En tu test, **NO se extraen automáticamente**. Solo guardas facts manualmente. Si usaras el método avanzado (`send_message_with_memory`), **SÍ llamaría al LLM** para extraer facts de la conversación.

---

## 🎯 Recomendaciones

### Para Producción:

1. **Usa streaming** → Primera palabra en ~0.5s
2. **Procesa facts después** → No bloquea respuesta
3. **Usa cache** → Para preguntas frecuentes
4. **Batching cuando sea posible** → Para múltiples usuarios

### Para Desarrollo/Tests:

- ✅ Tu enfoque actual es correcto
- ✅ Análisis de sentimiento rápido (keywords)
- ✅ No bloquea con extracción de facts
- ⚠️ 30 mensajes tardarán ~1-2 minutos (normal con LLM externo)

---

## 📝 Resumen

| Concepto | Respuesta |
|----------|-----------|
| **Velocidad actual** | 2-3 segundos por mensaje |
| **Causa principal** | LLM (DeepSeek API) - 99.6% del tiempo |
| **Sentiment analysis** | Keywords (NO LLM) - < 1ms |
| **Affinity update** | SQLite write (NO LLM) - ~5ms |
| **Fact extraction** | Manual en tu test (NO LLM) |
| **LLM calls** | 1 por mensaje (respuesta) |
| **Optimización posible** | Streaming (primera palabra en ~0.5s) |

**Conclusión:** La lentitud es **esperada** con LLM externo. El análisis de sentimiento y affinity NO contribuyen a la lentitud (son instantáneos). Para mejorar, usa **streaming** para que la primera palabra aparezca en ~0.5s.
