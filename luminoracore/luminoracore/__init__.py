"""
LuminoraCore - Universal AI Personality Management Standard

A comprehensive framework for creating, validating, and managing AI personalities
across multiple LLM providers.
"""

__version__ = "0.1.0"
__author__ = "LuminoraCore Team"
__email__ = "team@luminoracore.dev"
__license__ = "MIT"

from .core.personality import Personality, PersonalityError
from .core.schema import PersonalitySchema
from .tools.validator import PersonalityValidator
from .tools.compiler import PersonalityCompiler, LLMProvider
from .tools.blender import PersonaBlend

__all__ = [
    "Personality",
    "PersonalityError", 
    "PersonalitySchema",
    "PersonalityValidator",
    "PersonalityCompiler",
    "LLMProvider",
    "PersonaBlend",
]
