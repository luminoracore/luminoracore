"""LuminoraCore SDK - Advanced Python client for personality management."""

from importlib.metadata import version, PackageNotFoundError

from .client import LuminoraCoreClient
from .client_v1_1 import LuminoraCoreClientV11
from .session import (
    PersonalitySession,
    ConversationManager,
    SessionConfig,
    MemoryConfig,
    StorageV11Extension,
    InMemoryStorageV11,
)
from .providers import (
    ProviderFactory,
    OpenAIProvider,
    AnthropicProvider,
    LlamaProvider,
    MistralProvider,
)
from .personality import (
    PersonalityLoader,
    PersonalityBlender,
    BlendConfig,
)
from .types import (
    SessionType,
    ProviderType,
    StorageType,
    Message,
    Conversation,
)
from .utils.exceptions import (
    LuminoraCoreSDKError,
    SessionError,
    ProviderError,
    PersonalityError,
    CompilationError,
)

try:
    __version__ = version("luminoracore-sdk")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = [
    # Main client
    "LuminoraCoreClient",
    "LuminoraCoreClientV11",
    # Session management
    "PersonalitySession",
    "ConversationManager",
    "SessionConfig",
    "MemoryConfig",
    "StorageV11Extension",
    "InMemoryStorageV11",
    # Providers
    "ProviderFactory",
    "OpenAIProvider",
    "AnthropicProvider", 
    "LlamaProvider",
    "MistralProvider",
    # Personality management
    "PersonalityLoader",
    "PersonalityBlender",
    "BlendConfig",
    # Types
    "SessionType",
    "ProviderType",
    "StorageType",
    "Message",
    "Conversation",
    # Exceptions
    "LuminoraCoreSDKError",
    "SessionError",
    "ProviderError",
    "PersonalityError",
    "CompilationError",
    # Version
    "__version__",
]
