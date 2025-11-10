"""
Personality Interface
Abstract interface for personality system implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from datetime import datetime


class PersonalityInterface(ABC):
    """Abstract interface for personality system implementations"""
    
    @abstractmethod
    async def load_personality(self, name: str, data: Dict) -> bool:
        """Load a personality from data"""
        pass
    
    @abstractmethod
    async def get_personality(self, name: str) -> Optional[Dict]:
        """Get personality by name"""
        pass
    
    @abstractmethod
    async def list_personalities(self) -> List[str]:
        """List all available personalities"""
        pass
    
    @abstractmethod
    async def blend_personalities(self, personalities: List[str], weights: List[float]) -> Dict:
        """Blend multiple personalities"""
        pass
    
    @abstractmethod
    async def evolve_personality(self, personality_name: str, user_id: str, 
                                interaction_data: Dict) -> Dict:
        """Evolve personality based on interaction"""
        pass
    
    @abstractmethod
    async def get_personality_traits(self, name: str) -> Dict:
        """Get personality traits"""
        pass
    
    @abstractmethod
    async def update_personality_trait(self, name: str, trait: str, value: Any) -> bool:
        """Update a personality trait"""
        pass
    
    @abstractmethod
    async def get_personality_history(self, name: str, user_id: str) -> List[Dict]:
        """Get personality evolution history"""
        pass
    
    @abstractmethod
    async def reset_personality(self, name: str) -> bool:
        """Reset personality to original state"""
        pass
    
    @abstractmethod
    async def export_personality(self, name: str) -> Dict:
        """Export personality data"""
        pass
    
    @abstractmethod
    async def import_personality(self, data: Dict) -> bool:
        """Import personality data"""
        pass
