"""
Evolution Engine
Core personality evolution and adaptation system
"""

import asyncio
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from ..interfaces import EvolutionInterface


class EvolutionEngine(EvolutionInterface):
    """Core evolution engine for personality adaptation"""
    
    def __init__(self):
        self.evolution_history: Dict[str, List[Dict]] = {}
        self.evolution_stats: Dict[str, Dict] = {}
    
    async def evolve_personality(self, personality_name: str, user_id: str, 
                                interaction_data: Dict) -> Dict:
        """Evolve personality based on interaction"""
        # Calculate evolution delta
        delta = await self.calculate_evolution_delta(personality_name, user_id, interaction_data)
        
        # Apply evolution
        result = await self.apply_evolution(personality_name, delta)
        
        # Record evolution
        await self._record_evolution(personality_name, user_id, interaction_data, delta)
        
        return result
    
    async def calculate_evolution_delta(self, personality_name: str, user_id: str, 
                                       interaction_data: Dict) -> Dict:
        """Calculate how personality should evolve"""
        delta = {
            'traits': {},
            'behaviors': {},
            'preferences': {}
        }
        
        # Analyze interaction quality
        interaction_quality = interaction_data.get('quality', 'neutral')
        sentiment = interaction_data.get('sentiment', 'neutral')
        duration = interaction_data.get('duration', 0)
        
        # Calculate trait changes based on interaction
        if interaction_quality == 'positive':
            # Positive interactions increase positive traits
            delta['traits']['friendliness'] = 0.1
            delta['traits']['empathy'] = 0.05
            delta['traits']['patience'] = 0.05
        elif interaction_quality == 'negative':
            # Negative interactions might decrease some traits
            delta['traits']['friendliness'] = -0.05
            delta['traits']['patience'] = -0.1
        
        # Sentiment-based changes
        if sentiment == 'happy':
            delta['traits']['cheerfulness'] = 0.1
        elif sentiment == 'sad':
            delta['traits']['empathy'] = 0.1
        elif sentiment == 'angry':
            delta['traits']['patience'] = -0.1
        
        # Duration-based changes
        if duration > 300:  # Long interaction
            delta['traits']['engagement'] = 0.1
            delta['traits']['curiosity'] = 0.05
        
        # User-specific adaptations
        user_affinity = interaction_data.get('user_affinity', 0.5)
        if user_affinity > 0.7:
            # High affinity users get more personalized responses
            delta['behaviors']['personalization'] = 0.1
            delta['preferences']['user_focus'] = 0.05
        
        return delta
    
    async def apply_evolution(self, personality_name: str, evolution_delta: Dict) -> bool:
        """Apply evolution changes to personality"""
        # This would typically update the personality in storage
        # For now, we'll just record the evolution
        
        if personality_name not in self.evolution_stats:
            self.evolution_stats[personality_name] = {
                'total_evolutions': 0,
                'trait_changes': {},
                'last_evolution': None
            }
        
        # Update stats
        self.evolution_stats[personality_name]['total_evolutions'] += 1
        self.evolution_stats[personality_name]['last_evolution'] = datetime.now().isoformat()
        
        # Track trait changes
        for trait, change in evolution_delta.get('traits', {}).items():
            if trait not in self.evolution_stats[personality_name]['trait_changes']:
                self.evolution_stats[personality_name]['trait_changes'][trait] = 0
            self.evolution_stats[personality_name]['trait_changes'][trait] += change
        
        return True
    
    async def get_evolution_history(self, personality_name: str, user_id: str) -> List[Dict]:
        """Get evolution history for personality and user"""
        key = f"{personality_name}_{user_id}"
        return self.evolution_history.get(key, [])
    
    async def reset_evolution(self, personality_name: str, user_id: str) -> bool:
        """Reset evolution for specific user"""
        key = f"{personality_name}_{user_id}"
        if key in self.evolution_history:
            del self.evolution_history[key]
        return True
    
    async def get_evolution_stats(self, personality_name: str) -> Dict:
        """Get evolution statistics"""
        return self.evolution_stats.get(personality_name, {
            'total_evolutions': 0,
            'trait_changes': {},
            'last_evolution': None
        })
    
    async def predict_evolution(self, personality_name: str, user_id: str, 
                               future_interactions: List[Dict]) -> Dict:
        """Predict how personality will evolve"""
        prediction = {
            'predicted_traits': {},
            'confidence': 0.0,
            'recommendations': []
        }
        
        # Simple prediction based on interaction patterns
        positive_interactions = sum(1 for i in future_interactions if i.get('quality') == 'positive')
        negative_interactions = sum(1 for i in future_interactions if i.get('quality') == 'negative')
        
        total_interactions = len(future_interactions)
        if total_interactions > 0:
            positive_ratio = positive_interactions / total_interactions
            
            # Predict trait changes
            if positive_ratio > 0.7:
                prediction['predicted_traits']['friendliness'] = 0.2
                prediction['predicted_traits']['empathy'] = 0.1
                prediction['confidence'] = 0.8
                prediction['recommendations'].append("Continue positive interactions")
            elif positive_ratio < 0.3:
                prediction['predicted_traits']['friendliness'] = -0.1
                prediction['predicted_traits']['patience'] = -0.1
                prediction['confidence'] = 0.6
                prediction['recommendations'].append("Consider improving interaction quality")
        
        return prediction
    
    async def optimize_evolution(self, personality_name: str, user_id: str, 
                                target_traits: Dict) -> Dict:
        """Optimize evolution towards target traits"""
        current_stats = await self.get_evolution_stats(personality_name)
        current_traits = current_stats.get('trait_changes', {})
        
        optimization_plan = {
            'target_traits': target_traits,
            'current_traits': current_traits,
            'optimization_delta': {},
            'steps': []
        }
        
        # Calculate optimization delta
        for trait, target_value in target_traits.items():
            current_value = current_traits.get(trait, 0.0)
            delta = target_value - current_value
            
            if abs(delta) > 0.01:  # Only optimize if significant difference
                optimization_plan['optimization_delta'][trait] = delta
                
                if delta > 0:
                    optimization_plan['steps'].append(f"Increase {trait} through positive interactions")
                else:
                    optimization_plan['steps'].append(f"Decrease {trait} through specific behaviors")
        
        return optimization_plan
    
    async def _record_evolution(self, personality_name: str, user_id: str, 
                               interaction_data: Dict, delta: Dict):
        """Record evolution in history"""
        key = f"{personality_name}_{user_id}"
        
        if key not in self.evolution_history:
            self.evolution_history[key] = []
        
        evolution_record = {
            'timestamp': datetime.now().isoformat(),
            'interaction_data': interaction_data,
            'evolution_delta': delta,
            'personality_name': personality_name,
            'user_id': user_id
        }
        
        self.evolution_history[key].append(evolution_record)
        
        # Keep only last 100 evolutions per user
        if len(self.evolution_history[key]) > 100:
            self.evolution_history[key] = self.evolution_history[key][-100:]
