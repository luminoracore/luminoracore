"""
PostgreSQL Storage v1.1 Implementation

Real PostgreSQL implementation for v1.1 storage with persistent data.
"""

import asyncio
import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

try:
    import asyncpg
    from asyncpg import Connection, Pool
except ImportError:
    asyncpg = None
    Connection = None
    Pool = None

from .storage_v1_1 import StorageV11Extension

logger = logging.getLogger(__name__)


class PostgreSQLStorageV11(StorageV11Extension):
    """
    Real PostgreSQL storage implementation for v1.1 features
    """
    
    def __init__(self, connection_string: str, min_connections: int = 1, max_connections: int = 10):
        """
        Initialize PostgreSQL storage
        
        Args:
            connection_string: PostgreSQL connection string
            min_connections: Minimum connections in pool
            max_connections: Maximum connections in pool
        """
        if asyncpg is None:
            raise ImportError("asyncpg is required for PostgreSQL storage. Install with: pip install asyncpg")
        
        self.connection_string = connection_string
        self.min_connections = min_connections
        self.max_connections = max_connections
        self.pool: Optional[Pool] = None
        self._ensure_initialized = False
    
    async def _ensure_initialized(self):
        """Ensure database connection and tables exist"""
        if self._ensure_initialized:
            return
        
        try:
            # Create connection pool
            self.pool = await asyncpg.create_pool(
                self.connection_string,
                min_size=self.min_connections,
                max_size=self.max_connections
            )
            
            # Create tables
            async with self.pool.acquire() as conn:
                await self._create_tables(conn)
            
            self._ensure_initialized = True
            logger.info("PostgreSQL database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL database: {e}")
            raise
    
    async def _create_tables(self, conn: Connection):
        """Create all required tables"""
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS user_affinity (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                personality_name VARCHAR(255) NOT NULL,
                affinity_points INTEGER DEFAULT 0,
                current_level VARCHAR(50) DEFAULT 'stranger',
                total_interactions INTEGER DEFAULT 0,
                positive_interactions INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, personality_name)
            )
        """)
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS user_facts (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                category VARCHAR(100) NOT NULL,
                key VARCHAR(255) NOT NULL,
                value TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, category, key)
            )
        """)
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS user_episodes (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                episode_type VARCHAR(100) NOT NULL,
                title VARCHAR(500) NOT NULL,
                summary TEXT NOT NULL,
                importance REAL NOT NULL,
                sentiment VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS user_mood (
                id SERIAL PRIMARY KEY,
                session_id VARCHAR(255) NOT NULL,
                user_id VARCHAR(255) NOT NULL,
                current_mood VARCHAR(100) NOT NULL,
                mood_intensity REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS conversation_memory (
                id SERIAL PRIMARY KEY,
                session_id VARCHAR(255) NOT NULL,
                user_id VARCHAR(255) NOT NULL,
                memory_key VARCHAR(255) NOT NULL,
                memory_value TEXT NOT NULL,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(session_id, memory_key)
            )
        """)
        
        # Create indexes for better performance
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_user_affinity_user_id ON user_affinity(user_id)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_user_facts_user_id ON user_facts(user_id)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_user_facts_category ON user_facts(category)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_user_episodes_user_id ON user_episodes(user_id)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_user_episodes_importance ON user_episodes(importance DESC)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_user_mood_user_id ON user_mood(user_id)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_conversation_memory_session ON conversation_memory(session_id)")
    
    async def _get_connection(self) -> Connection:
        """Get database connection from pool"""
        await self._ensure_initialized()
        return await self.pool.acquire()
    
    # AFFINITY METHODS
    async def save_affinity(
        self,
        user_id: str,
        personality_name: str,
        affinity_points: int,
        current_level: str,
        **kwargs
    ) -> bool:
        """Save or update user affinity"""
        try:
            conn = await self._get_connection()
            try:
                await conn.execute("""
                    INSERT INTO user_affinity 
                    (user_id, personality_name, affinity_points, current_level, updated_at)
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT (user_id, personality_name) 
                    DO UPDATE SET 
                        affinity_points = EXCLUDED.affinity_points,
                        current_level = EXCLUDED.current_level,
                        updated_at = EXCLUDED.updated_at
                """, user_id, personality_name, affinity_points, current_level, datetime.now())
                return True
            finally:
                await self.pool.release(conn)
        except Exception as e:
            logger.error(f"Failed to save affinity: {e}")
            return False
    
    async def get_affinity(
        self,
        user_id: str,
        personality_name: str
    ) -> Optional[Dict[str, Any]]:
        """Get user affinity data"""
        try:
            conn = await self._get_connection()
            try:
                row = await conn.fetchrow("""
                    SELECT affinity_points, current_level, total_interactions, 
                           positive_interactions, created_at, updated_at
                    FROM user_affinity 
                    WHERE user_id = $1 AND personality_name = $2
                """, user_id, personality_name)
                
                if row:
                    return {
                        "affinity_points": row["affinity_points"],
                        "current_level": row["current_level"],
                        "total_interactions": row["total_interactions"],
                        "positive_interactions": row["positive_interactions"],
                        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
                        "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None
                    }
                return None
            finally:
                await self.pool.release(conn)
        except Exception as e:
            logger.error(f"Failed to get affinity: {e}")
            return None
    
    # FACT METHODS
    async def save_fact(
        self,
        user_id: str,
        category: str,
        key: str,
        value: Any,
        **kwargs
    ) -> bool:
        """Save a user fact"""
        try:
            confidence = kwargs.get('confidence', 1.0)
            value_str = json.dumps(value) if not isinstance(value, str) else value
            
            conn = await self._get_connection()
            try:
                await conn.execute("""
                    INSERT INTO user_facts 
                    (user_id, category, key, value, confidence, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    ON CONFLICT (user_id, category, key) 
                    DO UPDATE SET 
                        value = EXCLUDED.value,
                        confidence = EXCLUDED.confidence,
                        updated_at = EXCLUDED.updated_at
                """, user_id, category, key, value_str, confidence, datetime.now())
                return True
            finally:
                await self.pool.release(conn)
        except Exception as e:
            logger.error(f"Failed to save fact: {e}")
            return False
    
    async def get_facts(
        self,
        user_id: str,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get user facts, optionally filtered by category"""
        try:
            conn = await self._get_connection()
            try:
                if category:
                    rows = await conn.fetch("""
                        SELECT category, key, value, confidence, created_at, updated_at
                        FROM user_facts 
                        WHERE user_id = $1 AND category = $2
                        ORDER BY created_at DESC
                    """, user_id, category)
                else:
                    rows = await conn.fetch("""
                        SELECT category, key, value, confidence, created_at, updated_at
                        FROM user_facts 
                        WHERE user_id = $1
                        ORDER BY created_at DESC
                    """, user_id)
                
                facts = []
                for row in rows:
                    try:
                        value = json.loads(row["value"]) if row["value"].startswith(('{', '[', '"')) else row["value"]
                    except:
                        value = row["value"]
                    
                    facts.append({
                        "category": row["category"],
                        "key": row["key"],
                        "value": value,
                        "confidence": row["confidence"],
                        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
                        "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None
                    })
                
                return facts
            finally:
                await self.pool.release(conn)
        except Exception as e:
            logger.error(f"Failed to get facts: {e}")
            return []
    
    # EPISODE METHODS
    async def save_episode(
        self,
        user_id: str,
        episode_type: str,
        title: str,
        summary: str,
        importance: float,
        sentiment: str,
        **kwargs
    ) -> bool:
        """Save an episode"""
        try:
            conn = await self._get_connection()
            try:
                await conn.execute("""
                    INSERT INTO user_episodes 
                    (user_id, episode_type, title, summary, importance, sentiment)
                    VALUES ($1, $2, $3, $4, $5, $6)
                """, user_id, episode_type, title, summary, importance, sentiment)
                return True
            finally:
                await self.pool.release(conn)
        except Exception as e:
            logger.error(f"Failed to save episode: {e}")
            return False
    
    async def get_episodes(
        self,
        user_id: str,
        min_importance: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Get episodes, optionally filtered by importance"""
        try:
            conn = await self._get_connection()
            try:
                if min_importance is not None:
                    rows = await conn.fetch("""
                        SELECT episode_type, title, summary, importance, sentiment, created_at
                        FROM user_episodes 
                        WHERE user_id = $1 AND importance >= $2
                        ORDER BY importance DESC, created_at DESC
                    """, user_id, min_importance)
                else:
                    rows = await conn.fetch("""
                        SELECT episode_type, title, summary, importance, sentiment, created_at
                        FROM user_episodes 
                        WHERE user_id = $1
                        ORDER BY importance DESC, created_at DESC
                    """, user_id)
                
                episodes = []
                for row in rows:
                    episodes.append({
                        "episode_type": row["episode_type"],
                        "title": row["title"],
                        "summary": row["summary"],
                        "importance": row["importance"],
                        "sentiment": row["sentiment"],
                        "created_at": row["created_at"].isoformat() if row["created_at"] else None
                    })
                
                return episodes
            finally:
                await self.pool.release(conn)
        except Exception as e:
            logger.error(f"Failed to get episodes: {e}")
            return []
    
    # MOOD METHODS
    async def save_mood(
        self,
        session_id: str,
        user_id: str,
        current_mood: str,
        mood_intensity: float = 1.0
    ) -> bool:
        """Save current mood state"""
        try:
            conn = await self._get_connection()
            try:
                await conn.execute("""
                    INSERT INTO user_mood 
                    (session_id, user_id, current_mood, mood_intensity)
                    VALUES ($1, $2, $3, $4)
                """, session_id, user_id, current_mood, mood_intensity)
                return True
            finally:
                await self.pool.release(conn)
        except Exception as e:
            logger.error(f"Failed to save mood: {e}")
            return False
    
    async def get_mood_history(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get mood history for user"""
        try:
            conn = await self._get_connection()
            try:
                rows = await conn.fetch("""
                    SELECT session_id, current_mood, mood_intensity, created_at
                    FROM user_mood 
                    WHERE user_id = $1
                    ORDER BY created_at DESC
                    LIMIT $2
                """, user_id, limit)
                
                moods = []
                for row in rows:
                    moods.append({
                        "session_id": row["session_id"],
                        "current_mood": row["current_mood"],
                        "mood_intensity": row["mood_intensity"],
                        "created_at": row["created_at"].isoformat() if row["created_at"] else None
                    })
                
                return moods
            finally:
                await self.pool.release(conn)
        except Exception as e:
            logger.error(f"Failed to get mood history: {e}")
            return []
    
    # MEMORY METHODS
    async def save_memory(
        self,
        session_id: str,
        user_id: str,
        key: str,
        value: Any,
        expires_at: Optional[datetime] = None
    ) -> bool:
        """Save conversation memory"""
        try:
            value_str = json.dumps(value) if not isinstance(value, str) else value
            
            conn = await self._get_connection()
            try:
                await conn.execute("""
                    INSERT INTO conversation_memory 
                    (session_id, user_id, memory_key, memory_value, expires_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    ON CONFLICT (session_id, memory_key) 
                    DO UPDATE SET 
                        memory_value = EXCLUDED.memory_value,
                        expires_at = EXCLUDED.expires_at,
                        updated_at = EXCLUDED.updated_at
                """, session_id, user_id, key, value_str, expires_at, datetime.now())
                return True
            finally:
                await self.pool.release(conn)
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")
            return False
    
    async def get_memory(
        self,
        session_id: str,
        key: str
    ) -> Optional[Any]:
        """Get conversation memory"""
        try:
            conn = await self._get_connection()
            try:
                row = await conn.fetchrow("""
                    SELECT memory_value, expires_at
                    FROM conversation_memory 
                    WHERE session_id = $1 AND memory_key = $2
                """, session_id, key)
                
                if row:
                    # Check if expired
                    if row["expires_at"] and row["expires_at"] < datetime.now():
                        return None
                    
                    try:
                        return json.loads(row["memory_value"])
                    except:
                        return row["memory_value"]
                return None
            finally:
                await self.pool.release(conn)
        except Exception as e:
            logger.error(f"Failed to get memory: {e}")
            return None
    
    async def delete_memory(
        self,
        session_id: str,
        key: str
    ) -> bool:
        """Delete conversation memory"""
        try:
            conn = await self._get_connection()
            try:
                await conn.execute("""
                    DELETE FROM conversation_memory 
                    WHERE session_id = $1 AND memory_key = $2
                """, session_id, key)
                return True
            finally:
                await self.pool.release(conn)
        except Exception as e:
            logger.error(f"Failed to delete memory: {e}")
            return False
    
    async def get_all_memories(
        self,
        session_id: str
    ) -> Dict[str, Any]:
        """Get all memories for a session"""
        try:
            conn = await self._get_connection()
            try:
                rows = await conn.fetch("""
                    SELECT memory_key, memory_value, expires_at
                    FROM conversation_memory 
                    WHERE session_id = $1
                """, session_id)
                
                memories = {}
                for row in rows:
                    # Check if expired
                    if row["expires_at"] and row["expires_at"] < datetime.now():
                        continue
                    
                    try:
                        memories[row["memory_key"]] = json.loads(row["memory_value"])
                    except:
                        memories[row["memory_key"]] = row["memory_value"]
                
                return memories
            finally:
                await self.pool.release(conn)
        except Exception as e:
            logger.error(f"Failed to get all memories: {e}")
            return {}
    
    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
