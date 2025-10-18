# 📚 Documentación Real del SDK v1.1 - API Actual

**Documentación exacta de lo que tiene el SDK v1.1 - Sin asumir métodos que no existen**

---

## 🎯 **PROBLEMA IDENTIFICADO**

**❌ Lo que estaba mal:**
- Asumí métodos como `add_fact()`, `store_fact()` que NO existen
- Inventé parámetros como `category`, `limit` que NO acepta
- No verifiqué la API real del SDK v1.1

**✅ Lo que SÍ existe:**
- `MemoryManagerV11` con métodos limitados
- `StorageV11Extension` con métodos abstractos
- `LuminoraCoreClientV11` con métodos específicos

---

## 🔍 **API REAL DEL SDK V1.1**

### **1. LuminoraCoreClientV11**
```python
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11

# Inicialización
client_v11 = LuminoraCoreClientV11(base_client, storage_v11=storage)

# MÉTODOS DISPONIBLES:
await client_v11.search_memories(user_id, query, top_k=10)
await client_v11.get_facts(user_id, options=None)
await client_v11.get_episodes(user_id, min_importance=None, max_results=None)
await client_v11.get_affinity(user_id, personality_name)
await client_v11.get_relationship_level(user_id, personality_name)
await client_v11.export_personality_snapshot(user_id, personality_name, options=None)
```

### **2. MemoryManagerV11**
```python
from luminoracore_sdk.session.memory_v1_1 import MemoryManagerV11

# Inicialización
memory_manager = MemoryManagerV11(storage_v11=storage)

# MÉTODOS DISPONIBLES:
await memory_manager.get_facts(user_id, options=None)
await memory_manager.get_episodes(user_id, min_importance=None, max_results=None)
await memory_manager.get_episode_by_id(episode_id)  # ⚠️ No implementado
await memory_manager.semantic_search(user_id, query, top_k=10, filters=None)
```

### **3. StorageV11Extension**
```python
from luminoracore_sdk.session.storage_v1_1 import StorageV11Extension

# MÉTODOS ABSTRACTOS (deben implementarse):
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

# Implementación en memoria (para testing)
storage = InMemoryStorageV11()

# MÉTODOS IMPLEMENTADOS:
await storage.save_affinity(...)  # ✅ Implementado
await storage.get_affinity(...)   # ✅ Implementado
await storage.save_fact(...)      # ✅ Implementado
await storage.get_facts(...)      # ✅ Implementado
await storage.save_episode(...)   # ✅ Implementado
await storage.get_episodes(...)   # ✅ Implementado
await storage.save_mood(...)      # ✅ Implementado
await storage.get_mood(...)       # ✅ Implementado
```

---

## 🔧 **IMPLEMENTACIÓN CORRECTA PARA BACKEND**

### **1. Configuración Correcta**
```python
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
from luminoracore_sdk.session.memory_v1_1 import MemoryManagerV11

# Configurar storage
storage = InMemoryStorageV11()  # Para desarrollo
# storage = DynamoDBStorageV11(...)  # Para producción

# Configurar cliente v1.1
base_client = LuminoraCoreClient()  # Cliente base v1.0
client_v11 = LuminoraCoreClientV11(base_client, storage_v11=storage)
```

### **2. Endpoints Correctos**
```python
# ✅ CORRECTO: Usar métodos que SÍ existen
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

### **3. ❌ INCORRECTO: Métodos que NO existen**
```python
# ❌ ESTO NO EXISTE:
await memory_manager.add_fact(session_id, fact_data)  # ❌ No existe
await memory_manager.store_fact(session_id, content, category)  # ❌ No existe
await client_v11.save_fact(session_id, fact)  # ❌ No existe

# ❌ ESTOS PARÁMETROS NO EXISTEN:
await memory_manager.get_facts(session_id, category="personal_info")  # ❌ No acepta category
await memory_manager.get_facts(session_id, limit=10)  # ❌ No acepta limit
```

---

## 🎯 **ESTRATEGIA CORRECTA**

### **Opción 1: Usar Solo Lectura (Recomendado para Demo)**
```python
# Solo usar métodos de lectura que SÍ existen
async def handle_memory_readonly(session_id):
    # Leer hechos existentes
    facts = await client_v11.get_facts(session_id)
    
    # Leer episodios existentes
    episodes = await client_v11.get_episodes(session_id)
    
    # Buscar en memoria
    search_results = await client_v11.search_memories(session_id, "query")
    
    return {
        "facts": facts,
        "episodes": episodes,
        "search_results": search_results
    }
```

### **Opción 2: Implementar Storage Personalizado**
```python
class CustomStorageV11(StorageV11Extension):
    """Implementación personalizada para el backend"""
    
    async def save_fact(self, user_id: str, category: str, key: str, value: Any, **kwargs) -> bool:
        # Implementar guardado en DynamoDB/SQLite
        pass
    
    async def get_facts(self, user_id: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        # Implementar lectura desde DynamoDB/SQLite
        pass
    
    # ... implementar todos los métodos abstractos
```

### **Opción 3: Simular Escritura (Para Demo)**
```python
# Simular escritura usando el cliente base v1.0
async def simulate_fact_storage(session_id, fact_data):
    # Usar el cliente base para simular almacenamiento
    # Esto es solo para demostración
    pass
```

---

## 📋 **ENDPOINTS REALES QUE SE PUEDEN IMPLEMENTAR**

### **Endpoints de Lectura (✅ Funcionan)**
```bash
GET /api/v1/memory/session/{id}/facts           # Leer hechos
GET /api/v1/memory/session/{id}/episodes        # Leer episodios
POST /api/v1/memory/session/{id}/search         # Buscar en memoria
GET /api/v1/affinity/session/{id}               # Leer afinidad
GET /api/v1/relationship/session/{id}           # Leer nivel de relación
GET /api/v1/session/{id}/export                 # Exportar snapshot
```

### **Endpoints de Escritura (⚠️ Requieren implementación)**
```bash
POST /api/v1/memory/session/{id}/facts          # Guardar hecho (implementar)
POST /api/v1/memory/session/{id}/episodes       # Guardar episodio (implementar)
POST /api/v1/affinity/session/{id}              # Guardar afinidad (implementar)
```

---

## 🚀 **RECOMENDACIÓN PARA CURSOR AI**

### **Fase 1: Implementar Solo Lectura**
1. Usar `InMemoryStorageV11` para desarrollo
2. Implementar endpoints de lectura que SÍ existen
3. Probar que funciona correctamente

### **Fase 2: Implementar Escritura**
1. Crear `CustomStorageV11` que extienda `StorageV11Extension`
2. Implementar métodos abstractos para DynamoDB/SQLite
3. Agregar endpoints de escritura

### **Fase 3: Integración Completa**
1. Conectar con base de datos real
2. Implementar persistencia completa
3. Probar flujo completo

---

## ✅ **RESUMEN DE LO QUE SÍ EXISTE**

### **✅ Clases Disponibles:**
- `LuminoraCoreClientV11` - Cliente v1.1
- `MemoryManagerV11` - Gestión de memoria
- `StorageV11Extension` - Interfaz de almacenamiento
- `InMemoryStorageV11` - Implementación en memoria

### **✅ Métodos de Lectura:**
- `get_facts()` - Leer hechos
- `get_episodes()` - Leer episodios
- `search_memories()` - Buscar en memoria
- `get_affinity()` - Leer afinidad
- `export_personality_snapshot()` - Exportar snapshot

### **⚠️ Métodos de Escritura (Abstractos):**
- `save_fact()` - Guardar hecho (implementar)
- `save_episode()` - Guardar episodio (implementar)
- `save_affinity()` - Guardar afinidad (implementar)

---

**🎊 ¡Ahora Cursor AI sabe exactamente qué métodos existen y cuáles debe implementar!**
