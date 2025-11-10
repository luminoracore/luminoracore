"""
Test Step 9: SDK v1.1 Types

Validates v1.1 type definitions
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore_sdk.types.memory import (
    FactDict,
    EpisodeDict,
    MemorySearchResult,
    MemoryQueryOptions
)
from luminoracore_sdk.types.relationship import (
    AffinityDict,
    AffinityProgressDict,
    LevelChangeDict
)
from luminoracore_sdk.types.snapshot import (
    SnapshotMetadataDict,
    PersonalitySnapshotDict,
    SnapshotExportOptions
)


class TestMemoryTypes:
    """Test memory type definitions"""
    
    def test_fact_dict(self):
        """Test FactDict type"""
        fact: FactDict = {
            "id": "fact1",
            "user_id": "user1",
            "category": "personal_info",
            "key": "name",
            "value": "Diego",
            "confidence": 0.99,
            "tags": ["name"]
        }
        
        assert fact["user_id"] == "user1"
        assert fact["confidence"] == 0.99
    
    def test_episode_dict(self):
        """Test EpisodeDict type"""
        episode: EpisodeDict = {
            "id": "ep1",
            "user_id": "user1",
            "episode_type": "emotional_moment",
            "title": "Test",
            "summary": "Summary",
            "importance": 9.0,
            "sentiment": "positive",
            "timestamp": "2025-10-14T12:00:00",
            "tags": ["test"]
        }
        
        assert episode["importance"] == 9.0
        assert episode["episode_type"] == "emotional_moment"


class TestRelationshipTypes:
    """Test relationship type definitions"""
    
    def test_affinity_dict(self):
        """Test AffinityDict type"""
        affinity: AffinityDict = {
            "id": "aff1",
            "user_id": "user1",
            "personality_name": "alicia",
            "affinity_points": 50,
            "current_level": "friend",
            "total_messages": 100
        }
        
        assert affinity["affinity_points"] == 50
        assert affinity["current_level"] == "friend"
    
    def test_affinity_progress_dict(self):
        """Test AffinityProgressDict type"""
        progress: AffinityProgressDict = {
            "current_level": "friend",
            "points": 50,
            "progress_in_level": 0.45,
            "points_to_next_level": 11,
            "next_level": "close_friend"
        }
        
        assert progress["progress_in_level"] == 0.45


class TestSnapshotTypes:
    """Test snapshot type definitions"""
    
    def test_snapshot_metadata(self):
        """Test SnapshotMetadataDict type"""
        metadata: SnapshotMetadataDict = {
            "created_at": "2025-10-14T12:00:00",
            "template_name": "alicia",
            "template_version": "1.1.0",
            "user_id": "user1",
            "session_id": "session1",
            "total_messages": 150,
            "days_active": 30
        }
        
        assert metadata["template_name"] == "alicia"
        assert metadata["total_messages"] == 150
    
    def test_snapshot_export_options(self):
        """Test SnapshotExportOptions type"""
        options: SnapshotExportOptions = {
            "include_conversation_history": True,
            "include_facts": True,
            "include_episodes": True,
            "include_embeddings": False,
            "anonymize_user_data": False
        }
        
        assert options["include_facts"] == True
        assert options["include_embeddings"] == False


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

