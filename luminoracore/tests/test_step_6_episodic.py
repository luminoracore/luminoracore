"""
Test Step 6: Episodic Memory System

Validates episode detection and memorable moment tracking
"""

import pytest
from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore.core.memory.episodic import (
    Episode,
    EpisodeType,
    Sentiment,
    EpisodicMemoryManager
)


class TestEpisode:
    """Test Episode dataclass"""
    
    def test_create_valid_episode(self):
        """Test creating valid episode"""
        episode = Episode(
            user_id="user1",
            episode_type="emotional_moment",
            title="Loss of pet",
            summary="User shared sad news about pet",
            importance=9.0,
            sentiment="very_negative",
            timestamp=datetime.now()
        )
        assert episode.importance == 9.0
        assert episode.temporal_decay == 1.0
    
    def test_invalid_importance(self):
        """Test validation of importance"""
        with pytest.raises(ValueError):
            Episode(
                "user1", "emotional_moment", "Title", "Summary",
                importance=15.0,  # > 10
                sentiment="positive",
                timestamp=datetime.now()
            )
    
    def test_get_current_importance(self):
        """Test current importance with decay"""
        episode = Episode(
            "user1", "emotional_moment", "Title", "Summary",
            importance=9.0,
            sentiment="positive",
            timestamp=datetime.now(),
            temporal_decay=0.8
        )
        
        current = episode.get_current_importance()
        assert current == pytest.approx(7.2)  # 9.0 * 0.8
    
    def test_update_decay(self):
        """Test temporal decay update"""
        episode = Episode(
            "user1", "emotional_moment", "Title", "Summary",
            importance=9.0,
            sentiment="positive",
            timestamp=datetime.now()
        )
        
        # After 30 days
        episode.update_decay(days_passed=30)
        
        # Decay should be less than 1.0
        assert episode.temporal_decay < 1.0
        assert episode.temporal_decay > 0.0
    
    def test_episode_to_dict(self):
        """Test episode serialization"""
        episode = Episode(
            user_id="user1",
            episode_type="milestone",
            title="First conversation",
            summary="User and AI met for first time",
            importance=7.0,
            sentiment="positive",
            timestamp=datetime.now(),
            tags=["first", "milestone"]
        )
        
        data = episode.to_dict()
        
        assert data["user_id"] == "user1"
        assert data["episode_type"] == "milestone"
        assert data["importance"] == 7.0


class TestEpisodicMemoryManager:
    """Test EpisodicMemoryManager class"""
    
    def test_calculate_importance_emotional(self):
        """Test importance calculation for emotional moments"""
        manager = EpisodicMemoryManager()
        
        importance = manager.calculate_importance(
            episode_type="emotional_moment",
            sentiment="very_negative",
            message_count=1
        )
        
        # Emotional moments have high base importance
        assert importance >= 8.0
    
    def test_calculate_importance_routine(self):
        """Test importance calculation for routine"""
        manager = EpisodicMemoryManager()
        
        importance = manager.calculate_importance(
            episode_type="routine",
            sentiment="neutral",
            message_count=1
        )
        
        # Routine has low importance
        assert importance <= 3.0
    
    def test_should_store_episode(self):
        """Test storage threshold"""
        manager = EpisodicMemoryManager(importance_threshold=5.0)
        
        assert manager.should_store_episode(8.0) == True
        assert manager.should_store_episode(3.0) == False
    
    def test_create_episode(self):
        """Test episode creation"""
        manager = EpisodicMemoryManager()
        
        episode = manager.create_episode(
            user_id="user1",
            episode_type="milestone",
            title="First conversation",
            summary="User and AI met for first time",
            sentiment="positive",
            session_id="session123",
            tags=["first", "milestone"]
        )
        
        assert episode.user_id == "user1"
        assert episode.episode_type == "milestone"
        assert episode.importance > 0
        assert episode.timestamp is not None


class TestEpisodeTypes:
    """Test episode type enum"""
    
    def test_all_types_defined(self):
        """Test that all expected types are defined"""
        types = [t.value for t in EpisodeType]
        
        assert "emotional_moment" in types
        assert "milestone" in types
        assert "confession" in types
        assert "achievement" in types


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

