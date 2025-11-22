"""Personality management for LuminoraCore SDK."""

from .blender import PersonalityBlender
from .manager import PersonalityManager
from .validator import PersonalityValidator

# Adapter for Core integration (new in v1.2)
try:
    from .adapter import PersonaBlendAdapter
    HAS_ADAPTER = True
except ImportError:
    HAS_ADAPTER = False
    PersonaBlendAdapter = None

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

# Add adapter to exports if available
if HAS_ADAPTER:
    __all__.append("PersonaBlendAdapter")
