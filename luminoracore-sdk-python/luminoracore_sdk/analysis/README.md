# LuminoraCore SDK - Analysis Module

Módulo de análisis de sentimientos para el SDK.

---

## 📋 Propósito

Este módulo proporciona análisis avanzado de sentimientos para conversaciones:
- ✅ Análisis básico basado en keywords (español + inglés)
- ✅ Análisis avanzado usando LLM providers
- ✅ Detección de emociones
- ✅ Análisis de tendencias de sentimiento
- ✅ Historial de análisis

---

## 📁 Archivos

### `sentiment_analyzer.py`
Implementación de análisis avanzado de sentimientos usando LLM providers.

**Clases:**
- `AdvancedSentimentAnalyzer` - Analizador principal
- `SentimentResult` - Resultado del análisis

---

## 🔧 Componentes

### 1. AdvancedSentimentAnalyzer (`sentiment_analyzer.py`)

**Propósito:** Análisis avanzado de sentimientos usando LLM providers.

**Características:**
- ✅ Análisis básico basado en keywords
- ✅ Análisis avanzado usando LLM providers
- ✅ Detección de emociones (joy, sadness, anger, fear, surprise, disgust, trust, anticipation)
- ✅ Análisis de tendencias temporales
- ✅ Soporte multilingüe (español + inglés)
- ✅ Historial de análisis persistente

**Uso:**
```python
from luminoracore_sdk.analysis import AdvancedSentimentAnalyzer
from luminoracore_sdk.session import InMemoryStorageV11
from luminoracore_sdk.providers import OpenAIProvider
from luminoracore_sdk.types.provider import ProviderConfig

# Crear storage
storage = InMemoryStorageV11()

# Crear LLM provider (opcional, para análisis avanzado)
provider_config = ProviderConfig(
    name="openai",
    api_key="your-key",
    model="gpt-3.5-turbo"
)
llm_provider = OpenAIProvider(provider_config)

# Crear analizador
analyzer = AdvancedSentimentAnalyzer(
    storage=storage,
    llm_provider=llm_provider  # Opcional
)

# Analizar sentimiento
result = await analyzer.analyze_sentiment(
    session_id="session_123",
    user_id="user_456"
)

print(f"Sentiment: {result.overall_sentiment}")
print(f"Score: {result.sentiment_score}")
print(f"Emotions: {result.emotions_detected}")
print(f"Confidence: {result.confidence}")
print(f"Trend: {result.sentiment_trend}")
```

---

### 2. SentimentResult (`sentiment_analyzer.py`)

**Propósito:** Resultado del análisis de sentimiento.

**Campos:**
- `overall_sentiment` (str) - Sentimiento general: "positive", "negative", "neutral"
- `sentiment_score` (float) - Puntuación de sentimiento (0.0 - 1.0)
- `emotions_detected` (List[str]) - Emociones detectadas
- `confidence` (float) - Confianza del análisis (0.0 - 1.0)
- `analysis_timestamp` (str) - Timestamp del análisis
- `message_count` (int) - Número de mensajes analizados
- `sentiment_trend` (str) - Tendencia del sentimiento: "improving", "declining", "stable", "no_data"
- `detailed_analysis` (Dict[str, Any]) - Análisis detallado

---

## 💡 Funcionalidades

### 1. Análisis Básico

Análisis basado en keywords y patrones regex (español + inglés):

```python
# Análisis básico (sin LLM provider)
analyzer = AdvancedSentimentAnalyzer(storage=storage)
result = await analyzer.analyze_sentiment(session_id="session_123", user_id="user_456")
```

**Características:**
- ✅ Detección de sentimientos positivos/negativos/neutrales
- ✅ Cálculo de puntuación de sentimiento
- ✅ Soporte multilingüe (español + inglés)

---

### 2. Análisis Avanzado

Análisis usando LLM providers para mayor precisión:

```python
# Análisis avanzado (con LLM provider)
analyzer = AdvancedSentimentAnalyzer(
    storage=storage,
    llm_provider=llm_provider
)
result = await analyzer.analyze_sentiment(session_id="session_123", user_id="user_456")
```

**Características:**
- ✅ Análisis contextual usando LLM
- ✅ Mayor precisión en análisis complejos
- ✅ Análisis detallado de emociones
- ✅ Requiere LLM provider configurado

---

### 3. Detección de Emociones

Detección de 8 emociones básicas (Plutchik's Wheel):

- **Joy** - Alegría, felicidad, entusiasmo
- **Sadness** - Tristeza, melancolía, pena
- **Anger** - Enojo, frustración, ira
- **Fear** - Miedo, ansiedad, preocupación
- **Surprise** - Sorpresa, asombro, impacto
- **Disgust** - Disgusto, repulsión, asco
- **Trust** - Confianza, seguridad, lealtad
- **Anticipation** - Anticipación, esperanza, optimismo

**Soporte multilingüe:**
- ✅ Keywords en español e inglés
- ✅ Detección automática de idioma

---

### 4. Análisis de Tendencias

Análisis de tendencias temporales de sentimiento:

```python
result = await analyzer.analyze_sentiment(session_id="session_123", user_id="user_456")
print(f"Trend: {result.sentiment_trend}")  # "improving", "declining", "stable", "no_data"
```

**Tendencias:**
- **improving** - Sentimiento mejorando
- **declining** - Sentimiento empeorando
- **stable** - Sentimiento estable
- **no_data** - Sin datos suficientes

---

### 5. Historial de Análisis

Obtener historial de análisis previos:

```python
history = await analyzer.get_sentiment_history(
    session_id="session_123",
    user_id="user_456",
    limit=10,
    include_details=True
)

for entry in history:
    print(f"{entry['timestamp']}: {entry['sentiment']} (score: {entry['score']})")
```

**Características:**
- ✅ Historial persistente en storage
- ✅ Límite de resultados configurables
- ✅ Opción de incluir análisis detallado
- ✅ Máximo 50 análisis guardados por usuario

---

## 🔍 Obtención de Datos de Conversación

El analizador busca conversaciones en múltiples formatos:

### 1. Formato Principal (v1.1+)
```python
# Usa get_facts(user_id=session_id, category="conversation_history")
history_facts = await storage.get_facts(
    user_id=session_id,
    category="conversation_history"
)
# Parsea turn_* keys con user_message y assistant_response
```

### 2. Formato Legacy
```python
# Intenta conversation_key = f"conversation_{session_id}"
conversation_data = await storage.get_memory(session_id, conversation_key)
```

### 3. Formato Fallback (Episodios)
```python
# Intenta obtener de episodes
episodes = await storage.get_episodes(user_id)
```

---

## 📊 Ejemplo Completo

```python
import asyncio
from luminoracore_sdk.analysis import AdvancedSentimentAnalyzer
from luminoracore_sdk.session import InMemoryStorageV11
from luminoracore_sdk.providers import OpenAIProvider
from luminoracore_sdk.types.provider import ProviderConfig

async def main():
    # 1. Crear storage
    storage = InMemoryStorageV11()
    
    # 2. Crear LLM provider (opcional)
    provider_config = ProviderConfig(
        name="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo"
    )
    llm_provider = OpenAIProvider(provider_config)
    
    # 3. Crear analizador
    analyzer = AdvancedSentimentAnalyzer(
        storage=storage,
        llm_provider=llm_provider
    )
    
    # 4. Analizar sentimiento
    result = await analyzer.analyze_sentiment(
        session_id="session_123",
        user_id="user_456"
    )
    
    # 5. Mostrar resultados
    print(f"Overall Sentiment: {result.overall_sentiment}")
    print(f"Sentiment Score: {result.sentiment_score:.2f}")
    print(f"Emotions Detected: {', '.join(result.emotions_detected)}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Message Count: {result.message_count}")
    print(f"Sentiment Trend: {result.sentiment_trend}")
    print(f"Detailed Analysis: {result.detailed_analysis}")
    
    # 6. Obtener historial
    history = await analyzer.get_sentiment_history(
        session_id="session_123",
        user_id="user_456",
        limit=5
    )
    
    print("\nSentiment History:")
    for entry in history:
        print(f"  {entry['timestamp']}: {entry['sentiment']} (score: {entry['score']:.2f})")

asyncio.run(main())
```

---

## 🎯 Casos de Uso

### 1. Análisis de Conversaciones

```python
# Analizar sentimiento de una conversación completa
result = await analyzer.analyze_sentiment(
    session_id="conversation_session",
    user_id="user_id"
)

if result.overall_sentiment == "negative":
    print("⚠️ Negative sentiment detected. Consider intervention.")
elif result.overall_sentiment == "positive":
    print("✅ Positive sentiment. Conversation going well.")
```

### 2. Monitoreo de Tendencias

```python
# Obtener historial y detectar tendencias
history = await analyzer.get_sentiment_history(
    session_id="session_123",
    user_id="user_456",
    limit=10
)

if len(history) > 1:
    recent_scores = [entry['score'] for entry in history[:5]]
    if recent_scores[0] > recent_scores[-1]:
        print("📈 Sentiment improving")
    elif recent_scores[0] < recent_scores[-1]:
        print("📉 Sentiment declining")
```

### 3. Detección de Emociones

```python
# Analizar emociones detectadas
result = await analyzer.analyze_sentiment(session_id="session_123", user_id="user_456")

if "anger" in result.emotions_detected:
    print("⚠️ Anger detected. User may be frustrated.")
if "joy" in result.emotions_detected:
    print("😊 Joy detected. User seems happy.")
```

---

## 🔧 Configuración

### Thresholds

El analizador usa thresholds configurables:

```python
analyzer = AdvancedSentimentAnalyzer(storage=storage)

# Modificar thresholds
analyzer.POSITIVE_THRESHOLD = 0.7  # Default: 0.6
analyzer.NEGATIVE_THRESHOLD = 0.3  # Default: 0.4
analyzer.CONFIDENCE_THRESHOLD = 0.8  # Default: 0.7
```

---

## 🐛 Troubleshooting

### Error: "No conversation data found"

**Causa:** No hay datos de conversación para analizar.

**Solución:**
- Verifica que la sesión tenga conversaciones guardadas
- Verifica que el formato de datos sea compatible
- Revisa los logs para más detalles

---

### Error: "LLM provider not available"

**Causa:** Se intentó usar análisis avanzado sin LLM provider.

**Solución:**
- El análisis básico funciona sin LLM provider
- Para análisis avanzado, proporciona un LLM provider:
  ```python
  analyzer = AdvancedSentimentAnalyzer(
      storage=storage,
      llm_provider=llm_provider  # Requerido para análisis avanzado
  )
  ```

---

### Resultados imprecisos

**Causa:** Análisis básico puede ser menos preciso para textos complejos.

**Solución:**
- Usa análisis avanzado con LLM provider para mayor precisión
- Ajusta los thresholds según tus necesidades
- Revisa el `detailed_analysis` para más contexto

---

## 📚 Más Información

- **Storage:** `../session/storage_v1_1.py` (StorageV11Extension)
- **Providers:** `../providers/README.md`
- **Session Management:** `../session/README.md`

---

**Última Actualización:** 2025-11-21  
**Versión SDK:** 1.2.0  
**Estado:** ✅ Módulo completo y funcionando

