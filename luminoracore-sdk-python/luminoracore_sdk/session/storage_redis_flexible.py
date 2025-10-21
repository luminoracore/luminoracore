"""
Flexible Redis Storage v11 Implementation

This implementation allows users to use ANY Redis database with ANY key patterns.
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


class FlexibleRedisStorageV11(StorageV11Extension):
    """
    Flexible Redis storage that adapts to ANY key pattern
    
    The user can use their own Redis databases with any key structure.
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        key_prefix: str = "luminora",
        affinity_key_pattern: str = None,
        fact_key_pattern: str = None,
        episode_key_pattern: str = None,
        mood_key_pattern: str = None,
        memory_key_pattern: str = None,
        user_set_pattern: str = None,
        ttl_days: int = 365
    ):
        """
        Initialize flexible Redis storage
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            password: Redis password
            key_prefix: Base prefix for all keys (user's choice)
            affinity_key_pattern: Pattern for affinity keys (auto-generated if None)
            fact_key_pattern: Pattern for fact keys (auto-generated if None)
            episode_key_pattern: Pattern for episode keys (auto-generated if None)
            mood_key_pattern: Pattern for mood keys (auto-generated if None)
            memory_key_pattern: Pattern for memory keys (auto-generated if None)
            user_set_pattern: Pattern for user sets (auto-generated if None)
            ttl_days: Default TTL in days
        """
        if redis is None:
            raise ImportError("redis is required for Redis storage. Install with: pip install redis")
        
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.key_prefix = key_prefix
        self.ttl_days = ttl_days
        
        # Key patterns (user's choice or auto-generated)
        self.affinity_key_pattern = affinity_key_pattern
        self.fact_key_pattern = fact_key_pattern
        self.episode_key_pattern = episode_key_pattern
        self.mood_key_pattern = mood_key_pattern
        self.memory_key_pattern = memory_key_pattern
        self.user_set_pattern = user_set_pattern
        
        self.redis: Optional[Redis] = None
        self._initialized = False
        
        # Generate key patterns if not provided
        self._generate_key_patterns()
        
        logger.info(f"Flexible Redis storage initialized with prefix: {key_prefix}")
        logger.info(f"Key patterns: affinity={self.affinity_key_pattern}, facts={self.fact_key_pattern}")
    
    def _generate_key_patterns(self):
        """Generate key patterns based on prefix"""
        if not self.affinity_key_pattern:
            self.affinity_key_pattern = f"{self.key_prefix}:affinity:{{user_id}}:{{personality_name}}"
        
        if not self.fact_key_pattern:
            self.fact_key_pattern = f"{self.key_prefix}:fact:{{user_id}}:{{category}}:{{key}}"
        
        if not self.episode_key_pattern:
            self.episode_key_pattern = f"{self.key_prefix}:episode:{{user_id}}:{{episode_id}}"
        
        if not self.mood_key_pattern:
            self.mood_key_pattern = f"{self.key_prefix}:mood:{{user_id}}:{{mood_id}}"
        
        if not self.memory_key_pattern:
            self.memory_key_pattern = f"{self.key_prefix}:memory:{{user_id}}:{{memory_key}}"
        
        if not self.user_set_pattern:
            self.user_set_pattern = f"{self.key_prefix}:user:{{user_id}}"
    
    async def _ensure_initialized(self):
        """Ensure Redis connection is established"""
        if self._initialized:
            return
        
        try:
            self.redis = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=False  # Keep binary for pickle
            )
            
            # Test connection
            await self.redis.ping()
            
            self._initialized = True
            logger.info(f"Redis connection established to {self.host}:{self.port}/{self.db}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Redis storage: {e}")
            raise
    
    def _get_affinity_key(self, user_id: str, personality_name: str) -> str:
        """Get affinity key"""
        return self.affinity_key_pattern.format(
            user_id=user_id,
            personality_name=personality_name
        )
    
    def _get_fact_key(self, user_id: str, category: str, key: str) -> str:
        """Get fact key"""
        return self.fact_key_pattern.format(
            user_id=user_id,
            category=category,
            key=key
        )
    
    def _get_episode_key(self, user_id: str, episode_id: str) -> str:
        """Get episode key"""
        return self.episode_key_pattern.format(
            user_id=user_id,
            episode_id=episode_id
        )
    
    def _get_mood_key(self, user_id: str, mood_id: str) -> str:
        """Get mood key"""
        return self.mood_key_pattern.format(
            user_id=user_id,
            mood_id=mood_id
        )
    
    def _get_memory_key(self, user_id: str, memory_key: str) -> str:
        """Get memory key"""
        return self.memory_key_pattern.format(
            user_id=user_id,
            memory_key=memory_key
        )
    
    def _get_user_set_key(self, user_id: str, data_type: str) -> str:
        """Get user set key"""
        return self.user_set_pattern.format(user_id=user_id) + f":{data_type}"
    
    def _serialize_value(self, value: Any) -> bytes:
        """Serialize value for Redis storage"""
        try:
            return pickle.dumps(value)
        except:
            return json.dumps(value).encode('utf-8')
    
    def _deserialize_value(self, data: bytes) -> Any:
        """Deserialize value from Redis storage"""
        try:
            return pickle.loads(data)
        except:
            try:
                return json.loads(data.decode('utf-8'))
            except:
                return data.decode('utf-8')
    
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
                "session_id": kwargs.get('session_id', user_id),
                "created_at": kwargs.get('created_at', datetime.now().isoformat()),
                "updated_at": datetime.now().isoformat()
            }
            
            affinity_key = self._get_affinity_key(user_id, personality_name)
            user_affinity_set = self._get_user_set_key(user_id, "affinity")
            
            # Save affinity data
            await self.redis.set(affinity_key, self._serialize_value(affinity_data))
            
            # Add to user affinity set
            await self.redis.sadd(user_affinity_set, affinity_key)
            
            # Set TTL
            await self.redis.expire(affinity_key, self.ttl_days * 86400)
            await self.redis.expire(user_affinity_set, self.ttl_days * 86400)
            
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
            await self._ensure_initialized()
            
            affinity_key = self._get_affinity_key(user_id, personality_name)
            data = await self.redis.get(affinity_key)
            
            if data:
                affinity_data = self._deserialize_value(data)
                return {
                    "affinity_points": affinity_data.get('affinity_points', 0),
                    "current_level": affinity_data.get('current_level', 'stranger'),
                    "total_interactions": affinity_data.get('total_interactions', 0),
                    "positive_interactions": affinity_data.get('positive_interactions', 0),
                    "created_at": affinity_data.get('created_at'),
                    "updated_at": affinity_data.get('updated_at')
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
            await self._ensure_initialized()
            
            fact_data = {
                "category": category,
                "key": key,
                "value": value,
                "confidence": kwargs.get('confidence', 1.0),
                "session_id": kwargs.get('session_id', user_id),
                "created_at": kwargs.get('created_at', datetime.now().isoformat()),
                "updated_at": datetime.now().isoformat()
            }
            
            fact_key = self._get_fact_key(user_id, category, key)
            user_facts_set = self._get_user_set_key(user_id, "facts")
            
            # Save fact data
            await self.redis.set(fact_key, self._serialize_value(fact_data))
            
            # Add to user facts set
            await self.redis.sadd(user_facts_set, fact_key)
            
            # Set TTL
            await self.redis.expire(fact_key, self.ttl_days * 86400)
            await self.redis.expire(user_facts_set, self.ttl_days * 86400)
            
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
            
            user_facts_set = self._get_user_set_key(user_id, "facts")
            fact_keys = await self.redis.smembers(user_facts_set)
            
            facts = []
            for fact_key in fact_keys:
                try:
                    fact_key_str = fact_key.decode('utf-8') if isinstance(fact_key, bytes) else fact_key
                    data = await self.redis.get(fact_key_str)
                    
                    if data:
                        fact_data = self._deserialize_value(data)
                        
                        # Filter by category if specified
                        if category and fact_data.get('category') != category:
                            continue
                        
                        facts.append({
                            'category': fact_data['category'],
                            'key': fact_data['key'],
                            'value': fact_data['value'],
                            'confidence': fact_data.get('confidence', 1.0),
                            'created_at': fact_data.get('created_at'),
                            'updated_at': fact_data.get('updated_at')
                        })
                        
                except Exception as e:
                    logger.warning(f"Failed to parse fact {fact_key}: {e}")
                    continue
            
            # Sort by created_at
            facts.sort(key=lambda x: x.get('created_at', ''), reverse=True)
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
            await self._ensure_initialized()
            
            fact_key = self._get_fact_key(user_id, category, key)
            user_facts_set = self._get_user_set_key(user_id, "facts")
            
            # Remove from Redis and user set
            await self.redis.delete(fact_key)
            await self.redis.srem(user_facts_set, fact_key)
            
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
            await self._ensure_initialized()
            
            episode_id = f"{episode_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            episode_data = {
                "episode_type": episode_type,
                "title": title,
                "summary": summary,
                "importance": importance,
                "sentiment": sentiment,
                "session_id": kwargs.get('session_id', user_id),
                "created_at": kwargs.get('created_at', datetime.now().isoformat()),
                "updated_at": datetime.now().isoformat()
            }
            
            episode_key = self._get_episode_key(user_id, episode_id)
            user_episodes_set = self._get_user_set_key(user_id, "episodes")
            
            # Save episode data
            await self.redis.set(episode_key, self._serialize_value(episode_data))
            
            # Add to user episodes set
            await self.redis.sadd(user_episodes_set, episode_key)
            
            # Set TTL
            await self.redis.expire(episode_key, self.ttl_days * 86400)
            await self.redis.expire(user_episodes_set, self.ttl_days * 86400)
            
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
            await self._ensure_initialized()
            
            user_episodes_set = self._get_user_set_key(user_id, "episodes")
            episode_keys = await self.redis.smembers(user_episodes_set)
            
            episodes = []
            for episode_key in episode_keys:
                try:
                    episode_key_str = episode_key.decode('utf-8') if isinstance(episode_key, bytes) else episode_key
                    data = await self.redis.get(episode_key_str)
                    
                    if data:
                        episode_data = self._deserialize_value(data)
                        importance = episode_data.get('importance', 0.0)
                        
                        # Filter by importance if specified
                        if min_importance is not None and importance < min_importance:
                            continue
                        
                        episodes.append({
                            'episode_type': episode_data['episode_type'],
                            'title': episode_data['title'],
                            'summary': episode_data['summary'],
                            'importance': importance,
                            'sentiment': episode_data['sentiment'],
                            'created_at': episode_data.get('created_at'),
                            'updated_at': episode_data.get('updated_at')
                        })
                        
                except Exception as e:
                    logger.warning(f"Failed to parse episode {episode_key}: {e}")
                    continue
            
            # Sort by importance and limit results
            episodes.sort(key=lambda x: x['importance'], reverse=True)
            if max_results:
                episodes = episodes[:max_results]
            
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
            await self._ensure_initialized()
            
            mood_id = f"{mood_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            mood_data = {
                "mood_type": mood_type,
                "intensity": intensity,
                "context": context,
                "session_id": kwargs.get('session_id', user_id),
                "created_at": kwargs.get('created_at', datetime.now().isoformat()),
                "updated_at": datetime.now().isoformat()
            }
            
            mood_key = self._get_mood_key(user_id, mood_id)
            user_moods_set = self._get_user_set_key(user_id, "moods")
            
            # Save mood data
            await self.redis.set(mood_key, self._serialize_value(mood_data))
            
            # Add to user moods set
            await self.redis.sadd(user_moods_set, mood_key)
            
            # Set TTL (shorter for moods)
            mood_ttl = min(self.ttl_days, 30) * 86400  # Max 30 days for moods
            await self.redis.expire(mood_key, mood_ttl)
            await self.redis.expire(user_moods_set, mood_ttl)
            
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
            await self._ensure_initialized()
            
            user_moods_set = self._get_user_set_key(user_id, "moods")
            mood_keys = await self.redis.smembers(user_moods_set)
            
            moods = []
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            for mood_key in mood_keys:
                try:
                    mood_key_str = mood_key.decode('utf-8') if isinstance(mood_key, bytes) else mood_key
                    data = await self.redis.get(mood_key_str)
                    
                    if data:
                        mood_data = self._deserialize_value(data)
                        
                        # Filter by mood type if specified
                        if mood_type and mood_data.get('mood_type') != mood_type:
                            continue
                        
                        # Filter by date
                        created_at = mood_data.get('created_at')
                        if created_at:
                            try:
                                mood_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                                if mood_date < cutoff_date:
                                    continue
                            except:
                                pass  # Include if date parsing fails
                        
                        moods.append({
                            'mood_type': mood_data['mood_type'],
                            'intensity': mood_data['intensity'],
                            'context': mood_data['context'],
                            'created_at': created_at,
                            'updated_at': mood_data.get('updated_at')
                        })
                        
                except Exception as e:
                    logger.warning(f"Failed to parse mood {mood_key}: {e}")
                    continue
            
            # Sort by date
            moods.sort(key=lambda x: x['created_at'] or '', reverse=True)
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
            await self._ensure_initialized()
            
            memory_data = {
                "memory_key": memory_key,
                "memory_value": memory_value,
                "session_id": kwargs.get('session_id', user_id),
                "created_at": kwargs.get('created_at', datetime.now().isoformat()),
                "updated_at": datetime.now().isoformat()
            }
            
            redis_memory_key = self._get_memory_key(user_id, memory_key)
            user_memories_set = self._get_user_set_key(user_id, "memories")
            
            # Save memory data
            await self.redis.set(redis_memory_key, self._serialize_value(memory_data))
            
            # Add to user memories set
            await self.redis.sadd(user_memories_set, redis_memory_key)
            
            # Set TTL
            await self.redis.expire(redis_memory_key, self.ttl_days * 86400)
            await self.redis.expire(user_memories_set, self.ttl_days * 86400)
            
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
            await self._ensure_initialized()
            
            redis_memory_key = self._get_memory_key(user_id, memory_key)
            data = await self.redis.get(redis_memory_key)
            
            if data:
                memory_data = self._deserialize_value(data)
                return memory_data.get('memory_value')
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
            await self._ensure_initialized()
            
            redis_memory_key = self._get_memory_key(user_id, memory_key)
            user_memories_set = self._get_user_set_key(user_id, "memories")
            
            # Remove from Redis and user set
            await self.redis.delete(redis_memory_key)
            await self.redis.srem(user_memories_set, redis_memory_key)
            
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
            await self._ensure_initialized()
            
            session_key = self._get_session_key(session_id)
            session_data = {
                'session_id': session_id,
                'user_id': user_id,
                'personality_name': personality_name,
                'created_at': kwargs.get('created_at', datetime.now().isoformat()),
                'updated_at': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat(),
                'ttl': kwargs.get('ttl', int((datetime.now() + timedelta(days=30)).timestamp()))
            }
            
            # Save session data
            await self.redis.hset(session_key, mapping=session_data)
            
            # Set TTL
            ttl_seconds = int((datetime.now() + timedelta(days=30)).timestamp()) - int(datetime.now().timestamp())
            await self.redis.expire(session_key, ttl_seconds)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
            return False
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        try:
            await self._ensure_initialized()
            
            session_key = self._get_session_key(session_id)
            session_data = await self.redis.hgetall(session_key)
            
            if session_data:
                return {k.decode() if isinstance(k, bytes) else k: 
                       v.decode() if isinstance(v, bytes) else v 
                       for k, v in session_data.items()}
            return None
            
        except Exception as e:
            logger.error(f"Failed to get session: {e}")
            return None
    
    async def update_session_activity(self, session_id: str) -> bool:
        """Update session activity"""
        try:
            await self._ensure_initialized()
            
            session_key = self._get_session_key(session_id)
            await self.redis.hset(session_key, mapping={
                'last_activity': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update session activity: {e}")
            return False
    
    async def get_expired_sessions(self) -> List[Dict[str, Any]]:
        """Get expired sessions"""
        try:
            await self._ensure_initialized()
            
            current_time = datetime.now().timestamp()
            expired_sessions = []
            
            # Get all session keys
            session_keys = await self.redis.keys(f"{self.key_prefix}:sessions:*")
            
            for session_key in session_keys:
                session_data = await self.redis.hgetall(session_key)
                if session_data:
                    ttl = session_data.get(b'ttl', session_data.get('ttl'))
                    if ttl and float(ttl) < current_time:
                        session_dict = {k.decode() if isinstance(k, bytes) else k: 
                                       v.decode() if isinstance(v, bytes) else v 
                                       for k, v in session_data.items()}
                        expired_sessions.append(session_dict)
            
            return expired_sessions
            
        except Exception as e:
            logger.error(f"Failed to get expired sessions: {e}")
            return []
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete session"""
        try:
            await self._ensure_initialized()
            
            session_key = self._get_session_key(session_id)
            await self.redis.delete(session_key)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete session: {e}")
            return False
    
    def _get_session_key(self, session_id: str) -> str:
        """Get session key"""
        return f"{self.key_prefix}:sessions:{session_id}"
