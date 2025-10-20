"""
Flexible PostgreSQL Storage v11 Implementation

This implementation allows users to use ANY PostgreSQL database with ANY schema.
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


class FlexiblePostgreSQLStorageV11(StorageV11Extension):
    """
    Flexible PostgreSQL storage that adapts to ANY database schema
    
    The user can use their own PostgreSQL databases with any schema.
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        user: str = "postgres",
        password: str = "",
        database: str = "luminoracore_v11",
        schema: str = "public",
        facts_table: str = None,
        affinity_table: str = None,
        episodes_table: str = None,
        moods_table: str = None,
        memories_table: str = None,
        pool_size: int = 10,
        max_overflow: int = 20,
        auto_create_tables: bool = True
    ):
        """
        Initialize flexible PostgreSQL storage
        
        Args:
            host: PostgreSQL host
            port: PostgreSQL port
            user: PostgreSQL user
            password: PostgreSQL password
            database: Database name (user's database)
            schema: Schema name (user's schema)
            facts_table: Name of facts table (auto-detected if None)
            affinity_table: Name of affinity table (auto-detected if None)
            episodes_table: Name of episodes table (auto-detected if None)
            moods_table: Name of moods table (auto-detected if None)
            memories_table: Name of memories table (auto-detected if None)
            pool_size: Connection pool size
            max_overflow: Maximum overflow connections
            auto_create_tables: Whether to create tables if they don't exist
        """
        if asyncpg is None:
            raise ImportError("asyncpg is required for PostgreSQL storage. Install with: pip install asyncpg")
        
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.schema = schema
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.auto_create_tables = auto_create_tables
        
        # Table names (user's choice or auto-detected)
        self.facts_table = facts_table
        self.affinity_table = affinity_table
        self.episodes_table = episodes_table
        self.moods_table = moods_table
        self.memories_table = memories_table
        
        self.pool: Optional[Pool] = None
        self._initialized = False
        
        logger.info(f"Flexible PostgreSQL storage initialized for database: {database}")
    
    async def _ensure_initialized(self):
        """Ensure database connection and tables exist"""
        if self._initialized:
            return
        
        try:
            # Create connection pool
            self.pool = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                min_size=1,
                max_size=self.pool_size + self.max_overflow
            )
            
            # Auto-detect table names if not provided
            await self._detect_tables()
            
            # Create tables if needed
            if self.auto_create_tables:
                await self._ensure_tables_exist()
            
            self._initialized = True
            logger.info(f"PostgreSQL connection established. Tables: {self.facts_table}, {self.affinity_table}")
            
        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL storage: {e}")
            raise
    
    async def _detect_tables(self):
        """Auto-detect table names from existing database"""
        try:
            async with self.pool.acquire() as conn:
                # Get existing tables in the schema
                query = """
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = $1
                """
                rows = await conn.fetch(query, self.schema)
                existing_tables = [row['table_name'] for row in rows]
                
                # Common table name patterns
                if not self.facts_table:
                    possible_names = ['facts', 'user_facts', 'luminora_facts', 'facts_table']
                    self.facts_table = next((name for name in possible_names if name in existing_tables), 'facts')
                
                if not self.affinity_table:
                    possible_names = ['affinity', 'user_affinity', 'luminora_affinity', 'affinity_table']
                    self.affinity_table = next((name for name in possible_names if name in existing_tables), 'affinity')
                
                if not self.episodes_table:
                    possible_names = ['episodes', 'user_episodes', 'luminora_episodes', 'episodes_table']
                    self.episodes_table = next((name for name in possible_names if name in existing_tables), 'episodes')
                
                if not self.moods_table:
                    possible_names = ['moods', 'user_moods', 'luminora_moods', 'moods_table']
                    self.moods_table = next((name for name in possible_names if name in existing_tables), 'moods')
                
                if not self.memories_table:
                    possible_names = ['memories', 'user_memories', 'luminora_memories', 'memories_table']
                    self.memories_table = next((name for name in possible_names if name in existing_tables), 'memories')
                
                logger.info(f"Detected tables in schema {self.schema}: {existing_tables}")
                
        except Exception as e:
            logger.warning(f"Could not detect tables: {e}")
            # Use defaults
            self.facts_table = self.facts_table or 'facts'
            self.affinity_table = self.affinity_table or 'affinity'
            self.episodes_table = self.episodes_table or 'episodes'
            self.moods_table = self.moods_table or 'moods'
            self.memories_table = self.memories_table or 'memories'
    
    async def _ensure_tables_exist(self):
        """Create tables if they don't exist"""
        try:
            async with self.pool.acquire() as conn:
                # Create facts table
                await conn.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.schema}.{self.facts_table} (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(255) NOT NULL,
                        session_id VARCHAR(255),
                        category VARCHAR(100) NOT NULL,
                        key VARCHAR(255) NOT NULL,
                        value TEXT,
                        confidence REAL DEFAULT 1.0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, category, key)
                    )
                """)
                
                # Create affinity table
                await conn.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.schema}.{self.affinity_table} (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(255) NOT NULL,
                        session_id VARCHAR(255),
                        personality_name VARCHAR(100) NOT NULL,
                        affinity_points INTEGER DEFAULT 0,
                        current_level VARCHAR(50) DEFAULT 'stranger',
                        total_interactions INTEGER DEFAULT 0,
                        positive_interactions INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, personality_name)
                    )
                """)
                
                # Create episodes table
                await conn.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.schema}.{self.episodes_table} (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(255) NOT NULL,
                        session_id VARCHAR(255),
                        episode_type VARCHAR(100) NOT NULL,
                        title VARCHAR(255) NOT NULL,
                        summary TEXT,
                        importance REAL DEFAULT 0.0,
                        sentiment VARCHAR(50),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create moods table
                await conn.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.schema}.{self.moods_table} (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(255) NOT NULL,
                        session_id VARCHAR(255),
                        mood_type VARCHAR(100) NOT NULL,
                        intensity REAL DEFAULT 0.0,
                        context TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create memories table
                await conn.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.schema}.{self.memories_table} (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(255) NOT NULL,
                        session_id VARCHAR(255),
                        memory_key VARCHAR(255) NOT NULL,
                        memory_value TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, memory_key)
                    )
                """)
                
                # Create indexes for better performance
                await conn.execute(f"""
                    CREATE INDEX IF NOT EXISTS idx_{self.facts_table}_user_id 
                    ON {self.schema}.{self.facts_table}(user_id)
                """)
                
                await conn.execute(f"""
                    CREATE INDEX IF NOT EXISTS idx_{self.affinity_table}_user_personality 
                    ON {self.schema}.{self.affinity_table}(user_id, personality_name)
                """)
                
                logger.info(f"Tables created/verified in schema {self.schema}")
                
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise
    
    async def _get_connection(self) -> Connection:
        """Get database connection from pool"""
        await self._ensure_initialized()
        return self.pool.acquire()
    
    # AFFINITY METHODS
    async def save_affinity(
        self,
        user_id: str,
        personality_name: str,
        affinity_points: int,
        current_level: str,
        **kwargs
    ) -> bool:
        """Save or update user inventory"""
        try:
            async with self._get_connection() as conn:
                # Use UPSERT (INSERT ... ON CONFLICT)
                await conn.execute(f"""
                    INSERT INTO {self.schema}.{self.affinity_table} 
                    (user_id, session_id, personality_name, affinity_points, current_level,
                     total_interactions, positive_interactions, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                    ON CONFLICT (user_id, personality_name) 
                    DO UPDATE SET 
                        affinity_points = EXCLUDED.affinity_points,
                        current_level = EXCLUDED.current_level,
                        total_interactions = EXCLUDED.total_interactions,
                        positive_interactions = EXCLUDED.positive_interactions,
                        session_id = EXCLUDED.session_id,
                        updated_at = EXCLUDED.updated_at
                """, user_id, kwargs.get('session_id', user_id), personality_name,
                    affinity_points, current_level,
                    kwargs.get('total_interactions', 0),
                    kwargs.get('positive_interactions', 0),
                    datetime.now(), datetime.now())
                
                return True
                
        except Exception as e:
            logger.error(f"Failed to save affinity: {e}")
            return False
    
    async def get_affinity(
        self,
        user_id: str,
        personality_name: str
    ) -> Optional[Dict[str, Any]]:
        """Get user affinity"""
        try:
            async with self._get_connection() as conn:
                row = await conn.fetchrow(f"""
                    SELECT * FROM {self.schema}.{self.affinity_table} 
                    WHERE user_id = $1 AND personality_name = $2
                """, user_id, personality_name)
                
                if row:
                    return {
                        "affinity_points": row['affinity_points'],
                        "current_level": row['current_level'],
                        "total_interactions": row['total_interactions'],
                        "positive_interactions": row['positive_interactions'],
                        "created_at": row['created_at'].isoformat() if row['created_at'] else None,
                        "updated_at": row['updated_at'].isoformat() if row['updated_at'] else None
                    }
                return None
                
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
            async with self._get_connection() as conn:
                value_str = json.dumps(value) if not isinstance(value, str) else value
                
                # Use UPSERT (INSERT ... ON CONFLICT)
                await conn.execute(f"""
                    INSERT INTO {self.schema}.{self.facts_table} 
                    (user_id, session_id, category, key, value, confidence, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    ON CONFLICT (user_id, category, key) 
                    DO UPDATE SET 
                        value = EXCLUDED.value,
                        confidence = EXCLUDED.confidence,
                        session_id = EXCLUDED.session_id,
                        updated_at = EXCLUDED.updated_at
                """, user_id, kwargs.get('session_id', user_id), category, key,
                    value_str, kwargs.get('confidence', 1.0),
                    datetime.now(), datetime.now())
                
                return True
                
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
            async with self._get_connection() as conn:
                if category:
                    rows = await conn.fetch(f"""
                        SELECT * FROM {self.schema}.{self.facts_table} 
                        WHERE user_id = $1 AND category = $2
                        ORDER BY created_at DESC
                    """, user_id, category)
                else:
                    rows = await conn.fetch(f"""
                        SELECT * FROM {self.schema}.{self.facts_table} 
                        WHERE user_id = $1
                        ORDER BY created_at DESC
                    """, user_id)
                
                facts = []
                for row in rows:
                    try:
                        value = row['value']
                        try:
                            value = json.loads(value)
                        except:
                            pass  # Keep as string if not JSON
                        
                        facts.append({
                            'category': row['category'],
                            'key': row['key'],
                            'value': value,
                            'confidence': row['confidence'],
                            'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                            'updated_at': row['updated_at'].isoformat() if row['updated_at'] else None
                        })
                    except Exception as e:
                        logger.warning(f"Failed to parse fact: {e}")
                        continue
                
                return facts
                
        except Exception as e:
            logger.error(f"Failed to get facts: {e}")
            return []
    
    async def delete_fact(
        self,
        user_id: str,
        category: str,
        key: str
    ) -> bool:
        """Delete a user fact"""
        try:
            async with self._get_connection() as conn:
                await conn.execute(f"""
                    DELETE FROM {self.schema}.{self.facts_table} 
                    WHERE user_id = $1 AND category = $2 AND key = $3
                """, user_id, category, key)
                return True
                
        except Exception as e:
            logger.error(f"Failed to delete fact: {e}")
            return False
    
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
        """Save a memorable episode"""
        try:
            async with self._get_connection() as conn:
                await conn.execute(f"""
                    INSERT INTO {self.schema}.{self.episodes_table} 
                    (user_id, session_id, episode_type, title, summary, importance, sentiment, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                """, user_id, kwargs.get('session_id', user_id), episode_type, title, summary,
                    importance, sentiment, datetime.now(), datetime.now())
                return True
                
        except Exception as e:
            logger.error(f"Failed to save episode: {e}")
            return False
    
    async def get_episodes(
        self,
        user_id: str,
        min_importance: Optional[float] = None,
        max_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get user episodes"""
        try:
            async with self._get_connection() as conn:
                query = f"""
                    SELECT * FROM {self.schema}.{self.episodes_table} 
                    WHERE user_id = $1
                """
                params = [user_id]
                
                if min_importance is not None:
                    query += " AND importance >= $2"
                    params.append(min_importance)
                
                query += " ORDER BY importance DESC, created_at DESC"
                
                if max_results:
                    query += f" LIMIT ${len(params) + 1}"
                    params.append(max_results)
                
                rows = await conn.fetch(query, *params)
                
                episodes = []
                for row in rows:
                    episodes.append({
                        'episode_type': row['episode_type'],
                        'title': row['title'],
                        'summary': row['summary'],
                        'importance': row['importance'],
                        'sentiment': row['sentiment'],
                        'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                        'updated_at': row['updated_at'].isoformat() if row['updated_at'] else None
                    })
                
                return episodes
                
        except Exception as e:
            logger.error(f"Failed to get episodes: {e}")
            return []
    
    # MOOD METHODS
    async def save_mood(
        self,
        user_id: str,
        mood_type: str,
        intensity: float,
        context: str,
        **kwargs
    ) -> bool:
        """Save user mood"""
        try:
            async with self._get_connection() as conn:
                await conn.execute(f"""
                    INSERT INTO {self.schema}.{self.moods_table} 
                    (user_id, session_id, mood_type, intensity, context, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                """, user_id, kwargs.get('session_id', user_id), mood_type, intensity, context,
                    datetime.now(), datetime.now())
                return True
                
        except Exception as e:
            logger.error(f"Failed to save mood: {e}")
            return False
    
    async def get_mood(
        self,
        user_id: str,
        personality_name: str
    ) -> Optional[Dict[str, Any]]:
        """Get current mood for user and personality"""
        try:
            # Get latest mood from history
            mood_history = await self.get_mood_history(user_id, days_back=1)
            if mood_history:
                latest_mood = mood_history[0]  # Most recent mood
                return {
                    'mood_type': latest_mood['mood_type'],
                    'intensity': latest_mood['intensity'],
                    'context': latest_mood['context'],
                    'timestamp': latest_mood['created_at']
                }
            return None
            
        except Exception as e:
            logger.error(f"Failed to get mood: {e}")
            return None
    
    async def get_mood_history(
        self,
        user_id: str,
        mood_type: Optional[str] = None,
        days_back: int = 30
    ) -> List[Dict[str, Any]]:
        """Get user mood history"""
        try:
            async with self._get_connection() as conn:
                query = f"""
                    SELECT * FROM {self.schema}.{self.moods_table} 
                    WHERE user_id = $1 AND created_at >= $2
                """
                params = [user_id, datetime.now() - timedelta(days=days_back)]
                
                if mood_type:
                    query += " AND mood_type = $3"
                    params.append(mood_type)
                
                query += " ORDER BY created_at DESC"
                
                rows = await conn.fetch(query, *params)
                
                moods = []
                for row in rows:
                    moods.append({
                        'mood_type': row['mood_type'],
                        'intensity': row['intensity'],
                        'context': row['context'],
                        'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                        'updated_at': row['updated_at'].isoformat() if row['updated_at'] else None
                    })
                
                return moods
                
        except Exception as e:
            logger.error(f"Failed to get mood history: {e}")
            return []
    
    # MEMORY METHODS
    async def save_memory(
        self,
        user_id: str,
        memory_key: str,
        memory_value: Any,
        **kwargs
    ) -> bool:
        """Save a memory item"""
        try:
            async with self._get_connection() as conn:
                value_str = json.dumps(memory_value) if not isinstance(memory_value, str) else memory_value
                
                # Use UPSERT (INSERT ... ON CONFLICT)
                await conn.execute(f"""
                    INSERT INTO {self.schema}.{self.memories_table} 
                    (user_id, session_id, memory_key, memory_value, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    ON CONFLICT (user_id, memory_key) 
                    DO UPDATE SET 
                        memory_value = EXCLUDED.memory_value,
                        session_id = EXCLUDED.session_id,
                        updated_at = EXCLUDED.updated_at
                """, user_id, kwargs.get('session_id', user_id), memory_key, value_str,
                    datetime.now(), datetime.now())
                
                return True
                
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")
            return False
    
    async def get_memory(
        self,
        user_id: str,
        memory_key: str
    ) -> Optional[Any]:
        """Get a memory item"""
        try:
            async with self._get_connection() as conn:
                row = await conn.fetchrow(f"""
                    SELECT memory_value FROM {self.schema}.{self.memories_table} 
                    WHERE user_id = $1 AND memory_key = $2
                """, user_id, memory_key)
                
                if row:
                    try:
                        return json.loads(row['memory_value'])
                    except:
                        return row['memory_value']
                return None
                
        except Exception as e:
            logger.error(f"Failed to get memory: {e}")
            return None
    
    async def delete_memory(
        self,
        user_id: str,
        memory_key: str
    ) -> bool:
        """Delete a memory item"""
        try:
            async with self._get_connection() as conn:
                await conn.execute(f"""
                    DELETE FROM {self.schema}.{self.memories_table} 
                    WHERE user_id = $1 AND memory_key = $2
                """, user_id, memory_key)
                return True
                
        except Exception as e:
            logger.error(f"Failed to delete memory: {e}")
            return False
