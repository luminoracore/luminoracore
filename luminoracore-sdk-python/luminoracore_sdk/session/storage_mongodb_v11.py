"""
MongoDB Storage v1.1 Implementation

Real MongoDB implementation for v1.1 storage with persistent data.
"""

import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

try:
    from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
    from pymongo.errors import PyMongoError
except ImportError:
    AsyncIOMotorClient = None
    AsyncIOMotorDatabase = None
    AsyncIOMotorCollection = None
    PyMongoError = Exception

from .storage_v1_1 import StorageV11Extension

logger = logging.getLogger(__name__)


class MongoDBStorageV11(StorageV11Extension):
    """
    Real MongoDB storage implementation for v1.1 features
    """
    
    def __init__(self, connection_string: str, database_name: str = "luminoracore_v11"):
        """
        Initialize MongoDB storage
        
        Args:
            connection_string: MongoDB connection string
            database_name: Database name
        """
        if AsyncIOMotorClient is None:
            raise ImportError("motor is required for MongoDB storage. Install with: pip install motor")
        
        self.connection_string = connection_string
        self.database_name = database_name
        self.client: Optional[AsyncIOMotorClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None
        self._ensure_initialized = False
        
        # Collection names
        self.AFFINITY_COLLECTION = "user_affinity"
        self.FACTS_COLLECTION = "user_facts"
        self.EPISODES_COLLECTION = "user_episodes"
        self.MOOD_COLLECTION = "user_mood"
        self.MEMORY_COLLECTION = "conversation_memory"
    
    async def _ensure_initialized(self):
        """Ensure MongoDB connection and collections exist"""
        if self._ensure_initialized:
            return
        
        try:
            # Create client and connect
            self.client = AsyncIOMotorClient(self.connection_string)
            self.database = self.client[self.database_name]
            
            # Test connection
            await self.client.admin.command('ping')
            
            # Create collections and indexes
            await self._create_collections()
            
            self._ensure_initialized = True
            logger.info("MongoDB database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize MongoDB database: {e}")
            raise
    
    async def _create_collections(self):
        """Create collections and indexes"""
        try:
            # Create affinity collection and indexes
            affinity_collection = self.database[self.AFFINITY_COLLECTION]
            await affinity_collection.create_index([("user_id", 1), ("personality_name", 1)], unique=True)
            await affinity_collection.create_index("user_id")
            
            # Create facts collection and indexes
            facts_collection = self.database[self.FACTS_COLLECTION]
            await facts_collection.create_index([("user_id", 1), ("category", 1), ("key", 1)], unique=True)
            await facts_collection.create_index("user_id")
            await facts_collection.create_index("category")
            
            # Create episodes collection and indexes
            episodes_collection = self.database[self.EPISODES_COLLECTION]
            await episodes_collection.create_index("user_id")
            await episodes_collection.create_index([("user_id", 1), ("importance", -1)])
            await episodes_collection.create_index("importance")
            
            # Create mood collection and indexes
            mood_collection = self.database[self.MOOD_COLLECTION]
            await mood_collection.create_index("user_id")
            await mood_collection.create_index("session_id")
            
            # Create memory collection and indexes
            memory_collection = self.database[self.MEMORY_COLLECTION]
            await memory_collection.create_index([("session_id", 1), ("memory_key", 1)], unique=True)
            await memory_collection.create_index("session_id")
            await memory_collection.create_index("expires_at", expireAfterSeconds=0)
            
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
            
            affinity_collection = self.database[self.AFFINITY_COLLECTION]
            
            affinity_data = {
                "user_id": user_id,
                "personality_name": personality_name,
                "affinity_points": affinity_points,
                "current_level": current_level,
                "total_interactions": kwargs.get('total_interactions', 0),
                "positive_interactions": kwargs.get('positive_interactions', 0),
                "created_at": kwargs.get('created_at', datetime.now()),
                "updated_at": datetime.now()
            }
            
            await affinity_collection.replace_one(
                {"user_id": user_id, "personality_name": personality_name},
                affinity_data,
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
        """Get user affinity data"""
        try:
            await self._ensure_initialized()
            
            affinity_collection = self.database[self.AFFINITY_COLLECTION]
            
            result = await affinity_collection.find_one({
                "user_id": user_id,
                "personality_name": personality_name
            })
            
            if result:
                # Convert ObjectId and datetime to serializable formats
                result.pop('_id', None)
                if result.get('created_at'):
                    result['created_at'] = result['created_at'].isoformat()
                if result.get('updated_at'):
                    result['updated_at'] = result['updated_at'].isoformat()
                return result
            
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
            
            facts_collection = self.database[self.FACTS_COLLECTION]
            
            fact_data = {
                "user_id": user_id,
                "category": category,
                "key": key,
                "value": value,
                "confidence": kwargs.get('confidence', 1.0),
                "created_at": kwargs.get('created_at', datetime.now()),
                "updated_at": datetime.now()
            }
            
            await facts_collection.replace_one(
                {"user_id": user_id, "category": category, "key": key},
                fact_data,
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
            
            facts_collection = self.database[self.FACTS_COLLECTION]
            
            query = {"user_id": user_id}
            if category:
                query["category"] = category
            
            cursor = facts_collection.find(query).sort("created_at", -1)
            facts = []
            
            async for doc in cursor:
                # Convert ObjectId and datetime to serializable formats
                doc.pop('_id', None)
                if doc.get('created_at'):
                    doc['created_at'] = doc['created_at'].isoformat()
                if doc.get('updated_at'):
                    doc['updated_at'] = doc['updated_at'].isoformat()
                facts.append(doc)
            
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
            
            episodes_collection = self.database[self.EPISODES_COLLECTION]
            
            episode_data = {
                "user_id": user_id,
                "episode_type": episode_type,
                "title": title,
                "summary": summary,
                "importance": importance,
                "sentiment": sentiment,
                "created_at": kwargs.get('created_at', datetime.now())
            }
            
            await episodes_collection.insert_one(episode_data)
            
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
            
            episodes_collection = self.database[self.EPISODES_COLLECTION]
            
            query = {"user_id": user_id}
            if min_importance is not None:
                query["importance"] = {"$gte": min_importance}
            
            cursor = episodes_collection.find(query).sort([("importance", -1), ("created_at", -1)])
            episodes = []
            
            async for doc in cursor:
                # Convert ObjectId and datetime to serializable formats
                doc.pop('_id', None)
                if doc.get('created_at'):
                    doc['created_at'] = doc['created_at'].isoformat()
                episodes.append(doc)
            
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
            
            mood_collection = self.database[self.MOOD_COLLECTION]
            
            mood_data = {
                "session_id": session_id,
                "user_id": user_id,
                "current_mood": current_mood,
                "mood_intensity": mood_intensity,
                "created_at": datetime.now()
            }
            
            await mood_collection.insert_one(mood_data)
            
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
            
            mood_collection = self.database[self.MOOD_COLLECTION]
            
            cursor = mood_collection.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
            moods = []
            
            async for doc in cursor:
                # Convert ObjectId and datetime to serializable formats
                doc.pop('_id', None)
                if doc.get('created_at'):
                    doc['created_at'] = doc['created_at'].isoformat()
                moods.append(doc)
            
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
            
            memory_collection = self.database[self.MEMORY_COLLECTION]
            
            memory_data = {
                "session_id": session_id,
                "user_id": user_id,
                "memory_key": key,
                "memory_value": value,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            
            if expires_at:
                memory_data["expires_at"] = expires_at
            
            await memory_collection.replace_one(
                {"session_id": session_id, "memory_key": key},
                memory_data,
                upsert=True
            )
            
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
            
            memory_collection = self.database[self.MEMORY_COLLECTION]
            
            result = await memory_collection.find_one({
                "session_id": session_id,
                "memory_key": key
            })
            
            if result:
                # Check if expired
                if result.get("expires_at") and result["expires_at"] < datetime.now():
                    return None
                
                return result["memory_value"]
            
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
            
            memory_collection = self.database[self.MEMORY_COLLECTION]
            
            await memory_collection.delete_one({
                "session_id": session_id,
                "memory_key": key
            })
            
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
            
            memory_collection = self.database[self.MEMORY_COLLECTION]
            
            cursor = memory_collection.find({"session_id": session_id})
            memories = {}
            
            async for doc in cursor:
                # Check if expired
                if doc.get("expires_at") and doc["expires_at"] < datetime.now():
                    continue
                
                memories[doc["memory_key"]] = doc["memory_value"]
            
            return memories
            
        except Exception as e:
            logger.error(f"Failed to get all memories: {e}")
            return {}
    
    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
