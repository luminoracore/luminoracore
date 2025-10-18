"""
MySQL Storage v1.1 Implementation

Real MySQL implementation for v1.1 storage with persistent data.
"""

import asyncio
import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

try:
    import aiomysql
    from aiomysql import Connection, Cursor
except ImportError:
    aiomysql = None
    Connection = None
    Cursor = None

from .storage_v1_1 import StorageV11Extension

logger = logging.getLogger(__name__)


class MySQLStorageV11(StorageV11Extension):
    """
    Real MySQL storage implementation for v1.1 features
    """
    
    def __init__(self, host: str = "localhost", port: int = 3306, user: str = "root", 
                 password: str = "", database: str = "luminoracore_v11", charset: str = "utf8mb4"):
        """
        Initialize MySQL storage
        
        Args:
            host: MySQL host
            port: MySQL port
            user: MySQL user
            password: MySQL password
            database: Database name
            charset: Character set
        """
        if aiomysql is None:
            raise ImportError("aiomysql is required for MySQL storage. Install with: pip install aiomysql")
        
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.pool = None
        self._ensure_initialized = False
    
    async def _ensure_initialized(self):
        """Ensure database connection and tables exist"""
        if self._ensure_initialized:
            return
        
        try:
            # Create connection pool
            self.pool = await aiomysql.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.database,
                charset=self.charset,
                minsize=1,
                maxsize=10
            )
            
            # Create tables
            async with self.pool.acquire() as conn:
                await self._create_tables(conn)
            
            self._ensure_initialized = True
            logger.info("MySQL database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize MySQL database: {e}")
            raise
    
    async def _create_tables(self, conn: Connection):
        """Create all required tables"""
        async with conn.cursor() as cursor:
            # Create affinity table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_affinity (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    personality_name VARCHAR(255) NOT NULL,
                    affinity_points INT DEFAULT 0,
                    current_level VARCHAR(50) DEFAULT 'stranger',
                    total_interactions INT DEFAULT 0,
                    positive_interactions INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_user_personality (user_id, personality_name)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Create facts table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_facts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    key_name VARCHAR(255) NOT NULL,
                    value TEXT NOT NULL,
                    confidence FLOAT DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_user_category_key (user_id, category, key_name)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Create episodes table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_episodes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    episode_type VARCHAR(100) NOT NULL,
                    title VARCHAR(500) NOT NULL,
                    summary TEXT NOT NULL,
                    importance FLOAT NOT NULL,
                    sentiment VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_user_importance (user_id, importance DESC)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Create mood table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_mood (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    session_id VARCHAR(255) NOT NULL,
                    user_id VARCHAR(255) NOT NULL,
                    current_mood VARCHAR(100) NOT NULL,
                    mood_intensity FLOAT DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_user_mood (user_id, created_at DESC)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Create memory table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_memory (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    session_id VARCHAR(255) NOT NULL,
                    user_id VARCHAR(255) NOT NULL,
                    memory_key VARCHAR(255) NOT NULL,
                    memory_value TEXT NOT NULL,
                    expires_at TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_session_key (session_id, memory_key),
                    INDEX idx_session (session_id),
                    INDEX idx_expires (expires_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
        
        await conn.commit()
    
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
                async with conn.cursor() as cursor:
                    await cursor.execute("""
                        INSERT INTO user_affinity 
                        (user_id, personality_name, affinity_points, current_level, updated_at)
                        VALUES (%s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            affinity_points = VALUES(affinity_points),
                            current_level = VALUES(current_level),
                            updated_at = VALUES(updated_at)
                    """, (user_id, personality_name, affinity_points, current_level, datetime.now()))
                    await conn.commit()
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
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute("""
                        SELECT affinity_points, current_level, total_interactions, 
                               positive_interactions, created_at, updated_at
                        FROM user_affinity 
                        WHERE user_id = %s AND personality_name = %s
                    """, (user_id, personality_name))
                    
                    row = await cursor.fetchone()
                    if row:
                        # Convert datetime objects to ISO format strings
                        if row.get('created_at'):
                            row['created_at'] = row['created_at'].isoformat()
                        if row.get('updated_at'):
                            row['updated_at'] = row['updated_at'].isoformat()
                        return row
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
                async with conn.cursor() as cursor:
                    await cursor.execute("""
                        INSERT INTO user_facts 
                        (user_id, category, key_name, value, confidence, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            value = VALUES(value),
                            confidence = VALUES(confidence),
                            updated_at = VALUES(updated_at)
                    """, (user_id, category, key, value_str, confidence, datetime.now()))
                    await conn.commit()
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
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    if category:
                        await cursor.execute("""
                            SELECT category, key_name as key, value, confidence, created_at, updated_at
                            FROM user_facts 
                            WHERE user_id = %s AND category = %s
                            ORDER BY created_at DESC
                        """, (user_id, category))
                    else:
                        await cursor.execute("""
                            SELECT category, key_name as key, value, confidence, created_at, updated_at
                            FROM user_facts 
                            WHERE user_id = %s
                            ORDER BY created_at DESC
                        """, (user_id,))
                    
                    rows = await cursor.fetchall()
                    facts = []
                    
                    for row in rows:
                        try:
                            value = json.loads(row['value']) if row['value'].startswith(('{', '[', '"')) else row['value']
                        except:
                            value = row['value']
                        
                        # Convert datetime objects to ISO format strings
                        if row.get('created_at'):
                            row['created_at'] = row['created_at'].isoformat()
                        if row.get('updated_at'):
                            row['updated_at'] = row['updated_at'].isoformat()
                        
                        row['value'] = value
                        facts.append(row)
                    
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
                async with conn.cursor() as cursor:
                    await cursor.execute("""
                        INSERT INTO user_episodes 
                        (user_id, episode_type, title, summary, importance, sentiment)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (user_id, episode_type, title, summary, importance, sentiment))
                    await conn.commit()
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
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    if min_importance is not None:
                        await cursor.execute("""
                            SELECT episode_type, title, summary, importance, sentiment, created_at
                            FROM user_episodes 
                            WHERE user_id = %s AND importance >= %s
                            ORDER BY importance DESC, created_at DESC
                        """, (user_id, min_importance))
                    else:
                        await cursor.execute("""
                            SELECT episode_type, title, summary, importance, sentiment, created_at
                            FROM user_episodes 
                            WHERE user_id = %s
                            ORDER BY importance DESC, created_at DESC
                        """, (user_id,))
                    
                    rows = await cursor.fetchall()
                    episodes = []
                    
                    for row in rows:
                        # Convert datetime objects to ISO format strings
                        if row.get('created_at'):
                            row['created_at'] = row['created_at'].isoformat()
                        episodes.append(row)
                    
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
                async with conn.cursor() and cursor:
                    await cursor.execute("""
                        INSERT INTO user_mood 
                        (session_id, user_id, current_mood, mood_intensity)
                        VALUES (%s, %s, %s, %s)
                    """, (session_id, user_id, current_mood, mood_intensity))
                    await conn.commit()
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
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute("""
                        SELECT session_id, current_mood, mood_intensity, created_at
                        FROM user_mood 
                        WHERE user_id = %s
                        ORDER BY created_at DESC
                        LIMIT %s
                    """, (user_id, limit))
                    
                    rows = await cursor.fetchall()
                    moods = []
                    
                    for row in rows:
                        # Convert datetime objects to ISO format strings
                        if row.get('created_at'):
                            row['created_at'] = row['created_at'].isoformat()
                        moods.append(row)
                    
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
                async with conn.cursor() as cursor:
                    await cursor.execute("""
                        INSERT INTO conversation_memory 
                        (session_id, user_id, memory_key, memory_value, expires_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            memory_value = VALUES(memory_value),
                            expires_at = VALUES(expires_at),
                            updated_at = VALUES(updated_at)
                    """, (session_id, user_id, key, value_str, expires_at, datetime.now()))
                    await conn.commit()
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
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute("""
                        SELECT memory_value, expires_at
                        FROM conversation_memory 
                        WHERE session_id = %s AND memory_key = %s
                    """, (session_id, key))
                    
                    row = await cursor.fetchone()
                    if row:
                        # Check if expired
                        if row['expires_at'] and row['expires_at'] < datetime.now():
                            return None
                        
                        try:
                            return json.loads(row['memory_value'])
                        except:
                            return row['memory_value']
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
                async with conn.cursor() as cursor:
                    await cursor.execute("""
                        DELETE FROM conversation_memory 
                        WHERE session_id = %s AND memory_key = %s
                    """, (session_id, key))
                    await conn.commit()
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
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute("""
                        SELECT memory_key, memory_value, expires_at
                        FROM conversation_memory 
                        WHERE session_id = %s
                    """, (session_id,))
                    
                    rows = await cursor.fetchall()
                    memories = {}
                    
                    for row in rows:
                        # Check if expired
                        if row['expires_at'] and row['expires_at'] < datetime.now():
                            continue
                        
                        try:
                            memories[row['memory_key']] = json.loads(row['memory_value'])
                        except:
                            memories[row['memory_key']] = row['memory_value']
                    
                    return memories
            finally:
                await self.pool.release(conn)
        except Exception as e:
            logger.error(f"Failed to get all memories: {e}")
            return {}
    
    async def close(self):
        """Close MySQL connection pool"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
