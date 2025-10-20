"""
Flexible MongoDB Storage v11 Implementation

This implementation allows users to use ANY MongoDB database with ANY collection structure.
"""

import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

try:
    from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
except ImportError:
    AsyncIOMotorClient = None
    AsyncIOMotorDatabase = None
    AsyncIOMotorCollection = None

from .storage_v1_1 import StorageV11Extension

logger = logging.getLogger(__name__)


class FlexibleMongoDBStorageV11(StorageV11Extension):
    """
    Flexible MongoDB storage that adapts to ANY collection structure
    
    The user can use their own MongoDB databases with any collection names.
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 27017,
        database: str = "luminoracore_v11",
        username: Optional[str] = None,
        password: Optional[str] = None,
        auth_source: str = "admin",
        facts_collection: str = None,
        affinity_collection: str = None,
        episodes_collection: str = None,
        moods_collection: str = None,
        memories_collection: str = None,
        auto_create_collections: bool = True
    ):
        """
        Initialize flexible MongoDB storage
        
        Args:
            host: MongoDB host
            port: MongoDB port
            database: Database name (user's database)
            username: MongoDB username
            password: MongoDB password
            auth_source: Authentication source
            facts_collection: Name of facts collection (auto-detected if None)
            affinity_collection: Name of affinity collection (auto-detected if None)
            episodes_collection: Name of episodes collection (auto-detected if None)
            moods_collection: Name of moods collection (auto-detected if None)
            memories_collection: Name of memories collection (auto-detected if None)
            auto_create_collections: Whether to create collections if they don't exist
        """
        if AsyncIOMotorClient is None:
            raise ImportError("motor is required for MongoDB storage. Install with: pip install motor")
        
        self.host = host
        self.port = port
        self.database_name = database
        self.username = username
        self.password = password
        self.auth_source = auth_source
        self.auto_create_collections = auto_create_collections
        
        # Collection names (user's choice or auto-detected)
        self.facts_collection = facts_collection
        self.affinity_collection = affinity_collection
        self.episodes_collection = episodes_collection
        self.moods_collection = moods_collection
        self.memories_collection = memories_collection
        
        self.client: Optional[AsyncIOMotorClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None
        self._initialized = False
        
        logger.info(f"Flexible MongoDB storage initialized for database: {database}")
    
    async def _ensure_initialized(self):
        """Ensure MongoDB connection and collections exist"""
        if self._initialized:
            return
        
        try:
            # Create MongoDB connection
            if self.username and self.password:
                connection_string = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}?authSource={self.auth_source}"
            else:
                connection_string = f"mongodb://{self.host}:{self.port}/{self.database_name}"
            
            self.client = AsyncIOMotorClient(connection_string)
            self.database = self.client[self.database_name]
            
            # Test connection
            await self.client.admin.command('ping')
            
            # Auto-detect collection names if not provided
            await self._detect_collections()
            
            # Create collections if needed
            if self.auto_create_collections:
                await self._ensure_collections_exist()
            
            self._initialized = True
            logger.info(f"MongoDB connection established to {self.host}:{self.port}/{self.database_name}")
            logger.info(f"Collections: {self.facts_collection}, {self.affinity_collection}")
            
        except Exception as e:
            logger.error(f"Failed to initialize MongoDB storage: {e}")
            raise
    
    async def _detect_collections(self):
        """Auto-detect collection names from existing database"""
        try:
            existing_collections = await self.database.list_collection_names()
            
            # Common collection name patterns
            if not self.facts_collection:
                possible_names = ['facts', 'user_facts', 'luminora_facts', 'facts_collection']
                self.facts_collection = next((name for name in possible_names if name in existing_collections), 'facts')
            
            if not self.affinity_collection:
                possible_names = ['affinity', 'user_affinity', 'luminora_affinity', 'affinity_collection']
                self.affinity_collection = next((name for name in possible_names if name in existing_collections), 'affinity')
            
            if not self.episodes_collection:
                possible_names = ['episodes', 'user_episodes', 'luminora_episodes', 'episodes_collection']
                self.episodes_collection = next((name for name in possible_names if name in existing_collections), 'episodes')
            
            if not self.moods_collection:
                possible_names = ['moods', 'user_moods', 'luminora_moods', 'moods_collection']
                self.moods_collection = next((name for name in possible_names if name in existing_collections), 'moods')
            
            if not self.memories_collection:
                possible_names = ['memories', 'user_memories', 'luminora_memories', 'memories_collection']
                self.memories_collection = next((name for name in possible_names if name in existing_collections), 'memories')
            
            logger.info(f"Detected collections: {existing_collections}")
            
        except Exception as e:
            logger.warning(f"Could not detect collections: {e}")
            # Use defaults
            self.facts_collection = self.facts_collection or 'facts'
            self.affinity_collection = self.affinity_collection or 'affinity'
            self.episodes_collection = self.episodes_collection or 'episodes'
            self.moods_collection = self.moods_collection or 'moods'
            self.memories_collection = self.memories_collection or 'memories'
    
    async def _ensure_collections_exist(self):
        """Create collections and indexes if they don't exist"""
        try:
            # Facts collection
            facts_coll = self.database[self.facts_collection]
            await facts_coll.create_index([("user_id", 1), ("category", 1), ("key", 1)], unique=True)
            await facts_coll.create_index([("user_id", 1), ("created_at", -1)])
            
            # Affinity collection
            affinity_coll = self.database[self.affinity_collection]
            await affinity_coll.create_index([("user_id", 1), ("personality_name", 1)], unique=True)
            await affinity_coll.create_index([("user_id", 1)])
            
            # Episodes collection
            episodes_coll = self.database[self.episodes_collection]
            await episodes_coll.create_index([("user_id", 1), ("importance", -1)])
            await episodes_coll.create_index([("user_id", 1), ("created_at", -1)])
            
            # Moods collection
            moods_coll = self.database[self.moods_collection]
            await moods_coll.create_index([("user_id", 1), ("created_at", -1)])
            await moods_coll.create_index([("user_id", 1), ("mood_type", 1)])
            
            # Memories collection
            memories_coll = self.database[self.memories_collection]
            await memories_coll.create_index([("user_id", 1), ("memory_key", 1)], unique=True)
            await memories_coll.create_index([("user_id", 1)])
            
            logger.info(f"Collections and indexes created/verified")
            
        except Exception as e:
            logger.error(f"Failed to create collections: {e}")
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
            await self._ensure_initialized()
            
            affinity_data = {
                "user_id": user_id,
                "session_id": kwargs.get('session_id', user_id),
                "personality_name": personality_name,
                "affinity_points": affinity_points,
                "current_level": current_level,
                "total_interactions": kwargs.get('total_interactions', 0),
                "positive_interactions": kwargs.get('positive_interactions', 0),
                "created_at": kwargs.get('created_at', datetime.now()),
                "updated_at": datetime.now()
            }
            
            affinity_coll = self.database[self.affinity_collection]
            
            # Use upsert to update or insert
            await affinity_coll.update_one(
                {"user_id": user_id, "personality_name": personality_name},
                {"$set": affinity_data},
                upsert=True
            )
            
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
            
            affinity_coll = self.database[self.affinity_collection]
            affinity_doc = await affinity_coll.find_one({
                "user_id": user_id,
                "personality_name": personality_name
            })
            
            if affinity_doc:
                return {
                    "affinity_points": affinity_doc.get('affinity_points', 0),
                    "current_level": affinity_doc.get('current_level', 'stranger'),
                    "total_interactions": affinity_doc.get('total_interactions', 0),
                    "positive_interactions": affinity_doc.get('positive_interactions', 0),
                    "created_at": affinity_doc.get('created_at').isoformat() if affinity_doc.get('created_at') else None,
                    "updated_at": affinity_doc.get('updated_at').isoformat() if affinity_doc.get('updated_at') else None
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
                "user_id": user_id,
                "session_id": kwargs.get('session_id', user_id),
                "category": category,
                "key": key,
                "value": value,
                "confidence": kwargs.get('confidence', 1.0),
                "created_at": kwargs.get('created_at', datetime.now()),
                "updated_at": datetime.now()
            }
            
            facts_coll = self.database[self.facts_collection]
            
            # Use upsert to update or insert
            await facts_coll.update_one(
                {"user_id": user_id, "category": category, "key": key},
                {"$set": fact_data},
                upsert=True
            )
            
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
            
            facts_coll = self.database[self.facts_collection]
            
            query = {"user_id": user_id}
            if category:
                query["category"] = category
            
            cursor = facts_coll.find(query).sort("created_at", -1)
            
            facts = []
            async for fact_doc in cursor:
                facts.append({
                    'category': fact_doc['category'],
                    'key': fact_doc['key'],
                    'value': fact_doc['value'],
                    'confidence': fact_doc.get('confidence', 1.0),
                    'created_at': fact_doc.get('created_at').isoformat() if fact_doc.get('created_at') else None,
                    'updated_at': fact_doc.get('updated_at').isoformat() if fact_doc.get('updated_at') else None
                })
            
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
            
            facts_coll = self.database[self.facts_collection]
            result = await facts_coll.delete_one({
                "user_id": user_id,
                "category": category,
                "key": key
            })
            
            return result.deleted_count > 0
            
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
            
            episode_data = {
                "user_id": user_id,
                "session_id": kwargs.get('session_id', user_id),
                "episode_type": episode_type,
                "title": title,
                "summary": summary,
                "importance": importance,
                "sentiment": sentiment,
                "created_at": kwargs.get('created_at', datetime.now()),
                "updated_at": datetime.now()
            }
            
            episodes_coll = self.database[self.episodes_collection]
            await episodes_coll.insert_one(episode_data)
            
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
            
            episodes_coll = self.database[self.episodes_collection]
            
            query = {"user_id": user_id}
            if min_importance is not None:
                query["importance"] = {"$gte": min_importance}
            
            cursor = episodes_coll.find(query).sort([("importance", -1), ("created_at", -1)])
            
            if max_results:
                cursor = cursor.limit(max_results)
            
            episodes = []
            async for episode_doc in cursor:
                episodes.append({
                    'episode_type': episode_doc['episode_type'],
                    'title': episode_doc['title'],
                    'summary': episode_doc['summary'],
                    'importance': episode_doc['importance'],
                    'sentiment': episode_doc['sentiment'],
                    'created_at': episode_doc.get('created_at').isoformat() if episode_doc.get('created_at') else None,
                    'updated_at': episode_doc.get('updated_at').isoformat() if episode_doc.get('updated_at') else None
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
            await self._ensure_initialized()
            
            mood_data = {
                "user_id": user_id,
                "session_id": kwargs.get('session_id', user_id),
                "mood_type": mood_type,
                "intensity": intensity,
                "context": context,
                "created_at": kwargs.get('created_at', datetime.now()),
                "updated_at": datetime.now()
            }
            
            moods_coll = self.database[self.moods_collection]
            await moods_coll.insert_one(mood_data)
            
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
            
            moods_coll = self.database[self.moods_collection]
            
            query = {
                "user_id": user_id,
                "created_at": {"$gte": datetime.now() - timedelta(days=days_back)}
            }
            
            if mood_type:
                query["mood_type"] = mood_type
            
            cursor = moods_coll.find(query).sort("created_at", -1)
            
            moods = []
            async for mood_doc in cursor:
                moods.append({
                    'mood_type': mood_doc['mood_type'],
                    'intensity': mood_doc['intensity'],
                    'context': mood_doc['context'],
                    'created_at': mood_doc.get('created_at').isoformat() if mood_doc.get('created_at') else None,
                    'updated_at': mood_doc.get('updated_at').isoformat() if mood_doc.get('updated_at') else None
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
            await self._ensure_initialized()
            
            memory_data = {
                "user_id": user_id,
                "session_id": kwargs.get('session_id', user_id),
                "memory_key": memory_key,
                "memory_value": memory_value,
                "created_at": kwargs.get('created_at', datetime.now()),
                "updated_at": datetime.now()
            }
            
            memories_coll = self.database[self.memories_collection]
            
            # Use upsert to update or insert
            await memories_coll.update_one(
                {"user_id": user_id, "memory_key": memory_key},
                {"$set": memory_data},
                upsert=True
            )
            
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
            
            memories_coll = self.database[self.memories_collection]
            memory_doc = await memories_coll.find_one({
                "user_id": user_id,
                "memory_key": memory_key
            })
            
            if memory_doc:
                return memory_doc.get('memory_value')
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
            
            memories_coll = self.database[self.memories_collection]
            result = await memories_coll.delete_one({
                "user_id": user_id,
                "memory_key": memory_key
            })
            
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Failed to delete memory: {e}")
            return False
