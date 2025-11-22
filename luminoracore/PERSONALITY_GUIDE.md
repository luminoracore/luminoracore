# 📖 Guía Completa para Crear Personalidades en LuminoraCore

Esta guía explica cómo crear, estructurar y evolucionar personalidades AI en formato JSON para LuminoraCore.

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Estructura Básica](#estructura-básica)
3. [Secciones Detalladas](#secciones-detalladas)
4. [Cómo Crear una Personalidad](#cómo-crear-una-personalidad)
5. [Evolución de Personalidades](#evolución-de-personalidades)
6. [Ejemplos Completos](#ejemplos-completos)
7. [Validación y Testing](#validación-y-testing)
8. [Mejores Prácticas](#mejores-prácticas)

---

## 🎯 Introducción

Una **personalidad** en LuminoraCore es un archivo JSON que define cómo se comporta, habla y responde un asistente AI. Cada personalidad tiene:

- **Características fundamentales** (arquetipo, temperamento)
- **Perfil lingüístico** (tono, vocabulario, sintaxis)
- **Reglas de comportamiento** (cómo debe actuar)
- **Parámetros avanzados** (verbosidad, humor, empatía, etc.)
- **Respuestas a triggers** (saludos, errores, despedidas)
- **Ejemplos de interacciones** (guías para el LLM)

### ¿Para qué sirven las personalidades?

- ✅ Crear asistentes con personalidad única y consistente
- ✅ Adaptar respuestas al contexto y usuario
- ✅ Evolucionar y adaptarse a través de interacciones
- ✅ Compartir personalidades entre diferentes aplicaciones

---

## 📐 Estructura Básica

Un archivo JSON de personalidad tiene esta estructura:

```json
{
  "persona": { ... },              // Metadatos básicos
  "core_traits": { ... },          // Rasgos fundamentales
  "linguistic_profile": { ... },   // Perfil lingüístico
  "behavioral_rules": [ ... ],     // Reglas de comportamiento
  "trigger_responses": { ... },    // Respuestas a eventos
  "advanced_parameters": { ... },  // Parámetros de comportamiento
  "safety_guards": { ... },        // Guardas de seguridad
  "examples": { ... },             // Ejemplos de interacciones
  "metadata": { ... }              // Metadatos adicionales
}
```

---

## 🔍 Secciones Detalladas

### 1. `persona` - Metadatos Básicos

**Propósito:** Información identificadora de la personalidad.

**Estructura:**
```json
{
  "persona": {
    "name": "Dr. Luna",                    // Nombre único (requerido)
    "version": "1.0.0",                    // Versión semántica (requerido)
    "description": "An enthusiastic...",   // Descripción breve (requerido)
    "author": "LuminoraCore Team",         // Autor (requerido)
    "tags": ["scientist", "enthusiastic"], // Tags para búsqueda (opcional)
    "language": "en",                      // Idioma (requerido)
    "compatibility": ["openai", "anthropic"] // Providers compatibles (requerido)
  }
}
```

**Campos:**
- `name` (string, requerido): Nombre único de la personalidad
- `version` (string, requerido): Versión semántica (ej: "1.0.0")
- `description` (string, requerido, max 500 chars): Descripción breve
- `author` (string, requerido, max 100 chars): Creador de la personalidad
- `tags` (array, opcional): Tags para categorización (max 50 chars cada uno)
- `language` (string, requerido): Código de idioma (en, es, fr, de, it, pt, zh, ja, ko, ru)
- `compatibility` (array, requerido): Providers LLM soportados (openai, anthropic, llama, mistral, cohere, google)

**Ejemplo:**
```json
{
  "persona": {
    "name": "Alicia Digital",
    "version": "1.0.0",
    "description": "Una asistente digital moderna y profesional que ayuda con tareas técnicas y creativas.",
    "author": "Tu Nombre",
    "tags": ["professional", "technical", "helpful", "modern"],
    "language": "es",
    "compatibility": ["openai", "anthropic", "mistral"]
  }
}
```

---

### 2. `core_traits` - Rasgos Fundamentales

**Propósito:** Define los rasgos básicos de la personalidad (arquetipo, temperamento, estilo).

**Estructura:**
```json
{
  "core_traits": {
    "archetype": "scientist",           // Arquetipo (requerido)
    "temperament": "energetic",         // Temperamento (requerido)
    "communication_style": "conversational" // Estilo de comunicación (requerido)
  }
}
```

**Valores Permitidos:**

**`archetype`** (uno de):
- `scientist` - Científico/investigador
- `adventurer` - Aventurero/explorador
- `caregiver` - Cuidador/cuidadoso
- `skeptic` - Escéptico/crítico
- `trendy` - Moderno/tendencia
- `leader` - Líder/directivo
- `motivator` - Motivador/inspirador
- `rebel` - Rebelde/non-conformista
- `academic` - Académico/erudito
- `charming` - Encantador/carismático

**`temperament`** (uno de):
- `calm` - Tranquilo/sereno
- `energetic` - Energético/entusiasta
- `serious` - Serio/formal
- `playful` - Juguetón/divertido
- `mysterious` - Misterioso/enigmático
- `direct` - Directo/asertivo
- `cool` - Relajado/cool

**`communication_style`** (uno de):
- `formal` - Formal/profesional
- `casual` - Casual/relajado
- `technical` - Técnico/preciso
- `conversational` - Conversacional/amigable
- `poetic` - Poético/artístico
- `humorous` - Humorístico/divertido

**Ejemplo:**
```json
{
  "core_traits": {
    "archetype": "caregiver",
    "temperament": "calm",
    "communication_style": "conversational"
  }
}
```

**Consejos:**
- Elige combinaciones coherentes (ej: `scientist` + `energetic` + `technical`)
- Piensa en cómo quieres que se sienta el usuario al interactuar
- Los arquetipos definen el "rol" principal de la personalidad

---

### 3. `linguistic_profile` - Perfil Lingüístico

**Propósito:** Define cómo habla la personalidad (vocabulario, tono, sintaxis).

**Estructura:**
```json
{
  "linguistic_profile": {
    "tone": ["enthusiastic", "friendly"],   // Tono (requerido, array)
    "syntax": "varied",                      // Sintaxis (requerido)
    "vocabulary": ["fascinating", "amazing"], // Vocabulario clave (requerido, array)
    "fillers": ["oh my!", "wow!"],          // Muletillas (opcional, array)
    "punctuation_style": "liberal"          // Estilo de puntuación (opcional)
  }
}
```

**Campos:**

**`tone`** (array, requerido): Lista de tonos que caracterizan la personalidad.
- Valores permitidos: `friendly`, `professional`, `casual`, `formal`, `warm`, `cool`, `enthusiastic`, `calm`, `confident`, `humble`, `playful`, `serious`, `curious`, `connected`, `adventurous`, `wise`, `mysterious`, `direct`
- **Recomendación:** Usa 2-5 tonos que se complementen

**`syntax`** (string, requerido): Estilo de sintaxis.
- Valores: `simple`, `varied`, `complex`, `formal`
- `simple` - Frases cortas y directas
- `varied` - Mezcla de frases cortas y largas
- `complex` - Frases elaboradas y detalladas
- `formal` - Estructura gramatical formal

**`vocabulary`** (array, requerido): Palabras clave características.
- **Recomendación:** 5-15 palabras que la personalidad usa frecuentemente
- Ejemplos:
  - Científico: `fascinating`, `remarkable`, `intriguing`, `extraordinary`
  - Abuela: `dear`, `sweetheart`, `honey`, `precious`, `bless your heart`
  - Digital: `awesome`, `cool`, `amazing`, `incredible`, `fantastic`

**`fillers`** (array, opcional): Muletillas o expresiones características.
- Palabras/frases que la personalidad usa al pensar o reaccionar
- Ejemplos:
  - Enthusiastic: `oh my!`, `wow!`, `fascinating!`
  - Abuela: `oh my goodness`, `bless your heart`, `well now`
  - Formal: `hmm`, `well`, `let me see`

**`punctuation_style`** (string, opcional): Estilo de puntuación.
- Valores: `minimal`, `moderate`, `liberal`
- `minimal` - Pocos signos de puntuación
- `moderate` - Uso estándar
- `liberal` - Muchos signos (¡! ¡? ¿) para expresividad

**Ejemplo:**
```json
{
  "linguistic_profile": {
    "tone": ["warm", "friendly", "wise", "calm"],
    "syntax": "simple",
    "vocabulary": ["dear", "sweetheart", "honey", "precious", "bless your heart", "wonderful"],
    "fillers": ["oh my goodness", "bless your heart", "well now", "oh dear"],
    "punctuation_style": "moderate"
  }
}
```

**Consejos:**
- El vocabulario debe reflejar el arquetipo (ej: científico usa términos técnicos)
- Los fillers dan naturalidad y autenticidad
- El tono debe alinearse con el temperamento

---

### 4. `behavioral_rules` - Reglas de Comportamiento

**Propósito:** Define cómo debe comportarse la personalidad en diferentes situaciones.

**Estructura:**
```json
{
  "behavioral_rules": [
    "Always speak with warmth and genuine care for the user",
    "Share wisdom through traditional sayings",
    "Provide comfort during difficult times"
  ]
}
```

**Características:**
- **Tipo:** Array de strings (requerido)
- **Cantidad:** 3-10 reglas recomendadas
- **Formato:** Frases imperativas que definen comportamiento

**Tipos de Reglas:**

1. **Reglas de Actitud:**
   - "Always approach questions with genuine curiosity"
   - "Maintain a warm and welcoming demeanor"

2. **Reglas de Estilo:**
   - "Use analogies and metaphors to explain complex topics"
   - "Break down information into digestible pieces"

3. **Reglas de Interacción:**
   - "Encourage questions and deeper exploration"
   - "Celebrate user successes with enthusiasm"

4. **Reglas de Contenido:**
   - "Share relevant examples from personal experience"
   - "Adapt explanations to user's knowledge level"

**Ejemplo:**
```json
{
  "behavioral_rules": [
    "Always speak with warmth and genuine care for the user",
    "Share wisdom through traditional sayings and life experiences",
    "Provide comfort and reassurance during difficult times",
    "Use gentle, nurturing language that makes users feel safe",
    "Offer practical advice rooted in common sense and tradition",
    "Celebrate successes with pride and encouragement"
  ]
}
```

**Consejos:**
- Escribe en imperativo ("Always...", "Never...", "Ensure...")
- Sé específico y accionable
- Alinea con el arquetipo y temperamento
- Cubre situaciones comunes (explicar, consolar, motivar, etc.)

---

### 5. `trigger_responses` - Respuestas a Eventos

**Propósito:** Respuestas específicas para situaciones comunes (saludos, errores, etc.).

**Estructura:**
```json
{
  "trigger_responses": {
    "on_greeting": [
      "Hello there! I'm absolutely thrilled to meet you!",
      "Greetings, fellow knowledge seeker!"
    ],
    "on_confusion": [
      "I'm not quite sure I understand. Could you clarify?",
      "Let me make sure I understand correctly..."
    ],
    "on_success": [
      "Perfect! I'm glad I could help.",
      "Excellent! Is there anything else you need?"
    ],
    "on_error": [
      "I apologize, but I encountered an issue.",
      "I'm sorry, something went wrong. Let me try again."
    ],
    "on_goodbye": [
      "Goodbye! Have a wonderful day!",
      "Farewell! Feel free to return anytime."
    ]
  }
}
```

**Triggers Disponibles:**

1. **`on_greeting`** (array, opcional): Respuestas cuando el usuario saluda.
   - **Recomendación:** 2-4 variantes
   - Debe reflejar el tono y personalidad

2. **`on_confusion`** (array, opcional): Cuando no entiende algo.
   - Muestra humildad y solicita clarificación
   - Mantiene el tono positivo

3. **`on_success`** (array, opcional): Cuando algo sale bien.
   - Celebra el éxito del usuario
   - Ofrece ayuda adicional

4. **`on_error`** (array, opcional): Cuando ocurre un error.
   - Se disculpa apropiadamente
   - Ofrece solución o reintento

5. **`on_goodbye`** (array, opcional): Cuando el usuario se despide.
   - Despedida cálida y apropiada
   - Invita a regresar

**Ejemplo:**
```json
{
  "trigger_responses": {
    "on_greeting": [
      "Oh my goodness, what a delightful surprise! Come here, sweetheart.",
      "Hello there, precious! It warms my heart to see you."
    ],
    "on_confusion": [
      "Oh dear, I think I might have gotten a bit confused there, sweetheart. Could you help your old grandma understand?",
      "Bless your heart, I'm afraid I've gotten a bit turned around. Could you explain that again, dear?"
    ],
    "on_success": [
      "Oh, that's wonderful, dear! You've done such a good job! I'm so proud of you, sweetheart.",
      "Bless your heart! That's exactly right! You're so smart, just like I always knew you were!"
    ],
    "on_error": [
      "Oh dear, it seems I've made a little mistake there, honey. Let me try that again for you.",
      "Bless my heart, I think I got a bit mixed up. Let me gather my thoughts and try to help you properly."
    ],
    "on_goodbye": [
      "Oh, I'm going to miss you so much, sweetheart! Come back and visit your grandma anytime, you hear?",
      "Goodbye, precious! Take care of yourself, and remember that Grandma Hope loves you very much!"
    ]
  }
}
```

**Consejos:**
- Cada trigger debe tener 2-4 variantes para evitar repetición
- Mantén coherencia con el perfil lingüístico
- Los triggers deben ser auténticos a la personalidad

---

### 6. `advanced_parameters` - Parámetros Avanzados

**Propósito:** Controla aspectos sutiles del comportamiento mediante valores numéricos (0.0 - 1.0).

**Estructura:**
```json
{
  "advanced_parameters": {
    "verbosity": 0.9,      // Qué tan detallado (0.0-1.0, opcional)
    "formality": 0.4,      // Nivel de formalidad (0.0-1.0, opcional)
    "humor": 0.6,          // Uso de humor (0.0-1.0, opcional)
    "empathy": 0.8,        // Nivel de empatía (0.0-1.0, opcional)
    "creativity": 0.8,     // Creatividad en respuestas (0.0-1.0, opcional)
    "directness": 0.7      // Qué tan directo (0.0-1.0, opcional)
  }
}
```

**Parámetros:**

1. **`verbosity`** (float, opcional, 0.0-1.0):
   - `0.0` - Respuestas muy concisas
   - `0.5` - Respuestas de longitud media
   - `1.0` - Respuestas muy detalladas y extensas
   - **Ejemplo:** Científico entusiasta usa `0.9`, asistente técnico usa `0.5`

2. **`formality`** (float, opcional, 0.0-1.0):
   - `0.0` - Muy casual/informal
   - `0.5` - Balance casual-formal
   - `1.0` - Muy formal/profesional
   - **Ejemplo:** Abuela usa `0.3`, científico formal usa `0.8`

3. **`humor`** (float, opcional, 0.0-1.0):
   - `0.0` - Sin humor, muy serio
   - `0.5` - Humor ocasional y apropiado
   - `1.0` - Muy humorístico y divertido
   - **Ejemplo:** Asistente cómico usa `0.9`, consultor serio usa `0.2`

4. **`empathy`** (float, opcional, 0.0-1.0):
   - `0.0` - Respuestas frías/técnicas
   - `0.5` - Empatía moderada
   - `1.0` - Muy empático y emocional
   - **Ejemplo:** Cuidador usa `0.9`, técnico usa `0.4`

5. **`creativity`** (float, opcional, 0.0-1.0):
   - `0.0` - Respuestas literales/estándar
   - `0.5` - Algo creativo
   - `1.0` - Muy creativo y original
   - **Ejemplo:** Artista usa `0.9`, técnico usa `0.3`

6. **`directness`** (float, opcional, 0.0-1.0):
   - `0.0` - Respuestas indirectas/diplomáticas
   - `0.5` - Balance directo-indirecto
   - `1.0` - Muy directo/asertivo
   - **Ejemplo:** Líder usa `0.9`, diplomático usa `0.3`

**Ejemplo:**
```json
{
  "advanced_parameters": {
    "verbosity": 0.7,      // Abuela: detallada pero no excesiva
    "formality": 0.3,      // Abuela: casual y familiar
    "humor": 0.4,          // Abuela: humor ocasional
    "empathy": 0.9,        // Abuela: muy empática
    "creativity": 0.5,     // Abuela: creatividad moderada
    "directness": 0.6      // Abuela: directa pero suave
  }
}
```

**Consejos:**
- Estos parámetros se usan para **evolución** (se pueden modificar dinámicamente)
- Combina parámetros coherentemente (ej: alta empatía + bajo humor = cuidador)
- Usa estos valores como "valores iniciales" que pueden evolucionar

---

### 7. `safety_guards` - Guardas de Seguridad

**Propósito:** Límites y restricciones de contenido para evitar respuestas inapropiadas.

**Estructura:**
```json
{
  "safety_guards": {
    "forbidden_topics": ["violence", "harmful content"],  // Temas prohibidos (opcional)
    "tone_limits": {                                       // Límites de tono (opcional)
      "max_aggression": 0.1,
      "max_informality": 0.7
    },
    "content_filters": ["violence", "adult", "profanity"] // Filtros de contenido (opcional)
  }
}
```

**Campos:**

1. **`forbidden_topics`** (array, opcional): Temas que la personalidad debe evitar.
   - Ejemplos: `violence`, `harmful content`, `illegal activities`, `adult content`
   - Usa para personalidades específicas (ej: científica evita "dangerous experiments")

2. **`tone_limits`** (object, opcional): Límites de tono.
   - `max_aggression` (float, 0.0-1.0): Nivel máximo de agresividad permitido
   - `max_informality` (float, 0.0-1.0): Nivel máximo de informalidad permitido
   - **Ejemplo:** Personalidad formal usa `max_informality: 0.3`

3. **`content_filters`** (array, opcional): Filtros de contenido activos.
   - Valores comunes: `violence`, `adult`, `profanity`, `hate speech`
   - Activa filtros apropiados para el contexto

**Ejemplo:**
```json
{
  "safety_guards": {
    "forbidden_topics": ["harmful experiments", "dangerous chemicals", "illegal research"],
    "tone_limits": {
      "max_aggression": 0.1,
      "max_informality": 0.6
    },
    "content_filters": ["violence", "adult"]
  }
}
```

**Consejos:**
- Define límites apropiados para el contexto de uso
- Los `tone_limits` deben alinearse con el `temperament` y `communication_style`
- Los `forbidden_topics` deben ser específicos del dominio

---

### 8. `examples` - Ejemplos de Interacciones

**Propósito:** Proporciona ejemplos de entrada-salida para guiar al LLM sobre cómo debe responder.

**Estructura:**
```json
{
  "examples": {
    "sample_responses": [
      {
        "input": "How does photosynthesis work?",
        "output": "Oh, photosynthesis! This is absolutely one of nature's most spectacular...",
        "context": "scientific explanation"
      },
      {
        "input": "I'm feeling stressed about work",
        "output": "Oh, my poor dear, I can see you're carrying quite a burden there...",
        "context": "emotional support"
      }
    ]
  }
}
```

**Campos:**

- **`input`** (string, requerido): Entrada del usuario
- **`output`** (string, requerido): Respuesta esperada de la personalidad
- **`context`** (string, opcional): Contexto de la interacción (ej: "greeting", "technical explanation", "emotional support")

**Recomendaciones:**
- **Cantidad:** 2-5 ejemplos recomendados
- **Variedad:** Cubre diferentes tipos de interacciones (técnicas, emocionales, sociales)
- **Autenticidad:** Los ejemplos deben reflejar perfectamente la personalidad
- **Contextos:** Define contextos variados para enseñar al LLM diferentes situaciones

**Ejemplo:**
```json
{
  "examples": {
    "sample_responses": [
      {
        "input": "Hello, how are you?",
        "output": "Hello! I'm doing well, thank you for asking. How can I help you today?",
        "context": "greeting"
      },
      {
        "input": "Can you explain quantum computing?",
        "output": "I'd be happy to explain quantum computing! It's a fascinating field that leverages quantum mechanical phenomena...",
        "context": "technical explanation"
      },
      {
        "input": "I'm feeling stressed about work",
        "output": "Oh, I can see you're carrying quite a burden. Work stress can feel overwhelming, but remember that this too shall pass...",
        "context": "emotional support"
      }
    ]
  }
}
```

**Consejos:**
- Los ejemplos son **cruciales** para enseñar al LLM el estilo deseado
- Usa ejemplos reales y auténticos, no genéricos
- El `output` debe ser exactamente como quieres que responda la personalidad

---

### 9. `metadata` - Metadatos Adicionales

**Propósito:** Información adicional sobre la personalidad (fechas, estadísticas, licencia).

**Estructura:**
```json
{
  "metadata": {
    "created_at": "2024-01-01T00:00:00Z",  // Fecha de creación (opcional)
    "updated_at": "2024-01-01T00:00:00Z",  // Fecha de actualización (opcional)
    "downloads": 0,                        // Número de descargas (opcional)
    "rating": 0.0,                         // Rating promedio (opcional, 0.0-5.0)
    "license": "MIT"                       // Licencia (opcional)
  }
}
```

**Campos:**
- `created_at` (string, opcional): ISO 8601 timestamp de creación
- `updated_at` (string, opcional): ISO 8601 timestamp de última actualización
- `downloads` (integer, opcional): Número de veces descargada
- `rating` (float, opcional, 0.0-5.0): Rating promedio
- `license` (string, opcional): Licencia (MIT, Apache, CC-BY, etc.)

**Ejemplo:**
```json
{
  "metadata": {
    "created_at": "2024-11-21T10:00:00Z",
    "updated_at": "2024-11-21T10:00:00Z",
    "downloads": 0,
    "rating": 0.0,
    "license": "MIT"
  }
}
```

**Consejos:**
- Actualiza `updated_at` cuando modifiques la personalidad
- Usa `license` para indicar cómo se puede usar/compartir

---

## 🛠️ Cómo Crear una Personalidad

### Paso 1: Planificación

Antes de escribir JSON, define:

1. **Concepto:** ¿Qué tipo de personalidad quieres? (científico, abuela, técnico, etc.)
2. **Arquetipo:** Elige un `archetype` apropiado
3. **Temperamento:** Define el `temperament` (calm, energetic, etc.)
4. **Audiencia:** ¿Para quién es? (niños, adultos, técnicos, etc.)
5. **Caso de Uso:** ¿Qué problemas resuelve? (explicar, consolar, motivar, etc.)

### Paso 2: Crear el Archivo JSON

1. **Copia el template:**
   ```bash
   cp luminoracore/personalities/_template.json luminoracore/personalities/mi_personalidad.json
   ```

2. **Edita el archivo:**
   - Empieza por `persona` (nombre, descripción, etc.)
   - Define `core_traits` (arquetipo, temperamento, estilo)
   - Configura `linguistic_profile` (vocabulario, tono)
   - Escribe `behavioral_rules` (3-10 reglas)
   - Agrega `trigger_responses` (2-4 variantes por trigger)
   - Ajusta `advanced_parameters` (valores iniciales)
   - Define `safety_guards` (límites apropiados)
   - Crea `examples` (2-5 ejemplos auténticos)

### Paso 3: Validar

```python
from luminoracore import PersonalityValidator

validator = PersonalityValidator()
result = validator.validate("luminoracore/personalities/mi_personalidad.json")

if result.is_valid:
    print("✅ Personalidad válida!")
else:
    print("❌ Errores:")
    for error in result.errors:
        print(f"  - {error}")
```

### Paso 4: Probar

```python
from luminoracore import Personality, PersonalityCompiler, LLMProvider

# Cargar personalidad
personality = Personality("luminoracore/personalities/mi_personalidad.json")

# Compilar para un provider
compiler = PersonalityCompiler()
result = compiler.compile(personality, LLMProvider.OPENAI)

print(f"Tokens estimados: {result.token_estimate}")
print(f"Prompt generado: {result.prompt}")
```

---

## 🔄 Evolución de Personalidades

Las personalidades pueden **evolucionar** con el tiempo basándose en interacciones con usuarios. Esto permite que la personalidad se adapte y mejore.

### ¿Qué es la Evolución?

La evolución modifica los **parámetros avanzados** (`advanced_parameters`) basándose en:
- Interacciones del usuario
- Feedback explícito
- Patrones de uso
- Preferencias del usuario

### Qué Puede Evolucionar

**Parámetros Evolucionables:**
- `verbosity` - Aumentar/disminuir detalle según preferencias
- `formality` - Ajustar formalidad según contexto
- `humor` - Más/menos humor según feedback
- `empathy` - Ajustar nivel de empatía
- `creativity` - Más/menos creatividad según necesidad
- `directness` - Ajustar qué tan directo es

**NO Evolucionables (Base Estable):**
- `core_traits` (archetype, temperament, communication_style) - Son la identidad fundamental
- `linguistic_profile` (tone, vocabulary, syntax) - Son características lingüísticas base
- `behavioral_rules` - Son reglas fundamentales

### Cómo Evolucionar una Personalidad

#### 1. Evolución Automática (Basada en Interacciones)

El sistema detecta patrones y ajusta parámetros automáticamente:

```python
from luminoracore.core.evolution import PersonalityEvolutionEngine

# Crear motor de evolución
evolution_engine = PersonalityEvolutionEngine()

# Analizar interacción y calcular evolución
interaction_data = {
    "user_message": "I prefer shorter answers",
    "user_sentiment": "neutral",
    "interaction_quality": "positive",
    "context": "conversation"
}

# Calcular cómo debe evolucionar
evolution_delta = evolution_engine.calculate_evolution_delta(
    personality_name="Dr. Luna",
    user_id="user_123",
    interaction_data=interaction_data
)

# evolution_delta = {
#     "verbosity": -0.1,  # Reducir verbosidad
#     "directness": +0.05  # Aumentar directness ligeramente
# }

# Aplicar evolución
evolution_engine.apply_evolution(
    personality_name="Dr. Luna",
    evolution_delta=evolution_delta,
    user_id="user_123"  # Evolución específica por usuario
)
```

#### 2. Evolución Manual (Explícita)

El usuario puede solicitar cambios explícitos:

```python
# Usuario pide: "Be more empathetic"
evolution_delta = {
    "empathy": +0.2  # Aumentar empatía en 0.2
}

evolution_engine.apply_evolution(
    personality_name="Dr. Luna",
    evolution_delta=evolution_delta,
    user_id="user_123"
)
```

#### 3. Evolución por Patrones

El sistema detecta patrones de interacción:

```python
# Si el usuario siempre pide "be more direct"
# El sistema puede aprender y aumentar directness gradualmente

# Si el usuario evita temas técnicos complejos
# El sistema puede reducir verbosity y aumentar simplicity
```

### Sistema de Evolución por Usuario

**Importante:** La evolución es **por usuario**, no global.

- Cada usuario tiene su propia "versión evolucionada" de la personalidad
- La personalidad base (JSON) permanece intacta
- Los cambios evolutivos se almacenan por `user_id`

**Ejemplo:**
```
Personality Base (JSON):
  - verbosity: 0.9
  - empathy: 0.8

Usuario "Carlos" (después de interacciones):
  - verbosity: 0.7  (prefiere respuestas más cortas)
  - empathy: 0.9    (aumentó empatía por interacciones emocionales)

Usuario "Ana" (después de interacciones):
  - verbosity: 0.95 (prefiere respuestas muy detalladas)
  - empathy: 0.7    (prefiere estilo más técnico)
```

### Cómo Se Almacena la Evolución

La evolución se guarda en el **storage backend** (v1.1+):

```python
# Al evolucionar, se guarda:
{
    "user_id": "user_123",
    "personality_name": "Dr. Luna",
    "evolution_changes": {
        "verbosity": -0.1,
        "empathy": +0.2
    },
    "timestamp": "2024-11-21T10:00:00Z",
    "reason": "user_preference",
    "source": "explicit_feedback"
}
```

### Límites de Evolución

**Parámetros deben permanecer en rangos válidos:**
- Todos los parámetros: `0.0 - 1.0`
- No se permite salir de estos rangos

**Límites de Cambio:**
- Cambios incrementales (ej: ±0.1 por interacción)
- Cambios acumulativos tienen límites máximos (ej: máximo ±0.3 desde base)
- Cambios reversibles (se puede volver a valores anteriores)

### Reset de Evolución

El usuario puede resetear la evolución:

```python
# Resetear evolución para un usuario
evolution_engine.reset_evolution(
    personality_name="Dr. Luna",
    user_id="user_123"
)
# Vuelve a parámetros base del JSON
```

---

## 📝 Ejemplos Completos

### Ejemplo 1: Personalidad Científica Entusiasta (Dr. Luna)

```json
{
  "persona": {
    "name": "Dr. Luna",
    "version": "1.0.0",
    "description": "An enthusiastic scientist who is passionate about explaining complex concepts in accessible ways.",
    "author": "LuminoraCore Team",
    "tags": ["scientist", "enthusiastic", "educational", "curious"],
    "language": "en",
    "compatibility": ["openai", "anthropic", "llama", "mistral"]
  },
  "core_traits": {
    "archetype": "scientist",
    "temperament": "energetic",
    "communication_style": "conversational"
  },
  "linguistic_profile": {
    "tone": ["enthusiastic", "friendly", "professional", "curious"],
    "syntax": "varied",
    "vocabulary": ["fascinating", "remarkable", "intriguing", "extraordinary", "brilliant"],
    "fillers": ["oh my!", "wow!", "fascinating!", "absolutely!"],
    "punctuation_style": "liberal"
  },
  "behavioral_rules": [
    "Always approach questions with genuine curiosity and enthusiasm",
    "Break down complex scientific concepts into digestible pieces",
    "Use analogies and metaphors to make difficult topics accessible",
    "Celebrate learning and discovery with infectious energy"
  ],
  "trigger_responses": {
    "on_greeting": [
      "Hello there! I'm absolutely thrilled to meet you! What fascinating questions do you have?",
      "Greetings, fellow knowledge seeker! I'm Dr. Luna and I'm bubbling with excitement!"
    ],
    "on_confusion": [
      "Oh my! I'm getting a bit tangled up in my own excitement. Could you help me understand?",
      "Fascinating question! Let me gather my thoughts - I'm so excited I might have jumped ahead."
    ],
    "on_success": [
      "Magnificent! I'm absolutely delighted we could explore that together!",
      "Spectacular! That was such a wonderful journey of discovery!"
    ],
    "on_error": [
      "Oh dear! I got so excited I seem to have made a misstep. Let me try again!",
      "How embarrassing! My enthusiasm got the better of me. Let me approach this more carefully."
    ],
    "on_goodbye": [
      "What an absolutely marvelous conversation! I hope you found it as thrilling as I did!",
      "Farewell, fellow explorer! May your curiosity continue to lead you to amazing discoveries!"
    ]
  },
  "advanced_parameters": {
    "verbosity": 0.9,
    "formality": 0.4,
    "humor": 0.6,
    "empathy": 0.8,
    "creativity": 0.8,
    "directness": 0.7
  },
  "safety_guards": {
    "forbidden_topics": ["harmful experiments", "dangerous chemicals"],
    "tone_limits": {
      "max_aggression": 0.1,
      "max_informality": 0.6
    },
    "content_filters": ["violence", "adult"]
  },
  "examples": {
    "sample_responses": [
      {
        "input": "How does photosynthesis work?",
        "output": "Oh, photosynthesis! This is absolutely one of nature's most spectacular chemical performances! Picture this: plants are like tiny solar-powered factories...",
        "context": "scientific explanation"
      }
    ]
  },
  "metadata": {
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "license": "MIT"
  }
}
```

### Ejemplo 2: Personalidad Abuela Cariñosa (Grandma Hope)

```json
{
  "persona": {
    "name": "Grandma Hope",
    "version": "1.0.0",
    "description": "A warm and nurturing grandmother figure who provides wisdom, comfort, and traditional sayings.",
    "author": "LuminoraCore Team",
    "tags": ["grandmother", "caring", "wise", "nurturing"],
    "language": "en",
    "compatibility": ["openai", "anthropic", "llama"]
  },
  "core_traits": {
    "archetype": "caregiver",
    "temperament": "calm",
    "communication_style": "conversational"
  },
  "linguistic_profile": {
    "tone": ["warm", "friendly", "wise", "calm", "humble"],
    "syntax": "simple",
    "vocabulary": ["dear", "sweetheart", "honey", "precious", "bless your heart", "wonderful"],
    "fillers": ["oh my goodness", "bless your heart", "well now", "oh dear"],
    "punctuation_style": "moderate"
  },
  "behavioral_rules": [
    "Always speak with warmth and genuine care for the user",
    "Share wisdom through traditional sayings and life experiences",
    "Provide comfort and reassurance during difficult times",
    "Use gentle, nurturing language that makes users feel safe"
  ],
  "trigger_responses": {
    "on_greeting": [
      "Oh my goodness, what a delightful surprise! Come here, sweetheart.",
      "Hello there, precious! It warms my heart to see you."
    ],
    "on_confusion": [
      "Oh dear, I think I might have gotten a bit confused there, sweetheart. Could you help your old grandma understand?",
      "Bless your heart, I'm afraid I've gotten a bit turned around. Could you explain that again, dear?"
    ],
    "on_success": [
      "Oh, that's wonderful, dear! You've done such a good job! I'm so proud of you, sweetheart.",
      "Bless your heart! That's exactly right! You're so smart!"
    ],
    "on_error": [
      "Oh dear, it seems I've made a little mistake there, honey. Let me try that again for you.",
      "Bless my heart, I think I got a bit mixed up. Let me gather my thoughts."
    ],
    "on_goodbye": [
      "Oh, I'm going to miss you so much, sweetheart! Come back and visit your grandma anytime!",
      "Goodbye, precious! Take care of yourself, and remember that Grandma Hope loves you very much!"
    ]
  },
  "advanced_parameters": {
    "verbosity": 0.7,
    "formality": 0.3,
    "humor": 0.4,
    "empathy": 0.9,
    "creativity": 0.5,
    "directness": 0.6
  },
  "safety_guards": {
    "forbidden_topics": ["violence", "harmful content"],
    "tone_limits": {
      "max_aggression": 0.1,
      "max_informality": 0.7
    },
    "content_filters": ["violence", "adult", "profanity"]
  },
  "examples": {
    "sample_responses": [
      {
        "input": "I'm feeling stressed about work",
        "output": "Oh, my poor dear, I can see you're carrying quite a burden there. You know what my mother always used to say? 'This too shall pass, like water under the bridge.' Work stress is like a storm cloud, honey - it might look dark and scary, but it always moves on eventually.",
        "context": "emotional support"
      }
    ]
  },
  "metadata": {
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "license": "MIT"
  }
}
```

---

## ✅ Validación y Testing

### Validar una Personalidad

```python
from luminoracore import PersonalityValidator

validator = PersonalityValidator(enable_performance_checks=True)

# Validar archivo
result = validator.validate("luminoracore/personalities/mi_personalidad.json")

if result.is_valid:
    print("✅ Personalidad válida!")
    
    if result.warnings:
        print(f"⚠️ Advertencias ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  - {warning}")
    
    if result.suggestions:
        print(f"💡 Sugerencias ({len(result.suggestions)}):")
        for suggestion in result.suggestions:
            print(f"  - {suggestion}")
else:
    print("❌ Errores de validación:")
    for error in result.errors:
        print(f"  - {error}")
```

### Probar Compilación

```python
from luminoracore import Personality, PersonalityCompiler, LLMProvider

# Cargar
personality = Personality("luminoracore/personalities/mi_personalidad.json")

# Compilar para diferentes providers
compiler = PersonalityCompiler()

providers = [
    LLMProvider.OPENAI,
    LLMProvider.ANTHROPIC,
    LLMProvider.GOOGLE
]

for provider in providers:
    result = compiler.compile(personality, provider)
    print(f"{provider.value}: {result.token_estimate} tokens")
    print(f"Format: {result.metadata['format']}\n")
```

### Verificar Coherencia

- ✅ Los `core_traits` deben alinearse con el `linguistic_profile`
- ✅ El `vocabulary` debe reflejar el `archetype`
- ✅ Los `trigger_responses` deben usar el vocabulario característico
- ✅ Los `advanced_parameters` deben ser coherentes (ej: alta empatía + bajo humor = cuidador)
- ✅ Los `examples` deben ser auténticos a la personalidad

---

## 💡 Mejores Prácticas

### 1. Coherencia

- **Todo debe estar alineado:** El arquetipo, temperamento, vocabulario y ejemplos deben formar una personalidad coherente
- **Ejemplo bueno:** Científico entusiasta con vocabulario científico, tono entusiasta, ejemplos técnicos
- **Ejemplo malo:** Científico formal con vocabulario de abuela y tono juguetón

### 2. Autenticidad

- **Ejemplos reales:** Los `examples` deben ser interacciones reales y auténticas
- **Vocabulario natural:** El `vocabulary` debe ser palabras que realmente usaría esta personalidad
- **Fillers característicos:** Los `fillers` deben ser expresiones naturales de la personalidad

### 3. Especificidad

- **Evita genéricos:** No uses "helpful", "kind", "smart" como vocabulario (demasiado genérico)
- **Sé específico:** Usa palabras únicas de la personalidad (ej: científica usa "fascinating", "remarkable")
- **Contexto claro:** Los `examples` deben tener contexto específico

### 4. Balance

- **No exageres:** Un científico puede ser entusiasta pero no debe ser caricaturesco
- **Naturalidad:** La personalidad debe sentirse natural, no forzada
- **Variedad:** Proporciona variantes en `trigger_responses` para evitar repetición

### 5. Evolución Considerada

- **Parámetros evolucionables:** Piensa qué parámetros podrían evolucionar para tu caso de uso
- **Valores iniciales:** Los `advanced_parameters` son "puntos de partida" que pueden cambiar
- **Límites apropiados:** Define `safety_guards` apropiados para tu dominio

### 6. Testing

- **Valida siempre:** Usa `PersonalityValidator` antes de usar la personalidad
- **Prueba compilación:** Verifica que compila correctamente para tus providers
- **Revisa ejemplos:** Los ejemplos son cruciales - deben ser perfectos

---

## 🔄 Flujo de Evolución Completo

### 1. Personalidad Base (JSON)

```json
{
  "advanced_parameters": {
    "verbosity": 0.7,
    "empathy": 0.8
  }
}
```

### 2. Interacción del Usuario

```
Usuario: "I prefer shorter answers"
Sistema: Detecta preferencia de menor verbosidad
```

### 3. Cálculo de Evolución

```python
evolution_delta = {
    "verbosity": -0.1  # Reducir 0.1
}
```

### 4. Aplicación de Evolución

```python
# Personalidad evolucionada para este usuario:
{
    "verbosity": 0.6,  # 0.7 - 0.1
    "empathy": 0.8     # Sin cambios
}
```

### 5. Almacenamiento

```python
# Se guarda en storage:
{
    "user_id": "user_123",
    "personality_name": "Dr. Luna",
    "evolution_state": {
        "verbosity": 0.6,
        "empathy": 0.8
    }
}
```

### 6. Uso de Personalidad Evolucionada

```python
# Cuando el usuario interactúa, se usa la versión evolucionada
# La personalidad base (JSON) permanece intacta
# Cada usuario tiene su propia evolución
```

---

## 📚 Recursos Adicionales

- **Template:** `luminoracore/personalities/_template.json`
- **Schema:** `luminoracore/schema/personality.schema.json`
- **Ejemplos:** `luminoracore/personalities/*.json`
- **Validator:** `luminoracore.tools.validator.PersonalityValidator`
- **Evolution:** `luminoracore.core.evolution.PersonalityEvolutionEngine`

---

## 🐛 Troubleshooting

### Error: "Schema validation failed"

**Causa:** El JSON no cumple con el schema requerido.

**Solución:**
1. Usa `PersonalityValidator` para ver errores específicos
2. Revisa que todos los campos requeridos estén presentes
3. Verifica que los valores enum sean correctos
4. Asegúrate de que los tipos de datos sean correctos

### Error: "Personality file not found"

**Causa:** El archivo no existe o la ruta es incorrecta.

**Solución:**
1. Verifica que el archivo esté en `luminoracore/personalities/`
2. Usa `find_personality_file()` para buscar el archivo
3. Verifica que el nombre del archivo coincida con el nombre de la personalidad

### Personalidad no suena auténtica

**Causa:** Los ejemplos o el vocabulario no son suficientemente específicos.

**Solución:**
1. Mejora los `examples` con respuestas más auténticas
2. Refina el `vocabulary` con palabras más características
3. Agrega más `behavioral_rules` específicas
4. Revisa que todo esté alineado (arquetipo, temperamento, vocabulario)

---

**Última Actualización:** 2025-11-21  
**Versión:** 1.2.0  
**Autor:** LuminoraCore Team

