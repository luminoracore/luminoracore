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

