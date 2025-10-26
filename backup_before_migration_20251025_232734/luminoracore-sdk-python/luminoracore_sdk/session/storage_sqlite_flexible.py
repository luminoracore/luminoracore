"""
Flexible SQLite Storage v11 Implementation

This implementation allows users to use ANY SQLite database with ANY schema.
"""

import sqlite3
import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging
from contextlib import asynccontextmanager

from .storage_v1_1 import StorageV11Extension

logger = logging.getLogger(__name__)


class FlexibleSQLiteStorageV11(StorageV11Extension):
    """
    Flexible SQLite storage that adapts to ANY database schema
    
    The user can use their own SQLite databases with any table structure.
    """
    
    def __init__(
        self,
        database_path: str,
        facts_table: str = None,
        affinity_table: str = None,
        episodes_table: str = None,
        moods_table: str = None,
        memories_table: str = None,
        auto_create_tables: bool = True
    ):
        """
        Initialize flexible SQLite storage
        
        Args:
            database_path: Path to SQLite database file (user's database)
            facts_table: Name of facts table (auto-detected if None)
            affinity_table: Name of affinity table (auto-detected if None)
            episodes_table: Name of episodes table (auto-detected if None)
            moods_table: Name of moods table (auto-detected if None)
            memories_table: Name of memories table (auto-detected if None)
            auto_create_tables: Whether to create tables if they don't exist
        """
        self.database_path = database_path
        self.auto_create_tables = auto_create_tables
        
        # Table names (user's choice or auto-detected)
        self.facts_table = facts_table
        self.affinity_table = affinity_table
        self.episodes_table = episodes_table
        self.moods_table = moods_table
        self.memories_table = memories_table
        
        # Ensure database directory exists (only if path is not empty)
        if database_path and database_path != ":memory:":
            db_dir = os.path.dirname(database_path)
            if db_dir:  # Only create directory if there is one
                os.makedirs(db_dir, exist_ok=True)
        
        # Auto-detect table names if not provided
        self._detect_tables()
        
        # Create tables if needed
        if auto_create_tables:
            self._ensure_tables_exist()
        
        logger.info(f"Flexible SQLite storage initialized with database: {database_path}")
        logger.info(f"Tables: {self.facts_table}, {self.affinity_table}, {self.episodes_table}")
    
    def _detect_tables(self):
        """Auto-detect table names from existing database"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                existing_tables = [row[0] for row in cursor.fetchall()]
                
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
                
                logger.info(f"Detected tables: {existing_tables}")
                
        except Exception as e:
            logger.warning(f"Could not detect tables: {e}")
            # Use defaults
            self.facts_table = self.facts_table or 'facts'
            self.affinity_table = self.affinity_table or 'affinity'
            self.episodes_table = self.episodes_table or 'episodes'
            self.moods_table = self.moods_table or 'moods'
            self.memories_table = self.memories_table or 'memories'
    
    def _ensure_tables_exist(self):
        """Create tables if they don't exist"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                
                # Create facts table
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.facts_table} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        session_id TEXT,
                        category TEXT NOT NULL,
                        key TEXT NOT NULL,
                        value TEXT,
                        confidence REAL DEFAULT 1.0,
                        created_at TEXT,
                        updated_at TEXT,
                        UNIQUE(user_id, category, key)
                    )
                """)
                
                # Create affinity table
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.affinity_table} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        session_id TEXT,
                        personality_name TEXT NOT NULL,
                        affinity_points INTEGER DEFAULT 0,
                        current_level TEXT DEFAULT 'stranger',
                        total_interactions INTEGER DEFAULT 0,
                        positive_interactions INTEGER DEFAULT 0,
                        created_at TEXT,
                        updated_at TEXT,
                        UNIQUE(user_id, personality_name)
                    )
                """)
                
                # Create episodes table
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.episodes_table} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        session_id TEXT,
                        episode_type TEXT NOT NULL,
                        title TEXT NOT NULL,
                        summary TEXT,
                        importance REAL DEFAULT 0.0,
                        sentiment TEXT,
                        created_at TEXT,
                        updated_at TEXT
                    )
                """)
                
                # Create moods table
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.moods_table} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        session_id TEXT,
                        mood_type TEXT NOT NULL,
                        intensity REAL DEFAULT 0.0,
                        context TEXT,
                        created_at TEXT,
                        updated_at TEXT
                    )
                """)
                
                # Create memories table
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.memories_table} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        session_id TEXT,
                        memory_key TEXT NOT NULL,
                        memory_value TEXT,
                        created_at TEXT,
                        updated_at TEXT,
                        UNIQUE(user_id, memory_key)
                    )
                """)
                
                conn.commit()
                logger.info(f"Tables created/verified: {self.facts_table}, {self.affinity_table}, {self.episodes_table}")
                
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise
    
    @asynccontextmanager
    async def _get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
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
            async with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if affinity exists
                cursor.execute(f"""
                    SELECT id FROM {self.affinity_table} 
                    WHERE user_id = ? AND personality_name = ?
                """, (user_id, personality_name))
                
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing affinity
                    cursor.execute(f"""
                        UPDATE {self.affinity_table} 
                        SET affinity_points = ?, current_level = ?, 
                            total_interactions = ?, positive_interactions = ?,
                            session_id = ?, updated_at = ?
                        WHERE user_id = ? AND personality_name = ?
                    """, (affinity_points, current_level, 
                          kwargs.get('total_interactions', 0),
                          kwargs.get('positive_interactions', 0),
                          kwargs.get('session_id', user_id),
                          datetime.now().isoformat(),
                          user_id, personality_name))
                else:
                    # Insert new affinity
                    cursor.execute(f"""
                        INSERT INTO {self.affinity_table} 
                        (user_id, session_id, personality_name, affinity_points, current_level,
                         total_interactions, positive_interactions, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (user_id, kwargs.get('session_id', user_id), personality_name,
                          affinity_points, current_level,
                          kwargs.get('total_interactions', 0),
                          kwargs.get('positive_interactions', 0),
                          datetime.now().isoformat(),
                          datetime.now().isoformat()))
                
                conn.commit()
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
                cursor = conn.cursor()
                cursor.execute(f"""
                    SELECT * FROM {self.affinity_table} 
                    WHERE user_id = ? AND personality_name = ?
                """, (user_id, personality_name))
                
                row = cursor.fetchone()
                if row:
                    return {
                        "affinity_points": row['affinity_points'],
                        "current_level": row['current_level'],
                        "total_interactions": row['total_interactions'],
                        "positive_interactions": row['positive_interactions'],
                        "created_at": row['created_at'],
                        "updated_at": row['updated_at']
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
                cursor = conn.cursor()
                
                # Check if fact exists
                cursor.execute(f"""
                    SELECT id FROM {self.facts_table} 
                    WHERE user_id = ? AND category = ? AND key = ?
                """, (user_id, category, key))
                
                existing = cursor.fetchone()
                
                value_str = json.dumps(value) if not isinstance(value, str) else value
                
                if existing:
                    # Update existing fact
                    cursor.execute(f"""
                        UPDATE {self.facts_table} 
                        SET value = ?, confidence = ?, session_id = ?, updated_at = ?
                        WHERE user_id = ? AND category = ? AND key = ?
                    """, (value_str, kwargs.get('confidence', 1.0),
                          kwargs.get('session_id', user_id),
                          datetime.now().isoformat(),
                          user_id, category, key))
                else:
                    # Insert new fact
                    cursor.execute(f"""
                        INSERT INTO {self.facts_table} 
                        (user_id, session_id, category, key, value, confidence, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (user_id, kwargs.get('session_id', user_id), category, key,
                          value_str, kwargs.get('confidence', 1.0),
                          datetime.now().isoformat(),
                          datetime.now().isoformat()))
                
                conn.commit()
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
                cursor = conn.cursor()
                
                if category:
                    cursor.execute(f"""
                        SELECT * FROM {self.facts_table} 
                        WHERE user_id = ? AND category = ?
                        ORDER BY created_at DESC
                    """, (user_id, category))
                else:
                    cursor.execute(f"""
                        SELECT * FROM {self.facts_table} 
                        WHERE user_id = ?
                        ORDER BY created_at DESC
                    """, (user_id,))
                
                facts = []
                for row in cursor.fetchall():
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
                            'created_at': row['created_at'],
                            'updated_at': row['updated_at']
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
                cursor = conn.cursor()
                cursor.execute(f"""
                    DELETE FROM {self.facts_table} 
                    WHERE user_id = ? AND category = ? AND key = ?
                """, (user_id, category, key))
                conn.commit()
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
                cursor = conn.cursor()
                cursor.execute(f"""
                    INSERT INTO {self.episodes_table} 
                    (user_id, session_id, episode_type, title, summary, importance, sentiment, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, kwargs.get('session_id', user_id), episode_type, title, summary,
                      importance, sentiment, datetime.now().isoformat(), datetime.now().isoformat()))
                conn.commit()
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
                cursor = conn.cursor()
                
                query = f"""
                    SELECT * FROM {self.episodes_table} 
                    WHERE user_id = ?
                """
                params = [user_id]
                
                if min_importance is not None:
                    query += " AND importance >= ?"
                    params.append(min_importance)
                
                query += " ORDER BY importance DESC, created_at DESC"
                
                if max_results:
                    query += " LIMIT ?"
                    params.append(max_results)
                
                cursor.execute(query, params)
                
                episodes = []
                for row in cursor.fetchall():
                    episodes.append({
                        'episode_type': row['episode_type'],
                        'title': row['title'],
                        'summary': row['summary'],
                        'importance': row['importance'],
                        'sentiment': row['sentiment'],
                        'created_at': row['created_at'],
                        'updated_at': row['updated_at']
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
                cursor = conn.cursor()
                cursor.execute(f"""
                    INSERT INTO {self.moods_table} 
                    (user_id, session_id, mood_type, intensity, context, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user_id, kwargs.get('session_id', user_id), mood_type, intensity, context,
                      datetime.now().isoformat(), datetime.now().isoformat()))
                conn.commit()
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
                cursor = conn.cursor()
                
                query = f"""
                    SELECT * FROM {self.moods_table} 
                    WHERE user_id = ? AND created_at >= ?
                """
                params = [user_id, (datetime.now() - timedelta(days=days_back)).isoformat()]
                
                if mood_type:
                    query += " AND mood_type = ?"
                    params.append(mood_type)
                
                query += " ORDER BY created_at DESC"
                
                cursor.execute(query, params)
                
                moods = []
                for row in cursor.fetchall():
                    moods.append({
                        'mood_type': row['mood_type'],
                        'intensity': row['intensity'],
                        'context': row['context'],
                        'created_at': row['created_at'],
                        'updated_at': row['updated_at']
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
                cursor = conn.cursor()
                
                # Check if memory exists
                cursor.execute(f"""
                    SELECT id FROM {self.memories_table} 
                    WHERE user_id = ? AND memory_key = ?
                """, (user_id, memory_key))
                
                existing = cursor.fetchone()
                
                value_str = json.dumps(memory_value) if not isinstance(memory_value, str) else memory_value
                
                if existing:
                    # Update existing memory
                    cursor.execute(f"""
                        UPDATE {self.memories_table} 
                        SET memory_value = ?, session_id = ?, updated_at = ?
                        WHERE user_id = ? AND memory_key = ?
                    """, (value_str, kwargs.get('session_id', user_id),
                          datetime.now().isoformat(), user_id, memory_key))
                else:
                    # Insert new memory
                    cursor.execute(f"""
                        INSERT INTO {self.memories_table} 
                        (user_id, session_id, memory_key, memory_value, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (user_id, kwargs.get('session_id', user_id), memory_key, value_str,
                          datetime.now().isoformat(), datetime.now().isoformat()))
                
                conn.commit()
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
                cursor = conn.cursor()
                cursor.execute(f"""
                    SELECT memory_value FROM {self.memories_table} 
                    WHERE user_id = ? AND memory_key = ?
                """, (user_id, memory_key))
                
                row = cursor.fetchone()
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
                cursor = conn.cursor()
                cursor.execute(f"""
                    DELETE FROM {self.memories_table} 
                    WHERE user_id = ? AND memory_key = ?
                """, (user_id, memory_key))
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Failed to delete memory: {e}")
            return False
    
    async def save_session(
        self,
        session_id: str,
        user_id: str,
        personality_name: str,
        **kwargs
    ) -> bool:
        """Save session data"""
        try:
            async with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    INSERT OR REPLACE INTO {self.sessions_table} 
                    (session_id, user_id, personality_name, created_at, updated_at, last_activity, ttl)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_id, user_id, personality_name,
                    kwargs.get('created_at', datetime.now().isoformat()),
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                    kwargs.get('ttl', int((datetime.now() + timedelta(days=30)).timestamp()))
                ))
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
            return False
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        try:
            async with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    SELECT * FROM {self.sessions_table} 
                    WHERE session_id = ?
                """, (session_id,))
                
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
                
        except Exception as e:
            logger.error(f"Failed to get session: {e}")
            return None
    
    async def update_session_activity(self, session_id: str) -> bool:
        """Update session activity"""
        try:
            async with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    UPDATE {self.sessions_table} 
                    SET last_activity = ?, updated_at = ?
                    WHERE session_id = ?
                """, (datetime.now().isoformat(), datetime.now().isoformat(), session_id))
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Failed to update session activity: {e}")
            return False
    
    async def get_expired_sessions(self) -> List[Dict[str, Any]]:
        """Get expired sessions"""
        try:
            current_time = datetime.now().timestamp()
            async with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    SELECT * FROM {self.sessions_table} 
                    WHERE ttl < ?
                """, (current_time,))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Failed to get expired sessions: {e}")
            return []
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete session"""
        try:
            async with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    DELETE FROM {self.sessions_table} 
                    WHERE session_id = ?
                """, (session_id,))
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Failed to delete session: {e}")
            return False
