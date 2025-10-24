# API Reference - LuminoraCore SDK Python

This document provides comprehensive API reference for the LuminoraCore SDK Python.

> **Note:** This covers the v1.1 SDK API with full memory, affinity, and relationship features. All v1.0 code continues to work unchanged.

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

#### Session Management Methods

##### `create_session(personality_name: str = "default", provider_config: Optional[Dict[str, Any]] = None) -> str`
Create a new session for conversation memory.

```python
# Create session with personality
session_id = await client_v11.create_session(
    personality_name="alicia",
    provider_config={"name": "openai", "model": "gpt-3.5-turbo"}
)
```

##### `ensure_session_exists(session_id: str) -> bool`
Ensure a session exists, creating it if necessary.

```python
# Ensure session exists
exists = await client_v11.ensure_session_exists("session_123")
```

##### `send_message_with_memory(session_id: str, user_message: str, personality_name: str, provider_config: Dict[str, Any]) -> Dict[str, Any]`
Send a message with full memory integration.

```python
response = await client_v11.send_message_with_memory(
    session_id="session_123",
    user_message="Hello, I'm Carlos from Madrid",
    personality_name="alicia",
    provider_config={"name": "openai", "model": "gpt-3.5-turbo"}
)
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

##### `save_fact(user_id: str, category: str, key: str, value: Any, confidence: float = 0.8, source: str = "user_input") -> bool`
Save a user fact to memory.

```python
# Save personal fact
await client_v11.save_fact(
    user_id="user123",
    category="personal_info",
    key="name",
    value="Carlos",
    confidence=0.95
)
```

##### `delete_fact(user_id: str, category: str, key: str) -> bool`
Delete a specific fact from memory.

```python
# Delete a fact
deleted = await client_v11.delete_fact("user123", "personal_info", "name")
```

##### `get_episodes(user_id: str, min_importance: Optional[float], max_results: Optional[int]) -> List[EpisodeDict]`
Get memorable episodes, optionally filtered by importance.

```python
# Get all episodes
episodes = await client_v11.get_episodes(user_id="user123")

# Get important episodes only
important = await client_v11.get_episodes("user123", min_importance=7.0, max_results=10)
```

##### `save_episode(user_id: str, episode_type: str, title: str, summary: str, importance: float, sentiment: str = "neutral") -> bool`
Save a memorable episode.

```python
# Save memorable episode
await client_v11.save_episode(
    user_id="user123",
    episode_type="milestone",
    title="First conversation",
    summary="User introduced themselves",
    importance=8.5,
    sentiment="positive"
)
```

##### `get_memory_stats(user_id: str) -> Dict[str, Any]`
Get comprehensive memory statistics.

```python
# Get memory statistics
stats = await client_v11.get_memory_stats("user123")
print(f"Total facts: {stats['total_facts']}")
print(f"Total episodes: {stats['total_episodes']}")
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

#### Sentiment Analysis Methods

##### `analyze_sentiment(user_id: str, message: str, context: Optional[List[str]] = None) -> Dict[str, Any]`
Analyze sentiment of a message for a specific user using keyword-based or LLM-based analysis.

**Parameters:**
- `user_id` (str, **required**): User identifier for personalization
- `message` (str, **required**): Message to analyze
- `context` (Optional[List[str]]): Optional conversation context

**Returns:**
- Dict with sentiment analysis results including sentiment, confidence, emotions detected, and personalized insights

**Example:**
```python
# Analyze sentiment for a specific user
sentiment = await client_v11.analyze_sentiment(
    user_id="user123",
    message="I'm so frustrated with this bug!",
    context=["technical_support"]
)
print(f"Sentiment: {sentiment['sentiment']}")
print(f"Confidence: {sentiment['confidence']}")
print(f"Emotions: {sentiment['emotions_detected']}")
```

##### `get_sentiment_history(user_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]`
Get sentiment analysis history for a user.

```python
# Get sentiment history
history = await client_v11.get_sentiment_history("user123", limit=10)
```

#### Personality Evolution Methods

##### `evolve_personality(user_id: str, personality_name: str, evolution_data: Dict[str, Any]) -> Dict[str, Any]`
Evolve a personality based on user interactions and preferences.

```python
# Evolve personality
evolution = await client_v11.evolve_personality(
    user_id="user123",
    personality_name="alicia",
    evolution_data={
        "interaction_patterns": ["positive", "technical"],
        "preferences": {"formality": 0.3, "humor": 0.8}
    }
)
```

##### `get_evolution_history(user_id: str, personality_name: str) -> List[Dict[str, Any]]`
Get the evolution history for a personality.

```python
# Get evolution history
history = await client_v11.get_evolution_history("user123", "alicia")
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

#### Flexible Storage Options

All storage implementations support flexible configuration for any database schema.

##### InMemoryStorageV11
In-memory implementation for development and testing.

```python
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11

storage = InMemoryStorageV11()
```

##### FlexibleDynamoDBStorageV11
DynamoDB storage that works with any table schema.

```python
from luminoracore_sdk.session.storage_dynamodb_flexible import FlexibleDynamoDBStorageV11

# Works with ANY DynamoDB table
storage = FlexibleDynamoDBStorageV11(
    table_name="your-existing-table",
    region="eu-west-1"
)
```

##### FlexibleSQLiteStorageV11
SQLite storage that works with any database file.

```python
from luminoracore_sdk.session.storage_sqlite_flexible import FlexibleSQLiteStorageV11

# Works with ANY SQLite database
storage = FlexibleSQLiteStorageV11(
    database_path="./your-existing.db"
)
```

##### FlexiblePostgreSQLStorageV11
PostgreSQL storage that works with any database and schema.

```python
from luminoracore_sdk.session.storage_postgresql_flexible import FlexiblePostgreSQLStorageV11

# Works with ANY PostgreSQL database
storage = FlexiblePostgreSQLStorageV11(
    connection_string="postgresql://user:pass@localhost/your_db",
    table_prefix="custom_"
)
```

##### FlexibleRedisStorageV11
Redis storage that works with any Redis instance.

```python
from luminoracore_sdk.session.storage_redis_flexible import FlexibleRedisStorageV11

# Works with ANY Redis instance
storage = FlexibleRedisStorageV11(
    connection_string="redis://localhost:6379/0",
    key_prefix="your_app:"
)
```

##### FlexibleMongoDBStorageV11
MongoDB storage that works with any database and collection.

```python
from luminoracore_sdk.session.storage_mongodb_flexible import FlexibleMongoDBStorageV11

# Works with ANY MongoDB database
storage = FlexibleMongoDBStorageV11(
    connection_string="mongodb://localhost:27017/your_db",
    collection_prefix="custom_"
)
```

##### FlexibleMySQLStorageV11
MySQL storage that works with any database and schema.

```python
from luminoracore_sdk.session.storage_mysql_flexible import FlexibleMySQLStorageV11

# Works with ANY MySQL database
storage = FlexibleMySQLStorageV11(
    connection_string="mysql://user:pass@localhost/your_db",
    table_prefix="custom_"
)
```

#### Storage Configuration Examples

```python
# Environment-based configuration
import os

# DynamoDB (AWS)
if os.getenv("LUMINORA_STORAGE_TYPE") == "dynamodb":
    storage = FlexibleDynamoDBStorageV11(
        table_name=os.getenv("DYNAMODB_TABLE", "your-table"),
        region=os.getenv("AWS_REGION", "eu-west-1")
    )

# SQLite (Development)
elif os.getenv("LUMINORA_STORAGE_TYPE") == "sqlite":
    storage = FlexibleSQLiteStorageV11(
        database_path=os.getenv("SQLITE_DATABASE_PATH", "./luminora.db")
    )

# PostgreSQL (Production)
elif os.getenv("LUMINORA_STORAGE_TYPE") == "postgresql":
    storage = FlexiblePostgreSQLStorageV11(
        connection_string=os.getenv("POSTGRES_URL"),
        table_prefix=os.getenv("TABLE_PREFIX", "luminora_")
    )

# Redis (Caching)
elif os.getenv("LUMINORA_STORAGE_TYPE") == "redis":
    storage = FlexibleRedisStorageV11(
        connection_string=os.getenv("REDIS_URL"),
        key_prefix=os.getenv("REDIS_PREFIX", "luminora:")
    )

# Default to in-memory
else:
    storage = InMemoryStorageV11()
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
import os
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
from luminoracore_sdk.session.storage_dynamodb_flexible import FlexibleDynamoDBStorageV11
from luminoracore_sdk.types.provider import ProviderConfig

async def complete_example():
    """Complete example showing all v1.1 features."""
    
    # 1. Initialize storage (flexible - works with any DynamoDB table)
    storage_v11 = FlexibleDynamoDBStorageV11(
        table_name=os.getenv("DYNAMODB_TABLE", "your-existing-table"),
        region=os.getenv("AWS_REGION", "eu-west-1")
    )
    
    # 2. Initialize base client
    base_client = LuminoraCoreClient()
    await base_client.initialize()
    
    # 3. Initialize v1.1 client
    client_v11 = LuminoraCoreClientV11(base_client, storage_v11=storage_v11)
    
    # 4. Create session with memory
    session_id = await client_v11.create_session(
        personality_name="alicia",
        provider_config={"name": "openai", "model": "gpt-3.5-turbo"}
    )
    
    # 5. Send message with full memory integration
    response = await client_v11.send_message_with_memory(
        session_id=session_id,
        user_message="Hello, I'm Carlos from Madrid, I work as a software developer",
        personality_name="alicia",
        provider_config={"name": "openai", "model": "gpt-3.5-turbo"}
    )
    
    # 6. Save additional facts
    await client_v11.save_fact(
        user_id=session_id,
        category="personal_info",
        key="hobby",
        value="Playing guitar",
        confidence=0.9
    )
    
    # 7. Save memorable episode
    await client_v11.save_episode(
        user_id=session_id,
        episode_type="milestone",
        title="First conversation",
        summary="User introduced themselves as Carlos from Madrid",
        importance=8.5,
        sentiment="positive"
    )
    
    # 8. Update affinity
    affinity = await client_v11.update_affinity(
        user_id=session_id,
        personality_name="alicia",
        points_delta=5,
        interaction_type="positive"
    )
    
    # 9. Analyze sentiment
    sentiment = await client_v11.analyze_sentiment(
        user_id=user_id,
        message="I'm so excited about this new project!",
        context=["work", "enthusiasm"]
    )
    
    # 10. Get memory statistics
    stats = await client_v11.get_memory_stats(session_id)
    
    # 11. Export snapshot
    snapshot = await client_v11.export_snapshot(session_id)
    
    # Results
    print(f"Session: {session_id}")
    print(f"Response: {response['response']}")
    print(f"Affinity: {affinity['affinity_points']} points ({affinity['current_level']})")
    print(f"Sentiment: {sentiment['sentiment']} (confidence: {sentiment['confidence']})")
    print(f"Memory Stats: {stats['total_facts']} facts, {stats['total_episodes']} episodes")
    print(f"Snapshot exported: {snapshot['_snapshot_info']['template_name']}")
    
    # Cleanup
    await base_client.cleanup()

# Run example
asyncio.run(complete_example())
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

