"""
Relationship module for LuminoraCore v1.1

Manages relationship affinity and progression.
"""

from .affinity import AffinityState, AffinityManager
from .events import InteractionType, RelationshipEvent, LevelChangeEvent

__all__ = [
    'AffinityState',
    'AffinityManager',
    'InteractionType',
    'RelationshipEvent',
    'LevelChangeEvent'
]

