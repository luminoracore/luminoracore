# PROMPT 1.10: Implementar cache.py

**FASE:** 1 - Quick Wins  
**SEMANA:** 3  
**OBJETIVO:** LRU Cache con TTL para performance boost

---

## 📋 CONTEXTO

Con deduplicación implementada (118 tests passing), ahora agregamos caching para mejorar read performance 2-5x.

**Estado actual:**
- ✅ 4 módulos implementados: key_mapping, minifier, compact_format, deduplicator
- ✅ 118 tests passing (100% coverage en últimos 3 módulos)
- ✅ 45-55% token reduction lograda
- ✅ Sin errores de linting

**Problema:**
- Cada read accede a storage (lento)
- Facts frecuentes se leen repetidamente
- No hay capa de cache entre app y storage

**Solución:**
LRU (Least Recently Used) cache con TTL (Time To Live) que:
- Cache facts frecuentemente accedidos
- Eviction automático de items viejos/no usados
- Hit/miss statistics
- 2-5x faster reads

---

## 🎯 OBJETIVO

Crear `luminoracore/optimization/cache.py` que:
- Implementa LRU cache con capacidad fija
- TTL-based expiration automática
- Cache hit/miss metrics tracking
- Specialized FactCache para facts
- Configuration flexible

---

## 📦 DEPENDENCIAS

- ✅ deduplicator.py funcionando (34 tests)
- ✅ 118 tests baseline passing
- ✅ All modules sin errores

---

## 💡 BENEFICIO ESPERADO

```
Read Performance:
├─ Uncached: ~500ms
├─ Cached: ~150ms
└─ Speedup: 3.3x faster

Cache hit rate target: >60%
Memory overhead: Minimal (~1-2MB @ 1K items)
```

---

## 💻 ESPECIFICACIONES TÉCNICAS

### Crear archivo: `luminoracore/optimization/cache.py`

```python
"""
LRU Cache for Facts - Phase 1 Quick Wins
Intelligent caching layer for frequently accessed facts

Caching strategy:
- LRU (Least Recently Used) eviction policy
- TTL-based expiration
- Size-based limits
- Cache hit/miss metrics

Benefits:
- 2-5x faster reads for cached facts
- Reduced database/storage load
- Better response times

Author: LuminoraCore Team
Version: 1.2.0-lite
"""

from typing import Dict, List, Any, Optional, Tuple
from collections import OrderedDict
import time


class LRUCache:
    """
    Least Recently Used (LRU) cache implementation
    
    Features:
    - Fixed capacity
    - TTL (time-to-live) support
    - Automatic eviction of old/unused items
    - Hit/miss statistics
    """
    
    def __init__(self, capacity: int = 1000, ttl_seconds: int = 3600):
        """
        Initialize LRU cache
        
        Args:
            capacity: Maximum number of items in cache
            ttl_seconds: Time-to-live in seconds (default 1 hour)
            
        Example:
            >>> cache = LRUCache(capacity=100, ttl_seconds=300)
        """
        self.capacity = capacity
        self.ttl_seconds = ttl_seconds
        self.cache: OrderedDict = OrderedDict()
        self.timestamps: Dict[str, float] = {}
        
        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def _is_expired(self, key: str) -> bool:
        """Check if cached item is expired"""
        if key not in self.timestamps:
            return True
        
        age = time.time() - self.timestamps[key]
        return age > self.ttl_seconds
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get item from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
            
        Example:
            >>> cache = LRUCache()
            >>> cache.put("key1", "value1")
            >>> cache.get("key1")
            'value1'
        """
        # Check if key exists
        if key not in self.cache:
            self.misses += 1
            return None
        
        # Check if expired
        if self._is_expired(key):
            self.remove(key)
            self.misses += 1
            return None
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        self.hits += 1
        return self.cache[key]
    
    def put(self, key: str, value: Any) -> None:
        """
        Put item in cache
        
        Args:
            key: Cache key
            value: Value to cache
            
        Example:
            >>> cache = LRUCache()
            >>> cache.put("key1", {"data": "value"})
        """
        # If key exists, update and move to end
        if key in self.cache:
            self.cache.move_to_end(key)
            self.cache[key] = value
            self.timestamps[key] = time.time()
            return
        
        # If at capacity, remove oldest
        if len(self.cache) >= self.capacity:
            oldest_key = next(iter(self.cache))
            self.remove(oldest_key)
            self.evictions += 1
        
        # Add new item
        self.cache[key] = value
        self.timestamps[key] = time.time()
    
    def remove(self, key: str) -> None:
        """Remove item from cache"""
        if key in self.cache:
            del self.cache[key]
        if key in self.timestamps:
            del self.timestamps[key]
    
    def clear(self) -> None:
        """Clear entire cache"""
        self.cache.clear()
        self.timestamps.clear()
        # Don't reset statistics
    
    def size(self) -> int:
        """Get current cache size"""
        return len(self.cache)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with hit rate, miss rate, etc.
            
        Example:
            >>> cache = LRUCache()
            >>> # ... use cache ...
            >>> stats = cache.get_stats()
            >>> print(f"Hit rate: {stats['hit_rate']}%")
        """
        total_requests = self.hits + self.misses
        hit_rate = (
            (self.hits / total_requests * 100)
            if total_requests > 0
            else 0
        )
        miss_rate = 100 - hit_rate
        
        return {
            'size': len(self.cache),
            'capacity': self.capacity,
            'hits': self.hits,
            'misses': self.misses,
            'evictions': self.evictions,
            'total_requests': total_requests,
            'hit_rate': round(hit_rate, 2),
            'miss_rate': round(miss_rate, 2)
        }
    
    def cleanup_expired(self) -> int:
        """
        Remove all expired items
        
        Returns:
            Number of items removed
        """
        expired_keys = [
            key for key in self.cache.keys()
            if self._is_expired(key)
        ]
        
        for key in expired_keys:
            self.remove(key)
        
        return len(expired_keys)


class FactCache:
    """
    Specialized cache for facts
    
    Features:
    - Multiple cache keys per fact (by user_id, category, etc.)
    - Automatic key generation
    - Batch operations
    """
    
    def __init__(self, capacity: int = 1000, ttl_seconds: int = 3600):
        """
        Initialize fact cache
        
        Args:
            capacity: Maximum cache capacity
            ttl_seconds: TTL for cached facts
        """
        self.cache = LRUCache(capacity=capacity, ttl_seconds=ttl_seconds)
    
    @staticmethod
    def _make_key(user_id: str, category: str = None, key: str = None) -> str:
        """Generate cache key from fact components"""
        parts = [user_id]
        if category:
            parts.append(category)
        if key:
            parts.append(key)
        return ":".join(parts)
    
    def get_fact(
        self,
        user_id: str,
        category: str = None,
        key: str = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get cached fact
        
        Args:
            user_id: User ID
            category: Optional category filter
            key: Optional key filter
            
        Returns:
            Cached fact or None
            
        Example:
            >>> cache = FactCache()
            >>> cache.put_fact({"user_id": "carlos", "category": "pref", "key": "sport"})
            >>> fact = cache.get_fact("carlos", "pref", "sport")
        """
        cache_key = self._make_key(user_id, category, key)
        return self.cache.get(cache_key)
    
    def put_fact(self, fact: Dict[str, Any]) -> None:
        """
        Cache a fact
        
        Args:
            fact: Fact dictionary
            
        Example:
            >>> cache = FactCache()
            >>> fact = {"user_id": "carlos", "category": "pref"}
            >>> cache.put_fact(fact)
        """
        # Extract identifiers
        uid = fact.get("user_id") if "user_id" in fact else fact.get("uid")
        cat = fact.get("category") if "category" in fact else fact.get("cat")
        k = fact.get("key") if "key" in fact else fact.get("k")
        
        if not uid:
            return  # Can't cache without user_id
        
        # Cache with full key
        cache_key = self._make_key(uid, cat, k)
        self.cache.put(cache_key, fact)
    
    def put_facts_batch(self, facts: List[Dict[str, Any]]) -> None:
        """Cache multiple facts"""
        for fact in facts:
            self.put_fact(fact)
    
    def invalidate_user(self, user_id: str) -> None:
        """Invalidate all cached facts for a user"""
        # This is expensive - iterate through cache
        keys_to_remove = [
            key for key in self.cache.cache.keys()
            if key.startswith(f"{user_id}:")
        ]
        
        for key in keys_to_remove:
            self.cache.remove(key)
    
    def clear(self) -> None:
        """Clear entire cache"""
        self.cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return self.cache.get_stats()


class CacheConfig:
    """Configuration for caching behavior"""
    
    def __init__(
        self,
        enabled: bool = True,
        capacity: int = 1000,
        ttl_seconds: int = 3600,
        auto_cleanup: bool = True,
        cleanup_interval: int = 300
    ):
        """
        Initialize cache configuration
        
        Args:
            enabled: Whether caching is enabled
            capacity: Maximum cache size
            ttl_seconds: Time-to-live for cached items
            auto_cleanup: Automatically cleanup expired items
            cleanup_interval: Seconds between cleanups
        """
        self.enabled = enabled
        self.capacity = capacity
        self.ttl_seconds = ttl_seconds
        self.auto_cleanup = auto_cleanup
        self.cleanup_interval = cleanup_interval


# Module exports
__all__ = [
    "LRUCache",
    "FactCache",
    "CacheConfig"
]
```

---

## ✅ VALIDACIÓN OBLIGATORIA

```bash
# 1. Verificar sintaxis
python -m py_compile luminoracore/optimization/cache.py

# 2. Test manual básico
python3 << 'ENDPYTHON'
from luminoracore.optimization.cache import LRUCache, FactCache
import time

# Test 1: LRU basic operations
cache = LRUCache(capacity=3, ttl_seconds=2)
cache.put("key1", "value1")
cache.put("key2", "value2")
print(f"✅ Test 1 - Get: {cache.get('key1')}")
assert cache.get("key1") == "value1"

# Test 2: Capacity limit
cache.put("key3", "value3")
cache.put("key4", "value4")  # Should evict key2
print(f"✅ Test 2 - Evicted: {cache.get('key2')}")
assert cache.get("key2") is None

# Test 3: TTL expiration
cache2 = LRUCache(capacity=10, ttl_seconds=1)
cache2.put("expire_me", "value")
time.sleep(1.1)
print(f"✅ Test 3 - Expired: {cache2.get('expire_me')}")
assert cache2.get("expire_me") is None

# Test 4: Fact cache
fact_cache = FactCache()
fact = {"user_id": "carlos", "category": "pref", "key": "sport"}
fact_cache.put_fact(fact)
retrieved = fact_cache.get_fact("carlos", "pref", "sport")
print(f"✅ Test 4 - Fact cached: {retrieved is not None}")
assert retrieved is not None

# Test 5: Statistics
stats = cache.get_stats()
print(f"✅ Test 5 - Hit rate: {stats['hit_rate']}%")
assert 'hit_rate' in stats

print("\n🎉 ALL MANUAL TESTS PASSED!")
ENDPYTHON
```

---

## 📋 CRITERIOS DE ÉXITO

- [ ] Archivo creado sin errores
- [ ] LRU eviction funciona (oldest removed at capacity)
- [ ] TTL expiration funciona (expired items return None)
- [ ] Fact-specific cache funciona
- [ ] Statistics tracking correcto
- [ ] Todos los tests manuales pasan

---

## 🔧 ACTUALIZAR __init__.py

```bash
# Añadir a luminoracore/optimization/__init__.py:
cat >> luminoracore/optimization/__init__.py << 'EOF'

# cache exports
from .cache import (
    LRUCache,
    FactCache,
    CacheConfig
)

__all__.extend([
    "LRUCache",
    "FactCache",
    "CacheConfig"
])
EOF
```

---

## 🚀 PRÓXIMO PASO

**PROMPT 1.11:** Tests para cache.py

---

## 📊 ESTADO ESPERADO DESPUÉS

```
Módulos optimization:
├─ key_mapping.py ✅
├─ minifier.py ✅
├─ compact_format.py ✅
├─ deduplicator.py ✅
└─ cache.py ✅ (nuevo)

Tests:
├─ 118 tests baseline
└─ +tests cache (próximo)
```

---

## 💡 NOTAS IMPORTANTES

**LRU Cache:**
- OrderedDict mantiene orden de inserción
- move_to_end() marca como recientemente usado
- Eviction: remove oldest (first item)

**TTL:**
- Timestamp en cada put()
- Check expiration en cada get()
- cleanup_expired() manual disponible

**FactCache:**
- Cache key format: "user_id:category:key"
- Invalidate by user_id prefix matching
- Batch operations para efficiency

**Performance:**
- O(1) get/put operations
- O(n) invalidate_user (expensive)
- O(n) cleanup_expired

---

**Documento:** PROMPT_1.10_CACHE.md  
**Versión:** 1.0  
**Fecha:** 19 Noviembre 2024  
**Estado:** ✅ Listo para implementar
