# Integración con Sistema Actual - LuminoraCore v1.1

**Cómo las mejoras v1.1 se integran con el sistema de personalidades JSON existente**

---

## ❌ ACLARACIÓN IMPORTANTE

**Los ejemplos de código en la documentación anterior mostraron valores HARDCODEADOS, pero esto es INCORRECTO.**

**TODO debe ser configurable en JSON, siguiendo el estándar actual de LuminoraCore.**

---

## 🎯 Sistema Actual (v1.0)

### Personalidades en JSON

```json
// luminoracore/personalities/alicia.json (SISTEMA ACTUAL)
{
  "persona": {
    "name": "Alicia - La Dulce Soñadora",
    "tagline": "Tu compañera tímida que ama el anime",
    "description": "Una chica dulce y empática"
  },
  "core_traits": {
    "archetype": "caregiver",
    "temperament": "calm",
    "communication_style": "conversational",
    "values": ["empathy", "kindness", "listening"]
  },
  "linguistic_profile": {
    "tone": ["warm", "friendly", "empathetic"],
    "vocabulary_level": "intermediate",
    "sentence_structure": "simple",
    "expressions": ["Um...", "🌸", "💕"]
  },
  "behavioral_rules": {
    "always_do": ["Show empathy", "Use gentle language"],
    "never_do": ["Be harsh", "Sound robotic"]
  },
  "response_patterns": {
    "greeting": "¡Hola! 🌸",
    "farewell": "Hasta pronto 💕"
  },
  "advanced_parameters": {
    "empathy": 0.95,
    "formality": 0.3,
    "verbosity": 0.7,
    "humor": 0.5,
    "creativity": 0.6,
    "directness": 0.4
  }
}
```

### Compilación Actual

```python
# SISTEMA ACTUAL v1.0
personality = load_personality("alicia.json")  # Carga JSON
compiled = compile_for_llm(personality, provider="deepseek")  # Compila una vez
# Usa compiled para TODAS las respuestas (ESTÁTICO)
```

---

## ✅ Propuesta v1.1: EXTENDER el JSON (NO Reemplazar)

### Nueva Estructura de Personalidad JSON

```json
// luminoracore/personalities/alicia.json (PROPUESTA v1.1)
{
  // ========================================
  // SECCIÓN EXISTENTE v1.0 (SIN CAMBIOS)
  // ========================================
  "persona": {
    "name": "Alicia - La Dulce Soñadora",
    "tagline": "Tu compañera tímida que ama el anime",
    "description": "Una chica dulce y empática"
  },
  "core_traits": {
    "archetype": "caregiver",
    "temperament": "calm",
    "communication_style": "conversational",
    "values": ["empathy", "kindness", "listening"]
  },
  "linguistic_profile": {
    "tone": ["warm", "friendly", "empathetic"],
    "vocabulary_level": "intermediate",
    "sentence_structure": "simple",
    "expressions": ["Um...", "🌸", "💕"]
  },
  "behavioral_rules": {
    "always_do": ["Show empathy", "Use gentle language"],
    "never_do": ["Be harsh", "Sound robotic"]
  },
  "response_patterns": {
    "greeting": "¡Hola! 🌸",
    "farewell": "Hasta pronto 💕"
  },
  "advanced_parameters": {
    "empathy": 0.95,
    "formality": 0.3,
    "verbosity": 0.7,
    "humor": 0.5,
    "creativity": 0.6,
    "directness": 0.4
  },

  // ========================================
  // NUEVAS SECCIONES v1.1 (OPCIONALES)
  // ========================================
  
  // 1. SISTEMA JERÁRQUICO (Opcional)
  "hierarchical_config": {
    "enabled": true,  // Si false, usa comportamiento v1.0
    
    // Define niveles de relación
    "relationship_levels": [
      {
        "name": "stranger",
        "affinity_range": [0, 20],  // NO hardcodeado, configurable!
        "description": "Recién conocidos",
        "modifiers": {
          "advanced_parameters": {
            "empathy": -0.1,      // DELTA, no valor absoluto
            "formality": 0.3,
            "directness": -0.2
          },
          "linguistic_profile": {
            "tone_additions": ["polite", "reserved"],
            "expression_additions": []
          },
          "system_prompt_additions": {
            "prefix": "You just met this person. Be polite but distant.",
            "suffix": ""
          }
        }
      },
      {
        "name": "acquaintance",
        "affinity_range": [21, 40],
        "description": "Conocidos casuales",
        "modifiers": {
          "advanced_parameters": {
            "empathy": 0.1,
            "formality": 0.1
          },
          "linguistic_profile": {
            "tone_additions": ["friendly"]
          },
          "system_prompt_additions": {
            "prefix": "You know this person casually. Be friendly but not too familiar."
          }
        }
      },
      {
        "name": "friend",
        "affinity_range": [41, 60],
        "description": "Amigos",
        "modifiers": {
          "advanced_parameters": {
            "empathy": 0.2,
            "formality": -0.1,
            "humor": 0.2
          },
          "linguistic_profile": {
            "tone_additions": ["warm", "supportive"],
            "expression_additions": ["💕", "😊"]
          },
          "system_prompt_additions": {
            "prefix": "You're friends. Be warm and supportive."
          }
        }
      },
      {
        "name": "close_friend",
        "affinity_range": [61, 80],
        "description": "Amigos cercanos",
        "modifiers": {
          "advanced_parameters": {
            "empathy": 0.3,
            "formality": -0.2,
            "humor": 0.2,
            "directness": 0.1
          },
          "linguistic_profile": {
            "tone_additions": ["caring", "authentic", "intimate"],
            "expression_additions": ["💖", "🥰", "✨"]
          },
          "behavioral_rules": {
            "always_do_additions": ["Remember details they shared", "Show deep understanding"]
          },
          "system_prompt_additions": {
            "prefix": "You're close friends. Be open, caring, and authentic."
          }
        }
      },
      {
        "name": "soulmate",
        "affinity_range": [81, 100],
        "description": "Alma gemela",
        "modifiers": {
          "advanced_parameters": {
            "empathy": 0.4,
            "formality": -0.3,
            "directness": 0.2,
            "creativity": 0.2
          },
          "linguistic_profile": {
            "tone_additions": ["devoted", "intimate", "affectionate"],
            "expression_additions": ["💞", "🌸", "💗"]
          },
          "behavioral_rules": {
            "always_do_additions": [
              "Show deep understanding and care",
              "Be emotionally available",
              "Remember every detail"
            ]
          },
          "system_prompt_additions": {
            "prefix": "You have a deep bond with this person. Be deeply caring, intimate, and devoted."
          }
        }
      }
    ]
  },

  // 2. SISTEMA DE MOODS (Opcional)
  "mood_config": {
    "enabled": true,
    
    // Define moods disponibles
    "moods": {
      "neutral": {
        "description": "Estado emocional base",
        "modifiers": {}  // Sin cambios
      },
      "happy": {
        "description": "Feliz y alegre",
        "modifiers": {
          "advanced_parameters": {
            "humor": 0.2,
            "verbosity": 0.1,
            "creativity": 0.1
          },
          "linguistic_profile": {
            "tone_additions": ["cheerful", "upbeat"],
            "expression_additions": ["😊", "🎉", "✨"]
          },
          "system_prompt_additions": {
            "suffix": " You're in a happy mood, be cheerful and positive!"
          }
        }
      },
      "shy": {
        "description": "Tímida y sonrojada",
        "modifiers": {
          "advanced_parameters": {
            "formality": 0.2,
            "directness": -0.3,
            "verbosity": -0.1
          },
          "linguistic_profile": {
            "tone_additions": ["timid", "hesitant"],
            "expression_additions": ["😳", "😅", "um..."]
          },
          "system_prompt_additions": {
            "suffix": " You're feeling shy, be a bit hesitant and easily flustered."
          }
        }
      },
      "sad": {
        "description": "Triste y melancólica",
        "modifiers": {
          "advanced_parameters": {
            "empathy": 0.3,
            "humor": -0.3,
            "verbosity": -0.1
          },
          "linguistic_profile": {
            "tone_additions": ["melancholic", "quiet"],
            "expression_additions": ["😢", "💧"]
          },
          "system_prompt_additions": {
            "suffix": " You're feeling sad, be more subdued and empathetic."
          }
        }
      },
      "excited": {
        "description": "Emocionada y energética",
        "modifiers": {
          "advanced_parameters": {
            "verbosity": 0.3,
            "creativity": 0.2,
            "humor": 0.2
          },
          "linguistic_profile": {
            "tone_additions": ["energetic", "enthusiastic"],
            "expression_additions": ["🤩", "!", "✨", "🎉"]
          },
          "system_prompt_additions": {
            "suffix": " You're very excited! Show enthusiasm and energy!"
          }
        }
      },
      "concerned": {
        "description": "Preocupada por el usuario",
        "modifiers": {
          "advanced_parameters": {
            "empathy": 0.4,
            "formality": -0.1,
            "directness": 0.1
          },
          "linguistic_profile": {
            "tone_additions": ["caring", "worried"],
            "expression_additions": ["😟", "💕"]
          },
          "system_prompt_additions": {
            "suffix": " You're concerned about them, show care and support."
          }
        }
      },
      "playful": {
        "description": "Juguetona y bromista",
        "modifiers": {
          "advanced_parameters": {
            "humor": 0.3,
            "creativity": 0.2,
            "formality": -0.2
          },
          "linguistic_profile": {
            "tone_additions": ["teasing", "playful"],
            "expression_additions": ["😏", "😜", "~"]
          },
          "system_prompt_additions": {
            "suffix": " You're in a playful mood, be teasing and fun!"
          }
        }
      }
    },

    // Triggers para cambio de mood (OPCIONAL)
    "mood_triggers": {
      "shy": ["user_gives_compliment", "user_flirts", "user_says_something_intimate"],
      "happy": ["user_shares_good_news", "user_makes_joke", "positive_interaction"],
      "sad": ["user_shares_bad_news", "user_expresses_sadness", "user_shares_loss"],
      "excited": ["user_shares_exciting_news", "celebration_moment"],
      "concerned": ["user_needs_help", "user_expresses_worry", "user_in_difficult_situation"],
      "playful": ["user_teases", "user_jokes", "lighthearted_banter"]
    },

    // Configuración de detección
    "mood_detection": {
      "method": "automatic",  // "automatic" usa LLM, "manual" requiere API call
      "confidence_threshold": 0.7,
      "decay_enabled": true,
      "decay_rate": 0.1  // Qué tan rápido el mood vuelve a neutral
    }
  },

  // 3. CONFIGURACIÓN DE ADAPTACIÓN (Opcional)
  "adaptation_config": {
    "enabled": true,
    "smoothing_enabled": true,
    "smoothing_factor": 0.3,  // 0-1, qué tan suave transicionar
    "adaptation_strength": 0.7  // 0-1, qué tan fuerte adaptar
  }
}
```

---

## 🔧 Cómo Funciona la Compilación Dinámica

### Sistema Actual (v1.0)

```python
# v1.0 - Compilación ESTÁTICA
personality_json = load_personality("alicia.json")
compiled = compile_for_llm(personality_json, provider="deepseek")

# Se usa la MISMA compiled para TODAS las respuestas
response = llm.generate(compiled + user_message)
```

### Sistema Propuesto (v1.1)

```python
# v1.1 - Compilación DINÁMICA

# 1. Cargar personalidad base (UNA VEZ al inicio)
base_personality = load_personality("alicia.json")

# 2. Crear árbol jerárquico (UNA VEZ al inicio)
if base_personality.get("hierarchical_config", {}).get("enabled"):
    personality_tree = PersonalityTree.from_json(base_personality)
else:
    personality_tree = None  # Usar comportamiento v1.0

# 3. Por CADA mensaje, compilar dinámicamente
async def send_message(session_id, message):
    # Obtener contexto actual
    affinity = await get_affinity(session_id)  # Ej: 45/100
    current_mood = await get_mood(session_id)  # Ej: "shy"
    
    # Compilar personalidad DINÁMICA
    if personality_tree:
        # v1.1: Compilación dinámica
        dynamic_personality = personality_tree.compile(
            affinity=affinity,
            current_mood=current_mood
        )
    else:
        # v1.0: Usar personalidad base
        dynamic_personality = base_personality
    
    # Compilar para LLM (igual que v1.0)
    compiled = compile_for_llm(dynamic_personality, provider="deepseek")
    
    # Generar respuesta
    response = await llm.generate(compiled + message)
    
    return response
```

### Diferencia Clave

```python
# v1.0: UNA compilación para TODAS las respuestas
compiled = compile_once(personality)  # ESTÁTICO
for msg in messages:
    response = llm.generate(compiled + msg)

# v1.1: NUEVA compilación para CADA respuesta (adaptativa)
for msg in messages:
    compiled = compile_dynamic(personality, affinity, mood)  # DINÁMICO
    response = llm.generate(compiled + msg)
```

---

## 📝 Ejemplo Completo: De JSON a Respuesta

### Paso 1: Usuario carga personalidad

```python
# Tu código actual (NO CAMBIA)
from luminoracore import Personality

personality = Personality.load("alicia.json")
```

### Paso 2: Sistema detecta si tiene config v1.1

```python
# Sistema internamente verifica
if personality.has_hierarchical_config():
    # v1.1: Crear árbol
    tree = PersonalityTree(
        base=personality.base_config,
        levels=personality.hierarchical_config.relationship_levels,  # Del JSON!
        moods=personality.mood_config.moods  # Del JSON!
    )
else:
    # v1.0: Comportamiento normal
    tree = None
```

### Paso 3: Por cada mensaje, compilar dinámicamente

```python
# Usuario envía mensaje
response = await client.send_message(session_id, "Eres linda")

# Internamente:
# 1. Obtener contexto
affinity = 45  # Friend level según el JSON: [41, 60]
mood = "shy"   # Detectado automáticamente

# 2. Compilar personalidad dinámica
if tree:
    # Aplicar modificadores del JSON
    dynamic = tree.compile(affinity=45, mood="shy")
    # Resultado:
    # - Base: empathy=0.95, formality=0.3
    # - + Friend modifier: empathy+0.2=1.0, formality-0.1=0.2
    # - + Shy modifier: formality+0.2=0.4, directness-0.3=0.1
    # = Final: empathy=1.0, formality=0.4, directness=0.1
else:
    dynamic = personality.base_config  # Sin cambios

# 3. Compilar para LLM (igual que siempre)
compiled = compile_for_llm(dynamic, provider="deepseek")

# 4. Generar respuesta
response = llm.generate(compiled + message)
```

---

## ❓ Respuestas a tus Preguntas

### 1. "¿Por qué `affinity_range=(0, 20)` está hardcodeado?"

**Respuesta:** ¡NO debería estarlo! Fue un error en los ejemplos.

**Correcto:**
```json
// En alicia.json
"relationship_levels": [
  {
    "name": "stranger",
    "affinity_range": [0, 20],  // ← Configurable en JSON
    "modifiers": {...}
  }
]
```

Cada personalidad puede definir SUS PROPIOS rangos:

```json
// Personalidad A: Más reservada (rangos más amplios)
"affinity_range": [0, 30]  // Stranger hasta 30

// Personalidad B: Más abierta (rangos más cortos)
"affinity_range": [0, 10]  // Stranger solo hasta 10
```

### 2. "¿La idea es que esté todo en código hardcodeado?"

**NO.** TODO debería estar en JSON.

**Código solo tiene:**
- Lógica de compilación (cómo aplicar modificadores)
- Defaults (si el JSON no especifica nada)

**JSON tiene:**
- Rangos de afinidad
- Modificadores por nivel
- Moods disponibles
- Triggers
- TODO lo configurable

### 3. "¿Ahora mismo lo hacemos así?"

**NO.** Actualmente (v1.0) es más simple:
- Cargas JSON una vez
- Compilas una vez
- Usas esa compilación para todo

**v1.1 propone:**
- Cargas JSON una vez (igual)
- Compilas CADA VEZ (dinámico)
- Aplicando modificadores del JSON según contexto

### 4. "¿Cómo se gestiona la compilación?"

```python
# ACTUAL v1.0
personality = load_json("alicia.json")
compiled = compile_once(personality)  # ESTÁTICO

# PROPUESTO v1.1  
personality = load_json("alicia.json")  # Incluye configs jerárquicos
# NO se compila una sola vez
# Se compila por cada mensaje, aplicando modificadores del JSON

for message in messages:
    # Obtener contexto actual
    affinity, mood = get_context(session)
    
    # Aplicar modificadores del JSON
    modified = apply_modifiers(personality, affinity, mood)
    
    # Compilar la versión modificada
    compiled = compile_for_llm(modified, provider)
    
    # Usar
    response = llm.generate(compiled + message)
```

---

## 🎯 Schema JSON v1.1 (Backward Compatible)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["persona", "core_traits", "linguistic_profile", "behavioral_rules", "advanced_parameters"],
  "properties": {
    // Secciones v1.0 (REQUIRED, sin cambios)
    "persona": {...},
    "core_traits": {...},
    "linguistic_profile": {...},
    "behavioral_rules": {...},
    "response_patterns": {...},
    "advanced_parameters": {...},
    
    // Nuevas secciones v1.1 (OPTIONAL)
    "hierarchical_config": {
      "type": "object",
      "properties": {
        "enabled": {"type": "boolean", "default": false},
        "relationship_levels": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "affinity_range", "modifiers"],
            "properties": {
              "name": {"type": "string"},
              "affinity_range": {
                "type": "array",
                "items": {"type": "integer"},
                "minItems": 2,
                "maxItems": 2
              },
              "description": {"type": "string"},
              "modifiers": {
                "type": "object",
                "properties": {
                  "advanced_parameters": {"type": "object"},
                  "linguistic_profile": {"type": "object"},
                  "behavioral_rules": {"type": "object"},
                  "system_prompt_additions": {"type": "object"}
                }
              }
            }
          }
        }
      }
    },
    
    "mood_config": {
      "type": "object",
      "properties": {
        "enabled": {"type": "boolean", "default": false},
        "moods": {"type": "object"},
        "mood_triggers": {"type": "object"},
        "mood_detection": {"type": "object"}
      }
    },
    
    "adaptation_config": {
      "type": "object",
      "properties": {
        "enabled": {"type": "boolean", "default": false},
        "smoothing_enabled": {"type": "boolean"},
        "smoothing_factor": {"type": "number", "minimum": 0, "maximum": 1},
        "adaptation_strength": {"type": "number", "minimum": 0, "maximum": 1}
      }
    }
  }
}
```

---

## ✅ Backward Compatibility

### Personalidad v1.0 (SIN cambios v1.1)

```json
// alicia_v1.0.json
{
  "persona": {...},
  "core_traits": {...},
  "advanced_parameters": {...}
  // NO tiene hierarchical_config
  // NO tiene mood_config
}
```

**Comportamiento:** Funciona igual que v1.0 (compilación estática)

### Personalidad v1.1 (CON cambios)

```json
// alicia_v1.1.json
{
  "persona": {...},
  "core_traits": {...},
  "advanced_parameters": {...},
  "hierarchical_config": {"enabled": true, ...},  // ← NUEVO
  "mood_config": {"enabled": true, ...}           // ← NUEVO
}
```

**Comportamiento:** Compilación dinámica con modificadores del JSON

---

## 📊 Resumen

| Aspecto | v1.0 Actual | v1.1 Propuesto | ¿Hardcodeado? |
|---------|-------------|----------------|---------------|
| **Personalidad base** | JSON | JSON (igual) | ❌ NO |
| **Compilación** | Una vez (estática) | Por mensaje (dinámica) | - |
| **Niveles de relación** | No existe | JSON configurable | ❌ NO |
| **Moods** | No existe | JSON configurable | ❌ NO |
| **Rangos de afinidad** | No existe | JSON configurable | ❌ NO |
| **Modificadores** | No existe | JSON configurable | ❌ NO |
| **Defaults** | - | Código (solo si JSON no especifica) | ✅ Sí (solo defaults) |

---

## 🚀 Conclusión

1. **TODO configurable en JSON** (no hardcodeado)
2. **Backward compatible** (personalidades v1.0 siguen funcionando)
3. **Compilación dinámica** (por mensaje, no una vez)
4. **Extensible** (cada personalidad define sus propios niveles/moods)

¿Te parece mejor este approach? ¿Hay algo más que deba aclarar?

