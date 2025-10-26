"""Personality management for LuminoraCore SDK."""

from .blender import PersonalityBlender
from .manager import PersonalityManager
from .validator import PersonalityValidator

# Alias for backward compatibility
PersonalityLoader = PersonalityManager

# BlendConfig is an alias for PersonalityBlend
from ..types.personality import PersonalityBlend
BlendConfig = PersonalityBlend

__all__ = [
    "PersonalityBlender",
    "PersonalityManager",
    "PersonalityLoader",  # Alias
    "PersonalityValidator",
    "BlendConfig",
]
