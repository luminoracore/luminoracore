# 🚀 FASE 1: Quick Wins - Prompts Detallados Para Cursor AI

**Fase:** 1 de 8  
**Timeline:** 4 Semanas (Semanas 1-4 del roadmap)  
**Objetivo:** Token reduction 25-45% sin breaking changes  
**Complejidad:** 🟢 BAJA  
**ROI:** 🟢 ALTO ($18K/mes ahorro estimado)

---

## 📋 ÍNDICE DE CONTENIDOS

- [RESUMEN EJECUTIVO](#-resumen-ejecutivo)
- [SEMANA 1: Key Mapping + Minifier](#-semana-1-key-mapping--minifier)
- [SEMANA 2: Compact Array Format](#-semana-2-compact-array-format)  
- [SEMANA 3: Deduplication + Caching](#-semana-3-deduplication--caching)
- [SEMANA 4: Integration + Documentation](#-semana-4-integration--documentation)

---

## 🎯 RESUMEN EJECUTIVO

### Contexto

LuminoraCore v1.1 está funcionando pero tiene un problema de costos de tokens. Cada fact usa ~95 tokens en promedio debido a:
- Keys largas (`"user_id"`, `"timestamp"`, etc.)
- Formato JSON verboso con whitespace
- Datos duplicados
- Sin sistema de caché

### Objetivo de Esta Fase

Implementar optimizaciones de "bajo-colgante" (quick wins) que:
- Reduzcan tokens en 25-45%
- No rompan funcionalidad existente (100% backward compatible)
- Se implementen en solo 4 semanas
- Generen ahorro inmediato de costos

### Componentes a Implementar

```
luminoracore/optimization/
├── __init__.py              # Exports del módulo
├── key_mapping.py           # Semana 1 - Día 1-2
├── minifier.py              # Semana 1 - Día 3-5
├── compact_format.py        # Semana 2 - Toda la semana
├── deduplicator.py          # Semana 3 - Día 1-3
└── cache.py                 # Semana 3 - Día 4-5

tests/test_optimization/
├── __init__.py
├── test_key_mapping.py      # Semana 1
├── test_minifier.py         # Semana 1
├── test_compact_format.py   # Semana 2
├── test_deduplicator.py     # Semana 3
└── test_cache.py            # Semana 3
```

### Beneficio Esperado

```
ANTES (v1.1):
- 500 facts × 95 tokens/fact = 47,500 tokens
- Costo: $1.43 por request
- Mensual: $42,900 (@ 1K requests/día)

DESPUÉS (v1.2-lite):
- 500 facts × 55 tokens/fact = 27,500 tokens
- Costo: $0.83 por request
- Mensual: $24,900 (@ 1K requests/día)

AHORRO: $18,000/mes (42% reduction!)
```

---

## 📅 SEMANA 1: Key Mapping + Minifier

**Objetivos:**
- Implementar sistema de abreviación de keys
- Implementar minificación JSON
- Lograr 20-30% token reduction
- 100% tests passing

**Timeline:**
- Días 1-2: `key_mapping.py` + tests
- Días 3-4: `minifier.py` + tests
- Día 5: Integration tests + benchmarks

---

### PROMPT 1.1: Setup del Módulo de Optimization

**CONTEXTO:**  
Estamos iniciando la Fase 1 del roadmap de LuminoraCore. Necesitamos crear la estructura base del nuevo módulo `optimization` que contendrá todas las optimizaciones de tokens.

**OBJETIVO:**  
Crear la estructura de directorios y el `__init__.py` base del módulo de optimization.

**ACCIÓN REQUERIDA:**

1. Crear directorio:
```bash
mkdir -p luminoracore/optimization
```

2. Crear archivo `luminoracore/optimization/__init__.py`:

```python
"""
Optimization Module - LuminoraCore Phase 1 Quick Wins
Token reduction and performance optimizations

This module provides:
- Key abbreviation (key_mapping.py) - Compress JSON keys
- JSON minification (minifier.py) - Remove whitespace  
- Compact array format (compact_format.py) - Dict to array conversion
- Memory deduplication (deduplicator.py) - Merge duplicate facts
- Caching layer (cache.py) - LRU cache for facts

Author: LuminoraCore Team
Version: 1.2.0-lite
Status: Phase 1 - Quick Wins
"""

# Module metadata
__version__ = "1.2.0-lite"
__author__ = "LuminoraCore Team"
__all__ = []  # Se actualizará conforme agregamos módulos

# Placeholders para imports (se agregarán semana a semana)
# from .key_mapping import ...
# from .minifier import ...
# from .compact_format import ...
# from .deduplicator import ...
# from .cache import ...
```

**VALIDACIÓN:**

```bash
# Verificar que se creó correctamente
ls -la luminoracore/optimization/

# Debe mostrar:
# __init__.py

# Verificar que se puede importar
python3 -c "import luminoracore.optimization; print('✅ Import successful')"
```

**CRITERIOS DE ÉXITO:**
- [ ] Directorio `luminoracore/optimization/` existe
- [ ] Archivo `__init__.py` creado
- [ ] No hay errores de sintaxis
- [ ] Se puede importar sin errores

**SI HAY ERRORES:**
- Verifica que estás en el directorio raíz del proyecto
- Verifica que `luminoracore/` existe
- Verifica que hay `__init__.py` en `luminoracore/`

---

### PROMPT 1.2: Implementar key_mapping.py

**CONTEXTO:**  
Los fact dictionaries en LuminoraCore usan keys largas como `"user_id"`, `"timestamp"`, `"category"`, etc. Esto consume muchos tokens. Vamos a crear un sistema de abreviación reversible.

**OBJETIVO:**  
Crear `luminoracore/optimization/key_mapping.py` con funciones para comprimir/expandir keys recursivamente.

**ESPECIFICACIONES TÉCNICAS:**

Crear archivo: `luminoracore/optimization/key_mapping.py`

```python
"""
Key Mapping System - Phase 1 Quick Wins
Compress JSON keys to reduce token usage

This module provides bidirectional key compression:
- compress_keys(): Long keys → short keys
- expand_keys(): Short keys → long keys (lossless)

Example:
    >>> data = {"user_id": "123", "category": "preferences"}
    >>> compressed = compress_keys(data)
    >>> print(compressed)
    {"uid": "123", "cat": "preferences"}
    
    >>> expanded = expand_keys(compressed)  
    >>> print(expanded)
    {"user_id": "123", "category": "preferences"}

Author: LuminoraCore Team
Version: 1.2.0-lite
"""

from typing import Dict, Any, List, Union

# === MAPPING DICTIONARY ===
# Maps long keys to short abbreviations
KEY_MAPPINGS = {
    # User & Identity (3 keys)
    "user_id": "uid",
    "session_id": "sid",
    "conversation_id": "cid",
    
    # Memory Core (5 keys)
    "category": "cat",
    "key": "k",
    "value": "v",
    "importance": "imp",
    "confidence": "conf",
    
    # Temporal (4 keys)
    "timestamp": "ts",
    "created_at": "cr",
    "updated_at": "up",
    "last_accessed": "la",
    
    # Metadata (3 keys)
    "source": "src",
    "tags": "tags",        # Already short
    "metadata": "meta",
    
    # Affinity (3 keys)
    "affinity_score": "aff",
    "affinity_level": "lvl",
    "affinity_points": "pts",
    
    # Episodes (4 keys)
    "episode_id": "eid",
    "episode_title": "title",      # Keep meaningful
    "episode_description": "desc",
    "episode_summary": "sum",
    
    # Categories (9 core categories)
    "preferences": "pref",
    "relationships": "rel",
    "experiences": "exp",
    "goals": "goal",
    "characteristics": "char",
    "knowledge": "know",
    "communication_style": "style",
    "context": "ctx",
    "custom": "cust"
}

# Reverse mapping: short → long
# Generated automatically to ensure consistency
REVERSE_MAPPINGS = {v: k for k, v in KEY_MAPPINGS.items()}


def compress_keys(data: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
    """
    Compress dictionary keys recursively
    
    Replaces long keys with short abbreviations according to KEY_MAPPINGS.
    Unknown keys are preserved as-is. Works recursively on nested structures.
    
    Args:
        data: Dictionary, list, or primitive to compress
        
    Returns:
        Data with compressed keys (same type as input)
        
    Examples:
        >>> compress_keys({"user_id": "123", "category": "preferences"})
        {"uid": "123", "cat": "preferences"}
        
        >>> compress_keys([{"user_id": "1"}, {"user_id": "2"}])
        [{"uid": "1"}, {"uid": "2"}]
        
        >>> compress_keys({"user_id": "123", "metadata": {"source": "chat"}})
        {"uid": "123", "meta": {"src": "chat"}}
    """
    if isinstance(data, dict):
        return {
            KEY_MAPPINGS.get(k, k): compress_keys(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [compress_keys(item) for item in data]
    else:
        # Primitive value (string, int, float, bool, None)
        return data


def expand_keys(data: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
    """
    Expand compressed keys back to original
    
    Reverses the compression done by compress_keys(). Unknown keys are
    preserved as-is. Works recursively on nested structures.
    
    Args:
        data: Dictionary, list, or primitive with compressed keys
        
    Returns:
        Data with original keys restored (same type as input)
        
    Examples:
        >>> expand_keys({"uid": "123", "cat": "preferences"})
        {"user_id": "123", "category": "preferences"}
        
        >>> expand_keys([{"uid": "1"}, {"uid": "2"}])
        [{"user_id": "1"}, {"user_id": "2"}]
        
        >>> expand_keys({"uid": "123", "meta": {"src": "chat"}})
        {"user_id": "123", "metadata": {"source": "chat"}}
    """
    if isinstance(data, dict):
        return {
            REVERSE_MAPPINGS.get(k, k): expand_keys(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [expand_keys(item) for item in data]
    else:
        # Primitive value
        return data


def get_compression_ratio(original: Dict, compressed: Dict) -> float:
    """
    Calculate compression ratio between original and compressed data
    
    Args:
        original: Original dictionary
        compressed: Compressed dictionary
        
    Returns:
        Compression ratio as percentage (0-100)
        Higher percentage = better compression
        
    Example:
        >>> original = {"user_id": "123", "category": "preferences"}
        >>> compressed = {"uid": "123", "cat": "pref"}
        >>> ratio = get_compression_ratio(original, compressed)
        >>> print(f"Reduced by {ratio}%")
        Reduced by 25.5%
    """
    import json
    
    # Calculate sizes using minified JSON (no whitespace)
    original_size = len(json.dumps(original, separators=(',', ':')))
    compressed_size = len(json.dumps(compressed, separators=(',', ':')))
    
    if original_size == 0:
        return 0.0
    
    reduction = ((original_size - compressed_size) / original_size) * 100
    return round(reduction, 2)


# === CONVENIENCE FUNCTIONS FOR BATCH PROCESSING ===

def compress_fact_list(facts: List[Dict]) -> List[Dict]:
    """
    Compress a list of fact dictionaries
    
    Args:
        facts: List of fact dictionaries
        
    Returns:
        List of facts with compressed keys
        
    Example:
        >>> facts = [
        ...     {"user_id": "1", "category": "pref"},
        ...     {"user_id": "2", "category": "goal"}
        ... ]
        >>> compressed = compress_fact_list(facts)
        >>> print(compressed[0])
        {"uid": "1", "cat": "pref"}
    """
    return [compress_keys(fact) for fact in facts]


def expand_fact_list(facts: List[Dict]) -> List[Dict]:
    """
    Expand a list of compressed fact dictionaries
    
    Args:
        facts: List of compressed fact dictionaries
        
    Returns:
        List of facts with original keys
        
    Example:
        >>> compressed = [{"uid": "1", "cat": "pref"}]
        >>> expanded = expand_fact_list(compressed)
        >>> print(expanded[0])
        {"user_id": "1", "category": "pref"}
    """
    return [expand_keys(fact) for fact in facts]


# === MODULE EXPORTS ===
__all__ = [
    "KEY_MAPPINGS",
    "REVERSE_MAPPINGS",
    "compress_keys",
    "expand_keys",
    "get_compression_ratio",
    "compress_fact_list",
    "expand_fact_list"
]
```

**VALIDACIÓN OBLIGATORIA:**

```bash
# 1. Verificar sintaxis
python -m py_compile luminoracore/optimization/key_mapping.py
# Debe completar sin errores

# 2. Test manual en REPL
python3 << 'ENDPYTHON'
from luminoracore.optimization.key_mapping import compress_keys, expand_keys, get_compression_ratio

# Test 1: Compresión básica
original = {"user_id": "carlos", "category": "preferences", "timestamp": "2024-11-18"}
compressed = compress_keys(original)
print(f"✅ Test 1 - Original: {original}")
print(f"✅ Test 1 - Compressed: {compressed}")
assert "uid" in compressed
assert "cat" in compressed
assert "ts" in compressed

# Test 2: Expansión (roundtrip)
expanded = expand_keys(compressed)
print(f"✅ Test 2 - Expanded: {expanded}")
assert expanded == original

# Test 3: Ratio de compresión
ratio = get_compression_ratio(original, compressed)
print(f"✅ Test 3 - Compression ratio: {ratio}%")
assert ratio > 0

# Test 4: Nested dict
nested = {"user_id": "123", "metadata": {"source": "conversation", "confidence": 0.95}}
compressed_nested = compress_keys(nested)
print(f"✅ Test 4 - Nested compressed: {compressed_nested}")
assert compressed_nested["uid"] == "123"
assert "meta" in compressed_nested
assert compressed_nested["meta"]["src"] == "conversation"

# Test 5: List of dicts
fact_list = [
    {"user_id": "1", "category": "pref"},
    {"user_id": "2", "category": "goal"}
]
compressed_list = compress_keys(fact_list)
print(f"✅ Test 5 - List compressed: {compressed_list}")
assert len(compressed_list) == 2
assert compressed_list[0]["uid"] == "1"

print("\n🎉 ALL MANUAL TESTS PASSED!")
ENDPYTHON
```

**CRITERIOS DE ÉXITO:**
- [ ] Archivo creado sin errores de sintaxis
- [ ] `compress_keys()` funciona con dict simple
- [ ] `expand_keys()` restaura dict original (roundtrip)
- [ ] Funciona con nested dicts
- [ ] Funciona con listas de dicts
- [ ] `get_compression_ratio()` calcula correctamente
- [ ] Keys desconocidas se preservan sin cambios
- [ ] Todos los tests manuales pasan

**ACTUALIZAR __init__.py:**

Después de validar que funciona, actualiza `luminoracore/optimization/__init__.py`:

```python
"""
Optimization Module - LuminoraCore Phase 1 Quick Wins
...
"""

# Imports - Semana 1
from .key_mapping import (
    compress_keys,
    expand_keys,
    get_compression_ratio,
    compress_fact_list,
    expand_fact_list,
    KEY_MAPPINGS,
    REVERSE_MAPPINGS
)

__version__ = "1.2.0-lite"
__author__ = "LuminoraCore Team"

__all__ = [
    # key_mapping exports
    "compress_keys",
    "expand_keys",
    "get_compression_ratio",
    "compress_fact_list",
    "expand_fact_list",
    "KEY_MAPPINGS",
    "REVERSE_MAPPINGS"
]
```

**VALIDAR IMPORT:**

```bash
python3 -c "from luminoracore.optimization import compress_keys, expand_keys; print('✅ Import from module successful')"
```

---

### PROMPT 1.3: Tests Para key_mapping.py

**CONTEXTO:**  
Hemos implementado `key_mapping.py`. Ahora necesitamos tests comprehensivos para asegurar que funciona correctamente en todos los casos.

**OBJETIVO:**  
Crear suite completa de tests unitarios para `key_mapping.py`.

**ACCIÓN REQUERIDA:**

1. Crear directorio de tests:
```bash
mkdir -p tests/test_optimization
touch tests/test_optimization/__init__.py
```

2. Crear archivo `tests/test_optimization/test_key_mapping.py`:

```python
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
        
        # Should achieve significant compression
        assert ratio > 20, f"Expected >20% compression, got {ratio}%"
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
```

**VALIDACIÓN:**

```bash
# Ejecutar tests
pytest tests/test_optimization/test_key_mapping.py -v

# Verificar coverage
pytest tests/test_optimization/test_key_mapping.py --cov=luminoracore.optimization.key_mapping --cov-report=term-missing -v

# Ejecutar solo tests rápidos (sin performance tests)
pytest tests/test_optimization/test_key_mapping.py -v -m "not slow"
```

**CRITERIOS DE ÉXITO:**
- [ ] Todos los tests pasan (100%)
- [ ] Coverage ≥ 90%
- [ ] No hay errores de importación
- [ ] Tests de edge cases incluidos
- [ ] Performance tests pasan (opcional)

**OUTPUT ESPERADO:**

```
tests/test_optimization/test_key_mapping.py::TestKeyCompression::test_compress_simple_dict PASSED
tests/test_optimization/test_key_mapping.py::TestKeyCompression::test_expand_simple_dict PASSED
tests/test_optimization/test_key_mapping.py::TestKeyCompression::test_compress_expand_roundtrip PASSED
...
================================ X passed in Y.XXs ================================
```

---

**CONTINÚA EN PARTE 2...**

Este documento continúa con:
- Prompt 1.4: Implementar minifier.py
- Prompt 1.5: Tests para minifier.py
- Semana 2: Compact Array Format
- Semana 3: Deduplication + Caching
- Semana 4: Integration + Documentation

