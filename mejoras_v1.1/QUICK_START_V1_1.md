# Quick Start - LuminoraCore v1.1

Get started with v1.1 features in 5 minutes.

## 📦 Installation

```bash
# Install Core (if not already installed)
cd luminoracore
pip install -e .

# Install SDK
cd ../luminoracore-sdk-python
pip install -e .

# Install CLI
cd ../luminoracore-cli
pip install -e .
```

## 🚀 Step 1: Run Migrations

Create v1.1 database tables:

```bash
luminora-cli migrate
```

Output:
```
✅ Migration successful!

📊 Table Verification:
  ✅ user_affinity
  ✅ user_facts
  ✅ episodes
  ✅ session_moods
```

## 🎯 Step 2: Enable Features

Create `config/my_features.json`:

```json
{
  "v1_1_features": {
    "affinity_system": true,
    "hierarchical_personality": true,
    "fact_extraction": false,
    "episodic_memory": false
  }
}
```

Load in code:

```python
from luminoracore.core.config import FeatureFlagManager

FeatureFlagManager.load_from_file("config/my_features.json")
```

## 💡 Step 3: Use Affinity System

```python
from luminoracore.core.relationship.affinity import AffinityManager, AffinityState

# Initialize
manager = AffinityManager()
state = AffinityState(
    user_id="alice",
    personality_name="alicia",
    affinity_points=0,
    current_level="stranger"
)

# Simulate positive interaction
state = manager.update_affinity_state(state, points_delta=5)

print(f"Level: {state.current_level}")
print(f"Points: {state.affinity_points}/100")
```

## 🧠 Step 4: Extract Facts (Optional)

```python
from luminoracore.core.memory.fact_extractor import FactExtractor

extractor = FactExtractor()

# Simple extraction (no LLM)
facts = extractor.extract_sync(
    user_id="alice",
    message="I'm Alice, I love cats"
)

for fact in facts:
    print(f"{fact.key} = {fact.value}")
```

## 🎭 Step 5: Dynamic Personality

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
                "name": "friend",
                "affinity_range": [41, 60],
                "modifiers": {
                    "advanced_parameters": {"formality": -0.2}
                }
            }
        ]
    }
}

# Compile at different levels
extensions = PersonalityV11Extensions.from_personality_dict(personality_dict)
compiler = DynamicPersonalityCompiler(personality_dict, extensions)

# As stranger (affinity=10)
compiled_stranger = compiler.compile(affinity_points=10)
print(f"Formality (stranger): {compiled_stranger['advanced_parameters']['formality']}")

# As friend (affinity=50)
compiled_friend = compiler.compile(affinity_points=50)
print(f"Formality (friend): {compiled_friend['advanced_parameters']['formality']}")
```

## 📊 Step 6: Query Memory (CLI)

```bash
# View facts
luminora-cli memory facts session123

# View episodes
luminora-cli memory episodes session123 --min-importance 7.0

# Export snapshot
luminora-cli snapshot export session123 -o backup.json
```

## 🎮 Run Examples

```bash
# Run demos
python examples/v1_1_affinity_demo.py
python examples/v1_1_memory_demo.py
python examples/v1_1_dynamic_personality_demo.py
```

## 🧪 Run Tests

```bash
# Core tests
cd luminoracore
pytest tests/test_step_*.py -v

# SDK tests
cd ../luminoracore-sdk-python
pytest tests/test_step_*.py -v
```

## 📚 Next Steps

- Read `V1_1_FEATURES_SUMMARY.md` for full feature list
- Explore `STEP_BY_STEP_IMPLEMENTATION.md` for architecture details
- Check `TECHNICAL_ARCHITECTURE.md` for database schema
- Review examples in `examples/v1_1_*.py`

## 🆘 Troubleshooting

**Migration fails:**
```bash
luminora-cli migrate --dry-run  # Preview changes
luminora-cli migrate --status    # Check current version
```

**Import errors:**
```bash
# Make sure packages are installed
pip list | grep luminora
```

**Feature not working:**
```python
# Check feature flag
from luminoracore.core.config import is_enabled
print(is_enabled("affinity_system"))
```

---

**Need help?** See full documentation in `mejoras_v1.1/`

