"""Session management for LuminoraCore SDK."""

from .manager import SessionManager
from .conversation import ConversationManager
from .memory import MemoryManager
from .storage import SessionStorage
from .storage_v1_1 import StorageV11Extension, InMemoryStorageV11
from ..types.session import SessionConfig, MemoryConfig

# Alias for backward compatibility
PersonalitySession = SessionManager

__all__ = [
    "SessionManager",
    "PersonalitySession",  # Alias
    "ConversationManager", 
    "MemoryManager",
    "SessionStorage",
    "StorageV11Extension",
    "InMemoryStorageV11",
    "SessionConfig",
    "MemoryConfig",
]
