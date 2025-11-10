"""Type definitions for LuminoraCore SDK."""

from .session import (
    SessionType,
    MessageRole,
    StorageType,
    Message,
    Conversation,
    SessionConfig,
    StorageConfig,
    MemoryConfig,
)
from .provider import ProviderType, ProviderConfig, ChatMessage, ChatResponse
from .personality import PersonalityType
from .conversation import ConversationType
from .compilation import CompilationType
# v1.1 types
from .memory import FactDict, EpisodeDict, MemorySearchResult, MemoryQueryOptions
from .relationship import AffinityDict, AffinityProgressDict, LevelChangeDict
from .snapshot import SnapshotMetadataDict, PersonalitySnapshotDict, SnapshotExportOptions

__all__ = [
    # Session types
    "SessionType",
    "MessageRole", 
    "StorageType",
    "Message",
    "Conversation",
    "SessionConfig",
    "StorageConfig",
    "MemoryConfig",
    # Provider types
    "ProviderType",
    "ProviderConfig",
    "ChatMessage",
    "ChatResponse",
    # Personality types
    "PersonalityType",
    # Conversation types
    "ConversationType",
    # Compilation types
    "CompilationType",
    # v1.1 Memory types
    "FactDict",
    "EpisodeDict",
    "MemorySearchResult",
    "MemoryQueryOptions",
    # v1.1 Relationship types
    "AffinityDict",
    "AffinityProgressDict",
    "LevelChangeDict",
    # v1.1 Snapshot types
    "SnapshotMetadataDict",
    "PersonalitySnapshotDict",
    "SnapshotExportOptions",
]
