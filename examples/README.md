# LuminoraCore v1.1 - Examples

This folder contains **ONE PROFESSIONAL EXAMPLE** that demonstrates all LuminoraCore v1.1 features.

## 📚 Structure

```
examples/
├── luminoracore_v1_1_complete_demo.py  ⭐ THE ONLY EXAMPLE YOU NEED
└── README.md                           ⭐ This file
```

---

## 🚀 The Complete Demo

### `luminoracore_v1_1_complete_demo.py`

**The ONLY example you need to understand LuminoraCore v1.1**

**Features demonstrated:**
- ✅ **Flexible Storage** - Works with ANY database (DynamoDB, SQLite, PostgreSQL, Redis, MongoDB)
- ✅ **Memory System** - Facts, episodes, affinity tracking
- ✅ **Conversation Memory** - Context-aware responses that remember everything
- ✅ **Auto-configuration** - No hardcoding, works with existing databases
- ✅ **Professional** - Clean, organized, working code

**Run:**
```bash
python examples/luminoracore_v1_1_complete_demo.py
```

**Time:** ~30 seconds

**What it shows:**
1. **Flexible Storage** - How to use ANY database with custom configurations
2. **Memory System** - How facts, episodes, and affinity work together
3. **Conversation Memory** - How conversations maintain context across messages
4. **Auto-configuration** - How the framework adapts to your existing setup

---

## 🎯 Why Only One Example?

### ❌ **Before (Problematic):**
- 20+ example files
- Multiple versions of the same thing
- Broken imports and errors
- Confusing and unprofessional
- Users didn't know which one to use

### ✅ **Now (Professional):**
- **ONE** complete example
- **ALL** features demonstrated
- **WORKING** code with no errors
- **CLEAR** and easy to understand
- **PROFESSIONAL** and organized

---

## 🛠️ Requirements

### For v1.1:
```bash
# 1. Install core
pip install -e luminoracore/

# 2. Install SDK
pip install -e luminoracore-sdk-python/

# 3. Run the demo
python examples/luminoracore_v1_1_complete_demo.py
```

---

## 📝 What You'll Learn

### 1. **Flexible Storage**
```python
# Works with ANY database
storage = FlexibleSQLiteStorageV11(
    database_path="./my_database.sqlite",
    facts_table="my_facts",
    affinity_table="my_affinity"
)

# Or DynamoDB with existing table
storage = FlexibleDynamoDBStorageV11(
    table_name="my-existing-table",
    region_name="us-east-1"
)
```

### 2. **Memory System**
```python
# Save facts
await client.save_fact(session_id, "personal_info", "name", "Carlos", 0.95)

# Save episodes
await client.save_episode(session_id, "milestone", "First conversation", "User and AI met", 8.0, "positive")

# Update affinity
await client.update_affinity(session_id, "assistant", 5, "positive")
```

### 3. **Conversation Memory**
```python
# Send message with full context
response = await client.send_message_with_memory(
    session_id=session_id,
    user_message="Hello, I'm Carlos from Madrid",
    personality_name="assistant",
    provider_config=provider_config
)
```

### 4. **Auto-configuration**
```python
# Environment variables
os.environ["LUMINORA_STORAGE_TYPE"] = "sqlite_flexible"
os.environ["LUMINORA_SQLITE_PATH"] = "./my_database.sqlite"

# Configuration file
# luminora_config.json with your database settings
```

---

## 🎯 Key Takeaways

1. **✅ Flexible** - Works with ANY database configuration
2. **✅ Professional** - Clean, organized, working code
3. **✅ Complete** - All features demonstrated in one place
4. **✅ Auto-configurable** - No hardcoding required
5. **✅ Enterprise-ready** - Production-quality implementation

---

## 🆘 Troubleshooting

### "Module not found" errors
```bash
# Make sure you're in the project root
cd /path/to/LuminoraCoreBase

# Install packages in development mode
pip install -e luminoracore/
pip install -e luminoracore-sdk-python/
```

### "ImportError" errors
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Make sure luminoracore-sdk-python is in your path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/luminoracore-sdk-python"
```

---

## 📚 Additional Resources

- **[Complete Documentation](../DOCUMENTATION_INDEX.md)** - All documentation
- **[API Reference](../SDK_V1_1_ACTUAL_API_DOCUMENTATION.md)** - Complete API reference
- **[Flexible Storage Guide](../ALL_DATABASES_FLEXIBLE_CONFIGURATION_GUIDE.md)** - Database configuration

---

**Last updated:** October 2025 (v1.1 production ready)

**Status:** ✅ One professional example, fully working