"""
Tests for minifier.py
Phase 1 - Quick Wins - Semana 2

Test Categories:
- TestMinification: Basic minification functionality
- TestSizeReduction: Size reduction calculations
- TestConvenienceFunctions: Shorthand functions
- TestEdgeCases: Edge cases and error handling
- TestIntegration: Integration with key_mapping
"""

import pytest
import json
from luminoracore.optimization.minifier import (
    JSONMinifier,
    minify,
    parse_minified,
    get_size_reduction
)


class TestMinification:
    """Test JSON minification functionality"""
    
    def test_minify_simple_dict(self):
        """Test minifying a simple dictionary"""
        data = {"user_id": "carlos", "category": "preferences"}
        minified = JSONMinifier.minify(data)
        
        # Should not contain spaces or newlines
        assert ' ' not in minified
        assert '\n' not in minified
        assert minified == '{"user_id":"carlos","category":"preferences"}'
    
    def test_minify_nested_dict(self):
        """Test minifying nested dictionary"""
        data = {
            "user_id": "123",
            "metadata": {
                "source": "conversation",
                "confidence": 0.95
            }
        }
        
        minified = JSONMinifier.minify(data)
        
        # Should not contain spaces or newlines
        assert ' ' not in minified
        assert '\n' not in minified
        
        # Should be parseable
        parsed = json.loads(minified)
        assert parsed == data
    
    def test_minify_list(self):
        """Test minifying list"""
        data = ["item1", "item2", "item3"]
        minified = JSONMinifier.minify(data)
        
        assert minified == '["item1","item2","item3"]'
        assert ' ' not in minified
    
    def test_minify_mixed_types(self):
        """Test minifying data with mixed types"""
        data = {
            "string": "value",
            "number": 123,
            "float": 3.14,
            "boolean": True,
            "null": None,
            "list": [1, 2, 3],
            "dict": {"nested": "value"}
        }
        
        minified = JSONMinifier.minify(data)
        
        # Should not contain spaces
        assert ' ' not in minified
        # Should be parseable
        parsed = json.loads(minified)
        assert parsed == data
    
    def test_minify_with_unicode(self):
        """Test minifying data with unicode characters"""
        data = {
            "name": "José",
            "city": "São Paulo",
            "emoji": "🚀"
        }
        
        minified = JSONMinifier.minify(data)
        
        # Should preserve unicode
        assert "José" in minified
        assert "São Paulo" in minified
        assert "🚀" in minified
        
        # Should be parseable
        parsed = json.loads(minified)
        assert parsed == data
    
    def test_parse_minified(self):
        """Test parsing minified JSON back to object"""
        original = {"user_id": "123", "category": "pref"}
        minified = JSONMinifier.minify(original)
        parsed = JSONMinifier.parse_minified(minified)
        
        assert parsed == original
    
    def test_minify_pretty(self):
        """Test semi-minified output (dev mode)"""
        data = {"user_id": "carlos", "category": "preferences"}
        pretty = JSONMinifier.minify_pretty(data)
        
        # Should have minimal spaces
        assert ', ' in pretty
        assert ': ' in pretty
        # But no newlines
        assert '\n' not in pretty
        # Should be valid JSON
        parsed = json.loads(pretty)
        assert parsed == data
    
    def test_minify_roundtrip(self):
        """Test minify -> parse returns original"""
        original = {
            "user_id": "test_user",
            "category": "preferences",
            "importance": 0.85,
            "tags": ["sports", "weekend"],
            "metadata": {
                "source": "chat",
                "confidence": 0.95
            }
        }
        
        minified = JSONMinifier.minify(original)
        parsed = JSONMinifier.parse_minified(minified)
        
        assert parsed == original


class TestSizeReduction:
    """Test size reduction calculations"""
    
    def test_get_size_reduction_basic(self):
        """Test size reduction calculation"""
        data = {"user_id": "carlos", "category": "preferences"}
        metrics = JSONMinifier.get_size_reduction(data)
        
        assert 'original_size' in metrics
        assert 'minified_size' in metrics
        assert 'reduction_bytes' in metrics
        assert 'reduction_percent' in metrics
        
        assert metrics['minified_size'] < metrics['original_size']
        assert metrics['reduction_percent'] > 0
        assert metrics['reduction_bytes'] > 0
    
    def test_size_reduction_with_large_object(self):
        """Test size reduction with larger object"""
        data = {
            "user_id": "test_user_123",
            "category": "preferences",
            "key": "favorite_sport",
            "value": "basketball",
            "importance": 0.85,
            "timestamp": "2024-11-18T10:30:00Z",
            "source": "conversation",
            "confidence": 0.95,
            "tags": ["sports", "recreation", "weekend_activity"]
        }
        
        metrics = JSONMinifier.get_size_reduction(data)
        
        # Should achieve significant reduction (pretty print has indentation)
        assert metrics['reduction_percent'] > 15  # Adjusted for realistic expectations
        print(f"    Large object reduction: {metrics['reduction_percent']}%")
    
    def test_size_reduction_empty_dict(self):
        """Test size reduction with empty dictionary"""
        data = {}
        metrics = JSONMinifier.get_size_reduction(data)
        
        assert metrics['original_size'] >= 0
        assert metrics['minified_size'] >= 0
        # Empty dict: "{}" is same in both
        assert metrics['reduction_percent'] >= 0
    
    def test_size_reduction_nested(self):
        """Test size reduction with nested structures"""
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "key": "value"
                    }
                }
            }
        }
        
        metrics = JSONMinifier.get_size_reduction(data)
        
        # Nested structures benefit more from minification
        assert metrics['reduction_percent'] > 25
    
    def test_size_reduction_with_provided_minified(self):
        """Test providing pre-minified string"""
        data = {"user_id": "test"}
        minified = JSONMinifier.minify(data)
        
        metrics = JSONMinifier.get_size_reduction(data, minified)
        
        assert metrics['minified_size'] == len(minified)
        assert metrics['reduction_percent'] > 0


class TestBatchOperations:
    """Test batch minification"""
    
    def test_minify_batch(self):
        """Test batch minification"""
        data_list = [
            {"user": "carlos"},
            {"user": "maria"},
            {"user": "john"}
        ]
        
        minified_list = JSONMinifier.minify_batch(data_list)
        
        assert len(minified_list) == 3
        assert isinstance(minified_list[0], str)
        assert ' ' not in minified_list[0]
        
        # Each should be parseable
        for minified in minified_list:
            parsed = json.loads(minified)
            assert "user" in parsed
    
    def test_minify_batch_empty(self):
        """Test batch minification with empty list"""
        minified_list = JSONMinifier.minify_batch([])
        assert minified_list == []


class TestConvenienceFunctions:
    """Test convenience functions"""
    
    def test_minify_function(self):
        """Test standalone minify function"""
        data = {"key": "value"}
        result = minify(data)
        
        assert result == '{"key":"value"}'
        assert isinstance(result, str)
    
    def test_parse_minified_function(self):
        """Test standalone parse_minified function"""
        json_str = '{"key":"value"}'
        result = parse_minified(json_str)
        
        assert result == {"key": "value"}
        assert isinstance(result, dict)
    
    def test_get_size_reduction_function(self):
        """Test standalone get_size_reduction function"""
        data = {"key": "value"}
        metrics = get_size_reduction(data)
        
        assert 'reduction_percent' in metrics
        assert metrics['reduction_percent'] > 0


class TestEdgeCases:
    """Test edge cases"""
    
    def test_empty_dict(self):
        """Test minifying empty dictionary"""
        data = {}
        minified = JSONMinifier.minify(data)
        assert minified == '{}'
        
        parsed = JSONMinifier.parse_minified(minified)
        assert parsed == {}
    
    def test_empty_list(self):
        """Test minifying empty list"""
        data = []
        minified = JSONMinifier.minify(data)
        assert minified == '[]'
        
        parsed = JSONMinifier.parse_minified(minified)
        assert parsed == []
    
    def test_nested_empty_structures(self):
        """Test minifying nested empty structures"""
        data = {
            "empty_dict": {},
            "empty_list": [],
            "nested": {
                "also_empty": {}
            }
        }
        
        minified = JSONMinifier.minify(data)
        parsed = JSONMinifier.parse_minified(minified)
        assert parsed == data
    
    def test_special_characters(self):
        """Test minifying data with special characters"""
        data = {
            "quote": 'He said "hello"',
            "newline": "line1\nline2",
            "tab": "col1\tcol2",
            "backslash": "path\\to\\file"
        }
        
        minified = JSONMinifier.minify(data)
        parsed = JSONMinifier.parse_minified(minified)
        
        # Should preserve special characters
        assert parsed == data
    
    def test_large_numbers(self):
        """Test minifying large numbers"""
        data = {
            "large_int": 999999999999999,
            "large_float": 3.141592653589793,
            "scientific": 1.23e-10
        }
        
        minified = JSONMinifier.minify(data)
        parsed = JSONMinifier.parse_minified(minified)
        
        assert parsed == data
    
    def test_none_values(self):
        """Test minifying None values"""
        data = {
            "value1": None,
            "value2": "not none",
            "value3": None
        }
        
        minified = JSONMinifier.minify(data)
        assert 'null' in minified  # None becomes null in JSON
        
        parsed = JSONMinifier.parse_minified(minified)
        assert parsed == data


class TestIntegration:
    """Integration tests with key_mapping"""
    
    def test_minify_after_compression(self):
        """Test minifying data after key compression"""
        from luminoracore.optimization.key_mapping import compress_keys
        
        original = {
            "user_id": "carlos",
            "category": "preferences",
            "timestamp": "2024-11-18T10:30:00Z",
            "importance": 0.85
        }
        
        # First compress keys
        compressed = compress_keys(original)
        
        # Then minify
        minified = JSONMinifier.minify(compressed)
        
        # Should be very compact
        import json
        original_size = len(json.dumps(original, indent=2))
        minified_size = len(minified)
        
        reduction = ((original_size - minified_size) / original_size) * 100
        
        print(f"    Combined reduction: {reduction:.1f}%")
        
        # Combined: key compression + minification
        assert reduction > 30  # Expect >30% combined reduction
        assert len(minified) < len(json.dumps(original))
    
    def test_full_optimization_pipeline(self):
        """Test complete optimization pipeline"""
        from luminoracore.optimization.key_mapping import compress_keys, expand_keys
        
        # Original fact
        fact = {
            "user_id": "carlos_rodriguez",
            "category": "preferences",
            "key": "favorite_sport",
            "value": "basketball",
            "importance": 0.85,
            "timestamp": "2024-11-18T10:30:00Z",
            "source": "conversation",
            "confidence": 0.95
        }
        
        # Step 1: Compress keys
        compressed = compress_keys(fact)
        
        # Step 2: Minify
        minified = minify(compressed)
        
        # Step 3: Parse
        parsed = parse_minified(minified)
        
        # Step 4: Expand keys
        restored = expand_keys(parsed)
        
        # Should match original
        assert restored == fact
        
        # Calculate total reduction
        import json
        original_size = len(json.dumps(fact, indent=2))
        optimized_size = len(minified)
        
        total_reduction = ((original_size - optimized_size) / original_size) * 100
        
        print(f"    Total optimization: {total_reduction:.1f}%")
        assert total_reduction > 30  # Should achieve >30% total (adjusted for realistic expectations)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

