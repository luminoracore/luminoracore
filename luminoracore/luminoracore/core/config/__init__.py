"""
Configuration module for LuminoraCore Core
"""

from .feature_flags import (
    V11Features,
    FeatureFlagManager,
    FeatureCategory,
    get_features,
    is_enabled,
    require_feature
)

__all__ = [
    'V11Features',
    'FeatureFlagManager',
    'FeatureCategory',
    'get_features',
    'is_enabled',
    'require_feature'
]

