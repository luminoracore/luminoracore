"""
Test Step 2: Feature Flag System

Validates feature flag management and enforcement
"""

import pytest
import tempfile
import json
from pathlib import Path

# Add parent to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore.core.config.feature_flags import (
    V11Features,
    FeatureFlagManager,
    FeatureCategory,
    get_features,
    is_enabled,
    require_feature
)


class TestV11Features:
    """Test V11Features dataclass"""
    
    def test_default_all_disabled(self):
        """Test that default constructor disables all features"""
        features = V11Features()
        
        assert features.episodic_memory == False
        assert features.semantic_search == False
        assert features.hierarchical_personality == False
        assert features.affinity_system == False
    
    def test_all_disabled(self):
        """Test all_disabled factory method"""
        features = V11Features.all_disabled()
        
        disabled = features.get_disabled_features()
        assert len(disabled) == 8  # All 8 features
    
    def test_all_enabled(self):
        """Test all_enabled factory method"""
        features = V11Features.all_enabled()
        
        enabled = features.get_enabled_features()
        assert len(enabled) == 8  # All 8 features
        assert 'episodic_memory' in enabled
        assert 'affinity_system' in enabled
    
    def test_safe_rollout(self):
        """Test safe_rollout defaults"""
        features = V11Features.safe_rollout()
        
        # Should enable only simple features
        assert features.affinity_system == True
        assert features.hierarchical_personality == True
        
        # Should keep complex features disabled
        assert features.episodic_memory == False
        assert features.semantic_search == False
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        features = V11Features(episodic_memory=True, affinity_system=True)
        data = features.to_dict()
        
        assert isinstance(data, dict)
        assert data['episodic_memory'] == True
        assert data['affinity_system'] == True
    
    def test_from_dict(self):
        """Test creation from dictionary"""
        data = {
            'episodic_memory': True,
            'mood_system': True,
            'invalid_key': True  # Should be ignored
        }
        features = V11Features.from_dict(data)
        
        assert features.episodic_memory == True
        assert features.mood_system == True
    
    def test_get_enabled_features(self):
        """Test getting list of enabled features"""
        features = V11Features(
            episodic_memory=True,
            mood_system=True,
            affinity_system=True
        )
        
        enabled = features.get_enabled_features()
        assert len(enabled) == 3
        assert 'episodic_memory' in enabled
    
    def test_enable_disable_feature(self):
        """Test enabling and disabling individual features"""
        features = V11Features()
        
        # Enable a feature
        features.enable_feature('episodic_memory')
        assert features.episodic_memory == True
        
        # Disable it
        features.disable_feature('episodic_memory')
        assert features.episodic_memory == False
    
    def test_invalid_feature_name(self):
        """Test error handling for invalid feature names"""
        features = V11Features()
        
        with pytest.raises(ValueError, match="Unknown feature"):
            features.enable_feature('nonexistent_feature')
    
    def test_get_summary(self):
        """Test getting feature summary"""
        features = V11Features(episodic_memory=True, affinity_system=True)
        summary = features.get_summary()
        
        assert summary['total_features'] == 8
        assert summary['enabled_count'] == 2
        assert summary['disabled_count'] == 6


class TestFeatureFlagManager:
    """Test FeatureFlagManager singleton"""
    
    def test_singleton_pattern(self):
        """Test that manager is a singleton"""
        manager1 = FeatureFlagManager()
        manager2 = FeatureFlagManager()
        
        assert manager1 is manager2
    
    def test_get_set_features(self):
        """Test getting and setting features"""
        manager = FeatureFlagManager()
        
        # Set custom features
        custom = V11Features(episodic_memory=True, mood_system=True)
        manager.set_features(custom)
        
        # Get and verify
        retrieved = manager.get_features()
        assert retrieved.episodic_memory == True
    
    def test_load_from_file(self):
        """Test loading features from file"""
        manager = FeatureFlagManager()
        
        # Create temp config file
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        ) as f:
            config = {
                "v1_1_features": {
                    "episodic_memory": True,
                    "mood_system": True
                }
            }
            json.dump(config, f)
            filepath = f.name
        
        try:
            # Load from file
            loaded = manager.load_from_file(filepath)
            
            assert loaded.episodic_memory == True
            assert loaded.mood_system == True
        finally:
            try:
                Path(filepath).unlink()
            except:
                pass
    
    def test_save_to_file(self):
        """Test saving features to file"""
        manager = FeatureFlagManager()
        
        # Set features
        manager.set_features(V11Features(
            episodic_memory=True,
            mood_system=True
        ))
        
        # Save to temp file
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_features.json"
            manager.save_to_file(str(filepath))
            
            # Verify file exists
            assert filepath.exists()
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            assert 'v1_1_features' in data
            assert data['v1_1_features']['episodic_memory'] == True


class TestFeatureDecorator:
    """Test require_feature decorator"""
    
    def test_decorator_blocks_when_disabled(self):
        """Test that decorator blocks execution when feature disabled"""
        manager = FeatureFlagManager()
        manager.set_features(V11Features(episodic_memory=False))
        
        @require_feature('episodic_memory')
        async def test_async_function():
            return "success"
        
        # Should raise error
        with pytest.raises(RuntimeError, match="not enabled"):
            import asyncio
            asyncio.run(test_async_function())
    
    def test_decorator_allows_when_enabled(self):
        """Test that decorator allows execution when feature enabled"""
        manager = FeatureFlagManager()
        manager.set_features(V11Features(episodic_memory=True))
        
        @require_feature('episodic_memory')
        async def test_async_function():
            return "success"
        
        # Should work
        import asyncio
        result = asyncio.run(test_async_function())
        assert result == "success"


class TestConvenienceFunctions:
    """Test module-level convenience functions"""
    
    def test_get_features(self):
        """Test get_features function"""
        FeatureFlagManager.set_features(V11Features(mood_system=True))
        
        features = get_features()
        assert features.mood_system == True
    
    def test_is_enabled(self):
        """Test is_enabled function"""
        FeatureFlagManager.set_features(V11Features(affinity_system=True))
        
        assert is_enabled('affinity_system') == True
        assert is_enabled('episodic_memory') == False


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

