"""
Core Personality class for LuminoraCore.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict

from .schema import PersonalitySchema


class PersonalityError(Exception):
    """Custom exception for personality-related errors."""
    pass


@dataclass
class PersonaInfo:
    """Persona metadata information."""
    name: str
    version: str
    description: str
    author: str
    tags: List[str]
    language: str
    compatibility: List[str]


@dataclass
class CoreTraits:
    """Core personality traits."""
    archetype: str
    temperament: str
    communication_style: str


@dataclass
class LinguisticProfile:
    """Linguistic characteristics of the personality."""
    tone: List[str]
    syntax: str
    vocabulary: List[str]
    fillers: Optional[List[str]] = None
    punctuation_style: Optional[str] = None


@dataclass
class AdvancedParameters:
    """Advanced behavioral parameters."""
    verbosity: Optional[float] = None
    formality: Optional[float] = None
    humor: Optional[float] = None
    empathy: Optional[float] = None
    creativity: Optional[float] = None
    directness: Optional[float] = None


@dataclass
class TriggerResponses:
    """Responses to specific triggers."""
    on_greeting: Optional[List[str]] = None
    on_confusion: Optional[List[str]] = None
    on_success: Optional[List[str]] = None
    on_error: Optional[List[str]] = None
    on_goodbye: Optional[List[str]] = None


@dataclass
class SafetyGuards:
    """Safety and content filtering settings."""
    forbidden_topics: Optional[List[str]] = None
    tone_limits: Optional[Dict[str, float]] = None
    content_filters: Optional[List[str]] = None


@dataclass
class SampleResponse:
    """Example interaction."""
    input: str
    output: str
    context: Optional[str] = None


@dataclass
class Examples:
    """Example interactions for the personality."""
    sample_responses: List[SampleResponse]


@dataclass
class Metadata:
    """Personality metadata."""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    downloads: Optional[int] = None
    rating: Optional[float] = None
    license: Optional[str] = None


class Personality:
    """Main personality class for LuminoraCore."""
    
    def __init__(self, data: Union[Dict[str, Any], str, Path]):
        """
        Initialize a personality from data or file.
        
        Args:
            data: Dictionary containing personality data, or path to JSON file
            
        Raises:
            PersonalityError: If data is invalid or file cannot be loaded
        """
        if isinstance(data, (str, Path)):
            self._load_from_file(data)
        else:
            self._load_from_data(data)
        
        # Validate against schema
        schema = PersonalitySchema()
        schema.validate(self._raw_data)
    
    def _load_from_file(self, file_path: Union[str, Path]) -> None:
        """Load personality from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self._raw_data = json.load(f)
            self._file_path = Path(file_path)
        except FileNotFoundError:
            raise PersonalityError(f"Personality file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise PersonalityError(f"Invalid JSON in personality file: {e}")
    
    def _load_from_data(self, data: Dict[str, Any]) -> None:
        """Load personality from dictionary data."""
        self._raw_data = data.copy()
        self._file_path = None
    
    @property
    def persona(self) -> PersonaInfo:
        """Get persona information."""
        return PersonaInfo(**self._raw_data["persona"])
    
    @property
    def core_traits(self) -> CoreTraits:
        """Get core personality traits."""
        return CoreTraits(**self._raw_data["core_traits"])
    
    @property
    def linguistic_profile(self) -> LinguisticProfile:
        """Get linguistic profile."""
        return LinguisticProfile(**self._raw_data["linguistic_profile"])
    
    @property
    def behavioral_rules(self) -> List[str]:
        """Get behavioral rules."""
        return self._raw_data["behavioral_rules"]
    
    @property
    def trigger_responses(self) -> Optional[TriggerResponses]:
        """Get trigger responses."""
        if "trigger_responses" in self._raw_data:
            return TriggerResponses(**self._raw_data["trigger_responses"])
        return None
    
    @property
    def advanced_parameters(self) -> Optional[AdvancedParameters]:
        """Get advanced parameters."""
        if "advanced_parameters" in self._raw_data:
            return AdvancedParameters(**self._raw_data["advanced_parameters"])
        return None
    
    @property
    def safety_guards(self) -> Optional[SafetyGuards]:
        """Get safety guards."""
        if "safety_guards" in self._raw_data:
            return SafetyGuards(**self._raw_data["safety_guards"])
        return None
    
    @property
    def examples(self) -> Optional[Examples]:
        """Get examples."""
        if "examples" in self._raw_data and "sample_responses" in self._raw_data["examples"]:
            sample_responses = [
                SampleResponse(**resp) 
                for resp in self._raw_data["examples"]["sample_responses"]
            ]
            return Examples(sample_responses=sample_responses)
        return None
    
    @property
    def metadata(self) -> Optional[Metadata]:
        """Get metadata."""
        if "metadata" in self._raw_data:
            return Metadata(**self._raw_data["metadata"])
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert personality to dictionary."""
        return self._raw_data.copy()
    
    def to_json(self, indent: int = 2) -> str:
        """Convert personality to JSON string."""
        return json.dumps(self._raw_data, indent=indent, ensure_ascii=False)
    
    def save(self, file_path: Optional[Union[str, Path]] = None) -> None:
        """
        Save personality to JSON file.
        
        Args:
            file_path: Path to save the file. If None, uses original file path.
        """
        if file_path is None:
            if self._file_path is None:
                raise PersonalityError("No file path specified for saving")
            file_path = self._file_path
        
        file_path = Path(file_path)
        
        # Update metadata
        if "metadata" not in self._raw_data:
            self._raw_data["metadata"] = {}
        
        if self._raw_data["metadata"].get("created_at") is None:
            self._raw_data["metadata"]["created_at"] = datetime.utcnow().isoformat()
        
        self._raw_data["metadata"]["updated_at"] = datetime.utcnow().isoformat()
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self._raw_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise PersonalityError(f"Failed to save personality: {e}")
    
    def get_compatibility(self) -> List[str]:
        """Get list of compatible LLM providers."""
        return self.persona.compatibility
    
    def is_compatible_with(self, provider: str) -> bool:
        """Check if personality is compatible with a specific provider."""
        return provider in self.persona.compatibility
    
    def get_tags(self) -> List[str]:
        """Get personality tags."""
        return self.persona.tags
    
    def has_tag(self, tag: str) -> bool:
        """Check if personality has a specific tag."""
        return tag in self.persona.tags
