"""
Test Step 10: SDK Memory Manager v1.1

Validates v1.1 memory manager extensions
"""

import pytest
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
from luminoracore_sdk.session.memory_v1_1 import MemoryManagerV11


class TestMemoryManagerV11:
    """Test MemoryManagerV11 class"""
    
    @pytest.mark.asyncio
    async def test_get_facts(self):
        """Test getting facts"""
        storage = InMemoryStorageV11()
        manager = MemoryManagerV11(storage_v11=storage)
        
        # Save some facts
        await storage.save_fact("user1", "personal_info", "name", "Diego", confidence=0.99)
        await storage.save_fact("user1", "preferences", "anime", "Naruto", confidence=0.9)
        
        # Get all facts
        facts = await manager.get_facts("user1")
        assert len(facts) == 2
        
        # Get facts by category
        facts_filtered = await manager.get_facts("user1", options={"category": "personal_info"})
        assert len(facts_filtered) == 1
    
    @pytest.mark.asyncio
    async def test_get_episodes(self):
        """Test getting episodes"""
        storage = InMemoryStorageV11()
        manager = MemoryManagerV11(storage_v11=storage)
        
        # Save episodes
        await storage.save_episode(
            "user1", "emotional_moment", "Title1", "Summary1", 9.0, "positive"
        )
        await storage.save_episode(
            "user1", "routine", "Title2", "Summary2", 2.0, "neutral"
        )
        
        # Get all episodes
        episodes = await manager.get_episodes("user1")
        assert len(episodes) == 2
        
        # Get important episodes only
        episodes_important = await manager.get_episodes("user1", min_importance=5.0)
        assert len(episodes_important) == 1
        assert episodes_important[0]["importance"] == 9.0
    
    @pytest.mark.asyncio
    async def test_get_episodes_sorted_by_importance(self):
        """Test that episodes are sorted by current importance"""
        storage = InMemoryStorageV11()
        manager = MemoryManagerV11(storage_v11=storage)
        
        # Save episodes with different importance
        await storage.save_episode("user1", "routine", "Low", "Summary", 3.0, "neutral")
        await storage.save_episode("user1", "emotional_moment", "High", "Summary", 9.0, "positive")
        await storage.save_episode("user1", "achievement", "Medium", "Summary", 6.0, "positive")
        
        # Get all episodes
        episodes = await manager.get_episodes("user1")
        
        # Should be sorted by importance (descending)
        assert episodes[0]["importance"] == 9.0
        assert episodes[1]["importance"] == 6.0
        assert episodes[2]["importance"] == 3.0
    
    @pytest.mark.asyncio
    async def test_get_context_for_query(self):
        """Test getting combined context"""
        storage = InMemoryStorageV11()
        manager = MemoryManagerV11(storage_v11=storage)
        
        # Save data
        await storage.save_fact("user1", "personal_info", "name", "Diego")
        await storage.save_episode("user1", "milestone", "First chat", "Summary", 7.0, "positive")
        
        # Get context
        context = await manager.get_context_for_query("user1", "tell me about Diego")
        
        assert "facts" in context
        assert "episodes" in context
        assert "search_results" in context
        assert len(context["facts"]) > 0
        assert len(context["episodes"]) > 0


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

