# PROMPT 1.12: Implementar optimizer.py (Integración Completa)

**FASE:** 1 - Quick Wins  
**SEMANA:** 4  
**OBJETIVO:** Integración completa de todos los módulos de optimización

---

## 📋 CONTEXTO

Hemos completado las Semanas 1-3 con todos los módulos individuales funcionando:

**Estado actual:**
- ✅ key_mapping.py (25 tests) - 15-20% reduction
- ✅ minifier.py (26 tests) - +5-8% reduction
- ✅ compact_format.py (32 tests) - +10-15% reduction  
- ✅ deduplicator.py (34 tests) - +5-10% reduction
- ✅ cache.py (35 tests) - 2-5x faster reads
- ✅ ~152 tests passing, 100% coverage

**Problema:**
- Los módulos funcionan independientemente
- No hay una API unificada
- No hay configuración centralizada
- No hay pipeline de optimización completo

**Solución:**
Crear `optimizer.py` que:
- Integra TODOS los módulos en un pipeline coherente
- Proporciona API simple y unificada
- Configuración flexible y centralizada
- Optimization pipeline transparente

---

## 🎯 OBJETIVO

Crear `luminoracore/optimization/optimizer.py` que:
- Clase `Optimizer` que integra todos los módulos
- Clase `OptimizationConfig` para configuración
- Pipeline: key_mapping → minifier → compact_format → deduplicator → cache
- API transparente (compress/expand automático)
- Métricas y estadísticas unificadas

---

## 📦 DEPENDENCIAS

- ✅ key_mapping.py funcionando
- ✅ minifier.py funcionando
- ✅ compact_format.py funcionando
- ✅ deduplicator.py funcionando
- ✅ cache.py funcionando
- ✅ ~152 tests passing

---

## 💡 BENEFICIO ESPERADO

```
Pipeline completo:
├─ key_mapping: 15-20%
├─ minifier: +5-8%
├─ compact_format: +10-15%
├─ deduplicator: +5-10%
└─ cache: 2-5x faster

Total: 45-55% reduction
Performance: 3x faster reads
```

---

## 💻 ESPECIFICACIONES TÉCNICAS

### Crear archivo: `luminoracore/optimization/optimizer.py`

```python
"""
Unified Optimization Layer - Phase 1 Quick Wins
Integrates all optimization modules into a coherent pipeline

This module provides:
- OptimizationConfig: Centralized configuration
- Optimizer: Main optimization orchestrator
- Unified API for all optimizations
- Transparent compression/expansion
- Statistics tracking

Benefits:
- 45-55% total token reduction
- 2-5x faster reads (with cache)
- Simple API for users
- Flexible configuration

Author: LuminoraCore Team
Version: 1.2.0-lite
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import json

from .key_mapping import compress_keys, expand_keys
from .minifier import minify, parse_minified
from .compact_format import CompactFact
from .deduplicator import FactDeduplicator
from .cache import FactCache


@dataclass
class OptimizationConfig:
    """
    Configuration for optimization pipeline
    
    Controls which optimizations are enabled and their parameters.
    """
    
    # Feature flags
    key_abbreviation: bool = True
    minify_json: bool = True
    compact_format: bool = True
    deduplicate_memory: bool = True
    cache_enabled: bool = True
    
    # Cache configuration
    cache_capacity: int = 1000
    cache_ttl_seconds: int = 3600  # 1 hour
    
    # Deduplication config
    auto_deduplicate: bool = True
    preserve_sources: bool = True
    merge_tags: bool = True
    
    # Token budget (for future use)
    max_tokens_per_context: int = 20000
    
    # Backward compatibility
    auto_expand: bool = True  # Expand keys when returning to user
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            'key_abbreviation': self.key_abbreviation,
            'minify_json': self.minify_json,
            'compact_format': self.compact_format,
            'deduplicate_memory': self.deduplicate_memory,
            'cache_enabled': self.cache_enabled,
            'cache_capacity': self.cache_capacity,
            'cache_ttl_seconds': self.cache_ttl_seconds,
            'auto_deduplicate': self.auto_deduplicate,
            'preserve_sources': self.preserve_sources,
            'merge_tags': self.merge_tags,
            'max_tokens_per_context': self.max_tokens_per_context,
            'auto_expand': self.auto_expand
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OptimizationConfig':
        """Create config from dictionary"""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


class Optimizer:
    """
    Main optimization orchestrator
    
    Coordinates all optimization modules in a coherent pipeline.
    Provides simple API for compression and expansion.
    """
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """
        Initialize optimizer with configuration
        
        Args:
            config: Optimization configuration (uses defaults if None)
        """
        self.config = config or OptimizationConfig()
        
        # Initialize cache if enabled
        self.cache = None
        if self.config.cache_enabled:
            self.cache = FactCache(
                capacity=self.config.cache_capacity,
                ttl_seconds=self.config.cache_ttl_seconds
            )
        
        # Initialize deduplicator
        self.deduplicator = FactDeduplicator()
        
        # Statistics tracking
        self.stats = {
            'compressions': 0,
            'expansions': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'total_reduction_bytes': 0,
            'total_reduction_percent': 0.0
        }
    
    def compress(self, data: Dict[str, Any], calculate_stats: bool = True) -> Dict[str, Any]:
        """
        Apply full optimization pipeline to data
        
        Pipeline:
        1. Key abbreviation (if enabled)
        2. Compact format (if enabled)
        3. Minification (if enabled)
        
        Args:
            data: Original fact dictionary
            calculate_stats: Whether to calculate/update statistics
        
        Returns:
            Optimized data (compressed)
        """
        original_size = len(json.dumps(data))
        result = data.copy()
        
        # Step 1: Key abbreviation
        if self.config.key_abbreviation:
            result = compress_keys(result)
        
        # Step 2: Compact format (dict -> array)
        if self.config.compact_format:
            result = CompactFact.to_array(result)
        
        # Step 3: Minification
        # Note: Minification is typically applied when serializing to string
        # Here we return the structure, actual minification happens during JSON dump
        
        # Update stats
        if calculate_stats:
            compressed_size = len(json.dumps(result, separators=(',', ':')))
            self.stats['compressions'] += 1
            self.stats['total_reduction_bytes'] += (original_size - compressed_size)
            if self.stats['compressions'] > 0:
                self.stats['total_reduction_percent'] = (
                    (self.stats['total_reduction_bytes'] / 
                     (original_size * self.stats['compressions'])) * 100
                )
        
        return result
    
    def expand(self, data: Any) -> Dict[str, Any]:
        """
        Reverse optimization pipeline to restore original format
        
        Pipeline (reverse):
        1. Parse minified (if needed)
        2. Array to dict (if compact format)
        3. Expand keys (if abbreviated)
        
        Args:
            data: Compressed data (array or dict)
        
        Returns:
            Original format dictionary
        """
        result = data
        
        # Step 1: If it's an array, convert to dict
        if isinstance(result, list) and self.config.compact_format:
            result = CompactFact.from_array(result)
        
        # Step 2: Expand keys
        if self.config.key_abbreviation and isinstance(result, dict):
            result = expand_keys(result)
        
        self.stats['expansions'] += 1
        
        return result
    
    def compress_batch(self, facts: List[Dict[str, Any]]) -> List[Any]:
        """
        Compress multiple facts
        
        Args:
            facts: List of fact dictionaries
        
        Returns:
            List of compressed facts
        """
        compressed = [self.compress(fact, calculate_stats=False) for fact in facts]
        
        # Deduplicate if enabled
        if self.config.deduplicate_memory and len(compressed) > 1:
            # Convert back to dicts for deduplication
            if self.config.compact_format:
                dict_facts = [CompactFact.from_array(f) if isinstance(f, list) else f 
                             for f in compressed]
            else:
                dict_facts = compressed
            
            # Deduplicate
            deduplicated = self.deduplicator.deduplicate(dict_facts)
            
            # Convert back to compressed format
            compressed = [self.compress(fact, calculate_stats=False) 
                         for fact in deduplicated]
        
        return compressed
    
    def expand_batch(self, compressed_facts: List[Any]) -> List[Dict[str, Any]]:
        """
        Expand multiple facts
        
        Args:
            compressed_facts: List of compressed facts
        
        Returns:
            List of original format dictionaries
        """
        return [self.expand(fact) for fact in compressed_facts]
    
    def get_fact_cached(self, user_id: str, category: Optional[str] = None, 
                        key: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get fact from cache or return None
        
        Args:
            user_id: User ID
            category: Optional category filter
            key: Optional key filter
        
        Returns:
            Fact dictionary if cached, None otherwise
        """
        if not self.cache:
            return None
        
        cached = self.cache.get_fact(user_id, category, key)
        
        if cached:
            self.stats['cache_hits'] += 1
            return self.expand(cached) if self.config.auto_expand else cached
        else:
            self.stats['cache_misses'] += 1
            return None
    
    def put_fact_cache(self, fact: Dict[str, Any]) -> None:
        """
        Store fact in cache
        
        Args:
            fact: Fact dictionary (in original format)
        """
        if not self.cache:
            return
        
        # Compress before caching
        compressed = self.compress(fact)
        
        # Cache uses dict format, convert if needed
        if isinstance(compressed, list):
            compressed = CompactFact.from_array(compressed)
        
        self.cache.put_fact(compressed)
    
    def invalidate_user_cache(self, user_id: str) -> int:
        """
        Invalidate all cached facts for a user
        
        Args:
            user_id: User ID to invalidate
        
        Returns:
            Number of facts invalidated
        """
        if not self.cache:
            return 0
        
        return self.cache.invalidate_user(user_id)
    
    def calculate_reduction(self, original: Any, compressed: Any) -> Dict[str, Any]:
        """
        Calculate reduction statistics
        
        Args:
            original: Original data
            compressed: Compressed data
        
        Returns:
            Statistics dictionary with reduction metrics
        """
        original_size = len(json.dumps(original))
        compressed_size = len(json.dumps(compressed, separators=(',', ':')))
        
        reduction_bytes = original_size - compressed_size
        reduction_percent = (reduction_bytes / original_size * 100) if original_size > 0 else 0
        
        return {
            'original_size_bytes': original_size,
            'compressed_size_bytes': compressed_size,
            'reduction_bytes': reduction_bytes,
            'reduction_percent': round(reduction_percent, 2)
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get optimizer statistics
        
        Returns:
            Dictionary with current statistics
        """
        stats = self.stats.copy()
        
        # Add cache stats if available
        if self.cache:
            cache_stats = self.cache.get_stats()
            stats['cache_stats'] = cache_stats
        
        return stats
    
    def reset_stats(self) -> None:
        """Reset all statistics"""
        self.stats = {
            'compressions': 0,
            'expansions': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'total_reduction_bytes': 0,
            'total_reduction_percent': 0.0
        }
        
        if self.cache:
            # Cache stats reset is handled internally


# Convenience functions
def create_optimizer(config: Optional[Dict[str, Any]] = None) -> Optimizer:
    """
    Create optimizer with configuration
    
    Args:
        config: Configuration dictionary (optional)
    
    Returns:
        Configured Optimizer instance
    """
    if config:
        opt_config = OptimizationConfig.from_dict(config)
    else:
        opt_config = OptimizationConfig()
    
    return Optimizer(opt_config)


# Module exports
__all__ = [
    "Optimizer",
    "OptimizationConfig",
    "create_optimizer"
]
```

---

## ✅ VALIDACIÓN OBLIGATORIA

```bash
# 1. Verificar sintaxis
python -m py_compile luminoracore/optimization/optimizer.py

# 2. Test manual básico
python3 << 'ENDPYTHON'
from luminoracore.optimization.optimizer import Optimizer, OptimizationConfig

# Test 1: Basic compression/expansion
optimizer = Optimizer()
fact = {
    "user_id": "carlos",
    "category": "preferences",
    "key": "favorite_sport",
    "value": "basketball",
    "importance": 0.85
}

compressed = optimizer.compress(fact)
expanded = optimizer.expand(compressed)
print(f"✅ Test 1 - Roundtrip: {expanded == fact}")
assert expanded == fact

# Test 2: Compression reduces size
import json
original_size = len(json.dumps(fact))
compressed_size = len(json.dumps(compressed, separators=(',', ':')))
reduction = ((original_size - compressed_size) / original_size) * 100
print(f"✅ Test 2 - Reduction: {reduction:.1f}%")
assert reduction > 30

# Test 3: Batch operations
facts = [fact.copy() for _ in range(5)]
compressed_batch = optimizer.compress_batch(facts)
expanded_batch = optimizer.expand_batch(compressed_batch)
print(f"✅ Test 3 - Batch: {len(expanded_batch)} facts")
assert len(expanded_batch) == 5

# Test 4: Statistics
stats = optimizer.get_stats()
print(f"✅ Test 4 - Stats compressions: {stats['compressions']}")
assert stats['compressions'] > 0

print("\n🎉 ALL MANUAL TESTS PASSED!")
ENDPYTHON
```

---

## 📋 CRITERIOS DE ÉXITO

- [ ] Archivo creado sin errores
- [ ] Integra todos los módulos correctamente
- [ ] compress() reduce >30% tokens
- [ ] expand() restaura datos originales correctamente
- [ ] Batch operations funcionan
- [ ] Cache integration funciona
- [ ] Statistics tracking correcto
- [ ] Todos los tests manuales pasan

---

## 📧 ACTUALIZAR __init__.py

```bash
# Añadir a luminoracore/optimization/__init__.py:
cat >> luminoracore/optimization/__init__.py << 'EOF'

# optimizer exports
from .optimizer import (
    Optimizer,
    OptimizationConfig,
    create_optimizer
)

__all__.extend([
    "Optimizer",
    "OptimizationConfig",
    "create_optimizer"
])
EOF
```

---

## 🚀 PRÓXIMO PASO

**PROMPT 1.13:** Documentation completa (README.md)

---

## 📊 ESTADO ESPERADO DESPUÉS

```
Módulos optimization:
├─ key_mapping.py ✅
├─ minifier.py ✅
├─ compact_format.py ✅
├─ deduplicator.py ✅
├─ cache.py ✅
└─ optimizer.py ✅ (nuevo - integración)

Tests: ~152 baseline
Siguiente: Integration tests + Documentation
```

---

## 💡 NOTAS IMPORTANTES

**Pipeline de Optimización:**
```python
ENTRADA (Original Fact Dict)
    ↓
1. Key Abbreviation (compress_keys)
    ↓ user_id → uid, category → cat, etc.
2. Compact Format (to_array)
    ↓ Dict → Array
3. Minification (implicit en JSON dump)
    ↓ Remove whitespace
SALIDA (Compressed Data)

REVERSO:
ENTRADA (Compressed Data)
    ↓
1. Array to Dict (from_array)
    ↓
2. Key Expansion (expand_keys)
    ↓
SALIDA (Original Format)
```

**Cache Integration:**
- Cache stores compressed format
- get_fact_cached() auto-expands if configured
- put_fact_cache() auto-compresses before storing
- Cache invalidation by user_id

**Statistics:**
- Tracks compressions/expansions
- Calculates total reduction
- Cache hit/miss rates
- Aggregates across all operations

**Configuration:**
- All features optional (can disable individually)
- Flexible cache settings
- Backward compatibility mode
- Token budget for future use

---

**Documento:** PROMPT_1_12_OPTIMIZER.md  
**Versión:** 1.0  
**Fecha:** 21 Noviembre 2024  
**Estado:** ✅ Listo para implementar
