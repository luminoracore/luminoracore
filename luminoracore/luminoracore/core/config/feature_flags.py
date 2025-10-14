"""
Feature Flag System for LuminoraCore v1.1

Allows safe, gradual rollout of v1.1 features with fine-grained control.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, List
import json
from pathlib import Path
from enum import Enum
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class FeatureCategory(Enum):
    """Categories of v1.1 features"""
    MEMORY = "memory"
    PERSONALITY = "personality"
    ANALYTICS = "analytics"
    EXPORT = "export"


@dataclass
class V11Features:
    """
    v1.1 feature flags
    
    All features are disabled by default for safety.
    Enable progressively as implementation is tested.
    """
    
    # MEMORY SYSTEM FEATURES
    episodic_memory: bool = False
    semantic_search: bool = False
    fact_extraction: bool = False
    
    # PERSONALITY SYSTEM FEATURES
    hierarchical_personality: bool = False
    mood_system: bool = False
    affinity_system: bool = False
    
    # ADVANCED FEATURES
    conversation_analytics: bool = False
    snapshot_export: bool = False
    
    def to_dict(self) -> Dict[str, bool]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, bool]) -> 'V11Features':
        """Create from dictionary"""
        valid_keys = {k: v for k, v in data.items() if hasattr(cls, k)}
        return cls(**valid_keys)
    
    @classmethod
    def all_disabled(cls) -> 'V11Features':
        """Create with all features disabled (safe default)"""
        return cls()
    
    @classmethod
    def all_enabled(cls) -> 'V11Features':
        """Create with all features enabled (for development)"""
        return cls(
            episodic_memory=True,
            semantic_search=True,
            fact_extraction=True,
            hierarchical_personality=True,
            mood_system=True,
            affinity_system=True,
            conversation_analytics=True,
            snapshot_export=True
        )
    
    @classmethod
    def safe_rollout(cls) -> 'V11Features':
        """Safe default configuration for gradual rollout"""
        return cls(
            affinity_system=True,
            hierarchical_personality=True,
        )
    
    def get_enabled_features(self) -> List[str]:
        """Get list of enabled feature names"""
        return [name for name, enabled in self.to_dict().items() if enabled]
    
    def get_disabled_features(self) -> List[str]:
        """Get list of disabled feature names"""
        return [name for name, enabled in self.to_dict().items() if not enabled]
    
    def get_features_by_category(self, category: FeatureCategory) -> Dict[str, bool]:
        """Get features in a specific category"""
        category_map = {
            FeatureCategory.MEMORY: ['episodic_memory', 'semantic_search', 'fact_extraction'],
            FeatureCategory.PERSONALITY: ['hierarchical_personality', 'mood_system', 'affinity_system'],
            FeatureCategory.ANALYTICS: ['conversation_analytics'],
            FeatureCategory.EXPORT: ['snapshot_export']
        }
        
        features = category_map.get(category, [])
        return {f: getattr(self, f) for f in features}
    
    def enable_feature(self, feature_name: str) -> None:
        """Enable a specific feature"""
        if not hasattr(self, feature_name):
            raise ValueError(f"Unknown feature: {feature_name}")
        setattr(self, feature_name, True)
        logger.info(f"Feature enabled: {feature_name}")
    
    def disable_feature(self, feature_name: str) -> None:
        """Disable a specific feature"""
        if not hasattr(self, feature_name):
            raise ValueError(f"Unknown feature: {feature_name}")
        setattr(self, feature_name, False)
        logger.info(f"Feature disabled: {feature_name}")
    
    def is_enabled(self, feature_name: str) -> bool:
        """Check if a feature is enabled"""
        return getattr(self, feature_name, False)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of feature flag state"""
        enabled = self.get_enabled_features()
        disabled = self.get_disabled_features()
        
        return {
            'total_features': len(self.to_dict()),
            'enabled_count': len(enabled),
            'disabled_count': len(disabled),
            'enabled_features': enabled,
            'disabled_features': disabled,
            'rollout_percentage': len(enabled) / len(self.to_dict()) * 100
        }


class FeatureFlagManager:
    """Singleton manager for feature flags"""
    
    _instance = None
    _features: Optional[V11Features] = None
    
    def __new__(cls):
        """Ensure singleton instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._features = V11Features.safe_rollout()
            logger.info("FeatureFlagManager initialized with safe defaults")
        return cls._instance
    
    @classmethod
    def get_features(cls) -> V11Features:
        """Get current feature flags"""
        if cls._features is None:
            cls._features = V11Features.safe_rollout()
        return cls._features
    
    @classmethod
    def set_features(cls, features: V11Features) -> None:
        """Set feature flags"""
        cls._features = features
        logger.info(f"Features updated: {len(features.get_enabled_features())} enabled")
    
    @classmethod
    def load_from_file(cls, filepath: str) -> V11Features:
        """Load feature flags from JSON file"""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Support both direct format and nested format
            if 'v1_1_features' in data:
                features_data = data['v1_1_features']
            else:
                features_data = data
            
            features = V11Features.from_dict(features_data)
            cls.set_features(features)
            
            logger.info(f"Loaded features from {filepath}")
            return features
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading config file: {e}")
    
    @classmethod
    def save_to_file(cls, filepath: str) -> None:
        """Save current feature flags to JSON file"""
        data = {
            "v1_1_features": cls.get_features().to_dict(),
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "version": "1.1.0"
            }
        }
        
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Saved features to {filepath}")
    
    @classmethod
    def is_enabled(cls, feature_name: str) -> bool:
        """Check if a feature is enabled"""
        features = cls.get_features()
        return features.is_enabled(feature_name)
    
    @classmethod
    def require_feature(cls, feature_name: str):
        """Decorator to require a feature to be enabled"""
        def decorator(func):
            import inspect
            
            if inspect.iscoroutinefunction(func):
                async def async_wrapper(*args, **kwargs):
                    if not cls.is_enabled(feature_name):
                        raise RuntimeError(f"Feature '{feature_name}' is not enabled")
                    return await func(*args, **kwargs)
                return async_wrapper
            else:
                def sync_wrapper(*args, **kwargs):
                    if not cls.is_enabled(feature_name):
                        raise RuntimeError(f"Feature '{feature_name}' is not enabled")
                    return func(*args, **kwargs)
                return sync_wrapper
        
        return decorator
    
    @classmethod
    def get_summary(cls) -> Dict[str, Any]:
        """Get summary of current feature flag state"""
        return cls.get_features().get_summary()


# Convenience functions
def get_features() -> V11Features:
    """Get current feature flags"""
    return FeatureFlagManager.get_features()


def is_enabled(feature_name: str) -> bool:
    """Check if a feature is enabled"""
    return FeatureFlagManager.is_enabled(feature_name)


def require_feature(feature_name: str):
    """Decorator to require a feature"""
    return FeatureFlagManager.require_feature(feature_name)

