# LuminoraCore SDK - Evolution Module

Módulo de evolución de personalidades basado en interacciones del usuario.

---

## 📋 Componentes

### PersonalityEvolutionEngine (`personality_evolution.py`)

**Propósito:** Sistema de evolución de personalidades que analiza interacciones del usuario y adapta los rasgos de personalidad en consecuencia.

**Características:**
- ✅ Análisis de patrones de interacción
- ✅ Detección de triggers de evolución
- ✅ Cálculo de cambios en rasgos de personalidad
- ✅ Aplicación de cambios de forma gradual
- ✅ Historial de evolución
- ✅ Sistema de confianza para cambios

**Uso:**
```python
from luminoracore_sdk.evolution import PersonalityEvolutionEngine
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11

storage = InMemoryStorageV11()
evolution_engine = PersonalityEvolutionEngine(storage)

result = await evolution_engine.evolve_personality(
    session_id="session_123",
    user_id="user_456",
    personality_name="dr_luna"
)

if result.changes_detected:
    print(f"Evolution detected: {len(result.changes)} changes")
    for change in result.changes:
        print(f"  {change.trait_name}: {change.old_value} → {change.new_value}")
```

---

## 🔧 Funcionalidades

### 1. Evolución de Personalidad

**Método:** `evolve_personality()`

Analiza las interacciones del usuario y evoluciona la personalidad basándose en:
- Cambios en afinidad
- Patrones de comunicación
- Tendencias de sentimiento
- Preferencias de respuesta

**Parámetros:**
- `session_id: str` - ID de sesión
- `user_id: str` - ID de usuario
- `personality_name: str` - Nombre de la personalidad
- `**params` - Parámetros adicionales

**Retorna:**
- `EvolutionResult` - Resultado con cambios detectados y aplicados

---

### 2. Historial de Evolución

**Método:** `get_evolution_history()`

Obtiene el historial de evolución de una personalidad.

**Parámetros:**
- `session_id: str` - ID de sesión
- `user_id: str` - ID de usuario
- `limit: int` - Número máximo de entradas (default: 10)
- `include_details: bool` - Incluir detalles (default: True)

**Retorna:**
- `List[Dict[str, Any]]` - Lista de entradas de evolución

**Ejemplo:**
```python
history = await evolution_engine.get_evolution_history(
    session_id="session_123",
    user_id="user_456",
    limit=20,
    include_details=True
)

for entry in history:
    print(f"Evolution at {entry['timestamp']}")
    print(f"  Confidence: {entry['confidence_score']}")
    print(f"  Changes: {len(entry['changes'])}")
```

---

## 📊 Rasgos de Personalidad

El sistema evoluciona los siguientes rasgos:

| Rasgo | Peso | Descripción |
|-------|------|-------------|
| `formality` | 0.8 | Nivel de formalidad en comunicación |
| `humor` | 0.6 | Uso de humor |
| `empathy` | 0.9 | Nivel de empatía |
| `directness` | 0.7 | Directo vs indirecto |
| `verbosity` | 0.5 | Longitud de respuestas |
| `warmth` | 0.8 | Calidez en comunicación |
| `patience` | 0.7 | Paciencia con el usuario |
| `curiosity` | 0.6 | Nivel de curiosidad |

---

## 🎯 Triggers de Evolución

El sistema detecta evolución cuando:

1. **Cambio de Afinidad:** Afinidad cambia más de `AFFINITY_CHANGE_THRESHOLD` (10 puntos)
2. **Interacciones Mínimas:** Al menos `MIN_INTERACTIONS_FOR_EVOLUTION` (5 interacciones)
3. **Patrones Consistentes:** Patrones de comunicación consistentes detectados
4. **Sentimiento:** Tendencias de sentimiento claras

---

## 📈 Flujo de Evolución

```
1. Obtener personalidad actual
   ↓
2. Analizar interacciones
   ↓
3. Detectar triggers de evolución
   ↓
4. Calcular cambios en rasgos
   ↓
5. Aplicar cambios gradualmente
   ↓
6. Guardar personalidad evolucionada
   ↓
7. Guardar en historial
   ↓
8. Retornar EvolutionResult
```

---

## 🔍 Análisis de Interacciones

El sistema analiza:

- **Total de interacciones:** Número total de mensajes
- **Interacciones positivas/negativas:** Basado en sentimiento
- **Cambio de afinidad:** Diferencia en puntos de afinidad
- **Patrones de comunicación:** Estilo preferido del usuario
- **Tendencias de sentimiento:** Sentimiento general
- **Preferencias de respuesta:** Tipo de respuestas preferidas

---

## 💾 Almacenamiento

El módulo usa `StorageV11Extension` para persistir:

- **Personalidades evolucionadas:** Guardadas como facts
- **Historial de evolución:** Guardado en `evolution_history`
- **Metadata:** Timestamps, confidence scores, razones

**Estructura de datos:**
```python
{
    "personality_{user_id}_{personality_name}": {
        "name": "dr_luna",
        "advanced_parameters": {
            "formality": 0.6,
            "empathy": 0.8,
            ...
        },
        "last_evolution": {
            "timestamp": "2025-11-21T10:00:00",
            "changes_count": 3,
            "confidence_score": 0.85
        }
    }
}
```

---

## 🎨 Ejemplo Completo

```python
import asyncio
from luminoracore_sdk.evolution import PersonalityEvolutionEngine
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
from luminoracore_sdk import LuminoraCoreClient

async def main():
    # Setup
    base_client = LuminoraCoreClient()
    await base_client.initialize()
    
    storage_v11 = InMemoryStorageV11()
    client_v11 = LuminoraCoreClientV11(base_client, storage_v11=storage_v11)
    
    # Crear evolution engine
    evolution_engine = PersonalityEvolutionEngine(storage_v11)
    
    user_id = "user_123"
    personality_name = "dr_luna"
    session_id = "session_456"
    
    # Simular interacciones (en producción, esto viene de conversaciones reales)
    await client_v11.update_affinity(
        user_id, personality_name, points_delta=15, interaction_type="very_positive"
    )
    
    # Evolucionar personalidad
    result = await evolution_engine.evolve_personality(
        session_id=session_id,
        user_id=user_id,
        personality_name=personality_name
    )
    
    if result.changes_detected:
        print(f"✅ Evolution detected!")
        print(f"   Confidence: {result.confidence_score:.2f}")
        print(f"   Changes: {len(result.changes)}")
        
        for change in result.changes:
            print(f"   - {change.trait_name}: {change.old_value:.2f} → {change.new_value:.2f}")
            print(f"     Reason: {change.change_reason}")
    else:
        print("ℹ️  No evolution detected")
    
    # Obtener historial
    history = await evolution_engine.get_evolution_history(
        session_id=session_id,
        user_id=user_id,
        limit=10
    )
    
    print(f"\n📜 Evolution History ({len(history)} entries):")
    for entry in history:
        print(f"   {entry['timestamp']}: {entry['confidence_score']:.2f} confidence")
    
    await base_client.cleanup()

asyncio.run(main())
```

---

## ⚙️ Configuración

### Thresholds

```python
MIN_INTERACTIONS_FOR_EVOLUTION = 5  # Mínimo de interacciones
AFFINITY_CHANGE_THRESHOLD = 10       # Cambio mínimo de afinidad
CONFIDENCE_THRESHOLD = 0.7           # Confianza mínima para cambios
```

### Pesos de Rasgos

Los rasgos tienen diferentes pesos que afectan cómo se calculan los cambios:
- Mayor peso = Cambios más significativos
- Menor peso = Cambios más sutiles

---

## 🐛 Troubleshooting

### Error: "No evolution triggers detected"

**Causa:** No hay suficientes interacciones o cambios significativos.

**Solución:** Asegúrate de tener:
- Al menos 5 interacciones
- Cambio de afinidad > 10 puntos
- Patrones consistentes

### Error: "StorageV11Extension not found"

**Solución:** Asegúrate de usar storage v1.1:
```python
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
```

### Error: "No personality data found"

**Solución:** Asegúrate de tener una personalidad inicial:
```python
# El sistema usa personalidad por defecto si no encuentra una
# O puedes guardar una personalidad inicial usando storage
```

---

## 📚 Más Información

- **Storage v1.1:** `../session/storage_v1_1.py`
- **Client v1.1:** `../client_v1_1.py`
- **Memory System:** `../session/memory.py`

---

## 🔄 Compatibilidad

- **v1.1:** ✅ Totalmente compatible
- **v1.2.0:** ✅ Compatible (usa StorageV11Extension)
- **Core:** ⚠️ No requiere Core (feature específica del SDK)

---

**Última Actualización:** 2025-11-21  
**Versión SDK:** 1.2.0  
**Estado:** ✅ Módulo completo y funcionando

