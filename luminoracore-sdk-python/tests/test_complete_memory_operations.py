"""
Test Complete Memory Operations for LuminoraCore v1.1

Tests the COMPLETE memory system with both read and write operations:
✅ Save facts and episodes
✅ Retrieve facts and episodes
✅ Delete facts
✅ Get memory statistics
✅ Manage affinity relationships
"""

import pytest
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11


class MockBaseClient:
    """Mock base client for testing"""
    def __init__(self):
        self.sessions = {}


class TestCompleteMemoryOperations:
    """Test complete memory operations"""
    
    @pytest.mark.asyncio
    async def test_save_and_retrieve_facts(self):
        """Test saving and retrieving facts"""
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(MockBaseClient(), storage_v11=storage)
        
        user_id = "test_user"
        
        # Save facts
        await client.save_fact(user_id, "personal_info", "name", "Test User", confidence=0.95)
        await client.save_fact(user_id, "preferences", "language", "Python", confidence=0.9)
        await client.save_fact(user_id, "work", "company", "Test Corp", confidence=0.85)
        
        # Retrieve all facts
        all_facts = await client.get_facts(user_id)
        assert len(all_facts) == 3
        
        # Retrieve by category
        personal_facts = await client.get_facts(user_id, category="personal_info")
        assert len(personal_facts) == 1
        assert personal_facts[0]["key"] == "name"
        assert personal_facts[0]["value"] == "Test User"
        
        preference_facts = await client.get_facts(user_id, category="preferences")
        assert len(preference_facts) == 1
        assert preference_facts[0]["key"] == "language"
        assert preference_facts[0]["value"] == "Python"
    
    @pytest.mark.asyncio
    async def test_save_and_retrieve_episodes(self):
        """Test saving and retrieving episodes"""
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(MockBaseClient(), storage_v11=storage)
        
        user_id = "test_user"
        
        # Save episodes
        await client.save_episode(
            user_id, "milestone", "First meeting", "Initial conversation", 7.5, "positive"
        )
        await client.save_episode(
            user_id, "emotional_moment", "Shared interest", "Bonded over music", 8.0, "very_positive"
        )
        await client.save_episode(
            user_id, "routine", "Daily check", "Regular interaction", 4.0, "neutral"
        )
        
        # Retrieve all episodes
        all_episodes = await client.get_episodes(user_id)
        assert len(all_episodes) == 3
        
        # Retrieve important episodes only
        important_episodes = await client.get_episodes(user_id, min_importance=7.0)
        assert len(important_episodes) == 2
        
        # Check episode details
        milestone_episodes = [e for e in all_episodes if e["episode_type"] == "milestone"]
        assert len(milestone_episodes) == 1
        assert milestone_episodes[0]["title"] == "First meeting"
        assert milestone_episodes[0]["importance"] == 7.5
    
    @pytest.mark.asyncio
    async def test_affinity_management(self):
        """Test affinity management"""
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(MockBaseClient(), storage_v11=storage)
        
        user_id = "test_user"
        personality_name = "test_personality"
        
        # Update affinity
        affinity = await client.update_affinity(
            user_id, personality_name, points_delta=5, interaction_type="first_meeting"
        )
        assert affinity["affinity_points"] == 5
        assert affinity["current_level"] == "stranger"
        
        # Update affinity again
        affinity = await client.update_affinity(
            user_id, personality_name, points_delta=10, interaction_type="positive_interaction"
        )
        assert affinity["affinity_points"] == 15
        assert affinity["current_level"] == "stranger"
        
        # Update affinity to reach acquaintance level
        affinity = await client.update_affinity(
            user_id, personality_name, points_delta=10, interaction_type="deep_conversation"
        )
        assert affinity["affinity_points"] == 25
        assert affinity["current_level"] == "acquaintance"
        
        # Get affinity
        current_affinity = await client.get_affinity(user_id, personality_name)
        assert current_affinity["affinity_points"] == 25
        assert current_affinity["current_level"] == "acquaintance"
    
    @pytest.mark.asyncio
    async def test_delete_fact(self):
        """Test deleting facts"""
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(MockBaseClient(), storage_v11=storage)
        
        user_id = "test_user"
        
        # Save facts
        await client.save_fact(user_id, "preferences", "language", "Python", confidence=0.9)
        await client.save_fact(user_id, "preferences", "framework", "Django", confidence=0.8)
        
        # Verify facts exist
        facts = await client.get_facts(user_id, category="preferences")
        assert len(facts) == 2
        
        # Delete a fact
        deleted = await client.delete_fact(user_id, "preferences", "language")
        assert deleted is True
        
        # Verify deletion
        remaining_facts = await client.get_facts(user_id, category="preferences")
        assert len(remaining_facts) == 1
        assert remaining_facts[0]["key"] == "framework"
        assert remaining_facts[0]["value"] == "Django"
    
    @pytest.mark.asyncio
    async def test_memory_statistics(self):
        """Test memory statistics"""
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(MockBaseClient(), storage_v11=storage)
        
        user_id = "test_user"
        
        # Save facts
        await client.save_fact(user_id, "personal_info", "name", "Test User", confidence=0.95)
        await client.save_fact(user_id, "preferences", "language", "Python", confidence=0.9)
        await client.save_fact(user_id, "work", "company", "Test Corp", confidence=0.85)
        
        # Save episodes
        await client.save_episode(
            user_id, "milestone", "First meeting", "Initial conversation", 7.5, "positive"
        )
        await client.save_episode(
            user_id, "emotional_moment", "Shared interest", "Bonded over music", 8.0, "very_positive"
        )
        
        # Get statistics
        stats = await client.get_memory_stats(user_id)
        
        # Verify statistics
        assert stats["total_facts"] == 3
        assert stats["total_episodes"] == 2
        assert "personal_info" in stats["fact_categories"]
        assert "preferences" in stats["fact_categories"]
        assert "work" in stats["fact_categories"]
        assert stats["fact_categories"]["personal_info"] == 1
        assert stats["fact_categories"]["preferences"] == 1
        assert stats["fact_categories"]["work"] == 1
        
        assert "milestone" in stats["episode_types"]
        assert "emotional_moment" in stats["episode_types"]
        assert stats["episode_types"]["milestone"] == 1
        assert stats["episode_types"]["emotional_moment"] == 1
        
        # Check most important episode
        assert stats["most_important_episode"] is not None
        assert stats["most_important_episode"]["importance"] == 8.0
        assert stats["most_important_episode"]["title"] == "Shared interest"
    
    @pytest.mark.asyncio
    async def test_complete_workflow(self):
        """Test complete memory workflow"""
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(MockBaseClient(), storage_v11=storage)
        
        user_id = "test_user"
        personality_name = "test_personality"
        
        # 1. Save facts
        await client.save_fact(user_id, "personal_info", "name", "Test User", confidence=0.95)
        await client.save_fact(user_id, "preferences", "language", "Python", confidence=0.9)
        
        # 2. Save episodes
        await client.save_episode(
            user_id, "milestone", "First meeting", "Initial conversation", 7.5, "positive"
        )
        
        # 3. Update affinity
        affinity = await client.update_affinity(
            user_id, personality_name, points_delta=5, interaction_type="first_meeting"
        )
        
        # 4. Retrieve data
        facts = await client.get_facts(user_id)
        episodes = await client.get_episodes(user_id)
        current_affinity = await client.get_affinity(user_id, personality_name)
        
        # 5. Get statistics
        stats = await client.get_memory_stats(user_id)
        
        # 6. Verify everything
        assert len(facts) == 2
        assert len(episodes) == 1
        assert current_affinity["affinity_points"] == 5
        assert stats["total_facts"] == 2
        assert stats["total_episodes"] == 1
        
        # 7. Delete a fact
        deleted = await client.delete_fact(user_id, "preferences", "language")
        assert deleted is True
        
        # 8. Verify deletion
        remaining_facts = await client.get_facts(user_id)
        assert len(remaining_facts) == 1
        assert remaining_facts[0]["key"] == "name"
        
        # 9. Final statistics
        final_stats = await client.get_memory_stats(user_id)
        assert final_stats["total_facts"] == 1
        assert final_stats["total_episodes"] == 1


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
