# 📚 Real SDK v1.1 Documentation - Current API

**Exact documentation of what the SDK v1.1 has - Without assuming methods that don't exist**

---

## 🎯 **IDENTIFIED PROBLEM**

**❌ What was wrong:**
- Assumed methods like `add_fact()`, `store_fact()` that DON'T exist
- Invented parameters like `category`, `limit` that are NOT accepted
- Didn't verify the real SDK v1.1 API

**✅ What DOES exist:**
- `MemoryManagerV11` with limited methods
- `StorageV11Extension` with abstract methods
- `LuminoraCoreClientV11` with specific methods

---

## 🔍 **REAL SDK V1.1 API**

### **1. LuminoraCoreClientV11**
```python
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11

# Initialization
client_v11 = LuminoraCoreClientV11(base_client, storage_v11=storage)

# AVAILABLE METHODS:

# ✅ READ METHODS:
await client_v11.search_memories(user_id, query, top_k=10)
await client_v11.get_facts(user_id, options=None)
await client_v11.get_episodes(user_id, min_importance=None, max_results=None)
await client_v11.get_affinity(user_id, personality_name)
await client_v11.get_relationship_level(user_id, personality_name)
await client_v11.export_personality_snapshot(user_id, personality_name, options=None)

# ✅ WRITE METHODS (NEW):
await client_v11.save_fact(user_id, category, key, value, **kwargs)
await client_v11.save_episode(user_id, episode_type, title, summary, importance, sentiment, **kwargs)
await client_v11.delete_fact(user_id, category, key)
await client_v11.get_memory_stats(user_id)
```

### **2. MemoryManagerV11**
```python
from luminoracore_sdk.session.memory_v1_1 import MemoryManagerV11

# Initialization
memory_manager = MemoryManagerV11(storage_v11=storage)

# AVAILABLE METHODS:
await memory_manager.get_facts(user_id, options=None)
await memory_manager.get_episodes(user_id, min_importance=None, max_results=None)
await memory_manager.get_episode_by_id(episode_id)  # ⚠️ Not implemented
await memory_manager.semantic_search(user_id, query, top_k=10, filters=None)
```

### **3. StorageV11Extension**
```python
from luminoracore_sdk.session.storage_v1_1 import StorageV11Extension

# ABSTRACT METHODS (must be implemented):
await storage.save_affinity(user_id, personality_name, affinity_points, current_level)
await storage.get_affinity(user_id, personality_name)
await storage.save_fact(user_id, category, key, value)
await storage.get_facts(user_id, category=None)
await storage.save_episode(user_id, episode_type, title, summary, importance, sentiment)
await storage.get_episodes(user_id, min_importance=None)
await storage.save_mood(session_id, user_id, current_mood, mood_intensity=1.0)
await storage.get_mood(session_id)
```

### **4. InMemoryStorageV11**
```python
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11

# In-memory implementation (for testing)
storage = InMemoryStorageV11()

# IMPLEMENTED METHODS:
await storage.save_affinity(...)  # ✅ Implemented
await storage.get_affinity(...)   # ✅ Implemented
await storage.save_fact(...)      # ✅ Implemented
await storage.get_facts(...)      # ✅ Implemented
await storage.save_episode(...)   # ✅ Implemented
await storage.get_episodes(...)   # ✅ Implemented
await storage.save_mood(...)      # ✅ Implemented
await storage.get_mood(...)       # ✅ Implemented
```

---

## 🔧 **CORRECT IMPLEMENTATION FOR BACKEND**

### **1. Correct Configuration**
```python
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
from luminoracore_sdk.session.memory_v1_1 import MemoryManagerV11

# Configure storage
storage = InMemoryStorageV11()  # For development
# storage = DynamoDBStorageV11(...)  # For production

# Configure v1.1 client
base_client = LuminoraCoreClient()  # Base client v1.0
client_v11 = LuminoraCoreClientV11(base_client, storage_v11=storage)
```

### **2. Correct Endpoints**
```python
# ✅ CORRECT: Use methods that DO exist
@app.route('/api/v1/memory/session/<session_id>/facts', methods=['GET'])
async def get_memory_facts(session_id):
    facts = await client_v11.get_facts(session_id)
    return jsonify({"facts": facts})

@app.route('/api/v1/memory/session/<session_id>/episodes', methods=['GET'])
async def get_memory_episodes(session_id):
    episodes = await client_v11.get_episodes(session_id)
    return jsonify({"episodes": episodes})

@app.route('/api/v1/memory/session/<session_id>/search', methods=['POST'])
async def search_memory(session_id):
    data = request.json
    query = data.get('query', '')
    results = await client_v11.search_memories(session_id, query)
    return jsonify({"results": results})
```

### **3. ❌ INCORRECT: Methods that DON'T exist**
```python
# ❌ THIS DOES NOT EXIST:
await memory_manager.add_fact(session_id, fact_data)  # ❌ Does not exist
await memory_manager.store_fact(session_id, content, category)  # ❌ Does not exist
await client_v11.save_fact(session_id, fact)  # ❌ Does not exist

# ❌ THESE PARAMETERS DO NOT EXIST:
await memory_manager.get_facts(session_id, category="personal_info")  # ❌ Does not accept category
await memory_manager.get_facts(session_id, limit=10)  # ❌ Does not accept limit
```

---

## 🎯 **CORRECT STRATEGY**

### **Option 1: Use Only Reading (Recommended for Demo)**
```python
# Only use read methods that DO exist
async def handle_memory_readonly(session_id):
    # Read existing facts
    facts = await client_v11.get_facts(session_id)
    
    # Read existing episodes
    episodes = await client_v11.get_episodes(session_id)
    
    # Search in memory
    search_results = await client_v11.search_memories(session_id, "query")
    
    return {
        "facts": facts,
        "episodes": episodes,
        "search_results": search_results
    }
```

### **Option 2: Implement Custom Storage**
```python
class CustomStorageV11(StorageV11Extension):
    """Custom implementation for the backend"""
    
    async def save_fact(self, user_id: str, category: str, key: str, value: Any, **kwargs) -> bool:
        # Implement saving to DynamoDB/SQLite
        pass
    
    async def get_facts(self, user_id: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        # Implement reading from DynamoDB/SQLite
        pass
    
    # ... implement all abstract methods
```

### **Option 3: Simulate Writing (For Demo)**
```python
# Simulate writing using the base v1.0 client
async def simulate_fact_storage(session_id, fact_data):
    # Use the base client to simulate storage
    # This is only for demonstration
    pass
```

---

## 📋 **REAL ENDPOINTS THAT CAN BE IMPLEMENTED**

### **Read Endpoints (✅ Work)**
```bash
GET /api/v1/memory/session/{id}/facts           # Read facts
GET /api/v1/memory/session/{id}/episodes        # Read episodes
POST /api/v1/memory/session/{id}/search         # Search in memory
GET /api/v1/affinity/session/{id}               # Read affinity
GET /api/v1/relationship/session/{id}           # Read relationship level
GET /api/v1/session/{id}/export                 # Export snapshot
```

### **Write Endpoints (⚠️ Require implementation)**
```bash
POST /api/v1/memory/session/{id}/facts          # Save fact (implement)
POST /api/v1/memory/session/{id}/episodes       # Save episode (implement)
POST /api/v1/affinity/session/{id}              # Save affinity (implement)
```

---

## 🚀 **RECOMMENDATION FOR CURSOR AI**

### **Phase 1: Implement Only Reading**
1. Use `InMemoryStorageV11` for development
2. Implement read endpoints that DO exist
3. Test that it works correctly

### **Phase 2: Implement Writing**
1. Create `CustomStorageV11` that extends `StorageV11Extension`
2. Implement abstract methods for DynamoDB/SQLite
3. Add write endpoints

### **Phase 3: Complete Integration**
1. Connect with real database
2. Implement complete persistence
3. Test complete workflow

---

## ✅ **SUMMARY OF WHAT DOES EXIST**

### **✅ Available Classes:**
- `LuminoraCoreClientV11` - v1.1 Client
- `MemoryManagerV11` - Memory management
- `StorageV11Extension` - Storage interface
- `InMemoryStorageV11` - In-memory implementation

### **✅ Read Methods:**
- `get_facts()` - Read facts
- `get_episodes()` - Read episodes
- `search_memories()` - Search in memory
- `get_affinity()` - Read affinity
- `export_personality_snapshot()` - Export snapshot

### **⚠️ Write Methods (Abstract):**
- `save_fact()` - Save fact (implement)
- `save_episode()` - Save episode (implement)
- `save_affinity()` - Save affinity (implement)

---

## 💾 **Storage System - Complete Guide**

### **Storage Types Available:**

#### **1. Memory Storage (Default)**
```python
# In RAM - Lost when app closes
storage_config = StorageConfig(storage_type="memory")
```

**✅ Advantages:**
- Zero setup required
- Very fast
- Perfect for testing and demos

**❌ Disadvantages:**
- Data lost when app closes
- Not persistent
- Not suitable for production

#### **2. JSON File Storage**
```python
# Persistent file on disk
storage_config = StorageConfig(
    storage_type="json",
    connection_string="./sessions/conversations.json"  # File path
)
```

**✅ Advantages:**
- Persistent (saved on disk)
- No database server required
- Portable (can move the file)
- Human-readable format
- Easy backups

**❌ Disadvantages:**
- Slow with many sessions (>1000)
- Not suitable for concurrent access
- No complex queries

**📍 Where JSON files are saved:**
- **Default location**: `./sessions/conversations.json` (relative to your app)
- **Custom location**: You specify the path in `connection_string`
- **Directory**: Automatically created if it doesn't exist

**Example for API Demo:**
```python
# For a demo API, save in a specific folder
storage_config = StorageConfig(
    storage_type="json",
    connection_string="./demo_data/user_sessions.json"
)
# This creates: ./demo_data/user_sessions.json
```

#### **3. SQLite Storage**
```python
# Local database file
storage_config = StorageConfig(
    storage_type="sqlite",
    connection_string="./data/luminoracore.db"
)
```

**✅ Advantages:**
- Persistent database file
- Perfect for mobile apps
- Fast SQL queries
- No server required

**❌ Disadvantages:**
- Not suitable for high concurrency
- No horizontal scaling

#### **4. Redis Storage**
```python
# Redis server
storage_config = StorageConfig(
    storage_type="redis",
    connection_string="redis://localhost:6379"
)
```

**✅ Advantages:**
- Very fast (in-memory)
- Perfect for web applications
- Supports concurrent access
- Automatic TTL

**❌ Disadvantages:**
- Requires Redis server
- More complex setup

#### **5. PostgreSQL/MongoDB Storage**
```python
# Production databases
storage_config = StorageConfig(
    storage_type="postgres",  # or "mongodb"
    connection_string="postgresql://user:pass@localhost:5432/db"
)
```

### **Storage Decision Guide:**

```
┌─────────────────────────────────────────────────────────────┐
│                    STORAGE DECISION TREE                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Need persistence?                                          │
│  ├─ No → Use MEMORY (default)                              │
│  └─ Yes → What type of application?                        │
│       ├─ Demo/Testing → Use JSON FILE                      │
│       ├─ Mobile App → Use SQLITE                           │
│       ├─ Desktop App → Use JSON or SQLITE                  │
│       ├─ Web App (single server) → Use SQLITE or REDIS     │
│       ├─ Web App (multiple servers) → Use REDIS            │
│       └─ Enterprise → Use POSTGRESQL or MONGODB            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **For API Demo Implementation:**

#### **Recommended Setup for Demo API:**
```python
# Option 1: JSON File (Simple)
storage_config = StorageConfig(
    storage_type="json",
    connection_string="./demo_sessions.json"
)

# Option 2: SQLite (Better for demos)
storage_config = StorageConfig(
    storage_type="sqlite",
    connection_string="./demo_data/luminoracore_demo.db"
)
```

#### **File Structure for Demo:**
```
your_api_project/
├── demo_data/
│   ├── luminoracore_demo.db     # SQLite database
│   └── user_sessions.json       # JSON sessions
├── src/
│   └── api.py                   # Your API code
└── requirements.txt
```

### **Storage v1.1 Integration:**

The v1.1 memory system works with ALL storage types:

```python
# Initialize with your chosen storage
storage_config = StorageConfig(storage_type="json", connection_string="./sessions.json")
client = LuminoraCoreClient(storage_config=storage_config)

# Initialize v1.1 extensions
storage_v11 = InMemoryStorageV11()  # For v1.1 features
client_v11 = LuminoraCoreClientV11(client, storage_v11=storage_v11)

# Now you have:
# - v1.0 sessions stored in your chosen backend (JSON/SQLite/etc.)
# - v1.1 memory features (facts, episodes, affinity) in memory
```

---

**🎊 Now Cursor AI knows exactly which methods exist and which ones it must implement!**
