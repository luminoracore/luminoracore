# LuminoraCore SDK - Session Module

Módulo de gestión de sesiones, storage y memoria para el SDK.

---

## 📋 Componentes

### 1. SessionManager (`manager.py`)

**Propósito:** Gestión de sesiones de personalidades AI.

**Características:**
- ✅ Creación y eliminación de sesiones
- ✅ Gestión de conversaciones
- ✅ Integración con providers
- ✅ Persistencia con storage backends

**Uso:**
```python
from luminoracore_sdk.session import SessionManager

manager = SessionManager(storage=storage_backend)
session_id = await manager.create_session(
    personality=personality_data,
    provider_config=provider_config
)
```

---

### 2. ConversationManager (`conversation.py`)

**Propósito:** Gestión de conversaciones dentro de sesiones.

**Características:**
- ✅ Almacenamiento de mensajes
- ✅ Historial de conversación
- ✅ Gestión de contexto
- ✅ Limpieza de conversaciones

**Uso:**
```python
from luminoracore_sdk.session import ConversationManager

conversation = ConversationManager()
await conversation.add_message(session_id, message)
messages = await conversation.get_messages(session_id)
```

---

### 3. MemoryManager (`memory.py`)

**Propósito:** Gestión de memoria con integración Core.

**Características:**
- ✅ Almacenamiento de memoria
- ✅ Recuperación de memoria
- ✅ Integración con Core MemorySystem (v1.2.0)
- ✅ Fallback a implementación propia
- ✅ Soporte para optimizer

**Uso:**
```python
from luminoracore_sdk.session import MemoryManager

memory = MemoryManager(
    config=MemoryConfig(),
    optimizer=optimizer  # Opcional
)
await memory.store_memory(session_id, "key", "value")
value = await memory.get_memory(session_id, "key")
```

**Integración Core (v1.2.0):**
- Usa `luminoracore.core.memory_system.MemorySystem` cuando disponible
- Fallback automático si Core no está disponible
- Transparente para el usuario

---

### 4. SessionStorage (`storage.py`)

**Propósito:** Backends de almacenamiento para sesiones.

**Implementaciones:**
- ✅ `InMemoryStorage` - Almacenamiento en memoria
- ✅ `JSONFileStorage` - Almacenamiento en archivos JSON
- ✅ `RedisStorage` - Almacenamiento en Redis
- ✅ `PostgreSQLStorage` - Almacenamiento en PostgreSQL
- ✅ `MongoDBStorage` - Almacenamiento en MongoDB

**Uso:**
```python
from luminoracore_sdk.session import create_storage
from luminoracore_sdk.types.session import StorageConfig, StorageType

config = StorageConfig(storage_type=StorageType.MEMORY)
storage = create_storage(config, optimizer=optimizer)  # optimizer opcional
```

---

### 5. OptimizedStorageWrapper (`storage.py`)

**Propósito:** Wrapper que aplica optimización transparentemente.

**Características:**
- ✅ Compresión automática al guardar
- ✅ Expansión automática al cargar
- ✅ Transparente para el usuario
- ✅ Soporte para todos los storage backends

**Uso:**
```python
from luminoracore_sdk.session import OptimizedStorageWrapper
from luminoracore.optimization import Optimizer, OptimizationConfig

opt_config = OptimizationConfig(
    key_abbreviation=True,
    compact_format=True,
    minify_json=True
)
optimizer = Optimizer(opt_config)

# Wrapper automático cuando se usa create_storage con optimizer
storage = create_storage(config, optimizer=optimizer)
# storage es automáticamente OptimizedStorageWrapper
```

**Funcionamiento:**
1. `save_session()`: Comprime datos antes de guardar
2. `load_session()`: Expande datos después de cargar
3. Otros métodos: Delega al storage base

---

## 🔧 Funciones Principales

### `create_storage()`

**Función:** Factory para crear storage backends con optimización opcional.

**Parámetros:**
- `config: StorageConfig` - Configuración de storage
- `optimizer: Optional[Optimizer]` - Optimizer del Core (opcional)

**Retorna:**
- `SessionStorage` - Instancia de storage (potencialmente wrapped)

**Ejemplo:**
```python
from luminoracore_sdk.session import create_storage
from luminoracore_sdk.types.session import StorageConfig, StorageType
from luminoracore.optimization import OptimizationConfig, Optimizer

# Sin optimización
storage = create_storage(StorageConfig(storage_type=StorageType.MEMORY))

# Con optimización
opt_config = OptimizationConfig(key_abbreviation=True, compact_format=True)
optimizer = Optimizer(opt_config)
storage = create_storage(
    StorageConfig(storage_type=StorageType.MEMORY),
    optimizer=optimizer
)
# storage es OptimizedStorageWrapper
```

---

## 🆕 v1.2.0 - Nuevas Features

### 1. OptimizedStorageWrapper

**Nuevo:** Wrapper transparente para optimización.

**Beneficios:**
- ✅ Token reduction: 25-45%
- ✅ Storage size: Reduced by ~30-40%
- ✅ Transparente: No cambios de código necesarios

### 2. Core MemorySystem Integration

**Nuevo:** MemoryManager usa Core MemorySystem cuando disponible.

**Beneficios:**
- ✅ Mejor rendimiento
- ✅ Consistencia con Core
- ✅ Fallback automático

---

## 📊 Arquitectura

```
SessionManager
    ├── ConversationManager (gestión de mensajes)
    ├── MemoryManager (gestión de memoria)
    │   ├── Core MemorySystem (si disponible)
    │   └── Fallback implementation
    └── SessionStorage (persistencia)
        ├── InMemoryStorage
        ├── JSONFileStorage
        ├── RedisStorage
        ├── PostgreSQLStorage
        ├── MongoDBStorage
        └── OptimizedStorageWrapper (v1.2.0)
            └── Wraps any storage with optimization
```

---

## 🔄 Flujo de Datos

### Guardar Sesión (con optimización)

```
SessionManager.save_session()
    ↓
OptimizedStorageWrapper.save_session()
    ↓
Optimizer.compress()  # Comprime datos
    ↓
BaseStorage.save_session()  # Guarda datos comprimidos
```

### Cargar Sesión (con optimización)

```
SessionManager.load_session()
    ↓
OptimizedStorageWrapper.load_session()
    ↓
BaseStorage.load_session()  # Carga datos comprimidos
    ↓
Optimizer.expand()  # Expande datos
    ↓
Retorna datos expandidos
```

---

## 🐛 Troubleshooting

### Error: "OptimizedStorageWrapper not found"

**Solución:** Asegúrate de usar `create_storage()` con optimizer:
```python
storage = create_storage(config, optimizer=optimizer)
```

### Error: "Core MemorySystem not available"

**Solución:** Es normal si Core no está instalado. MemoryManager usa fallback automáticamente.

### Error: "Storage type not supported"

**Solución:** Verifica que el `StorageType` sea válido:
```python
from luminoracore_sdk.types.session import StorageType
# StorageType.MEMORY, StorageType.REDIS, etc.
```

---

## 📚 Más Información

- **Client Documentation:** `../client.py`
- **Types:** `../types/session.py`
- **Core Integration:** `../../luminoracore/core/memory_system.py`
- **Optimization:** `../../luminoracore/optimization/`

---

**Última Actualización:** 2025-11-21  
**Versión SDK:** 1.2.0  
**Estado:** ✅ Módulo completo y funcionando

