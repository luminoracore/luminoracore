"""
LuminoraCore - Universal AI Personality Management Standard

A comprehensive framework for creating, validating, and managing AI personalities
across multiple LLM providers.
"""

__version__ = "1.1.0"
__author__ = "LuminoraCore Team"
__email__ = "team@luminoracore.dev"
__license__ = "MIT"

from .core.personality import Personality, PersonalityError
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

__all__ = [
    # v1.0 modules
    "Personality",
    "PersonalityError", 
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
]
