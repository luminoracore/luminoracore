# Integration with Current System - LuminoraCore v1.1

**How v1.1 improvements integrate with the existing JSON personality system**

---

## ❌ IMPORTANT CLARIFICATION

**Code examples in previous documentation showed HARDCODED values, but this is INCORRECT.**

**EVERYTHING should be configurable in JSON, following LuminoraCore's current standard.**

---

## 🎯 Current System (v1.0)

### Personalities in JSON

```json
// luminoracore/personalities/alicia.json (CURRENT SYSTEM)
{
  "persona": {
    "name": "Alicia - The Sweet Dreamer",
    "tagline": "Your shy companion who loves anime",
    "description": "A sweet and empathetic girl"
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
    "greeting": "Hello! 🌸",
    "farewell": "See you soon 💕"
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

### Current Compilation

```python
# CURRENT SYSTEM v1.0
personality = load_personality("alicia.json")  # Load JSON
compiled = compile_for_llm(personality, provider="deepseek")  # Compile once
# Use compiled for ALL responses (STATIC)
```

---

## ✅ Proposal v1.1: EXTEND the JSON (NOT Replace)

### New JSON Personality Structure

```json
// luminoracore/personalities/alicia.json (PROPOSED v1.1)
{
  // ========================================
  // EXISTING v1.0 SECTION (NO CHANGES)
  // ========================================
  "persona": {...},
  "core_traits": {...},
  "linguistic_profile": {...},
  "behavioral_rules": {...},
  "response_patterns": {...},
  "advanced_parameters": {...},

  // ========================================
  // NEW v1.1 SECTIONS (OPTIONAL)
  // ========================================
  
  // 1. HIERARCHICAL SYSTEM (Optional)
  "hierarchical_config": {
    "enabled": true,  // If false, uses v1.0 behavior
    
    // Define relationship levels
    "relationship_levels": [
      {
        "name": "stranger",
        "affinity_range": [0, 20],  // NOT hardcoded, configurable!
        "description": "Just met",
        "modifiers": {
          "advanced_parameters": {
            "empathy": -0.1,      // DELTA, not absolute value
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
        "name": "friend",
        "affinity_range": [41, 60],
        "description": "Friends",
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
      }
      // ... more levels
    ]
  },

  // 2. MOOD SYSTEM (Optional)
  "mood_config": {
    "enabled": true,
    
    // Define available moods
    "moods": {
      "neutral": {
        "description": "Base emotional state",
        "modifiers": {}  // No changes
      },
      "happy": {
        "description": "Happy and cheerful",
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
        "description": "Shy and blushing",
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
      }
    },

    // Triggers for mood change (OPTIONAL)
    "mood_triggers": {
      "shy": ["user_gives_compliment", "user_flirts", "user_says_something_intimate"],
      "happy": ["user_shares_good_news", "user_makes_joke", "positive_interaction"]
    },

    // Detection configuration
    "mood_detection": {
      "method": "automatic",  // "automatic" uses LLM, "manual" requires API call
      "confidence_threshold": 0.7,
      "decay_enabled": true,
      "decay_rate": 0.1  // How fast mood returns to neutral
    }
  },

  // 3. ADAPTATION CONFIGURATION (Optional)
  "adaptation_config": {
    "enabled": true,
    "smoothing_enabled": true,
    "smoothing_factor": 0.3,  // 0-1, how gradual the transition
    "adaptation_strength": 0.7  // 0-1, how strongly to adapt
  }
}
```

---

## 🔧 How Dynamic Compilation Works

### Current System (v1.0)

```python
# v1.0 - STATIC compilation
personality_json = load_personality("alicia.json")
compiled = compile_for_llm(personality_json, provider="deepseek")

# Same compiled used for ALL responses
response = llm.generate(compiled + user_message)
```

### Proposed System (v1.1)

```python
# v1.1 - DYNAMIC compilation

# 1. Load base personality (ONCE at startup)
base_personality = load_personality("alicia.json")

# 2. Create hierarchical tree (ONCE at startup)
if base_personality.get("hierarchical_config", {}).get("enabled"):
    personality_tree = PersonalityTree.from_json(base_personality)
else:
    personality_tree = None  # Use v1.0 behavior

# 3. For EACH message, compile dynamically
async def send_message(session_id, message):
    # Get current context
    affinity = await get_affinity(session_id)  # Ex: 45/100
    current_mood = await get_mood(session_id)  # Ex: "shy"
    
    # Compile DYNAMIC personality
    if personality_tree:
        # v1.1: Dynamic compilation
        dynamic_personality = personality_tree.compile(
            affinity=affinity,
            current_mood=current_mood
        )
    else:
        # v1.0: Use base personality
        dynamic_personality = base_personality
    
    # Compile for LLM (same as v1.0)
    compiled = compile_for_llm(dynamic_personality, provider="deepseek")
    
    # Generate response
    response = await llm.generate(compiled + message)
    
    return response
```

### Key Difference

```python
# v1.0: ONE compilation for ALL responses
compiled = compile_once(personality)  # STATIC
for msg in messages:
    response = llm.generate(compiled + msg)

# v1.1: NEW compilation for EACH response (adaptive)
for msg in messages:
    compiled = compile_dynamic(personality, affinity, mood)  # DYNAMIC
    response = llm.generate(compiled + msg)
```

---

## ❓ Answers to Your Questions

### 1. "Why is `affinity_range=(0, 20)` hardcoded?"

**Answer:** It shouldn't be! It was an error in the examples.

**Correct:**
```json
// In alicia.json
"relationship_levels": [
  {
    "name": "stranger",
    "affinity_range": [0, 20],  // ← Configurable in JSON
    "modifiers": {...}
  }
]
```

Each personality can define ITS OWN ranges:

```json
// Personality A: More reserved (wider ranges)
"affinity_range": [0, 30]  // Stranger until 30

// Personality B: More open (shorter ranges)
"affinity_range": [0, 10]  // Stranger only until 10
```

### 2. "Is the idea to have everything hardcoded?"

**NO.** EVERYTHING should be in JSON.

**Code only has:**
- Compilation logic (how to apply modifiers)
- Defaults (if JSON doesn't specify anything)

**JSON has:**
- Affinity ranges
- Modifiers per level
- Available moods
- Triggers
- EVERYTHING configurable

### 3. "Do we currently do it this way?"

**NO.** Currently (v1.0) is simpler:
- Load JSON once
- Compile once
- Use that compilation for everything

**v1.1 proposes:**
- Load JSON once (same)
- Compile EACH TIME (dynamic)
- Applying JSON modifiers based on context

---

## 🎯 JSON Schema v1.1 (Backward Compatible)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["persona", "core_traits", "linguistic_profile", "behavioral_rules", "advanced_parameters"],
  "properties": {
    // v1.0 sections (REQUIRED, no changes)
    "persona": {...},
    "core_traits": {...},
    "linguistic_profile": {...},
    "behavioral_rules": {...},
    "response_patterns": {...},
    "advanced_parameters": {...},
    
    // New v1.1 sections (OPTIONAL)
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
              "modifiers": {"type": "object"}
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
    }
  }
}
```

---

## ✅ Backward Compatibility

### v1.0 Personality (NO v1.1 changes)

```json
// alicia_v1.0.json
{
  "persona": {...},
  "core_traits": {...},
  "advanced_parameters": {...}
  // NO hierarchical_config
  // NO mood_config
}
```

**Behavior:** Works same as v1.0 (static compilation)

### v1.1 Personality (WITH changes)

```json
// alicia_v1.1.json
{
  "persona": {...},
  "core_traits": {...},
  "advanced_parameters": {...},
  "hierarchical_config": {"enabled": true, ...},  // ← NEW
  "mood_config": {"enabled": true, ...}           // ← NEW
}
```

**Behavior:** Dynamic compilation with JSON modifiers

---

## 📊 Summary

| Aspect | v1.0 Current | v1.1 Proposed | Hardcoded? |
|--------|-------------|---------------|------------|
| **Base personality** | JSON | JSON (same) | ❌ NO |
| **Compilation** | Once (static) | Per message (dynamic) | - |
| **Relationship levels** | Doesn't exist | JSON configurable | ❌ NO |
| **Moods** | Doesn't exist | JSON configurable | ❌ NO |
| **Affinity ranges** | Doesn't exist | JSON configurable | ❌ NO |
| **Modifiers** | Doesn't exist | JSON configurable | ❌ NO |
| **Defaults** | - | Code (only if JSON doesn't specify) | ✅ Yes (only defaults) |

---

## 🚀 Conclusion

1. **EVERYTHING configurable in JSON** (not hardcoded)
2. **Backward compatible** (v1.0 personalities keep working)
3. **Dynamic compilation** (per message, not once)
4. **Extensible** (each personality defines its own levels/moods)

---

<div align="center">

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

