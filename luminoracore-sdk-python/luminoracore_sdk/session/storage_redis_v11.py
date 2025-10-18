"""
Redis Storage v11 Implementation

Real Redis implementation for v1.1 storage with persistent data.
"""

import json
import pickle
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

try:
    import redis.asyncio as redis
    from redis.asyncio import Redis
except ImportError:
    redis = None
    Redis = None

from .storage_v1_1 import StorageV11Extension

logger = logging.getLogger(__name__)


class RedisStorageV11(StorageV11Extension):
    """
    Real Redis storage implementation for v1.1 features
    """
    
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, password: Optional[str] = None):
        """
        Initialize Redis storage
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            password: Redis password
        """
        if redis is None:
            raise ImportError("redis is required for Redis storage. Install with: pip install redis")
        
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.redis: Optional[Redis] = None
        self._ensure_initialized = False
        
        # Key prefixes for different data types
        self.AFFINITY_PREFIX = "luminora:affinity:"
        self.FACT_PREFIX = "luminora:fact:"
        self.EPISODE_PREFIX = "luminora:episode:"
        self.MOOD_PREFIX = "luminora:mood:"
        self.MEMORY_PREFIX = "luminora:memory:"
        self.USER_PREFIX = "luminora:user:"
    
    async def _ensure_initialized(self):
        """Ensure Redis connection is established"""
        if self._ensure_initialized:
            return
        
        try:
            self.redis = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=False  # We'll handle encoding/decoding manually
            )
            
            # Test connection
            await self.redis.ping()
            self._ensure_initialized = True
            logger.info("Redis connection established successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Redis connection: {e}")
            raise
    
    def _serialize_value(self, value: Any) -> bytes:
        """Serialize value for Redis storage"""
        try:
            # Try JSON first for simple types
            return json.dumps(value).encode('utf-8')
        except (TypeError, ValueError):
            # Fall back to pickle for complex types
            return pickle.dumps(value)
    
    def _deserialize_value(self, data: bytes) -> Any:
        """Deserialize value from Redis storage"""
        try:
            # Try JSON first
            return json.loads(data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            try:
                # Fall back to pickle
                return pickle.loads(data)
            except:
                # Return as string if all else fails
                return data.decode('utf-8', errors='ignore')
    
    def _get_affinity_key(self, user_id: str, personality_name: str) -> str:
        """Get Redis key for affinity data"""
        return f"{self.AFFINITY_PREFIX}{user_id}:{personality_name}"
    
    def _get_fact_key(self, user_id: str, category: str, key: str) -> str:
        """Get Redis key for fact data"""
        return f"{self.FACT_PREFIX}{user_id}:{category}:{key}"
    
    def _get_user_facts_key(self, user_id: str) -> str:
        """Get Redis key for user facts set"""
        return f"{self.USER_PREFIX}{user_id}:facts"
    
    def _get_episode_key(self, user_id: str, episode_id: str) -> str:
        """Get Redis key for episode data"""
        return f"{self.EPISODE_PREFIX}{user_id}:{episode_id}"
    
    def _get_user_episodes_key(self, user_id: str) -> str:
        """Get Redis key for user episodes set"""
        return f"{self.USER_PREFIX}{user_id}:episodes"
    
    def _get_mood_key(self, user_id: str, session_id: str) -> str:
        """Get Redis key for mood data"""
        return f"{self.MOOD_PREFIX}{user_id}:{session_id}"
    
    def _get_user_mood_key(self, user_id: str) -> str:
        """Get Redis key for user mood history"""
        return f"{self.USER_PREFIX}{user_id}:moods"
    
    def _get_memory_key(self, session_id: str, memory_key: str) -> str:
        """Get Redis key for memory data"""
        return f"{self.MEMORY_PREFIX}{session_id}:{memory_key}"
    
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
            await self._ensure_initialized()
            
            affinity_data = {
                "affinity_points": affinity_points,
                "current_level": current_level,
                "total_interactions": kwargs.get('total_interactions', 0),
                "positive_interactions": kwargs.get('positive_interactions', 0),
                "created_at": kwargs.get('created_at', datetime.now().isoformat()),
                "updated_at": datetime.now().isoformat()
            }
            
            key = self._get_affinity_key(user_id, personality_name)
            await self.redis.set(key, self._serialize_value(affinity_data))
            
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
            await self._ensure_initialized()
            
            key = self._get_affinity_key(user_id, personality_name)
            data = await self.redis.get(key)
            
            if data:
                return self._deserialize_value(data)
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
            await self._ensure_initialized()
            
            fact_data = {
                "category": category,
                "key": key,
                "value": value,
                "confidence": kwargs.get('confidence', 1.0),
                "created_at": kwargs.get('created_at', datetime.now().isoformat()),
                "updated_at": datetime.now().isoformat()
            }
            
            fact_key = self._get_fact_key(user_id, category, key)
            user_facts_key = self._get_user_facts_key(user_id)
            
            # Save fact data
            await self.redis.set(fact_key, self._serialize_value(fact_data))
            
            # Add to user facts set
            await self.redis.sadd(user_facts_key, fact_key)
            
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
            await self._ensure_initialized()
            
            user_facts_key = self._get_user_facts_key(user_id)
            fact_keys = await self.redis.smembers(user_facts_key)
            
            facts = []
            for fact_key_bytes in fact_keys:
                fact_key = fact_key_bytes.decode('utf-8')
                
                # Skip if category filter doesn't match
                if category and f":{category}:" not in fact_key:
                    continue
                
                data = await self.redis.get(fact_key)
                if data:
                    fact_data = self._deserialize_value(data)
                    facts.append({
                        "category": fact_data["category"],
                        "key": fact_data["key"],
                        "value": fact_data["value"],
                        "confidence": fact_data["confidence"],
                        "created_at": fact_data["created_at"],
                        "updated_at": fact_data["updated_at"]
                    })
            
            # Sort by created_at descending
            facts.sort(key=lambda x: x["created_at"], reverse=True)
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
            await self._ensure_initialized()
            
            episode_id = kwargs.get('episode_id', datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
            
            episode_data = {
                "episode_type": episode_type,
                "title": title,
                "summary": summary,
                "importance": importance,
                "sentiment": sentiment,
                "created_at": datetime.now().isoformat()
            }
            
            episode_key = self._get_episode_key(user_id, episode_id)
            user_episodes_key = self._get_user_episodes_key(user_id)
            
            # Save episode data
            await self.redis.set(episode_key, self._serialize_value(episode_data))
            
            # Add to user episodes set with score for sorting
            await self.redis.zadd(user_episodes_key, {episode_key: importance})
            
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
            await self._ensure_initialized()
            
            user_episodes_key = self._get_user_episodes_key(user_id)
            
            # Get episodes sorted by importance (descending)
            if min_importance is not None:
                episode_keys = await self.redis.zrevrangebyscore(
                    user_episodes_key, '+inf', min_importance, withscores=True
                )
            else:
                episode_keys = await self.redis.zrevrange(
                    user_episodes_key, 0, -1, withscores=True
                )
            
            episodes = []
            for episode_key_bytes, importance in episode_keys:
                episode_key = episode_key_bytes.decode('utf-8')
                
                data = await self.redis.get(episode_key)
                if data:
                    episode_data = self._deserialize_value(data)
                    episodes.append({
                        "episode_type": episode_data["episode_type"],
                        "title": episode_data["title"],
                        "summary": episode_data["summary"],
                        "importance": episode_data["importance"],
                        "sentiment": episode_data["sentiment"],
                        "created_at": episode_data["created_at"]
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
            await self._ensure_initialized()
            
            mood_data = {
                "current_mood": current_mood,
                "mood_intensity": mood_intensity,
                "created_at": datetime.now().isoformat()
            }
            
            mood_key = self._get_mood_key(user_id, session_id)
            user_mood_key = self._get_user_mood_key(user_id)
            
            # Save mood data
            await self.redis.set(mood_key, self._serialize_value(mood_data))
            
            # Add to user mood history (sorted by timestamp)
            timestamp = datetime.now().timestamp()
            await self.redis.zadd(user_mood_key, {mood_key: timestamp})
            
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
            await self._ensure_initialized()
            
            user_mood_key = self._get_user_mood_key(user_id)
            mood_keys = await self.redis.zrevrange(user_mood_key, 0, limit - 1)
            
            moods = []
            for mood_key_bytes in mood_keys:
                mood_key = mood_key_bytes.decode('utf-8')
                
                data = await self.redis.get(mood_key)
                if data:
                    mood_data = self._deserialize_value(data)
                    moods.append({
                        "session_id": mood_key.split(':')[-1],
                        "current_mood": mood_data["current_mood"],
                        "mood_intensity": mood_data["mood_intensity"],
                        "created_at": mood_data["created_at"]
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
            await self._ensure_initialized()
            
            memory_key = self._get_memory_key(session_id, key)
            
            # Set expiration if provided
            if expires_at:
                ttl_seconds = int((expires_at - datetime.now()).total_seconds())
                await self.redis.setex(memory_key, ttl_seconds, self._serialize_value(value))
            else:
                # Default TTL of 30 days
                await self.redis.setex(memory_key, 30 * 24 * 60 * 60, self._serialize_value(value))
            
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
            await self._ensure_initialized()
            
            memory_key = self._get_memory_key(session_id, key)
            data = await self.redis.get(memory_key)
            
            if data:
                return self._deserialize_value(data)
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
            await self._ensure_initialized()
            
            memory_key = self._get_memory_key(session_id, key)
            await self.redis.delete(memory_key)
            
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
            await self._ensure_initialized()
            
            pattern = f"{self.MEMORY_PREFIX}{session_id}:*"
            memory_keys = await self.redis.keys(pattern)
            
            memories = {}
            for memory_key_bytes in memory_keys:
                memory_key = memory_key_bytes.decode('utf-8')
                key_name = memory_key.split(':')[-1]
                
                data = await self.redis.get(memory_key)
                if data:
                    memories[key_name] = self._deserialize_value(data)
            
            return memories
            
        except Exception as e:
            logger.error(f"Failed to get all memories: {e}")
            return {}
    
    async def close(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()
