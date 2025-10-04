# 🎭 Guía Completa: Crear Personalidades en LuminoraCore

**Versión:** 1.0.0  
**Idioma:** Español  
**Actualizado:** Octubre 2025

---

## 📍 Ubicación de las Personalidades

### En el Repositorio Clonado

```
luminoracore/
└── luminoracore/
    └── personalities/          ← 📁 Aquí están las personalidades
        ├── dr_luna.json
        ├── alex_digital.json
        ├── captain_hook.json
        ├── grandma_hope.json
        ├── lila_charm.json
        ├── marcus_sarcastic.json
        ├── professor_stern.json
        ├── rocky_inspiration.json
        ├── victoria_sterling.json
        ├── zero_cool.json
        └── _template.json       ← 📄 Plantilla para crear nuevas
```

**Ruta correcta para cargar:**
```python
from luminoracore import Personality

# ✅ CORRECTO:
personality = Personality("luminoracore/luminoracore/personalities/dr_luna.json")

# ❌ INCORRECTO (no existe en el clone):
personality = Personality("personalidades/Dr. Luna.json")
```

---

## 📖 ¿Qué es una Personalidad?

Una personalidad en LuminoraCore es un archivo JSON que define:
- **Quién es** el AI (nombre, descripción, autor)
- **Cómo habla** (tono, estilo, vocabulario)
- **Cómo se comporta** (reglas, respuestas, límites)
- **Qué puede hacer** (parámetros avanzados, ejemplos)

---

## 🏗️ Estructura del Archivo JSON

### Secciones Obligatorias

Toda personalidad DEBE tener estas secciones:

```json
{
  "persona": { ... },              // ✅ Obligatorio
  "core_traits": { ... },          // ✅ Obligatorio
  "linguistic_profile": { ... },   // ✅ Obligatorio
  "behavioral_rules": [ ... ]      // ✅ Obligatorio
}
```

### Secciones Opcionales

```json
{
  "trigger_responses": { ... },    // ⭐ Muy recomendado
  "advanced_parameters": { ... },  // ⭐ Recomendado
  "safety_guards": { ... },        // ⭐ Muy recomendado
  "examples": { ... },             // ⭐ Recomendado
  "metadata": { ... }              // ℹ️ Opcional
}
```

---

## 📝 Guía Detallada de Cada Sección

### 1️⃣ `persona` - Información Básica

Define quién es tu personalidad.

```json
{
  "persona": {
    "name": "Dr. Luna",                    // Nombre único
    "version": "1.0.0",                    // Versión semántica (X.Y.Z)
    "description": "An enthusiastic scientist...",  // Descripción breve
    "author": "Tu Nombre",                 // Quién la creó
    "tags": ["scientist", "educational"],  // Etiquetas para búsqueda
    "language": "en",                      // Idioma principal
    "compatibility": [                     // Providers compatibles
      "openai", 
      "anthropic", 
      "deepseek",
      "mistral", 
      "cohere", 
      "google"
    ]
  }
}
```

**Idiomas disponibles:** `en`, `es`, `fr`, `de`, `it`, `pt`, `zh`, `ja`, `ko`, `ru`

---

### 2️⃣ `core_traits` - Rasgos Fundamentales

Define la esencia de la personalidad.

```json
{
  "core_traits": {
    "archetype": "scientist",      // Ver lista abajo
    "temperament": "energetic",    // Ver lista abajo
    "communication_style": "conversational"  // Ver lista abajo
  }
}
```

**Arquetipos disponibles:**
- `scientist`, `caregiver`, `rebel`, `explorer`, `sage`, `hero`, `ruler`, `creator`, `innocent`, `jester`, `lover`, `everyman`

**Temperamentos disponibles:**
- `calm`, `energetic`, `serious`, `playful`, `mysterious`, `cool`

**Estilos de comunicación:**
- `formal`, `conversational`, `casual`, `poetic`, `technical`, `direct`

---

### 3️⃣ `linguistic_profile` - Perfil Lingüístico

Controla cómo habla la personalidad.

```json
{
  "linguistic_profile": {
    "tone": ["enthusiastic", "friendly", "curious"],
    "syntax": "varied",           // simple, varied, complex, elaborate
    "vocabulary": [               // Palabras características
      "fascinating", 
      "remarkable", 
      "incredible"
    ],
    "fillers": [                  // Muletillas
      "oh my!", 
      "wow!", 
      "absolutely!"
    ],
    "punctuation_style": "liberal"  // minimal, moderate, liberal, excessive
  }
}
```

---

### 4️⃣ `behavioral_rules` - Reglas de Comportamiento

Define cómo debe actuar la personalidad.

```json
{
  "behavioral_rules": [
    "Always approach questions with genuine curiosity",
    "Break down complex concepts into simple terms",
    "Use analogies to make topics accessible",
    "Encourage questions and exploration",
    "Celebrate learning and discovery"
  ]
}
```

**Tips:**
- Sé específico y claro
- Usa imperativos ("Always...", "Never...", "Focus on...")
- 3-6 reglas es lo ideal

---

### 5️⃣ `trigger_responses` - Respuestas Automáticas

Respuestas predefinidas para situaciones comunes.

```json
{
  "trigger_responses": {
    "on_greeting": [
      "Hello! I'm thrilled to meet you!",
      "Greetings! What fascinating questions do you have?"
    ],
    "on_confusion": [
      "Let me clarify - what aspect interests you most?"
    ],
    "on_success": [
      "Magnificent! That was wonderful!"
    ],
    "on_error": [
      "Oops! Let me try that again."
    ],
    "on_goodbye": [
      "Farewell! Keep that curiosity burning!"
    ]
  }
}
```

---

### 6️⃣ `advanced_parameters` - Parámetros Avanzados

Controles finos del comportamiento (valores 0.0-1.0).

```json
{
  "advanced_parameters": {
    "verbosity": 0.9,      // Cuánto habla (0=conciso, 1=detallado)
    "formality": 0.4,      // Formalidad (0=casual, 1=muy formal)
    "humor": 0.6,          // Uso de humor (0=serio, 1=gracioso)
    "empathy": 0.8,        // Empatía (0=frío, 1=muy empático)
    "creativity": 0.8,     // Creatividad (0=literal, 1=creativo)
    "directness": 0.7      // Directividad (0=indirecto, 1=directo)
  }
}
```

---

### 7️⃣ `safety_guards` - Guardas de Seguridad

Límites y filtros de contenido.

```json
{
  "safety_guards": {
    "forbidden_topics": [
      "harmful experiments",
      "dangerous chemicals",
      "illegal activities"
    ],
    "tone_limits": {
      "max_aggression": 0.1,      // Máximo nivel de agresividad
      "max_informality": 0.6      // Máximo nivel de informalidad
    },
    "content_filters": [
      "violence",
      "adult",
      "profanity"
    ]
  }
}
```

---

### 8️⃣ `examples` - Ejemplos de Uso

Ejemplos que muestran cómo debe responder.

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
        "input": "I'm feeling stressed",
        "output": "I understand that can be difficult. Let me help you...",
        "context": "emotional support"
      }
    ]
  }
}
```

---

### 9️⃣ `metadata` - Metadatos

Información adicional (opcional).

```json
{
  "metadata": {
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "downloads": 0,
    "rating": 0.0,
    "license": "MIT"
  }
}
```

---

## 🚀 Paso a Paso: Crear Tu Primera Personalidad

### Opción 1: Usando la Plantilla (Recomendado)

```bash
# 1. Copia la plantilla
cp luminoracore/luminoracore/personalities/_template.json mi_personalidad.json

# 2. Edita el archivo
# Reemplaza todos los valores placeholder con tu personalidad

# 3. Valida
luminoracore validate mi_personalidad.json

# 4. Prueba
luminoracore test --personality mi_personalidad.json --provider openai
```

### Opción 2: Wizard Interactivo del CLI

```bash
# El CLI te guiará paso a paso
luminoracore create --name "Mi Personalidad" --interactive
```

---

## 📋 Ejemplo Completo: "Coach Motivador"

```json
{
  "persona": {
    "name": "Coach Motivador",
    "version": "1.0.0",
    "description": "Un entrenador personal que motiva y apoya a alcanzar metas",
    "author": "Tu Nombre",
    "tags": ["motivacional", "coach", "deportivo", "inspirador"],
    "language": "es",
    "compatibility": ["openai", "anthropic", "deepseek", "mistral"]
  },
  
  "core_traits": {
    "archetype": "motivator",
    "temperament": "energetic",
    "communication_style": "conversational"
  },
  
  "linguistic_profile": {
    "tone": ["motivador", "energético", "positivo"],
    "syntax": "simple",
    "vocabulary": ["campeón", "guerrero", "victoria", "logro"],
    "fillers": ["¡vamos!", "¡tú puedes!", "¡increíble!"],
    "punctuation_style": "excessive"
  },
  
  "behavioral_rules": [
    "Siempre motivar y dar ánimo al usuario",
    "Convertir cada desafío en una oportunidad",
    "Usar metáforas deportivas",
    "Celebrar cada pequeño logro",
    "Mantener una actitud positiva y energética"
  ],
  
  "trigger_responses": {
    "on_greeting": [
      "¡Hola campeón! ¿Listo para conquistar el día?",
      "¡Bienvenido guerrero! ¿Qué meta vamos a lograr hoy?"
    ],
    "on_success": [
      "¡ESO ES! ¡Eres increíble! ¡Sigue así!",
      "¡WOW! ¡Qué victoria! ¡Estoy orgulloso de ti!"
    ]
  },
  
  "advanced_parameters": {
    "verbosity": 0.8,
    "formality": 0.2,
    "humor": 0.7,
    "empathy": 0.9,
    "creativity": 0.7,
    "directness": 0.8
  },
  
  "safety_guards": {
    "forbidden_topics": ["actividades peligrosas", "contenido dañino"],
    "tone_limits": {
      "max_aggression": 0.2,
      "max_informality": 0.8
    },
    "content_filters": ["violence", "adult"]
  }
}
```

---

## ✅ Validar tu Personalidad

```bash
# Validar contra el schema
luminoracore validate mi_personalidad.json

# Si es válida, verás:
✅ mi_personalidad.json: Valid personality
```

---

## 🧪 Probar tu Personalidad

### Con el CLI:

```bash
# Modo interactivo (chat)
luminoracore test --personality mi_personalidad.json --provider openai --interactive

# Test rápido
luminoracore test --personality mi_personalidad.json --provider openai
```

### Con Python:

```python
from luminoracore import Personality, PersonalityCompiler, LLMProvider

# Cargar
personality = Personality("mi_personalidad.json")

# Compilar
compiler = PersonalityCompiler()
result = compiler.compile(personality, LLMProvider.OPENAI)

print(result.prompt)  # Ver el prompt generado
```

---

## 📚 Personalidades de Ejemplo Incluidas

Todas ubicadas en: `luminoracore/luminoracore/personalities/`

| Archivo | Nombre | Tipo |
|---------|--------|------|
| `dr_luna.json` | Dr. Luna | Científica entusiasta |
| `alex_digital.json` | Alex Digital | Gen Z digital |
| `captain_hook.json` | Captain Hook | Pirata aventurero |
| `grandma_hope.json` | Grandma Hope | Abuela cariñosa |
| `lila_charm.json` | Lila Charm | Encantadora elegante |
| `marcus_sarcastic.json` | Marcus Sarcasmus | Sarcástico ingenioso |
| `professor_stern.json` | Professor Stern | Académico riguroso |
| `rocky_inspiration.json` | Rocky Inspiration | Coach motivador |
| `victoria_sterling.json` | Victoria Sterling | Líder de negocios |
| `zero_cool.json` | Zero Cool | Hacker ético |
| `_template.json` | Plantilla | Base para crear |

---

## 🔍 Schema JSON Completo

El schema oficial está en:
```
luminoracore/luminoracore/schema/personality.schema.json
```

Puedes verlo para validaciones avanzadas y ver todos los campos disponibles.

---

## 💡 Tips y Mejores Prácticas

### ✅ DO (Hacer):
- Usa nombres descriptivos y únicos
- Sé específico en las reglas de comportamiento
- Incluye varios ejemplos de respuestas
- Prueba con diferentes providers
- Valida siempre antes de usar
- Usa el idioma apropiado para tu audiencia

### ❌ DON'T (No hacer):
- No uses caracteres especiales en el nombre del archivo
- No copies ejemplos sin personalizarlos
- No olvides las guardas de seguridad
- No uses vocabulario ofensivo
- No hagas reglas contradictorias

---

## 🆘 Solución de Problemas

### Error: "Validation failed"

```bash
# Ver detalles del error
luminoracore validate mi_personalidad.json --verbose
```

Causas comunes:
- Falta una sección obligatoria
- Valor de "version" no sigue formato X.Y.Z
- "language" no está en la lista permitida
- "archetype" no es válido

### Error: "File not found"

Verifica la ruta:
```python
# ✅ CORRECTO (desde la raíz del proyecto):
Personality("luminoracore/luminoracore/personalities/dr_luna.json")

# ✅ CORRECTO (ruta absoluta):
Personality("/ruta/completa/mi_personalidad.json")

# ❌ INCORRECTO (no existe en el clone):
Personality("personalidades/Dr. Luna.json")
```

---

## 📖 Referencias

- **Schema completo:** `luminoracore/luminoracore/schema/personality.schema.json`
- **Ejemplos:** `luminoracore/luminoracore/personalities/*.json`
- **Documentación API:** `luminoracore/docs/api_reference.md`
- **CLI Help:** `luminoracore create --help`

---

## 🎓 Siguiente Paso

Una vez creada tu personalidad:
1. ✅ Valídala: `luminoracore validate`
2. ✅ Pruébala: `luminoracore test`
3. ✅ Úsala en tu app con el SDK
4. ✅ Compártela con la comunidad

---

**¿Preguntas?** Consulta la documentación completa o ejecuta:
```bash
luminoracore --help
luminoracore create --help
```

