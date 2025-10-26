# LuminoraCore Restructure - Detailed Task List
## Step-by-Step Implementation Guide

**Priority Order**: Core → SDK → CLI → Testing → Documentation

---

## 🎯 **Phase 1: Core Independence (CRITICAL)**

### **Task 1.1: Create Core Interfaces**
```bash
# Create directory structure
mkdir -p luminoracore/luminoracore/interfaces
mkdir -p luminoracore/luminoracore/core
mkdir -p luminoracore/luminoracore/memory
mkdir -p luminoracore/luminoracore/storage
```

**Files to Create:**
- `luminoracore/luminoracore/interfaces/storage_interface.py`
- `luminoracore/luminoracore/interfaces/memory_interface.py`
- `luminoracore/luminoracore/interfaces/personality_interface.py`
- `luminoracore/luminoracore/interfaces/evolution_interface.py`

**Priority**: HIGH  
**Estimated Time**: 4 hours  
**Dependencies**: None

### **Task 1.2: Move Core Classes from SDK to Core**
```bash
# Move these files:
# FROM: luminoracore-sdk-python/luminoracore_sdk/core/
# TO:   luminoracore/luminoracore/core/

# Files to move:
- personality_engine.py
- memory_system.py
- evolution_engine.py
- affinity_manager.py
- fact_extractor.py
- episode_manager.py
```

**Priority**: HIGH  
**Estimated Time**: 6 hours  
**Dependencies**: Task 1.1

### **Task 1.3: Update Core Dependencies**
```python
# luminoracore/requirements.txt should contain ONLY:
# - Core database drivers (sqlite3, psycopg2, boto3, redis, pymongo)
# - Basic utilities (datetime, json, asyncio, typing)
# - NO SDK-specific dependencies
```

**Priority**: HIGH  
**Estimated Time**: 2 hours  
**Dependencies**: Task 1.2

### **Task 1.4: Create Core Storage Base Classes**
```python
# luminoracore/luminoracore/storage/base_storage.py
class BaseStorage(StorageInterface):
    """Base implementation of storage interface"""
    pass

# luminoracore/luminoracore/storage/in_memory_storage.py
class InMemoryStorage(BaseStorage):
    """In-memory storage implementation"""
    pass
```

**Priority**: HIGH  
**Estimated Time**: 4 hours  
**Dependencies**: Task 1.1

### **Task 1.5: Test Core Independence**
```bash
# Create test script
python -c "
from luminoracore import PersonalityEngine, MemorySystem
from luminoracore.storage import InMemoryStorage

# Test core works without SDK
engine = PersonalityEngine()
storage = InMemoryStorage()
memory = MemorySystem(storage)
print('Core independence test: PASSED')
"
```

**Priority**: HIGH  
**Estimated Time**: 2 hours  
**Dependencies**: Tasks 1.1-1.4

---

## 🔧 **Phase 2: SDK Refactoring (HIGH)**

### **Task 2.1: Update SDK Imports**
```python
# Update all files in luminoracore-sdk-python/
# FROM: from luminoracore_sdk.core import ...
# TO:   from luminoracore import ...

# Files to update:
- luminoracore_sdk/__init__.py
- luminoracore_sdk/client.py
- luminoracore_sdk/client_v1_1.py
- All files in luminoracore_sdk/session/
- All files in luminoracore_sdk/types/
```

**Priority**: HIGH  
**Estimated Time**: 4 hours  
**Dependencies**: Phase 1 complete

### **Task 2.2: Move Storage Implementations to SDK**
```bash
# Move these files:
# FROM: luminoracore-sdk-python/luminoracore_sdk/session/
# TO:   luminoracore-sdk-python/luminoracore_sdk/storage/

# Files to move:
- storage_sqlite_flexible.py → storage/sqlite_storage.py
- storage_dynamodb_flexible.py → storage/dynamodb_storage.py
- storage_postgresql_flexible.py → storage/postgresql_storage.py
- storage_redis_flexible.py → storage/redis_storage.py
- storage_mongodb_flexible.py → storage/mongodb_storage.py
```

**Priority**: HIGH  
**Estimated Time**: 6 hours  
**Dependencies**: Task 2.1

### **Task 2.3: Create SDK Client Wrappers**
```python
# luminoracore-sdk-python/luminoracore_sdk/client.py
from luminoracore import PersonalityEngine, MemorySystem
from luminoracore.interfaces import StorageInterface

class LuminoraCoreClient:
    def __init__(self, storage: StorageInterface):
        self.core_engine = PersonalityEngine()
        self.memory_system = MemorySystem(storage)
        self.storage = storage
    
    # Wrap core methods with SDK convenience methods
    async def save_fact(self, user_id: str, category: str, key: str, value: Any, confidence: float = 0.8) -> bool:
        return await self.storage.save_fact(user_id, category, key, value, confidence)
```

**Priority**: HIGH  
**Estimated Time**: 8 hours  
**Dependencies**: Task 2.2

### **Task 2.4: Update SDK Requirements**
```python
# luminoracore-sdk-python/requirements.txt should contain:
# - luminoracore (core dependency)
# - SDK-specific dependencies
# - NO core functionality
```

**Priority**: MEDIUM  
**Estimated Time**: 1 hour  
**Dependencies**: Task 2.3

### **Task 2.5: Test SDK Functionality**
```bash
# Test SDK still works
python -c "
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.storage import SQLiteStorage

storage = SQLiteStorage('test.db')
client = LuminoraCoreClient(storage)
print('SDK functionality test: PASSED')
"
```

**Priority**: HIGH  
**Estimated Time**: 2 hours  
**Dependencies**: Task 2.4

---

## 🛠 **Phase 3: CLI Refactoring (MEDIUM)**

### **Task 3.1: Update CLI Imports**
```python
# Update all files in luminoracore-cli/
# FROM: from luminoracore_sdk import ...
# TO:   from luminoracore import ...

# Files to update:
- luminoracore_cli/__init__.py
- luminoracore_cli/main.py
- All files in luminoracore_cli/commands/
- All files in luminoracore_cli/management/
```

**Priority**: MEDIUM  
**Estimated Time**: 3 hours  
**Dependencies**: Phase 2 complete

### **Task 3.2: Update CLI Commands**
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

**Priority**: MEDIUM  
**Estimated Time**: 6 hours  
**Dependencies**: Task 3.1

### **Task 3.3: Update CLI Requirements**
```python
# luminoracore-cli/requirements.txt should contain:
# - luminoracore (core dependency)
# - CLI-specific dependencies (click, rich, etc.)
# - NO SDK dependencies
```

**Priority**: MEDIUM  
**Estimated Time**: 1 hour  
**Dependencies**: Task 3.2

### **Task 3.4: Test CLI Functionality**
```bash
# Test CLI still works
luminoracore-cli --help
luminoracore-cli memory list --user-id test_user
```

**Priority**: MEDIUM  
**Estimated Time**: 2 hours  
**Dependencies**: Task 3.3

---

## 🧪 **Phase 4: Testing & Validation (HIGH)**

### **Task 4.1: Integration Testing**
```bash
# Test all components together
python examples/luminoracore_v1_1_complete_demo.py
```

**Priority**: HIGH  
**Estimated Time**: 4 hours  
**Dependencies**: Phase 3 complete

### **Task 4.2: Performance Testing**
```bash
# Benchmark performance
python -c "
import time
import asyncio
from luminoracore import MemorySystem
from luminoracore.storage import InMemoryStorage

async def benchmark():
    storage = InMemoryStorage()
    memory = MemorySystem(storage)
    
    start = time.time()
    for i in range(1000):
        await memory.save_fact(f'user{i}', 'test', 'key', 'value')
    end = time.time()
    
    print(f'Performance: {(end-start)*1000:.2f}ms for 1000 operations')
"
```

**Priority**: HIGH  
**Estimated Time**: 2 hours  
**Dependencies**: Task 4.1

### **Task 4.3: Regression Testing**
```bash
# Test all existing functionality
python -m pytest tests/
```

**Priority**: HIGH  
**Estimated Time**: 4 hours  
**Dependencies**: Task 4.2

### **Task 4.4: End-to-End Testing**
```bash
# Test complete workflow
python examples/luminoracore_v1_1_complete_demo.py
luminoracore-cli memory list --user-id demo_user
```

**Priority**: HIGH  
**Estimated Time**: 2 hours  
**Dependencies**: Task 4.3

---

## 📚 **Phase 5: Documentation Update (MEDIUM)**

### **Task 5.1: Update Core Documentation**
```markdown
# Update luminoracore/docs/
- Update API reference
- Update architecture diagrams
- Update installation guide
- Update examples
```

**Priority**: MEDIUM  
**Estimated Time**: 4 hours  
**Dependencies**: Phase 4 complete

### **Task 5.2: Update SDK Documentation**
```markdown
# Update luminoracore-sdk-python/docs/
- Update API reference
- Update integration guide
- Update examples
- Update migration guide
```

**Priority**: MEDIUM  
**Estimated Time**: 4 hours  
**Dependencies**: Task 5.1

### **Task 5.3: Update CLI Documentation**
```markdown
# Update luminoracore-cli/README.md
- Update command reference
- Update usage examples
- Update installation guide
```

**Priority**: MEDIUM  
**Estimated Time**: 2 hours  
**Dependencies**: Task 5.2

### **Task 5.4: Update Main Documentation**
```markdown
# Update root README.md
- Update architecture diagram
- Update installation instructions
- Update examples
- Update links
```

**Priority**: MEDIUM  
**Estimated Time**: 2 hours  
**Dependencies**: Task 5.3

---

## 📋 **Summary of Tasks**

### **Critical Path (Must Complete First):**
1. **Task 1.1**: Create Core Interfaces (4h)
2. **Task 1.2**: Move Core Classes (6h)
3. **Task 1.3**: Update Core Dependencies (2h)
4. **Task 1.4**: Create Core Storage Base (4h)
5. **Task 1.5**: Test Core Independence (2h)

### **High Priority (Complete After Critical Path):**
6. **Task 2.1**: Update SDK Imports (4h)
7. **Task 2.2**: Move Storage Implementations (6h)
8. **Task 2.3**: Create SDK Client Wrappers (8h)
9. **Task 2.4**: Update SDK Requirements (1h)
10. **Task 2.5**: Test SDK Functionality (2h)

### **Medium Priority (Complete After High Priority):**
11. **Task 3.1**: Update CLI Imports (3h)
12. **Task 3.2**: Update CLI Commands (6h)
13. **Task 3.3**: Update CLI Requirements (1h)
14. **Task 3.4**: Test CLI Functionality (2h)

### **Testing Phase (Complete After All Code Changes):**
15. **Task 4.1**: Integration Testing (4h)
16. **Task 4.2**: Performance Testing (2h)
17. **Task 4.3**: Regression Testing (4h)
18. **Task 4.4**: End-to-End Testing (2h)

### **Documentation Phase (Complete After Testing):**
19. **Task 5.1**: Update Core Documentation (4h)
20. **Task 5.2**: Update SDK Documentation (4h)
21. **Task 5.3**: Update CLI Documentation (2h)
22. **Task 5.4**: Update Main Documentation (2h)

---

## ⏱ **Time Estimation**

### **Total Estimated Time**: 80 hours
### **Critical Path**: 22 hours
### **High Priority**: 21 hours
### **Medium Priority**: 12 hours
### **Testing**: 12 hours
### **Documentation**: 12 hours

### **Recommended Schedule:**
- **Week 1**: Critical Path (22h)
- **Week 2**: High Priority (21h)
- **Week 3**: Medium Priority + Testing (24h)
- **Week 4**: Documentation + Final Testing (13h)

---

## ✅ **Success Criteria**

### **Technical Success:**
- ✅ Core is completely independent
- ✅ SDK depends only on Core
- ✅ CLI depends only on Core
- ✅ No circular dependencies
- ✅ All tests passing
- ✅ Performance maintained or improved

### **Functional Success:**
- ✅ All existing functionality preserved
- ✅ No breaking changes for end users
- ✅ Examples still work
- ✅ Documentation updated
- ✅ Installation process unchanged

### **Architectural Success:**
- ✅ Clear dependency hierarchy
- ✅ Easy to add new storage implementations
- ✅ Easy to add new features to core
- ✅ Easy to create new SDKs
- ✅ Easy to extend CLI functionality

---

**This restructure will create a proper, maintainable architecture where Core is the foundation, SDK provides convenient client access, and CLI provides management tools.**
