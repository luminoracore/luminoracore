"""
Test Step 5: Fact Extraction System

Validates automatic fact extraction from user messages
"""

import pytest
from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore.core.memory.fact_extractor import Fact, FactCategory, FactExtractor


class TestFact:
    """Test Fact dataclass"""
    
    def test_create_valid_fact(self):
        """Test creating valid fact"""
        fact = Fact(
            user_id="user1",
            category="personal_info",
            key="name",
            value="Diego",
            confidence=0.99
        )
        assert fact.user_id == "user1"
        assert fact.confidence == 0.99
    
    def test_invalid_confidence(self):
        """Test validation of confidence"""
        with pytest.raises(ValueError):
            Fact("user1", "personal_info", "name", "Diego", confidence=1.5)
        
        with pytest.raises(ValueError):
            Fact("user1", "personal_info", "name", "Diego", confidence=-0.1)
    
    def test_fact_to_dict(self):
        """Test fact serialization"""
        fact = Fact(
            user_id="user1",
            category="personal_info",
            key="name",
            value="Diego",
            tags=["name", "personal"]
        )
        
        data = fact.to_dict()
        
        assert data["user_id"] == "user1"
        assert data["category"] == "personal_info"
        assert data["key"] == "name"
        assert data["value"] == "Diego"


class TestFactExtractor:
    """Test FactExtractor class"""
    
    def test_build_extraction_prompt(self):
        """Test prompt building"""
        extractor = FactExtractor()
        
        prompt = extractor.build_extraction_prompt("I'm Diego, I'm 28")
        
        assert "Diego" in prompt
        assert "28" in prompt
        assert "Extract factual information" in prompt
    
    def test_parse_llm_response_valid_json(self):
        """Test parsing valid JSON response"""
        extractor = FactExtractor()
        
        response = '''{
            "facts": [
                {"category": "personal_info", "key": "name", "value": "Diego", "confidence": 0.99, "tags": []}
            ]
        }'''
        
        facts_data = extractor.parse_llm_response(response)
        
        assert len(facts_data) == 1
        assert facts_data[0]["key"] == "name"
    
    def test_parse_llm_response_markdown(self):
        """Test parsing JSON in markdown code block"""
        extractor = FactExtractor()
        
        response = '''Here are the facts:
```json
{
    "facts": [
        {"category": "personal_info", "key": "name", "value": "Diego", "confidence": 0.99, "tags": []}
    ]
}
```'''
        
        facts_data = extractor.parse_llm_response(response)
        
        assert len(facts_data) == 1
        assert facts_data[0]["key"] == "name"
    
    def test_filter_by_confidence(self):
        """Test confidence filtering"""
        extractor = FactExtractor(confidence_threshold=0.8)
        
        facts_data = [
            {"key": "fact1", "confidence": 0.9},  # Above threshold
            {"key": "fact2", "confidence": 0.7},  # Below threshold
            {"key": "fact3", "confidence": 0.85}  # Above threshold
        ]
        
        filtered = extractor.filter_by_confidence(facts_data)
        
        assert len(filtered) == 2
        assert filtered[0]["key"] == "fact1"
        assert filtered[1]["key"] == "fact3"
    
    def test_create_fact_objects(self):
        """Test creating Fact objects from data"""
        extractor = FactExtractor()
        
        facts_data = [
            {
                "category": "personal_info",
                "key": "name",
                "value": "Diego",
                "confidence": 0.99,
                "tags": ["name"]
            }
        ]
        
        facts = extractor.create_fact_objects(
            user_id="user1",
            facts_data=facts_data,
            source_message_id="msg123"
        )
        
        assert len(facts) == 1
        assert facts[0].user_id == "user1"
        assert facts[0].key == "name"
        assert facts[0].source_message_id == "msg123"
    
    def test_extract_sync_simple(self):
        """Test synchronous extraction (no LLM)"""
        extractor = FactExtractor()
        
        facts = extractor.extract_sync(
            user_id="user1",
            message="I'm Diego",
            message_id="msg1"
        )
        
        # Should extract at least the name
        assert len(facts) > 0
        name_fact = [f for f in facts if f.key == "name"]
        assert len(name_fact) == 1
        assert name_fact[0].value == "Diego"


class TestFactCategory:
    """Test FactCategory enum"""
    
    def test_all_categories_defined(self):
        """Test that all expected categories are defined"""
        categories = [c.value for c in FactCategory]
        
        assert "personal_info" in categories
        assert "preferences" in categories
        assert "relationships" in categories
        assert "hobbies" in categories
        assert "work" in categories


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

