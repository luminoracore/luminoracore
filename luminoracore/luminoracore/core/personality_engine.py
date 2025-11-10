"""
Personality Engine
Core personality management and evolution system
"""

import json
import asyncio
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from ..interfaces import PersonalityInterface, EvolutionInterface


class PersonalityEngine(PersonalityInterface):
    """Core personality engine for managing and evolving personalities"""
    
    def __init__(self):
        self.personalities: Dict[str, Dict] = {}
        self.evolution_engine: Optional[EvolutionInterface] = None
        self.personality_history: Dict[str, List[Dict]] = {}
    
    async def load_personality(self, name: str, data: Dict) -> bool:
        """Load a personality from data"""
        try:
            # Validate personality data
            if not self._validate_personality_data(data):
                return False
            
            # Store personality
            self.personalities[name] = {
                'data': data,
                'created_at': datetime.now().isoformat(),
                'last_modified': datetime.now().isoformat()
            }
            
            # Initialize history
            if name not in self.personality_history:
                self.personality_history[name] = []
            
            return True
        except Exception as e:
            print(f"Error loading personality {name}: {e}")
            return False
    
    async def get_personality(self, name: str) -> Optional[Dict]:
        """Get personality by name"""
        return self.personalities.get(name, {}).get('data')
    
    async def list_personalities(self) -> List[str]:
        """List all available personalities"""
        return list(self.personalities.keys())
    
    async def blend_personalities(self, personalities: List[str], weights: List[float]) -> Dict:
        """Blend multiple personalities"""
        if len(personalities) != len(weights):
            raise ValueError("Number of personalities must match number of weights")
        
        if not personalities:
            raise ValueError("At least one personality required")
        
        # Get personality data
        personality_data = []
        for name in personalities:
            data = await self.get_personality(name)
            if not data:
                raise ValueError(f"Personality {name} not found")
            personality_data.append(data)
        
        # Blend personalities
        blended = self._blend_personality_data(personality_data, weights)
        
        return {
            'name': f"blended_{'_'.join(personalities)}",
            'data': blended,
            'source_personalities': personalities,
            'weights': weights,
            'created_at': datetime.now().isoformat()
        }
    
    async def evolve_personality(self, personality_name: str, user_id: str, 
                                interaction_data: Dict) -> Dict:
        """Evolve personality based on interaction"""
        if not self.evolution_engine:
            raise RuntimeError("Evolution engine not initialized")
        
        # Get current personality
        personality = await self.get_personality(personality_name)
        if not personality:
            raise ValueError(f"Personality {personality_name} not found")
        
        # Calculate evolution
        evolution_delta = await self.evolution_engine.calculate_evolution_delta(
            personality_name, user_id, interaction_data
        )
        
        # Apply evolution
        evolved_personality = self._apply_evolution_delta(personality, evolution_delta)
        
        # Update personality
        self.personalities[personality_name]['data'] = evolved_personality
        self.personalities[personality_name]['last_modified'] = datetime.now().isoformat()
        
        # Record evolution
        evolution_record = {
            'user_id': user_id,
            'interaction_data': interaction_data,
            'evolution_delta': evolution_delta,
            'timestamp': datetime.now().isoformat()
        }
        
        if personality_name not in self.personality_history:
            self.personality_history[personality_name] = []
        self.personality_history[personality_name].append(evolution_record)
        
        return evolved_personality
    
    async def get_personality_traits(self, name: str) -> Dict:
        """Get personality traits"""
        personality = await self.get_personality(name)
        if not personality:
            return {}
        
        return personality.get('traits', {})
    
    async def update_personality_trait(self, name: str, trait: str, value: Any) -> bool:
        """Update a personality trait"""
        personality = await self.get_personality(name)
        if not personality:
            return False
        
        if 'traits' not in personality:
            personality['traits'] = {}
        
        personality['traits'][trait] = value
        self.personalities[name]['data'] = personality
        self.personalities[name]['last_modified'] = datetime.now().isoformat()
        
        return True
    
    async def get_personality_history(self, name: str, user_id: str) -> List[Dict]:
        """Get personality evolution history"""
        if name not in self.personality_history:
            return []
        
        return [
            record for record in self.personality_history[name]
            if record.get('user_id') == user_id
        ]
    
    async def reset_personality(self, name: str) -> bool:
        """Reset personality to original state"""
        if name not in self.personalities:
            return False
        
        # Clear history
        self.personality_history[name] = []
        
        # Reset to original data (would need to store original)
        # For now, just clear history
        return True
    
    async def export_personality(self, name: str) -> Dict:
        """Export personality data"""
        personality = await self.get_personality(name)
        if not personality:
            return {}
        
        return {
            'name': name,
            'data': personality,
            'created_at': self.personalities[name].get('created_at'),
            'last_modified': self.personalities[name].get('last_modified'),
            'history_count': len(self.personality_history.get(name, []))
        }
    
    async def import_personality(self, data: Dict) -> bool:
        """Import personality data"""
        name = data.get('name')
        personality_data = data.get('data', {})
        
        if not name or not personality_data:
            return False
        
        return await self.load_personality(name, personality_data)
    
    def _validate_personality_data(self, data: Dict) -> bool:
        """Validate personality data structure"""
        required_fields = ['name', 'description']
        return all(field in data for field in required_fields)
    
    def _blend_personality_data(self, personality_data: List[Dict], weights: List[float]) -> Dict:
        """Blend personality data using weights"""
        if not personality_data:
            return {}
        
        # Normalize weights
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]
        
        # Start with first personality
        blended = personality_data[0].copy()
        
        # Blend traits
        if 'traits' in blended:
            for i, personality in enumerate(personality_data[1:], 1):
                if 'traits' in personality:
                    for trait, value in personality['traits'].items():
                        if trait in blended['traits']:
                            # Blend numeric traits
                            if isinstance(value, (int, float)) and isinstance(blended['traits'][trait], (int, float)):
                                blended['traits'][trait] = (
                                    blended['traits'][trait] * (1 - normalized_weights[i]) +
                                    value * normalized_weights[i]
                                )
                            else:
                                # For non-numeric traits, use weighted selection
                                if normalized_weights[i] > 0.5:
                                    blended['traits'][trait] = value
                        else:
                            blended['traits'][trait] = value
        
        return blended
    
    def _apply_evolution_delta(self, personality: Dict, delta: Dict) -> Dict:
        """Apply evolution delta to personality"""
        evolved = personality.copy()
        
        if 'traits' in delta and 'traits' in evolved:
            for trait, change in delta['traits'].items():
                if trait in evolved['traits']:
                    if isinstance(evolved['traits'][trait], (int, float)) and isinstance(change, (int, float)):
                        evolved['traits'][trait] += change
                        # Clamp values to reasonable ranges
                        if isinstance(evolved['traits'][trait], float):
                            evolved['traits'][trait] = max(0.0, min(1.0, evolved['traits'][trait]))
        
        return evolved
