# PROMPT 1.8: Implementar deduplicator.py

**FASE:** 1 - Quick Wins  
**SEMANA:** 3  
**OBJETIVO:** Deduplication - Merge duplicate facts

---

## 📋 CONTEXTO

Con key_mapping y compact_format tenemos 40-50% token reduction. Ahora eliminamos facts duplicados que consumen espacio innecesario en memoria.

**Estado actual:**
- ✅ key_mapping.py funcionando (25 tests)
- ✅ minifier.py funcionando (26 tests)
- ✅ compact_format.py funcionando (32 tests)
- ✅ 84 tests passing, >35% reduction

**Problema:**
Los facts duplicados ocurren cuando:
1. Usuario menciona la misma información múltiples veces
2. Import desde diferentes fuentes
3. Actualizaciones con valores ligeramente diferentes

**Solución:**
Deduplicator que detecta duplicados y los merge inteligentemente.

---

## 🎯 OBJETIVO

Crear `luminoracore/optimization/deduplicator.py` que:
- Detecta facts duplicados usando fingerprints
- Merge duplicados preservando mejor metadata
- Mantiene tracking de sources
- Logra 5-10% reduction adicional

---

## 📦 DEPENDENCIAS

- ✅ compact_format.py funcionando
- ✅ Tests compact_format passing (32 tests)
- ✅ 84 tests baseline passing

---

## 💡 BENEFICIO ESPERADO

```
ANTES: 500 facts (muchos duplicados)
DESPUÉS: 350 facts (30% menos)

Reduction adicional: 5-10%
Total acumulado: 45-55%
```

---

## 💻 ESPECIFICACIONES TÉCNICAS

### Crear archivo: `luminoracore/optimization/deduplicator.py`

```python
"""
Memory Deduplication - Phase 1 Quick Wins
Detect and merge duplicate facts to reduce memory footprint

Duplicate facts occur when:
1. Same user_id + category + key + value
2. User mentions same information multiple times
3. Import from different sources

This module:
- Detects duplicates using hash-based comparison
- Merges duplicates preserving highest importance/confidence
- Maintains source tracking
- Achieves 5-10% additional memory reduction

Author: LuminoraCore Team
Version: 1.2.0-lite
"""

from typing import Dict, List, Any, Set, Tuple, Optional
import hashlib
import json
from datetime import datetime


class FactDeduplicator:
    """
    Deduplication engine for facts
    
    Detects duplicate facts and merges them intelligently,
    preserving the most important metadata.
    """
    
    @staticmethod
    def get_fact_fingerprint(fact: Dict[str, Any]) -> str:
        """
        Generate unique fingerprint for a fact based on core fields
        
        Core fields: user_id, category, key, value
        (excludes metadata like timestamp, importance, etc.)
        
        Args:
            fact: Fact dictionary
            
        Returns:
            SHA256 hash of core fields
            
        Example:
            >>> fact1 = {"user_id": "carlos", "category": "pref", "key": "sport"}
            >>> fact2 = {"user_id": "carlos", "category": "pref", "key": "sport", "timestamp": "..."}
            >>> FactDeduplicator.get_fact_fingerprint(fact1) == FactDeduplicator.get_fact_fingerprint(fact2)
            True
        """
        # Extract core fields (support both long and short keys)
        uid = fact.get("user_id") if "user_id" in fact else fact.get("uid")
        cat = fact.get("category") if "category" in fact else fact.get("cat")
        key = fact.get("key") if "key" in fact else fact.get("k")
        val = fact.get("value") if "value" in fact else fact.get("v")
        
        # Create canonical representation
        core_data = {
            "user_id": uid,
            "category": cat,
            "key": key,
            "value": val
        }
        
        # Generate hash
        canonical = json.dumps(core_data, sort_keys=True, separators=(',', ':'))
        fingerprint = hashlib.sha256(canonical.encode()).hexdigest()
        
        return fingerprint
    
    @staticmethod
    def merge_duplicates(facts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge duplicate facts into single fact
        
        Merging strategy:
        - Keep highest importance
        - Keep highest confidence
        - Use most recent timestamp
        - Combine sources
        - Merge tags
        
        Args:
            facts: List of duplicate facts
            
        Returns:
            Single merged fact
            
        Example:
            >>> fact1 = {"user_id": "carlos", "importance": 0.7, "timestamp": "2024-11-17"}
            >>> fact2 = {"user_id": "carlos", "importance": 0.9, "timestamp": "2024-11-18"}
            >>> merged = FactDeduplicator.merge_duplicates([fact1, fact2])
            >>> merged["importance"]
            0.9
        """
        if not facts:
            return {}
        
        if len(facts) == 1:
            return facts[0]
        
        # Start with first fact as base
        merged = dict(facts[0])
        
        # Track all sources and tags
        all_sources = set()
        all_tags = set()
        
        # Find best values across all facts
        max_importance = 0.0
        max_confidence = 0.0
        latest_timestamp = None
        
        for fact in facts:
            # Importance
            imp = fact.get("importance") if "importance" in fact else fact.get("imp")
            if imp is not None and imp > max_importance:
                max_importance = imp
            
            # Confidence
            conf = fact.get("confidence") if "confidence" in fact else fact.get("conf")
            if conf is not None and conf > max_confidence:
                max_confidence = conf
            
            # Timestamp
            ts = fact.get("timestamp") if "timestamp" in fact else fact.get("ts")
            if ts:
                if latest_timestamp is None or ts > latest_timestamp:
                    latest_timestamp = ts
            
            # Sources
            src = fact.get("source") if "source" in fact else fact.get("src")
            if src:
                all_sources.add(src)
            
            # Tags
            tags = fact.get("tags", [])
            if tags:
                all_tags.update(tags)
        
        # Update merged fact with best values
        if max_importance > 0:
            merged["importance"] = max_importance
        if max_confidence > 0:
            merged["confidence"] = max_confidence
        if latest_timestamp:
            merged["timestamp"] = latest_timestamp
        if all_sources:
            merged["source"] = ",".join(sorted(all_sources))
        if all_tags:
            merged["tags"] = sorted(list(all_tags))
        
        return merged
    
    @staticmethod
    def deduplicate(facts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Deduplicate a list of facts
        
        Args:
            facts: List of facts (may contain duplicates)
            
        Returns:
            List of unique facts (duplicates merged)
            
        Example:
            >>> facts = [
            ...     {"user_id": "carlos", "category": "pref", "key": "sport", "importance": 0.7},
            ...     {"user_id": "carlos", "category": "pref", "key": "sport", "importance": 0.9},
            ...     {"user_id": "maria", "category": "goal", "key": "career"}
            ... ]
            >>> unique = FactDeduplicator.deduplicate(facts)
            >>> len(unique)
            2
        """
        # Group facts by fingerprint
        groups: Dict[str, List[Dict[str, Any]]] = {}
        
        for fact in facts:
            fingerprint = FactDeduplicator.get_fact_fingerprint(fact)
            if fingerprint not in groups:
                groups[fingerprint] = []
            groups[fingerprint].append(fact)
        
        # Merge each group
        deduplicated = []
        for group_facts in groups.values():
            merged = FactDeduplicator.merge_duplicates(group_facts)
            deduplicated.append(merged)
        
        return deduplicated
    
    @staticmethod
    def get_deduplication_stats(
        original: List[Dict[str, Any]],
        deduplicated: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate deduplication statistics
        
        Args:
            original: Original facts list
            deduplicated: Deduplicated facts list
            
        Returns:
            Statistics dictionary
            
        Example:
            >>> original = [fact1, fact2, fact3]  # 3 facts, 1 duplicate
            >>> deduplicated = FactDeduplicator.deduplicate(original)
            >>> stats = FactDeduplicator.get_deduplication_stats(original, deduplicated)
            >>> stats['reduction_percent']
            33.3
        """
        original_count = len(original)
        deduplicated_count = len(deduplicated)
        removed_count = original_count - deduplicated_count
        
        reduction_percent = (
            (removed_count / original_count * 100)
            if original_count > 0
            else 0
        )
        
        # Calculate size reduction
        original_size = len(json.dumps(original, separators=(',', ':')))
        deduplicated_size = len(json.dumps(deduplicated, separators=(',', ':')))
        size_reduction_bytes = original_size - deduplicated_size
        size_reduction_percent = (
            (size_reduction_bytes / original_size * 100)
            if original_size > 0
            else 0
        )
        
        return {
            'original_count': original_count,
            'deduplicated_count': deduplicated_count,
            'removed_count': removed_count,
            'reduction_percent': round(reduction_percent, 2),
            'original_size_bytes': original_size,
            'deduplicated_size_bytes': deduplicated_size,
            'size_reduction_bytes': size_reduction_bytes,
            'size_reduction_percent': round(size_reduction_percent, 2)
        }


class DeduplicationConfig:
    """Configuration for deduplication behavior"""
    
    def __init__(
        self,
        enabled: bool = True,
        auto_deduplicate: bool = True,
        preserve_sources: bool = True,
        merge_tags: bool = True
    ):
        """
        Initialize deduplication configuration
        
        Args:
            enabled: Whether deduplication is enabled
            auto_deduplicate: Automatically deduplicate on save
            preserve_sources: Preserve all sources when merging
            merge_tags: Merge tags from duplicates
        """
        self.enabled = enabled
        self.auto_deduplicate = auto_deduplicate
        self.preserve_sources = preserve_sources
        self.merge_tags = merge_tags


# Convenience function
def deduplicate_facts(facts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Shorthand for FactDeduplicator.deduplicate()"""
    return FactDeduplicator.deduplicate(facts)


# Module exports
__all__ = [
    "FactDeduplicator",
    "DeduplicationConfig",
    "deduplicate_facts"
]
```

---

## ✅ VALIDACIÓN OBLIGATORIA

```bash
# 1. Verificar sintaxis
python -m py_compile luminoracore/optimization/deduplicator.py

# 2. Test manual básico
python3 << 'ENDPYTHON'
from luminoracore.optimization.deduplicator import FactDeduplicator, deduplicate_facts

# Test 1: Fingerprint generation
fact1 = {"user_id": "carlos", "category": "pref", "key": "sport"}
fact2 = {"user_id": "carlos", "category": "pref", "key": "sport", "timestamp": "2024-11-18"}
fp1 = FactDeduplicator.get_fact_fingerprint(fact1)
fp2 = FactDeduplicator.get_fact_fingerprint(fact2)
print(f"✅ Test 1 - Same fingerprint: {fp1 == fp2}")
assert fp1 == fp2

# Test 2: Merge duplicates
duplicates = [
    {"user_id": "carlos", "importance": 0.7, "timestamp": "2024-11-17"},
    {"user_id": "carlos", "importance": 0.9, "timestamp": "2024-11-18"}
]
merged = FactDeduplicator.merge_duplicates(duplicates)
print(f"✅ Test 2 - Merged importance: {merged['importance']}")
assert merged["importance"] == 0.9

# Test 3: Deduplicate list
facts = [
    {"user_id": "carlos", "category": "pref", "key": "sport", "importance": 0.7},
    {"user_id": "carlos", "category": "pref", "key": "sport", "importance": 0.9},
    {"user_id": "maria", "category": "goal", "key": "career"}
]
unique = deduplicate_facts(facts)
print(f"✅ Test 3 - Deduplicated: {len(facts)} → {len(unique)}")
assert len(unique) == 2

# Test 4: Stats
stats = FactDeduplicator.get_deduplication_stats(facts, unique)
print(f"✅ Test 4 - Reduction: {stats['reduction_percent']}%")
assert stats['removed_count'] == 1

print("\n🎉 ALL MANUAL TESTS PASSED!")
ENDPYTHON
```

---

## 📋 CRITERIOS DE ÉXITO

- [ ] Archivo creado sin errores
- [ ] Fingerprints detectan duplicados correctamente
- [ ] Merge preserva mejor metadata (highest importance, confidence)
- [ ] Merge combina sources y tags
- [ ] Deduplication funciona correctamente
- [ ] Stats calculation es precisa
- [ ] Todos los tests manuales pasan

---

## 🔧 ACTUALIZAR __init__.py

```bash
# Añadir a luminoracore/optimization/__init__.py:
cat >> luminoracore/optimization/__init__.py << 'EOF'

# deduplicator exports
from .deduplicator import (
    FactDeduplicator,
    DeduplicationConfig,
    deduplicate_facts
)

__all__.extend([
    "FactDeduplicator",
    "DeduplicationConfig",
    "deduplicate_facts"
])
EOF
```

---

## 🚀 PRÓXIMO PASO

**PROMPT 1.9:** Tests para deduplicator.py

---

## 📊 ESTADO ESPERADO DESPUÉS

```
Tests optimization:
├─ test_key_mapping: 25 tests ✅
├─ test_minifier: 26 tests ✅
├─ test_compact_format: 32 tests ✅
├─ test_deduplicator: ~25 tests (próximo)
└─ Total: ~108 tests
```

---

**Documento:** PROMPT_1.8_DEDUPLICATOR.md  
**Versión:** 1.0  
**Fecha:** 19 Noviembre 2024  
**Estado:** ✅ Listo para implementar
