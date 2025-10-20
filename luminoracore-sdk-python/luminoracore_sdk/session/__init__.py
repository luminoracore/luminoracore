"""Session management for LuminoraCore SDK."""

from .manager import SessionManager
from .conversation import ConversationManager
from .memory import MemoryManager
from .memory_v1_1 import MemoryManagerV11
from .storage import SessionStorage
from .storage_v1_1 import StorageV11Extension, InMemoryStorageV11
from .storage_dynamodb_flexible import FlexibleDynamoDBStorageV11
from .storage_sqlite_flexible import FlexibleSQLiteStorageV11
from .storage_postgresql_flexible import FlexiblePostgreSQLStorageV11
from .storage_redis_flexible import FlexibleRedisStorageV11
from .storage_mongodb_flexible import FlexibleMongoDBStorageV11
from ..types.session import SessionConfig, MemoryConfig

# Alias for backward compatibility
PersonalitySession = SessionManager

__all__ = [
    "SessionManager",
    "PersonalitySession",  # Alias
    "ConversationManager", 
    "MemoryManager",
    "MemoryManagerV11",
    "SessionStorage",
    "StorageV11Extension",
    "InMemoryStorageV11",
    "FlexibleDynamoDBStorageV11",
    "FlexibleSQLiteStorageV11",
    "FlexiblePostgreSQLStorageV11",
    "FlexibleRedisStorageV11",
    "FlexibleMongoDBStorageV11",
    "SessionConfig",
    "MemoryConfig",
]
