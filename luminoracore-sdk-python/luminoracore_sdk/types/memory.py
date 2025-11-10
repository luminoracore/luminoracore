"""
Memory types for LuminoraCore SDK v1.1

Type definitions for facts, episodes, and memory operations.
"""

from typing import TypedDict, List, Optional, Any
from datetime import datetime


class FactDict(TypedDict, total=False):
    """Type for fact dictionary"""
    id: str
    user_id: str
    session_id: Optional[str]
    category: str
    key: str
    value: Any
    confidence: float
    source_message_id: Optional[str]
    first_mentioned: str
    last_updated: str
    mention_count: int
    tags: List[str]
    context: Optional[str]
    is_active: bool


class EpisodeDict(TypedDict, total=False):
    """Type for episode dictionary"""
    id: str
    user_id: str
    session_id: Optional[str]
    episode_type: str
    title: str
    summary: str
    importance: float
    sentiment: str
    tags: List[str]
    context_messages: List[str]
    timestamp: str
    temporal_decay: float
    related_facts: List[str]
    related_episodes: List[str]
    metadata: Optional[dict]


class MemorySearchResult(TypedDict):
    """Type for memory search result"""
    id: str
    content: str
    similarity: float
    metadata: dict
    timestamp: str


class MemoryQueryOptions(TypedDict, total=False):
    """Options for memory queries"""
    category: Optional[str]
    min_importance: Optional[float]
    max_results: int
    include_inactive: bool
    sort_by: str
    order: str

