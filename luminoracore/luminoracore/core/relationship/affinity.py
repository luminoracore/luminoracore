"""
Affinity Management System for LuminoraCore v1.1

Manages relationship affinity points and level progression.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class AffinityState:
    """Current affinity state for a user-personality pair"""
    user_id: str
    personality_name: str
    affinity_points: int = 0
    current_level: str = "stranger"
    total_messages: int = 0
    positive_interactions: int = 0
    negative_interactions: int = 0
    last_interaction: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate affinity points"""
        if not (0 <= self.affinity_points <= 100):
            raise ValueError(f"Affinity points must be 0-100, got {self.affinity_points}")


class AffinityManager:
    """
    Manages affinity point tracking and level progression
    
    Usage:
        manager = AffinityManager(db_connection)
        
        # Update affinity
        new_state = await manager.update_affinity(
            user_id="user123",
            personality_name="alicia",
            points_delta=2,
            interaction_type="positive"
        )
        
        # Get current affinity
        state = await manager.get_affinity(user_id, personality_name)
    """
    
    def __init__(self, storage_provider=None):
        """
        Initialize affinity manager
        
        Args:
            storage_provider: Storage provider for persistence (from SDK)
        """
        self.storage = storage_provider
    
    def calculate_points_delta(
        self,
        interaction_type: str,
        message_length: Optional[int] = None,
        sentiment: Optional[str] = None
    ) -> int:
        """
        Calculate affinity points delta based on interaction
        
        Args:
            interaction_type: Type of interaction (positive, negative, neutral)
            message_length: Length of user message (optional)
            sentiment: Detected sentiment (optional)
            
        Returns:
            Points to add/subtract (-10 to +10)
        """
        base_points = {
            "very_positive": 5,
            "positive": 2,
            "neutral": 1,
            "negative": -2,
            "very_negative": -5
        }
        
        # Start with base points
        delta = base_points.get(interaction_type, 1)
        
        # Bonus for longer messages (shows engagement)
        if message_length and message_length > 100:
            delta += 1
        
        # Clamp to [-10, 10]
        return max(-10, min(10, delta))
    
    def determine_level(
        self,
        affinity_points: int,
        level_definitions: Optional[List[dict]] = None
    ) -> str:
        """
        Determine relationship level based on affinity points
        
        Args:
            affinity_points: Current affinity points (0-100)
            level_definitions: Optional custom level definitions from JSON
            
        Returns:
            Level name (e.g., "stranger", "friend")
        """
        # Default levels if not provided by personality JSON
        default_levels = [
            {"name": "stranger", "min": 0, "max": 20},
            {"name": "acquaintance", "min": 21, "max": 40},
            {"name": "friend", "min": 41, "max": 60},
            {"name": "close_friend", "min": 61, "max": 80},
            {"name": "soulmate", "min": 81, "max": 100}
        ]
        
        levels = level_definitions or default_levels
        
        for level in levels:
            if level["min"] <= affinity_points <= level["max"]:
                return level["name"]
        
        # Fallback
        return "stranger"
    
    def update_affinity_state(
        self,
        state: AffinityState,
        points_delta: int,
        level_definitions: Optional[List[dict]] = None
    ) -> AffinityState:
        """
        Update affinity state with new points
        
        Args:
            state: Current affinity state
            points_delta: Points to add/subtract
            level_definitions: Optional level definitions from personality JSON
            
        Returns:
            Updated affinity state
        """
        # Update points (clamped to 0-100)
        new_points = state.affinity_points + points_delta
        new_points = max(0, min(100, new_points))
        
        # Determine new level
        new_level = self.determine_level(new_points, level_definitions)
        
        # Check if level changed
        level_changed = new_level != state.current_level
        if level_changed:
            logger.info(f"Level progression: {state.current_level} → {new_level} (affinity: {new_points})")
        
        # Update state
        state.affinity_points = new_points
        state.current_level = new_level
        state.total_messages += 1
        state.last_interaction = datetime.now()
        
        if points_delta > 0:
            state.positive_interactions += 1
        elif points_delta < 0:
            state.negative_interactions += 1
        
        return state
    
    def get_level_progress(self, state: AffinityState, level_definitions: Optional[List[dict]] = None) -> dict:
        """
        Get progress within current level
        
        Args:
            state: Current affinity state
            level_definitions: Optional level definitions
            
        Returns:
            Dict with progress information
        """
        levels = level_definitions or [
            {"name": "stranger", "min": 0, "max": 20},
            {"name": "acquaintance", "min": 21, "max": 40},
            {"name": "friend", "min": 41, "max": 60},
            {"name": "close_friend", "min": 61, "max": 80},
            {"name": "soulmate", "min": 81, "max": 100}
        ]
        
        # Find current level
        current_level_def = None
        next_level_def = None
        
        for i, level in enumerate(levels):
            if level["name"] == state.current_level:
                current_level_def = level
                if i + 1 < len(levels):
                    next_level_def = levels[i + 1]
                break
        
        if not current_level_def:
            return {
                "current_level": state.current_level,
                "points": state.affinity_points,
                "progress_in_level": 0.0,
                "next_level": None
            }
        
        # Calculate progress within level
        level_range = current_level_def["max"] - current_level_def["min"]
        points_in_level = state.affinity_points - current_level_def["min"]
        progress = points_in_level / level_range if level_range > 0 else 1.0
        
        return {
            "current_level": state.current_level,
            "points": state.affinity_points,
            "progress_in_level": progress,
            "points_to_next_level": (next_level_def["min"] - state.affinity_points) if next_level_def else 0,
            "next_level": next_level_def["name"] if next_level_def else None
        }

