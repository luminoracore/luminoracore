# Getting Started with LuminoraCore

Welcome to LuminoraCore! This guide will help you get up and running with the Universal AI Personality Management Standard.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install LuminoraCore

```bash
pip install luminoracore
```

### Development Installation

For development or to use the latest features:

```bash
git clone https://github.com/luminoracore/luminoracore.git
cd luminoracore
pip install -e ".[dev]"
```

## Quick Start

### 1. Load a Personality

```python
from luminoracore import Personality

# Load a built-in personality
personality = Personality("personalities/dr_luna.json")

print(f"Loaded: {personality.persona.name}")
print(f"Description: {personality.persona.description}")
```

### 2. Validate a Personality

```python
from luminoracore import PersonalityValidator

validator = PersonalityValidator()
result = validator.validate(personality)

if result.is_valid:
    print("✓ Personality is valid!")
else:
    print("✗ Validation errors:")
    for error in result.errors:
        print(f"  - {error}")
```

### 3. Compile for an LLM Provider

```python
from luminoracore import PersonalityCompiler, LLMProvider

compiler = PersonalityCompiler()
result = compiler.compile(personality, LLMProvider.OPENAI)

print(f"Token estimate: {result.token_estimate}")
print(f"Prompt format: {result.metadata['format']}")
```

### 4. Use the Compiled Prompt

```python
# For OpenAI (messages format)
if isinstance(result.prompt, dict) and 'messages' in result.prompt:
    messages = result.prompt['messages']
    # Use with OpenAI API
    # response = openai.ChatCompletion.create(messages=messages, ...)

# For other providers
print(result.prompt)
```

## Command Line Interface

LuminoraCore includes a powerful CLI for all operations:

### Validate Personalities

```bash
# Validate a single personality
luminora validate personalities/dr_luna.json

# Validate all personalities in a directory
luminora validate-all personalities/

# Verbose validation with suggestions
luminora validate personalities/dr_luna.json --verbose
```

### Compile Prompts

```bash
# Compile for a specific provider
luminora compile-prompt personalities/dr_luna.json --provider openai

# Compile for all providers
luminora compile-all personalities/dr_luna.json

# Test compilation
luminora test-compilation personalities/dr_luna.json --provider anthropic
```

### Blend Personalities

```bash
# Blend two personalities with equal weights
luminora blend personalities/dr_luna.json personalities/captain_hook.json

# Blend with custom weights
luminora blend personalities/dr_luna.json personalities/captain_hook.json --weights "0.7,0.3"

# Blend with specific strategy
luminora blend personalities/dr_luna.json personalities/grandma_hope.json --strategy dominant
```

### Get Information

```bash
# Show personality information
luminora info personalities/dr_luna.json

# List all personalities
luminora list personalities/

# Show version
luminora version
```

## Working with Personalities

### Understanding the Schema

LuminoraCore personalities follow a strict JSON schema. Key components:

- **persona**: Basic information (name, version, description, etc.)
- **core_traits**: Fundamental personality characteristics
- **linguistic_profile**: Language and communication patterns
- **behavioral_rules**: Guidelines for behavior
- **trigger_responses**: Responses to specific situations
- **advanced_parameters**: Fine-tuning parameters
- **safety_guards**: Content filtering and safety measures

### Creating a Custom Personality

```python
from luminoracore import Personality

# Define personality data
personality_data = {
    "persona": {
        "name": "My Custom Personality",
        "version": "1.0.0",
        "description": "A custom personality I created",
        "author": "Your Name",
        "tags": ["custom", "example"],
        "language": "en",
        "compatibility": ["openai", "anthropic"]
    },
    "core_traits": {
        "archetype": "scientist",
        "temperament": "calm",
        "communication_style": "formal"
    },
    "linguistic_profile": {
        "tone": ["professional", "friendly"],
        "syntax": "varied",
        "vocabulary": ["example", "demonstration", "illustration"]
    },
    "behavioral_rules": [
        "Always provide accurate information",
        "Be helpful and supportive",
        "Use clear explanations"
    ]
}

# Create and validate
personality = Personality(personality_data)
personality.save("my_custom_personality.json")
```

### Blending Personalities

```python
from luminoracore import PersonaBlend

# Load personalities to blend
personality1 = Personality("personalities/dr_luna.json")
personality2 = Personality("personalities/captain_hook.json")

# Create blender
blender = PersonaBlend()

# Blend with weights
weights = {
    "Dr. Luna": 0.6,
    "Captain Hook Digital": 0.4
}

result = blender.blend([personality1, personality2], weights, strategy="weighted_average")

# Save blended personality
result.blended_personality.save("blended_personality.json")
```

## Examples

LuminoraCore includes comprehensive examples:

### Basic Usage

```bash
python examples/basic_usage.py
```

Demonstrates:
- Loading personalities
- Validation
- Compilation
- Basic operations

### Personality Switching

```bash
python examples/personality_switching.py
```

Shows how to:
- Load multiple personalities
- Compare their characteristics
- Switch between different styles

### Blending Demo

```bash
python examples/blending_demo.py
```

Explores:
- Different blending strategies
- Weighted combinations
- Hybrid approaches

### Multi-LLM Demo

```bash
python examples/multi_llm_demo.py
```

Demonstrates:
- Compilation for different providers
- Format differences
- Token estimation

## Best Practices

### 1. Validation First

Always validate personalities before using them:

```python
validator = PersonalityValidator()
result = validator.validate(personality)

if not result.is_valid:
    # Fix validation errors before proceeding
    pass
```

### 2. Token Management

Be aware of token limits:

```python
# Check token estimate
result = compiler.compile(personality, LLMProvider.OPENAI)
if result.token_estimate > 4000:
    print("Warning: Prompt may be too long")
```

### 3. Provider Compatibility

Check compatibility before compilation:

```python
if personality.is_compatible_with("openai"):
    result = compiler.compile(personality, LLMProvider.OPENAI)
```

### 4. Quality Personalities

Create high-quality personalities by:
- Providing comprehensive behavioral rules
- Including realistic examples
- Setting appropriate safety guards
- Using diverse vocabulary
- Testing with different scenarios

## Troubleshooting

### Common Issues

**Import Error**: Make sure LuminoraCore is installed correctly
```bash
pip install luminoracore
```

**Validation Errors**: Check your personality JSON against the schema
```bash
luminora validate your_personality.json --verbose
```

**Compilation Failures**: Ensure the personality is compatible with the provider
```python
personality.is_compatible_with("openai")  # Should return True
```

### Getting Help

- 📖 Check the [API Reference](api_reference.md)
- 🐛 Report issues on [GitHub](https://github.com/luminoracore/luminoracore/issues)
- 💬 Join our [Discord community](https://discord.gg/luminoracore)
- 📧 Email: team@luminoracore.dev

## Next Steps

Now that you're up and running with LuminoraCore:

1. **Explore the built-in personalities** - Try different ones to see their unique characteristics
2. **Create your own personality** - Follow the schema and best practices
3. **Experiment with blending** - Mix personalities to create unique combinations
4. **Integrate with your application** - Use compiled prompts with your LLM provider
5. **Contribute to the project** - Submit new personalities or improvements

Happy personality crafting! 🎭✨

## What's New in v1.1?

LuminoraCore v1.1 adds powerful memory and relationship features:

- **Hierarchical Personality** - Relationship levels that evolve (stranger → friend → soulmate)
- **Affinity System** - Track relationship points (0-100)
- **Fact Extraction** - Automatically learn from conversations
- **Episodic Memory** - Remember memorable moments
- **Memory Classification** - Organize by importance

**See:** [v1.1 Features Documentation](v1_1_features.md) for complete details.

**Quick example:**
```python
from luminoracore.core.relationship.affinity import AffinityManager, AffinityState

manager = AffinityManager()
state = AffinityState(user_id="user1", personality_name="alicia", affinity_points=0)
state = manager.update_affinity_state(state, points_delta=5)
print(f"Level: {state.current_level}, Points: {state.affinity_points}")
```

All v1.1 features are **100% backward compatible** and **opt-in** via feature flags.