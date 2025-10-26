"""
LuminoraCore Storage Components
Storage implementations for different databases
"""

from .base_storage import BaseStorage
from .in_memory_storage import InMemoryStorage

# Import flexible storage if available
try:
    from .flexible_storage import FlexibleStorageManager, StorageType, StorageConfig
    __all__ = [
        'BaseStorage',
        'InMemoryStorage',
        'FlexibleStorageManager',
        'StorageType',
        'StorageConfig'
    ]
except ImportError:
    __all__ = [
        'BaseStorage',
        'InMemoryStorage'
    ]