"""
Test Step 11: SDK Client v1.1 Extensions

Validates v1.1 client API methods
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
        pass


class TestClientV11Memory:
    """Test v1.1 memory methods"""
    
    @pytest.mark.asyncio
    async def test_get_facts(self):
        """Test getting facts"""
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(MockBaseClient(), storage_v11=storage)
        
        # Save a fact
        await storage.save_fact("user1", "personal_info", "name", "Diego")
        
        # Get facts
        facts = await client.get_facts("user1")
        
        assert len(facts) == 1
        assert facts[0]["key"] == "name"
    
    @pytest.mark.asyncio
    async def test_get_episodes(self):
        """Test getting episodes"""
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(MockBaseClient(), storage_v11=storage)
        
        # Save an episode
        await storage.save_episode(
            "user1", "milestone", "First chat", "Summary", 7.0, "positive"
        )
        
        # Get episodes
        episodes = await client.get_episodes("user1")
        
        assert len(episodes) == 1
        assert episodes[0]["title"] == "First chat"


class TestClientV11Affinity:
    """Test v1.1 affinity methods"""
    
    @pytest.mark.asyncio
    async def test_get_affinity(self):
        """Test getting affinity"""
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(MockBaseClient(), storage_v11=storage)
        
        # Save affinity
        await storage.save_affinity("user1", "alicia", 50, "friend")
        
        # Get affinity
        affinity = await client.get_affinity("user1", "alicia")
        
        assert affinity is not None
        assert affinity["affinity_points"] == 50
    
    @pytest.mark.asyncio
    async def test_update_affinity_new_user(self):
        """Test updating affinity for new user"""
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(MockBaseClient(), storage_v11=storage)
        
        # Update affinity (user doesn't exist yet)
        result = await client.update_affinity("user1", "alicia", points_delta=5, interaction_type="positive")
        
        assert result is not None
        assert result["affinity_points"] == 5
    
    @pytest.mark.asyncio
    async def test_update_affinity_existing_user(self):
        """Test updating affinity for existing user"""
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(MockBaseClient(), storage_v11=storage)
        
        # Save initial affinity
        await storage.save_affinity("user1", "alicia", 40, "acquaintance")
        
        # Update affinity
        result = await client.update_affinity("user1", "alicia", points_delta=10, interaction_type="positive")
        
        assert result is not None
        assert result["affinity_points"] == 50


class TestClientV11Snapshot:
    """Test v1.1 snapshot methods"""
    
    @pytest.mark.asyncio
    async def test_export_snapshot(self):
        """Test exporting snapshot"""
        client = LuminoraCoreClientV11(MockBaseClient())
        
        snapshot = await client.export_snapshot("session1")
        
        assert "_snapshot_info" in snapshot
        assert "current_state" in snapshot
    
    @pytest.mark.asyncio
    async def test_import_snapshot(self):
        """Test importing snapshot"""
        client = LuminoraCoreClientV11(MockBaseClient())
        
        snapshot: PersonalitySnapshotDict = {
            "_snapshot_info": {
                "created_at": "2025-10-14T12:00:00",
                "template_name": "alicia",
                "template_version": "1.1.0",
                "user_id": "user1",
                "session_id": "old_session",
                "total_messages": 100,
                "days_active": 10
            },
            "persona": {},
            "core_traits": {},
            "linguistic_profile": {},
            "behavioral_rules": {},
            "advanced_parameters": {},
            "current_state": {
                "learned_facts": [],
                "memorable_episodes": []
            }
        }
        
        session_id = await client.import_snapshot(snapshot, "user2")
        
        assert session_id is not None
        assert "session_" in session_id


# Import for type checking
from luminoracore_sdk.types.snapshot import PersonalitySnapshotDict


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

