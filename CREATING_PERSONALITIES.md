# 🎭 Complete Guide: Creating Personalities in LuminoraCore

**Version:** 1.0.0  
**Language:** English  
**Updated:** October 2025

---

## 📍 Personality Location

### In the Cloned Repository

```
luminoracore/
└── luminoracore/
    └── personalities/          ← 📁 Personalities are here
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
        └── _template.json       ← 📄 Template for creating new ones
```

**Correct path to load:**
```python
from luminoracore import Personality

# ✅ CORRECT:
personality = Personality("luminoracore/luminoracore/personalities/dr_luna.json")

# ❌ INCORRECT (doesn't exist in clone):
personality = Personality("personalidades/Dr. Luna.json")
```

---

## 📖 What is a Personality?

A personality in LuminoraCore is a JSON file that defines:
- **Who** the AI is (name, description, author)
- **How it speaks** (tone, style, vocabulary)
- **How it behaves** (rules, responses, limits)
- **What it can do** (advanced parameters, examples)

---

## 🏗️ JSON File Structure

### Required Sections

Every personality MUST have these sections:

```json
{
  "persona": { ... },              // ✅ Required
  "core_traits": { ... },          // ✅ Required
  "linguistic_profile": { ... },   // ✅ Required
  "behavioral_rules": [ ... ]      // ✅ Required
}
```

### Optional Sections

```json
{
  "trigger_responses": { ... },    // ⭐ Highly recommended
  "advanced_parameters": { ... },  // ⭐ Recommended
  "safety_guards": { ... },        // ⭐ Highly recommended
  "examples": { ... },             // ⭐ Recommended
  "metadata": { ... }              // ℹ️ Optional
}
```

---

## 📝 Detailed Guide for Each Section

### 1️⃣ `persona` - Basic Information

Defines who your personality is.

```json
{
  "persona": {
    "name": "Dr. Luna",                    // Unique name
    "version": "1.0.0",                    // Semantic version (X.Y.Z)
    "description": "An enthusiastic scientist...",  // Brief description
    "author": "Your Name",                 // Who created it
    "tags": ["scientist", "educational"],  // Search tags
    "language": "en",                      // Primary language
    "compatibility": [                     // Compatible providers
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

**Available languages:** `en`, `es`, `fr`, `de`, `it`, `pt`, `zh`, `ja`, `ko`, `ru`

---

### 2️⃣ `core_traits` - Fundamental Traits

Defines the essence of the personality.

```json
{
  "core_traits": {
    "archetype": "scientist",      // See list below
    "temperament": "energetic",    // See list below
    "communication_style": "conversational"  // See list below
  }
}
```

**Available archetypes:**
- `scientist`, `caregiver`, `rebel`, `explorer`, `sage`, `hero`, `ruler`, `creator`, `innocent`, `jester`, `lover`, `everyman`

**Available temperaments:**
- `calm`, `energetic`, `serious`, `playful`, `mysterious`, `cool`

**Communication styles:**
- `formal`, `conversational`, `casual`, `poetic`, `technical`, `direct`

---

### 3️⃣ `linguistic_profile` - Linguistic Profile

Controls how the personality speaks.

```json
{
  "linguistic_profile": {
    "tone": ["enthusiastic", "friendly", "curious"],
    "syntax": "varied",           // simple, varied, complex, elaborate
    "vocabulary": [               // Characteristic words
      "fascinating", 
      "remarkable", 
      "incredible"
    ],
    "fillers": [                  // Speech fillers
      "oh my!", 
      "wow!", 
      "absolutely!"
    ],
    "punctuation_style": "liberal"  // minimal, moderate, liberal, excessive
  }
}
```

---

### 4️⃣ `behavioral_rules` - Behavioral Rules

Defines how the personality should act.

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
- Be specific and clear
- Use imperatives ("Always...", "Never...", "Focus on...")
- 3-6 rules is ideal

---

### 5️⃣ `trigger_responses` - Automatic Responses

Predefined responses for common situations.

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

### 6️⃣ `advanced_parameters` - Advanced Parameters

Fine-grained behavior controls (values 0.0-1.0).

```json
{
  "advanced_parameters": {
    "verbosity": 0.9,      // How much it talks (0=concise, 1=detailed)
    "formality": 0.4,      // Formality (0=casual, 1=very formal)
    "humor": 0.6,          // Use of humor (0=serious, 1=funny)
    "empathy": 0.8,        // Empathy (0=cold, 1=very empathetic)
    "creativity": 0.8,     // Creativity (0=literal, 1=creative)
    "directness": 0.7      // Directness (0=indirect, 1=direct)
  }
}
```

---

### 7️⃣ `safety_guards` - Safety Guards

Content limits and filters.

```json
{
  "safety_guards": {
    "forbidden_topics": [
      "harmful experiments",
      "dangerous chemicals",
      "illegal activities"
    ],
    "tone_limits": {
      "max_aggression": 0.1,      // Maximum aggression level
      "max_informality": 0.6      // Maximum informality level
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

### 8️⃣ `examples` - Usage Examples

Examples showing how it should respond.

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

### 9️⃣ `metadata` - Metadata

Additional information (optional).

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

## 🚀 Step by Step: Create Your First Personality

### Option 1: Using the Template (Recommended)

```bash
# 1. Copy the template
cp luminoracore/luminoracore/personalities/_template.json my_personality.json

# 2. Edit the file
# Replace all placeholder values with your personality

# 3. Validate
luminoracore validate my_personality.json

# 4. Test
luminoracore test --personality my_personality.json --provider openai
```

### Option 2: CLI Interactive Wizard

```bash
# The CLI will guide you step by step
luminoracore create --name "My Personality" --interactive
```

---

## 📋 Complete Example: "Motivational Coach"

```json
{
  "persona": {
    "name": "Motivational Coach",
    "version": "1.0.0",
    "description": "A personal trainer who motivates and supports achieving goals",
    "author": "Your Name",
    "tags": ["motivational", "coach", "sports", "inspiring"],
    "language": "en",
    "compatibility": ["openai", "anthropic", "deepseek", "mistral"]
  },
  
  "core_traits": {
    "archetype": "hero",
    "temperament": "energetic",
    "communication_style": "conversational"
  },
  
  "linguistic_profile": {
    "tone": ["motivational", "energetic", "positive"],
    "syntax": "simple",
    "vocabulary": ["champion", "warrior", "victory", "achievement"],
    "fillers": ["let's go!", "you can do it!", "incredible!"],
    "punctuation_style": "excessive"
  },
  
  "behavioral_rules": [
    "Always motivate and encourage the user",
    "Turn each challenge into an opportunity",
    "Use sports metaphors",
    "Celebrate every small achievement",
    "Maintain a positive and energetic attitude"
  ],
  
  "trigger_responses": {
    "on_greeting": [
      "Hello champion! Ready to conquer the day?",
      "Welcome warrior! What goal are we achieving today?"
    ],
    "on_success": [
      "THAT'S IT! You're incredible! Keep it up!",
      "WOW! What a victory! I'm proud of you!"
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
    "forbidden_topics": ["dangerous activities", "harmful content"],
    "tone_limits": {
      "max_aggression": 0.2,
      "max_informality": 0.8
    },
    "content_filters": ["violence", "adult"]
  }
}
```

---

## ✅ Validate Your Personality

```bash
# Validate against schema
luminoracore validate my_personality.json

# If valid, you'll see:
✅ my_personality.json: Valid personality
```

---

## 🧪 Test Your Personality

### With CLI:

```bash
# Interactive mode (chat)
luminoracore test --personality my_personality.json --provider openai --interactive

# Quick test
luminoracore test --personality my_personality.json --provider openai
```

### With Python:

```python
from luminoracore import Personality, PersonalityCompiler, LLMProvider

# Load
personality = Personality("my_personality.json")

# Compile
compiler = PersonalityCompiler()
result = compiler.compile(personality, LLMProvider.OPENAI)

print(result.prompt)  # See generated prompt
```

---

## 📚 Included Example Personalities

All located in: `luminoracore/luminoracore/personalities/`

| File | Name | Type |
|------|------|------|
| `dr_luna.json` | Dr. Luna | Enthusiastic scientist |
| `alex_digital.json` | Alex Digital | Gen Z digital native |
| `captain_hook.json` | Captain Hook | Adventurous pirate |
| `grandma_hope.json` | Grandma Hope | Caring grandmother |
| `lila_charm.json` | Lila Charm | Elegant charmer |
| `marcus_sarcastic.json` | Marcus Sarcasmus | Witty sarcastic |
| `professor_stern.json` | Professor Stern | Rigorous academic |
| `rocky_inspiration.json` | Rocky Inspiration | Motivational coach |
| `victoria_sterling.json` | Victoria Sterling | Business leader |
| `zero_cool.json` | Zero Cool | Ethical hacker |
| `_template.json` | Template | Base for creating |

---

## 🔍 Complete JSON Schema

The official schema is at:
```
luminoracore/luminoracore/schema/personality.schema.json
```

You can view it for advanced validations and see all available fields.

---

## 💡 Tips and Best Practices

### ✅ DO:
- Use descriptive and unique names
- Be specific in behavioral rules
- Include several response examples
- Test with different providers
- Always validate before using
- Use appropriate language for your audience

### ❌ DON'T:
- Don't use special characters in the file name
- Don't copy examples without personalizing them
- Don't forget safety guards
- Don't use offensive vocabulary
- Don't make contradictory rules

---

## 🆘 Troubleshooting

### Error: "Validation failed"

```bash
# See error details
luminoracore validate my_personality.json --verbose
```

Common causes:
- Missing required section
- "version" value doesn't follow X.Y.Z format
- "language" not in allowed list
- "archetype" not valid

### Error: "File not found"

Verify the path:
```python
# ✅ CORRECT (from project root):
Personality("luminoracore/luminoracore/personalities/dr_luna.json")

# ✅ CORRECT (absolute path):
Personality("/complete/path/my_personality.json")

# ❌ INCORRECT (doesn't exist in clone):
Personality("personalidades/Dr. Luna.json")
```

---

## 📖 References

- **Complete schema:** `luminoracore/luminoracore/schema/personality.schema.json`
- **Examples:** `luminoracore/luminoracore/personalities/*.json`
- **API Documentation:** `luminoracore/docs/api_reference.md`
- **CLI Help:** `luminoracore create --help`

---

## 🎓 Next Step

Once your personality is created:
1. ✅ Validate it: `luminoracore validate`
2. ✅ Test it: `luminoracore test`
3. ✅ Use it in your app with the SDK
4. ✅ Share it with the community

---

---

## 🎉 NEW in v1.1: Hierarchical Personalities

LuminoraCore v1.1 adds relationship levels to personalities!

### What's New?

You can now define how personality changes based on relationship level:

```json
{
  "persona": {
    "name": "Alicia",
    "version": "1.1.0",
    ...
  },
  
  "advanced_parameters": {
    "empathy": 0.9,
    "formality": 0.5,
    "humor": 0.6
  },
  
  "hierarchical_config": {
    "enabled": true,
    "relationship_levels": [
      {
        "name": "stranger",
        "affinity_range": [0, 20],
        "description": "Initial interactions, more formal",
        "modifiers": {
          "advanced_parameters": {
            "formality": 0.2,
            "humor": -0.1
          }
        }
      },
      {
        "name": "friend",
        "affinity_range": [41, 60],
        "description": "Comfortable relationship",
        "modifiers": {
          "advanced_parameters": {
            "formality": -0.2,
            "humor": 0.2
          }
        }
      },
      {
        "name": "close_friend",
        "affinity_range": [61, 80],
        "description": "Very close relationship",
        "modifiers": {
          "advanced_parameters": {
            "formality": -0.3,
            "humor": 0.3
          }
        }
      }
    ]
  }
}
```

### How It Works

1. **Base Parameters:** Define default values in `advanced_parameters`
2. **Level Modifiers:** Each level adds/subtracts from base values
3. **Dynamic Compilation:** Parameters adjust automatically based on affinity points
4. **Backward Compatible:** Optional - personalities without it work as v1.0

### Default Relationship Levels

- `stranger` (0-20 points) - Formal, reserved
- `acquaintance` (21-40 points) - Polite, cautious
- `friend` (41-60 points) - Casual, comfortable
- `close_friend` (61-80 points) - Playful, intimate
- `soulmate` (81-100 points) - Deep connection

### Usage

```python
from luminoracore.core.personality_v1_1 import PersonalityV11Extensions
from luminoracore.core.compiler_v1_1 import DynamicPersonalityCompiler

# Load personality with hierarchical config
extensions = PersonalityV11Extensions.from_personality_dict(personality_dict)
compiler = DynamicPersonalityCompiler(personality_dict, extensions)

# Compile at different affinity levels
compiled_stranger = compiler.compile(affinity_points=10)
compiled_friend = compiler.compile(affinity_points=50)
```

**See:** [v1.1 Features Guide](mejoras_v1.1/V1_1_FEATURES_SUMMARY.md) for complete details.

---

**Questions?** Check the complete documentation or run:
```bash
luminoracore --help
luminoracore create --help
```

**Updated:** October 2025 (v1.1 release)

