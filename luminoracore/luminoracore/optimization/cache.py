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

# Default configuration constants
DEFAULT_CACHE_CAPACITY = 1000
DEFAULT_TTL_SECONDS = 3600  # 1 hour
DEFAULT_CLEANUP_INTERVAL = 300  # 5 minutes
CACHE_KEY_SEPARATOR = ":"


class LRUCache:
    """
    Least Recently Used (LRU) cache implementation
    
    Features:
    - Fixed capacity
    - TTL (time-to-live) support
    - Automatic eviction of old/unused items
    - Hit/miss statistics
    """
    
    def __init__(self, capacity: int = DEFAULT_CACHE_CAPACITY, ttl_seconds: int = DEFAULT_TTL_SECONDS):
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
        if len(self.cache) >= self.capacity and self.capacity > 0:
            oldest_key = next(iter(self.cache))
            self.remove(oldest_key)
            self.evictions += 1
        
        # Add new item (only if capacity > 0)
        if self.capacity > 0:
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
    
    def __init__(self, capacity: int = DEFAULT_CACHE_CAPACITY, ttl_seconds: int = DEFAULT_TTL_SECONDS):
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
        return CACHE_KEY_SEPARATOR.join(parts)
    
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
        capacity: int = DEFAULT_CACHE_CAPACITY,
        ttl_seconds: int = DEFAULT_TTL_SECONDS,
        auto_cleanup: bool = True,
        cleanup_interval: int = DEFAULT_CLEANUP_INTERVAL
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

