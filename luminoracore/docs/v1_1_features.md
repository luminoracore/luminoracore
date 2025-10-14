# LuminoraCore v1.1 Features

**New in version 1.1!** This document describes the advanced memory and relationship features added in v1.1.

## Overview

Version 1.1 introduces a powerful memory and relationship system that enables AI personalities to:
- **Remember facts** about users across conversations
- **Track relationship progression** through affinity levels
- **Detect memorable moments** and store them as episodes
- **Adapt behavior** dynamically based on relationship level

All v1.1 features are **100% backward compatible** with v1.0 and are **opt-in** via feature flags.

## Key Features

### 1. Hierarchical Personality System

Personalities can now evolve through relationship levels:

```python
from luminoracore.core.personality_v1_1 import PersonalityV11Extensions
from luminoracore.core.compiler_v1_1 import DynamicPersonalityCompiler

# Load personality with hierarchical config
personality_dict = {
    "persona": {"name": "Alicia"},
    "advanced_parameters": {"empathy": 0.9, "formality": 0.5},
    "hierarchical_config": {
        "enabled": True,
        "relationship_levels": [
            {
                "name": "stranger",
                "affinity_range": [0, 20],
                "modifiers": {
                    "advanced_parameters": {"formality": 0.2}
                }
            },
            {
                "name": "friend",
                "affinity_range": [41, 60],
                "modifiers": {
                    "advanced_parameters": {"formality": -0.2}
                }
            }
        ]
    }
}

# Parse extensions
extensions = PersonalityV11Extensions.from_personality_dict(personality_dict)

# Compile dynamically based on affinity
compiler = DynamicPersonalityCompiler(personality_dict, extensions)
compiled_stranger = compiler.compile(affinity_points=10)
compiled_friend = compiler.compile(affinity_points=50)
```

**Default Levels:**
- `stranger` (0-20 points) - Formal, reserved
- `acquaintance` (21-40 points) - Polite, cautious
- `friend` (41-60 points) - Casual, comfortable
- `close_friend` (61-80 points) - Playful, intimate
- `soulmate` (81-100 points) - Deep connection

### 2. Affinity Management

Track and update relationship points:

```python
from luminoracore.core.relationship.affinity import AffinityManager, AffinityState

# Initialize manager
manager = AffinityManager()

# Create initial state
state = AffinityState(
    user_id="user123",
    personality_name="alicia",
    affinity_points=0,
    current_level="stranger"
)

# Update after positive interaction
state = manager.update_affinity_state(state, points_delta=5)

# Check for level change
if state.current_level != "stranger":
    print(f"Progressed to: {state.current_level}")

# Get progress information
progress = manager.get_level_progress(state)
print(f"Progress: {progress['progress_in_level']*100:.0f}%")
print(f"Points to next level: {progress['points_to_next_level']}")
```

### 3. Fact Extraction

Automatically learn facts from conversations:

```python
from luminoracore.core.memory.fact_extractor import FactExtractor

# With LLM provider
extractor = FactExtractor(llm_provider=provider)
facts = await extractor.extract_from_message(
    user_id="user123",
    message="I'm Diego, I'm 28 and work in IT. I love anime!"
)

for fact in facts:
    print(f"{fact.category} - {fact.key}: {fact.value}")
    print(f"  Confidence: {fact.confidence:.2f}")
```

**Fact Categories:**
- `personal_info` - Name, age, location, etc.
- `preferences` - Likes, dislikes, interests
- `relationships` - Family, friends
- `hobbies` - Activities, pastimes
- `goals` - Aspirations, plans
- `health` - Medical, wellness
- `work` - Career, profession
- `events` - Significant occurrences

### 4. Episodic Memory

Store memorable moments:

```python
from luminoracore.core.memory.episodic import EpisodicMemoryManager

manager = EpisodicMemoryManager()

# Create episode
episode = manager.create_episode(
    user_id="user123",
    episode_type="emotional_moment",
    title="Loss of pet",
    summary="User's dog passed away",
    sentiment="very_negative",
    tags=["sad", "pet"]
)

print(f"Importance: {episode.importance}/10")
print(f"Should store: {manager.should_store_episode(episode.importance)}")
```

**Episode Types:**
- `emotional_moment` - Strong emotions
- `milestone` - Significant events
- `confession` - Personal revelations
- `achievement` - Accomplishments
- `conflict` - Disagreements
- `bonding` - Connection moments

### 5. Memory Classification

Organize memories by importance:

```python
from luminoracore.core.memory.classifier import MemoryClassifier

classifier = MemoryClassifier()

# Classify fact
classification = classifier.classify_fact(fact)
print(f"Importance: {classification.importance_level}")

# Get top episodes
top_episodes = classifier.get_top_n_episodes(episodes, n=5)

# Filter by category
personal_facts = classifier.get_facts_by_category(facts, "personal_info")
```

**Importance Levels:**
- `critical` (9-10) - Extremely important
- `high` (7-8) - Very important
- `medium` (5-6) - Moderately important
- `low` (3-4) - Somewhat important
- `trivial` (0-2) - Minor importance

### 6. Feature Flags

Control feature activation:

```python
from luminoracore.core.config import FeatureFlagManager, get_features, is_enabled

# Load from JSON
FeatureFlagManager.load_from_file("config/features.json")

# Check if enabled
if is_enabled("affinity_system"):
    # Use affinity features
    pass

# Get all features
features = get_features()
print(f"Affinity enabled: {features.affinity_system}")
print(f"Fact extraction enabled: {features.fact_extraction}")
```

**Available Features:**
- `episodic_memory` - Memorable moments
- `semantic_search` - Vector search
- `fact_extraction` - Automatic learning
- `hierarchical_personality` - Relationship levels
- `mood_system` - Mood states
- `affinity_system` - Point tracking
- `conversation_analytics` - Metrics
- `snapshot_export` - State export

### 7. Database Migrations

Manage v1.1 database tables:

```bash
# Run migrations
luminora-cli migrate

# Check status
luminora-cli migrate --status

# Preview changes
luminora-cli migrate --dry-run

# View history
luminora-cli migrate --history
```

### 8. CLI Tools

New commands for v1.1:

```bash
# Query facts
luminora-cli memory facts session123 --category personal_info

# Query episodes
luminora-cli memory episodes session123 --min-importance 7.0

# Export snapshot
luminora-cli snapshot export session123 -o backup.json

# Import snapshot
luminora-cli snapshot import backup.json --user-id user123
```

## Database Schema

### New Tables

**user_affinity:**
- Tracks relationship points and levels
- Fields: user_id, personality_name, affinity_points, current_level

**user_facts:**
- Stores learned facts
- Fields: user_id, category, key, value, confidence

**episodes:**
- Memorable moments
- Fields: user_id, episode_type, title, summary, importance, sentiment

**session_moods:**
- Current mood states
- Fields: session_id, user_id, current_mood, mood_intensity

**schema_migrations:**
- Migration tracking
- Fields: version, name, applied_at

## SDK Extensions

### Storage v1.1

```python
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11

storage = InMemoryStorageV11()

# Save/get affinity
await storage.save_affinity("user1", "alicia", 50, "friend")
affinity = await storage.get_affinity("user1", "alicia")

# Save/get facts
await storage.save_fact("user1", "personal_info", "name", "Diego")
facts = await storage.get_facts("user1", category="personal_info")

# Save/get episodes
await storage.save_episode("user1", "milestone", "First chat", "...", 7.0, "positive")
episodes = await storage.get_episodes("user1", min_importance=5.0)
```

### Memory Manager v1.1

```python
from luminoracore_sdk.session.memory_v1_1 import MemoryManagerV11

manager = MemoryManagerV11(storage_v11=storage)

# Get facts
facts = await manager.get_facts("user1", options={"category": "personal_info"})

# Get episodes
episodes = await manager.get_episodes("user1", min_importance=7.0)

# Get context for query
context = await manager.get_context_for_query("user1", "tell me about Diego")
```

### Client v1.1

```python
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11

client_v11 = LuminoraCoreClientV11(base_client, storage_v11=storage)

# Memory operations
facts = await client_v11.get_facts("user1")
episodes = await client_v11.get_episodes("user1", min_importance=7.0)

# Affinity operations
affinity = await client_v11.get_affinity("user1", "alicia")
await client_v11.update_affinity("user1", "alicia", points_delta=5, interaction_type="positive")

# Snapshot operations
snapshot = await client_v11.export_snapshot("session123")
```

## Examples

See the following example files:

- `examples/v1_1_affinity_demo.py` - Affinity system demo
- `examples/v1_1_memory_demo.py` - Memory system demo
- `examples/v1_1_dynamic_personality_demo.py` - Dynamic compilation demo

## Migration Guide

### From v1.0 to v1.1

1. **Install/Update:**
   ```bash
   cd luminoracore
   pip install -e .
   ```

2. **Run Migrations:**
   ```bash
   luminora-cli migrate
   ```

3. **Enable Features (optional):**
   ```python
   from luminoracore.core.config import FeatureFlagManager
   
   FeatureFlagManager.load_from_file("config/features_development.json")
   ```

4. **Update Personality JSON (optional):**
   Add hierarchical config to your personality:
   ```json
   {
     "persona": {...},
     "hierarchical_config": {
       "enabled": true,
       "relationship_levels": [...]
     }
   }
   ```

5. **Use v1.1 Features:**
   ```python
   from luminoracore.core.relationship.affinity import AffinityManager
   
   manager = AffinityManager()
   # Use affinity features
   ```

### Backward Compatibility

**All v1.0 code continues to work unchanged:**

```python
# v1.0 code still works
from luminoracore import Personality, PersonalityValidator

personality = Personality("personality.json")
validator = PersonalityValidator()
result = validator.validate(personality)
```

**v1.1 features are opt-in:**
- If feature flags are disabled, v1.1 features are not used
- If hierarchical_config is not in JSON, personality works as v1.0
- All new tables are optional

## Best Practices

### 1. Enable Features Gradually

Start with core features:
```json
{
  "affinity_system": true,
  "hierarchical_personality": true,
  "fact_extraction": false,
  "episodic_memory": false
}
```

### 2. Monitor Performance

Check database and LLM usage:
```python
# Fact extraction uses LLM
if is_enabled("fact_extraction"):
    # Monitor API usage
    pass
```

### 3. Test Thoroughly

Test with real users before full rollout:
```python
# Start with test users
test_users = ["user_test_1", "user_test_2"]
```

### 4. Configure Appropriately

Set thresholds based on your needs:
```python
# Episode importance threshold
episode_manager = EpisodicMemoryManager(importance_threshold=6.0)

# Fact confidence threshold
fact_extractor = FactExtractor(confidence_threshold=0.8)
```

## Documentation

- **Quick Start:** `mejoras_v1.1/QUICK_START_V1_1.md`
- **Features Summary:** `mejoras_v1.1/V1_1_FEATURES_SUMMARY.md`
- **Implementation Plan:** `mejoras_v1.1/STEP_BY_STEP_IMPLEMENTATION.md`
- **Technical Architecture:** `mejoras_v1.1/TECHNICAL_ARCHITECTURE.md`

## Support

- Examples: See `examples/v1_1_*.py`
- Tests: See `*/tests/test_step_*.py`
- Issues: GitHub issue tracker

---

**Version:** 1.1.0  
**Status:** Production Ready  
**Backward Compatible:** 100%

