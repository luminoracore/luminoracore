"""
Test Step 8: SDK Storage v1.1 Extensions

Validates v1.1 storage methods for affinity, facts, episodes, moods
"""

import pytest
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11


class TestInMemoryStorageV11:
    """Test InMemoryStorageV11 implementation"""
    
    @pytest.mark.asyncio
    async def test_save_and_get_affinity(self):
        """Test saving and retrieving affinity"""
        storage = InMemoryStorageV11()
        
        # Save affinity
        success = await storage.save_affinity(
            user_id="user1",
            personality_name="alicia",
            affinity_points=50,
            current_level="friend"
        )
        
        assert success == True
        
        # Get affinity
        affinity = await storage.get_affinity("user1", "alicia")
        
        assert affinity is not None
        assert affinity["affinity_points"] == 50
        assert affinity["current_level"] == "friend"
    
    @pytest.mark.asyncio
    async def test_save_and_get_facts(self):
        """Test saving and retrieving facts"""
        storage = InMemoryStorageV11()
        
        # Save facts
        await storage.save_fact(
            user_id="user1",
            category="personal_info",
            key="name",
            value="Diego",
            confidence=0.99
        )
        
        await storage.save_fact(
            user_id="user1",
            category="preferences",
            key="anime",
            value="Naruto",
            confidence=0.9
        )
        
        # Get all facts
        facts = await storage.get_facts("user1")
        assert len(facts) == 2
        
        # Get facts by category
        personal_facts = await storage.get_facts("user1", category="personal_info")
        assert len(personal_facts) == 1
        assert personal_facts[0]["key"] == "name"
    
    @pytest.mark.asyncio
    async def test_save_and_get_episodes(self):
        """Test saving and retrieving episodes"""
        storage = InMemoryStorageV11()
        
        # Save episodes
        await storage.save_episode(
            user_id="user1",
            episode_type="emotional_moment",
            title="Loss of pet",
            summary="User's dog passed away",
            importance=9.5,
            sentiment="very_negative"
        )
        
        await storage.save_episode(
            user_id="user1",
            episode_type="routine",
            title="Small talk",
            summary="Weather chat",
            importance=2.0,
            sentiment="neutral"
        )
        
        # Get all episodes
        episodes = await storage.get_episodes("user1")
        assert len(episodes) == 2
        
        # Get important episodes only
        important = await storage.get_episodes("user1", min_importance=5.0)
        assert len(important) == 1
        assert important[0]["importance"] == 9.5
    
    @pytest.mark.asyncio
    async def test_save_and_get_mood(self):
        """Test saving and retrieving mood"""
        storage = InMemoryStorageV11()
        
        # Save mood
        success = await storage.save_mood(
            session_id="session1",
            user_id="user1",
            current_mood="shy",
            mood_intensity=0.8
        )
        
        assert success == True
        
        # Get mood
        mood = await storage.get_mood("session1")
        
        assert mood is not None
        assert mood["current_mood"] == "shy"
        assert mood["mood_intensity"] == 0.8
    
    @pytest.mark.asyncio
    async def test_update_existing_fact(self):
        """Test updating an existing fact"""
        storage = InMemoryStorageV11()
        
        # Save initial fact
        await storage.save_fact(
            user_id="user1",
            category="preferences",
            key="anime",
            value="Naruto",
            confidence=0.8
        )
        
        # Update with higher confidence
        await storage.save_fact(
            user_id="user1",
            category="preferences",
            key="anime",
            value="Naruto and One Piece",
            confidence=0.95
        )
        
        # Should have only one fact (updated)
        facts = await storage.get_facts("user1", category="preferences")
        assert len(facts) == 1
        assert facts[0]["value"] == "Naruto and One Piece"
        assert facts[0]["confidence"] == 0.95


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

