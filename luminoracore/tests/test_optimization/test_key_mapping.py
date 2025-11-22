"""
Tests for key_mapping.py
Phase 1 - Quick Wins - Semana 1

Test Categories:
- TestKeyCompression: Basic compression/expansion
- TestMappingDictionaries: Validate KEY_MAPPINGS consistency
- TestEdgeCases: Edge cases and error handling
- TestPerformance: Basic performance checks (optional)
"""

import pytest
from luminoracore.optimization.key_mapping import (
    compress_keys,
    expand_keys,
    get_compression_ratio,
    compress_fact_list,
    expand_fact_list,
    KEY_MAPPINGS,
    REVERSE_MAPPINGS
)


class TestKeyCompression:
    """Test key compression and expansion functionality"""
    
    def test_compress_simple_dict(self):
        """Test compressing a simple dictionary"""
        original = {
            "user_id": "123",
            "category": "preferences",
            "key": "favorite_sport",
            "value": "basketball"
        }
        
        compressed = compress_keys(original)
        
        assert compressed["uid"] == "123"
        assert compressed["cat"] == "preferences"
        assert compressed["k"] == "favorite_sport"
        assert compressed["v"] == "basketball"
        assert len(compressed) == 4
    
    def test_expand_simple_dict(self):
        """Test expanding compressed dictionary"""
        compressed = {
            "uid": "123",
            "cat": "pref",
            "k": "fav_sport",
            "v": "basketball"
        }
        
        expanded = expand_keys(compressed)
        
        assert expanded["user_id"] == "123"
        assert expanded["category"] == "pref"
        assert expanded["key"] == "fav_sport"
        assert expanded["value"] == "basketball"
    
    def test_compress_expand_roundtrip(self):
        """Test that compress -> expand returns original"""
        original = {
            "user_id": "test_user",
            "category": "preferences",
            "timestamp": "2024-11-18T10:30:00Z",
            "importance": 0.85,
            "tags": ["sports", "weekend"]
        }
        
        compressed = compress_keys(original)
        expanded = expand_keys(compressed)
        
        assert expanded == original
    
    def test_compress_nested_dict(self):
        """Test compressing nested dictionaries"""
        original = {
            "user_id": "123",
            "metadata": {
                "source": "conversation",
                "confidence": 0.95,
                "timestamp": "2024-11-18"
            }
        }
        
        compressed = compress_keys(original)
        
        assert compressed["uid"] == "123"
        assert "meta" in compressed
        assert compressed["meta"]["src"] == "conversation"
        assert compressed["meta"]["conf"] == 0.95
        assert compressed["meta"]["ts"] == "2024-11-18"
    
    def test_compress_list_of_dicts(self):
        """Test compressing list of dictionaries"""
        original = [
            {"user_id": "123", "category": "pref"},
            {"user_id": "456", "category": "goal"}
        ]
        
        compressed = compress_keys(original)
        
        assert len(compressed) == 2
        assert compressed[0]["uid"] == "123"
        assert compressed[0]["cat"] == "pref"
        assert compressed[1]["uid"] == "456"
        assert compressed[1]["cat"] == "goal"
    
    def test_unknown_keys_preserved(self):
        """Test that unknown keys are preserved unchanged"""
        original = {
            "user_id": "123",
            "unknown_key": "should_remain",
            "another_unknown": "also_remain"
        }
        
        compressed = compress_keys(original)
        
        assert compressed["uid"] == "123"
        assert compressed["unknown_key"] == "should_remain"
        assert compressed["another_unknown"] == "also_remain"
    
    def test_all_category_keys_compressed(self):
        """Test compression of all 9 core category keys"""
        categories = [
            "preferences", "relationships", "experiences",
            "goals", "characteristics", "knowledge",
            "communication_style", "context", "custom"
        ]
        
        for category in categories:
            original = {"category": category}
            compressed = compress_keys(original)
            # Category value itself doesn't change, key does
            assert "cat" in compressed
            assert compressed["cat"] == category
    
    def test_compression_ratio_calculation(self):
        """Test compression ratio calculation"""
        original = {
            "user_id": "carlos_rodriguez",
            "category": "preferences",
            "timestamp": "2024-11-18T10:30:00Z",
            "importance": 0.85
        }
        
        compressed = compress_keys(original)
        ratio = get_compression_ratio(original, compressed)
        
        assert ratio > 0, "Should have some compression"
        assert ratio < 100, "Should not be 100% compressed"
        assert isinstance(ratio, float)
        # Expect at least 15% reduction for this example
        assert ratio >= 15


class TestBatchOperations:
    """Test batch compression/expansion functions"""
    
    def test_compress_fact_list(self):
        """Test batch compression of fact list"""
        facts = [
            {"user_id": "1", "category": "pref", "key": "sport"},
            {"user_id": "2", "category": "goal", "key": "career"},
            {"user_id": "3", "category": "exp", "key": "travel"}
        ]
        
        compressed = compress_fact_list(facts)
        
        assert len(compressed) == 3
        assert all("uid" in fact for fact in compressed)
        assert all("cat" in fact for fact in compressed)
        assert compressed[0]["uid"] == "1"
        assert compressed[1]["cat"] == "goal"
        assert compressed[2]["k"] == "travel"
    
    def test_expand_fact_list(self):
        """Test batch expansion of fact list"""
        compressed_facts = [
            {"uid": "1", "cat": "pref"},
            {"uid": "2", "cat": "goal"}
        ]
        
        expanded = expand_fact_list(compressed_facts)
        
        assert len(expanded) == 2
        assert all("user_id" in fact for fact in expanded)
        assert all("category" in fact for fact in expanded)
        assert expanded[0]["user_id"] == "1"
        assert expanded[1]["category"] == "goal"
    
    def test_batch_roundtrip(self):
        """Test batch compress -> expand returns original"""
        original_facts = [
            {"user_id": "1", "category": "pref", "timestamp": "2024-11-18"},
            {"user_id": "2", "category": "goal", "importance": 0.9}
        ]
        
        compressed = compress_fact_list(original_facts)
        expanded = expand_fact_list(compressed)
        
        assert expanded == original_facts


class TestMappingDictionaries:
    """Test mapping dictionaries for consistency"""
    
    def test_key_mappings_exists(self):
        """Test that KEY_MAPPINGS is defined"""
        assert KEY_MAPPINGS is not None
        assert isinstance(KEY_MAPPINGS, dict)
        assert len(KEY_MAPPINGS) > 0
    
    def test_reverse_mappings_exists(self):
        """Test that REVERSE_MAPPINGS is defined"""
        assert REVERSE_MAPPINGS is not None
        assert isinstance(REVERSE_MAPPINGS, dict)
        assert len(REVERSE_MAPPINGS) == len(KEY_MAPPINGS)
    
    def test_reverse_mapping_consistency(self):
        """Test that reverse mapping is correct inverse"""
        for long_key, short_key in KEY_MAPPINGS.items():
            assert REVERSE_MAPPINGS[short_key] == long_key
    
    def test_no_mapping_collisions(self):
        """Test that there are no collisions in short keys"""
        short_keys = list(KEY_MAPPINGS.values())
        unique_short_keys = set(short_keys)
        assert len(short_keys) == len(unique_short_keys), \
            "Found duplicate short keys in KEY_MAPPINGS"
    
    def test_mappings_are_shorter(self):
        """Test that abbreviated keys are actually shorter"""
        for long_key, short_key in KEY_MAPPINGS.items():
            # Allow equal length for already-short keys like "tags"
            assert len(short_key) <= len(long_key), \
                f"Short key '{short_key}' is longer than long key '{long_key}'"


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_dict(self):
        """Test compressing empty dictionary"""
        original = {}
        compressed = compress_keys(original)
        assert compressed == {}
        
        expanded = expand_keys(compressed)
        assert expanded == {}
    
    def test_empty_list(self):
        """Test compressing empty list"""
        original = []
        compressed = compress_keys(original)
        assert compressed == []
        
        expanded = expand_keys(compressed)
        assert expanded == []
    
    def test_primitive_values_unchanged(self):
        """Test that primitive values are unchanged"""
        assert compress_keys("string") == "string"
        assert compress_keys(123) == 123
        assert compress_keys(3.14) == 3.14
        assert compress_keys(True) is True
        assert compress_keys(False) is False
        assert compress_keys(None) is None
    
    def test_deeply_nested_structures(self):
        """Test deeply nested structures (3+ levels)"""
        original = {
            "user_id": "123",
            "metadata": {
                "source": "conversation",
                "details": {
                    "timestamp": "2024-11-18",
                    "confidence": 0.95,
                    "tags": ["tag1", "tag2"]
                }
            }
        }
        
        compressed = compress_keys(original)
        expanded = expand_keys(compressed)
        
        assert expanded == original
    
    def test_mixed_types_in_list(self):
        """Test list with mixed types"""
        original = [
            {"user_id": "123"},
            "plain_string",
            42,
            {"category": "pref"}
        ]
        
        compressed = compress_keys(original)
        
        assert compressed[0]["uid"] == "123"
        assert compressed[1] == "plain_string"
        assert compressed[2] == 42
        assert compressed[3]["cat"] == "pref"
    
    def test_none_values_preserved(self):
        """Test that None values are preserved"""
        original = {
            "user_id": "123",
            "value": None,
            "importance": None
        }
        
        compressed = compress_keys(original)
        expanded = expand_keys(compressed)
        
        assert expanded["value"] is None
        assert expanded["importance"] is None
    
    def test_numeric_keys_preserved(self):
        """Test that numeric keys are preserved (not compressed)"""
        # This shouldn't happen in normal use but test anyway
        original = {
            "user_id": "123",
            123: "numeric_key",  # Non-string key
            "category": "pref"
        }
        
        compressed = compress_keys(original)
        
        assert compressed["uid"] == "123"
        assert compressed[123] == "numeric_key"  # Preserved
        assert compressed["cat"] == "pref"


class TestCompressionRatio:
    """Test compression ratio calculations"""
    
    def test_compression_ratio_realistic_fact(self):
        """Test compression ratio with realistic fact"""
        fact = {
            "user_id": "carlos_rodriguez_123",
            "category": "preferences",
            "key": "favorite_sport",
            "value": "basketball",
            "importance": 0.85,
            "timestamp": "2024-11-18T10:30:00Z",
            "source": "conversation",
            "confidence": 0.95,
            "tags": ["sports", "recreation", "weekend"]
        }
        
        compressed = compress_keys(fact)
        ratio = get_compression_ratio(fact, compressed)
        
        # Should achieve significant compression (at least 15% for realistic facts)
        assert ratio > 15, f"Expected >15% compression, got {ratio}%"
        print(f"    Compression ratio: {ratio}%")
    
    def test_compression_ratio_edge_cases(self):
        """Test compression ratio edge cases"""
        # Already short keys
        already_short = {"a": "1", "b": "2"}
        compressed = compress_keys(already_short)
        ratio = get_compression_ratio(already_short, compressed)
        assert ratio >= 0  # No negative compression
        
        # Empty dict
        empty = {}
        compressed_empty = compress_keys(empty)
        ratio_empty = get_compression_ratio(empty, compressed_empty)
        assert ratio_empty == 0.0


# === OPTIONAL PERFORMANCE TESTS ===
class TestPerformance:
    """Optional performance tests (can be slow)"""
    
    @pytest.mark.slow
    def test_large_list_performance(self):
        """Test performance with large list (1000 facts)"""
        import time
        
        # Create 1000 test facts
        large_list = [
            {
                "user_id": f"user_{i}",
                "category": "preferences",
                "key": f"key_{i}",
                "value": f"value_{i}",
                "timestamp": "2024-11-18T10:30:00Z"
            }
            for i in range(1000)
        ]
        
        # Time compression
        start = time.time()
        compressed = compress_fact_list(large_list)
        compress_time = time.time() - start
        
        # Time expansion
        start = time.time()
        expanded = expand_fact_list(compressed)
        expand_time = time.time() - start
        
        # Should be reasonably fast (<1 second for 1000 facts)
        assert compress_time < 1.0, f"Compression too slow: {compress_time}s"
        assert expand_time < 1.0, f"Expansion too slow: {expand_time}s"
        
        print(f"\n    Compressed 1000 facts in {compress_time:.4f}s")
        print(f"    Expanded 1000 facts in {expand_time:.4f}s")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])

