"""
Episodic Memory System for LuminoraCore v1.1

Detects and stores memorable moments in conversations.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum
import logging
import math

logger = logging.getLogger(__name__)


class EpisodeType(Enum):
    """Types of memorable episodes"""
    EMOTIONAL_MOMENT = "emotional_moment"
    MILESTONE = "milestone"
    CONFESSION = "confession"
    CONFLICT = "conflict"
    ACHIEVEMENT = "achievement"
    BONDING = "bonding"
    ROUTINE = "routine"


class Sentiment(Enum):
    """Sentiment values"""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"


@dataclass
class Episode:
    """Represents a memorable episode in conversation"""
    user_id: str
    episode_type: str
    title: str
    summary: str
    importance: float
    sentiment: str
    timestamp: datetime
    session_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    context_messages: List[str] = field(default_factory=list)
    temporal_decay: float = 1.0
    related_facts: List[str] = field(default_factory=list)
    related_episodes: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate importance"""
        if not (0.0 <= self.importance <= 10.0):
            raise ValueError(f"Importance must be 0-10, got {self.importance}")
        if not (0.0 <= self.temporal_decay <= 1.0):
            raise ValueError(f"Temporal decay must be 0-1, got {self.temporal_decay}")
    
    def get_current_importance(self) -> float:
        """Get importance considering temporal decay"""
        return self.importance * self.temporal_decay
    
    def update_decay(self, days_passed: int) -> None:
        """
        Update temporal decay based on time
        
        Args:
            days_passed: Days since episode occurred
        """
        # Logarithmic decay: recent events decay slowly
        decay_rate = 0.1
        self.temporal_decay = 1.0 / (1.0 + decay_rate * math.log(days_passed + 1))
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "episode_type": self.episode_type,
            "title": self.title,
            "summary": self.summary,
            "importance": self.importance,
            "sentiment": self.sentiment,
            "timestamp": self.timestamp.isoformat(),
            "tags": self.tags,
            "context_messages": self.context_messages,
            "temporal_decay": self.temporal_decay,
            "related_facts": self.related_facts,
            "related_episodes": self.related_episodes
        }


class EpisodicMemoryManager:
    """
    Manages episodic memory detection and storage
    
    Usage:
        manager = EpisodicMemoryManager(llm_provider=provider)
        
        # Detect if messages form an episode
        episode = await manager.detect_episode(
            user_id="user123",
            messages=[msg1, msg2, msg3]
        )
    """
    
    def __init__(self, llm_provider=None, importance_threshold: float = 5.0):
        """
        Initialize episodic memory manager
        
        Args:
            llm_provider: LLM provider from SDK (optional)
            importance_threshold: Minimum importance to store episode
        """
        self.llm_provider = llm_provider
        self.importance_threshold = importance_threshold
    
    def calculate_importance(
        self,
        episode_type: str,
        sentiment: str,
        message_count: int = 1
    ) -> float:
        """
        Calculate episode importance (0-10)
        
        Args:
            episode_type: Type of episode
            sentiment: Sentiment of episode
            message_count: Number of messages in episode
            
        Returns:
            Importance score (0-10)
        """
        # Base importance by type
        base_importance = {
            "emotional_moment": 8.0,
            "milestone": 7.0,
            "confession": 7.5,
            "conflict": 6.0,
            "achievement": 7.0,
            "bonding": 6.5,
            "routine": 2.0
        }
        
        importance = base_importance.get(episode_type, 5.0)
        
        # Adjust by sentiment
        sentiment_modifier = {
            "very_positive": 1.2,
            "positive": 1.1,
            "neutral": 1.0,
            "negative": 1.1,
            "very_negative": 1.3  # Strong negative is also important
        }
        
        importance *= sentiment_modifier.get(sentiment, 1.0)
        
        # Bonus for multi-message episodes
        if message_count > 3:
            importance += 0.5
        
        # Clamp to 0-10
        return max(0.0, min(10.0, importance))
    
    def should_store_episode(self, importance: float) -> bool:
        """Check if episode should be stored based on importance"""
        return importance >= self.importance_threshold
    
    def create_episode(
        self,
        user_id: str,
        episode_type: str,
        title: str,
        summary: str,
        sentiment: str,
        session_id: Optional[str] = None,
        context_messages: Optional[List[str]] = None,
        tags: Optional[List[str]] = None
    ) -> Episode:
        """
        Create an episode
        
        Args:
            user_id: User ID
            episode_type: Type of episode
            title: Short title
            summary: Summary of episode
            sentiment: Sentiment
            session_id: Session ID (optional)
            context_messages: Message IDs that form the episode
            tags: Tags for categorization
            
        Returns:
            Episode object
        """
        importance = self.calculate_importance(
            episode_type,
            sentiment,
            len(context_messages) if context_messages else 1
        )
        
        episode = Episode(
            user_id=user_id,
            session_id=session_id,
            episode_type=episode_type,
            title=title,
            summary=summary,
            importance=importance,
            sentiment=sentiment,
            timestamp=datetime.now(),
            context_messages=context_messages or [],
            tags=tags or []
        )
        
        logger.info(
            f"Created episode: {episode_type} "
            f"(importance: {importance:.1f}/10)"
        )
        
        return episode

