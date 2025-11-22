"""
Tests for deduplicator.py
Phase 1 - Quick Wins - Semana 3

Test Categories:
- TestFingerprinting: Fingerprint generation
- TestMerging: Duplicate merging logic
- TestDeduplication: Full deduplication process
- TestStatistics: Stats calculation
- TestConfiguration: DeduplicationConfig
- TestEdgeCases: Edge cases
"""

import pytest
from luminoracore.optimization.deduplicator import (
    FactDeduplicator,
    DeduplicationConfig,
    deduplicate_facts
)


class TestFingerprinting:
    """Test fingerprint generation"""
    
    def test_same_core_fields_same_fingerprint(self):
        """Facts with same core fields should have same fingerprint"""
        fact1 = {
            "user_id": "carlos",
            "category": "pref",
            "key": "sport",
            "value": "basketball"
        }
        fact2 = {
            "user_id": "carlos",
            "category": "pref",
            "key": "sport",
            "value": "basketball",
            "timestamp": "2024-11-18",
            "importance": 0.85
        }
        
        fp1 = FactDeduplicator.get_fact_fingerprint(fact1)
        fp2 = FactDeduplicator.get_fact_fingerprint(fact2)
        
        assert fp1 == fp2
    
    def test_different_values_different_fingerprint(self):
        """Facts with different values should have different fingerprints"""
        fact1 = {"user_id": "carlos", "category": "pref", "value": "basketball"}
        fact2 = {"user_id": "carlos", "category": "pref", "value": "soccer"}
        
        fp1 = FactDeduplicator.get_fact_fingerprint(fact1)
        fp2 = FactDeduplicator.get_fact_fingerprint(fact2)
        
        assert fp1 != fp2
    
    def test_different_user_different_fingerprint(self):
        """Facts with different users should have different fingerprints"""
        fact1 = {"user_id": "carlos", "category": "pref", "key": "sport"}
        fact2 = {"user_id": "maria", "category": "pref", "key": "sport"}
        
        fp1 = FactDeduplicator.get_fact_fingerprint(fact1)
        fp2 = FactDeduplicator.get_fact_fingerprint(fact2)
        
        assert fp1 != fp2
    
    def test_short_keys_compatibility(self):
        """Should work with abbreviated keys"""
        fact_long = {"user_id": "carlos", "category": "pref", "key": "sport"}
        fact_short = {"uid": "carlos", "cat": "pref", "k": "sport"}
        
        fp1 = FactDeduplicator.get_fact_fingerprint(fact_long)
        fp2 = FactDeduplicator.get_fact_fingerprint(fact_short)
        
        assert fp1 == fp2
    
    def test_fingerprint_is_consistent(self):
        """Same fact should always produce same fingerprint"""
        fact = {"user_id": "carlos", "category": "pref"}
        
        fp1 = FactDeduplicator.get_fact_fingerprint(fact)
        fp2 = FactDeduplicator.get_fact_fingerprint(fact)
        fp3 = FactDeduplicator.get_fact_fingerprint(fact)
        
        assert fp1 == fp2 == fp3
    
    def test_fingerprint_is_hash(self):
        """Fingerprint should be SHA256 hash (64 hex chars)"""
        fact = {"user_id": "carlos", "category": "pref"}
        fp = FactDeduplicator.get_fact_fingerprint(fact)
        
        assert len(fp) == 64
        assert all(c in '0123456789abcdef' for c in fp)


class TestMerging:
    """Test duplicate merging logic"""
    
    def test_merge_keeps_highest_importance(self):
        """Should keep highest importance value"""
        facts = [
            {"user_id": "carlos", "importance": 0.5},
            {"user_id": "carlos", "importance": 0.9},
            {"user_id": "carlos", "importance": 0.7}
        ]
        
        merged = FactDeduplicator.merge_duplicates(facts)
        
        assert merged["importance"] == 0.9
    
    def test_merge_keeps_highest_confidence(self):
        """Should keep highest confidence value"""
        facts = [
            {"user_id": "carlos", "confidence": 0.6},
            {"user_id": "carlos", "confidence": 0.95},
            {"user_id": "carlos", "confidence": 0.8}
        ]
        
        merged = FactDeduplicator.merge_duplicates(facts)
        
        assert merged["confidence"] == 0.95
    
    def test_merge_uses_latest_timestamp(self):
        """Should use most recent timestamp"""
        facts = [
            {"user_id": "carlos", "timestamp": "2024-11-17"},
            {"user_id": "carlos", "timestamp": "2024-11-19"},
            {"user_id": "carlos", "timestamp": "2024-11-18"}
        ]
        
        merged = FactDeduplicator.merge_duplicates(facts)
        
        assert merged["timestamp"] == "2024-11-19"
    
    def test_merge_combines_sources(self):
        """Should combine all sources"""
        facts = [
            {"user_id": "carlos", "source": "conversation"},
            {"user_id": "carlos", "source": "document"},
            {"user_id": "carlos", "source": "api"}
        ]
        
        merged = FactDeduplicator.merge_duplicates(facts)
        
        sources = merged["source"].split(",")
        assert "api" in sources
        assert "conversation" in sources
        assert "document" in sources
        assert len(sources) == 3
    
    def test_merge_combines_tags(self):
        """Should merge all unique tags"""
        facts = [
            {"user_id": "carlos", "tags": ["sports", "hobbies"]},
            {"user_id": "carlos", "tags": ["recreation", "sports"]},
            {"user_id": "carlos", "tags": ["outdoor"]}
        ]
        
        merged = FactDeduplicator.merge_duplicates(facts)
        
        assert set(merged["tags"]) == {"sports", "hobbies", "recreation", "outdoor"}
    
    def test_merge_single_fact(self):
        """Merging single fact should return it unchanged"""
        fact = {"user_id": "carlos", "importance": 0.8}
        
        merged = FactDeduplicator.merge_duplicates([fact])
        
        assert merged == fact
    
    def test_merge_empty_list(self):
        """Merging empty list should return empty dict"""
        merged = FactDeduplicator.merge_duplicates([])
        
        assert merged == {}
    
    def test_merge_preserves_core_fields(self):
        """Merge should preserve core fields from base fact"""
        facts = [
            {"user_id": "carlos", "category": "pref", "key": "sport", "importance": 0.7},
            {"user_id": "carlos", "category": "pref", "key": "sport", "importance": 0.9}
        ]
        
        merged = FactDeduplicator.merge_duplicates(facts)
        
        assert merged["user_id"] == "carlos"
        assert merged["category"] == "pref"
        assert merged["key"] == "sport"
    
    def test_merge_with_short_keys(self):
        """Should handle abbreviated keys"""
        facts = [
            {"uid": "carlos", "imp": 0.5},
            {"uid": "carlos", "imp": 0.9}
        ]
        
        merged = FactDeduplicator.merge_duplicates(facts)
        
        assert merged["importance"] == 0.9


class TestDeduplication:
    """Test full deduplication process"""
    
    def test_deduplicate_basic(self):
        """Should remove duplicate facts"""
        facts = [
            {"user_id": "carlos", "category": "pref", "key": "sport", "importance": 0.7},
            {"user_id": "carlos", "category": "pref", "key": "sport", "importance": 0.9},
            {"user_id": "maria", "category": "goal", "key": "career"}
        ]
        
        unique = FactDeduplicator.deduplicate(facts)
        
        assert len(unique) == 2
    
    def test_deduplicate_no_duplicates(self):
        """Should handle list with no duplicates"""
        facts = [
            {"user_id": "carlos", "category": "pref", "key": "sport"},
            {"user_id": "maria", "category": "goal", "key": "career"},
            {"user_id": "john", "category": "exp", "key": "travel"}
        ]
        
        unique = FactDeduplicator.deduplicate(facts)
        
        assert len(unique) == 3
    
    def test_deduplicate_all_duplicates(self):
        """Should handle all duplicates"""
        facts = [
            {"user_id": "carlos", "category": "pref", "key": "sport", "importance": 0.5},
            {"user_id": "carlos", "category": "pref", "key": "sport", "importance": 0.7},
            {"user_id": "carlos", "category": "pref", "key": "sport", "importance": 0.9}
        ]
        
        unique = FactDeduplicator.deduplicate(facts)
        
        assert len(unique) == 1
        assert unique[0]["importance"] == 0.9
    
    def test_deduplicate_empty_list(self):
        """Should handle empty list"""
        unique = FactDeduplicator.deduplicate([])
        
        assert unique == []
    
    def test_deduplicate_preserves_unique_facts(self):
        """Should preserve all unique facts"""
        facts = [
            {"user_id": "carlos", "category": "pref", "key": "sport"},
            {"user_id": "carlos", "category": "pref", "key": "food"},
            {"user_id": "maria", "category": "goal", "key": "career"}
        ]
        
        unique = FactDeduplicator.deduplicate(facts)
        
        assert len(unique) == 3
    
    def test_deduplicate_multiple_duplicate_groups(self):
        """Should handle multiple groups of duplicates"""
        facts = [
            {"user_id": "carlos", "category": "pref", "key": "sport", "importance": 0.7},
            {"user_id": "carlos", "category": "pref", "key": "sport", "importance": 0.9},
            {"user_id": "maria", "category": "goal", "key": "career", "importance": 0.8},
            {"user_id": "maria", "category": "goal", "key": "career", "importance": 0.95}
        ]
        
        unique = FactDeduplicator.deduplicate(facts)
        
        assert len(unique) == 2
        # Find carlos and maria facts
        carlos_fact = next(f for f in unique if f.get("user_id") == "carlos")
        maria_fact = next(f for f in unique if f.get("user_id") == "maria")
        
        assert carlos_fact["importance"] == 0.9
        assert maria_fact["importance"] == 0.95


class TestStatistics:
    """Test statistics calculation"""
    
    def test_stats_calculation(self):
        """Should calculate correct statistics"""
        original = [
            {"user_id": "carlos", "category": "pref", "key": "sport"},
            {"user_id": "carlos", "category": "pref", "key": "sport"},
            {"user_id": "maria", "category": "goal", "key": "career"}
        ]
        deduplicated = FactDeduplicator.deduplicate(original)
        
        stats = FactDeduplicator.get_deduplication_stats(original, deduplicated)
        
        assert stats['original_count'] == 3
        assert stats['deduplicated_count'] == 2
        assert stats['removed_count'] == 1
        assert stats['reduction_percent'] == pytest.approx(33.33, rel=0.1)
    
    def test_stats_no_duplicates(self):
        """Should handle case with no duplicates"""
        facts = [
            {"user_id": "carlos", "category": "pref"},
            {"user_id": "maria", "category": "goal"}
        ]
        
        stats = FactDeduplicator.get_deduplication_stats(facts, facts)
        
        assert stats['removed_count'] == 0
        assert stats['reduction_percent'] == 0
    
    def test_stats_size_reduction(self):
        """Should calculate size reduction"""
        original = [
            {"user_id": "carlos", "category": "pref"},
            {"user_id": "carlos", "category": "pref"}
        ]
        deduplicated = [{"user_id": "carlos", "category": "pref"}]
        
        stats = FactDeduplicator.get_deduplication_stats(original, deduplicated)
        
        assert stats['size_reduction_bytes'] > 0
        assert stats['size_reduction_percent'] > 0
    
    def test_stats_all_duplicates(self):
        """Should handle 100% duplicates"""
        original = [
            {"user_id": "carlos", "category": "pref"},
            {"user_id": "carlos", "category": "pref"},
            {"user_id": "carlos", "category": "pref"}
        ]
        deduplicated = FactDeduplicator.deduplicate(original)
        
        stats = FactDeduplicator.get_deduplication_stats(original, deduplicated)
        
        assert stats['reduction_percent'] == pytest.approx(66.67, rel=0.1)


class TestConfiguration:
    """Test DeduplicationConfig"""
    
    def test_config_init(self):
        """Test configuration initialization"""
        config = DeduplicationConfig(
            enabled=True,
            auto_deduplicate=True,
            preserve_sources=True,
            merge_tags=True
        )
        
        assert config.enabled is True
        assert config.auto_deduplicate is True
        assert config.preserve_sources is True
        assert config.merge_tags is True
    
    def test_config_defaults(self):
        """Test default configuration values"""
        config = DeduplicationConfig()
        
        assert config.enabled is True
        assert config.auto_deduplicate is True
        assert config.preserve_sources is True
        assert config.merge_tags is True


class TestConvenienceFunction:
    """Test convenience function"""
    
    def test_deduplicate_facts_function(self):
        """Test deduplicate_facts shorthand"""
        facts = [
            {"user_id": "carlos", "category": "pref", "key": "sport"},
            {"user_id": "carlos", "category": "pref", "key": "sport"}
        ]
        
        unique = deduplicate_facts(facts)
        
        assert len(unique) == 1


class TestEdgeCases:
    """Test edge cases"""
    
    def test_partial_metadata(self):
        """Should handle facts with partial metadata"""
        facts = [
            {"user_id": "carlos", "importance": 0.8},
            {"user_id": "carlos"}
        ]
        
        merged = FactDeduplicator.merge_duplicates(facts)
        
        assert merged["importance"] == 0.8
    
    def test_mixed_key_formats(self):
        """Should handle mixed long/short key formats"""
        facts = [
            {"user_id": "carlos", "category": "pref", "importance": 0.7},
            {"uid": "carlos", "cat": "pref", "imp": 0.9}
        ]
        
        unique = FactDeduplicator.deduplicate(facts)
        
        assert len(unique) == 1
        # Should keep highest importance
        result = unique[0]
        imp = result.get("importance") or result.get("imp")
        assert imp == 0.9
    
    def test_none_values_in_core_fields(self):
        """Should handle None values in core fields"""
        fact1 = {"user_id": "carlos", "category": None, "key": "sport"}
        fact2 = {"user_id": "carlos", "category": None, "key": "food"}
        
        fp1 = FactDeduplicator.get_fact_fingerprint(fact1)
        fp2 = FactDeduplicator.get_fact_fingerprint(fact2)
        
        # Different keys should produce different fingerprints
        assert fp1 != fp2
    
    def test_empty_tags_list(self):
        """Should handle empty tags list"""
        facts = [
            {"user_id": "carlos", "tags": []},
            {"user_id": "carlos", "tags": ["sport"]}
        ]
        
        merged = FactDeduplicator.merge_duplicates(facts)
        
        assert "sport" in merged["tags"]
    
    def test_duplicate_tags_in_merge(self):
        """Should deduplicate tags when merging"""
        facts = [
            {"user_id": "carlos", "tags": ["sport", "hobby"]},
            {"user_id": "carlos", "tags": ["sport", "recreation"]}
        ]
        
        merged = FactDeduplicator.merge_duplicates(facts)
        
        # Should have 3 unique tags, not 4
        assert len(merged["tags"]) == 3
        assert set(merged["tags"]) == {"sport", "hobby", "recreation"}
    
    def test_special_characters_in_values(self):
        """Should handle special characters in values"""
        fact1 = {"user_id": "carlos", "value": "test@email.com"}
        fact2 = {"user_id": "carlos", "value": "test@email.com"}
        
        fp1 = FactDeduplicator.get_fact_fingerprint(fact1)
        fp2 = FactDeduplicator.get_fact_fingerprint(fact2)
        
        assert fp1 == fp2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

