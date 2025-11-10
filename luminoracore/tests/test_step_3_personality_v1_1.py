"""
Test Step 3: Personality v1.1 Extensions

Validates hierarchical personality and mood system classes
"""

import pytest
from pathlib import Path
import sys

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore.core.personality_v1_1 import (
    AffinityRange,
    ParameterModifiers,
    LinguisticModifiers,
    SystemPromptModifiers,
    LevelModifiers,
    RelationshipLevelConfig,
    MoodConfig,
    HierarchicalConfig,
    MoodSystemConfig,
    PersonalityV11Extensions
)

from luminoracore.core.compiler_v1_1 import DynamicPersonalityCompiler


class TestAffinityRange:
    """Test AffinityRange class"""
    
    def test_valid_range(self):
        """Test creating valid affinity range"""
        range_obj = AffinityRange(0, 20)
        assert range_obj.min_points == 0
        assert range_obj.max_points == 20
    
    def test_contains(self):
        """Test range containment check"""
        range_obj = AffinityRange(0, 20)
        assert range_obj.contains(10) == True
        assert range_obj.contains(25) == False
        assert range_obj.contains(0) == True
        assert range_obj.contains(20) == True
    
    def test_invalid_range(self):
        """Test validation of invalid ranges"""
        with pytest.raises(ValueError):
            AffinityRange(-10, 20)  # Negative min
        
        with pytest.raises(ValueError):
            AffinityRange(0, 150)  # Max > 100
        
        with pytest.raises(ValueError):
            AffinityRange(50, 20)  # Min > max


class TestParameterModifiers:
    """Test ParameterModifiers class"""
    
    def test_apply_modifiers(self):
        """Test applying parameter modifiers"""
        modifiers = ParameterModifiers(empathy=0.2, formality=-0.1)
        base = {"empathy": 0.5, "formality": 0.8}
        
        result = modifiers.apply_to(base)
        
        assert result["empathy"] == pytest.approx(0.7)  # 0.5 + 0.2
        assert result["formality"] == pytest.approx(0.7)  # 0.8 - 0.1
    
    def test_clamp_values(self):
        """Test that values are clamped to [0, 1]"""
        modifiers = ParameterModifiers(empathy=0.8)
        base = {"empathy": 0.5}
        
        result = modifiers.apply_to(base)
        
        assert result["empathy"] == 1.0  # Clamped from 1.3


class TestHierarchicalConfig:
    """Test HierarchicalConfig class"""
    
    def test_from_dict(self):
        """Test creating config from dictionary"""
        data = {
            "enabled": True,
            "relationship_levels": [
                {
                    "name": "stranger",
                    "affinity_range": [0, 20],
                    "description": "Just met",
                    "modifiers": {
                        "advanced_parameters": {"empathy": -0.1},
                        "linguistic_profile": {"tone_additions": ["polite"]},
                        "system_prompt_additions": {"prefix": "You just met. "}
                    }
                }
            ]
        }
        
        config = HierarchicalConfig.from_dict(data)
        
        assert config.enabled == True
        assert len(config.relationship_levels) == 1
        assert config.relationship_levels[0].name == "stranger"
    
    def test_get_level_for_affinity(self):
        """Test getting level for affinity points"""
        data = {
            "enabled": True,
            "relationship_levels": [
                {"name": "stranger", "affinity_range": [0, 20], "modifiers": {}},
                {"name": "friend", "affinity_range": [41, 60], "modifiers": {}}
            ]
        }
        
        config = HierarchicalConfig.from_dict(data)
        
        level = config.get_level_for_affinity(10)
        assert level.name == "stranger"
        
        level = config.get_level_for_affinity(50)
        assert level.name == "friend"
        
        level = config.get_level_for_affinity(30)
        assert level is None  # Gap in ranges


class TestDynamicCompiler:
    """Test DynamicPersonalityCompiler"""
    
    def test_compile_without_modifiers(self):
        """Test compilation with no v1.1 features"""
        base = {
            "persona": {"name": "Alicia"},
            "advanced_parameters": {"empathy": 0.9, "formality": 0.3}
        }
        
        extensions = PersonalityV11Extensions()
        compiler = DynamicPersonalityCompiler(base, extensions)
        
        compiled = compiler.compile()
        
        # Should be identical to base
        assert compiled["advanced_parameters"]["empathy"] == 0.9
        assert compiled["advanced_parameters"]["formality"] == 0.3
    
    def test_compile_with_level_modifiers(self):
        """Test compilation with relationship level"""
        base = {
            "persona": {"name": "Alicia"},
            "advanced_parameters": {"empathy": 0.9, "formality": 0.3},
            "hierarchical_config": {
                "enabled": True,
                "relationship_levels": [
                    {
                        "name": "friend",
                        "affinity_range": [41, 60],
                        "modifiers": {
                            "advanced_parameters": {"empathy": 0.1, "formality": -0.1}
                        }
                    }
                ]
            }
        }
        
        extensions = PersonalityV11Extensions.from_personality_dict(base)
        compiler = DynamicPersonalityCompiler(base, extensions)
        
        compiled = compiler.compile(affinity_points=50)
        
        # Modifiers should be applied
        assert compiled["advanced_parameters"]["empathy"] == pytest.approx(1.0)  # 0.9 + 0.1
        assert compiled["advanced_parameters"]["formality"] == pytest.approx(0.2)  # 0.3 - 0.1
    
    def test_base_unchanged_after_compile(self):
        """Test that base personality is not modified by compilation"""
        base = {
            "advanced_parameters": {"empathy": 0.9}
        }
        
        extensions = PersonalityV11Extensions()
        compiler = DynamicPersonalityCompiler(base, extensions)
        
        # Compile multiple times
        compiler.compile()
        compiler.compile()
        
        # Base should be unchanged
        assert base["advanced_parameters"]["empathy"] == 0.9


class TestPersonalityV11Extensions:
    """Test PersonalityV11Extensions"""
    
    def test_from_v1_0_personality(self):
        """Test extracting extensions from v1.0 personality (no v1.1 features)"""
        personality = {
            "persona": {"name": "Alicia"},
            "advanced_parameters": {}
        }
        
        extensions = PersonalityV11Extensions.from_personality_dict(personality)
        
        assert extensions.is_v1_0_only() == True
        assert extensions.has_hierarchical() == False
        assert extensions.has_moods() == False
    
    def test_from_v1_1_personality(self):
        """Test extracting extensions from v1.1 personality"""
        personality = {
            "persona": {"name": "Alicia"},
            "hierarchical_config": {
                "enabled": True,
                "relationship_levels": []
            }
        }
        
        extensions = PersonalityV11Extensions.from_personality_dict(personality)
        
        assert extensions.has_hierarchical() == True
        assert extensions.is_v1_0_only() == False


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

