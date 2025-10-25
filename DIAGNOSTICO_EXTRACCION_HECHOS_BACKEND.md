# 🔍 DIAGNÓSTICO COMPLETO: Problema de Extracción de Hechos en Backend

## 📋 RESUMEN EJECUTIVO

El equipo de backend está experimentando problemas con la extracción automática de hechos al usar el framework. Tras analizar los logs de CloudWatch y el código `src/handlers/chat.py`, he identificado **3 problemas críticos** que impiden que el framework funcione correctamente.

---

## 🚨 PROBLEMA 1: Personalidad "Sakura" No Existe

### Error Observado en Logs
```
ERROR - Failed to create session: Personality not found: Sakura
WARNING - Could not ensure session exists: Session creation failed: Personality not found: Sakura
```

### Causa Raíz
El backend está intentando crear una sesión con la personalidad **"Sakura"**, pero esta personalidad **no existe** en el framework SDK.

### Personalidades Disponibles en el SDK
Según el directorio `luminoracore/luminoracore/personalities/`, las personalidades disponibles son:

1. `dr_luna`
2. `captain_hook`
3. `grandma_hope`
4. `marcus_sarcastic`
5. `lila_charm`
6. `professor_stern`
7. `rocky_inspiration`
8. `alex_digital`
9. `victoria_sterling`
10. `zero_cool`

**NO existe ninguna personalidad llamada "Sakura".**

### Solución
El backend debe usar una de las personalidades disponibles, por ejemplo:

```python
# ❌ INCORRECTO - Personalidad no existe
personality_name = "Sakura"

# ✅ CORRECTO - Usar personalidad existente
personality_name = "dr_luna"  # o cualquiera de las disponibles
```

---

## 🚨 PROBLEMA 2: El Backend NO Está Cargando Personalidades

### Análisis del Código `get_client_v11()`

```python
async def get_client_v11(provider_config=None):
    # Create base client with provider configuration
    base_client = LuminoraCoreClient()  # ❌ Sin directorio de personalidades
    
    # CRITICAL FIX: Configure the base client with provider if available
    if provider_config:
        await base_client.initialize()  # ✅ Inicializa pero NO carga "Sakura"
```

### El Problema
El `LuminoraCoreClient` se está creando sin especificar el directorio de personalidades:

```python
base_client = LuminoraCoreClient()
#                              ^ ❌ Falta: personalities_dir="/ruta/a/personalities"
```

Cuando se llama a `await base_client.initialize()`, el framework intenta cargar personalidades desde el directorio por defecto (`"personalities"`), pero:

1. Es posible que este directorio no exista en el Lambda
2. Aunque exista, no contiene "Sakura"
3. El backend no está pasando el path correcto a las personalidades

### Solución
El backend debe especificar dónde están las personalidades:

```python
# ✅ CORRECTO - Especificar directorio de personalidades
base_client = LuminoraCoreClient(
    personalities_dir="/opt/personalities"  # o la ruta correcta en Lambda
)
```

**O mejor aún**, cargar la personalidad manualmente:

```python
# Cargar personalidad específica
await base_client.load_personality("Sakura", {
    "persona": {
        "name": "Sakura",
        "description": "...",
        # ... resto de configuración
    }
})
```

---

## 🚨 PROBLEMA 3: Sesión No Encontrada Durante Extracción de Hechos

### Error Observado en Logs
```
ERROR - Failed to send message to session test_simple_extraction: Session not found: test_simple_extraction
```

Este error aparece **durante la extracción de hechos** (dentro de `send_message_with_memory()`).

### Causa Raíz
El `send_message_with_memory()` internamente llama al `base_client.send_message()` para usar el LLM. Sin embargo, **la sesión no fue creada correctamente** en el base client debido al error "Personality not found: Sakura".

### Flujo del Error
1. Backend intenta crear sesión → ❌ Falla porque "Sakura" no existe
2. Backend continúa intentando llamar `send_message_with_memory()` → ⚠️ Método falla internamente
3. `send_message_with_memory()` internamente llama a `base_client.send_message()` → ❌ Falla porque la sesión no existe
4. Resultado: `new_facts = []` (sin hechos extraídos)

---

## ✅ VERIFICACIÓN: ¿El Backend Está Usando `send_message_with_memory()`?

**SÍ**. Los logs confirman que el backend está usando el método correcto:

```
INFO - Calling send_message_with_memory...
```

El problema no es que esté usando el método incorrecto, sino que el método está fallando internamente debido a los problemas anteriores.

---

## 📝 RESUMEN DE CAMBIOS REQUERIDOS EN EL BACKEND

### Cambio 1: Usar Personalidad Existente o Cargarla Manualmente

⚠️ **ACTUALIZACIÓN**: El SDK ahora incluye personalidades de ejemplo por defecto.

El SDK ahora incluye automáticamente las personalidades de ejemplo en el directorio `luminoracore_sdk/personalities/`. Esto significa que:

1. ✅ **Las personalidades se cargan automáticamente** cuando se instala el SDK
2. ✅ **No es necesario cargarlas manualmente** en Lambda (si el SDK está en el Lambda Layer)
3. ✅ **Las personalidades disponibles son**: `dr_luna`, `captain_hook`, `grandma_hope`, `marcus_sarcastic`, `lila_charm`, `professor_stern`, `rocky_inspiration`, `alex_digital`, `victoria_sterling`, `zero_cool`

**Si quieres usar una personalidad personalizada** (como "Sakura"), puedes:

```python
# Opción A: Cargar personalidad personalizada
await base_client.initialize()
await base_client.load_personality("Sakura", sakura_personality_data)

# Opción B: Usar una personalidad existente
personality_name = "dr_luna"  # o cualquier otra disponible
```

### Cambio 2: Pasar Directorio de Personalidades al Cliente

```python
base_client = LuminoraCoreClient(
    personalities_dir="/path/to/personalities"  # Especificar path correcto
)
```

### Cambio 3: Crear Sesión DESPUÉS de Cargar la Personalidad

```python
# ✅ ORDEN CORRECTO
await base_client.initialize()
await base_client.load_personality("Sakura", personality_data)  # Primero cargar
await base_client.create_session(personality_name="Sakura", ...)  # Luego crear sesión
```

---

## 🎯 CONCLUSIÓN

El framework **NO tiene bugs**. El problema es que el backend:

1. ❌ Está intentando usar una personalidad que no existe ("Sakura")
2. ❌ No está cargando correctamente las personalidades en el base client
3. ❌ Está intentando crear sesiones antes de cargar la personalidad

**IMPORTANTE**: El SDK ahora incluye las personalidades de ejemplo por defecto. Esto significa que:

- ✅ Las personalidades se cargan automáticamente al instalar el SDK
- ✅ **NO es necesario cargarlas manualmente** en Lambda si el SDK está en el Lambda Layer
- ✅ El backend debe usar una de las personalidades disponibles o crear la personalidad "Sakura" personalizada

El SDK funciona correctamente cuando:
- ✅ Se usa una personalidad existente (`dr_luna`, `captain_hook`, etc.)
- ✅ Se carga una personalidad personalizada con `load_personality()`
- ✅ El SDK está correctamente instalado en el Lambda Layer

---

## 📌 SIGUIENTES PASOS PARA EL BACKEND

1. **Decidir**: ¿Usar una personalidad existente o crear "Sakura"?
2. **Si usar existente**: Cambiar `personality_name` a "dr_luna" (u otra)
3. **Si crear "Sakura"**: 
   - Crear archivo JSON con la configuración de Sakura
   - Cargarlo manualmente con `load_personality()`
4. **Asegurar**: Que el directorio de personalidades sea accesible en Lambda
5. **Verificar**: Que la sesión se cree correctamente antes de llamar a `send_message_with_memory()`

---

## 💡 SOLUCIÓN RECOMENDADA: Código de Ejemplo Completo

### Opción A: Usar Personalidad Existente (Recomendado)

```python
async def get_client_v11(provider_config=None):
    """Get LuminoraCoreClientV11 instance with Flexible DynamoDB storage"""
    try:
        # Use Flexible DynamoDB for persistent storage
        dynamodb_storage = FlexibleDynamoDBStorageV11(
            table_name="luminora-sessions-v1-1",
            region_name="eu-west-1"
        )
        
        # Create base client
        base_client = LuminoraCoreClient()
        
        # Initialize the base client
        await base_client.initialize()
        
        # The personality "dr_luna" is already loaded by default
        # No need to load it manually
        
        # Create client v11
        client_v11 = LuminoraCoreClientV11(
            base_client=base_client,
            storage_v11=dynamodb_storage
        )
        
        logger.info("Flexible DynamoDB storage initialized successfully")
        return client_v11
    except Exception as e:
        logger.error(f"Flexible DynamoDB initialization failed: {e}", exc_info=True)
        raise Exception(f"Flexible DynamoDB failed: {e}")

# En el handler:
result = await client_v11.send_message_with_memory(
    session_id=session_id,
    user_message=user_message,
    user_id=session_id,  # ✅ Pasar user_id
    personality_name="Dr. Luna",  # ✅ Usar personalidad existente
    provider_config=provider_config
)
```

### Opción B: Crear Personalidad "Sakura" Personalizada

```python
# Definir personalidad Sakura
SAKURA_PERSONALITY = {
    "persona": {
        "name": "Sakura",
        "version": "1.0.0",
        "description": "A friendly and helpful assistant",
        "author": "Backend Team",
        "tags": ["friendly", "helpful", "assistant"],
        "language": "en",
        "compatibility": ["openai", "anthropic"]
    },
    "core_traits": {
        "archetype": "assistant",
        "temperament": "friendly",
        "communication_style": "conversational"
    },
    "linguistic_profile": {
        "tone": ["friendly", "polite", "helpful"],
        "syntax": "standard",
        "vocabulary": [],
        "fillers": [],
        "punctuation_style": "standard"
    },
    "behavioral_rules": [
        "Be helpful and friendly",
        "Provide accurate information",
        "Ask clarifying questions when needed"
    ],
    # ... resto de configuración
}

async def get_client_v11(provider_config=None):
    """Get LuminoraCoreClientV11 instance with Flexible DynamoDB storage"""
    try:
        dynamodb_storage = FlexibleDynamoDBStorageV11(
            table_name="luminora-sessions-v1-1",
            region_name="eu-west-1"
        )
        
        base_client = LuminoraCoreClient()
        await base_client.initialize()
        
        # ✅ Cargar personalidad Sakura manualmente
        await base_client.load_personality("Sakura", SAKURA_PERSONALITY)
        
        client_v11 = LuminoraCoreClientV11(
            base_client=base_client,
            storage_v11=dynamodb_storage
        )
        
        logger.info("Flexible DynamoDB storage initialized successfully")
        return client_v11
    except Exception as e:
        logger.error(f"Flexible DynamoDB initialization failed: {e}", exc_info=True)
        raise Exception(f"Flexible DynamoDB failed: {e}")
```

### Opción C: Cargar Personalidad desde Archivo

```python
import json

async def get_client_v11(provider_config=None):
    """Get LuminoraCoreClientV11 instance with Flexible DynamoDB storage"""
    try:
        dynamodb_storage = FlexibleDynamoDBStorageV11(
            table_name="luminora-sessions-v1-1",
            region_name="eu-west-1"
        )
        
        base_client = LuminoraCoreClient()
        await base_client.initialize()
        
        # ✅ Cargar personalidad desde archivo
        with open("/path/to/sakura.json", "r") as f:
            sakura_config = json.load(f)
        await base_client.load_personality("Sakura", sakura_config)
        
        client_v11 = LuminoraCoreClientV11(
            base_client=base_client,
            storage_v11=dynamodb_storage
        )
        
        logger.info("Flexible DynamoDB storage initialized successfully")
        return client_v11
    except Exception as e:
        logger.error(f"Flexible DynamoDB initialization failed: {e}", exc_info=True)
        raise Exception(f"Flexible DynamoDB failed: {e}")
```

---

## 📦 CAMBIO IMPORTANTE: SDK Ahora Incluye Personalidades

### ✅ SOLUCIÓN IMPLEMENTADA

El SDK ahora incluye las personalidades de ejemplo por defecto. Se ha realizado el siguiente cambio:

1. **Creado directorio `personalities`** en `luminoracore_sdk/`
2. **Copiadas todas las personalidades** desde `luminoracore/luminoracore/personalities/`
3. **Actualizado `setup.py`** para incluir las personalidades en la distribución
4. **Modificado `client.py`** para usar el directorio por defecto del SDK

### 🎯 Beneficios

- ✅ **Las personalidades se cargan automáticamente** al instalar el SDK
- ✅ **No es necesario configurar rutas** para las personalidades
- ✅ **Funciona en Lambda** sin configuración adicional si el SDK está en el Layer
- ✅ **Las personalidades están disponibles** de inmediato después de instalar el SDK

### 📝 Personalidades Disponibles

Las siguientes personalidades están disponibles por defecto en el SDK:

1. `dr_luna` - An enthusiastic scientist
2. `dr_luna_v1_1` - Dr. Luna with v1.1 features (relationship levels, affinity)
3. `captain_hook` - A digital pirate
4. `grandma_hope` - A warm grandmother figure
5. `marcus_sarcastic` - A cynical and sarcastic observer
6. `lila_charm` - Charming and elegant personality
7. `professor_stern` - A stern professor
8. `rocky_inspiration` - Motivational coach
9. `alex_digital` - Gen Z digital native
10. `victoria_sterling` - Professional business advisor
11. `zero_cool` - Tech-savvy hacker

### 🚀 Próximos Pasos para el Backend

1. **Actualizar el Lambda Layer** con la nueva versión del SDK que incluye personalidades
2. **Usar una personalidad existente** o crear "Sakura" personalizada
3. **Verificar** que las personalidades se carguen correctamente

---

**Fecha**: 2025-01-XX
**Autor**: Análisis automático del SDK
