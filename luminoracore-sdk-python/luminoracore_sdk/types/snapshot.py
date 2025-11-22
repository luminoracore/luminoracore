"""
Snapshot types for LuminoraCore SDK v1.1

Type definitions for personality snapshots.
"""

from typing import TypedDict, List, Dict, Any, Optional


class SnapshotMetadataDict(TypedDict):
    """Metadata for a personality snapshot"""
    created_at: str
    template_name: str
    template_version: str
    user_id: str
    session_id: str
    total_messages: int
    days_active: int


class SnapshotAffinityDict(TypedDict):
    """Affinity data in snapshot"""
    points: int
    level: str
    progression_history: List[Dict[str, Any]]


class SnapshotMoodDict(TypedDict):
    """Mood data in snapshot"""
    current: str
    intensity: float
    started_at: str
    history: List[Dict[str, Any]]


class SnapshotStateDict(TypedDict, total=False):
    """Current state in snapshot"""
    affinity: SnapshotAffinityDict
    mood: SnapshotMoodDict
    learned_facts: List[Dict[str, Any]]
    memorable_episodes: List[Dict[str, Any]]
    conversation_summary: Dict[str, Any]


class PersonalitySnapshotDict(TypedDict):
    """Complete personality snapshot"""
    _snapshot_info: SnapshotMetadataDict
    persona: Dict[str, Any]
    core_traits: Dict[str, Any]
    linguistic_profile: Dict[str, Any]
    behavioral_rules: Dict[str, Any]
    advanced_parameters: Dict[str, float]
    current_state: SnapshotStateDict
    active_configuration: Optional[Dict[str, Any]]


class SnapshotExportOptions(TypedDict, total=False):
    """Options for snapshot export"""
    include_conversation_history: bool
    include_facts: bool
    include_episodes: bool
    include_embeddings: bool
    anonymize_user_data: bool
    max_messages: Optional[int]

