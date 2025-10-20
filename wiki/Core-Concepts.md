# Core Concepts

Understanding the fundamental concepts behind LuminoraCore.

---

## 🎭 What is a Personality?

A **personality** in LuminoraCore is a JSON-based definition that describes how an AI should behave, communicate, and respond.

### Anatomy of a Personality

```json
{
  "persona": {
    "name": "Dr. Luna",
    "tagline": "Your enthusiastic science guide",
    "description": "An enthusiastic scientist who makes complex concepts accessible"
  },
  "core_traits": {
    "archetype": "scientist",
    "temperament": "enthusiastic",
    "communication_style": "educational",
    "values": ["curiosity", "accuracy", "learning"],
    "strengths": ["Explaining complex topics", "Using analogies"]
  },
  "linguistic_profile": {
    "tone": ["enthusiastic", "friendly", "professional"],
    "vocabulary_level": "intermediate",
    "sentence_structure": "varied",
    "expressions": ["Fascinating!", "Let me explain..."]
  },
  "behavioral_rules": {
    "always_do": [
      "Use analogies to explain complex concepts",
      "Show enthusiasm for scientific topics"
    ],
    "never_do": [
      "Use overly technical jargon without explanation",
      "Dismiss questions as 'too basic'"
    ]
  },
  "response_patterns": {
    "greeting": "Hello! I'm Dr. Luna. What scientific mystery shall we explore today?",
    "farewell": "Keep exploring! Science is all around us!",
    "uncertainty": "That's a great question! Let me think about it carefully..."
  }
}
```

### 9 Main Sections

1. **persona** - Basic identity (name, description, tagline)
2. **core_traits** - Fundamental characteristics (archetype, temperament, values)
3. **linguistic_profile** - How they speak (tone, vocabulary, expressions)
4. **behavioral_rules** - What they should/shouldn't do
5. **response_patterns** - Template responses for common situations
6. **context_adaptation** - How they adapt to different contexts
7. **examples** - Sample conversations showing the personality
8. **advanced_parameters** - LLM settings (temperature, max_tokens)
9. **metadata** - Version, author, tags, language

**All sections are validated against JSON Schema.**

---

## ✅ Validation

LuminoraCore validates personalities against a strict JSON Schema to ensure quality and consistency.

### What Gets Validated?

- ✅ All required fields are present
- ✅ Data types are correct (string, array, number, etc.)
- ✅ Enum values are valid (archetype, temperament, tone, etc.)
- ✅ Structure follows the schema
- ✅ Cross-field consistency

### Validation Levels

```bash
# Basic validation
luminoracore validate personality.json

# Strict validation (stricter rules)
luminoracore validate personality.json --strict

# Programmatic validation
from luminoracore import Personality, PersonalityValidator

personality = Personality("personality.json")
validator = PersonalityValidator()
result = validator.validate(personality)

if result.is_valid:
    print("✅ Valid")
    print(f"Warnings: {len(result.warnings)}")
else:
    print("❌ Invalid")
    for error in result.errors:
        print(f"  - {error}")
```

---

## 🔄 Compilation

**Compilation** is the process of converting a personality JSON into a text prompt optimized for a specific LLM provider.

### Why Compilation?

Different LLM providers have different:
- Prompt formats
- Token limits
- Special instructions
- Optimization techniques

LuminoraCore handles these differences automatically.

### How It Works

```python
from luminoracore import Personality, PersonalityCompiler, LLMProvider

# Load personality
personality = Personality("dr_luna.json")

# Compile for OpenAI
compiler = PersonalityCompiler()
result = compiler.compile(personality, LLMProvider.OPENAI)

print(result.prompt)
# → "You are Dr. Luna, an enthusiastic scientist who makes complex 
#     concepts accessible. Always use analogies to explain... [etc]"

print(f"Estimated tokens: {result.token_estimate}")
# → Estimated tokens: 387
```

### Supported Providers

LuminoraCore compiles for 7 providers:

1. **OpenAI** - GPT-3.5, GPT-4
2. **Anthropic** - Claude 3 (Sonnet, Opus, Haiku)
3. **DeepSeek** - DeepSeek Chat
4. **Mistral** - Mistral Large, Medium, Small
5. **Cohere** - Command, Command Light
6. **Google** - Gemini Pro, Gemini Ultra
7. **Llama** - Llama 2, Llama 3 (via Replicate)

### Compilation Options

```python
# Include examples in prompt
result = compiler.compile(personality, provider, include_examples=True)

# Compact mode (fewer tokens)
result = compiler.compile(personality, provider, include_examples=False)

# With caching (faster for repeated compilations)
compiler = PersonalityCompiler(cache_size=128)
result = compiler.compile(personality, provider)
```

---

## 🎨 PersonaBlend™ Technology

**PersonaBlend™** is LuminoraCore's proprietary technology for blending multiple personalities into a new, cohesive personality.

### How Blending Works

PersonaBlend uses **weighted mathematical fusion** of personality traits:

#### 1. Numerical/Scale Values
```
warmth_blended = (warmth_A × weight_A) + (warmth_B × weight_B)
```

#### 2. Categorical Values (Enums)
```
archetype_blended = archetype with highest weighted score
```

#### 3. Lists (tone, strengths, etc.)
```
tone_blended = top N items ranked by weighted frequency
```

#### 4. Text Fields
```
description_blended = base from highest weight + key elements from others
```

### Example: Blend Two Personalities

```python
from luminoracore import Personality, PersonalityBlender

# Load personalities
dr_luna = Personality("dr_luna.json")      # Scientist
rocky = Personality("rocky_inspiration.json")  # Motivator

# Blend: 70% scientist + 30% motivator
blender = PersonalityBlender()
blended = blender.blend_personalities(
    personalities=[dr_luna, rocky],
    weights=[0.7, 0.3],
    strategy="weighted_average"
)

print(blended.persona.name)
# → "Dr. Luna + Rocky Inspiration Blend"

print(blended.persona.description)
# → "An enthusiastic scientist who motivates through scientific discovery..."
```

### Blend Strategies

1. **weighted_average** (default)
   - Mathematical weighted average
   - Deterministic results
   - Balanced fusion

2. **dominant** (coming in v1.1)
   - Highest weight personality dominates
   - Others add flavor
   - More pronounced character

3. **adaptive** (coming in v1.2)
   - Context-aware blending
   - Dynamic weight adjustment
   - Intelligent fusion

### CLI Blending

```bash
# Blend two personalities
luminoracore blend \
  "dr_luna.json:0.6" \
  "rocky_inspiration.json:0.4" \
  --output enthusiastic_scientist.json

# Validate the blend
luminoracore validate enthusiastic_scientist.json

# Test the blend
luminoracore test enthusiastic_scientist.json --provider deepseek
```

### SDK Blending (Runtime)

```python
from luminoracore_sdk import LuminoraCoreClient

client = LuminoraCoreClient()
await client.initialize()

# Load personalities
await client.load_personality("dr_luna", dr_luna_data)
await client.load_personality("rocky", rocky_data)

# Blend at runtime
blended = await client.blend_personalities(
    personality_names=["dr_luna", "rocky"],
    weights=[0.6, 0.4],
    blend_name="enthusiastic_scientist"
)

# Use the blended personality
session_id = await client.create_session(
    personality_name="enthusiastic_scientist",
    provider_config=provider_config
)
```

### Common Blend Combinations

| Blend | Result | Use Case |
|-------|--------|----------|
| 70% Scientist + 30% Motivator | Enthusiastic Science Coach | Educational content |
| 50% Professional + 50% Caring | Wise Business Mentor | Executive coaching |
| 60% Technical + 40% Creative | Innovative Engineer | Product development |
| 80% Academic + 20% Humor | Engaging Professor | Online courses |

---

## 📊 Sessions & Conversations (SDK)

### What is a Session?

A **session** represents a conversation with a specific personality and LLM provider.

```python
session_id = await client.create_session(
    personality_name="dr_luna",
    provider_config=ProviderConfig(
        name="deepseek",
        api_key="sk-...",
        model="deepseek-chat"
    )
)
```

### Session Lifecycle

```
1. CREATE SESSION
   ↓
2. SEND MESSAGES (conversation history builds up)
   ↓
3. STORE CUSTOM MEMORY (optional - user preferences, context)
   ↓
4. SWITCH PERSONALITY (optional)
   ↓
5. END SESSION (cleanup)
```

### Conversation History

```python
# Add messages to conversation
response1 = await client.send_message(session_id, "What is quantum mechanics?")
response2 = await client.send_message(session_id, "Can you explain more?")

# Get full conversation history
messages = await client.get_conversation(session_id)
# → [
#     {"role": "user", "content": "What is quantum mechanics?"},
#     {"role": "assistant", "content": "Quantum mechanics is..."},
#     {"role": "user", "content": "Can you explain more?"},
#     {"role": "assistant", "content": "Certainly! Let me dive deeper..."}
#   ]
```

### Session Memory

Store custom data about the user/session:

```python
# Store user preferences
await client.store_memory(
    session_id=session_id,
    key="experience_level",
    value="intermediate"
)

await client.store_memory(
    session_id=session_id,
    key="topics_of_interest",
    value=["quantum physics", "cosmology", "particle physics"]
)

# Retrieve memory
level = await client.get_memory(session_id, "experience_level")
# → "intermediate"
```

---

## 💾 Storage Backends

### Memory (Default)

**Pros:**
- ✅ Zero setup
- ✅ Very fast
- ✅ Perfect for testing

**Cons:**
- ❌ Lost when app closes
- ❌ Not shareable between processes

```python
client = LuminoraCoreClient(
    storage_config=StorageConfig(storage_type="memory")
)
```

### JSON File

**Pros:**
- ✅ Persistent
- ✅ Zero setup
- ✅ Portable
- ✅ Human-readable

**Cons:**
- ❌ Slow with many sessions
- ❌ Not suitable for high concurrency

```python
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="json",
        json_file_path="./sessions/conversations.json"
    )
)
```

### SQLite

**Pros:**
- ✅ Persistent
- ✅ Zero setup
- ✅ Perfect for mobile
- ✅ Fast SQL queries

**Cons:**
- ❌ Not for high concurrency
- ❌ No horizontal scaling

```python
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="sqlite",
        sqlite_path="./data/luminoracore.db"
    )
)
```

### Redis

**Pros:**
- ✅ Persistent
- ✅ Very fast (in-memory)
- ✅ Perfect for sessions
- ✅ Automatic TTL

**Cons:**
- ❌ Requires Redis server

```python
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="redis",
        redis_url="redis://localhost:6379"
    )
)
```

### Decision Tree

```
Need persistence?
  └─ No  → Use MEMORY
  └─ Yes → What type of app?
           ├─ Mobile app → Use SQLITE
           ├─ Simple desktop app → Use JSON or SQLITE
           ├─ Web app (single server) → Use SQLITE or REDIS
           ├─ Web app (multiple servers) → Use REDIS
           └─ Enterprise → Use POSTGRESQL or MONGODB
```

---

## 🔧 Provider Configuration

### Basic Configuration

```python
from luminoracore_sdk.types.provider import ProviderConfig

provider_config = ProviderConfig(
    name="deepseek",           # Which provider
    api_key="sk-your-key",     # Your API key
    model="deepseek-chat",     # Which model
    base_url=None,             # Optional: custom URL
    extra={                    # Optional: additional settings
        "timeout": 30,
        "max_retries": 3
    }
)
```

### Custom Endpoints

Use custom or local LLM endpoints:

```python
# Ollama (local)
provider_config = ProviderConfig(
    name="openai",  # OpenAI-compatible API
    api_key="ollama",
    base_url="http://localhost:11434/v1",
    model="llama2"
)

# Azure OpenAI
provider_config = ProviderConfig(
    name="openai",
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    base_url="https://YOUR-RESOURCE.openai.azure.com",
    model="gpt-35-turbo"
)

# Corporate proxy
provider_config = ProviderConfig(
    name="openai",
    api_key="sk-...",
    base_url="https://proxy.company.com/openai/v1",
    model="gpt-4"
)
```

---

## 🏗️ Architecture

### Component Relationships

```
┌──────────────────────────────────────┐
│  Base Engine (luminoracore)          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  • Load personalities                │
│  • Validate against schema           │
│  • Compile to prompts                │
│  • Blend personalities               │
│  • NO LLM calls                      │
│  • NO session management             │
└──────────────┬───────────────────────┘
               │
               │ BOTH USE THE ENGINE
               │
        ┌──────┴──────┐
        ▼             ▼
┌───────────┐  ┌──────────────────┐
│  CLI      │  │  SDK             │
│  ━━━━━━━  │  │  ━━━━━━━━━━━━━  │
│  Terminal │  │  Python Apps     │
│  Commands │  │  ━━━━━━━━━━━━━  │
│  Wizard   │  │  • Sessions      │
│  Server   │  │  • LLM calls     │
│           │  │  • Storage       │
│           │  │  • Analytics     │
└───────────┘  └──────────────────┘
```

### Data Flow

```
1. PERSONALITY JSON
   ↓
2. VALIDATION (schema check)
   ↓
3. COMPILATION (JSON → prompt text)
   ↓
4. LLM API CALL (SDK only)
   ↓
5. RESPONSE + USAGE TRACKING
```

---

## 🎯 Use Cases by Component

### Use Core Engine When:
- ✅ Building custom tools
- ✅ Need programmatic access
- ✅ No LLM calls needed
- ✅ Validating personalities
- ✅ Compiling prompts for manual use

### Use CLI When:
- ✅ Quick testing/validation
- ✅ Development workflow
- ✅ Automation scripts
- ✅ Interactive personality creation
- ✅ Local development server

### Use SDK When:
- ✅ Building production apps
- ✅ Need real LLM calls
- ✅ Session management required
- ✅ Persistent storage needed
- ✅ Analytics/monitoring important

---

## 🔐 Security Best Practices

### API Keys

**❌ NEVER:**
```python
# DON'T hardcode API keys
api_key = "sk-proj-1234567890"  # ❌ Bad
```

**✅ ALWAYS:**
```python
# Use environment variables
api_key = os.getenv("OPENAI_API_KEY")  # ✅ Good
```

### Validation

**Always validate personalities before deployment:**

```bash
# Strict validation before production
luminoracore validate personality.json --strict
```

### Storage

**For production:**
- ✅ Use encrypted connections (Redis TLS, PostgreSQL SSL)
- ✅ Sanitize user inputs
- ✅ Implement rate limiting
- ✅ Monitor token usage

---

## 📈 Performance Optimization

### Caching

**Enable compilation caching** (enabled by default):

```python
# LRU cache for compiled prompts
compiler = PersonalityCompiler(cache_size=128)

# Check cache performance
stats = compiler.get_cache_stats()
print(f"Cache hit rate: {stats['hit_rate']:.2%}")
```

### Token Optimization

**Reduce token usage:**

```python
# 1. Shorter descriptions
# 2. Fewer examples
# 3. Compact behavioral rules
# 4. Use include_examples=False when compiling

compiler.compile(personality, provider, include_examples=False)
```

### Async Concurrency

**Process multiple requests in parallel:**

```python
# Instead of sequential:
for message in messages:
    response = await client.send_message(session_id, message)

# Do parallel:
tasks = [client.send_message(session_id, msg) for msg in messages]
responses = await asyncio.gather(*tasks)
```

---

## 🎓 Advanced Concepts

### Custom Providers (Coming Soon)

You'll be able to register custom LLM providers:

```python
from luminoracore_sdk.providers import ProviderFactory, BaseProvider

class MyCustomProvider(BaseProvider):
    async def chat(self, messages, **kwargs):
        # Your implementation
        pass

# Register
ProviderFactory.register_provider("mycustom", MyCustomProvider)
```

### Custom Storage (Coming Soon)

Implement your own storage backend:

```python
from luminoracore_sdk.session.storage import BaseStorage

class MyCustomStorage(BaseStorage):
    async def save_session(self, session_id, data):
        # Your implementation
        pass
```

### Personality Adaptation (v2.0 Roadmap)

Real-time personality adaptation based on:
- User feedback
- Conversation tone
- Context changes
- Performance metrics

---

## 📚 Related Pages

- **[Getting Started](Getting-Started)** - Installation and setup
- **[FAQ](FAQ)** - Common questions
- **[Troubleshooting](Troubleshooting)** - Problem solving

---

**Want to dive into code? Check the [examples](https://github.com/luminoracore/luminoracore/tree/main/luminoracore/examples)!**

---

_Last updated: October 2025 | LuminoraCore v1.1.0_

