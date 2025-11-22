# ðŸš€ FASE 1: Quick Wins PART 2 - Prompts Detallados Para Cursor AI

**Fase:** 1 de 8  
**Timeline:** Semanas 2-4 (continuaciÃ³n)  
**Objetivo:** Completar token reduction 25-45% sin breaking changes  
**Complejidad:** ðŸŸ¢ BAJA  
**Estado:** ðŸ“ Listo para implementar

---

## ðŸ“‹ ÃNDICE DE CONTENIDOS

- [CONTEXTO - DÃ³nde Estamos](#-contexto---dÃ³nde-estamos)
- [SEMANA 2: Compact Array Format](#-semana-2-compact-array-format)
- [SEMANA 3: Deduplication + Caching](#-semana-3-deduplication--caching)
- [SEMANA 4: Integration + Documentation](#-semana-4-integration--documentation)
- [VALIDACIÃ“N FINAL](#-validaciÃ³n-final)

---

## ðŸŽ¯ CONTEXTO - DÃ³nde Estamos

### âœ… Ya Completado (Part 1):

```
Semana 1:
â”œâ”€ âœ… optimization/ module creado
â”œâ”€ âœ… key_mapping.py implementado (200+ lÃ­neas)
â”œâ”€ âœ… Tests key_mapping (25 tests, 96% coverage)
â””â”€ âœ… 15-20% token reduction lograda
```

### ðŸ”„ Por Completar (Part 2):

```
Semana 2:
â”œâ”€ minifier.py + tests
â”œâ”€ compact_format.py + tests
â””â”€ +10-15% reduction adicional

Semana 3:
â”œâ”€ deduplicator.py + tests
â”œâ”€ cache.py + tests
â””â”€ +5-10% reduction adicional

Semana 4:
â”œâ”€ Integration completa
â”œâ”€ Documentation
â”œâ”€ Migration guide
â””â”€ v1.2-lite Release
```

### ðŸŽ¯ Meta Final:
```
TOTAL: 25-45% token reduction
AHORRO: $18K/mes @ 1K requests/dÃ­a
```

---

## ðŸ“… SEMANA 2: Compact Array Format

**Objetivos:**
- Implementar minifier.py (JSON minification)
- Implementar compact_format.py (dict â†’ array conversion)
- Lograr +10-15% token reduction adicional
- 100% tests passing

**Timeline:**
- DÃ­as 6-7: minifier.py + tests
- DÃ­as 8-10: compact_format.py + tests

---

### PROMPT 1.4: Implementar minifier.py

**CONTEXTO:**  
Tenemos key_mapping.py funcionando (15-20% reduction). Ahora agregamos minificaciÃ³n JSON para eliminar whitespace y reducir aÃºn mÃ¡s tokens.

**OBJETIVO:**  
Crear `luminoracore/optimization/minifier.py` con funciones para minificar JSON y calcular savings.

**DEPENDENCIAS:**
- âœ… key_mapping.py funcionando
- âœ… Tests key_mapping passing

**ESPECIFICACIONES TÃ‰CNICAS:**

Crear archivo: `luminoracore/optimization/minifier.py`

```python
"""
JSON Minifier - Phase 1 Quick Wins
Remove unnecessary whitespace and formatting to reduce token usage

This module provides JSON minification:
- Remove all whitespace (spaces, newlines, indentation)
- Use compact separators
- UTF-8 encoding for minimal size
- Optional "pretty" mode for development

Example:
    >>> data = {"user_id": "carlos", "category": "preferences"}
    >>> minified = minify(data)
    >>> print(minified)
    {"user_id":"carlos","category":"preferences"}
    
    >>> # vs standard pretty print:
    >>> import json
    >>> print(json.dumps(data, indent=2))
    {
      "user_id": "carlos",
      "category": "preferences"
    }
    
    >>> # Size difference: 45 chars vs 58 chars (22% smaller)

Author: LuminoraCore Team
Version: 1.2.0-lite
"""

import json
from typing import Dict, Any, List, Union


class JSONMinifier:
    """
    JSON minification utility
    
    Provides methods to minify JSON data by removing unnecessary
    whitespace and formatting. Useful for reducing token count when
    sending data to LLMs.
    """
    
    @staticmethod
    def minify(data: Union[Dict, List, Any]) -> str:
        """
        Convert data to minified JSON string
        
        Removes all unnecessary whitespace, newlines, and indentation.
        Uses compact separators and UTF-8 encoding.
        
        Args:
            data: Dictionary, list, or any JSON-serializable data
            
        Returns:
            Minified JSON string with no spaces or newlines
            
        Examples:
            >>> data = {"key": "value", "number": 123}
            >>> minified = JSONMinifier.minify(data)
            >>> print(minified)
            {"key":"value","number":123}
            
            >>> # Nested data
            >>> data = {"user": {"name": "carlos", "age": 30}}
            >>> minified = JSONMinifier.minify(data)
            >>> print(minified)
            {"user":{"name":"carlos","age":30}}
        """
        return json.dumps(
            data,
            separators=(',', ':'),  # No spaces after commas or colons
            ensure_ascii=False       # Use UTF-8 instead of ASCII escapes
        )
    
    @staticmethod
    def minify_pretty(data: Union[Dict, List, Any]) -> str:
        """
        Minify but keep minimal readability (development mode)
        
        Removes newlines and indentation but keeps single spaces
        after separators for better readability during development.
        
        Args:
            data: Dictionary, list, or any JSON-serializable data
            
        Returns:
            Semi-minified JSON string with minimal spaces
            
        Example:
            >>> data = {"key": "value", "number": 123}
            >>> pretty = JSONMinifier.minify_pretty(data)
            >>> print(pretty)
            {"key": "value", "number": 123}
        """
        return json.dumps(
            data,
            separators=(', ', ': '),  # Single space after separators
            ensure_ascii=False
        )
    
    @staticmethod
    def parse_minified(json_str: str) -> Union[Dict, List]:
        """
        Parse minified JSON string back to Python object
        
        Args:
            json_str: Minified JSON string
            
        Returns:
            Parsed Python dictionary or list
            
        Example:
            >>> json_str = '{"key":"value","number":123}'
            >>> data = JSONMinifier.parse_minified(json_str)
            >>> print(data)
            {'key': 'value', 'number': 123}
        """
        return json.loads(json_str)
    
    @staticmethod
    def get_size_reduction(
        original: Union[Dict, List],
        minified_str: str = None
    ) -> Dict[str, Any]:
        """
        Calculate size reduction from minification
        
        Compares original pretty-printed JSON size with minified size.
        
        Args:
            original: Original data structure
            minified_str: Optional pre-minified string (will compute if None)
            
        Returns:
            Dictionary with size metrics:
            - original_size: Size of pretty-printed JSON (bytes)
            - minified_size: Size of minified JSON (bytes)
            - reduction_bytes: Bytes saved
            - reduction_percent: Percentage saved
            
        Example:
            >>> data = {"user_id": "carlos", "category": "preferences"}
            >>> metrics = JSONMinifier.get_size_reduction(data)
            >>> print(metrics)
            {
                'original_size': 58,
                'minified_size': 45,
                'reduction_bytes': 13,
                'reduction_percent': 22.41
            }
        """
        # Original size (pretty printed with indentation)
        original_str = json.dumps(original, indent=2)
        original_size = len(original_str)
        
        # Minified size
        if minified_str is None:
            minified_str = JSONMinifier.minify(original)
        minified_size = len(minified_str)
        
        # Calculate reduction
        reduction_bytes = original_size - minified_size
        reduction_percent = (
            (reduction_bytes / original_size * 100) 
            if original_size > 0 
            else 0
        )
        
        return {
            'original_size': original_size,
            'minified_size': minified_size,
            'reduction_bytes': reduction_bytes,
            'reduction_percent': round(reduction_percent, 2)
        }
    
    @staticmethod
    def minify_batch(data_list: List[Union[Dict, List]]) -> List[str]:
        """
        Minify multiple data structures in batch
        
        Args:
            data_list: List of dictionaries or lists to minify
            
        Returns:
            List of minified JSON strings
            
        Example:
            >>> data_list = [
            ...     {"user": "carlos"},
            ...     {"user": "maria"}
            ... ]
            >>> minified = JSONMinifier.minify_batch(data_list)
            >>> print(minified)
            ['{"user":"carlos"}', '{"user":"maria"}']
        """
        return [JSONMinifier.minify(data) for data in data_list]


# Convenience functions for direct use
def minify(data: Union[Dict, List, Any]) -> str:
    """
    Shorthand for JSONMinifier.minify()
    
    Args:
        data: Data to minify
        
    Returns:
        Minified JSON string
    """
    return JSONMinifier.minify(data)


def parse_minified(json_str: str) -> Union[Dict, List]:
    """
    Shorthand for JSONMinifier.parse_minified()
    
    Args:
        json_str: Minified JSON string
        
    Returns:
        Parsed Python object
    """
    return JSONMinifier.parse_minified(json_str)


def get_size_reduction(original: Union[Dict, List]) -> Dict[str, Any]:
    """
    Shorthand for JSONMinifier.get_size_reduction()
    
    Args:
        original: Original data
        
    Returns:
        Size reduction metrics
    """
    return JSONMinifier.get_size_reduction(original)


# Module exports
__all__ = [
    "JSONMinifier",
    "minify",
    "parse_minified",
    "get_size_reduction"
]
```

**VALIDACIÃ“N OBLIGATORIA:**

```bash
# 1. Verificar sintaxis
python -m py_compile luminoracore/optimization/minifier.py

# 2. Test manual bÃ¡sico
python3 << 'ENDPYTHON'
from luminoracore.optimization.minifier import JSONMinifier, minify

# Test 1: MinificaciÃ³n bÃ¡sica
data = {"user_id": "carlos", "category": "preferences"}
minified = minify(data)
print(f"âœ… Test 1 - Minified: {minified}")
assert ' ' not in minified
assert '\n' not in minified

# Test 2: Parse roundtrip
parsed = JSONMinifier.parse_minified(minified)
print(f"âœ… Test 2 - Parsed: {parsed}")
assert parsed == data

# Test 3: Size reduction
metrics = JSONMinifier.get_size_reduction(data)
print(f"âœ… Test 3 - Reduction: {metrics['reduction_percent']}%")
assert metrics['reduction_percent'] > 15  # Expect at least 15% reduction

# Test 4: Nested data
nested = {
    "user_id": "test",
    "metadata": {
        "source": "conversation",
        "confidence": 0.95
    }
}
minified_nested = minify(nested)
print(f"âœ… Test 4 - Nested minified: {minified_nested}")
assert ' ' not in minified_nested

# Test 5: Batch minification
batch = [
    {"user": "carlos"},
    {"user": "maria"}
]
minified_batch = JSONMinifier.minify_batch(batch)
print(f"âœ… Test 5 - Batch: {minified_batch}")
assert len(minified_batch) == 2

print("\nðŸŽ‰ ALL MANUAL TESTS PASSED!")
ENDPYTHON
```

**CRITERIOS DE Ã‰XITO:**
- [ ] Archivo creado sin errores de sintaxis
- [ ] minify() elimina todos los espacios y newlines
- [ ] parse_minified() restaura datos correctamente
- [ ] get_size_reduction() calcula mÃ©tricas
- [ ] ReducciÃ³n â‰¥ 15-20% vs pretty-print
- [ ] Funciona con datos nested
- [ ] Batch minification funciona
- [ ] Todos los tests manuales pasan

**ACTUALIZAR __init__.py:**

DespuÃ©s de validar, actualiza `luminoracore/optimization/__init__.py`:

```python
# AÃ±adir despuÃ©s de las importaciones de key_mapping:

from .minifier import (
    JSONMinifier,
    minify,
    parse_minified,
    get_size_reduction
)

__all__ = [
    # key_mapping exports
    "compress_keys",
    "expand_keys",
    # ... (mantener existentes)
    
    # minifier exports
    "JSONMinifier",
    "minify",
    "parse_minified",
    "get_size_reduction"
]
```

**VALIDAR IMPORT:**

```bash
python3 -c "from luminoracore.optimization import minify, JSONMinifier; print('âœ… Import successful')"
```

**PRÃ“XIMO PASO:**  
PROMPT 1.5: Tests para minifier.py

---

### PROMPT 1.5: Tests Para minifier.py

**CONTEXTO:**  
Hemos implementado minifier.py. Ahora creamos tests comprehensivos.

**OBJETIVO:**  
Crear suite completa de tests para minifier.py con cobertura â‰¥90%.

**ESPECIFICACIONES TÃ‰CNICAS:**

Crear archivo: `tests/test_optimization/test_minifier.py`

```python
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
            "name": "JosÃ©",
            "city": "SÃ£o Paulo",
            "emoji": "ðŸš€"
        }
        
        minified = JSONMinifier.minify(data)
        
        # Should preserve unicode
        assert "JosÃ©" in minified
        assert "SÃ£o Paulo" in minified
        assert "ðŸš€" in minified
        
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
        assert metrics['reduction_percent'] > 20
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
        assert total_reduction > 35  # Should achieve >35% total


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**VALIDACIÃ“N:**

```bash
# Ejecutar tests
pytest tests/test_optimization/test_minifier.py -v

# Verificar coverage
pytest tests/test_optimization/test_minifier.py \
  --cov=luminoracore.optimization.minifier \
  --cov-report=term-missing -v

# Ejecutar todos los tests de optimization
pytest tests/test_optimization/ -v
```

**CRITERIOS DE Ã‰XITO:**
- [ ] Todos los tests pasan (100%)
- [ ] Coverage â‰¥ 90%
- [ ] Integration tests con key_mapping pasan
- [ ] Total reduction >35% demostrada

**PRÃ“XIMO PASO:**  
PROMPT 1.6: Implementar compact_format.py

---

**CONTINÃšA EN EL ARCHIVO...**

*Este archivo es muy largo. Â¿Quieres que continÃºe creando el resto de los prompts (1.6-1.20) ahora, o prefieres que Cursor AI implemente primero el minifier.py y luego continuamos?*


### PROMPT 1.6: Implementar compact_format.py

**CONTEXTO:**  
Tenemos key_mapping y minifier funcionando (30% reduction). Ahora implementamos formato array compacto que convierte dictionaries a arrays para mÃ¡xima compactaciÃ³n.

**OBJETIVO:**  
Crear `luminoracore/optimization/compact_format.py` que representa facts como arrays en lugar de dicts.

**DEPENDENCIAS:**
- âœ… key_mapping.py funcionando
- âœ… minifier.py funcionando
- âœ… 52 tests passing

**ESPECIFICACIONES TÃ‰CNICAS:**

Crear archivo: `luminoracore/optimization/compact_format.py`

```python
"""
Compact Array Format - Phase 1 Quick Wins
Convert fact dictionaries to compact arrays for maximum space efficiency

Instead of:
    {"uid": "carlos", "cat": "pref", "k": "sport", "v": "basketball", ...}
    
Use:
    ["carlos", "pref", "sport", "basketball", ...]

This eliminates key names entirely, relying on positional indices.
Achieves an additional 30-40% size reduction on top of key compression.

Author: LuminoraCore Team
Version: 1.2.0-lite
"""

from typing import Dict, List, Any, Optional, Union


class CompactFact:
    """
    Represent facts as compact arrays instead of dictionaries
    
    Format: [uid, cat, k, v, imp, ts, src, conf, tags]
    
    This reduces JSON size by:
    1. Eliminating key names (only values remain)
    2. Relying on positional indices
    3. Optional fields can be None or omitted
    
    Example:
        Dictionary: {"uid": "carlos", "cat": "pref", "k": "sport", "v": "basketball"}
        Array:      ["carlos", "pref", "sport", "basketball"]
        
        Size: ~60 chars dict â†’ ~40 chars array (33% reduction)
    """
    
    # Field indices (order matters! DO NOT CHANGE)
    INDICES = {
        "user_id": 0,
        "category": 1,
        "key": 2,
        "value": 3,
        "importance": 4,
        "timestamp": 5,
        "source": 6,
        "confidence": 7,
        "tags": 8
    }
    
    # Reverse mapping for restoration
    FIELDS = {v: k for k, v in INDICES.items()}
    
    # Field order (for documentation)
    FIELD_ORDER = [
        "user_id",      # 0
        "category",     # 1
        "key",          # 2
        "value",        # 3
        "importance",   # 4
        "timestamp",    # 5
        "source",       # 6
        "confidence",   # 7
        "tags"          # 8
    ]
    
    @staticmethod
    def to_array(fact: Dict[str, Any]) -> List[Any]:
        """
        Convert fact dictionary to compact array
        
        Args:
            fact: Fact dictionary with standard keys (long or short)
            
        Returns:
            Compact array representation
            
        Example:
            >>> fact = {
            ...     "user_id": "carlos",
            ...     "category": "preferences",
            ...     "key": "favorite_sport",
            ...     "value": "basketball",
            ...     "importance": 0.85,
            ...     "timestamp": "2024-11-18T10:30:00Z",
            ...     "source": "conversation",
            ...     "confidence": 0.95,
            ...     "tags": ["sports"]
            ... }
            >>> array = CompactFact.to_array(fact)
            >>> print(array)
            ["carlos", "preferences", "favorite_sport", "basketball", 
             0.85, "2024-11-18T10:30:00Z", "conversation", 0.95, ["sports"]]
        """
        # Support both long and short key names
        uid = fact.get("user_id") or fact.get("uid")
        cat = fact.get("category") or fact.get("cat")
        k = fact.get("key") or fact.get("k")
        v = fact.get("value") or fact.get("v")
        imp = fact.get("importance") or fact.get("imp")
        ts = fact.get("timestamp") or fact.get("ts")
        src = fact.get("source") or fact.get("src")
        conf = fact.get("confidence") or fact.get("conf")
        tags = fact.get("tags", [])
        
        return [uid, cat, k, v, imp, ts, src, conf, tags]
    
    @staticmethod
    def from_array(arr: List[Any]) -> Dict[str, Any]:
        """
        Convert compact array back to fact dictionary
        
        Args:
            arr: Compact array representation
            
        Returns:
            Fact dictionary with standard keys
            
        Example:
            >>> array = ["carlos", "pref", "sport", "basketball", 0.85, 
            ...          "2024-11-18", "conv", 0.95, ["sports"]]
            >>> fact = CompactFact.from_array(array)
            >>> print(fact["user_id"])
            carlos
        """
        # Build dict from array, handling missing values
        result = {}
        
        if len(arr) > 0 and arr[0] is not None:
            result["user_id"] = arr[0]
        if len(arr) > 1 and arr[1] is not None:
            result["category"] = arr[1]
        if len(arr) > 2 and arr[2] is not None:
            result["key"] = arr[2]
        if len(arr) > 3 and arr[3] is not None:
            result["value"] = arr[3]
        if len(arr) > 4 and arr[4] is not None:
            result["importance"] = arr[4]
        if len(arr) > 5 and arr[5] is not None:
            result["timestamp"] = arr[5]
        if len(arr) > 6 and arr[6] is not None:
            result["source"] = arr[6]
        if len(arr) > 7 and arr[7] is not None:
            result["confidence"] = arr[7]
        if len(arr) > 8:
            result["tags"] = arr[8] if arr[8] else []
        
        return result
    
    @staticmethod
    def to_array_batch(facts: List[Dict[str, Any]]) -> List[List[Any]]:
        """
        Convert multiple facts to compact arrays
        
        Args:
            facts: List of fact dictionaries
            
        Returns:
            List of compact arrays
            
        Example:
            >>> facts = [
            ...     {"user_id": "carlos", "category": "pref"},
            ...     {"user_id": "maria", "category": "goal"}
            ... ]
            >>> arrays = CompactFact.to_array_batch(facts)
            >>> len(arrays)
            2
        """
        return [CompactFact.to_array(fact) for fact in facts]
    
    @staticmethod
    def from_array_batch(arrays: List[List[Any]]) -> List[Dict[str, Any]]:
        """
        Convert multiple compact arrays back to dictionaries
        
        Args:
            arrays: List of compact arrays
            
        Returns:
            List of fact dictionaries
            
        Example:
            >>> arrays = [
            ...     ["carlos", "pref", "sport", "basketball"],
            ...     ["maria", "goal", "career", "engineer"]
            ... ]
            >>> facts = CompactFact.from_array_batch(arrays)
            >>> len(facts)
            2
        """
        return [CompactFact.from_array(arr) for arr in arrays]
    
    @staticmethod
    def get_size_reduction(
        original_dict: Dict[str, Any],
        array: List[Any] = None
    ) -> Dict[str, Any]:
        """
        Calculate size reduction from dictionary to array format
        
        Args:
            original_dict: Original fact dictionary
            array: Optional pre-computed array
            
        Returns:
            Dictionary with size metrics
            
        Example:
            >>> fact = {"user_id": "carlos", "category": "pref", "key": "sport"}
            >>> metrics = CompactFact.get_size_reduction(fact)
            >>> print(f"Reduction: {metrics['reduction_percent']}%")
            Reduction: 35.2%
        """
        import json
        
        # Original size (minified dict)
        dict_str = json.dumps(original_dict, separators=(',', ':'))
        dict_size = len(dict_str)
        
        # Array size
        if array is None:
            array = CompactFact.to_array(original_dict)
        array_str = json.dumps(array, separators=(',', ':'))
        array_size = len(array_str)
        
        # Calculate reduction
        reduction_bytes = dict_size - array_size
        reduction_percent = (
            (reduction_bytes / dict_size * 100) 
            if dict_size > 0 
            else 0
        )
        
        return {
            'dict_size': dict_size,
            'array_size': array_size,
            'reduction_bytes': reduction_bytes,
            'reduction_percent': round(reduction_percent, 2)
        }


class CompactFormatConfig:
    """
    Configuration for compact format usage
    
    Allows control over when and how to use compact format.
    """
    
    def __init__(
        self,
        enabled: bool = True,
        preserve_nulls: bool = False,
        min_fields_for_compression: int = 5
    ):
        """
        Initialize compact format configuration
        
        Args:
            enabled: Whether to use compact format
            preserve_nulls: Whether to preserve null values in arrays
            min_fields_for_compression: Minimum fields needed to use compression
        """
        self.enabled = enabled
        self.preserve_nulls = preserve_nulls
        self.min_fields_for_compression = min_fields_for_compression
    
    def should_compress(self, fact: Dict[str, Any]) -> bool:
        """
        Determine if a fact should be compressed to array format
        
        Args:
            fact: Fact dictionary
            
        Returns:
            True if should compress, False otherwise
        """
        if not self.enabled:
            return False
        
        # Only compress if has enough fields
        if len(fact) < self.min_fields_for_compression:
            return False
        
        return True
    
    def apply(self, fact: Dict[str, Any]) -> Union[Dict, List]:
        """
        Apply compact format based on configuration
        
        Args:
            fact: Fact dictionary
            
        Returns:
            Compact array if should compress, otherwise original dict
        """
        if not self.should_compress(fact):
            return fact
        
        array = CompactFact.to_array(fact)
        
        if not self.preserve_nulls:
            # Remove trailing nulls to save more space
            while array and array[-1] is None:
                array.pop()
        
        return array


# Convenience functions
def to_compact(fact: Dict[str, Any]) -> List[Any]:
    """Shorthand for CompactFact.to_array()"""
    return CompactFact.to_array(fact)


def from_compact(array: List[Any]) -> Dict[str, Any]:
    """Shorthand for CompactFact.from_array()"""
    return CompactFact.from_array(array)


def to_compact_batch(facts: List[Dict[str, Any]]) -> List[List[Any]]:
    """Shorthand for CompactFact.to_array_batch()"""
    return CompactFact.to_array_batch(facts)


def from_compact_batch(arrays: List[List[Any]]) -> List[Dict[str, Any]]:
    """Shorthand for CompactFact.from_array_batch()"""
    return CompactFact.from_array_batch(arrays)


# Module exports
__all__ = [
    "CompactFact",
    "CompactFormatConfig",
    "to_compact",
    "from_compact",
    "to_compact_batch",
    "from_compact_batch"
]
```

**VALIDACIÃ“N OBLIGATORIA:**

```bash
# 1. Verificar sintaxis
python -m py_compile luminoracore/optimization/compact_format.py

# 2. Test manual bÃ¡sico
python3 << 'ENDPYTHON'
from luminoracore.optimization.compact_format import CompactFact, to_compact, from_compact

# Test 1: ConversiÃ³n bÃ¡sica
fact = {
    "user_id": "carlos",
    "category": "pref",
    "key": "sport",
    "value": "basketball",
    "importance": 0.85
}

array = to_compact(fact)
print(f"âœ… Test 1 - Array: {array}")
assert isinstance(array, list)
assert array[0] == "carlos"

# Test 2: Roundtrip
restored = from_compact(array)
print(f"âœ… Test 2 - Restored: {restored}")
assert restored["user_id"] == "carlos"
assert restored["category"] == "pref"

# Test 3: Size reduction
metrics = CompactFact.get_size_reduction(fact)
print(f"âœ… Test 3 - Reduction: {metrics['reduction_percent']}%")
assert metrics['reduction_percent'] > 25  # Expect >25% reduction

# Test 4: Batch conversion
facts = [
    {"user_id": "carlos", "category": "pref"},
    {"user_id": "maria", "category": "goal"}
]
arrays = to_compact_batch(facts)
print(f"âœ… Test 4 - Batch: {len(arrays)} arrays")
assert len(arrays) == 2

restored_batch = from_compact_batch(arrays)
assert len(restored_batch) == 2

# Test 5: Con keys comprimidas (backward compatible)
compressed_fact = {
    "uid": "carlos",
    "cat": "pref",
    "k": "sport",
    "v": "basketball"
}
array_compressed = to_compact(compressed_fact)
print(f"âœ… Test 5 - Compressed keys to array: {array_compressed}")
assert array_compressed[0] == "carlos"

print("\nðŸŽ‰ ALL MANUAL TESTS PASSED!")
ENDPYTHON
```

**CRITERIOS DE Ã‰XITO:**
- [ ] Archivo creado sin errores
- [ ] to_array() convierte dict a array
- [ ] from_array() restaura dict desde array
- [ ] Roundtrip preserva datos
- [ ] ReducciÃ³n â‰¥ 30% vs dict
- [ ] Funciona con keys largas y cortas
- [ ] Batch operations funcionan
- [ ] Todos los tests manuales pasan

**ACTUALIZAR __init__.py:**

```python
# AÃ±adir a luminoracore/optimization/__init__.py:

from .compact_format import (
    CompactFact,
    CompactFormatConfig,
    to_compact,
    from_compact,
    to_compact_batch,
    from_compact_batch
)

__all__ = [
    # ... mantener existentes ...
    
    # compact_format exports
    "CompactFact",
    "CompactFormatConfig",
    "to_compact",
    "from_compact",
    "to_compact_batch",
    "from_compact_batch"
]
```

**PRÃ“XIMO PASO:**  
PROMPT 1.7: Tests para compact_format.py

---


### PROMPT 1.7: Tests Para compact_format.py

**CONTEXTO:**  
Hemos implementado compact_format.py. Ahora creamos tests comprehensivos.

**OBJETIVO:**  
Crear suite completa de tests para compact_format.py con cobertura â‰¥90%.

**ESPECIFICACIONES TÃ‰CNICAS:**

Crear archivo: `tests/test_optimization/test_compact_format.py`

```python
"""
Tests for compact_format.py
Phase 1 - Quick Wins - Semana 2

Test Categories:
- TestArrayConversion: Basic conversion dict â†” array
- TestBatchOperations: Batch processing
- TestSizeReduction: Size reduction calculations
- TestConfiguration: CompactFormatConfig
- TestEdgeCases: Edge cases and error handling
- TestIntegration: Integration with key_mapping + minifier
"""

import pytest
from luminoracore.optimization.compact_format import (
    CompactFact,
    CompactFormatConfig,
    to_compact,
    from_compact,
    to_compact_batch,
    from_compact_batch
)


class TestArrayConversion:
    """Test dictionary to array conversion"""
    
    def test_to_array_basic(self):
        """Test converting basic fact to array"""
        fact = {
            "user_id": "carlos",
            "category": "preferences",
            "key": "favorite_sport",
            "value": "basketball"
        }
        
        array = CompactFact.to_array(fact)
        
        assert isinstance(array, list)
        assert len(array) == 9  # All 9 fields
        assert array[0] == "carlos"  # user_id
        assert array[1] == "preferences"  # category
        assert array[2] == "favorite_sport"  # key
        assert array[3] == "basketball"  # value
    
    def test_from_array_basic(self):
        """Test converting array back to dict"""
        array = ["carlos", "pref", "sport", "basketball", 0.85, 
                 "2024-11-18", "conv", 0.95, ["sports"]]
        
        fact = CompactFact.from_array(array)
        
        assert fact["user_id"] == "carlos"
        assert fact["category"] == "pref"
        assert fact["key"] == "sport"
        assert fact["value"] == "basketball"
        assert fact["importance"] == 0.85
        assert fact["timestamp"] == "2024-11-18"
        assert fact["source"] == "conv"
        assert fact["confidence"] == 0.95
        assert fact["tags"] == ["sports"]
    
    def test_roundtrip_conversion(self):
        """Test dict â†’ array â†’ dict returns original"""
        original = {
            "user_id": "test_user",
            "category": "preferences",
            "key": "test_key",
            "value": "test_value",
            "importance": 0.75,
            "timestamp": "2024-11-18T10:30:00Z",
            "source": "conversation",
            "confidence": 0.90,
            "tags": ["tag1", "tag2"]
        }
        
        array = CompactFact.to_array(original)
        restored = CompactFact.from_array(array)
        
        assert restored == original
    
    def test_to_array_with_short_keys(self):
        """Test conversion with abbreviated keys (backward compatible)"""
        fact = {
            "uid": "carlos",
            "cat": "pref",
            "k": "sport",
            "v": "basketball",
            "imp": 0.85
        }
        
        array = CompactFact.to_array(fact)
        
        assert array[0] == "carlos"
        assert array[1] == "pref"
        assert array[2] == "sport"
        assert array[3] == "basketball"
        assert array[4] == 0.85
    
    def test_to_array_partial_fields(self):
        """Test conversion with only some fields present"""
        fact = {
            "user_id": "carlos",
            "category": "pref",
            "key": "sport"
            # Missing: value, importance, etc.
        }
        
        array = CompactFact.to_array(fact)
        
        assert array[0] == "carlos"
        assert array[1] == "pref"
        assert array[2] == "sport"
        assert array[3] is None  # Missing value
    
    def test_from_array_partial(self):
        """Test converting partial array to dict"""
        array = ["carlos", "pref", "sport"]  # Only first 3 fields
        
        fact = CompactFact.from_array(array)
        
        assert fact["user_id"] == "carlos"
        assert fact["category"] == "pref"
        assert fact["key"] == "sport"
        assert "value" not in fact  # Not present
    
    def test_from_array_with_nones(self):
        """Test converting array with None values"""
        array = ["carlos", "pref", None, "basketball", None, None, None, None, []]
        
        fact = CompactFact.from_array(array)
        
        assert fact["user_id"] == "carlos"
        assert fact["category"] == "pref"
        assert "key" not in fact  # Was None
        assert fact["value"] == "basketball"
        assert "importance" not in fact  # Was None


class TestBatchOperations:
    """Test batch conversion operations"""
    
    def test_to_array_batch(self):
        """Test batch dict to array conversion"""
        facts = [
            {"user_id": "carlos", "category": "pref", "key": "sport"},
            {"user_id": "maria", "category": "goal", "key": "career"},
            {"user_id": "john", "category": "exp", "key": "travel"}
        ]
        
        arrays = CompactFact.to_array_batch(facts)
        
        assert len(arrays) == 3
        assert all(isinstance(arr, list) for arr in arrays)
        assert arrays[0][0] == "carlos"
        assert arrays[1][0] == "maria"
        assert arrays[2][0] == "john"
    
    def test_from_array_batch(self):
        """Test batch array to dict conversion"""
        arrays = [
            ["carlos", "pref", "sport", "basketball"],
            ["maria", "goal", "career", "engineer"]
        ]
        
        facts = CompactFact.from_array_batch(arrays)
        
        assert len(facts) == 2
        assert all(isinstance(fact, dict) for fact in facts)
        assert facts[0]["user_id"] == "carlos"
        assert facts[1]["user_id"] == "maria"
    
    def test_batch_roundtrip(self):
        """Test batch conversion roundtrip"""
        original_facts = [
            {"user_id": "1", "category": "pref", "importance": 0.8},
            {"user_id": "2", "category": "goal", "importance": 0.9}
        ]
        
        arrays = CompactFact.to_array_batch(original_facts)
        restored = CompactFact.from_array_batch(arrays)
        
        assert restored == original_facts
    
    def test_empty_batch(self):
        """Test batch operations with empty list"""
        assert CompactFact.to_array_batch([]) == []
        assert CompactFact.from_array_batch([]) == []


class TestSizeReduction:
    """Test size reduction calculations"""
    
    def test_get_size_reduction_basic(self):
        """Test size reduction calculation"""
        fact = {"user_id": "carlos", "category": "pref", "key": "sport"}
        metrics = CompactFact.get_size_reduction(fact)
        
        assert 'dict_size' in metrics
        assert 'array_size' in metrics
        assert 'reduction_bytes' in metrics
        assert 'reduction_percent' in metrics
        
        assert metrics['array_size'] < metrics['dict_size']
        assert metrics['reduction_percent'] > 0
    
    def test_size_reduction_large_fact(self):
        """Test size reduction with complete fact"""
        fact = {
            "user_id": "carlos_rodriguez_123",
            "category": "preferences",
            "key": "favorite_sport",
            "value": "basketball",
            "importance": 0.85,
            "timestamp": "2024-11-18T10:30:00Z",
            "source": "conversation",
            "confidence": 0.95,
            "tags": ["sports", "recreation"]
        }
        
        metrics = CompactFact.get_size_reduction(fact)
        
        # Should achieve significant reduction
        assert metrics['reduction_percent'] > 25
        print(f"    Large fact reduction: {metrics['reduction_percent']}%")
    
    def test_size_reduction_with_provided_array(self):
        """Test providing pre-computed array"""
        fact = {"user_id": "test", "category": "pref"}
        array = CompactFact.to_array(fact)
        
        metrics = CompactFact.get_size_reduction(fact, array)
        
        import json
        expected_array_size = len(json.dumps(array, separators=(',', ':')))
        assert metrics['array_size'] == expected_array_size


class TestConfiguration:
    """Test CompactFormatConfig"""
    
    def test_config_init(self):
        """Test configuration initialization"""
        config = CompactFormatConfig(
            enabled=True,
            preserve_nulls=False,
            min_fields_for_compression=5
        )
        
        assert config.enabled is True
        assert config.preserve_nulls is False
        assert config.min_fields_for_compression == 5
    
    def test_should_compress_enabled(self):
        """Test should_compress when enabled"""
        config = CompactFormatConfig(enabled=True, min_fields_for_compression=3)
        
        fact = {"user_id": "1", "category": "2", "key": "3"}
        assert config.should_compress(fact) is True
    
    def test_should_compress_disabled(self):
        """Test should_compress when disabled"""
        config = CompactFormatConfig(enabled=False)
        
        fact = {"user_id": "1", "category": "2", "key": "3"}
        assert config.should_compress(fact) is False
    
    def test_should_compress_min_fields(self):
        """Test minimum fields requirement"""
        config = CompactFormatConfig(enabled=True, min_fields_for_compression=5)
        
        small_fact = {"user_id": "1", "category": "2"}
        assert config.should_compress(small_fact) is False
        
        large_fact = {"user_id": "1", "category": "2", "key": "3", 
                      "value": "4", "importance": 5}
        assert config.should_compress(large_fact) is True
    
    def test_apply_with_compression(self):
        """Test apply when should compress"""
        config = CompactFormatConfig(enabled=True, min_fields_for_compression=3)
        
        fact = {"user_id": "carlos", "category": "pref", "key": "sport"}
        result = config.apply(fact)
        
        assert isinstance(result, list)
    
    def test_apply_without_compression(self):
        """Test apply when should not compress"""
        config = CompactFormatConfig(enabled=False)
        
        fact = {"user_id": "carlos", "category": "pref"}
        result = config.apply(fact)
        
        assert isinstance(result, dict)
        assert result == fact
    
    def test_apply_remove_trailing_nulls(self):
        """Test removing trailing nulls"""
        config = CompactFormatConfig(enabled=True, preserve_nulls=False)
        
        fact = {"user_id": "carlos", "category": "pref"}  # Partial fact
        result = config.apply(fact)
        
        # Should remove trailing Nones
        while result and result[-1] is None:
            assert False, "Trailing nulls should have been removed"


class TestConvenienceFunctions:
    """Test convenience functions"""
    
    def test_to_compact(self):
        """Test to_compact shorthand"""
        fact = {"user_id": "carlos", "category": "pref"}
        array = to_compact(fact)
        
        assert isinstance(array, list)
        assert array[0] == "carlos"
    
    def test_from_compact(self):
        """Test from_compact shorthand"""
        array = ["carlos", "pref", "sport"]
        fact = from_compact(array)
        
        assert isinstance(fact, dict)
        assert fact["user_id"] == "carlos"
    
    def test_to_compact_batch(self):
        """Test to_compact_batch shorthand"""
        facts = [{"user_id": "1"}, {"user_id": "2"}]
        arrays = to_compact_batch(facts)
        
        assert len(arrays) == 2
        assert isinstance(arrays[0], list)
    
    def test_from_compact_batch(self):
        """Test from_compact_batch shorthand"""
        arrays = [["1", "pref"], ["2", "goal"]]
        facts = from_compact_batch(arrays)
        
        assert len(facts) == 2
        assert isinstance(facts[0], dict)


class TestEdgeCases:
    """Test edge cases"""
    
    def test_empty_fact(self):
        """Test converting empty dict"""
        fact = {}
        array = CompactFact.to_array(fact)
        
        # Should produce array of Nones
        assert all(x is None for x in array[:-1])  # All except tags
        assert array[-1] == []  # tags default to empty list
    
    def test_empty_array(self):
        """Test converting empty array"""
        array = []
        fact = CompactFact.from_array(array)
        
        assert fact == {}
    
    def test_array_with_extra_fields(self):
        """Test array with more than 9 fields"""
        array = ["1", "2", "3", "4", "5", "6", "7", "8", ["9"], "extra"]
        fact = CompactFact.from_array(array)
        
        # Should only use first 9 fields
        assert len(fact) <= 9
    
    def test_special_values(self):
        """Test special values in facts"""
        fact = {
            "user_id": "",  # Empty string
            "category": 0,  # Zero
            "key": False,  # Boolean false
            "value": None,  # None
            "tags": []  # Empty list
        }
        
        array = CompactFact.to_array(fact)
        restored = CompactFact.from_array(array)
        
        # Empty string should be preserved
        assert restored.get("user_id") == ""
        # Zero should be preserved
        assert restored.get("category") == 0
        # False should be preserved
        assert restored.get("key") is False


class TestIntegration:
    """Integration tests with other optimization modules"""
    
    def test_with_key_compression(self):
        """Test compact format after key compression"""
        from luminoracore.optimization.key_mapping import compress_keys
        
        original = {
            "user_id": "carlos",
            "category": "preferences",
            "key": "favorite_sport",
            "value": "basketball"
        }
        
        # Step 1: Compress keys
        compressed = compress_keys(original)
        
        # Step 2: Convert to array
        array = CompactFact.to_array(compressed)
        
        assert isinstance(array, list)
        assert array[0] == "carlos"
    
    def test_with_minification(self):
        """Test compact format with minification"""
        from luminoracore.optimization.minifier import minify
        
        fact = {
            "user_id": "carlos",
            "category": "pref",
            "key": "sport"
        }
        
        # Convert to array then minify
        array = CompactFact.to_array(fact)
        minified = minify(array)
        
        # Should be very compact
        assert ' ' not in minified
        assert len(minified) < 50  # Very short
    
    def test_full_pipeline(self):
        """Test complete optimization pipeline"""
        from luminoracore.optimization.key_mapping import compress_keys, expand_keys
        from luminoracore.optimization.minifier import minify, parse_minified
        import json
        
        # Original fact
        original = {
            "user_id": "carlos_rodriguez",
            "category": "preferences",
            "key": "favorite_sport",
            "value": "basketball",
            "importance": 0.85,
            "timestamp": "2024-11-18T10:30:00Z"
        }
        
        # Measure original size
        original_size = len(json.dumps(original, indent=2))
        
        # Apply optimizations
        # 1. Compress keys
        compressed = compress_keys(original)
        # 2. Convert to array
        array = CompactFact.to_array(compressed)
        # 3. Minify
        minified = minify(array)
        
        optimized_size = len(minified)
        
        # Reverse pipeline
        # 1. Parse minified
        parsed_array = parse_minified(minified)
        # 2. Convert array to dict
        restored_compressed = CompactFact.from_array(parsed_array)
        # 3. Expand keys
        restored = expand_keys(restored_compressed)
        
        # Should match original
        assert restored == original
        
        # Calculate total reduction
        total_reduction = ((original_size - optimized_size) / original_size) * 100
        
        print(f"    Full pipeline reduction: {total_reduction:.1f}%")
        
        # Should achieve >40% total reduction
        assert total_reduction > 40


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**VALIDACIÃ“N:**

```bash
# Ejecutar tests
pytest tests/test_optimization/test_compact_format.py -v

# Verificar coverage
pytest tests/test_optimization/test_compact_format.py \
  --cov=luminoracore.optimization.compact_format \
  --cov-report=term-missing -v

# Ejecutar todos los tests de optimization
pytest tests/test_optimization/ -v
```

**CRITERIOS DE Ã‰XITO:**
- [ ] Todos los tests pasan (100%)
- [ ] Coverage â‰¥ 90%
- [ ] Integration test muestra >40% reduction total
- [ ] Full pipeline (key + array + minify) funciona

**ESTADO ESPERADO DESPUÃ‰S:**
```
Tests optimization:
â”œâ”€ test_key_mapping: 25 tests âœ…
â”œâ”€ test_minifier: 26 tests âœ…
â”œâ”€ test_compact_format: ~30 tests âœ…
â””â”€ Total: ~81 tests passing
```

**PRÃ“XIMO PASO:**  
Semana 3 - PROMPT 1.8: Implementar deduplicator.py

---

