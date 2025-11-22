"""
Test Step 4: Affinity Management System

Validates affinity point tracking and level progression
"""

import pytest
from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore.core.relationship.affinity import AffinityState, AffinityManager
from luminoracore.core.relationship.events import InteractionType, RelationshipEvent


class TestAffinityState:
    """Test AffinityState dataclass"""
    
    def test_create_valid_state(self):
        """Test creating valid affinity state"""
        state = AffinityState(
            user_id="user1",
            personality_name="alicia",
            affinity_points=50
        )
        assert state.affinity_points == 50
        assert state.current_level == "stranger"
    
    def test_invalid_points(self):
        """Test validation of affinity points"""
        with pytest.raises(ValueError):
            AffinityState("user1", "alicia", affinity_points=150)
        
        with pytest.raises(ValueError):
            AffinityState("user1", "alicia", affinity_points=-10)


class TestAffinityManager:
    """Test AffinityManager class"""
    
    def test_calculate_points_delta(self):
        """Test points delta calculation"""
        manager = AffinityManager()
        
        assert manager.calculate_points_delta("very_positive") == 5
        assert manager.calculate_points_delta("positive") == 2
        assert manager.calculate_points_delta("neutral") == 1
        assert manager.calculate_points_delta("negative") == -2
    
    def test_calculate_with_message_length(self):
        """Test bonus for long messages"""
        manager = AffinityManager()
        
        # Short message
        delta_short = manager.calculate_points_delta("positive", message_length=50)
        assert delta_short == 2
        
        # Long message (bonus)
        delta_long = manager.calculate_points_delta("positive", message_length=150)
        assert delta_long == 3
    
    def test_determine_level_defaults(self):
        """Test level determination with default levels"""
        manager = AffinityManager()
        
        assert manager.determine_level(10) == "stranger"
        assert manager.determine_level(30) == "acquaintance"
        assert manager.determine_level(50) == "friend"
        assert manager.determine_level(70) == "close_friend"
        assert manager.determine_level(90) == "soulmate"
    
    def test_determine_level_custom(self):
        """Test level determination with custom definitions"""
        manager = AffinityManager()
        
        custom_levels = [
            {"name": "unknown", "min": 0, "max": 30},
            {"name": "buddy", "min": 31, "max": 100}
        ]
        
        assert manager.determine_level(20, custom_levels) == "unknown"
        assert manager.determine_level(50, custom_levels) == "buddy"
    
    def test_update_affinity_state(self):
        """Test updating affinity state"""
        manager = AffinityManager()
        
        state = AffinityState(
            user_id="user1",
            personality_name="alicia",
            affinity_points=40,
            current_level="acquaintance"
        )
        
        # Update with positive delta
        updated = manager.update_affinity_state(state, points_delta=5)
        
        assert updated.affinity_points == 45
        assert updated.current_level == "friend"  # Should have progressed
        assert updated.total_messages == 1
        assert updated.positive_interactions == 1
    
    def test_update_clamps_at_boundaries(self):
        """Test that affinity is clamped to 0-100"""
        manager = AffinityManager()
        
        # Test upper bound
        state_high = AffinityState("user1", "alicia", affinity_points=98)
        updated_high = manager.update_affinity_state(state_high, points_delta=10)
        assert updated_high.affinity_points == 100
        
        # Test lower bound
        state_low = AffinityState("user1", "alicia", affinity_points=2)
        updated_low = manager.update_affinity_state(state_low, points_delta=-10)
        assert updated_low.affinity_points == 0
    
    def test_get_level_progress(self):
        """Test getting progress within current level"""
        manager = AffinityManager()
        
        state = AffinityState(
            user_id="user1",
            personality_name="alicia",
            affinity_points=50,
            current_level="friend"
        )
        
        progress = manager.get_level_progress(state)
        
        assert progress["current_level"] == "friend"
        assert progress["points"] == 50
        assert progress["next_level"] == "close_friend"
        assert progress["points_to_next_level"] == 11  # 61 - 50


class TestRelationshipEvent:
    """Test RelationshipEvent class"""
    
    def test_create_event(self):
        """Test creating relationship event"""
        event = RelationshipEvent(
            user_id="user1",
            personality_name="alicia",
            interaction_type=InteractionType.POSITIVE,
            points_delta=2,
            reason="User gave compliment"
        )
        
        assert event.user_id == "user1"
        assert event.points_delta == 2
        assert event.timestamp is not None
    
    def test_event_to_dict(self):
        """Test event serialization"""
        event = RelationshipEvent(
            user_id="user1",
            personality_name="alicia",
            interaction_type=InteractionType.POSITIVE,
            points_delta=2
        )
        
        data = event.to_dict()
        
        assert data["user_id"] == "user1"
        assert data["interaction_type"] == "positive"
        assert data["points_delta"] == 2


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

