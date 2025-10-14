# API Reference

This document provides a comprehensive reference for the LuminoraCore API.

## Core Classes

### Personality

The main class for working with AI personalities.

```python
from luminoracore import Personality

# Load from file
personality = Personality("path/to/personality.json")

# Load from dictionary
personality = Personality(personality_data)

# Access properties
print(personality.persona.name)
print(personality.core_traits.archetype)
print(personality.linguistic_profile.tone)
```

#### Properties

- `persona` - Basic personality information
- `core_traits` - Fundamental characteristics
- `linguistic_profile` - Language patterns
- `behavioral_rules` - Behavior guidelines
- `trigger_responses` - Situation-specific responses
- `advanced_parameters` - Fine-tuning parameters
- `safety_guards` - Content filtering
- `examples` - Sample interactions
- `metadata` - Additional information

#### Methods

- `save(path)` - Save personality to file
- `validate()` - Validate personality data
- `is_compatible_with(provider)` - Check provider compatibility
- `compile(provider)` - Compile for specific provider

### PersonalityValidator

Validates personality data against the schema.

```python
from luminoracore import PersonalityValidator

validator = PersonalityValidator()
result = validator.validate(personality)

if result.is_valid:
    print("Valid!")
else:
    for error in result.errors:
        print(f"Error: {error}")
```

#### Methods

- `validate(personality)` - Validate personality
- `validate_file(path)` - Validate from file
- `is_valid()` - Check if last validation passed
- `get_errors()` - Get validation errors
- `get_warnings()` - Get validation warnings
- `get_suggestions()` - Get improvement suggestions

#### Performance Features

```python
# Enable performance validations
validator = PersonalityValidator(enable_performance_checks=True)

# Validate with performance checks
result = validator.validate(personality)

# Check for performance warnings
for warning in result.warnings:
    if "performance" in warning.lower():
        print(f"Performance warning: {warning}")
```

### PersonalityCompiler

Compiles personalities for different LLM providers with caching and performance optimizations.

```python
from luminoracore import PersonalityCompiler, LLMProvider

# Create compiler with cache
compiler = PersonalityCompiler(cache_size=128)

# Compile personality
result = compiler.compile(personality, LLMProvider.OPENAI)

# Get cache statistics
stats = compiler.get_cache_stats()
print(f"Cache hit rate: {stats['hit_rate']}%")

# Clear cache if needed
compiler.clear_cache()

print(result.prompt)
print(result.token_estimate)
print(result.metadata)
```

#### Methods

- `compile(personality, provider)` - Compile personality
- `compile_all(personality)` - Compile for all providers
- `get_supported_providers()` - List supported providers
- `estimate_tokens(personality, provider)` - Estimate token usage

### PersonaBlend

Blends multiple personalities together.

```python
from luminoracore import PersonaBlend

blender = PersonaBlend()
result = blender.blend(
    personalities=[personality1, personality2],
    weights={"Personality1": 0.6, "Personality2": 0.4},
    strategy="weighted_average"
)

blended = result.blended_personality
```

#### Methods

- `blend(personalities, weights, strategy)` - Blend personalities
- `get_strategies()` - List available strategies
- `validate_weights(weights)` - Validate weight configuration

## Enums

### LLMProvider

Supported LLM providers.

```python
from luminoracore import LLMProvider

# Available providers
LLMProvider.OPENAI
LLMProvider.ANTHROPIC
LLMProvider.LLAMA
LLMProvider.MISTRAL
LLMProvider.COHERE
LLMProvider.GOOGLE
```

### Archetype

Personality archetypes.

```python
from luminoracore import Archetype

# Available archetypes
Archetype.SCIENTIST
Archetype.ADVENTURER
Archetype.CAREGIVER
Archetype.SKEPTIC
Archetype.TRENDY
Archetype.LEADER
Archetype.MOTIVATOR
Archetype.REBEL
Archetype.ACADEMIC
Archetype.CHARMING
```

### Temperament

Personality temperaments.

```python
from luminoracore import Temperament

# Available temperaments
Temperament.CALM
Temperament.ENERGETIC
Temperament.SERIOUS
Temperament.PLAYFUL
Temperament.MYSTERIOUS
Temperament.DIRECT
```

### CommunicationStyle

Communication styles.

```python
from luminoracore import CommunicationStyle

# Available styles
CommunicationStyle.FORMAL
CommunicationStyle.CASUAL
CommunicationStyle.TECHNICAL
CommunicationStyle.CONVERSATIONAL
CommunicationStyle.POETIC
CommunicationStyle.HUMOROUS
```

## Data Models

### PersonaData

Basic personality information.

```python
{
    "name": "string",
    "version": "string",
    "description": "string",
    "author": "string",
    "tags": ["string"],
    "language": "string",
    "compatibility": ["string"]
}
```

### CoreTraits

Fundamental personality characteristics.

```python
{
    "archetype": "string",
    "temperament": "string",
    "communication_style": "string"
}
```

### LinguisticProfile

Language and communication patterns.

```python
{
    "tone": ["string"],
    "syntax": "string",
    "vocabulary": ["string"],
    "fillers": ["string"],
    "punctuation_style": "string"
}
```

### BehavioralRules

Guidelines for behavior.

```python
[
    "string",  # Rule 1
    "string",  # Rule 2
    "string"   # Rule 3
]
```

### TriggerResponses

Responses to specific situations.

```python
{
    "on_greeting": ["string"],
    "on_confusion": ["string"],
    "on_success": ["string"],
    "on_error": ["string"],
    "on_goodbye": ["string"]
}
```

### AdvancedParameters

Fine-tuning parameters (0.0-1.0 scale).

```python
{
    "verbosity": 0.7,
    "formality": 0.8,
    "humor": 0.3,
    "empathy": 0.6,
    "creativity": 0.5,
    "directness": 0.7
}
```

### SafetyGuards

Content filtering and safety measures.

```python
{
    "forbidden_topics": ["string"],
    "tone_limits": {
        "max_aggression": 0.1,
        "max_informality": 0.3
    },
    "content_filters": ["string"]
}
```

### Examples

Sample interactions.

```python
{
    "sample_responses": [
        {
            "input": "string",
            "output": "string",
            "context": "string"
        }
    ]
}
```

### Metadata

Additional information.

```python
{
    "created_at": "string",
    "updated_at": "string",
    "downloads": 0,
    "rating": 0.0,
    "license": "string"
}
```

## Compilation Results

### CompilationResult

Result of personality compilation.

```python
class CompilationResult:
    prompt: str | dict  # Compiled prompt
    token_estimate: int  # Estimated token count
    metadata: dict  # Additional information
    provider: str  # Target provider
    format: str  # Output format
```

## Validation Results

### ValidationResult

Result of personality validation.

```python
class ValidationResult:
    is_valid: bool  # Whether validation passed
    errors: List[str]  # Validation errors
    warnings: List[str]  # Validation warnings
    suggestions: List[str]  # Improvement suggestions
    score: float  # Quality score (0.0-1.0)
```

## Blending Results

### BlendResult

Result of personality blending.

```python
class BlendResult:
    blended_personality: Personality  # Resulting personality
    blend_metadata: dict  # Blending information
    strategy_used: str  # Strategy applied
    weights_used: dict  # Weights applied
    quality_score: float  # Blend quality score
```

## Error Handling

### LuminoraCoreError

Base exception for all LuminoraCore errors.

```python
from luminoracore import LuminoraCoreError

try:
    personality = Personality("invalid.json")
except LuminoraCoreError as e:
    print(f"Error: {e}")
```

### Specific Exceptions

- `ValidationError` - Validation failures
- `CompilationError` - Compilation failures
- `BlendError` - Blending failures
- `ProviderError` - Provider-specific errors
- `FileError` - File I/O errors

## Utility Functions

### File Operations

```python
from luminoracore.utils import load_personality, save_personality

# Load personality from file
personality = load_personality("path/to/personality.json")

# Save personality to file
save_personality(personality, "path/to/output.json")
```

### Validation Helpers

```python
from luminoracore.utils import validate_schema, check_compatibility

# Validate against schema
is_valid = validate_schema(personality_data)

# Check provider compatibility
compatible = check_compatibility(personality, "openai")
```

### Token Estimation

```python
from luminoracore.utils import estimate_tokens

# Estimate token count
token_count = estimate_tokens(prompt_text)
```

## Configuration

### Global Settings

```python
from luminoracore import configure

# Configure global settings
configure(
    default_provider="openai",
    validation_strict=True,
    cache_enabled=True,
    log_level="INFO"
)
```

### Provider Configuration

```python
from luminoracore import set_provider_config

# Configure specific provider
set_provider_config("openai", {
    "api_key": "your-api-key",
    "model": "gpt-4",
    "temperature": 0.7
})
```

## Examples

### Complete Example

```python
from luminoracore import Personality, PersonalityValidator, PersonalityCompiler, LLMProvider

# Load and validate personality
personality = Personality("personalities/dr_luna.json")
validator = PersonalityValidator()
result = validator.validate(personality)

if result.is_valid:
    # Compile for OpenAI
    compiler = PersonalityCompiler()
    openai_result = compiler.compile(personality, LLMProvider.OPENAI)
    
    # Use the compiled prompt
    print(f"OpenAI prompt: {openai_result.prompt}")
    print(f"Token estimate: {openai_result.token_estimate}")
else:
    print("Validation failed:")
    for error in result.errors:
        print(f"  - {error}")
```

## v1.1 Features - Memory & Relationships

LuminoraCore v1.1 introduces advanced memory management and relationship tracking. This section provides a quick overview. For complete v1.1 API documentation, see [v1.1 Features Documentation](v1_1_features.md).

### AffinityManager

Track relationship points and levels:

```python
from luminoracore.core.affinity_manager import AffinityManager

affinity_mgr = AffinityManager(storage)

# Update affinity
affinity_mgr.update_affinity(
    session_id="user_123",
    interaction_type="positive",
    points=5
)

# Get current affinity
affinity = affinity_mgr.get_affinity("user_123")
print(f"Points: {affinity.points}, Level: {affinity.level}")
```

### FactExtractor

Extract and store facts from conversations:

```python
from luminoracore.core.fact_extractor import FactExtractor

fact_extractor = FactExtractor()

# Extract facts
facts = fact_extractor.extract_facts(
    message="I love playing guitar on weekends",
    session_id="user_123"
)

# Query facts
facts = fact_extractor.get_facts(
    session_id="user_123",
    category="hobbies"
)
```

### EpisodicMemoryManager

Store and retrieve memorable moments:

```python
from luminoracore.core.episodic_memory import EpisodicMemoryManager

memory_mgr = EpisodicMemoryManager(storage)

# Create episode
memory_mgr.create_episode(
    session_id="user_123",
    episode_type="achievement",
    content="User completed first project",
    importance=0.9
)

# Query episodes
episodes = memory_mgr.get_episodes(
    session_id="user_123",
    episode_type="achievement",
    min_importance=0.8
)
```

### FeatureFlagManager

Control v1.1 features dynamically:

```python
from luminoracore.core.feature_flags import FeatureFlagManager

flag_mgr = FeatureFlagManager()

# Check if feature is enabled
if flag_mgr.is_enabled("affinity_system"):
    # Use affinity system
    pass

# Configure features
flag_mgr.load_config("config/features_production.json")
```

### MigrationManager

Manage database schema migrations:

```python
from luminoracore.storage.migration_manager import MigrationManager

migration_mgr = MigrationManager(storage)

# Check status
status = migration_mgr.get_status()

# Apply migrations
migration_mgr.migrate_up()

# Rollback
migration_mgr.migrate_down()
```

---

This API reference covers all the main components of LuminoraCore v1.0 and introduces v1.1 features. For complete v1.1 documentation with detailed examples, see [v1.1 Features Documentation](v1_1_features.md).

For more detailed information, see the [Getting Started Guide](getting_started.md) and [Personality Format Documentation](personality_format.md).
