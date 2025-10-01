"""
Tests for Personality class.
"""

import pytest
import json
from pathlib import Path
import tempfile

from luminoracore.core.personality import Personality, PersonalityError


class TestPersonality:
    """Test cases for Personality class."""
    
    def test_personality_creation_from_dict(self):
        """Test creating personality from dictionary."""
        data = {
            "persona": {
                "name": "Test Personality",
                "version": "1.0.0",
                "description": "A test personality for unit testing",
                "author": "Test Author",
                "tags": ["test", "unit"],
                "language": "en",
                "compatibility": ["openai", "anthropic"]
            },
            "core_traits": {
                "archetype": "scientist",
                "temperament": "calm",
                "communication_style": "formal"
            },
            "linguistic_profile": {
                "tone": ["professional", "friendly"],
                "syntax": "varied",
                "vocabulary": ["test", "example", "sample"]
            },
            "behavioral_rules": [
                "Always be helpful",
                "Provide accurate information",
                "Be respectful"
            ]
        }
        
        personality = Personality(data)
        
        assert personality.persona.name == "Test Personality"
        assert personality.persona.version == "1.0.0"
        assert personality.core_traits.archetype == "scientist"
        assert personality.linguistic_profile.tone == ["professional", "friendly"]
        assert len(personality.behavioral_rules) == 3
    
    def test_personality_creation_from_file(self):
        """Test creating personality from JSON file."""
        data = {
            "persona": {
                "name": "File Test Personality",
                "version": "1.0.0",
                "description": "A test personality loaded from file",
                "author": "Test Author",
                "tags": ["test", "file"],
                "language": "en",
                "compatibility": ["openai"]
            },
            "core_traits": {
                "archetype": "scientist",
                "temperament": "calm",
                "communication_style": "formal"
            },
            "linguistic_profile": {
                "tone": ["professional"],
                "syntax": "simple",
                "vocabulary": ["test"]
            },
            "behavioral_rules": [
                "Be helpful"
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        
        try:
            personality = Personality(temp_path)
            assert personality.persona.name == "File Test Personality"
            assert personality.persona.version == "1.0.0"
        finally:
            Path(temp_path).unlink()
    
    def test_personality_invalid_data(self):
        """Test creating personality with invalid data."""
        invalid_data = {
            "persona": {
                "name": "Invalid Personality",
                # Missing required fields
            }
        }
        
        with pytest.raises(PersonalityError):
            Personality(invalid_data)
    
    def test_personality_to_dict(self):
        """Test converting personality to dictionary."""
        data = {
            "persona": {
                "name": "Dict Test",
                "version": "1.0.0",
                "description": "Test personality",
                "author": "Test Author",
                "tags": ["test"],
                "language": "en",
                "compatibility": ["openai"]
            },
            "core_traits": {
                "archetype": "scientist",
                "temperament": "calm",
                "communication_style": "formal"
            },
            "linguistic_profile": {
                "tone": ["professional"],
                "syntax": "simple",
                "vocabulary": ["test"]
            },
            "behavioral_rules": [
                "Be helpful"
            ]
        }
        
        personality = Personality(data)
        result_dict = personality.to_dict()
        
        assert result_dict["persona"]["name"] == "Dict Test"
        assert result_dict["core_traits"]["archetype"] == "scientist"
    
    def test_personality_to_json(self):
        """Test converting personality to JSON string."""
        data = {
            "persona": {
                "name": "JSON Test",
                "version": "1.0.0",
                "description": "Test personality",
                "author": "Test Author",
                "tags": ["test"],
                "language": "en",
                "compatibility": ["openai"]
            },
            "core_traits": {
                "archetype": "scientist",
                "temperament": "calm",
                "communication_style": "formal"
            },
            "linguistic_profile": {
                "tone": ["professional"],
                "syntax": "simple",
                "vocabulary": ["test"]
            },
            "behavioral_rules": [
                "Be helpful"
            ]
        }
        
        personality = Personality(data)
        json_str = personality.to_json()
        
        assert '"name": "JSON Test"' in json_str
        assert '"archetype": "scientist"' in json_str
    
    def test_personality_compatibility(self):
        """Test personality compatibility checking."""
        data = {
            "persona": {
                "name": "Compatibility Test",
                "version": "1.0.0",
                "description": "Test personality",
                "author": "Test Author",
                "tags": ["test"],
                "language": "en",
                "compatibility": ["openai", "anthropic", "llama"]
            },
            "core_traits": {
                "archetype": "scientist",
                "temperament": "calm",
                "communication_style": "formal"
            },
            "linguistic_profile": {
                "tone": ["professional"],
                "syntax": "simple",
                "vocabulary": ["test"]
            },
            "behavioral_rules": [
                "Be helpful"
            ]
        }
        
        personality = Personality(data)
        
        assert personality.is_compatible_with("openai")
        assert personality.is_compatible_with("anthropic")
        assert personality.is_compatible_with("llama")
        assert not personality.is_compatible_with("mistral")
    
    def test_personality_tags(self):
        """Test personality tag operations."""
        data = {
            "persona": {
                "name": "Tag Test",
                "version": "1.0.0",
                "description": "Test personality",
                "author": "Test Author",
                "tags": ["test", "unit", "scientist"],
                "language": "en",
                "compatibility": ["openai"]
            },
            "core_traits": {
                "archetype": "scientist",
                "temperament": "calm",
                "communication_style": "formal"
            },
            "linguistic_profile": {
                "tone": ["professional"],
                "syntax": "simple",
                "vocabulary": ["test"]
            },
            "behavioral_rules": [
                "Be helpful"
            ]
        }
        
        personality = Personality(data)
        
        assert personality.has_tag("test")
        assert personality.has_tag("scientist")
        assert not personality.has_tag("nonexistent")
        assert len(personality.get_tags()) == 3
    
    def test_personality_optional_fields(self):
        """Test personality with optional fields."""
        data = {
            "persona": {
                "name": "Optional Test",
                "version": "1.0.0",
                "description": "Test personality with optional fields",
                "author": "Test Author",
                "tags": ["test"],
                "language": "en",
                "compatibility": ["openai"]
            },
            "core_traits": {
                "archetype": "scientist",
                "temperament": "calm",
                "communication_style": "formal"
            },
            "linguistic_profile": {
                "tone": ["professional"],
                "syntax": "simple",
                "vocabulary": ["test"],
                "fillers": ["hmm", "well"],
                "punctuation_style": "moderate"
            },
            "behavioral_rules": [
                "Be helpful"
            ],
            "trigger_responses": {
                "on_greeting": ["Hello!", "Hi there!"],
                "on_confusion": ["I'm not sure I understand."]
            },
            "advanced_parameters": {
                "verbosity": 0.7,
                "formality": 0.8,
                "humor": 0.3
            },
            "safety_guards": {
                "forbidden_topics": ["violence"],
                "content_filters": ["profanity"]
            },
            "examples": {
                "sample_responses": [
                    {
                        "input": "Hello",
                        "output": "Hi there! How can I help?",
                        "context": "greeting"
                    }
                ]
            },
            "metadata": {
                "created_at": "2024-01-01T00:00:00Z",
                "rating": 4.5,
                "license": "MIT"
            }
        }
        
        personality = Personality(data)
        
        # Test optional fields are accessible
        assert personality.trigger_responses is not None
        assert personality.advanced_parameters is not None
        assert personality.safety_guards is not None
        assert personality.examples is not None
        assert personality.metadata is not None
        
        # Test specific values
        assert personality.linguistic_profile.fillers == ["hmm", "well"]
        assert personality.advanced_parameters.verbosity == 0.7
        assert personality.safety_guards.forbidden_topics == ["violence"]
        assert len(personality.examples.sample_responses) == 1
        assert personality.metadata.rating == 4.5
