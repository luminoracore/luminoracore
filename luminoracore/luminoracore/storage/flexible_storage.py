"""
Flexible Storage Manager for LuminoraCore v1.1

Provides a unified interface for all flexible storage implementations.
"""

from enum import Enum
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
import json
import os


class StorageType(Enum):
    """Supported storage types"""
    DYNAMODB_FLEXIBLE = "dynamodb_flexible"
    SQLITE_FLEXIBLE = "sqlite_flexible"
    POSTGRESQL_FLEXIBLE = "postgresql_flexible"
    REDIS_FLEXIBLE = "redis_flexible"
    MONGODB_FLEXIBLE = "mongodb_flexible"
    IN_MEMORY = "in_memory"


@dataclass
class StorageConfig:
    """Storage configuration"""
    storage_type: StorageType
    config: Dict[str, Any]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StorageConfig":
        """Create StorageConfig from dictionary"""
        storage_type = StorageType(data["storage"]["type"])
        return cls(storage_type=storage_type, config=data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "storage": {
                "type": self.storage_type.value,
                **self.config.get("storage", {})
            }
        }


class FlexibleStorageManager:
    """
    Unified manager for all flexible storage implementations.
    
    Automatically selects and configures the appropriate storage
    based on configuration or environment variables.
    """
    
    def __init__(self, config: Optional[Union[StorageConfig, Dict[str, Any]]] = None):
        """
        Initialize flexible storage manager
        
        Args:
            config: Storage configuration (dict, StorageConfig, or None for auto-detection)
        """
        if config is None:
            config = self._auto_detect_config()
        elif isinstance(config, dict):
            config = StorageConfig.from_dict(config)
        
        self.config = config
        self.storage = self._create_storage()
    
    def _auto_detect_config(self) -> StorageConfig:
        """Auto-detect storage configuration from environment variables"""
        
        # Check for specific storage type - default to in-memory for demos
        storage_type = os.environ.get("LUMINORA_STORAGE_TYPE", "in_memory")
        
        try:
            storage_type_enum = StorageType(storage_type)
        except ValueError:
            storage_type_enum = StorageType.IN_MEMORY
        
        config = {"storage": {"type": storage_type_enum.value}}
        
        # Add type-specific configuration
        if storage_type_enum == StorageType.DYNAMODB_FLEXIBLE:
            config["storage"]["dynamodb"] = {
                "table_name": os.environ.get("LUMINORA_DYNAMODB_TABLE", "luminora-sessions"),
                "region": os.environ.get("LUMINORA_DYNAMODB_REGION", "eu-west-1"),
                "hash_key": os.environ.get("LUMINORA_DYNAMODB_HASH_KEY"),
                "range_key": os.environ.get("LUMINORA_DYNAMODB_RANGE_KEY")
            }
        
        elif storage_type_enum == StorageType.SQLITE_FLEXIBLE:
            config["storage"]["sqlite"] = {
                "database_path": os.environ.get("LUMINORA_SQLITE_PATH", "./luminora.db"),
                "facts_table": os.environ.get("LUMINORA_SQLITE_FACTS_TABLE"),
                "affinity_table": os.environ.get("LUMINORA_SQLITE_AFFINITY_TABLE")
            }
        
        elif storage_type_enum == StorageType.POSTGRESQL_FLEXIBLE:
            config["storage"]["postgresql"] = {
                "host": os.environ.get("LUMINORA_POSTGRES_HOST", "localhost"),
                "port": int(os.environ.get("LUMINORA_POSTGRES_PORT", "5432")),
                "database": os.environ.get("LUMINORA_POSTGRES_DATABASE", "luminora"),
                "schema": os.environ.get("LUMINORA_POSTGRES_SCHEMA", "public"),
                "username": os.environ.get("LUMINORA_POSTGRES_USERNAME", "postgres"),
                "password": os.environ.get("LUMINORA_POSTGRES_PASSWORD", "")
            }
        
        elif storage_type_enum == StorageType.REDIS_FLEXIBLE:
            config["storage"]["redis"] = {
                "host": os.environ.get("LUMINORA_REDIS_HOST", "localhost"),
                "port": int(os.environ.get("LUMINORA_REDIS_PORT", "6379")),
                "db": int(os.environ.get("LUMINORA_REDIS_DB", "0")),
                "key_prefix": os.environ.get("LUMINORA_REDIS_KEY_PREFIX", "luminora")
            }
        
        elif storage_type_enum == StorageType.MONGODB_FLEXIBLE:
            config["storage"]["mongodb"] = {
                "host": os.environ.get("LUMINORA_MONGODB_HOST", "localhost"),
                "port": int(os.environ.get("LUMINORA_MONGODB_PORT", "27017")),
                "database": os.environ.get("LUMINORA_MONGODB_DATABASE", "luminora"),
                "username": os.environ.get("LUMINORA_MONGODB_USERNAME", ""),
                "password": os.environ.get("LUMINORA_MONGODB_PASSWORD", "")
            }
        
        return StorageConfig(storage_type=storage_type_enum, config=config)
    
    def _create_storage(self):
        """Create storage instance based on configuration"""
        storage_type = self.config.storage_type
        storage_config = self.config.config.get("storage", {})
        
        if storage_type == StorageType.DYNAMODB_FLEXIBLE:
            try:
                from luminoracore_sdk.session import FlexibleDynamoDBStorageV11
                dynamodb_config = storage_config.get("dynamodb", {})
                return FlexibleDynamoDBStorageV11(
                    table_name=dynamodb_config.get("table_name"),
                    region_name=dynamodb_config.get("region"),
                    hash_key_name=dynamodb_config.get("hash_key"),
                    range_key_name=dynamodb_config.get("range_key")
                )
            except ImportError:
                raise ImportError("boto3 is required for DynamoDB storage")
        
        elif storage_type == StorageType.SQLITE_FLEXIBLE:
            try:
                from luminoracore_sdk.session import FlexibleSQLiteStorageV11
                sqlite_config = storage_config.get("sqlite", {})
                return FlexibleSQLiteStorageV11(
                    database_path=sqlite_config.get("database_path"),
                    facts_table=sqlite_config.get("facts_table"),
                    affinity_table=sqlite_config.get("affinity_table"),
                    episodes_table=sqlite_config.get("episodes_table"),
                    moods_table=sqlite_config.get("moods_table"),
                    memories_table=sqlite_config.get("memories_table")
                )
            except ImportError:
                raise ImportError("sqlite3 is required for SQLite storage")
        
        elif storage_type == StorageType.POSTGRESQL_FLEXIBLE:
            try:
                from luminoracore_sdk.session import FlexiblePostgreSQLStorageV11
                postgres_config = storage_config.get("postgresql", {})
                return FlexiblePostgreSQLStorageV11(
                    host=postgres_config.get("host"),
                    port=postgres_config.get("port"),
                    database=postgres_config.get("database"),
                    schema=postgres_config.get("schema"),
                    username=postgres_config.get("username"),
                    password=postgres_config.get("password"),
                    facts_table=postgres_config.get("facts_table"),
                    affinity_table=postgres_config.get("affinity_table"),
                    episodes_table=postgres_config.get("episodes_table"),
                    moods_table=postgres_config.get("moods_table"),
                    memories_table=postgres_config.get("memories_table")
                )
            except ImportError:
                raise ImportError("asyncpg is required for PostgreSQL storage")
        
        elif storage_type == StorageType.REDIS_FLEXIBLE:
            try:
                from luminoracore_sdk.session import FlexibleRedisStorageV11
                redis_config = storage_config.get("redis", {})
                return FlexibleRedisStorageV11(
                    host=redis_config.get("host"),
                    port=redis_config.get("port"),
                    db=redis_config.get("db"),
                    key_prefix=redis_config.get("key_prefix"),
                    affinity_key_pattern=redis_config.get("affinity_key_pattern"),
                    fact_key_pattern=redis_config.get("fact_key_pattern"),
                    episode_key_pattern=redis_config.get("episode_key_pattern"),
                    mood_key_pattern=redis_config.get("mood_key_pattern"),
                    memory_key_pattern=redis_config.get("memory_key_pattern")
                )
            except ImportError:
                raise ImportError("redis is required for Redis storage")
        
        elif storage_type == StorageType.MONGODB_FLEXIBLE:
            try:
                from luminoracore_sdk.session import FlexibleMongoDBStorageV11
                mongodb_config = storage_config.get("mongodb", {})
                return FlexibleMongoDBStorageV11(
                    host=mongodb_config.get("host"),
                    port=mongodb_config.get("port"),
                    database=mongodb_config.get("database"),
                    username=mongodb_config.get("username"),
                    password=mongodb_config.get("password"),
                    facts_collection=mongodb_config.get("facts_collection"),
                    affinity_collection=mongodb_config.get("affinity_collection"),
                    episodes_collection=mongodb_config.get("episodes_collection"),
                    moods_collection=mongodb_config.get("moods_collection"),
                    memories_collection=mongodb_config.get("memories_collection")
                )
            except ImportError:
                raise ImportError("motor is required for MongoDB storage")
        
        elif storage_type == StorageType.IN_MEMORY:
            try:
                from luminoracore_sdk.session import InMemoryStorageV11
                return InMemoryStorageV11()
            except ImportError:
                raise ImportError("InMemoryStorageV11 is required for in-memory storage")
        
        else:
            raise ValueError(f"Unsupported storage type: {storage_type}")
    
    def get_storage(self):
        """Get the configured storage instance"""
        return self.storage
    
    def get_config(self) -> StorageConfig:
        """Get the storage configuration"""
        return self.config
    
    def save_config(self, file_path: str):
        """Save configuration to file"""
        with open(file_path, 'w') as f:
            json.dump(self.config.to_dict(), f, indent=2)
    
    # USER MANAGEMENT METHODS
    def create_user_session(
        self,
        user_id: str = "demo",
        personality_name: str = "default",
        session_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new user session with proper user management
        
        Args:
            user_id: User ID (persistent across sessions) - defaults to "demo"
            personality_name: Name of the personality to use
            session_config: Session configuration (ttl, max_idle, etc.)
            
        Returns:
            Session ID
        """
        import uuid
        from datetime import datetime, timedelta
        
        # Default session configuration
        config = session_config or {}
        ttl = config.get("ttl", 3600)  # 1 hour default
        max_idle = config.get("max_idle", 1800)  # 30 minutes default
        
        # Generate unique session ID
        session_id = f"session_{uuid.uuid4().hex[:12]}_{int(datetime.now().timestamp())}"
        
        # Calculate expiration times
        created_at = datetime.now()
        expires_at = created_at + timedelta(seconds=ttl)
        last_activity = created_at
        
        # Store session information
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "personality_name": personality_name,
            "created_at": created_at.isoformat(),
            "expires_at": expires_at.isoformat(),
            "last_activity": last_activity.isoformat(),
            "status": "active",
            "config": config
        }
        
        # Store in session storage (if available)
        if hasattr(self.storage, 'save_session'):
            self.storage.save_session(
                session_id=session_id,
                user_id=user_id,
                personality_name=personality_name,
                created_at=created_at.isoformat(),
                expires_at=expires_at.isoformat(),
                last_activity=last_activity.isoformat(),
                status="active"
            )
        
        return session_id
    
    def get_user_context(
        self,
        user_id: str,
        personality_name: str = "default"
    ) -> Dict[str, Any]:
        """
        Get complete user context for personalized interactions
        
        Args:
            user_id: User ID
            personality_name: Personality name
            
        Returns:
            Complete user context
        """
        context = {
            "user_id": user_id,
            "personality_name": personality_name,
            "facts": [],
            "affinity": {},
            "sentiment_history": [],
            "personality_evolution": {}
        }
        
        if hasattr(self.storage, 'get_facts'):
            try:
                context["facts"] = self.storage.get_facts(user_id)
            except:
                pass
        
        if hasattr(self.storage, 'get_affinity'):
            try:
                context["affinity"] = self.storage.get_affinity(user_id, personality_name)
            except:
                pass
        
        if hasattr(self.storage, 'get_mood'):
            try:
                context["sentiment_history"] = self.storage.get_mood(user_id)
            except:
                pass
        
        return context
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions
        
        Returns:
            Number of sessions cleaned up
        """
        if not hasattr(self.storage, 'get_expired_sessions'):
            return 0
        
        try:
            expired_sessions = self.storage.get_expired_sessions()
            cleaned_count = 0
            
            for session_id in expired_sessions:
                if hasattr(self.storage, 'delete_session'):
                    if self.storage.delete_session(session_id):
                        cleaned_count += 1
            
            return cleaned_count
        except:
            return 0
    
    @classmethod
    def from_config_file(cls, file_path: str) -> "FlexibleStorageManager":
        """Create FlexibleStorageManager from configuration file"""
        with open(file_path, 'r') as f:
            config_data = json.load(f)
        return cls(config_data)
