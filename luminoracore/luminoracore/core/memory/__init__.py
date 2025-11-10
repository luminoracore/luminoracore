"""
Memory module for LuminoraCore v1.1

Manages episodic memory, fact extraction, and semantic search.
"""

from .fact_extractor import Fact, FactCategory, FactExtractor
from .episodic import Episode, EpisodeType, Sentiment, EpisodicMemoryManager
from .classifier import ImportanceLevel, ClassificationResult, MemoryClassifier

__all__ = [
    'Fact',
    'FactCategory',
    'FactExtractor',
    'Episode',
    'EpisodeType',
    'Sentiment',
    'EpisodicMemoryManager',
    'ImportanceLevel',
    'ClassificationResult',
    'MemoryClassifier'
]

