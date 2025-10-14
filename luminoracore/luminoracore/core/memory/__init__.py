"""
Memory module for LuminoraCore v1.1

Manages episodic memory, fact extraction, and semantic search.
"""

from .fact_extractor import Fact, FactCategory, FactExtractor
from .episodic import Episode, EpisodeType, Sentiment, EpisodicMemoryManager

__all__ = [
    'Fact',
    'FactCategory',
    'FactExtractor',
    'Episode',
    'EpisodeType',
    'Sentiment',
    'EpisodicMemoryManager'
]

