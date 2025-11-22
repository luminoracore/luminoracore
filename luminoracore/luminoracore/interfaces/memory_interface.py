"""
Memory Interface
Abstract interface for memory system implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from datetime import datetime


class MemoryInterface(ABC):
    """Abstract interface for memory system implementations"""
    
    @abstractmethod
    async def extract_facts(self, conversation: List[Dict], user_id: str) -> List[Dict]:
        """Extract facts from conversation"""
        pass
    
    @abstractmethod
    async def extract_episodes(self, conversation: List[Dict], user_id: str) -> List[Dict]:
        """Extract episodes from conversation"""
        pass
    
    @abstractmethod
    async def get_relevant_memories(self, user_id: str, context: str, 
                                   memory_types: List[str] = None) -> List[Dict]:
        """Get relevant memories for context"""
        pass
    
    @abstractmethod
    async def update_affinity(self, user_id: str, personality_name: str, 
                             interaction_quality: str, points_delta: int) -> Dict:
        """Update affinity based on interaction"""
        pass
    
    @abstractmethod
    async def get_user_context(self, user_id: str) -> Dict:
        """Get comprehensive user context"""
        pass
    
    @abstractmethod
    async def search_memories(self, user_id: str, query: str, 
                             memory_types: List[str] = None) -> List[Dict]:
        """Search memories using semantic search"""
        pass
    
    @abstractmethod
    async def get_memory_stats(self, user_id: str) -> Dict:
        """Get memory statistics for user"""
        pass
    
    @abstractmethod
    async def cleanup_memories(self, user_id: str, days_old: int = 365) -> int:
        """Clean up old memories"""
        pass
