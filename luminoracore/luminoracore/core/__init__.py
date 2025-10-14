"""
Core components for LuminoraCore personality management.
"""

# v1.0 exports
from .personality import Personality, PersonalityError
from .schema import PersonalitySchema

# v1.1 exports - config
from .config import (
    V11Features,
    FeatureFlagManager,
    get_features,
    is_enabled,
    require_feature
)

__all__ = [
    # v1.0
    "Personality",
    "PersonalityError",
    "PersonalitySchema",
    # v1.1
    "V11Features",
    "FeatureFlagManager",
    "get_features",
    "is_enabled",
    "require_feature"
]
