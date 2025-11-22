# 🚀 FASE 1: Quick Wins PART 2 - Prompts Detallados Para Cursor AI

**Fase:** 1 de 8  
**Timeline:** Semanas 2-4 (continuación)  
**Objetivo:** Completar token reduction 25-45% sin breaking changes  
**Complejidad:** 🟢 BAJA  
**Estado:** 📝 Listo para implementar

---

## 📋 ÍNDICE DE CONTENIDOS

- [CONTEXTO - Dónde Estamos](#-contexto---dónde-estamos)
- [SEMANA 2: Compact Array Format](#-semana-2-compact-array-format)
- [SEMANA 3: Deduplication + Caching](#-semana-3-deduplication--caching)
- [SEMANA 4: Integration + Documentation](#-semana-4-integration--documentation)
- [VALIDACIÓN FINAL](#-validación-final)

---

## 🎯 CONTEXTO - Dónde Estamos

### ✅ Ya Completado (Part 1):

```
Semana 1:
├─ ✅ optimization/ module creado
├─ ✅ key_mapping.py implementado (200+ líneas)
├─ ✅ Tests key_mapping (25 tests, 96% coverage)
└─ ✅ 15-20% token reduction lograda
```

### 🔄 Por Completar (Part 2):

```
Semana 2:
├─ minifier.py + tests
├─ compact_format.py + tests
└─ +10-15% reduction adicional

Semana 3:
├─ deduplicator.py + tests
├─ cache.py + tests
└─ +5-10% reduction adicional

Semana 4:
├─ Integration completa
├─ Documentation
├─ Migration guide
└─ v1.2-lite Release
```

### 🎯 Meta Final:
```
TOTAL: 25-45% token reduction
AHORRO: $18K/mes @ 1K requests/día
```

---

## 📅 SEMANA 2: Compact Array Format

**Objetivos:**
- Implementar minifier.py (JSON minification)
- Implementar compact_format.py (dict → array conversion)
- Lograr +10-15% token reduction adicional
- 100% tests passing

**Timeline:**
- Días 6-7: minifier.py + tests
- Días 8-10: compact_format.py + tests

---

### PROMPT 1.4: Implementar minifier.py

**CONTEXTO:**  
Tenemos key_mapping.py funcionando (15-20% reduction). Ahora agregamos minificación JSON para eliminar whitespace y reducir aún más tokens.

**OBJETIVO:**  
Crear `luminoracore/optimization/minifier.py` con funciones para minificar JSON y calcular savings.

**DEPENDENCIAS:**
- ✅ key_mapping.py funcionando
- ✅ Tests key_mapping passing

**ESPECIFICACIONES TÉCNICAS:**

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

**VALIDACIÓN OBLIGATORIA:**

```bash
# 1. Verificar sintaxis
python -m py_compile luminoracore/optimization/minifier.py

# 2. Test manual básico
python3 << 'ENDPYTHON'
from luminoracore.optimization.minifier import JSONMinifier, minify

# Test 1: Minificación básica
data = {"user_id": "carlos", "category": "preferences"}
minified = minify(data)
print(f"✅ Test 1 - Minified: {minified}")
assert ' ' not in minified
assert '\n' not in minified

# Test 2: Parse roundtrip
parsed = JSONMinifier.parse_minified(minified)
print(f"✅ Test 2 - Parsed: {parsed}")
assert parsed == data

# Test 3: Size reduction
metrics = JSONMinifier.get_size_reduction(data)
print(f"✅ Test 3 - Reduction: {metrics['reduction_percent']}%")
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
print(f"✅ Test 4 - Nested minified: {minified_nested}")
assert ' ' not in minified_nested

# Test 5: Batch minification
batch = [
    {"user": "carlos"},
    {"user": "maria"}
]
minified_batch = JSONMinifier.minify_batch(batch)
print(f"✅ Test 5 - Batch: {minified_batch}")
assert len(minified_batch) == 2

print("\n🎉 ALL MANUAL TESTS PASSED!")
ENDPYTHON
```

**CRITERIOS DE ÉXITO:**
- [ ] Archivo creado sin errores de sintaxis
- [ ] minify() elimina todos los espacios y newlines
- [ ] parse_minified() restaura datos correctamente
- [ ] get_size_reduction() calcula métricas
- [ ] Reducción ≥ 15-20% vs pretty-print
- [ ] Funciona con datos nested
- [ ] Batch minification funciona
- [ ] Todos los tests manuales pasan

**ACTUALIZAR __init__.py:**

Después de validar, actualiza `luminoracore/optimization/__init__.py`:

```python
# Añadir después de las importaciones de key_mapping:

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
python3 -c "from luminoracore.optimization import minify, JSONMinifier; print('✅ Import successful')"
```

**PRÓXIMO PASO:**  
PROMPT 1.5: Tests para minifier.py

---

### PROMPT 1.5: Tests Para minifier.py

**CONTEXTO:**  
Hemos implementado minifier.py. Ahora creamos tests comprehensivos.

**OBJETIVO:**  
Crear suite completa de tests para minifier.py con cobertura ≥90%.

**ESPECIFICACIONES TÉCNICAS:**

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

**VALIDACIÓN:**

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

**CRITERIOS DE ÉXITO:**
- [ ] Todos los tests pasan (100%)
- [ ] Coverage ≥ 90%
- [ ] Integration tests con key_mapping pasan
- [ ] Total reduction >35% demostrada

**PRÓXIMO PASO:**  
PROMPT 1.6: Implementar compact_format.py

---

**CONTINÚA EN EL ARCHIVO...**

*Este archivo es muy largo. ¿Quieres que continúe creando el resto de los prompts (1.6-1.20) ahora, o prefieres que Cursor AI implemente primero el minifier.py y luego continuamos?*

