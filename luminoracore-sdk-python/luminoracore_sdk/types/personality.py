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
    description: str = Field(..., description="Personality description")
    system_prompt: str = Field(..., description="System prompt for the personality")
    name_override: Optional[str] = Field(None, description="Override for display name")
    description_override: Optional[str] = Field(None, description="Override for display description")
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
