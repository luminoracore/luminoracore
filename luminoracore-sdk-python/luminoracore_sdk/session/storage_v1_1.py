"""
Storage v1.1 Extensions for LuminoraCore SDK

Adds v1.1 table support to existing storage backends.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class StorageV11Extension(ABC):
    """
    Abstract extension for v1.1 storage methods
    
    Storage implementations can inherit from both SessionStorage and this
    to provide v1.1 functionality.
    """
    
    # AFFINITY METHODS
    @abstractmethod
    async def save_affinity(
        self,
        user_id: str,
        personality_name: str,
        affinity_points: int,
        current_level: str,
        **kwargs
    ) -> bool:
        """Save or update user affinity"""
        pass
    
    @abstractmethod
    async def get_affinity(
        self,
        user_id: str,
        personality_name: str
    ) -> Optional[Dict[str, Any]]:
        """Get user affinity data"""
        pass
    
    # FACT METHODS
    @abstractmethod
    async def save_fact(
        self,
        user_id: str,
        category: str,
        key: str,
        value: Any,
        **kwargs
    ) -> bool:
        """Save a user fact"""
        pass
    
    @abstractmethod
    async def get_facts(
        self,
        user_id: str,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get user facts, optionally filtered by category"""
        pass
    
    # EPISODE METHODS
    @abstractmethod
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
        pass
    
    @abstractmethod
    async def get_episodes(
        self,
        user_id: str,
        min_importance: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Get episodes, optionally filtered by importance"""
        pass
    
    # MOOD METHODS
    @abstractmethod
    async def save_mood(
        self,
        session_id: str,
        user_id: str,
        current_mood: str,
        mood_intensity: float = 1.0
    ) -> bool:
        """Save current mood state"""
        pass
    
    @abstractmethod
    async def get_mood(
        self,
        session_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get current mood state"""
        pass


class InMemoryStorageV11(StorageV11Extension):
    """In-memory implementation of v1.1 storage"""
    
    def __init__(self):
        """Initialize in-memory v1.1 storage"""
        self._affinity: Dict[str, Dict[str, Any]] = {}
        self._facts: Dict[str, List[Dict[str, Any]]] = {}
        self._episodes: Dict[str, List[Dict[str, Any]]] = {}
        self._moods: Dict[str, Dict[str, Any]] = {}
    
    async def save_affinity(
        self,
        user_id: str,
        personality_name: str,
        affinity_points: int,
        current_level: str,
        **kwargs
    ) -> bool:
        """Save affinity in memory"""
        key = f"{user_id}:{personality_name}"
        self._affinity[key] = {
            "user_id": user_id,
            "personality_name": personality_name,
            "affinity_points": affinity_points,
            "current_level": current_level,
            "updated_at": datetime.now().isoformat(),
            **kwargs
        }
        return True
    
    async def get_affinity(
        self,
        user_id: str,
        personality_name: str
    ) -> Optional[Dict[str, Any]]:
        """Get affinity from memory"""
        key = f"{user_id}:{personality_name}"
        return self._affinity.get(key)
    
    async def save_fact(
        self,
        user_id: str,
        category: str,
        key: str,
        value: Any,
        **kwargs
    ) -> bool:
        """Save fact in memory"""
        if user_id not in self._facts:
            self._facts[user_id] = []
        
        # Update if exists, otherwise append
        fact_dict = {
            "user_id": user_id,
            "category": category,
            "key": key,
            "value": value,
            "updated_at": datetime.now().isoformat(),
            **kwargs
        }
        
        # Replace existing fact with same key
        self._facts[user_id] = [
            f for f in self._facts[user_id]
            if not (f["category"] == category and f["key"] == key)
        ]
        self._facts[user_id].append(fact_dict)
        
        return True
    
    async def get_facts(
        self,
        user_id: str,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get facts from memory"""
        facts = self._facts.get(user_id, [])
        
        if category:
            return [f for f in facts if f["category"] == category]
        
        return facts
    
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
        """Save episode in memory"""
        if user_id not in self._episodes:
            self._episodes[user_id] = []
        
        episode_dict = {
            "user_id": user_id,
            "episode_type": episode_type,
            "title": title,
            "summary": summary,
            "importance": importance,
            "sentiment": sentiment,
            "timestamp": kwargs.get("timestamp", datetime.now().isoformat()),
            **kwargs
        }
        
        self._episodes[user_id].append(episode_dict)
        return True
    
    async def get_episodes(
        self,
        user_id: str,
        min_importance: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Get episodes from memory"""
        episodes = self._episodes.get(user_id, [])
        
        if min_importance is not None:
            return [e for e in episodes if e["importance"] >= min_importance]
        
        return episodes
    
    async def save_mood(
        self,
        session_id: str,
        user_id: str,
        current_mood: str,
        mood_intensity: float = 1.0
    ) -> bool:
        """Save mood in memory"""
        self._moods[session_id] = {
            "session_id": session_id,
            "user_id": user_id,
            "current_mood": current_mood,
            "mood_intensity": mood_intensity,
            "updated_at": datetime.now().isoformat()
        }
        return True
    
    async def get_mood(
        self,
        session_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get mood from memory"""
        return self._moods.get(session_id)

