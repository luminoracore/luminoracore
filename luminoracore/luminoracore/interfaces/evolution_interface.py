"""
Evolution Interface
Abstract interface for personality evolution implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from datetime import datetime


class EvolutionInterface(ABC):
    """Abstract interface for personality evolution implementations"""
    
    @abstractmethod
    async def evolve_personality(self, personality_name: str, user_id: str, 
                                interaction_data: Dict) -> Dict:
        """Evolve personality based on interaction"""
        pass
    
    @abstractmethod
    async def calculate_evolution_delta(self, personality_name: str, user_id: str, 
                                      interaction_data: Dict) -> Dict:
        """Calculate how personality should evolve"""
        pass
    
    @abstractmethod
    async def apply_evolution(self, personality_name: str, evolution_delta: Dict) -> bool:
        """Apply evolution changes to personality"""
        pass
    
    @abstractmethod
    async def get_evolution_history(self, personality_name: str, user_id: str) -> List[Dict]:
        """Get evolution history for personality and user"""
        pass
    
    @abstractmethod
    async def reset_evolution(self, personality_name: str, user_id: str) -> bool:
        """Reset evolution for specific user"""
        pass
    
    @abstractmethod
    async def get_evolution_stats(self, personality_name: str) -> Dict:
        """Get evolution statistics"""
        pass
    
    @abstractmethod
    async def predict_evolution(self, personality_name: str, user_id: str, 
                               future_interactions: List[Dict]) -> Dict:
        """Predict how personality will evolve"""
        pass
    
    @abstractmethod
    async def optimize_evolution(self, personality_name: str, user_id: str, 
                                target_traits: Dict) -> Dict:
        """Optimize evolution towards target traits"""
        pass
