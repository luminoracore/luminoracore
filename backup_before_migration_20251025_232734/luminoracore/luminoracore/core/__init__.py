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

# v1.1 exports - personality extensions
from .personality_v1_1 import (
    PersonalityV11Extensions,
    HierarchicalConfig,
    MoodSystemConfig,
    RelationshipLevelConfig,
    AffinityRange
)

# v1.1 exports - compiler
from .compiler_v1_1 import DynamicPersonalityCompiler

__all__ = [
    # v1.0
    "Personality",
    "PersonalityError",
    "PersonalitySchema",
    # v1.1 - config
    "V11Features",
    "FeatureFlagManager",
    "get_features",
    "is_enabled",
    "require_feature",
    # v1.1 - personality
    "PersonalityV11Extensions",
    "HierarchicalConfig",
    "MoodSystemConfig",
    "RelationshipLevelConfig",
    "AffinityRange",
    # v1.1 - compiler
    "DynamicPersonalityCompiler"
]
