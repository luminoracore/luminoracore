"""
Memory Classification System for LuminoraCore v1.1

Classifies facts and episodes into categories for better organization.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import logging

from .fact_extractor import Fact, FactCategory
from .episodic import Episode, EpisodeType

logger = logging.getLogger(__name__)


class ImportanceLevel(Enum):
    """Importance levels for classification"""
    CRITICAL = "critical"  # 9-10
    HIGH = "high"  # 7-8
    MEDIUM = "medium"  # 5-6
    LOW = "low"  # 3-4
    TRIVIAL = "trivial"  # 0-2


@dataclass
class ClassificationResult:
    """Result of memory classification"""
    item_id: str
    item_type: str  # "fact" or "episode"
    primary_category: str
    secondary_categories: List[str]
    importance_level: str
    tags: List[str]
    confidence: float = 1.0
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "item_id": self.item_id,
            "item_type": self.item_type,
            "primary_category": self.primary_category,
            "secondary_categories": self.secondary_categories,
            "importance_level": self.importance_level,
            "tags": self.tags,
            "confidence": self.confidence
        }


class MemoryClassifier:
    """
    Classifies facts and episodes
    
    Usage:
        classifier = MemoryClassifier()
        
        # Classify a fact
        result = classifier.classify_fact(fact)
        
        # Classify an episode
        result = classifier.classify_episode(episode)
    """
    
    def __init__(self):
        """Initialize classifier"""
        pass
    
    def classify_fact(self, fact: Fact) -> ClassificationResult:
        """
        Classify a fact
        
        Args:
            fact: Fact to classify
            
        Returns:
            ClassificationResult
        """
        # Primary category from fact
        primary_category = fact.category
        
        # Derive secondary categories from tags/value
        secondary_categories = self._derive_secondary_categories(
            fact.key,
            str(fact.value),
            fact.tags
        )
        
        # Importance based on category and confidence
        importance_level = self._classify_fact_importance(fact)
        
        return ClassificationResult(
            item_id=fact.source_message_id or "unknown",
            item_type="fact",
            primary_category=primary_category,
            secondary_categories=secondary_categories,
            importance_level=importance_level.value,
            tags=fact.tags,
            confidence=fact.confidence
        )
    
    def classify_episode(self, episode: Episode) -> ClassificationResult:
        """
        Classify an episode
        
        Args:
            episode: Episode to classify
            
        Returns:
            ClassificationResult
        """
        # Primary category from episode type
        primary_category = episode.episode_type
        
        # Secondary categories from tags/summary
        secondary_categories = self._derive_secondary_categories(
            episode.title,
            episode.summary,
            episode.tags
        )
        
        # Importance level from importance score
        importance_level = self._classify_episode_importance(episode)
        
        return ClassificationResult(
            item_id=episode.session_id or "unknown",
            item_type="episode",
            primary_category=primary_category,
            secondary_categories=secondary_categories,
            importance_level=importance_level.value,
            tags=episode.tags,
            confidence=1.0
        )
    
    def _derive_secondary_categories(
        self,
        title: str,
        content: str,
        tags: List[str]
    ) -> List[str]:
        """Derive secondary categories from content"""
        categories = set()
        
        # Add categories based on keywords
        keywords = {
            "work": ["work", "job", "career", "office", "business"],
            "family": ["family", "mom", "dad", "sibling", "parent"],
            "relationship": ["partner", "boyfriend", "girlfriend", "relationship"],
            "health": ["health", "doctor", "sick", "medicine"],
            "entertainment": ["anime", "movie", "game", "music", "show"]
        }
        
        content_lower = (title + " " + content).lower()
        
        for category, words in keywords.items():
            if any(word in content_lower for word in words):
                categories.add(category)
        
        return list(categories)
    
    def _classify_fact_importance(self, fact: Fact) -> ImportanceLevel:
        """Classify fact importance"""
        # High confidence facts are more important
        if fact.confidence >= 0.95:
            return ImportanceLevel.HIGH
        elif fact.confidence >= 0.8:
            return ImportanceLevel.MEDIUM
        else:
            return ImportanceLevel.LOW
    
    def _classify_episode_importance(self, episode: Episode) -> ImportanceLevel:
        """Classify episode importance"""
        current_importance = episode.get_current_importance()
        
        if current_importance >= 9.0:
            return ImportanceLevel.CRITICAL
        elif current_importance >= 7.0:
            return ImportanceLevel.HIGH
        elif current_importance >= 5.0:
            return ImportanceLevel.MEDIUM
        elif current_importance >= 3.0:
            return ImportanceLevel.LOW
        else:
            return ImportanceLevel.TRIVIAL
    
    def get_facts_by_category(
        self,
        facts: List[Fact],
        category: str
    ) -> List[Fact]:
        """Get all facts in a specific category"""
        return [f for f in facts if f.category == category]
    
    def get_episodes_by_importance(
        self,
        episodes: List[Episode],
        min_importance: float
    ) -> List[Episode]:
        """Get episodes above importance threshold"""
        return [
            e for e in episodes
            if e.get_current_importance() >= min_importance
        ]
    
    def get_top_n_episodes(
        self,
        episodes: List[Episode],
        n: int = 10
    ) -> List[Episode]:
        """Get top N most important episodes"""
        sorted_episodes = sorted(
            episodes,
            key=lambda e: e.get_current_importance(),
            reverse=True
        )
        return sorted_episodes[:n]

