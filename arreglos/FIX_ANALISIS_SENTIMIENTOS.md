# ✅ Fix: Análisis de Sentimientos - Encuentra Conversaciones

## 🐛 Problema Identificado

El análisis de sentimientos no encontraba las conversaciones guardadas porque:

1. **Creaba un nuevo `session_id`** en lugar de usar el original
2. **Buscaba en formato incorrecto**: `get_memory(session_id, "conversation_{session_id}")`
3. **Las conversaciones se guardan en formato diferente**: `get_facts(user_id=session_id, category="conversation_history")`

### Flujo Roto (ANTES):
```
Handler recibe: session_id = "test_session_123"
↓
client_v11.analyze_sentiment(user_id="test", message="") 
↓
Crea NUEVO session_id = "test_analysis_20250127_123456" ❌
↓
Busca con: get_memory("test_analysis_...", "conversation_test_analysis_...") ❌
↓
No encuentra nada → Retorna valores por defecto
```

## ✅ Solución Implementada

### 1. Modificado `client_v1_1.analyze_sentiment()` (Línea 719)

**Cambios:**
- ✅ Acepta `session_id` opcional como parámetro
- ✅ Acepta `message` opcional
- ✅ **MODO 1**: Si `session_id` presente y `message` vacío → Analiza toda la sesión
- ✅ **MODO 2**: Si `message` presente → Analiza solo ese mensaje

**Firma nueva:**
```python
async def analyze_sentiment(
    self,
    user_id: str,
    message: Optional[str] = None,  # ← Opcional
    context: Optional[List[str]] = None,
    session_id: Optional[str] = None  # ← NUEVO: session_id opcional
) -> Dict[str, Any]:
```

**Lógica:**
```python
# MODO 1: Analizar sesión completa
if session_id and not message:
    # Usa el session_id ORIGINAL
    result = await self.sentiment_analyzer.analyze_sentiment(session_id, user_id)
    
# MODO 2: Analizar mensaje específico
elif message:
    # Analiza solo el mensaje (no necesita buscar conversaciones)
    ...
```

### 2. Modificado `sentiment_analyzer._get_conversation_data()` (Línea 185)

**Cambios:**
- ✅ **PRIMERO**: Busca con `get_facts(user_id=session_id, category="conversation_history")` (formato correcto)
- ✅ Parsea los `turn_*` keys correctamente
- ✅ Extrae `user_message` y `assistant_response` de cada turno
- ✅ Fallbacks para compatibilidad con formatos antiguos

**Búsqueda correcta:**
```python
# ✅ BÚSQUEDA PRINCIPAL
history_facts = await self.storage.get_facts(
    user_id=session_id,  # ← Usa session_id como user_id (coincide con cómo se guardan)
    category="conversation_history"  # ← Categoría correcta
)

# Parsea cada turno
for fact in history_facts:
    if fact.get("key", "").startswith("turn_"):
        turn_data = json.loads(fact["value"])  # Parse JSON
        # Agrega user_message y assistant_response al análisis
```

## 🔄 Flujo Corregido (AHORA):

```
Handler recibe: session_id = "test_session_123"
↓
client_v11.analyze_sentiment(
    user_id="test", 
    message="",  # Vacío
    session_id="test_session_123"  # ✅ Pasa session_id original
)
↓
MODO 1 activado: Analizar sesión completa
↓
sentiment_analyzer.analyze_sentiment("test_session_123", "test")
↓
_get_conversation_data busca:
  get_facts(user_id="test_session_123", category="conversation_history") ✅
↓
Encuentra conversaciones: 10 turnos
↓
Analiza todos los mensajes
↓
Retorna análisis completo con:
  - sentiment: "positive"
  - message_count: 20 (10 turnos × 2 mensajes)
  - confidence: 0.85
  - emotions_detected: ["joy", "excitement"]
```

## 📝 Cambios en el Handler de la API

El handler debe pasar `session_id` al método:

### ANTES (Roto):
```python
async def handle_analyze_sentiment(event: Dict[str, Any], session_id: str):
    user_id = session_id.split('_')[0] if '_' in session_id else "default_user"
    message = analysis_params.get('message', '')
    
    # ❌ No pasaba session_id
    sentiment_result = await client_v11.analyze_sentiment(
        user_id=user_id,
        message=message,
        context=context
    )
```

### AHORA (Corregido):
```python
async def handle_analyze_sentiment(event: Dict[str, Any], session_id: str):
    user_id = session_id.split('_')[0] if '_' in session_id else session_id  # Mejor: usar session_id completo
    message = analysis_params.get('message', '')
    context = analysis_params.get('context', [])
    
    # ✅ Pasa session_id para que pueda analizar la sesión completa
    sentiment_result = await client_v11.analyze_sentiment(
        user_id=user_id,
        message=message if message else None,  # None si está vacío
        context=context if message else None,
        session_id=session_id  # ← AÑADIR: session_id original
    )
```

## 🎯 Casos de Uso

### Caso 1: Analizar toda la sesión
```http
POST /api/v1/sentiment/analyze/test_session_123
Authorization: Bearer TOKEN
Content-Type: application/json

{}  # Body vacío o sin "message"
```

**Resultado:**
```json
{
  "sentiment": "positive",
  "sentiment_score": 0.75,
  "confidence": 0.88,
  "message_count": 20,
  "emotions_detected": ["joy", "excitement"],
  "sentiment_trend": "improving",
  "detailed_analysis": {...}
}
```

### Caso 2: Analizar mensaje específico
```http
POST /api/v1/sentiment/analyze/test_session_123
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "message": "Estoy muy feliz hoy",
  "context": ["Mensaje anterior 1", "Mensaje anterior 2"]
}
```

**Resultado:**
```json
{
  "sentiment": "positive",
  "sentiment_score": 0.92,
  "confidence": 0.95,
  "message_count": 3,
  "emotions_detected": ["joy"],
  "sentiment_trend": "stable",
  "detailed_analysis": {...}
}
```

## ✅ Verificación

Para verificar que funciona:

1. **Crear conversaciones:**
   ```python
   # Varios mensajes en la misma sesión
   POST /api/v1/chat
   {"session_id": "test_sentiment", "message": "Estoy feliz"}
   POST /api/v1/chat
   {"session_id": "test_sentiment", "message": "Todo va bien"}
   POST /api/v1/chat
   {"session_id": "test_sentiment", "message": "Me siento genial"}
   ```

2. **Analizar sesión completa:**
   ```python
   POST /api/v1/sentiment/analyze/test_sentiment
   {}  # Body vacío
   ```

3. **Verificar respuesta:**
   ```json
   {
     "message_count": 6,  // 3 turnos × 2 mensajes
     "sentiment": "positive",
     "confidence": > 0.7  // Debe ser > 0.5
   }
   ```

## 📊 Archivos Modificados

1. **`luminoracore-sdk-python/luminoracore_sdk/client_v1_1.py`**
   - Línea 719-819: Método `analyze_sentiment()` completamente reescrito
   - ✅ Soporta dos modos: sesión completa o mensaje específico
   - ✅ Usa `session_id` original en lugar de crear uno nuevo

2. **`luminoracore-sdk-python/luminoracore_sdk/analysis/sentiment_analyzer.py`**
   - Línea 185-285: Método `_get_conversation_data()` corregido
   - ✅ Busca primero en `get_facts(user_id=session_id, category="conversation_history")`
   - ✅ Parsea correctamente los turnos de conversación
   - ✅ Mantiene fallbacks para compatibilidad

## 🚀 Próximos Pasos

1. ✅ **SDK corregido** - Listo para desplegar
2. ⏳ **Handler de API** - Necesita actualización para pasar `session_id`
3. ⏳ **Testing** - Ejecutar tests de sentimientos después del deployment

## 📋 Resumen

**Problema:** El análisis creaba un `session_id` nuevo y buscaba en formato incorrecto.

**Solución:** 
- Pasar `session_id` original al método
- Buscar conversaciones con `get_facts(user_id=session_id, category="conversation_history")`
- Parsear correctamente los turnos guardados

**Estado:** ✅ Código corregido, pendiente deployment y actualización del handler

