"""
LuminoraCore - Universal AI Personality Management Standard

A comprehensive framework for creating, validating, and managing AI personalities
across multiple LLM providers.
"""

__version__ = "1.1.0"
__author__ = "LuminoraCore Team"
__email__ = "team@luminoracore.dev"
__license__ = "MIT"

from .core.personality import Personality, PersonalityError, find_personality_file
from .core.schema import PersonalitySchema
from .tools.validator import PersonalityValidator
from .tools.compiler import PersonalityCompiler, LLMProvider
from .tools.blender import PersonaBlend

# v1.1 Core modules
from .core import config
from .core import relationship
from .core import memory
from .core import personality_v1_1
from .core import compiler_v1_1
from .storage import migrations

# New core components
from .core import PersonalityEngine, MemorySystem, EvolutionEngine
from .interfaces import StorageInterface, MemoryInterface, PersonalityInterface, EvolutionInterface
from .storage import BaseStorage, InMemoryStorage

# Flexible storage modules
from .storage import (
    FlexibleStorageManager,
    StorageType,
    StorageConfig
)

# Logging configuration
from .logging_config import setup_logging, auto_configure, get_logger

__all__ = [
    # v1.0 modules
    "Personality",
    "PersonalityError",
    "find_personality_file",
    "PersonalitySchema",
    "PersonalityValidator",
    "PersonalityCompiler",
    "LLMProvider",
    "PersonaBlend",
    
    # v1.1 modules
    "config",
    "relationship", 
    "memory",
    "personality_v1_1",
    "compiler_v1_1",
    "migrations",
    
    # New core components
    "PersonalityEngine",
    "MemorySystem", 
    "EvolutionEngine",
    "StorageInterface",
    "MemoryInterface",
    "PersonalityInterface",
    "EvolutionInterface",
    "BaseStorage",
    "InMemoryStorage",
    
    # Flexible storage modules
    "FlexibleStorageManager",
    "StorageType",
    "StorageConfig",
    
    # Logging configuration
    "setup_logging",
    "auto_configure",
    "get_logger",
]
