# LuminoraCore Memory System - Guía Profunda

## 📋 Índice

1. [Visión General](#visión-general)
2. [¿Qué se Envía en Cada Conversación?](#qué-se-envía-en-cada-conversación)
3. [Sistema de Memoria (Facts)](#sistema-de-memoria-facts)
4. [Análisis de Sentimiento](#análisis-de-sentimiento)
5. [Evolución de Personalidad](#evolución-de-personalidad)
6. [Affinity y Relación Usuario-Personalidad](#affinity-y-relación-usuario-personalidad)
7. [Modos de Uso](#modos-de-uso)
8. [Mejores Prácticas](#mejores-prácticas)
9. [Ejemplos de Código](#ejemplos-de-código)

---

## 📊 Visión General

LuminoraCore tiene **dos modos principales** de operación:

### ✅ Modo Básico (`send_message`)
- **Velocidad:** Rápido (~2-3 segundos/mensaje)
- **LLM Calls:** 1 por mensaje (solo respuesta)
- **Extracción Facts:** Manual (hardcoded)
- **Sentiment:** Keywords simples
- **Uso:** Tests, desarrollo, demos rápidos

### 🚀 Modo Avanzado (`send_message_with_memory`)
- **Velocidad:** Lento (~4-6 segundos/mensaje)
- **LLM Calls:** 2-3 por mensaje (respuesta + extracción + sentiment)
- **Extracción Facts:** Automática con LLM
- **Sentiment:** Análisis LLM real
- **Uso:** Producción, aplicaciones reales

---

## 🔄 ¿Qué se Envía en Cada Conversación?

Cuando usas `send_message_with_memory()`, el sistema envía al LLM:

### 1. **Historial de Conversación** (20 últimos mensajes)
```python
conversation_history = [
    {"role": "user", "content": "Mi nombre es Alice"},
    {"role": "assistant", "content": "Hola Alice, encantada de conocerte..."},
    # ... hasta 20 mensajes recientes
]
```
**Límite:** Configurable (`max_history_turns = 20`)

### 2. **Facts del Usuario** (Memoria Persistente)
```python
user_facts = [
    {"category": "personal", "key": "name", "value": "Alice", "confidence": 0.95},
    {"category": "personal", "key": "age", "value": "28", "confidence": 0.9},
    {"category": "preferences", "key": "favorite_food", "value": "sushi", "confidence": 0.85}
]
```
**Persistencia:** Guardados en SQLite/DynamoDB/Redis
**Alcance:** Trans-sesión (persiste entre conversaciones)

### 3. **Affinity/Relationship Level**
```python
affinity = {
    "current_level": "friend",  # stranger → acquaintance → friend → close_friend
    "affinity_points": 45,
    "total_interactions": 12,
    "positive_interactions": 8
}
```
**Actualización:** Automática después de cada mensaje

### 4. **Estado de Personalidad Actual**
```python
personality_state = {
    "name": "alex_digital",
    "traits": {...},
    "current_mood": "enthusiastic",
    "evolution_history": [...]
}
```

### 5. **Contexto del Mensaje Actual**
```python
current_message = "Hi! My name is Alice and I'm 28 years old."
```

**TODO esto se envía juntos al LLM** para generar respuestas contextualmente relevantes.

---

## 🧠 Sistema de Memoria (Facts)

### ¿Qué Son los Facts?

Los **facts** son datos estructurados sobre el usuario que el sistema **recuerda** entre conversaciones.

### Estructura de un Fact

```python
{
    "category": "personal",      # personal | preferences | relationships | hobbies | work
    "key": "name",               # name, age, location, favorite_color, etc.
    "value": "Alice",            # El valor actual
    "confidence": 0.95,          # 0.0 - 1.0
    "timestamp": "2025-01-15T10:30:00Z",
    "source": "user_explicit"   # user_explicit | inferred | extracted
}
```

### Extracción Automática de Facts

En **modo avanzado** (`send_message_with_memory`):

1. **Usuario envía mensaje:** "Hi! My name is Alice and I'm 28 years old."

2. **LLM extrae facts automáticamente:**
   ```json
   {
     "facts": [
       {"category": "personal", "key": "name", "value": "Alice", "confidence": 0.99},
       {"category": "personal", "key": "age", "value": "28", "confidence": 0.98}
     ]
   }
   ```

3. **Se guardan en base de datos** (SQLite/DynamoDB/etc.)

4. **Estos facts se incluyen en futuras conversaciones**

### Almacenamiento

- **Base de datos:** SQLite (local) / DynamoDB (AWS) / Redis / MongoDB
- **Persistencia:** Permanente entre sesiones
- **Recuperación:** Automática en cada conversación

---

## 😊 Análisis de Sentimiento

### Modalidades Disponibles

#### 1. **Sentiment por Mensaje** (Individual)
```python
# Se analiza cada mensaje del usuario
sentiment = analyze_sentiment(user_message)
# Resultado: "positive", "negative", "neutral", "excited", "frustrated"
```

#### 2. **Sentiment por Sesión** (Agregado)
```python
# Se analiza toda la conversación en una sesión
session_sentiment = analyze_session_sentiment(session_id)
# Resultado: Overall sentiment + emociones detectadas
```

#### 3. **Sentiment por Grupo de Mensajes**
```python
# Se analizan los últimos N mensajes
group_sentiment = analyze_message_group(messages, n=5)
# Resultado: Sentiment trend y patrones
```

### Implementación

#### Modo Básico (Keywords)
```python
# Análisis instantáneo basado en keywords
sentiment = "neutral"
if any(word in message.lower() for word in ['great', 'wonderful', 'amazing']):
    sentiment = "positive"
```
**Tiempo:** < 1ms
**Precisión:** Baja (~60-70%)

#### Modo Avanzado (LLM)
```python
# Análisis con LLM para precisión
sentiment = await llm_analyze_sentiment(message, context)
```
**Tiempo:** ~1-2 segundos
**Precisión:** Alta (~85-95%)

### Actualización de Affinity

El sentimiento afecta directamente la **affinity**:

```python
if sentiment == "positive":
    affinity_points += 5
elif sentiment == "negative":
    affinity_points -= 2
else:
    affinity_points += 1
```

---

## 🎭 Evolución de Personalidad

### ¿Cómo Funciona?

La personalidad **evoluciona** basándose en las interacciones con el usuario.

### Qué Cambia

1. **Mood/Estado de Ánimo**
   - `enthusiastic` → `calm` → `excited`
   - Se adapta al tono de la conversación

2. **Tono de Respuesta**
   - Más formal o casual
   - Más o menos entusiasta

3. **Preferencias de Conversación**
   - Temas que el usuario prefiere
   - Nivel de profundidad técnica

### Tracking de Evolución

```python
# Estado inicial (antes de conversaciones)
initial_personality = {
    "name": "alex_digital",
    "mood": "neutral",
    "enthusiasm_level": 0.5,
    "formality_level": 0.5
}

# Estado después de 10 conversaciones
evolved_personality = {
    "name": "alex_digital",
    "mood": "enthusiastic",
    "enthusiasm_level": 0.75,  # Aumentó por interacciones positivas
    "formality_level": 0.3     # Decreció (más casual)
}
```

### Exportación JSON

El sistema puede exportar:
- Estado inicial de personalidad (JSON)
- Estado final evolucionado (JSON)
- Comparación antes/después

---

## 💝 Affinity y Relación Usuario-Personalidad

### Niveles de Affinity

```
stranger (0 puntos) 
  ↓ 
acquaintance (10 puntos)
  ↓
friend (25 puntos)
  ↓
close_friend (50 puntos)
  ↓
best_friend (100 puntos)
```

### Factores que Afectan Affinity

| Factor | Punto Impacto | Duración |
|--------|---------------|----------|
| Mensaje positivo | +5 | Instantáneo |
| Mensaje neutral | +1 | Instantáneo |
| Mensaje negativo | -2 | Instantáneo |
| Conversación larga | +10 | Por sesión |
| Compartir hechos personales | +3 | Por fact |
| Interacción frecuente | +2 | Diario |

### Uso en Conversaciones

La affinity afecta el **tono** de las respuestas:

```python
if affinity_level == "stranger":
    tone = "formal, polite, introduction"
elif affinity_level == "friend":
    tone = "casual, familiar, jokes allowed"
elif affinity_level == "close_friend":
    tone = "very casual, inside jokes, personal"
```

---

## 🛠️ Modos de Uso

### Modo 1: Básico (Desarrollo/Tests)

```python
# 1. Initialize
client = LuminoraCoreClient()
await client.initialize()

# 2. Create session
session_id = await client.create_session(
    personality_name="alex_digital",
    provider_config=deepseek_config
)

# 3. Send messages (NO extracción automática)
response = await client.send_message(session_id, "Hello!")
```

**Características:**
- ✅ Rápido (2-3s/mensaje)
- ❌ No extrae facts automáticamente
- ❌ Sentiment simple (keywords)
- ⚠️  Facts deben guardarse manualmente

**Uso:** Tests, demos, desarrollo rápido

### Modo 2: Avanzado (Producción)

```python
# 1. Initialize with v1.1 extensions
client = LuminoraCoreClient()
await client.initialize()

storage_v11 = FlexibleSQLiteStorageV11(database_path="memory.db")
client_v11 = LuminoraCoreClientV11(client, storage_v11=storage_v11)

# 2. Use send_message_with_memory (extracción automática)
result = await client_v11.send_message_with_memory(
    session_id=session_id,
    user_message="Hi! My name is Alice",
    user_id="alice_user",
    personality_name="alex_digital",
    provider_config=deepseek_config
)

# Facts extraídos automáticamente y guardados
facts = await client_v11.get_facts("alice_user")
```

**Características:**
- ❌ Lento (4-6s/mensaje)
- ✅ Extrae facts automáticamente
- ✅ Sentiment real (LLM)
- ✅ Affinity automático

**Uso:** Producción, aplicaciones reales

---

## ✅ Mejores Prácticas

### 1. **Para Tests/Desarrollo**

```python
# ✅ Use modo básico para velocidad
response = await client.send_message(session_id, message)

# ✅ Guarde facts manualmente para tests
await client_v11.save_fact("user123", "personal", "name", "Test User")
```

### 2. **Para Producción**

```python
# ✅ SIEMPRE use modo avanzado
result = await client_v11.send_message_with_memory(...)

# ✅ NO hardcodee facts
# El sistema los extrae automáticamente
```

### 3. **Gestión de Sentiment**

```python
# Para análisis rápido
if quick_analysis_needed:
    sentiment = analyze_keywords(message)  # ⚡ Instantáneo

# Para precisión
if precision_needed:
    sentiment = await llm_analyze_sentiment(message)  # ⏳ Lento pero preciso
```

### 4. **Optimización de Velocidad**

```python
# Use streaming para respuesta instantánea
async for chunk in client.stream_message(session_id, message):
    print(chunk.content)  # Primera palabra en ~0.5s

# Procese facts después (no bloquea respuesta)
facts = await extract_facts_offline(conversation_history)
```

### 5. **Persistencia**

```python
# SQLite para desarrollo
storage = FlexibleSQLiteStorageV11(database_path="dev.db")

# DynamoDB para producción (AWS)
storage = FlexibleDynamoDBStorageV11(table_name="production")

# PostgreSQL para escalado
storage = FlexiblePostgreSQLStorageV11(connection_string="...")
```

---

## 💻 Ejemplos de Código

### Ejemplo 1: Uso Básico

```python
import asyncio
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.provider import ProviderConfig

async def basic_chat():
    # Initialize
    client = LuminoraCoreClient()
    await client.initialize()
    
    # Create session
    provider_config = ProviderConfig(
        name="deepseek",
        api_key="your-key",
        model="deepseek-chat"
    )
    
    session_id = await client.create_session(
        personality_name="alex_digital",
        provider_config=provider_config
    )
    
    # Chat
    response = await client.send_message(session_id, "Hello!")
    print(response.content)
    
    await client.cleanup()

asyncio.run(basic_chat())
```

### Ejemplo 2: Uso Avanzado con Extracción

```python
import asyncio
from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
from luminoracore_sdk.session.storage_sqlite_flexible import FlexibleSQLiteStorageV11
from luminoracore_sdk.types.provider import ProviderConfig

async def advanced_chat():
    # Initialize base client
    client = LuminoraCoreClient()
    await client.initialize()
    
    # Initialize v1.1 extensions
    storage = FlexibleSQLiteStorageV11(database_path="memory.db")
    client_v11 = LuminoraCoreClientV11(client, storage_v11=storage)
    
    # Provider config
    provider_config = ProviderConfig(
        name="deepseek",
        api_key="your-key",
        model="deepseek-chat"
    )
    
    # Use send_message_with_memory (extracción automática)
    result = await client_v11.send_message_with_memory(
        session_id=None,  # Creará automáticamente
        user_message="Hi! My name is Alice, I'm 28 years old",
        user_id="alice_user",
        personality_name="alex_digital",
        provider_config=provider_config
    )
    
    # Facts extraídos automáticamente
    facts = await client_v11.get_facts("alice_user")
    print(f"Extracted {len(facts)} facts:")
    for fact in facts:
        print(f"  - {fact['key']}: {fact['value']}")
    
    await client.cleanup()

asyncio.run(advanced_chat())
```

### Ejemplo 3: Tracking de Evolución

```python
import asyncio
import json
from luminoracore_sdk import LuminoraCoreClient

async def track_evolution():
    client = LuminoraCoreClient()
    await client.initialize()
    
    personality_name = "alex_digital"
    
    # Get initial state
    initial = await client.get_personality(personality_name)
    with open("initial.json", "w") as f:
        json.dump(initial, f, indent=2)
    
    # ... have conversations ...
    
    # Get final state
    final = await client.get_personality(personality_name)
    with open("final.json", "w") as f:
        json.dump(final, f, indent=2)
    
    # Compare evolution
    print("Evolution tracked!")
    
    await client.cleanup()

asyncio.run(track_evolution())
```

---

## 📊 Resumen de Capacidades

### ✅ Lo que LuminoraCore Hace

| Característica | Básico | Avanzado |
|---------------|--------|----------|
| Extracción automática de facts | ❌ Manual | ✅ LLM |
| Sentiment analysis | ⚠️  Keywords | ✅ LLM |
| Affinity tracking | ❌ Manual | ✅ Automático |
| Evolución personalidad | ✅ Básica | ✅ Avanzada |
| Persistencia de memoria | ✅ SQLite | ✅ Múltiples |
| Historial conversación | ✅ 20 mensajes | ✅ 20 mensajes |
| Velocidad | ⚡ 2-3s | 🐌 4-6s |

### 📦 Qué se Envía al LLM

1. ✅ Últimos 20 mensajes de la conversación
2. ✅ Todos los facts del usuario (memoria persistente)
3. ✅ Affinity actual (nivel de relación)
4. ✅ Estado de personalidad
5. ✅ Contexto del mensaje actual

### 🎯 Recomendaciones Finales

1. **Development/Tests:** Use modo básico (rápido)
2. **Production:** Use modo avanzado (extracción automática)
3. **Sentiment:** Use LLM para precisión, keywords para velocidad
4. **Storage:** SQLite para dev, DynamoDB para production
5. **Evolution:** Exporte JSON antes/después para tracking

---

## 🚀 Siguiente Paso

Ejecuta el test `test_with_real_memory_extraction.py` para ver:
- ✅ Extracción automática de facts (sin hardcode)
- ✅ Sentiment analysis real
- ✅ Evolución de personalidad
- ✅ JSON export de estado inicial y final

**Comando:**
```bash
$env:DEEPSEEK_API_KEY="tu-clave"; python test_with_real_memory_extraction.py
```
