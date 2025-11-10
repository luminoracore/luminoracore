"""
Relationship types for LuminoraCore SDK v1.1

Type definitions for affinity and relationship data.
"""

from typing import TypedDict, Optional, List


class AffinityDict(TypedDict, total=False):
    """Type for affinity dictionary"""
    id: str
    user_id: str
    personality_name: str
    affinity_points: int
    current_level: str
    total_messages: int
    positive_interactions: int
    negative_interactions: int
    last_interaction: str
    created_at: str
    updated_at: str


class AffinityProgressDict(TypedDict):
    """Type for affinity progress information"""
    current_level: str
    points: int
    progress_in_level: float
    points_to_next_level: int
    next_level: Optional[str]


class LevelChangeDict(TypedDict):
    """Type for level change event"""
    user_id: str
    personality_name: str
    old_level: str
    new_level: str
    affinity_points: int
    timestamp: str

