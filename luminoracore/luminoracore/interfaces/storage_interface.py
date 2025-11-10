"""
Storage Interface
Abstract interface for all storage implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from datetime import datetime


class StorageInterface(ABC):
    """Abstract interface for storage implementations"""
    
    @abstractmethod
    async def save_fact(self, user_id: str, category: str, key: str, value: Any, confidence: float = 0.8) -> bool:
        """Save a fact for a user"""
        pass
    
    @abstractmethod
    async def get_facts(self, user_id: str, category: Optional[str] = None) -> List[Dict]:
        """Get facts for a user, optionally filtered by category"""
        pass
    
    @abstractmethod
    async def update_fact(self, user_id: str, category: str, key: str, value: Any, confidence: float = 0.8) -> bool:
        """Update an existing fact"""
        pass
    
    @abstractmethod
    async def delete_fact(self, user_id: str, category: str, key: str) -> bool:
        """Delete a fact"""
        pass
    
    @abstractmethod
    async def save_episode(self, user_id: str, episode_type: str, title: str, summary: str, 
                          importance: float = 0.5, sentiment: str = "neutral", 
                          metadata: Optional[Dict] = None) -> bool:
        """Save an episode for a user"""
        pass
    
    @abstractmethod
    async def get_episodes(self, user_id: str, min_importance: Optional[float] = None, 
                          limit: Optional[int] = None) -> List[Dict]:
        """Get episodes for a user, optionally filtered by importance"""
        pass
    
    @abstractmethod
    async def update_episode(self, user_id: str, episode_id: str, **kwargs) -> bool:
        """Update an existing episode"""
        pass
    
    @abstractmethod
    async def delete_episode(self, user_id: str, episode_id: str) -> bool:
        """Delete an episode"""
        pass
    
    @abstractmethod
    async def update_affinity(self, user_id: str, personality_name: str, points_delta: int, 
                             interaction_type: str = "neutral") -> Dict:
        """Update affinity between user and personality"""
        pass
    
    @abstractmethod
    async def get_affinity(self, user_id: str, personality_name: str) -> Optional[Dict]:
        """Get affinity between user and personality"""
        pass
    
    @abstractmethod
    async def get_all_affinities(self, user_id: str) -> List[Dict]:
        """Get all affinities for a user"""
        pass
    
    @abstractmethod
    async def search_facts(self, user_id: str, query: str, limit: Optional[int] = None) -> List[Dict]:
        """Search facts using semantic search"""
        pass
    
    @abstractmethod
    async def search_episodes(self, user_id: str, query: str, limit: Optional[int] = None) -> List[Dict]:
        """Search episodes using semantic search"""
        pass
    
    @abstractmethod
    async def get_user_stats(self, user_id: str) -> Dict:
        """Get statistics for a user"""
        pass
    
    @abstractmethod
    async def cleanup_old_data(self, days_old: int = 365) -> int:
        """Clean up old data"""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict:
        """Check storage health"""
        pass
