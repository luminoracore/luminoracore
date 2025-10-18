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
from .session.storage_sqlite_v11 import SQLiteStorageV11
from .session.storage_dynamodb_v11 import DynamoDBStorageV11
from .session.storage_postgresql_v11 import PostgreSQLStorageV11
from .session.storage_redis_v11 import RedisStorageV11
from .session.storage_mongodb_v11 import MongoDBStorageV11
from .session.storage_mysql_v11 import MySQLStorageV11
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
    "SQLiteStorageV11",
    "DynamoDBStorageV11",
    "PostgreSQLStorageV11",
    "RedisStorageV11",
    "MongoDBStorageV11",
    "MySQLStorageV11",
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
