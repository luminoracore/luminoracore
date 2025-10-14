# API Reference - LuminoraCore SDK Python

This document provides comprehensive API reference for the LuminoraCore SDK Python.

> **Note:** This covers the v1.0 SDK API. For v1.1 extensions (memory, affinity, snapshots), see [v1.1 SDK Features](#v11-sdk-features) at the end of this document.

## Table of Contents

- [Client](#client)
- [Personality Management](#personality-management)
- [Session Management](#session-management)
- [Provider Configuration](#provider-configuration)
- [Storage Configuration](#storage-configuration)
- [Memory Configuration](#memory-configuration)
- [Types](#types)

## Client

### LuminoraCoreClient

The main client class for interacting with LuminoraCore.

```python
from luminoracore import LuminoraCoreClient
from luminoracore.types.session import StorageConfig, MemoryConfig

client = LuminoraCoreClient(
    storage_config=StorageConfig(storage_type="memory"),
    memory_config=MemoryConfig()
)
```

#### Methods

##### `initialize() -> None`
Initialize the client and all its components.

##### `cleanup() -> None`
Clean up resources and close connections.

##### `load_personality(name: str, data: Dict[str, Any]) -> None`
Load a personality into the client.

**Parameters:**
- `name`: Personality name
- `data`: Personality data dictionary

##### `get_personality(name: str) -> Optional[PersonalityData]`
Get a personality by name.

**Returns:** Personality data or None if not found

##### `blend_personalities(personality_names: List[str], weights: List[float], blend_name: str) -> PersonalityData`
Blend multiple personalities.

**Parameters:**
- `personality_names`: List of personality names to blend
- `weights`: List of blend weights
- `blend_name`: Name for the blended personality

**Returns:** Blended personality data

##### `create_session(personality_name: str, provider_config: ProviderConfig) -> str`
Create a new session.

**Parameters:**
- `personality_name`: Name of the personality to use
- `provider_config`: Provider configuration

**Returns:** Session ID

##### `send_message(session_id: str, message: str, **kwargs) -> ChatResponse`
Send a message to a session.

**Parameters:**
- `session_id`: Session ID
- `message`: User message
- `**kwargs`: Additional parameters

**Returns:** Chat response

##### `stream_message(session_id: str, message: str, **kwargs) -> AsyncGenerator[ChatResponse, None]`
Stream a message to a session.

**Parameters:**
- `session_id`: Session ID
- `message`: User message
- `**kwargs`: Additional parameters

**Yields:** Chat response chunks

##### `get_conversation(session_id: str) -> Optional[Conversation]`
Get conversation for a session.

**Parameters:**
- `session_id`: Session ID

**Returns:** Conversation or None if not found

##### `store_memory(session_id: str, key: str, value: Any) -> None`
Store memory for a session.

**Parameters:**
- `session_id`: Session ID
- `key`: Memory key
- `value`: Memory value

##### `get_memory(session_id: str, key: str) -> Any`
Get memory for a session.

**Parameters:**
- `session_id`: Session ID
- `key`: Memory key

**Returns:** Memory value or None if not found

## Personality Management

### PersonalityData

Represents a personality configuration.

```python
from luminoracore.types.personality import PersonalityData

personality = PersonalityData(
    name="helpful_assistant",
    description="A helpful AI assistant",
    system_prompt="You are a helpful AI assistant.",
    metadata={}
)
```

#### Fields

- `name: str` - Personality name
- `description: str` - Personality description
- `system_prompt: str` - System prompt for the personality
- `name_override: Optional[str]` - Override for display name
- `description_override: Optional[str]` - Override for display description
- `metadata: Dict[str, Any]` - Additional metadata

### PersonalityBlend

Represents a personality blend configuration.

```python
from luminoracore.types.personality import PersonalityBlend

blend = PersonalityBlend(
    personalities=[personality1, personality2],
    weights=[0.6, 0.4],
    blend_type="weighted"
)
```

#### Fields

- `personalities: List[PersonalityData]` - Personalities to blend
- `weights: List[float]` - Blend weights for each personality
- `blend_type: str` - Type of blending
- `custom_rules: Optional[Dict[str, Any]]` - Custom blending rules

## Session Management

### SessionConfig

Configuration for personality sessions.

```python
from luminoracore.types.session import SessionConfig, SessionType

config = SessionConfig(
    session_id="session_123",
    personality={"name": "helpful_assistant"},
    provider_config={"name": "openai"},
    session_type=SessionType.CHAT,
    max_history=100,
    timeout=300
)
```

#### Fields

- `session_id: str` - Unique session identifier
- `personality: Dict[str, Any]` - Personality configuration
- `provider_config: Dict[str, Any]` - Provider configuration
- `session_type: SessionType` - Type of session
- `max_history: int` - Maximum conversation history length
- `timeout: int` - Session timeout in seconds

### Conversation

Represents a conversation with messages and metadata.

```python
from luminoracore.types.session import Conversation, Message, MessageRole
from datetime import datetime

conversation = Conversation(
    session_id="session_123",
    messages=[
        Message(
            role=MessageRole.USER,
            content="Hello!",
            timestamp=datetime.utcnow()
        )
    ]
)
```

#### Fields

- `session_id: str` - Session identifier
- `messages: List[Message]` - List of messages
- `metadata: Dict[str, Any]` - Conversation metadata
- `created_at: datetime` - Creation timestamp
- `updated_at: datetime` - Last update timestamp

## Provider Configuration

### ProviderConfig

Configuration for LLM providers.

```python
from luminoracore.types.provider import ProviderConfig

config = ProviderConfig(
    name="openai",
    api_key="your-api-key",
    model="gpt-3.5-turbo",
    base_url="https://api.openai.com/v1",
    extra={"timeout": 30, "max_retries": 3}
)
```

#### Fields

- `name: str` - Provider name
- `api_key: str` - API key
- `model: str` - Model name
- `base_url: Optional[str]` - Base URL for the API
- `extra: Optional[Dict[str, Any]]` - Additional configuration

### Supported Providers

- **OpenAI**: `openai`
- **Anthropic**: `anthropic`
- **Mistral**: `mistral`
- **Cohere**: `cohere`
- **Google**: `google`
- **Llama**: `llama`

## Storage Configuration

### StorageConfig

Configuration for conversation storage.

```python
from luminoracore.types.session import StorageConfig, StorageType

# In-memory storage
config = StorageConfig(storage_type=StorageType.MEMORY)

# Redis storage
config = StorageConfig(
    storage_type=StorageType.REDIS,
    connection_string="redis://localhost:6379"
)

# PostgreSQL storage
config = StorageConfig(
    storage_type=StorageType.POSTGRES,
    connection_string="postgresql://user:password@localhost/db"
)

# MongoDB storage
config = StorageConfig(
    storage_type=StorageType.MONGODB,
    connection_string="mongodb://localhost:27017/db"
)
```

#### Fields

- `storage_type: StorageType` - Type of storage backend
- `connection_string: Optional[str]` - Connection string
- `table_name: str` - Table name for database storage
- `auto_create_tables: bool` - Whether to auto-create tables
- `encryption_enabled: bool` - Whether encryption is enabled
- `compression_enabled: bool` - Whether compression is enabled

## Memory Configuration

### MemoryConfig

Configuration for conversation memory.

```python
from luminoracore.types.session import MemoryConfig

config = MemoryConfig(
    enabled=True,
    max_entries=1000,
    decay_factor=0.1,
    importance_threshold=0.5,
    track_topics=True,
    track_preferences=True,
    track_context=True,
    track_emotions=False
)
```

#### Fields

- `enabled: bool` - Whether memory is enabled
- `max_entries: int` - Maximum number of memory entries
- `decay_factor: float` - Memory decay factor
- `importance_threshold: float` - Importance threshold for memory
- `track_topics: bool` - Whether to track topics
- `track_preferences: bool` - Whether to track preferences
- `track_context: bool` - Whether to track context
- `track_emotions: bool` - Whether to track emotions

## Types

### Enums

#### SessionType
- `STATEFUL` - Stateful session
- `STATELESS` - Stateless session
- `CHAT` - Chat session

#### MessageRole
- `USER` - User message
- `ASSISTANT` - Assistant message
- `SYSTEM` - System message

#### StorageType
- `MEMORY` - In-memory storage
- `REDIS` - Redis storage
- `POSTGRES` - PostgreSQL storage
- `MONGODB` - MongoDB storage
- `FILE` - File storage

### ChatMessage

Represents a chat message.

```python
from luminoracore.types.provider import ChatMessage

message = ChatMessage(
    role="user",
    content="Hello!"
)
```

### ChatResponse

Represents a chat response.

```python
from luminoracore.types.provider import ChatResponse

response = ChatResponse(
    content="Hello! How can I help you?",
    role="assistant",
    finish_reason="stop",
    usage={"prompt_tokens": 10, "completion_tokens": 20},
    model="gpt-3.5-turbo"
)
```

## Error Handling

The SDK uses custom exceptions for error handling:

- `PersonalityError` - Personality-related errors
- `SessionError` - Session-related errors
- `ProviderError` - Provider-related errors
- `StorageError` - Storage-related errors

```python
from luminoracore.utils.exceptions import PersonalityError, SessionError

try:
    await client.load_personality("invalid", {})
except PersonalityError as e:
    print(f"Personality error: {e}")

try:
    await client.send_message("invalid_session", "Hello")
except SessionError as e:
    print(f"Session error: {e}")
```

---

## v1.1 SDK Features

LuminoraCore SDK v1.1 adds advanced memory and relationship features.

### LuminoraCoreClientV11

Extended client with v1.1 features.

```python
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11

# Create v1.1 storage
storage_v11 = InMemoryStorageV11()

# Create v1.1 client extension
client_v11 = LuminoraCoreClientV11(base_client, storage_v11=storage_v11)
```

#### Memory Methods

##### `get_facts(user_id: str, category: Optional[str]) -> List[FactDict]`
Get user facts, optionally filtered by category.

```python
# Get all facts
facts = await client_v11.get_facts(user_id="user123")

# Get facts by category
personal_facts = await client_v11.get_facts("user123", category="personal_info")
```

##### `get_episodes(user_id: str, min_importance: Optional[float], max_results: Optional[int]) -> List[EpisodeDict]`
Get memorable episodes, optionally filtered by importance.

```python
# Get all episodes
episodes = await client_v11.get_episodes(user_id="user123")

# Get important episodes only
important = await client_v11.get_episodes("user123", min_importance=7.0, max_results=10)
```

##### `search_memories(user_id: str, query: str, top_k: int) -> List[MemorySearchResult]`
Semantic search in memories (requires vector store).

```python
results = await client_v11.search_memories(
    user_id="user123",
    query="remember when we talked about my dog?",
    top_k=5
)
```

#### Affinity Methods

##### `get_affinity(user_id: str, personality_name: str) -> Optional[AffinityDict]`
Get relationship affinity data.

```python
affinity = await client_v11.get_affinity("user123", "alicia")
print(f"Points: {affinity['affinity_points']}")
print(f"Level: {affinity['current_level']}")
```

##### `update_affinity(user_id: str, personality_name: str, points_delta: int, interaction_type: str) -> Optional[AffinityDict]`
Update affinity points based on interaction.

```python
updated = await client_v11.update_affinity(
    user_id="user123",
    personality_name="alicia",
    points_delta=5,
    interaction_type="positive"
)
```

#### Snapshot Methods

##### `export_snapshot(session_id: str, options: Optional[SnapshotExportOptions]) -> PersonalitySnapshotDict`
Export complete personality state.

```python
snapshot = await client_v11.export_snapshot(
    session_id="session123",
    options={
        "include_conversation_history": True,
        "include_facts": True,
        "include_episodes": True
    }
)
```

##### `import_snapshot(snapshot: PersonalitySnapshotDict, user_id: str) -> str`
Import personality state from snapshot.

```python
new_session_id = await client_v11.import_snapshot(snapshot, user_id="user456")
```

#### Analytics Methods

##### `get_session_analytics(session_id: str) -> Dict[str, Any]`
Get session analytics and metrics.

```python
analytics = await client_v11.get_session_analytics("session123")
print(f"Total messages: {analytics['total_messages']}")
print(f"Facts learned: {analytics['facts_learned']}")
```

### v1.1 Storage Extensions

#### StorageV11Extension

Abstract interface for v1.1 storage methods.

##### `save_affinity(...) -> bool`
Save affinity data.

##### `get_affinity(...) -> Optional[Dict]`
Retrieve affinity data.

##### `save_fact(...) -> bool`
Save a user fact.

##### `get_facts(...) -> List[Dict]`
Retrieve user facts.

##### `save_episode(...) -> bool`
Save an episode.

##### `get_episodes(...) -> List[Dict]`
Retrieve episodes.

##### `save_mood(...) -> bool`
Save mood state.

##### `get_mood(...) -> Optional[Dict]`
Retrieve mood state.

#### InMemoryStorageV11

In-memory implementation of v1.1 storage.

```python
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11

storage = InMemoryStorageV11()

# Save affinity
await storage.save_affinity("user1", "alicia", 50, "friend")

# Get affinity
affinity = await storage.get_affinity("user1", "alicia")
```

### v1.1 Types

#### FactDict
Type definition for facts.

```python
from luminoracore_sdk.types.memory import FactDict

fact: FactDict = {
    "user_id": "user123",
    "category": "personal_info",
    "key": "name",
    "value": "Diego",
    "confidence": 0.99
}
```

#### EpisodeDict
Type definition for episodes.

```python
from luminoracore_sdk.types.memory import EpisodeDict

episode: EpisodeDict = {
    "user_id": "user123",
    "episode_type": "emotional_moment",
    "title": "Loss of pet",
    "summary": "User's dog passed away",
    "importance": 9.5,
    "sentiment": "very_negative"
}
```

#### AffinityDict
Type definition for affinity data.

```python
from luminoracore_sdk.types.relationship import AffinityDict

affinity: AffinityDict = {
    "user_id": "user123",
    "personality_name": "alicia",
    "affinity_points": 50,
    "current_level": "friend"
}
```

### Complete Example

```python
import asyncio
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11

async def example():
    # Initialize
    base_client = LuminoraCoreClient()
    await base_client.initialize()
    
    storage_v11 = InMemoryStorageV11()
    client_v11 = LuminoraCoreClientV11(base_client, storage_v11=storage_v11)
    
    # Use v1.1 features
    affinity = await client_v11.update_affinity(
        "user123", "alicia", points_delta=5, interaction_type="positive"
    )
    
    facts = await client_v11.get_facts("user123")
    episodes = await client_v11.get_episodes("user123", min_importance=7.0)
    
    print(f"Affinity: {affinity['affinity_points']} points")
    print(f"Facts: {len(facts)}")
    print(f"Episodes: {len(episodes)}")
    
    await base_client.cleanup()

asyncio.run(example())
```

### Migration from v1.0

**v1.0 code continues to work unchanged:**

```python
# v1.0 (still works)
client = LuminoraCoreClient(...)
session_id = await client.create_session(...)
response = await client.send_message(session_id, "Hello")
```

**v1.1 features are opt-in:**

```python
# v1.1 (opt-in)
client_v11 = LuminoraCoreClientV11(client, storage_v11=storage)
affinity = await client_v11.get_affinity(user_id, personality)
```

### See Also

- **Examples:** `examples/v1_1_sdk_usage.py`
- **Core v1.1 Docs:** `luminoracore/docs/v1_1_features.md`
- **Implementation Guide:** `mejoras_v1.1/STEP_BY_STEP_IMPLEMENTATION.md`

---

**Version:** 1.1.0  
**Status:** Production Ready  
**Backward Compatible:** 100%

