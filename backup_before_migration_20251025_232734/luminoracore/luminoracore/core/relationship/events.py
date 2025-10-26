"""
Relationship Events for LuminoraCore v1.1

Defines events that can affect relationship affinity.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime


class InteractionType(Enum):
    """Types of interactions that affect affinity"""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"


@dataclass
class RelationshipEvent:
    """Event that affects relationship affinity"""
    user_id: str
    personality_name: str
    interaction_type: InteractionType
    points_delta: int
    reason: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        """Set timestamp if not provided"""
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "user_id": self.user_id,
            "personality_name": self.personality_name,
            "interaction_type": self.interaction_type.value,
            "points_delta": self.points_delta,
            "reason": self.reason,
            "timestamp": self.timestamp.isoformat()
        }


class LevelChangeEvent:
    """Event triggered when relationship level changes"""
    
    def __init__(
        self,
        user_id: str,
        personality_name: str,
        old_level: str,
        new_level: str,
        affinity_points: int,
        timestamp: Optional[datetime] = None
    ):
        self.user_id = user_id
        self.personality_name = personality_name
        self.old_level = old_level
        self.new_level = new_level
        self.affinity_points = affinity_points
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "user_id": self.user_id,
            "personality_name": self.personality_name,
            "old_level": self.old_level,
            "new_level": self.new_level,
            "affinity_points": self.affinity_points,
            "timestamp": self.timestamp.isoformat()
        }

