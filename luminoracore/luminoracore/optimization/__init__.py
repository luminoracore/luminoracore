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

# Imports - Semana 2
from .minifier import (
    JSONMinifier,
    minify,
    parse_minified,
    get_size_reduction
)

from .compact_format import (
    CompactFact,
    CompactFormatConfig,
    to_compact,
    from_compact,
    to_compact_batch,
    from_compact_batch
)

# Imports - Semana 3
from .deduplicator import (
    FactDeduplicator,
    DeduplicationConfig,
    deduplicate_facts
)

from .cache import (
    LRUCache,
    FactCache,
    CacheConfig,
    DEFAULT_CACHE_CAPACITY,
    DEFAULT_TTL_SECONDS,
    DEFAULT_CLEANUP_INTERVAL,
    CACHE_KEY_SEPARATOR
)
from .deduplicator import (
    SOURCE_SEPARATOR
)

# Imports - Semana 4
from .optimizer import (
    Optimizer,
    OptimizationConfig,
    create_optimizer
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
    "REVERSE_MAPPINGS",
    
    # minifier exports
    "JSONMinifier",
    "minify",
    "parse_minified",
    "get_size_reduction",
    
    # compact_format exports
    "CompactFact",
    "CompactFormatConfig",
    "to_compact",
    "from_compact",
    "to_compact_batch",
    "from_compact_batch",
    
    # deduplicator exports
    "FactDeduplicator",
    "DeduplicationConfig",
    "deduplicate_facts",
    
    # cache exports
    "LRUCache",
    "FactCache",
    "CacheConfig",
    "DEFAULT_CACHE_CAPACITY",
    "DEFAULT_TTL_SECONDS",
    "DEFAULT_CLEANUP_INTERVAL",
    "CACHE_KEY_SEPARATOR",
    
    # deduplicator constants
    "SOURCE_SEPARATOR",
    
    # optimizer exports
    "Optimizer",
    "OptimizationConfig",
    "create_optimizer"
]

