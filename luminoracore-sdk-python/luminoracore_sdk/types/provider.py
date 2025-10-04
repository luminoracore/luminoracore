"""Provider-related type definitions."""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any, List


class ProviderType(str, Enum):
    """LLM provider type enumeration."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    LLAMA = "llama"
    MISTRAL = "mistral"
    COHERE = "cohere"
    GOOGLE = "google"


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class ChatResponse:
    content: str
    role: str = "assistant"
    finish_reason: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    model: Optional[str] = None
    provider_metadata: Optional[Dict[str, Any]] = None  # Metadatos adicionales del provider


@dataclass
class ProviderConfig:
    name: str
    api_key: Optional[str] = None
    model: Optional[str] = None
    base_url: Optional[str] = None
    extra: Dict[str, Any] = None

    def __post_init__(self):
        if self.extra is None:
            self.extra = {}
