# LuminoraCore Architecture Restructure Plan
## Correcting the Dependency Hierarchy

**Current Problem**: Core and CLI depend on SDK (incorrect architecture)  
**Target Solution**: SDK depends on Core (correct architecture)

---

## 🎯 **Current Architecture Issues**

### **❌ Current (Incorrect) Architecture:**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LuminoraCore  │◄───┤   SDK Python    │◄───┤      CLI        │
│                 │    │                 │    │                 │
│ • Depends on SDK│    │ • Depends on SDK│    │ • Depends on SDK│
│ • Not standalone│    │ • Not standalone│    │ • Not standalone│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **✅ Target (Correct) Architecture:**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LuminoraCore  │    │   SDK Python    │    │      CLI        │
│                 │    │                 │    │                 │
│ • Standalone    │◄───┤ • Uses Core     │◄───┤ • Uses Core     │
│ • Core Engine   │    │ • Client Layer  │    │ • Tools Layer   │
│ • Memory System │    │ • API Wrapper   │    │ • Management    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🏗 **Correct Architecture Design**

### **Core Layer (luminoracore/)**
- **Personality Engine**: Core personality management and evolution
- **Memory System**: Facts, episodes, affinity tracking
- **Storage Abstractions**: Database-agnostic storage interfaces
- **Evolution Engine**: Personality adaptation algorithms
- **Core Types**: Base data structures and models

### **SDK Layer (luminoracore-sdk-python/)**
- **Client Implementation**: High-level client for applications
- **Storage Implementations**: Concrete storage implementations
- **API Wrappers**: Convenient wrappers around core functionality
- **Integration Helpers**: Easy integration with existing systems

### **CLI Layer (luminoracore-cli/)**
- **Management Tools**: Database and memory management
- **Development Tools**: Testing and validation tools
- **Deployment Tools**: Installation and configuration tools
- **Monitoring Tools**: System health and analytics

---

## 📋 **Restructure Tasks**

### **Phase 1: Core Independence (Priority: HIGH)**

#### **1.1 Move Core Functionality to luminoracore/**
```bash
# Move these from SDK to Core:
luminoracore-sdk-python/luminoracore_sdk/core/ → luminoracore/luminoracore/core/
luminoracore-sdk-python/luminoracore_sdk/memory/ → luminoracore/luminoracore/memory/
luminoracore-sdk-python/luminoracore_sdk/storage/ → luminoracore/luminoracore/storage/
luminoracore-sdk-python/luminoracore_sdk/evolution/ → luminoracore/luminoracore/evolution/
```

#### **1.2 Create Core Interfaces**
```python
# luminoracore/luminoracore/interfaces/
├── storage_interface.py      # Abstract storage interface
├── memory_interface.py       # Abstract memory interface
├── personality_interface.py  # Abstract personality interface
└── evolution_interface.py     # Abstract evolution interface
```

#### **1.3 Core Dependencies**
```python
# luminoracore/requirements.txt should contain:
# - Only core dependencies (no SDK dependencies)
# - Database drivers (sqlite3, psycopg2, boto3, etc.)
# - Basic utilities (datetime, json, etc.)
# - NO SDK-specific dependencies
```

### **Phase 2: SDK Refactoring (Priority: HIGH)**

#### **2.1 SDK Should Import from Core**
```python
# luminoracore-sdk-python/luminoracore_sdk/client.py
from luminoracore import PersonalityEngine, MemorySystem, StorageInterface
from luminoracore.storage import SQLiteStorage, DynamoDBStorage
from luminoracore.memory import FactExtractor, EpisodeManager
```

#### **2.2 SDK Storage Implementations**
```python
# luminoracore-sdk-python/luminoracore_sdk/storage/
├── sqlite_storage.py         # SQLite implementation
├── dynamodb_storage.py       # DynamoDB implementation
├── postgresql_storage.py     # PostgreSQL implementation
├── redis_storage.py          # Redis implementation
└── mongodb_storage.py        # MongoDB implementation
```

#### **2.3 SDK Client Layer**
```python
# luminoracore-sdk-python/luminoracore_sdk/client.py
class LuminoraCoreClient:
    def __init__(self, storage: StorageInterface):
        self.core = PersonalityEngine()
        self.memory = MemorySystem(storage)
        self.storage = storage
```

### **Phase 3: CLI Refactoring (Priority: MEDIUM)**

#### **3.1 CLI Should Use Core Directly**
```python
# luminoracore-cli/luminoracore_cli/commands/
from luminoracore import PersonalityEngine, MemorySystem
from luminoracore.storage import get_storage_implementation
```

#### **3.2 CLI Management Tools**
```python
# luminoracore-cli/luminoracore_cli/management/
├── memory_manager.py         # Direct core memory management
├── database_manager.py       # Direct core database operations
├── personality_manager.py    # Direct core personality operations
└── analytics_manager.py      # Direct core analytics
```

### **Phase 4: Dependency Cleanup (Priority: MEDIUM)**

#### **4.1 Remove Circular Dependencies**
```bash
# Remove these dependencies:
# - Core should NOT import from SDK
# - CLI should NOT import from SDK
# - SDK should ONLY import from Core
```

#### **4.2 Update Import Statements**
```python
# Before (incorrect):
from luminoracore_sdk import LuminoraCoreClient

# After (correct):
from luminoracore import PersonalityEngine, MemorySystem
from luminoracore_sdk import LuminoraCoreClient  # Only for SDK users
```

---

## 🔧 **Implementation Steps**

### **Step 1: Create Core Interfaces**
```python
# luminoracore/luminoracore/interfaces/storage_interface.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

class StorageInterface(ABC):
    @abstractmethod
    async def save_fact(self, user_id: str, category: str, key: str, value: Any, confidence: float) -> bool:
        pass
    
    @abstractmethod
    async def get_facts(self, user_id: str, category: Optional[str] = None) -> List[Dict]:
        pass
    
    @abstractmethod
    async def save_episode(self, user_id: str, episode_type: str, title: str, summary: str, importance: float, sentiment: str) -> bool:
        pass
    
    @abstractmethod
    async def get_episodes(self, user_id: str, min_importance: Optional[float] = None) -> List[Dict]:
        pass
    
    @abstractmethod
    async def update_affinity(self, user_id: str, personality_name: str, points_delta: int, interaction_type: str) -> Dict:
        pass
    
    @abstractmethod
    async def get_affinity(self, user_id: str, personality_name: str) -> Optional[Dict]:
        pass
```

### **Step 2: Move Core Classes**
```python
# luminoracore/luminoracore/core/personality_engine.py
class PersonalityEngine:
    def __init__(self):
        self.personalities = {}
        self.evolution_engine = EvolutionEngine()
    
    def load_personality(self, name: str, data: Dict) -> None:
        # Core personality loading logic
        pass
    
    def evolve_personality(self, user_id: str, personality_name: str, interaction_data: Dict) -> Dict:
        # Core personality evolution logic
        pass
```

### **Step 3: Create SDK Wrappers**
```python
# luminoracore-sdk-python/luminoracore_sdk/client.py
from luminoracore import PersonalityEngine, MemorySystem
from luminoracore.interfaces import StorageInterface

class LuminoraCoreClient:
    def __init__(self, storage: StorageInterface):
        self.core_engine = PersonalityEngine()
        self.memory_system = MemorySystem(storage)
        self.storage = storage
    
    async def save_fact(self, user_id: str, category: str, key: str, value: Any, confidence: float = 0.8) -> bool:
        return await self.storage.save_fact(user_id, category, key, value, confidence)
    
    async def get_facts(self, user_id: str, category: Optional[str] = None) -> List[Dict]:
        return await self.storage.get_facts(user_id, category)
```

### **Step 4: Update CLI to Use Core**
```python
# luminoracore-cli/luminoracore_cli/commands/memory.py
from luminoracore import MemorySystem
from luminoracore.storage import get_storage_implementation

class MemoryCommand:
    def __init__(self, storage_config: Dict):
        self.storage = get_storage_implementation(storage_config)
        self.memory = MemorySystem(self.storage)
    
    async def list_facts(self, user_id: str) -> List[Dict]:
        return await self.memory.get_facts(user_id)
```

---

## 📦 **Package Structure After Restructure**

### **luminoracore/ (Core Package)**
```
luminoracore/
├── __init__.py
├── core/
│   ├── personality_engine.py
│   ├── memory_system.py
│   └── evolution_engine.py
├── interfaces/
│   ├── storage_interface.py
│   ├── memory_interface.py
│   └── personality_interface.py
├── storage/
│   ├── base_storage.py
│   └── in_memory_storage.py
├── memory/
│   ├── fact_extractor.py
│   ├── episode_manager.py
│   └── affinity_tracker.py
└── requirements.txt
```

### **luminoracore-sdk-python/ (SDK Package)**
```
luminoracore-sdk-python/
├── __init__.py
├── client.py
├── storage/
│   ├── sqlite_storage.py
│   ├── dynamodb_storage.py
│   ├── postgresql_storage.py
│   └── redis_storage.py
├── types/
│   ├── provider.py
│   └── session.py
└── requirements.txt
```

### **luminoracore-cli/ (CLI Package)**
```
luminoracore-cli/
├── __init__.py
├── commands/
│   ├── memory.py
│   ├── database.py
│   └── personality.py
├── management/
│   ├── memory_manager.py
│   └── database_manager.py
└── requirements.txt
```

---

## 🎯 **Migration Strategy**

### **Phase 1: Preparation (Week 1)**
1. **Create Core Interfaces**: Define all abstract interfaces
2. **Move Core Classes**: Move core functionality to luminoracore/
3. **Update Core Dependencies**: Remove SDK dependencies from core
4. **Test Core Independence**: Ensure core works standalone

### **Phase 2: SDK Refactoring (Week 2)**
1. **Update SDK Imports**: Change SDK to import from core
2. **Create SDK Wrappers**: Create client wrappers around core
3. **Update SDK Storage**: Move storage implementations to SDK
4. **Test SDK Functionality**: Ensure SDK still works

### **Phase 3: CLI Refactoring (Week 3)**
1. **Update CLI Imports**: Change CLI to import from core
2. **Update CLI Commands**: Update all CLI commands to use core
3. **Test CLI Functionality**: Ensure CLI still works
4. **Update Documentation**: Update all documentation

### **Phase 4: Testing & Validation (Week 4)**
1. **Integration Testing**: Test all components together
2. **Performance Testing**: Ensure no performance regression
3. **Documentation Update**: Update all documentation
4. **Release Preparation**: Prepare for release

---

## ✅ **Success Criteria**

### **Architecture Goals:**
- ✅ Core is completely independent
- ✅ SDK depends only on Core
- ✅ CLI depends only on Core
- ✅ No circular dependencies
- ✅ Clear separation of concerns

### **Functionality Goals:**
- ✅ All existing functionality preserved
- ✅ No breaking changes for end users
- ✅ Performance maintained or improved
- ✅ Documentation updated
- ✅ Tests passing

### **Maintainability Goals:**
- ✅ Clear dependency hierarchy
- ✅ Easy to add new storage implementations
- ✅ Easy to add new features to core
- ✅ Easy to create new SDKs for other languages
- ✅ Easy to extend CLI functionality

---

## 🚀 **Benefits of Correct Architecture**

### **For Core Development:**
- **Independence**: Core can be developed without SDK dependencies
- **Testing**: Core can be tested in isolation
- **Performance**: Core can be optimized without SDK concerns
- **Reusability**: Core can be used by multiple SDKs

### **For SDK Development:**
- **Clarity**: SDK is clearly a client layer over core
- **Flexibility**: SDK can provide different APIs for different use cases
- **Maintainability**: SDK changes don't affect core
- **Extensibility**: Easy to add new SDK features

### **For CLI Development:**
- **Direct Access**: CLI has direct access to core functionality
- **Performance**: CLI operations are faster without SDK overhead
- **Flexibility**: CLI can access core features not exposed in SDK
- **Maintainability**: CLI changes don't affect SDK or core

---

## 📋 **Action Items**

### **Immediate Actions (This Week):**
1. **Create Core Interfaces**: Start with storage_interface.py
2. **Move Core Classes**: Begin moving core functionality
3. **Update Core Dependencies**: Remove SDK dependencies
4. **Test Core Independence**: Ensure core works standalone

### **Next Week:**
1. **Refactor SDK**: Update SDK to use core
2. **Update Storage Implementations**: Move to SDK
3. **Test SDK Functionality**: Ensure SDK still works
4. **Update Documentation**: Update SDK documentation

### **Following Week:**
1. **Refactor CLI**: Update CLI to use core
2. **Test CLI Functionality**: Ensure CLI still works
3. **Integration Testing**: Test all components together
4. **Performance Testing**: Ensure no regression

---

**This restructure will create a proper, maintainable architecture where Core is the foundation, SDK provides convenient client access, and CLI provides management tools.**
