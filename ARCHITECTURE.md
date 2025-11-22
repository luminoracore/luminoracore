# LuminoraCore Architecture v1.2.0

**Last Updated:** November 21, 2025  
**Version:** 1.2.0

---

## Overview

LuminoraCore uses a **3-layer architecture** that separates business logic, client functionality, and user interface. This design enables:

- **Modularity:** Each layer can be used independently
- **Maintainability:** Clear separation of concerns
- **Scalability:** Easy to extend and modify individual layers
- **Backward Compatibility:** Changes don't break existing code

---

## Architecture Layers

### Layer 1: Core (`luminoracore/`)

**Purpose:** Pure business logic — no external dependencies

**Location:** `luminoracore/`

**Responsibilities:**
- Personality management (JSON schema, validation, compilation, blending)
- Memory system (facts, episodes, affinity tracking)
- Optimization module (token reduction techniques)
- Storage interfaces (pluggable backends)
- Migration system (database migrations)

**Key Modules:**
```
luminoracore/
├── core/
│   ├── personality.py      # Personality data models
│   ├── memory_system.py     # Memory management
│   └── ...
├── tools/
│   ├── blender.py           # PersonaBlend (personality blending)
│   ├── validator.py         # PersonalityValidator
│   └── ...
├── optimization/
│   ├── optimizer.py         # Unified optimization pipeline
│   ├── key_mapping.py       # Key abbreviation
│   ├── minifier.py          # JSON minification
│   ├── compact_format.py    # Compact array format
│   ├── deduplicator.py      # Fact deduplication
│   └── cache.py             # LRU cache with TTL
├── storage/
│   ├── in_memory_storage.py
│   ├── sqlite_storage.py
│   └── ...
└── interfaces/
    └── storage_interface.py
```

**Dependencies:** None (pure Python, standard library + minimal deps)

**Usage Example:**
```python
from luminoracore import Personality, PersonaBlend
from luminoracore.optimization import Optimizer, OptimizationConfig

# Use Core directly
personality = Personality.from_file("personality.json")
blender = PersonaBlend()
result = blender.blend([personality1, personality2], weights={"p1": 0.6, "p2": 0.4})

# Use optimization
config = OptimizationConfig(key_abbreviation=True, cache_enabled=True)
optimizer = Optimizer(config)
compressed = optimizer.compress(data)
```

---

### Layer 2: SDK (`luminoracore-sdk-python/`)

**Purpose:** Client layer with LLM integration — uses Core internally

**Location:** `luminoracore-sdk-python/`

**Responsibilities:**
- LLM provider integration (OpenAI, Anthropic, DeepSeek, Mistral, Cohere, Google, Llama)
- Session management (stateful conversations)
- Storage adapters (SQLite, Redis, PostgreSQL, MongoDB, DynamoDB, InMemory)
- Analytics & metrics (token tracking, performance monitoring)
- Async/await support for high-performance applications

**Key Modules:**
```
luminoracore-sdk-python/
├── luminoracore_sdk/
│   ├── client.py                    # LuminoraCoreClient
│   ├── personality/
│   │   ├── blender.py               # PersonalityBlender (uses Core via adapter)
│   │   ├── adapter.py               # PersonaBlendAdapter (NEW in v1.2)
│   │   └── manager.py
│   ├── session/
│   │   ├── memory.py                # MemoryManager (uses Core MemorySystem)
│   │   ├── storage.py               # Storage with OptimizedStorageWrapper
│   │   └── ...
│   ├── providers/
│   │   ├── openai_provider.py
│   │   ├── anthropic_provider.py
│   │   └── ...
│   └── ...
```

**Dependencies:** 
- `luminoracore>=1.2.0` (Core)
- LLM provider SDKs (OpenAI, Anthropic, etc.)

**Integration with Core:**
- **PersonalityBlender** → Uses `PersonaBlendAdapter` → Calls Core `PersonaBlend`
- **MemoryManager** → Uses Core `MemorySystem` when available (fallback to SDK implementation)
- **Storage** → Wrapped with `OptimizedStorageWrapper` when optimization enabled
- **Client** → Accepts `OptimizationConfig` and creates `Optimizer` instance

**Usage Example:**
```python
from luminoracore_sdk import LuminoraCoreClient
from luminoracore.optimization import OptimizationConfig
from luminoracore_sdk.types.session import StorageConfig, StorageType

# SDK uses Core internally
client = LuminoraCoreClient(
    storage_config=StorageConfig(storage_type=StorageType.MEMORY),
    optimization_config=OptimizationConfig(
        key_abbreviation=True,
        cache_enabled=True
    )
)
await client.initialize()

# Personality blending uses Core PersonaBlend via adapter
result = await client.blend_personalities(
    personality_names=["assistant", "analyst"],
    weights=[0.6, 0.4]
)
```

---

### Layer 3: CLI (`luminoracore-cli/`)

**Purpose:** User interface layer — built on top of Core

**Location:** `luminoracore-cli/`

**Responsibilities:**
- Validation tools (personality validation and compilation)
- Memory commands (fact/episode/affinity management)
- Migration tools (database migration commands)
- Developer tools (interactive mode, snapshots)

**Key Modules:**
```
luminoracore-cli/
├── luminoracore_cli/
│   ├── main.py                      # CLI entry point
│   ├── commands/
│   │   ├── validate.py              # Uses Core PersonalityValidator
│   │   ├── migrate.py               # Uses Core MigrationManager
│   │   └── ...
│   ├── core/
│   │   ├── validator.py             # CLIValidator (uses Core)
│   │   └── ...
│   └── ...
```

**Dependencies:**
- `luminoracore>=1.2.0` (Core) — **REQUIRED** (NEW in v1.2)
- `luminoracore-sdk` (optional, for some features)

**Integration with Core:**
- **CLIValidator** → Uses Core `PersonalityValidator`
- **Migration Commands** → Uses Core `MigrationManager`
- **Memory Commands** → Uses Core `MemorySystem` when available

**Usage Example:**
```bash
# CLI uses Core directly
luminoracore validate personality.json
luminoracore memory list --user-id user123
luminoracore migrate --upgrade
```

---

## Data Flow

### Example: Personality Blending

```
User Code (SDK)
    ↓
PersonalityBlender.blend_personalities()
    ↓
PersonaBlendAdapter.blend_personalities()  [Adapter Layer]
    ↓
Core PersonaBlend.blend()                  [Core Layer]
    ↓
Blended Personality
    ↓
PersonaBlendAdapter._core_to_sdk_personality()  [Adapter Layer]
    ↓
SDK PersonalityData
    ↓
User Code
```

### Example: Memory Storage with Optimization

```
User Code (SDK)
    ↓
MemoryManager.store_memory()
    ↓
Core MemorySystem (if available) OR SDK fallback
    ↓
OptimizedStorageWrapper.save_session()  [If optimization enabled]
    ↓
Optimizer.compress()                     [Core Layer]
    ↓
Base Storage Backend (SQLite, Redis, etc.)
```

---

## Key Design Patterns

### 1. Adapter Pattern

**Purpose:** Bridge SDK and Core interfaces

**Implementation:**
- `PersonaBlendAdapter` translates between SDK `PersonalityData` and Core `Personality`
- Handles async/sync conversion (Core is sync, SDK is async)
- Maintains 100% backward compatibility

**Location:** `luminoracore-sdk-python/luminoracore_sdk/personality/adapter.py`

### 2. Wrapper Pattern

**Purpose:** Transparent optimization application

**Implementation:**
- `OptimizedStorageWrapper` wraps storage backends
- Automatically compresses on save, expands on load
- No changes required to user code

**Location:** `luminoracore-sdk-python/luminoracore_sdk/session/storage.py`

### 3. Fallback Pattern

**Purpose:** Graceful degradation when Core not available

**Implementation:**
- `MemoryManager` uses Core `MemorySystem` if available
- Falls back to SDK implementation if Core not installed
- Maintains API consistency

**Location:** `luminoracore-sdk-python/luminoracore_sdk/session/memory.py`

---

## Dependency Graph

```
┌─────────────────┐
│   User Code     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌─────────────────┐
│       CLI        │──────│      Core       │
│  (luminoracore-  │      │  (luminoracore) │
│      cli)        │      │                 │
└────────┬─────────┘      └────────┬────────┘
         │                           │
         │                           │
         ▼                           │
┌─────────────────┐                  │
│       SDK       │──────────────────┘
│ (luminoracore-  │
│   sdk-python)   │
└─────────────────┘
```

**Dependencies:**
- CLI → Core (required)
- CLI → SDK (optional)
- SDK → Core (required)

---

## Migration from v1.1 to v1.2

### What Changed

1. **SDK PersonalityBlender:** Now uses Core `PersonaBlend` via adapter
2. **SDK MemoryManager:** Uses Core `MemorySystem` when available
3. **SDK Storage:** Wrapped with optimizer when optimization enabled
4. **CLI:** Now requires Core as dependency (was optional)

### What Stayed the Same

- **Public APIs:** 100% backward compatible
- **User Code:** No changes required
- **Data Formats:** Same JSON schemas
- **Storage Backends:** Same interfaces

### Migration Steps

1. **SDK Users:** No changes required. Optional: enable optimization.
2. **CLI Users:** Reinstall CLI (Core dependency now required).
3. **Core Users:** No changes required.

See [`MIGRATION_1.1_to_1.2.md`](MIGRATION_1.1_to_1.2.md) for complete details.

---

## Benefits of 3-Layer Architecture

### 1. Modularity
- Each layer can be used independently
- Core can be used without SDK/CLI
- SDK can be used without CLI

### 2. Maintainability
- Clear separation of concerns
- Easy to locate and fix bugs
- Simple to add new features

### 3. Testability
- Each layer can be tested independently
- Integration tests validate layer interactions
- Full stack tests validate entire system

### 4. Scalability
- Easy to add new LLM providers (SDK layer)
- Easy to add new storage backends (Core layer)
- Easy to add new CLI commands (CLI layer)

### 5. Backward Compatibility
- Changes in Core don't break SDK/CLI
- Adapters maintain API compatibility
- Fallbacks ensure graceful degradation

---

## Future Enhancements

### Planned Improvements

1. **Plugin System:** Allow third-party plugins for each layer
2. **GraphQL API:** Add GraphQL layer for web applications
3. **REST API:** Add REST API layer for microservices
4. **Web UI:** Add web interface layer (Layer 4)

### Extension Points

- **Core:** New storage backends, optimization techniques
- **SDK:** New LLM providers, session types
- **CLI:** New commands, interactive modes

---

## Related Documentation

- **Migration Guide:** [`MIGRATION_1.1_to_1.2.md`](MIGRATION_1.1_to_1.2.md)
- **Changelog Core:** [`luminoracore/CHANGELOG.md`](luminoracore/CHANGELOG.md)
- **Changelog SDK:** [`luminoracore-sdk-python/CHANGELOG.md`](luminoracore-sdk-python/CHANGELOG.md)
- **Changelog CLI:** [`luminoracore-cli/CHANGELOG.md`](luminoracore-cli/CHANGELOG.md)
- **Fase 0 Documentation:** [`evolucion/FASE_0_REFACTOR_ARQUITECTURA_PROMPTS.md`](evolucion/FASE_0_REFACTOR_ARQUITECTURA_PROMPTS.md)

---

**Version:** 1.2.0  
**Last Updated:** November 21, 2025

