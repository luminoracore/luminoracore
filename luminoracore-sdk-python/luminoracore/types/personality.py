"""Personality-related type definitions."""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, ConfigDict


class PersonalityType(str, Enum):
    """Personality type enumeration."""
    INDIVIDUAL = "individual"
    BLENDED = "blended"
    CUSTOM = "custom"


class PersonalityData(BaseModel):
    """Personality data structure."""
    
    name: str = Field(..., description="Personality name")
    version: str = Field(..., description="Personality version")
    description: str = Field(..., description="Personality description")
    author: Optional[str] = Field(None, description="Personality author")
    tags: List[str] = Field(default_factory=list, description="Personality tags")
    
    # Core personality structure
    persona: Dict[str, Any] = Field(..., description="Persona definition")
    core_traits: List[str] = Field(..., description="Core personality traits")
    linguistic_profile: Dict[str, Any] = Field(..., description="Linguistic profile")
    behavioral_rules: List[str] = Field(..., description="Behavioral rules")
    advanced_parameters: Dict[str, Any] = Field(default_factory=dict, description="Advanced parameters")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    model_config = ConfigDict(
        extra="allow",
        validate_assignment=True
    )


class PersonalityBlend(BaseModel):
    """Personality blend configuration."""
    
    personalities: List[PersonalityData] = Field(..., description="Personalities to blend")
    weights: List[float] = Field(..., description="Blend weights for each personality")
    blend_type: str = Field(default="weighted", description="Type of blending")
    custom_rules: Optional[Dict[str, Any]] = Field(None, description="Custom blending rules")
    
    model_config = ConfigDict(
        extra="allow",
        validate_assignment=True
    )
