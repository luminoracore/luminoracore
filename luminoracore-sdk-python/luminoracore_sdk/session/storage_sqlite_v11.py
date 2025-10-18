"""
SQLite Storage v1.1 Implementation

Real SQLite implementation for v1.1 storage with persistent data.
"""

import sqlite3
import json
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path
import logging

from .storage_v1_1 import StorageV11Extension

logger = logging.getLogger(__name__)


class SQLiteStorageV11(StorageV11Extension):
    """
    Real SQLite storage implementation for v1.1 features
    """
    
    def __init__(self, db_path: str = "luminoracore_v11.db"):
        """
        Initialize SQLite storage
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Ensure database and tables exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS user_affinity (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        personality_name TEXT NOT NULL,
                        affinity_points INTEGER DEFAULT 0,
                        current_level TEXT DEFAULT 'stranger',
                        total_interactions INTEGER DEFAULT 0,
                        positive_interactions INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, personality_name)
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS user_facts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        category TEXT NOT NULL,
                        key TEXT NOT NULL,
                        value TEXT NOT NULL,
                        confidence REAL DEFAULT 1.0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, category, key)
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS user_episodes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        episode_type TEXT NOT NULL,
                        title TEXT NOT NULL,
                        summary TEXT NOT NULL,
                        importance REAL NOT NULL,
                        sentiment TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS user_mood (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        user_id TEXT NOT NULL,
                        current_mood TEXT NOT NULL,
                        mood_intensity REAL DEFAULT 1.0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS conversation_memory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        user_id TEXT NOT NULL,
                        memory_key TEXT NOT NULL,
                        memory_value TEXT NOT NULL,
                        expires_at TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(session_id, memory_key)
                    )
                """)
                
                conn.commit()
                logger.info(f"SQLite database initialized at {self.db_path}")
                
        except Exception as e:
            logger.error(f"Failed to initialize SQLite database: {e}")
            raise
    
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
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO user_affinity 
                    (user_id, personality_name, affinity_points, current_level, updated_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, personality_name, affinity_points, current_level, datetime.now().isoformat()))
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
        """Get user affinity data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT affinity_points, current_level, total_interactions, 
                           positive_interactions, created_at, updated_at
                    FROM user_affinity 
                    WHERE user_id = ? AND personality_name = ?
                """, (user_id, personality_name))
                
                row = cursor.fetchone()
                if row:
                    return {
                        "affinity_points": row[0],
                        "current_level": row[1],
                        "total_interactions": row[2],
                        "positive_interactions": row[3],
                        "created_at": row[4],
                        "updated_at": row[5]
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
            confidence = kwargs.get('confidence', 1.0)
            value_str = json.dumps(value) if not isinstance(value, str) else value
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO user_facts 
                    (user_id, category, key, value, confidence, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, category, key, value_str, confidence, datetime.now().isoformat()))
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
            with sqlite3.connect(self.db_path) as conn:
                if category:
                    cursor = conn.execute("""
                        SELECT category, key, value, confidence, created_at, updated_at
                        FROM user_facts 
                        WHERE user_id = ? AND category = ?
                        ORDER BY created_at DESC
                    """, (user_id, category))
                else:
                    cursor = conn.execute("""
                        SELECT category, key, value, confidence, created_at, updated_at
                        FROM user_facts 
                        WHERE user_id = ?
                        ORDER BY created_at DESC
                    """, (user_id,))
                
                facts = []
                for row in cursor.fetchall():
                    try:
                        # Try to parse JSON value, fallback to string
                        value = json.loads(row[2]) if row[2].startswith(('{', '[', '"')) else row[2]
                    except:
                        value = row[2]
                    
                    facts.append({
                        "category": row[0],
                        "key": row[1],
                        "value": value,
                        "confidence": row[3],
                        "created_at": row[4],
                        "updated_at": row[5]
                    })
                
                return facts
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
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO user_episodes 
                    (user_id, episode_type, title, summary, importance, sentiment)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, episode_type, title, summary, importance, sentiment))
                conn.commit()
                return True
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
            with sqlite3.connect(self.db_path) as conn:
                if min_importance is not None:
                    cursor = conn.execute("""
                        SELECT episode_type, title, summary, importance, sentiment, created_at
                        FROM user_episodes 
                        WHERE user_id = ? AND importance >= ?
                        ORDER BY importance DESC, created_at DESC
                    """, (user_id, min_importance))
                else:
                    cursor = conn.execute("""
                        SELECT episode_type, title, summary, importance, sentiment, created_at
                        FROM user_episodes 
                        WHERE user_id = ?
                        ORDER BY importance DESC, created_at DESC
                    """, (user_id,))
                
                episodes = []
                for row in cursor.fetchall():
                    episodes.append({
                        "episode_type": row[0],
                        "title": row[1],
                        "summary": row[2],
                        "importance": row[3],
                        "sentiment": row[4],
                        "created_at": row[5]
                    })
                
                return episodes
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
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO user_mood 
                    (session_id, user_id, current_mood, mood_intensity)
                    VALUES (?, ?, ?, ?)
                """, (session_id, user_id, current_mood, mood_intensity))
                conn.commit()
                return True
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
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT session_id, current_mood, mood_intensity, created_at
                    FROM user_mood 
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (user_id, limit))
                
                moods = []
                for row in cursor.fetchall():
                    moods.append({
                        "session_id": row[0],
                        "current_mood": row[1],
                        "mood_intensity": row[2],
                        "created_at": row[3]
                    })
                
                return moods
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
            expires_str = expires_at.isoformat() if expires_at else None
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO conversation_memory 
                    (session_id, user_id, memory_key, memory_value, expires_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (session_id, user_id, key, value_str, expires_str, datetime.now().isoformat()))
                conn.commit()
                return True
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
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT memory_value, expires_at
                    FROM conversation_memory 
                    WHERE session_id = ? AND memory_key = ?
                """, (session_id, key))
                
                row = cursor.fetchone()
                if row:
                    # Check if expired
                    if row[1] and datetime.fromisoformat(row[1]) < datetime.now():
                        return None
                    
                    try:
                        return json.loads(row[0])
                    except:
                        return row[0]
                return None
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
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    DELETE FROM conversation_memory 
                    WHERE session_id = ? AND memory_key = ?
                """, (session_id, key))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to delete memory: {e}")
            return False
    
    async def get_all_memories(
        self,
        session_id: str
    ) -> Dict[str, Any]:
        """Get all memories for a session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT memory_key, memory_value, expires_at
                    FROM conversation_memory 
                    WHERE session_id = ?
                """, (session_id,))
                
                memories = {}
                for row in cursor.fetchall():
                    # Check if expired
                    if row[2] and datetime.fromisoformat(row[2]) < datetime.now():
                        continue
                    
                    try:
                        memories[row[0]] = json.loads(row[1])
                    except:
                        memories[row[0]] = row[1]
                
                return memories
        except Exception as e:
            logger.error(f"Failed to get all memories: {e}")
            return {}
