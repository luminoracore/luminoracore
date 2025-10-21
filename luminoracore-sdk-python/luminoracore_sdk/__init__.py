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
from .session.storage_sqlite_flexible import FlexibleSQLiteStorageV11
from .session.storage_dynamodb_flexible import FlexibleDynamoDBStorageV11
from .session.storage_postgresql_flexible import FlexiblePostgreSQLStorageV11
from .session.storage_redis_flexible import FlexibleRedisStorageV11
from .session.storage_mongodb_flexible import FlexibleMongoDBStorageV11
from .evolution.personality_evolution import PersonalityEvolutionEngine
from .analysis.sentiment_analyzer import AdvancedSentimentAnalyzer
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
    __version__ = "1.1.2"  # Fixed version for backend compatibility - v30 layer

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
    "FlexibleSQLiteStorageV11",
    "FlexibleDynamoDBStorageV11",
    "FlexiblePostgreSQLStorageV11",
    "FlexibleRedisStorageV11",
    "FlexibleMongoDBStorageV11",
    "PersonalityEvolutionEngine",
    "AdvancedSentimentAnalyzer",
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
