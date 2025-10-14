"""
Test Step 7: Memory Classification System

Validates classification of facts and episodes
"""

import pytest
from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore.core.memory.fact_extractor import Fact
from luminoracore.core.memory.episodic import Episode
from luminoracore.core.memory.classifier import (
    ImportanceLevel,
    ClassificationResult,
    MemoryClassifier
)


class TestMemoryClassifier:
    """Test MemoryClassifier class"""
    
    def test_classify_fact(self):
        """Test fact classification"""
        classifier = MemoryClassifier()
        
        fact = Fact(
            user_id="user1",
            category="personal_info",
            key="name",
            value="Diego",
            confidence=0.99,
            tags=["name", "personal"]
        )
        
        result = classifier.classify_fact(fact)
        
        assert result.item_type == "fact"
        assert result.primary_category == "personal_info"
        assert result.confidence == 0.99
    
    def test_classify_episode(self):
        """Test episode classification"""
        classifier = MemoryClassifier()
        
        episode = Episode(
            user_id="user1",
            episode_type="emotional_moment",
            title="Loss of pet",
            summary="User's dog passed away",
            importance=9.5,
            sentiment="very_negative",
            timestamp=datetime.now(),
            tags=["sad", "loss", "pet"]
        )
        
        result = classifier.classify_episode(episode)
        
        assert result.item_type == "episode"
        assert result.primary_category == "emotional_moment"
        assert result.importance_level == "critical"
    
    def test_classify_fact_importance_high_confidence(self):
        """Test high confidence fact classified as high importance"""
        classifier = MemoryClassifier()
        
        fact = Fact(
            user_id="user1",
            category="personal_info",
            key="name",
            value="Diego",
            confidence=0.99
        )
        
        result = classifier.classify_fact(fact)
        
        assert result.importance_level == "high"
    
    def test_classify_fact_importance_low_confidence(self):
        """Test low confidence fact classified as low importance"""
        classifier = MemoryClassifier()
        
        fact = Fact(
            user_id="user1",
            category="preferences",
            key="maybe_likes",
            value="something",
            confidence=0.6
        )
        
        result = classifier.classify_fact(fact)
        
        assert result.importance_level == "low"
    
    def test_get_facts_by_category(self):
        """Test filtering facts by category"""
        classifier = MemoryClassifier()
        
        facts = [
            Fact("user1", "personal_info", "name", "Diego", 0.99),
            Fact("user1", "preferences", "anime", "Naruto", 0.9),
            Fact("user1", "personal_info", "age", 28, 0.99),
        ]
        
        personal_facts = classifier.get_facts_by_category(facts, "personal_info")
        
        assert len(personal_facts) == 2
        assert all(f.category == "personal_info" for f in personal_facts)
    
    def test_get_top_n_episodes(self):
        """Test getting top N episodes"""
        classifier = MemoryClassifier()
        
        episodes = [
            Episode("user1", "routine", "Chat", "Regular chat", 2.0, "neutral", datetime.now()),
            Episode("user1", "emotional_moment", "Loss", "Pet died", 9.5, "very_negative", datetime.now()),
            Episode("user1", "achievement", "Success", "Got promotion", 7.0, "positive", datetime.now()),
        ]
        
        top_2 = classifier.get_top_n_episodes(episodes, n=2)
        
        assert len(top_2) == 2
        assert top_2[0].importance == 9.5  # Highest first
        assert top_2[1].importance == 7.0


class TestImportanceLevel:
    """Test ImportanceLevel enum"""
    
    def test_all_levels_defined(self):
        """Test that all importance levels are defined"""
        levels = [l.value for l in ImportanceLevel]
        
        assert "critical" in levels
        assert "high" in levels
        assert "medium" in levels
        assert "low" in levels
        assert "trivial" in levels


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

