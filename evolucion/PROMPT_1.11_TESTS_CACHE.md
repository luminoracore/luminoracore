# PROMPT 1.11: Tests Para cache.py

**FASE:** 1 - Quick Wins  
**SEMANA:** 3  
**OBJETIVO:** Test suite completa para cache.py

---

## 📋 CONTEXTO

Hemos implementado cache.py con LRU y TTL. Ahora creamos tests comprehensivos con cobertura ≥90%.

**Estado actual:**
- ✅ cache.py implementado (~250 líneas)
- ✅ Tests manuales pasando (5 tests)
- ✅ 118 tests baseline passing
- ✅ 5 módulos implementados

---

## 🎯 OBJETIVO

Crear `tests/test_optimization/test_cache.py` con ~30 tests que validen:
- LRU operations básicas
- Eviction policy
- TTL expiration
- FactCache specialized operations
- Statistics tracking
- Edge cases

---

## 💻 ESPECIFICACIONES TÉCNICAS

### Crear archivo: `tests/test_optimization/test_cache.py`

```python
"""
Tests for cache.py
Phase 1 - Quick Wins - Semana 3

Test Categories:
- TestLRUCache: Basic LRU operations
- TestTTL: Time-to-live expiration
- TestEviction: Eviction policy
- TestFactCache: Fact-specific caching
- TestStatistics: Cache statistics
- TestConfiguration: CacheConfig
"""

import pytest
import time
from luminoracore.optimization.cache import (
    LRUCache,
    FactCache,
    CacheConfig
)


class TestLRUCache:
    """Test basic LRU cache operations"""
    
    def test_put_and_get(self):
        """Test basic put and get operations"""
        cache = LRUCache(capacity=10)
        
        cache.put("key1", "value1")
        assert cache.get("key1") == "value1"
    
    def test_get_nonexistent_key(self):
        """Test getting non-existent key"""
        cache = LRUCache()
        
        assert cache.get("nonexistent") is None
    
    def test_update_existing_key(self):
        """Test updating existing key"""
        cache = LRUCache()
        
        cache.put("key1", "value1")
        cache.put("key1", "value2")
        
        assert cache.get("key1") == "value2"
    
    def test_cache_size(self):
        """Test cache size tracking"""
        cache = LRUCache(capacity=10)
        
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        
        assert cache.size() == 2
    
    def test_clear_cache(self):
        """Test clearing cache"""
        cache = LRUCache()
        
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.clear()
        
        assert cache.size() == 0
        assert cache.get("key1") is None
    
    def test_remove_key(self):
        """Test removing specific key"""
        cache = LRUCache()
        
        cache.put("key1", "value1")
        cache.remove("key1")
        
        assert cache.get("key1") is None
    
    def test_remove_nonexistent_key(self):
        """Test removing non-existent key doesn't error"""
        cache = LRUCache()
        
        cache.remove("nonexistent")  # Should not raise error
        assert cache.size() == 0


class TestEviction:
    """Test eviction policy"""
    
    def test_capacity_limit(self):
        """Test that cache respects capacity limit"""
        cache = LRUCache(capacity=3)
        
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")
        cache.put("key4", "value4")  # Should evict key1
        
        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"
        assert cache.get("key4") == "value4"
    
    def test_lru_eviction_order(self):
        """Test that least recently used item is evicted"""
        cache = LRUCache(capacity=3)
        
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")
        
        # Access key1 to make it recently used
        cache.get("key1")
        
        # Add new key - should evict key2 (least recently used)
        cache.put("key4", "value4")
        
        assert cache.get("key2") is None
        assert cache.get("key1") == "value1"
    
    def test_eviction_count(self):
        """Test eviction statistics"""
        cache = LRUCache(capacity=2)
        
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")
        
        stats = cache.get_stats()
        assert stats['evictions'] == 1
    
    def test_update_doesnt_evict(self):
        """Test updating existing key doesn't cause eviction"""
        cache = LRUCache(capacity=2)
        
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key1", "value1_updated")  # Update, not new
        
        stats = cache.get_stats()
        assert stats['evictions'] == 0
        assert cache.size() == 2


class TestTTL:
    """Test time-to-live expiration"""
    
    def test_expired_item_returns_none(self):
        """Test that expired items return None"""
        cache = LRUCache(capacity=10, ttl_seconds=1)
        
        cache.put("key1", "value1")
        time.sleep(1.1)
        
        assert cache.get("key1") is None
    
    def test_non_expired_item_accessible(self):
        """Test that non-expired items are accessible"""
        cache = LRUCache(capacity=10, ttl_seconds=2)
        
        cache.put("key1", "value1")
        time.sleep(0.5)
        
        assert cache.get("key1") == "value1"
    
    def test_cleanup_expired(self):
        """Test manual cleanup of expired items"""
        cache = LRUCache(capacity=10, ttl_seconds=1)
        
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        time.sleep(1.1)
        
        removed_count = cache.cleanup_expired()
        
        assert removed_count == 2
        assert cache.size() == 0
    
    def test_expired_removed_on_get(self):
        """Test expired items removed when accessed"""
        cache = LRUCache(capacity=10, ttl_seconds=1)
        
        cache.put("key1", "value1")
        time.sleep(1.1)
        
        # Access should remove expired item
        result = cache.get("key1")
        
        assert result is None
        assert cache.size() == 0
    
    def test_partial_expiration(self):
        """Test that only expired items are removed"""
        cache = LRUCache(capacity=10, ttl_seconds=2)
        
        cache.put("key1", "value1")
        time.sleep(1)
        cache.put("key2", "value2")
        time.sleep(1.1)
        
        # key1 expired, key2 not
        removed = cache.cleanup_expired()
        
        assert removed == 1
        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"


class TestStatistics:
    """Test cache statistics"""
    
    def test_hit_statistics(self):
        """Test cache hit tracking"""
        cache = LRUCache()
        
        cache.put("key1", "value1")
        cache.get("key1")
        cache.get("key1")
        
        stats = cache.get_stats()
        assert stats['hits'] == 2
    
    def test_miss_statistics(self):
        """Test cache miss tracking"""
        cache = LRUCache()
        
        cache.get("nonexistent1")
        cache.get("nonexistent2")
        
        stats = cache.get_stats()
        assert stats['misses'] == 2
    
    def test_hit_rate_calculation(self):
        """Test hit rate percentage calculation"""
        cache = LRUCache()
        
        cache.put("key1", "value1")
        cache.get("key1")  # Hit
        cache.get("key2")  # Miss
        
        stats = cache.get_stats()
        assert stats['hit_rate'] == 50.0
    
    def test_stats_structure(self):
        """Test that stats return all expected fields"""
        cache = LRUCache()
        stats = cache.get_stats()
        
        assert 'size' in stats
        assert 'capacity' in stats
        assert 'hits' in stats
        assert 'misses' in stats
        assert 'evictions' in stats
        assert 'hit_rate' in stats
        assert 'miss_rate' in stats
    
    def test_stats_after_clear(self):
        """Test that clear doesn't reset statistics"""
        cache = LRUCache()
        
        cache.put("key1", "value1")
        cache.get("key1")  # Hit
        cache.clear()
        
        stats = cache.get_stats()
        assert stats['hits'] == 1  # Statistics preserved
        assert stats['size'] == 0  # But cache is empty


class TestFactCache:
    """Test fact-specific caching"""
    
    def test_put_and_get_fact(self):
        """Test caching and retrieving facts"""
        cache = FactCache()
        
        fact = {
            "user_id": "carlos",
            "category": "pref",
            "key": "sport",
            "value": "basketball"
        }
        
        cache.put_fact(fact)
        retrieved = cache.get_fact("carlos", "pref", "sport")
        
        assert retrieved == fact
    
    def test_get_fact_by_user_only(self):
        """Test retrieving fact with only user_id"""
        cache = FactCache()
        
        fact = {"user_id": "carlos", "category": "pref"}
        cache.put_fact(fact)
        
        # Can't retrieve with user_id only if cached with more specificity
        retrieved = cache.get_fact("carlos")
        assert retrieved is None
    
    def test_batch_put_facts(self):
        """Test batch caching of facts"""
        cache = FactCache()
        
        facts = [
            {"user_id": "carlos", "category": "pref", "key": "sport"},
            {"user_id": "maria", "category": "goal", "key": "career"}
        ]
        
        cache.put_facts_batch(facts)
        
        assert cache.get_fact("carlos", "pref", "sport") is not None
        assert cache.get_fact("maria", "goal", "career") is not None
    
    def test_invalidate_user(self):
        """Test invalidating all facts for a user"""
        cache = FactCache()
        
        cache.put_fact({"user_id": "carlos", "category": "pref", "key": "sport"})
        cache.put_fact({"user_id": "carlos", "category": "goal", "key": "career"})
        cache.put_fact({"user_id": "maria", "category": "pref", "key": "food"})
        
        cache.invalidate_user("carlos")
        
        assert cache.get_fact("carlos", "pref", "sport") is None
        assert cache.get_fact("carlos", "goal", "career") is None
        assert cache.get_fact("maria", "pref", "food") is not None
    
    def test_short_keys_support(self):
        """Test that cache handles abbreviated keys"""
        cache = FactCache()
        
        fact = {"uid": "carlos", "cat": "pref", "k": "sport"}
        cache.put_fact(fact)
        
        # Should be retrievable
        assert cache.get_fact("carlos", "pref", "sport") is not None
    
    def test_fact_without_user_id(self):
        """Test that facts without user_id aren't cached"""
        cache = FactCache()
        
        fact = {"category": "pref", "key": "sport"}
        cache.put_fact(fact)
        
        # Should not be cached
        assert cache.cache.size() == 0


class TestConfiguration:
    """Test CacheConfig"""
    
    def test_config_init(self):
        """Test configuration initialization"""
        config = CacheConfig(
            enabled=True,
            capacity=500,
            ttl_seconds=1800,
            auto_cleanup=True,
            cleanup_interval=300
        )
        
        assert config.enabled is True
        assert config.capacity == 500
        assert config.ttl_seconds == 1800
    
    def test_config_defaults(self):
        """Test default configuration values"""
        config = CacheConfig()
        
        assert config.enabled is True
        assert config.capacity == 1000
        assert config.ttl_seconds == 3600


class TestEdgeCases:
    """Test edge cases"""
    
    def test_cache_with_zero_capacity(self):
        """Test cache with zero capacity"""
        cache = LRUCache(capacity=0)
        
        cache.put("key1", "value1")
        
        # Should not cache anything
        assert cache.get("key1") is None
    
    def test_cache_complex_values(self):
        """Test caching complex data structures"""
        cache = LRUCache()
        
        complex_value = {
            "nested": {
                "data": [1, 2, 3],
                "more": {"deep": True}
            }
        }
        
        cache.put("key1", complex_value)
        retrieved = cache.get("key1")
        
        assert retrieved == complex_value
    
    def test_cache_none_value(self):
        """Test caching None as a value"""
        cache = LRUCache()
        
        cache.put("key1", None)
        
        # Should return None but it's cached (not a miss)
        result = cache.get("key1")
        assert result is None
        
        stats = cache.get_stats()
        assert stats['hits'] == 1
        assert stats['misses'] == 0
    
    def test_multiple_gets_update_lru(self):
        """Test that multiple gets update LRU order"""
        cache = LRUCache(capacity=3)
        
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")
        
        # Access key1 multiple times
        cache.get("key1")
        cache.get("key1")
        cache.get("key1")
        
        # Add new key - should evict key2 (not key1)
        cache.put("key4", "value4")
        
        assert cache.get("key1") == "value1"
        assert cache.get("key2") is None
    
    def test_fact_cache_key_generation(self):
        """Test cache key generation for facts"""
        cache = FactCache()
        
        # Test different key combinations
        key1 = cache._make_key("carlos")
        key2 = cache._make_key("carlos", "pref")
        key3 = cache._make_key("carlos", "pref", "sport")
        
        assert key1 == "carlos"
        assert key2 == "carlos:pref"
        assert key3 == "carlos:pref:sport"
        assert key1 != key2 != key3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

---

## ✅ VALIDACIÓN

```bash
# Ejecutar tests
pytest tests/test_optimization/test_cache.py -v

# Verificar coverage
pytest tests/test_optimization/test_cache.py \
  --cov=luminoracore.optimization.cache \
  --cov-report=term-missing -v

# Todos los tests optimization
pytest tests/test_optimization/ -v
```

---

## 📋 CRITERIOS DE ÉXITO

- [ ] Todos los tests pasan (100%)
- [ ] Coverage ≥ 90%
- [ ] LRU policy validada
- [ ] TTL expiration validada
- [ ] FactCache operations validadas
- [ ] Statistics tracking validada

---

## 📊 ESTADO ESPERADO DESPUÉS

```
Tests optimization:
├─ test_key_mapping: 25 tests ✅
├─ test_minifier: 26 tests ✅
├─ test_compact_format: 32 tests ✅
├─ test_deduplicator: 34 tests ✅
├─ test_cache: ~35 tests ✅
└─ Total: ~152 tests passing
```

---

## 🎯 ESTRUCTURA DE TESTS

```
test_cache.py (~35 tests):
├─ TestLRUCache (7 tests)
│  └─ Basic operations
│
├─ TestEviction (5 tests)
│  └─ Capacity & LRU policy
│
├─ TestTTL (5 tests)
│  └─ Expiration logic
│
├─ TestStatistics (5 tests)
│  └─ Hit/miss tracking
│
├─ TestFactCache (6 tests)
│  └─ Fact-specific ops
│
├─ TestConfiguration (2 tests)
│  └─ CacheConfig
│
└─ TestEdgeCases (5 tests)
    └─ Special cases
```

---

## 🚀 PRÓXIMO PASO

**Semana 4:** Integration + Documentation
- PROMPT 1.12: optimizer.py (integración completa)
- PROMPT 1.13: Documentation
- PROMPT 1.14: Migration guide

---

**Documento:** PROMPT_1.11_TESTS_CACHE.md  
**Versión:** 1.0  
**Fecha:** 19 Noviembre 2024  
**Estado:** ✅ Listo para implementar
