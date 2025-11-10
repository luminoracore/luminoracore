"""
New LuminoraCore SDK Client
Uses the core directly instead of depending on SDK components
"""

import asyncio
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

# Import from core directly
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'luminoracore'))

from luminoracore import PersonalityEngine, MemorySystem, EvolutionEngine, InMemoryStorage
from luminoracore.interfaces import StorageInterface


class LuminoraCoreClientNew:
    """New SDK client that uses core directly"""
    
    def __init__(self, storage: Optional[StorageInterface] = None, storage_config: Optional[Dict] = None):
        """
        Initialize the client
        
        Args:
            storage: Storage interface implementation
            storage_config: Configuration for storage (if storage not provided)
        """
        # Initialize core components
        self.personality_engine = PersonalityEngine()
        self.evolution_engine = EvolutionEngine()
        
        # Set up storage
        if storage:
            self.storage = storage
        elif storage_config:
            self.storage = self._create_storage_from_config(storage_config)
        else:
            # Default to in-memory storage
            self.storage = InMemoryStorage()
        
        # Initialize memory system
        self.memory_system = MemorySystem(self.storage)
        
        # Set evolution engine in personality engine
        self.personality_engine.evolution_engine = self.evolution_engine
    
    def _create_storage_from_config(self, config: Dict) -> StorageInterface:
        """Create storage from configuration"""
        storage_type = config.get('storage_type', 'memory')
        
        if storage_type == 'memory':
            return InMemoryStorage()
        else:
            # For now, default to in-memory
            # In the future, this would create other storage types
            return InMemoryStorage()
    
    # Personality methods
    async def load_personality(self, name: str, data: Dict) -> bool:
        """Load a personality"""
        return await self.personality_engine.load_personality(name, data)
    
    async def get_personality(self, name: str) -> Optional[Dict]:
        """Get personality by name"""
        return await self.personality_engine.get_personality(name)
    
    async def list_personalities(self) -> List[str]:
        """List all personalities"""
        return await self.personality_engine.list_personalities()
    
    async def blend_personalities(self, personalities: List[str], weights: List[float]) -> Dict:
        """Blend multiple personalities"""
        return await self.personality_engine.blend_personalities(personalities, weights)
    
    # Memory methods
    async def save_fact(self, user_id: str, category: str, key: str, value: Any, confidence: float = 0.8) -> bool:
        """Save a fact for a user"""
        return await self.storage.save_fact(user_id, category, key, value, confidence)
    
    async def get_facts(self, user_id: str, category: Optional[str] = None) -> List[Dict]:
        """Get facts for a user"""
        return await self.storage.get_facts(user_id, category)
    
    async def save_episode(self, user_id: str, episode_type: str, title: str, summary: str, 
                          importance: float = 0.5, sentiment: str = "neutral", 
                          metadata: Optional[Dict] = None) -> bool:
        """Save an episode for a user"""
        return await self.storage.save_episode(user_id, episode_type, title, summary, 
                                             importance, sentiment, metadata)
    
    async def get_episodes(self, user_id: str, min_importance: Optional[float] = None, 
                          limit: Optional[int] = None) -> List[Dict]:
        """Get episodes for a user"""
        return await self.storage.get_episodes(user_id, min_importance, limit)
    
    async def update_affinity(self, user_id: str, personality_name: str, points_delta: int, 
                             interaction_type: str = "neutral") -> Dict:
        """Update affinity between user and personality"""
        return await self.storage.update_affinity(user_id, personality_name, points_delta, 
                                                interaction_type)
    
    async def get_affinity(self, user_id: str, personality_name: str) -> Optional[Dict]:
        """Get affinity between user and personality"""
        return await self.storage.get_affinity(user_id, personality_name)
    
    async def get_all_affinities(self, user_id: str) -> List[Dict]:
        """Get all affinities for a user"""
        return await self.storage.get_all_affinities(user_id)
    
    # Search methods
    async def search_facts(self, user_id: str, query: str, limit: Optional[int] = None) -> List[Dict]:
        """Search facts using semantic search"""
        return await self.storage.search_facts(user_id, query, limit)
    
    async def search_episodes(self, user_id: str, query: str, limit: Optional[int] = None) -> List[Dict]:
        """Search episodes using semantic search"""
        return await self.storage.search_episodes(user_id, query, limit)
    
    # Context methods
    async def get_user_context(self, user_id: str) -> Dict:
        """Get comprehensive user context"""
        return await self.memory_system.get_user_context(user_id)
    
    async def get_relevant_memories(self, user_id: str, context: str, 
                                   memory_types: List[str] = None) -> List[Dict]:
        """Get relevant memories for context"""
        return await self.memory_system.get_relevant_memories(user_id, context, memory_types)
    
    # Evolution methods
    async def evolve_personality(self, personality_name: str, user_id: str, 
                                interaction_data: Dict) -> Dict:
        """Evolve personality based on interaction"""
        return await self.personality_engine.evolve_personality(personality_name, user_id, 
                                                               interaction_data)
    
    # Stats methods
    async def get_user_stats(self, user_id: str) -> Dict:
        """Get statistics for a user"""
        return await self.storage.get_user_stats(user_id)
    
    async def get_memory_stats(self, user_id: str) -> Dict:
        """Get memory statistics for a user"""
        return await self.memory_system.get_memory_stats(user_id)
    
    # Health methods
    async def health_check(self) -> Dict:
        """Check system health"""
        return await self.storage.health_check()
    
    # Utility methods
    async def cleanup_old_data(self, days_old: int = 365) -> int:
        """Clean up old data"""
        return await self.storage.cleanup_old_data(days_old)
