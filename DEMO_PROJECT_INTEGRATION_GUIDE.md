# LuminoraCore v1.1 - Demo Project Integration Guide

**Complete guide for integrating LuminoraCore v1.1 into demo projects and applications.**

---

## 🎯 Quick Demo Setup

### 1. Installation for Demo Projects

```bash
# Install LuminoraCore components
pip install -e luminoracore/
pip install -e luminoracore-sdk-python/

# Set PYTHONPATH for Windows (required for v1.1 modules)
$env:PYTHONPATH = "D:\Proyectos Ereace\LuminoraCoreBase\luminoracore"

# Verify installation
python verify_installation.py
```

### 2. Basic Demo Integration

```python
from luminoracore_sdk import LuminoraCoreClientV11, SQLiteStorageV11

# Initialize client with persistent storage
storage = SQLiteStorageV11("demo.db")
client = LuminoraCoreClientV11(
    storage=storage,
    personality_name="Demo Assistant"
)

# Start conversation with memory
async def demo_conversation():
    # User introduces themselves
    response = await client.process_message(
        session_id="demo_user",
        message="Hi, I'm Sarah and I love playing guitar!"
    )
    print(response)
    
    # AI remembers user in next interaction
    response = await client.process_message(
        session_id="demo_user", 
        message="What do you know about me?"
    )
    print(response)  # AI remembers Sarah and her guitar hobby
```

---

## 🚀 Demo Features Showcase

### ✅ Fully Functional Features for Demos

#### 1. **Memory System** - User Recognition & Fact Storage
```python
# Save user facts
await client.save_fact(
    session_id="user123",
    fact="loves_guitar",
    value="acoustic guitar",
    confidence=0.9
)

# Retrieve facts
facts = await client.get_facts("user123")
print(facts)  # [{"fact": "loves_guitar", "value": "acoustic guitar", ...}]
```

#### 2. **Affinity System** - Relationship Progression
```python
# Check relationship level
affinity = await client.get_affinity("user123", "Assistant")
print(f"Relationship: {affinity['current_level']}")  # stranger → friend → close_friend

# Update relationship through interactions
await client.update_affinity("user123", "Assistant", 5, "positive")
```

#### 3. **Feature Flags** - Dynamic Feature Control
```python
from luminoracore.core.config import FeatureFlagManager

# Load demo configuration
manager = FeatureFlagManager()
manager.load_from_file("config/features_demo.json")

# Check if feature is enabled
if manager.is_enabled("affinity_system"):
    # Use affinity features
    pass
```

#### 4. **Database Migrations** - Schema Management
```python
from luminoracore.storage.migrations import MigrationManager

# Initialize migrations
migration_manager = MigrationManager("demo.db")

# Apply migrations
migration_manager.migrate()

# Verify tables
tables = migration_manager.verify_tables()
print(tables)  # {"user_affinity": True, "user_facts": True, ...}
```

#### 5. **Sentiment Analysis** - Mood Detection
```python
# Analyze user sentiment
sentiment = await client.analyze_sentiment("user123", "I'm feeling great today!")
print(sentiment)  # {"sentiment": "positive", "confidence": 0.85, ...}
```

#### 6. **Personality Evolution** - Dynamic Adaptation
```python
# Evolve personality based on interactions
evolution = await client.evolve_personality("user123", "Assistant")
print(evolution)  # {"changes": [...], "new_traits": [...]}
```

---

## 🗄️ Storage Options for Demos

### 1. **SQLite** (Recommended for Demos)
```python
from luminoracore_sdk import SQLiteStorageV11

storage = SQLiteStorageV11("demo.db")
client = LuminoraCoreClientV11(storage=storage)
```
- ✅ **Pros**: No setup required, persistent data, perfect for demos
- ❌ **Cons**: Single-user, local file

### 2. **In-Memory** (Quick Testing)
```python
from luminoracore_sdk import InMemoryStorageV11

storage = InMemoryStorageV11()
client = LuminoraCoreClientV11(storage=storage)
```
- ✅ **Pros**: Fastest, no files, good for testing
- ❌ **Cons**: Data lost on restart

### 3. **PostgreSQL** (Production Demos)
```python
from luminoracore_sdk import PostgreSQLStorageV11

storage = PostgreSQLStorageV11(
    host="localhost",
    port=5432,
    database="demo_db",
    user="demo_user",
    password="demo_pass"
)
client = LuminoraCoreClientV11(storage=storage)
```

### 4. **DynamoDB** (AWS Demos)
```python
from luminoracore_sdk import DynamoDBStorageV11

storage = DynamoDBStorageV11(
    region_name="us-east-1",
    table_name="demo-table"
)
client = LuminoraCoreClientV11(storage=storage)
```

---

## 🎨 Demo Project Templates

### Template 1: **Simple Chat Demo**
```python
import asyncio
from luminoracore_sdk import LuminoraCoreClientV11, SQLiteStorageV11

async def simple_chat_demo():
    storage = SQLiteStorageV11("chat_demo.db")
    client = LuminoraCoreClientV11(storage=storage)
    
    print("🤖 Chat Demo - Type 'quit' to exit")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
            
        response = await client.process_message("demo_user", user_input)
        print(f"AI: {response}")

if __name__ == "__main__":
    asyncio.run(simple_chat_demo())
```

### Template 2: **Feature Showcase Demo**
```python
import asyncio
from luminoracore_sdk import LuminoraCoreClientV11, SQLiteStorageV11

async def feature_showcase():
    storage = SQLiteStorageV11("showcase.db")
    client = LuminoraCoreClientV11(storage=storage)
    
    # Demonstrate memory
    await client.save_fact("user1", "hobby", "photography", 0.9)
    facts = await client.get_facts("user1")
    print(f"Memory: {facts}")
    
    # Demonstrate affinity
    affinity = await client.get_affinity("user1", "Assistant")
    print(f"Relationship: {affinity}")
    
    # Demonstrate sentiment
    sentiment = await client.analyze_sentiment("user1", "I love this demo!")
    print(f"Sentiment: {sentiment}")

if __name__ == "__main__":
    asyncio.run(feature_showcase())
```

### Template 3: **Multi-User Demo**
```python
import asyncio
from luminoracore_sdk import LuminoraCoreClientV11, PostgreSQLStorageV11

async def multi_user_demo():
    storage = PostgreSQLStorageV11(
        host="localhost",
        database="multi_user_demo"
    )
    client = LuminoraCoreClientV11(storage=storage)
    
    users = ["alice", "bob", "charlie"]
    
    for user in users:
        # Each user has independent memory and relationships
        await client.save_fact(user, "demo_user", "true", 1.0)
        affinity = await client.get_affinity(user, "Assistant")
        print(f"{user}: {affinity['current_level']}")

if __name__ == "__main__":
    asyncio.run(multi_user_demo())
```

---

## 🔧 Configuration for Demos

### 1. **Feature Flags Configuration**
Create `config/features_demo.json`:
```json
{
  "v1_1_features": {
    "episodic_memory": true,
    "mood_system": true,
    "affinity_system": true,
    "personality_evolution": true,
    "advanced_sentiment": true,
    "hierarchical_personalities": false,
    "dynamic_compilation": false,
    "fact_extraction": true,
    "semantic_search": true,
    "session_export": true
  }
}
```

### 2. **Environment Variables**
```bash
# For demo projects
export LUMINORA_DEMO_MODE=true
export LUMINORA_STORAGE_TYPE=sqlite
export LUMINORA_DB_PATH=demo.db
```

### 3. **Logging Configuration**
```python
import logging

# Configure logging for demos
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## 🚨 Troubleshooting Demo Issues

### Issue 1: **Import Errors**
```bash
# Error: ModuleNotFoundError: No module named 'luminoracore.core.config'
# Solution: Set PYTHONPATH
$env:PYTHONPATH = "D:\Proyectos Ereace\LuminoraCoreBase\luminoracore"
```

### Issue 2: **Unicode Errors on Windows**
```python
# Error: UnicodeEncodeError: 'charmap' codec can't encode character
# Solution: Use examples without emojis
python examples/v1_1_feature_flags_demo_no_emojis.py
```

### Issue 3: **Storage Connection Errors**
```python
# Error: Database connection failed
# Solution: Use SQLite for demos
storage = SQLiteStorageV11("demo.db")  # Always works
```

### Issue 4: **Feature Not Enabled**
```python
# Error: Feature 'affinity_system' is not enabled
# Solution: Load demo configuration
manager = FeatureFlagManager()
manager.load_from_file("config/features_demo.json")
```

---

## 📊 Demo Performance Expectations

### Response Times
- **Memory Operations**: 5-15ms
- **Affinity Updates**: 2-8ms  
- **Sentiment Analysis**: 100-500ms (depends on LLM)
- **Database Queries**: 10-50ms

### Storage Requirements
- **SQLite**: ~1MB per 1000 interactions
- **In-Memory**: ~100KB per 1000 interactions
- **PostgreSQL**: ~500KB per 1000 interactions

### Memory Usage
- **Base Framework**: ~50MB
- **Per User Session**: ~1-5MB
- **Per Conversation**: ~100-500KB

---

## 🎯 Demo Best Practices

### 1. **Start Simple**
- Begin with SQLite storage
- Use InMemoryStorageV11 for quick tests
- Enable only essential features

### 2. **Progressive Enhancement**
- Start with basic memory
- Add affinity tracking
- Include sentiment analysis
- Enable personality evolution

### 3. **Error Handling**
```python
try:
    response = await client.process_message(session_id, message)
except Exception as e:
    print(f"Error: {e}")
    # Fallback response
    response = "I'm having trouble processing that. Could you try again?"
```

### 4. **Demo Data**
- Pre-populate with sample users
- Include realistic conversation examples
- Show relationship progression
- Demonstrate memory persistence

---

## 📞 Support for Demo Projects

- **📖 Documentation**: [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
- **🧪 Examples**: [examples/](examples/) directory
- **🐛 Issues**: Report demo-specific issues
- **💬 Community**: GitHub Discussions

---

**Ready to build amazing AI demos with LuminoraCore v1.1! 🚀**
