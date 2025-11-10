# LuminoraCore - Personalities

This folder contains pre-built personalities for LuminoraCore, available in v1.0 format (basic) and v1.1 format (with memory and relationship features).

## 📚 Available Personalities

### ✅ v1.0 - Basic Personalities (100% Functional)

All work perfectly without database or additional configuration:

| Personality | File | Archetype | Temperament | Description |
|------------|------|-----------|-------------|-------------|
| **Dr. Luna** | `dr_luna.json` | scientist | energetic | Enthusiastic scientist explaining complex concepts |
| **Captain Hook Digital** | `captain_hook.json` | adventurer | energetic | Digital pirate turning everything into adventure |
| **Grandma Hope** | `grandma_hope.json` | caregiver | calm | Caring grandmother with traditional wisdom |
| **Marcus Sarcasmus** | `marcus_sarcastic.json` | skeptic | cool | Cynical observer with sarcastic humor |
| **Alex Digital** | `alex_digital.json` | trendy | energetic | Gen Z digital native with internet slang |
| **Victoria Sterling** | `victoria_sterling.json` | leader | serious | Executive leader focused on results |
| **Rocky Inspiration** | `rocky_inspiration.json` | motivator | energetic | Motivational coach full of energy |
| **Zero Cool** | `zero_cool.json` | rebel | cool | Ethical hacker explaining tech from underground |
| **Professor Stern** | `professor_stern.json` | academic | serious | Rigorous academic with Socratic method |
| **Lila Charm** | `lila_charm.json` | charming | mysterious | Charming and sophisticated personality |
| **Template** | `_template.json` | - | - | Template for creating new personalities |

---

### ✨ v1.1 - Personalities with Memory & Relationships

These personalities include advanced configuration to leverage v1.1 features:

| Personality | File | v1.1 Features |
|------------|------|---------------|
| **Dr. Luna v1.1** | `dr_luna_v1_1.json` | Hierarchical system, affinity tracking, memory preferences |

---

## 🔄 Differences between v1.0 and v1.1

### v1.0 - Static Personalities

```json
{
  "persona": {...},
  "core_traits": {...},
  "linguistic_profile": {...},
  "behavioral_rules": [...],
  "advanced_parameters": {
    "verbosity": 0.9,
    "formality": 0.4,
    "humor": 0.6
  }
}
```

**Features:**
- ✅ Consistent and predictable personality
- ✅ No database required
- ✅ Easy to use
- ✅ Perfect for simple use cases

---

### v1.1 - Adaptive Personalities

```json
{
  "persona": {...},
  "core_traits": {...},
  // ... v1.0 fields ...
  
  "hierarchical_config": {
    "enabled": true,
    "relationship_levels": [
      {
        "name": "stranger",
        "affinity_range": [0, 20],
        "modifiers": {
          "advanced_parameters": {
            "formality": 0.3
          }
        }
      },
      {
        "name": "friend",
        "affinity_range": [41, 60],
        "modifiers": {
          "advanced_parameters": {
            "formality": -0.2
          }
        }
      }
    ]
  },
  
  "memory_preferences": {
    "fact_categories": ["personal_info", "preferences"],
    "episode_types": ["milestone", "achievement"],
    "importance_threshold": 6.0
  },
  
  "affinity_config": {
    "interaction_types": {
      "positive": 3,
      "very_positive": 5,
      "shared_interest": 4
    }
  }
}
```

**Features:**
- ✨ Personality that evolves with relationship
- ✨ Remembers facts about the user
- ✨ Stores memorable moments
- ✨ Adjusts behavior based on affinity
- ✨ Requires v1.1 database

---

## 🚀 How to Use

### Use v1.0 Personality (Basic)

```python
from luminoracore import Personality, PersonalityCompiler, LLMProvider

# Load v1.0 personality
personality = Personality("personalities/dr_luna.json")

# Compile
compiler = PersonalityCompiler()
result = compiler.compile(personality, LLMProvider.OPENAI)

print(result.prompt)
```

**✅ Advantages:**
- No additional setup required
- Works immediately
- Predictable behavior

---

### Use v1.1 Personality (Advanced)

```python
from luminoracore.core.personality_v1_1 import PersonalityV11Extensions
from luminoracore.core.compiler_v1_1 import DynamicPersonalityCompiler

# Load v1.1 personality
personality_dict = load_json("personalities/dr_luna_v1_1.json")

# Parse v1.1 extensions
extensions = PersonalityV11Extensions.from_personality_dict(personality_dict)

# Compile dynamically based on affinity
compiler = DynamicPersonalityCompiler(personality_dict, extensions)

# Compile for different affinity levels
compiled_stranger = compiler.compile(affinity_points=10)  # More formal
compiled_friend = compiler.compile(affinity_points=50)     # More casual
```

**✨ Advantages:**
- Personality adapts to relationship
- Remembers user information
- More personalized experience

**Requirements:**
```bash
# Setup v1.1 database
./scripts/setup-v1_1-database.sh
```

---

## 📝 Create Your Own Personality

### Option 1: v1.0 Personality (Recommended to start)

```bash
# Copy template
cp personalities/_template.json my_personality.json

# Edit and customize
# ...

# Validate
luminoracore validate my_personality.json
```

### Option 2: Extend to v1.1

Once you have a working v1.0 personality, you can add:

```json
{
  // ... your v1.0 personality ...
  
  "hierarchical_config": {
    "enabled": true,
    "relationship_levels": [
      {
        "name": "stranger",
        "affinity_range": [0, 20],
        "modifiers": {
          "advanced_parameters": {
            "formality": 0.2  // More formal with strangers
          }
        }
      }
    ]
  }
}
```

---

## 🎯 Recommendations

### When to use v1.0:
- ✅ Simple applications without memory
- ✅ Quick response bots
- ✅ Stateless assistants
- ✅ Rapid prototyping
- ✅ Don't want DB complexity

### When to use v1.1:
- ✨ Personal assistants
- ✨ Chatbots with long-term memory
- ✨ Virtual companions
- ✨ Educational applications
- ✨ Customer support with history

---

## 🔧 Migrate from v1.0 to v1.1

v1.0 personalities **continue working** in v1.1 without changes. Migration is optional:

```bash
# 1. Copy v1.0 personality
cp dr_luna.json dr_luna_v1_1.json

# 2. Add v1.1 fields (see dr_luna_v1_1.json as example)

# 3. Validate
luminoracore validate dr_luna_v1_1.json

# 4. Test
python examples/v1_1_dynamic_personality_demo.py
```

---

## 📊 Feature Comparison

| Feature | v1.0 | v1.1 |
|---------|------|------|
| **Personality Core** | ✅ | ✅ |
| **Multi-LLM Support** | ✅ | ✅ |
| **PersonaBlend™** | ✅ | ✅ |
| **Hierarchical Levels** | ❌ | ✅ |
| **Affinity Tracking** | ❌ | ✅ |
| **Fact Extraction** | ❌ | ✅ |
| **Episodic Memory** | ❌ | ✅ |
| **Dynamic Compilation** | ❌ | ✅ |
| **Database Required** | ❌ | ✅ (optional) |

---

## 📚 Additional Documentation

- **[Personality Format](../docs/personality_format.md)** - v1.0 JSON format
- **[v1.1 Features](../docs/v1_1_features.md)** - v1.1 features
- **[Best Practices](../docs/best_practices.md)** - Best practices
- **[Creating Personalities](../../../CREATING_PERSONALITIES.md)** - Complete guide

---

## 🎉 Quick Examples

### v1.0 Example
```python
# Simple usage without memory
personality = Personality("personalities/dr_luna.json")
compiler = PersonalityCompiler()
result = compiler.compile(personality, LLMProvider.OPENAI)
```

### v1.1 Example
```python
# With memory and affinity
from luminoracore.core.relationship.affinity import AffinityManager

affinity = AffinityManager()
state = affinity.create_state("user123", "dr_luna")

# Update after positive interaction
state = affinity.update_affinity_state(state, points_delta=5)

# Compile with current level
compiler = DynamicPersonalityCompiler(personality_dict, extensions)
compiled = compiler.compile(affinity_points=state.affinity_points)
```

---

**Last update:** October 2025 (v1.1)

**Status:** 
- ✅ 10 v1.0 personalities ready for production
- ✅ 1 v1.1 personality example (Dr. Luna)
- 🔄 More v1.1 personalities in development
