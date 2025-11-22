"""
In-Memory Storage Implementation
Simple in-memory storage for development and testing
"""

from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from .base_storage import BaseStorage


class InMemoryStorage(BaseStorage):
    """In-memory storage implementation"""
    
    def __init__(self):
        super().__init__()
        self.name = "InMemoryStorage"
        self.description = "Simple in-memory storage for development and testing"
    
    async def save_fact(self, user_id: str, category: str, key: str, value: Any, confidence: float = 0.8) -> bool:
        """Save a fact for a user"""
        return await super().save_fact(user_id, category, key, value, confidence)
    
    async def get_facts(self, user_id: str, category: Optional[str] = None) -> List[Dict]:
        """Get facts for a user, optionally filtered by category"""
        return await super().get_facts(user_id, category)
    
    async def update_fact(self, user_id: str, category: str, key: str, value: Any, confidence: float = 0.8) -> bool:
        """Update an existing fact"""
        return await super().update_fact(user_id, category, key, value, confidence)
    
    async def delete_fact(self, user_id: str, category: str, key: str) -> bool:
        """Delete a fact"""
        return await super().delete_fact(user_id, category, key)
    
    async def save_episode(self, user_id: str, episode_type: str, title: str, summary: str, 
                          importance: float = 0.5, sentiment: str = "neutral", 
                          metadata: Optional[Dict] = None) -> bool:
        """Save an episode for a user"""
        return await super().save_episode(user_id, episode_type, title, summary, importance, sentiment, metadata)
    
    async def get_episodes(self, user_id: str, min_importance: Optional[float] = None, 
                          limit: Optional[int] = None) -> List[Dict]:
        """Get episodes for a user, optionally filtered by importance"""
        return await super().get_episodes(user_id, min_importance, limit)
    
    async def update_episode(self, user_id: str, episode_id: str, **kwargs) -> bool:
        """Update an existing episode"""
        return await super().update_episode(user_id, episode_id, **kwargs)
    
    async def delete_episode(self, user_id: str, episode_id: str) -> bool:
        """Delete an episode"""
        return await super().delete_episode(user_id, episode_id)
    
    async def update_affinity(self, user_id: str, personality_name: str, points_delta: int, 
                             interaction_type: str = "neutral") -> Dict:
        """Update affinity between user and personality"""
        return await super().update_affinity(user_id, personality_name, points_delta, interaction_type)
    
    async def get_affinity(self, user_id: str, personality_name: str) -> Optional[Dict]:
        """Get affinity between user and personality"""
        return await super().get_affinity(user_id, personality_name)
    
    async def get_all_affinities(self, user_id: str) -> List[Dict]:
        """Get all affinities for a user"""
        return await super().get_all_affinities(user_id)
    
    async def search_facts(self, user_id: str, query: str, limit: Optional[int] = None) -> List[Dict]:
        """Search facts using semantic search"""
        return await super().search_facts(user_id, query, limit)
    
    async def search_episodes(self, user_id: str, query: str, limit: Optional[int] = None) -> List[Dict]:
        """Search episodes using semantic search"""
        return await super().search_episodes(user_id, query, limit)
    
    async def get_user_stats(self, user_id: str) -> Dict:
        """Get statistics for a user"""
        return await super().get_user_stats(user_id)
    
    async def cleanup_old_data(self, days_old: int = 365) -> int:
        """Clean up old data"""
        return await super().cleanup_old_data(days_old)
    
    async def health_check(self) -> Dict:
        """Check storage health"""
        return await super().health_check()
    
    def get_storage_info(self) -> Dict:
        """Get storage information"""
        return {
            'type': 'in_memory',
            'name': self.name,
            'description': self.description,
            'persistent': False,
            'thread_safe': False
        }
