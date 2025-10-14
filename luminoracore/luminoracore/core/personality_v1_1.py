"""
LuminoraCore v1.1 - Personality Extensions

Extends v1.0 personality system with:
- Hierarchical relationship levels
- Dynamic mood states
- Affinity-based adaptation

These are EXTENSIONS - v1.0 Personality class remains unchanged.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class RelationshipLevel(Enum):
    """Standard relationship level names"""
    STRANGER = "stranger"
    ACQUAINTANCE = "acquaintance"
    FRIEND = "friend"
    CLOSE_FRIEND = "close_friend"
    SOULMATE = "soulmate"


@dataclass
class AffinityRange:
    """Defines an affinity point range for a relationship level"""
    min_points: int  # 0-100
    max_points: int  # 0-100
    
    def contains(self, points: int) -> bool:
        """Check if points fall within this range"""
        return self.min_points <= points <= self.max_points
    
    def __post_init__(self):
        """Validate range on creation"""
        if not (0 <= self.min_points <= 100):
            raise ValueError(f"min_points must be 0-100, got {self.min_points}")
        if not (0 <= self.max_points <= 100):
            raise ValueError(f"max_points must be 0-100, got {self.max_points}")
        if self.min_points > self.max_points:
            raise ValueError(f"min_points cannot be greater than max_points")


@dataclass
class ParameterModifiers:
    """Modifiers to apply to advanced_parameters (DELTAS)"""
    empathy: float = 0.0
    formality: float = 0.0
    verbosity: float = 0.0
    humor: float = 0.0
    creativity: float = 0.0
    directness: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {
            "empathy": self.empathy,
            "formality": self.formality,
            "verbosity": self.verbosity,
            "humor": self.humor,
            "creativity": self.creativity,
            "directness": self.directness
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'ParameterModifiers':
        """Create from dictionary"""
        valid_keys = {k: v for k, v in data.items() if k in cls.__annotations__}
        return cls(**valid_keys)
    
    def apply_to(self, base_params: Dict[str, float]) -> Dict[str, float]:
        """Apply modifiers to base parameters"""
        result = base_params.copy()
        for key, delta in self.to_dict().items():
            if key in result and delta != 0.0:
                new_value = result[key] + delta
                result[key] = max(0.0, min(1.0, new_value))  # Clamp to [0, 1]
        return result


@dataclass
class LinguisticModifiers:
    """Modifiers to apply to linguistic_profile (ADDITIONS)"""
    tone_additions: List[str] = field(default_factory=list)
    expression_additions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, List[str]]:
        """Convert to dictionary"""
        return {
            "tone_additions": self.tone_additions,
            "expression_additions": self.expression_additions
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, List[str]]) -> 'LinguisticModifiers':
        """Create from dictionary"""
        return cls(
            tone_additions=data.get('tone_additions', []),
            expression_additions=data.get('expression_additions', [])
        )
    
    def apply_to(self, base_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Apply linguistic modifiers to base profile"""
        result = base_profile.copy()
        
        # Add tones
        if self.tone_additions and 'tone' in result:
            if isinstance(result['tone'], list):
                result['tone'] = result['tone'] + self.tone_additions
            else:
                result['tone'] = [result['tone']] + self.tone_additions
        
        # Add expressions
        if self.expression_additions:
            if 'expressions' in result:
                if isinstance(result['expressions'], list):
                    result['expressions'] = result['expressions'] + self.expression_additions
                else:
                    result['expressions'] = [result['expressions']] + self.expression_additions
            else:
                result['expressions'] = self.expression_additions
        
        return result


@dataclass
class SystemPromptModifiers:
    """Modifiers to apply to system prompt"""
    prefix: str = ""
    suffix: str = ""
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary"""
        return {"prefix": self.prefix, "suffix": self.suffix}
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'SystemPromptModifiers':
        """Create from dictionary"""
        return cls(
            prefix=data.get('prefix', ''),
            suffix=data.get('suffix', '')
        )
    
    def apply_to(self, base_prompt: str) -> str:
        """Apply prompt modifiers to base system prompt"""
        result = base_prompt
        if self.prefix:
            result = self.prefix + result
        if self.suffix:
            result = result + self.suffix
        return result


@dataclass
class LevelModifiers:
    """Complete set of modifiers for a relationship level"""
    advanced_parameters: ParameterModifiers = field(default_factory=ParameterModifiers)
    linguistic_profile: LinguisticModifiers = field(default_factory=LinguisticModifiers)
    system_prompt_additions: SystemPromptModifiers = field(default_factory=SystemPromptModifiers)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "advanced_parameters": self.advanced_parameters.to_dict(),
            "linguistic_profile": self.linguistic_profile.to_dict(),
            "system_prompt_additions": self.system_prompt_additions.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LevelModifiers':
        """Create from dictionary"""
        return cls(
            advanced_parameters=ParameterModifiers.from_dict(
                data.get('advanced_parameters', {})
            ),
            linguistic_profile=LinguisticModifiers.from_dict(
                data.get('linguistic_profile', {})
            ),
            system_prompt_additions=SystemPromptModifiers.from_dict(
                data.get('system_prompt_additions', {})
            )
        )


@dataclass
class RelationshipLevelConfig:
    """Configuration for a single relationship level"""
    name: str
    affinity_range: AffinityRange
    description: str
    modifiers: LevelModifiers
    
    def applies_to_affinity(self, points: int) -> bool:
        """Check if this level applies to given affinity points"""
        return self.affinity_range.contains(points)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "affinity_range": [
                self.affinity_range.min_points,
                self.affinity_range.max_points
            ],
            "description": self.description,
            "modifiers": self.modifiers.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RelationshipLevelConfig':
        """Create from personality JSON dictionary"""
        affinity_range_list = data['affinity_range']
        
        return cls(
            name=data['name'],
            affinity_range=AffinityRange(
                min_points=affinity_range_list[0],
                max_points=affinity_range_list[1]
            ),
            description=data.get('description', ''),
            modifiers=LevelModifiers.from_dict(data.get('modifiers', {}))
        )


@dataclass
class MoodConfig:
    """Configuration for a mood state"""
    description: str
    modifiers: LevelModifiers
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "description": self.description,
            "modifiers": self.modifiers.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MoodConfig':
        """Create from dictionary"""
        return cls(
            description=data.get('description', ''),
            modifiers=LevelModifiers.from_dict(data.get('modifiers', {}))
        )


@dataclass
class HierarchicalConfig:
    """Hierarchical personality configuration"""
    enabled: bool = False
    relationship_levels: List[RelationshipLevelConfig] = field(default_factory=list)
    
    def get_level_for_affinity(self, points: int) -> Optional[RelationshipLevelConfig]:
        """Get the relationship level that applies to given affinity points"""
        for level in self.relationship_levels:
            if level.applies_to_affinity(points):
                return level
        return None
    
    def get_level_names(self) -> List[str]:
        """Get list of all level names"""
        return [level.name for level in self.relationship_levels]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "enabled": self.enabled,
            "relationship_levels": [
                level.to_dict() for level in self.relationship_levels
            ]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HierarchicalConfig':
        """Create from personality JSON dictionary"""
        return cls(
            enabled=data.get('enabled', False),
            relationship_levels=[
                RelationshipLevelConfig.from_dict(level)
                for level in data.get('relationship_levels', [])
            ]
        )


@dataclass
class MoodSystemConfig:
    """Mood system configuration"""
    enabled: bool = False
    moods: Dict[str, MoodConfig] = field(default_factory=dict)
    mood_triggers: Dict[str, List[str]] = field(default_factory=dict)
    mood_detection: Dict[str, Any] = field(default_factory=dict)
    
    def get_mood_config(self, mood_name: str) -> Optional[MoodConfig]:
        """Get configuration for a specific mood"""
        return self.moods.get(mood_name)
    
    def get_mood_names(self) -> List[str]:
        """Get list of all available mood names"""
        return list(self.moods.keys())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "enabled": self.enabled,
            "moods": {
                name: mood.to_dict() for name, mood in self.moods.items()
            },
            "mood_triggers": self.mood_triggers,
            "mood_detection": self.mood_detection
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MoodSystemConfig':
        """Create from personality JSON dictionary"""
        return cls(
            enabled=data.get('enabled', False),
            moods={
                name: MoodConfig.from_dict(mood_data)
                for name, mood_data in data.get('moods', {}).items()
            },
            mood_triggers=data.get('mood_triggers', {}),
            mood_detection=data.get('mood_detection', {})
        )


@dataclass
class PersonalityV11Extensions:
    """v1.1 extensions that can be added to a v1.0 personality"""
    hierarchical_config: Optional[HierarchicalConfig] = None
    mood_config: Optional[MoodSystemConfig] = None
    
    @classmethod
    def from_personality_dict(cls, personality_dict: Dict[str, Any]) -> 'PersonalityV11Extensions':
        """Extract v1.1 extensions from personality dictionary"""
        extensions = cls()
        
        # Load hierarchical config if present
        if 'hierarchical_config' in personality_dict:
            extensions.hierarchical_config = HierarchicalConfig.from_dict(
                personality_dict['hierarchical_config']
            )
        
        # Load mood config if present
        if 'mood_config' in personality_dict:
            extensions.mood_config = MoodSystemConfig.from_dict(
                personality_dict['mood_config']
            )
        
        return extensions
    
    def has_hierarchical(self) -> bool:
        """Check if hierarchical personality is configured and enabled"""
        return (
            self.hierarchical_config is not None and
            self.hierarchical_config.enabled
        )
    
    def has_moods(self) -> bool:
        """Check if mood system is configured and enabled"""
        return (
            self.mood_config is not None and
            self.mood_config.enabled
        )
    
    def is_v1_0_only(self) -> bool:
        """Check if this is a pure v1.0 personality (no v1.1 features)"""
        return not (self.has_hierarchical() or self.has_moods())

