"""
Tests for PersonalityValidator class.
"""

import pytest
import json
from pathlib import Path
import tempfile

from luminoracore.core.personality import Personality
from luminoracore.tools.validator import PersonalityValidator, ValidationResult


class TestPersonalityValidator:
    """Test cases for PersonalityValidator class."""
    
    def test_valid_personality(self):
        """Test validation of a valid personality."""
        data = {
            "persona": {
                "name": "Valid Personality",
                "version": "1.0.0",
                "description": "A valid personality for testing",
                "author": "Test Author",
                "tags": ["test", "valid"],
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
                "vocabulary": ["test", "example", "sample", "valid", "data"]
            },
            "behavioral_rules": [
                "Always provide accurate information",
                "Be helpful and supportive",
                "Maintain professional communication"
            ]
        }
        
        validator = PersonalityValidator()
        result = validator.validate(data)
        
        assert result.is_valid
        assert len(result.errors) == 0
    
    def test_invalid_personality_missing_fields(self):
        """Test validation of personality with missing required fields."""
        data = {
            "persona": {
                "name": "Invalid Personality",
                # Missing required fields
            }
        }
        
        validator = PersonalityValidator()
        result = validator.validate(data)
        
        assert not result.is_valid
        assert len(result.errors) > 0
    
    def test_invalid_personality_wrong_types(self):
        """Test validation of personality with wrong data types."""
        data = {
            "persona": {
                "name": "Invalid Personality",
                "version": 1.0,  # Should be string
                "description": "Test personality",
                "author": "Test Author",
                "tags": "test",  # Should be array
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
        
        validator = PersonalityValidator()
        result = validator.validate(data)
        
        assert not result.is_valid
        assert len(result.errors) > 0
    
    def test_validation_with_warnings(self):
        """Test validation that produces warnings."""
        data = {
            "persona": {
                "name": "Warning Test",
                "version": "1.0.0",
                "description": "A",  # Too short
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
                "vocabulary": ["test"]  # Too few vocabulary words
            },
            "behavioral_rules": [
                "Be helpful"  # Too few rules
            ]
        }
        
        validator = PersonalityValidator()
        result = validator.validate(data)
        
        # Should still be valid but with warnings/suggestions
        assert result.is_valid
        assert len(result.warnings) > 0 or len(result.suggestions) > 0
    
    def test_validation_file(self):
        """Test validation of personality file."""
        data = {
            "persona": {
                "name": "File Test",
                "version": "1.0.0",
                "description": "Test personality loaded from file",
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
                "vocabulary": ["test", "file", "validation", "example", "data"]
            },
            "behavioral_rules": [
                "Always be helpful",
                "Provide accurate information",
                "Be respectful"
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        
        try:
            validator = PersonalityValidator()
            result = validator.validate_file(temp_path)
            
            assert result.is_valid
            assert len(result.errors) == 0
        finally:
            Path(temp_path).unlink()
    
    def test_validation_directory(self):
        """Test validation of personality directory."""
        # Create temporary directory with personality files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create valid personality file
            valid_data = {
                "persona": {
                    "name": "Valid Test",
                    "version": "1.0.0",
                    "description": "Valid personality for testing",
                    "author": "Test Author",
                    "tags": ["test", "valid"],
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
                    "vocabulary": ["test", "valid", "data", "example", "sample"]
                },
                "behavioral_rules": [
                    "Always be helpful",
                    "Provide accurate information",
                    "Be respectful"
                ]
            }
            
            valid_file = temp_path / "valid_personality.json"
            with open(valid_file, 'w') as f:
                json.dump(valid_data, f)
            
            # Create invalid personality file
            invalid_data = {
                "persona": {
                    "name": "Invalid Test",
                    # Missing required fields
                }
            }
            
            invalid_file = temp_path / "invalid_personality.json"
            with open(invalid_file, 'w') as f:
                json.dump(invalid_data, f)
            
            validator = PersonalityValidator()
            results = validator.validate_directory(temp_path)
            
            assert len(results) == 2
            assert "valid_personality.json" in results
            assert "invalid_personality.json" in results
            assert results["valid_personality.json"].is_valid
            assert not results["invalid_personality.json"].is_valid
    
    def test_validation_summary(self):
        """Test validation summary generation."""
        # Create mock validation results
        results = {
            "valid1.json": ValidationResult(True, [], ["warning1"], ["suggestion1"]),
            "valid2.json": ValidationResult(True, [], [], []),
            "invalid1.json": ValidationResult(False, ["error1"], [], []),
            "invalid2.json": ValidationResult(False, ["error2", "error3"], ["warning2"], [])
        }
        
        validator = PersonalityValidator()
        summary = validator.get_validation_summary(results)
        
        assert summary["total_files"] == 4
        assert summary["valid_files"] == 2
        assert summary["invalid_files"] == 2
        assert summary["total_errors"] == 3
        assert summary["total_warnings"] == 2
        assert summary["total_suggestions"] == 1
        assert summary["validation_rate"] == 0.5
    
    def test_quality_validation(self):
        """Test quality validation rules."""
        data = {
            "persona": {
                "name": "Quality Test",
                "version": "1.0.0",
                "description": "A test personality with quality issues",
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
                "vocabulary": ["test"]  # Too few vocabulary words
            },
            "behavioral_rules": [
                "Be helpful"  # Too few rules
            ]
        }
        
        validator = PersonalityValidator()
        result = validator.validate(data)
        
        # Should be valid but with suggestions
        assert result.is_valid
        assert len(result.suggestions) > 0
    
    def test_coherence_validation(self):
        """Test coherence validation rules."""
        data = {
            "persona": {
                "name": "Coherence Test",
                "version": "1.0.0",
                "description": "Test personality for coherence validation",
                "author": "Test Author",
                "tags": ["test"],
                "language": "en",
                "compatibility": ["openai"]
            },
            "core_traits": {
                "archetype": "scientist",
                "temperament": "energetic",  # Mismatch with communication style
                "communication_style": "formal"
            },
            "linguistic_profile": {
                "tone": ["professional"],  # Doesn't include "energetic"
                "syntax": "simple",
                "vocabulary": ["test", "data", "science", "research", "analysis"]
            },
            "behavioral_rules": [
                "Always be helpful",
                "Provide accurate information",
                "Be respectful"
            ]
        }
        
        validator = PersonalityValidator()
        result = validator.validate(data)
        
        # Should be valid but with coherence suggestions
        assert result.is_valid
        assert len(result.suggestions) > 0
