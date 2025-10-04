"""Session management for LuminoraCore SDK."""

from .manager import SessionManager
from .conversation import ConversationManager
from .memory import MemoryManager
from .storage import SessionStorage
from ..types.session import SessionConfig, MemoryConfig

# Alias for backward compatibility
PersonalitySession = SessionManager

__all__ = [
    "SessionManager",
    "PersonalitySession",  # Alias
    "ConversationManager", 
    "MemoryManager",
    "SessionStorage",
    "SessionConfig",
    "MemoryConfig",
]
