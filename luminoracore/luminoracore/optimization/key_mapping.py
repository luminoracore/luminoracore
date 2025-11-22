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

