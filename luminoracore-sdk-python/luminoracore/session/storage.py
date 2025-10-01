"""Storage backend for LuminoraCore SDK."""

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import logging
from datetime import datetime

from ..types.session import StorageConfig, StorageType
from ..utils.exceptions import StorageError

logger = logging.getLogger(__name__)


class SessionStorage(ABC):
    """Abstract base class for session storage backends."""
    
    def __init__(self, config: StorageConfig):
        """
        Initialize the storage backend.
        
        Args:
            config: Storage configuration
        """
        self.config = config
        self.storage_type = config.storage_type
    
    @abstractmethod
    async def save_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """
        Save session data.
        
        Args:
            session_id: Session ID
            session_data: Session data to save
            
        Returns:
            True if saved successfully
        """
        pass
    
    @abstractmethod
    async def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load session data.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session data or None if not found
        """
        pass
    
    @abstractmethod
    async def delete_session(self, session_id: str) -> bool:
        """
        Delete session data.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if deleted successfully
        """
        pass
    
    @abstractmethod
    async def list_sessions(self) -> List[str]:
        """
        List all session IDs.
        
        Returns:
            List of session IDs
        """
        pass
    
    @abstractmethod
    async def session_exists(self, session_id: str) -> bool:
        """
        Check if session exists.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if session exists
        """
        pass


class InMemoryStorage(SessionStorage):
    """In-memory storage implementation."""
    
    def __init__(self, config: StorageConfig):
        """Initialize in-memory storage."""
        super().__init__(config)
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()
    
    async def save_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Save session data to memory."""
        async with self._lock:
            self._sessions[session_id] = session_data.copy()
        return True
    
    async def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session data from memory."""
        async with self._lock:
            return self._sessions.get(session_id)
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete session data from memory."""
        async with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                return True
        return False
    
    async def list_sessions(self) -> List[str]:
        """List all session IDs in memory."""
        async with self._lock:
            return list(self._sessions.keys())
    
    async def session_exists(self, session_id: str) -> bool:
        """Check if session exists in memory."""
        async with self._lock:
            return session_id in self._sessions


class RedisStorage(SessionStorage):
    """Redis storage implementation."""
    
    def __init__(self, config: StorageConfig):
        """Initialize Redis storage."""
        super().__init__(config)
        self.redis_url = config.connection_string or "redis://localhost:6379"
        self._redis = None
    
    async def _get_redis(self):
        """Get Redis connection."""
        if self._redis is None:
            import redis.asyncio as redis
            self._redis = redis.from_url(self.redis_url)
        return self._redis
    
    async def save_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Save session data to Redis."""
        try:
            redis_client = await self._get_redis()
            key = f"session:{session_id}"
            
            # Serialize session data
            import json
            serialized_data = json.dumps(session_data, default=str)
            
            # Save with TTL if configured
            if hasattr(self.config, 'ttl') and self.config.ttl:
                await redis_client.setex(key, self.config.ttl, serialized_data)
            else:
                await redis_client.set(key, serialized_data)
            
            return True
        except Exception as e:
            logger.error(f"Failed to save session to Redis: {e}")
            raise StorageError(f"Redis save failed: {e}")
    
    async def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session data from Redis."""
        try:
            redis_client = await self._get_redis()
            key = f"session:{session_id}"
            
            serialized_data = await redis_client.get(key)
            if not serialized_data:
                return None
            
            # Deserialize session data
            import json
            return json.loads(serialized_data)
            
        except Exception as e:
            logger.error(f"Failed to load session from Redis: {e}")
            raise StorageError(f"Redis load failed: {e}")
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete session data from Redis."""
        try:
            redis_client = await self._get_redis()
            key = f"session:{session_id}"
            
            result = await redis_client.delete(key)
            return result > 0
            
        except Exception as e:
            logger.error(f"Failed to delete session from Redis: {e}")
            raise StorageError(f"Redis delete failed: {e}")
    
    async def list_sessions(self) -> List[str]:
        """List all session IDs from Redis."""
        try:
            redis_client = await self._get_redis()
            keys = await redis_client.keys("session:*")
            return [key.decode('utf-8').replace("session:", "") for key in keys]
            
        except Exception as e:
            logger.error(f"Failed to list sessions from Redis: {e}")
            raise StorageError(f"Redis list failed: {e}")
    
    async def session_exists(self, session_id: str) -> bool:
        """Check if session exists in Redis."""
        try:
            redis_client = await self._get_redis()
            key = f"session:{session_id}"
            return await redis_client.exists(key) > 0
            
        except Exception as e:
            logger.error(f"Failed to check session existence in Redis: {e}")
            raise StorageError(f"Redis exists check failed: {e}")


class PostgreSQLStorage(SessionStorage):
    """PostgreSQL storage implementation."""
    
    def __init__(self, config: StorageConfig):
        """Initialize PostgreSQL storage."""
        super().__init__(config)
        self.postgres_url = config.connection_string or "postgresql://localhost/luminoracore"
        self._pool = None
    
    async def _get_pool(self):
        """Get PostgreSQL connection pool."""
        if self._pool is None:
            import asyncpg
            self._pool = await asyncpg.create_pool(self.postgres_url)
        return self._pool
    
    async def _ensure_table_exists(self):
        """Ensure the sessions table exists."""
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id VARCHAR(255) PRIMARY KEY,
                    session_data JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    async def save_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Save session data to PostgreSQL."""
        try:
            await self._ensure_table_exists()
            pool = await self._get_pool()
            
            async with pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO sessions (session_id, session_data, updated_at)
                    VALUES ($1, $2, CURRENT_TIMESTAMP)
                    ON CONFLICT (session_id)
                    DO UPDATE SET
                        session_data = $2,
                        updated_at = CURRENT_TIMESTAMP
                """, session_id, session_data)
            
            return True
        except Exception as e:
            logger.error(f"Failed to save session to PostgreSQL: {e}")
            raise StorageError(f"PostgreSQL save failed: {e}")
    
    async def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session data from PostgreSQL."""
        try:
            pool = await self._get_pool()
            
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT session_data FROM sessions WHERE session_id = $1",
                    session_id
                )
                
                if row:
                    return row['session_data']
                return None
                
        except Exception as e:
            logger.error(f"Failed to load session from PostgreSQL: {e}")
            raise StorageError(f"PostgreSQL load failed: {e}")
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete session data from PostgreSQL."""
        try:
            pool = await self._get_pool()
            
            async with pool.acquire() as conn:
                result = await conn.execute(
                    "DELETE FROM sessions WHERE session_id = $1",
                    session_id
                )
                
                return result == "DELETE 1"
                
        except Exception as e:
            logger.error(f"Failed to delete session from PostgreSQL: {e}")
            raise StorageError(f"PostgreSQL delete failed: {e}")
    
    async def list_sessions(self) -> List[str]:
        """List all session IDs from PostgreSQL."""
        try:
            pool = await self._get_pool()
            
            async with pool.acquire() as conn:
                rows = await conn.fetch("SELECT session_id FROM sessions")
                return [row['session_id'] for row in rows]
                
        except Exception as e:
            logger.error(f"Failed to list sessions from PostgreSQL: {e}")
            raise StorageError(f"PostgreSQL list failed: {e}")
    
    async def session_exists(self, session_id: str) -> bool:
        """Check if session exists in PostgreSQL."""
        try:
            pool = await self._get_pool()
            
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT 1 FROM sessions WHERE session_id = $1",
                    session_id
                )
                
                return row is not None
                
        except Exception as e:
            logger.error(f"Failed to check session existence in PostgreSQL: {e}")
            raise StorageError(f"PostgreSQL exists check failed: {e}")


class MongoDBStorage(SessionStorage):
    """MongoDB storage implementation."""
    
    def __init__(self, config: StorageConfig):
        """Initialize MongoDB storage."""
        super().__init__(config)
        self.mongodb_url = config.connection_string or "mongodb://localhost:27017/luminoracore"
        self._client = None
        self._db = None
    
    async def _get_db(self):
        """Get MongoDB database."""
        if self._client is None:
            import motor.motor_asyncio
            self._client = motor.motor_asyncio.AsyncIOMotorClient(self.mongodb_url)
            self._db = self._client.luminoracore
        
        return self._db
    
    async def save_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Save session data to MongoDB."""
        try:
            db = await self._get_db()
            collection = db.sessions
            
            # Add timestamp
            session_data['updated_at'] = datetime.utcnow()
            
            await collection.replace_one(
                {"session_id": session_id},
                {"session_id": session_id, "session_data": session_data},
                upsert=True
            )
            
            return True
        except Exception as e:
            logger.error(f"Failed to save session to MongoDB: {e}")
            raise StorageError(f"MongoDB save failed: {e}")
    
    async def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session data from MongoDB."""
        try:
            db = await self._get_db()
            collection = db.sessions
            
            document = await collection.find_one({"session_id": session_id})
            if document:
                return document['session_data']
            return None
            
        except Exception as e:
            logger.error(f"Failed to load session from MongoDB: {e}")
            raise StorageError(f"MongoDB load failed: {e}")
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete session data from MongoDB."""
        try:
            db = await self._get_db()
            collection = db.sessions
            
            result = await collection.delete_one({"session_id": session_id})
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Failed to delete session from MongoDB: {e}")
            raise StorageError(f"MongoDB delete failed: {e}")
    
    async def list_sessions(self) -> List[str]:
        """List all session IDs from MongoDB."""
        try:
            db = await self._get_db()
            collection = db.sessions
            
            cursor = collection.find({}, {"session_id": 1})
            sessions = await cursor.to_list(length=None)
            return [session['session_id'] for session in sessions]
            
        except Exception as e:
            logger.error(f"Failed to list sessions from MongoDB: {e}")
            raise StorageError(f"MongoDB list failed: {e}")
    
    async def session_exists(self, session_id: str) -> bool:
        """Check if session exists in MongoDB."""
        try:
            db = await self._get_db()
            collection = db.sessions
            
            count = await collection.count_documents({"session_id": session_id})
            return count > 0
            
        except Exception as e:
            logger.error(f"Failed to check session existence in MongoDB: {e}")
            raise StorageError(f"MongoDB exists check failed: {e}")


def create_storage(config: StorageConfig) -> SessionStorage:
    """
    Create a storage backend from configuration.
    
    Args:
        config: Storage configuration
        
    Returns:
        Storage backend instance
        
    Raises:
        StorageError: If storage type is not supported
    """
    if config.storage_type == StorageType.MEMORY:
        return InMemoryStorage(config)
    elif config.storage_type == StorageType.REDIS:
        return RedisStorage(config)
    elif config.storage_type == StorageType.POSTGRES:
        return PostgreSQLStorage(config)
    elif config.storage_type == StorageType.MONGODB:
        return MongoDBStorage(config)
    else:
        raise StorageError(f"Unsupported storage type: {config.storage_type}")
