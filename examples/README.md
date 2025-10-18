# LuminoraCore - Examples

This folder contains practical examples of LuminoraCore v1.0 and v1.1 features.

## 📚 Structure

```
examples/
├── v1.0 (Core Features)
│   ├── luminoracore/examples/basic_usage.py
│   ├── luminoracore/examples/blending_demo.py
│   ├── luminoracore/examples/multi_llm_demo.py
│   ├── luminoracore/examples/performance_demo.py
│   └── luminoracore/examples/personality_switching.py
│
└── v1.1 (Memory & Relationships)
    ├── v1_1_affinity_demo.py
    ├── v1_1_memory_demo.py
    ├── v1_1_dynamic_personality_demo.py
    ├── v1_1_complete_workflow.py ⭐ NEW - Complete workflow
    ├── v1_1_feature_flags_demo.py ⭐ NEW - Feature flags
    ├── v1_1_migrations_demo.py ⭐ NEW - Database migrations
    ├── luminoracore/examples/v1_1_quick_example.py
    └── luminoracore-sdk-python/examples/v1_1_sdk_usage.py
```

---

## 🚀 v1.0 Examples - Core Features

### 1. Basic Usage (`luminoracore/examples/basic_usage.py`)

**Features demonstrated:**
- Load personalities
- Schema validation
- Compilation for multiple providers
- Personality information

**Run:**
```bash
python luminoracore/examples/basic_usage.py
```

**Time:** ~30 seconds

---

### 2. Personality Blending (`luminoracore/examples/blending_demo.py`)

**Features demonstrated:**
- PersonaBlend™ Technology
- Blending strategies (weighted_average, dominant, hybrid)
- Advanced parameters combination

**Run:**
```bash
python luminoracore/examples/blending_demo.py
```

**Time:** ~45 seconds

---

### 3. Multi-LLM Compilation (`luminoracore/examples/multi_llm_demo.py`)

**Features demonstrated:**
- Compilation for 7 LLM providers
- Format comparison
- Token estimation
- Compatibility

**Run:**
```bash
python luminoracore/examples/multi_llm_demo.py
```

**Time:** ~60 seconds

---

### 4. Performance Demo (`luminoracore/examples/performance_demo.py`)

**Features demonstrated:**
- Intelligent cache system
- Performance statistics
- Performance validations
- Optimized compilation

**Run:**
```bash
python luminoracore/examples/performance_demo.py
```

**Time:** ~30 seconds

---

### 5. Personality Switching (`luminoracore/examples/personality_switching.py`)

**Features demonstrated:**
- Load multiple personalities
- Switch between personalities
- Compare characteristics
- Compilation differences

**Run:**
```bash
python luminoracore/examples/personality_switching.py
```

**Time:** ~45 seconds

---

## 🎉 v1.1 Examples - Memory & Relationships

### 1. Affinity System Demo (`v1_1_affinity_demo.py`)

**Features demonstrated:**
- ✨ Affinity points tracking (0-100)
- ✨ Relationship level progression
- ✨ AffinityManager and AffinityState
- ✨ Progress calculation

**Run:**
```bash
python examples/v1_1_affinity_demo.py
```

**v1.1 Features covered:**
- ✅ Affinity Management
- ✅ Hierarchical Personalities (basic)

**Time:** ~10 seconds

---

### 2. Memory System Demo (`v1_1_memory_demo.py`)

**Features demonstrated:**
- 🧠 Automatic fact extraction
- 🧠 Episodic memory
- 🧠 Memory classification
- 🧠 9 fact categories
- 🧠 7 episode types

**Run:**
```bash
python examples/v1_1_memory_demo.py
```

**v1.1 Features covered:**
- ✅ Fact Extraction
- ✅ Episodic Memory
- ✅ Memory Classification

**Time:** ~15 seconds

---

### 3. Dynamic Personality Demo (`v1_1_dynamic_personality_demo.py`)

**Features demonstrated:**
- 🎭 Dynamic compilation based on affinity
- 🎭 Hierarchical personality levels
- 🎭 Parameter modifiers
- 🎭 Automatic adaptation

**Run:**
```bash
python examples/v1_1_dynamic_personality_demo.py
```

**v1.1 Features covered:**
- ✅ Hierarchical Personalities
- ✅ Dynamic Compilation
- ✅ Relationship Levels

**Time:** ~10 seconds

---

### 4. Quick Example (`luminoracore/examples/v1_1_quick_example.py`)

**Features demonstrated:**
- ⚡ Quick overview of all v1.1 features
- ⚡ Simplified synchronous usage
- ⚡ Perfect for getting started

**Run:**
```bash
python luminoracore/examples/v1_1_quick_example.py
```

**v1.1 Features covered:**
- ✅ Affinity (basic)
- ✅ Fact Extraction (basic)
- ✅ Episodic Memory (basic)
- ✅ Classification (basic)

**Time:** ~5 seconds

---

### 5. SDK Complete Usage (`luminoracore-sdk-python/examples/v1_1_sdk_usage.py`)

**Features demonstrated:**
- 🐍 Complete v1.1 SDK
- 🐍 Affinity management via SDK
- 🐍 Fact & Episode management
- 🐍 Memory context for queries
- 🐍 Snapshot export/import
- 🐍 Session analytics

**Run:**
```bash
python luminoracore-sdk-python/examples/v1_1_sdk_usage.py
```

**v1.1 Features covered:**
- ✅ All v1.1 features via SDK
- ✅ InMemoryStorageV11
- ✅ MemoryManagerV11
- ✅ LuminoraCoreClientV11

**Time:** ~20 seconds

---

### 6. 🆕 Complete Workflow ⭐ (`v1_1_complete_workflow.py`)

**Features demonstrated:**
- 🔄 Complete production workflow
- 🔄 Feature flags in real context
- 🔄 Database migrations verified
- 🔄 ALL features integrated
- 🔄 Use case: Complete educational chatbot

**Run:**
```bash
python examples/v1_1_complete_workflow.py
```

**v1.1 Features covered:**
- ✅ Feature Flags (configuration and usage)
- ✅ Database Migrations (status and verification)
- ✅ Affinity System (complete tracking)
- ✅ Fact Extraction (automatic learning)
- ✅ Episodic Memory (important moments)
- ✅ Hierarchical Personalities (adaptation)
- ✅ Dynamic Compilation (real-time)
- ✅ Snapshot Export (complete backup)
- ✅ Analytics (session metrics)

**Time:** ~30 seconds

**💡 This is THE MOST complete example - demonstrates ALL v1.1 integrated**

---

### 7. 🆕 Feature Flags Deep Dive ⭐ (`v1_1_feature_flags_demo.py`)

**Features demonstrated:**
- 🚩 Predefined configurations (minimal, development, production)
- 🚩 Loading and applying features
- 🚩 Usage in code with is_enabled()
- 🚩 Gradual rollout strategy
- 🚩 Rollback without code changes

**Run:**
```bash
python examples/v1_1_feature_flags_demo.py
```

**v1.1 Features covered:**
- ✅ Feature Flag Management
- ✅ Dynamic Configuration
- ✅ Rollout Strategy
- ✅ A/B Testing Setup

**Time:** ~10 seconds

**💡 Essential for understanding feature control in production**

---

### 8. 🆕 Database Migrations Deep Dive ⭐ (`v1_1_migrations_demo.py`)

**Features demonstrated:**
- 🗄️  5 v1.1 migrations explained
- 🗄️  Status verification
- 🗄️  Dry-run mode
- 🗄️  Migration application
- 🗄️  Rollback strategy
- 🗄️  Production best practices

**Run:**
```bash
python examples/v1_1_migrations_demo.py
```

**v1.1 Features covered:**
- ✅ Migration Management
- ✅ Schema Evolution
- ✅ Rollback Strategy
- ✅ Production Best Practices

**Time:** ~10 seconds

**💡 Essential for managing v1.1 database in production**

---

### 9. 🆕 Real Implementations Demo ⭐ (`v1_1_real_implementations_demo_simple.py`)

**Features demonstrated:**
- 🗄️  SQLite storage with REAL persistence
- 🧠  Advanced sentiment analysis with LLM integration
- 🔄  Real personality evolution engine
- 📦  Complete session export with all data
- 📊  Memory statistics and analytics
- ✅  No more mock implementations!

**Run:**
```bash
python examples/v1_1_real_implementations_demo_simple.py
```

**v1.1 Features covered:**
- ✅ Real SQLite Storage Implementation
- ✅ Real Sentiment Analysis with LLM
- ✅ Real Personality Evolution Engine
- ✅ Complete Session Export
- ✅ Memory Statistics
- ✅ Production-Ready Framework

**Time:** ~15 seconds

**💡 Demonstrates 100% complete framework with REAL implementations**

---

### 10. 🆕 Simplified Examples (SDK v1.1) ⭐

#### Affinity Demo (`v1_1_affinity_demo_simple.py`)
**Features demonstrated:**
- 💝  Affinity point tracking
- 📈  Level progression simulation
- 🔄  Update affinity functionality
- 📊  Get affinity state

**Run:**
```bash
python examples/v1_1_affinity_demo_simple.py
```

#### Memory Demo (`v1_1_memory_demo_simple.py`)
**Features demonstrated:**
- 🧠  Fact management (save/get)
- 📖  Episode management (save/get)
- 📊  Memory statistics
- 🔍  Search functionality

**Run:**
```bash
python examples/v1_1_memory_demo_simple.py
```

#### Dynamic Personality Demo (`v1_1_dynamic_personality_demo_simple.py`)
**Features demonstrated:**
- 🎭  Personality evolution simulation
- 💝  Affinity level progression
- 🔄  Evolution analysis
- 📦  Session management

**Run:**
```bash
python examples/v1_1_dynamic_personality_demo_simple.py
```

**💡 All simplified examples work with SDK v1.1 and InMemoryStorageV11**

---

## 📊 v1.1 Features Coverage

| Feature | Main Example | Additional Examples |
|---------|--------------|-------------------|
| **Affinity Management** | v1_1_affinity_demo.py | v1_1_complete_workflow.py, v1_1_sdk_usage.py |
| **Fact Extraction** | v1_1_memory_demo.py | v1_1_complete_workflow.py, v1_1_quick_example.py |
| **Episodic Memory** | v1_1_memory_demo.py | v1_1_complete_workflow.py, v1_1_quick_example.py |
| **Memory Classification** | v1_1_memory_demo.py | v1_1_complete_workflow.py, v1_1_quick_example.py |
| **Hierarchical Personalities** | v1_1_dynamic_personality_demo.py | v1_1_complete_workflow.py |
| **Dynamic Compilation** | v1_1_dynamic_personality_demo.py | v1_1_complete_workflow.py |
| **Feature Flags** | v1_1_feature_flags_demo.py ⭐ | v1_1_complete_workflow.py |
| **Database Migrations** | v1_1_migrations_demo.py ⭐ | v1_1_complete_workflow.py |
| **Snapshot Export/Import** | v1_1_sdk_usage.py | v1_1_complete_workflow.py |
| **Complete Integration** | v1_1_complete_workflow.py ⭐ | - |

|| **Real Implementations** | v1_1_real_implementations_demo_simple.py ⭐ | - |
|| **Simplified Examples** | v1_1_affinity_demo_simple.py, v1_1_memory_demo_simple.py, v1_1_dynamic_personality_demo_simple.py ⭐ | - |

**✅ 100% of v1.1 features covered with examples**

---

## 🎯 Quick Start Guide

### For new users (v1.0):
```bash
# 1. Basic usage
python luminoracore/examples/basic_usage.py

# 2. Blending
python luminoracore/examples/blending_demo.py

# 3. Multi-LLM
python luminoracore/examples/multi_llm_demo.py
```

### For advanced users (v1.1):
```bash
# 1. Quick overview of all features
python luminoracore/examples/v1_1_quick_example.py

# 2. Deep dive into specific features
python examples/v1_1_affinity_demo.py        # Affinity
python examples/v1_1_memory_demo.py          # Memory
python examples/v1_1_dynamic_personality_demo.py  # Hierarchical

# 3. Production management
python examples/v1_1_feature_flags_demo.py   # Feature flags
python examples/v1_1_migrations_demo.py      # Migrations

# 4. ⭐ Complete workflow (ALL integrated)
python examples/v1_1_complete_workflow.py

# 5. ⭐ Real implementations (100% functional)
python examples/v1_1_real_implementations_demo_simple.py

# 6. ⭐ Simplified examples (SDK v1.1)
python examples/v1_1_affinity_demo_simple.py        # Affinity system
python examples/v1_1_memory_demo_simple.py          # Memory system
python examples/v1_1_dynamic_personality_demo_simple.py  # Personality evolution
```

### For SDK developers:
```bash
# Complete v1.1 SDK
python luminoracore-sdk-python/examples/v1_1_sdk_usage.py
```

---

## 🔧 Requirements

### For v1.0:
```bash
pip install -e luminoracore/
```

### For v1.1:
```bash
# 1. Install core
pip install -e luminoracore/

# 2. Setup database
./scripts/setup-v1_1-database.sh  # Linux/Mac
.\scripts\setup-v1_1-database.ps1  # Windows

# 3. (Optional) Install SDK
pip install -e luminoracore-sdk-python/
```

---

## 📝 Notes

### Compatibility
- ✅ All v1.0 examples work without changes
- ✅ v1.1 is 100% backward compatible
- ✅ Feature flags allow enabling/disabling v1.1

### Database
- v1.0: No database required
- v1.1: Database setup required for memory features

### API Keys
- Some examples may require LLM provider API keys
- Configure appropriate environment variables

---

## 🐛 Troubleshooting

### "Module not found"
```bash
# Make sure you're in the root directory
cd /path/to/LuminoraCoreBase
python examples/v1_1_affinity_demo.py
```

### "Database not found"
```bash
# Run v1.1 setup
./scripts/setup-v1_1-database.sh
```

### "Feature not enabled"
```python
# Check feature flags
from luminoracore.core.config import FeatureFlagManager
FeatureFlagManager.load_from_file("config/features_development.json")
```

---

## 📚 Additional Documentation

- **[v1.1 Features Guide](../luminoracore/docs/v1_1_features.md)** - Complete v1.1 features guide
- **[Quick Start v1.1](../mejoras_v1.1/QUICK_START_V1_1.md)** - 5-minute tutorial
- **[Best Practices](../luminoracore/docs/best_practices.md)** - v1.1 best practices
- **[API Reference](../luminoracore/docs/api_reference.md)** - Complete API reference

---

**Last updated:** October 2025 (v1.1 production ready)

**Status:** ✅ All examples verified and working
