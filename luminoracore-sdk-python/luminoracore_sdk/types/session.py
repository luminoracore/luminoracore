"""Session-related type definitions."""

from __future__ import annotations

from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime


class SessionType(str, Enum):
    """Session type enumeration."""
    STATEFUL = "stateful"
    STATELESS = "stateless"
    CHAT = "chat"


class MessageRole(str, Enum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class StorageType(str, Enum):
    """Storage backend type enumeration."""
    MEMORY = "memory"
    REDIS = "redis"
    POSTGRES = "postgres"
    MONGODB = "mongodb"
    FILE = "file"


@dataclass
class Message:
    """Represents a single message in a conversation."""
    
    role: MessageRole
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Message:
        """Create message from dictionary."""
        return cls(
            role=MessageRole(data["role"]),
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {}),
        )


@dataclass
class Conversation:
    """Represents a conversation with messages and metadata."""
    
    session_id: str
    messages: List[Message] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def add_message(self, message: Message) -> None:
        """Add a message to the conversation."""
        self.messages.append(message)
        self.updated_at = datetime.utcnow()
    
    def get_recent_messages(self, count: int) -> List[Message]:
        """Get the most recent messages."""
        return self.messages[-count:] if count > 0 else self.messages
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert conversation to dictionary."""
        return {
            "session_id": self.session_id,
            "messages": [msg.to_dict() for msg in self.messages],
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class SessionConfig:
    """Configuration for personality sessions."""
    
    session_id: str
    personality: Dict[str, Any]
    provider_config: Dict[str, Any]
    session_type: SessionType = SessionType.CHAT
    max_history: int = 100
    timeout: int = 300
    
    # Generation parameters
    generation_params: Dict[str, Any] = field(default_factory=dict)
    
    # Conversation settings
    max_history_length: int = 50
    context_window_size: int = 4000
    include_context_in_prompt: bool = True
    
    # Memory settings
    memory_enabled: bool = True
    memory_decay_factor: float = 0.1
    
    # Storage settings
    storage: Optional[StorageConfig] = None
    
    # Session behavior
    auto_save: bool = True
    auto_save_interval: int = 60  # seconds
    
    def __post_init__(self):
        """Set default generation parameters."""
        if not self.generation_params:
            self.generation_params = {
                "temperature": 0.7,
                "max_tokens": 1024,
            }


@dataclass
class StorageConfig:
    """Configuration for conversation storage."""
    
    storage_type: StorageType = StorageType.MEMORY
    connection_string: Optional[str] = None
    table_name: str = "conversations"
    auto_create_tables: bool = True
    encryption_enabled: bool = False
    compression_enabled: bool = False
    
    # Redis specific
    redis_db: int = 0
    redis_prefix: str = "luminoracore:"
    
    # File specific
    file_path: str = "./conversations"
    file_format: str = "json"


@dataclass
class MemoryConfig:
    """Configuration for conversation memory."""
    
    enabled: bool = True
    max_entries: int = 1000
    decay_factor: float = 0.1
    importance_threshold: float = 0.5
    ttl: Optional[int] = None  # Time-to-live in seconds (None = no expiration)
    
    # Memory types to track
    track_topics: bool = True
    track_preferences: bool = True
    track_context: bool = True
    track_emotions: bool = False
