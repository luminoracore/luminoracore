"""
Flexible Storage Management for LuminoraCore v1.1

Provides flexible storage implementations for all database types.
"""

# Import flexible storage implementations
from .flexible_storage import (
    FlexibleStorageManager,
    StorageType,
    StorageConfig
)

# Import database-specific flexible implementations
try:
    from .dynamodb_flexible import FlexibleDynamoDBStorage
except ImportError:
    FlexibleDynamoDBStorage = None

try:
    from .sqlite_flexible import FlexibleSQLiteStorage
except ImportError:
    FlexibleSQLiteStorage = None

try:
    from .postgresql_flexible import FlexiblePostgreSQLStorage
except ImportError:
    FlexiblePostgreSQLStorage = None

try:
    from .redis_flexible import FlexibleRedisStorage
except ImportError:
    FlexibleRedisStorage = None

try:
    from .mongodb_flexible import FlexibleMongoDBStorage
except ImportError:
    FlexibleMongoDBStorage = None

# Import migration manager
from .migrations import MigrationManager

__all__ = [
    "FlexibleStorageManager",
    "StorageType",
    "StorageConfig",
    "FlexibleDynamoDBStorage",
    "FlexibleSQLiteStorage", 
    "FlexiblePostgreSQLStorage",
    "FlexibleRedisStorage",
    "FlexibleMongoDBStorage",
    "MigrationManager",
]