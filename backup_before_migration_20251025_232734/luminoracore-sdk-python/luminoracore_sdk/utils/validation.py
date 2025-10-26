"""Validation utilities for LuminoraCore SDK."""

from typing import Any, Dict, List, Optional, Union
import re

from ..types.session import SessionConfig, StorageConfig, MemoryConfig
from ..types.provider import ProviderConfig
from ..types.personality import PersonalityData
from .exceptions import ValidationError


def validate_session_config(config: SessionConfig) -> bool:
    """
    Validate session configuration.
    
    Args:
        config: Session configuration to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If configuration is invalid
    """
    if not config.session_id:
        raise ValidationError("Session ID is required")
    
    if not config.personality:
        raise ValidationError("Personality is required")
    
    if config.max_history < 0:
        raise ValidationError("Max history must be non-negative")
    
    if config.timeout and config.timeout <= 0:
        raise ValidationError("Timeout must be positive")
    
    return True


def validate_personality_data(personality: PersonalityData) -> bool:
    """
    Validate personality data.
    
    Args:
        personality: Personality data to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If personality data is invalid
    """
    if not personality.name:
        raise ValidationError("Personality name is required")
    
    if not personality.description:
        raise ValidationError("Personality description is required")
    
    if not personality.system_prompt:
        raise ValidationError("System prompt is required")
    
    if personality.name_override and len(personality.name_override) > 50:
        raise ValidationError("Name override must be 50 characters or less")
    
    if personality.description_override and len(personality.description_override) > 200:
        raise ValidationError("Description override must be 200 characters or less")
    
    return True


def validate_provider_config(config: ProviderConfig) -> bool:
    """
    Validate provider configuration.
    
    Args:
        config: Provider configuration to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If configuration is invalid
    """
    if not config.name:
        raise ValidationError("Provider name is required")
    
    if not config.api_key:
        raise ValidationError("API key is required")
    
    if config.base_url and not _is_valid_url(config.base_url):
        raise ValidationError("Invalid base URL")
    
    if config.timeout and config.timeout <= 0:
        raise ValidationError("Timeout must be positive")
    
    if config.max_retries and config.max_retries < 0:
        raise ValidationError("Max retries must be non-negative")
    
    return True


def validate_storage_config(config: StorageConfig) -> bool:
    """
    Validate storage configuration.
    
    Args:
        config: Storage configuration to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If configuration is invalid
    """
    if not config.storage_type:
        raise ValidationError("Storage type is required")
    
    if config.storage_type == "redis" and not config.redis_url:
        raise ValidationError("Redis URL is required for Redis storage")
    
    if config.storage_type == "postgresql" and not config.postgres_url:
        raise ValidationError("PostgreSQL URL is required for PostgreSQL storage")
    
    if config.storage_type == "mongodb" and not config.mongodb_url:
        raise ValidationError("MongoDB URL is required for MongoDB storage")
    
    return True


def validate_memory_config(config: MemoryConfig) -> bool:
    """
    Validate memory configuration.
    
    Args:
        config: Memory configuration to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If configuration is invalid
    """
    if config.max_tokens and config.max_tokens <= 0:
        raise ValidationError("Max tokens must be positive")
    
    if config.max_messages and config.max_messages <= 0:
        raise ValidationError("Max messages must be positive")
    
    if config.ttl and config.ttl <= 0:
        raise ValidationError("TTL must be positive")
    
    return True


def validate_api_key(api_key: str) -> bool:
    """
    Validate API key format.
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If API key is invalid
    """
    if not api_key or not isinstance(api_key, str):
        raise ValidationError("API key must be a non-empty string")
    
    if len(api_key) < 10:
        raise ValidationError("API key is too short")
    
    if len(api_key) > 200:
        raise ValidationError("API key is too long")
    
    return True


def validate_session_id(session_id: str) -> bool:
    """
    Validate session ID format.
    
    Args:
        session_id: Session ID to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If session ID is invalid
    """
    if not session_id or not isinstance(session_id, str):
        raise ValidationError("Session ID must be a non-empty string")
    
    if len(session_id) < 10:
        raise ValidationError("Session ID is too short")
    
    if len(session_id) > 100:
        raise ValidationError("Session ID is too long")
    
    # Check for valid characters (alphanumeric, hyphens, underscores)
    if not re.match(r'^[a-zA-Z0-9_-]+$', session_id):
        raise ValidationError("Session ID contains invalid characters")
    
    return True


def validate_personality_blend(blend_config: Dict[str, float]) -> bool:
    """
    Validate personality blend configuration.
    
    Args:
        blend_config: Personality blend configuration
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If blend configuration is invalid
    """
    if not blend_config:
        raise ValidationError("Blend configuration cannot be empty")
    
    total_weight = sum(blend_config.values())
    if abs(total_weight - 1.0) > 0.01:  # Allow small floating point errors
        raise ValidationError(f"Blend weights must sum to 1.0, got {total_weight}")
    
    for personality, weight in blend_config.items():
        if not isinstance(weight, (int, float)):
            raise ValidationError(f"Weight for {personality} must be a number")
        
        if weight < 0 or weight > 1:
            raise ValidationError(f"Weight for {personality} must be between 0 and 1")
    
    return True


def _is_valid_url(url: str) -> bool:
    """Check if a string is a valid URL."""
    try:
        from urllib.parse import urlparse
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_message_content(content: str) -> bool:
    """
    Validate message content.
    
    Args:
        content: Message content to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If content is invalid
    """
    if not content or not isinstance(content, str):
        raise ValidationError("Message content must be a non-empty string")
    
    if len(content) > 100000:  # 100KB limit
        raise ValidationError("Message content is too long")
    
    return True


def validate_temperature(temperature: float) -> bool:
    """
    Validate temperature parameter.
    
    Args:
        temperature: Temperature to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If temperature is invalid
    """
    if not isinstance(temperature, (int, float)):
        raise ValidationError("Temperature must be a number")
    
    if temperature < 0 or temperature > 2:
        raise ValidationError("Temperature must be between 0 and 2")
    
    return True


def validate_max_tokens(max_tokens: int) -> bool:
    """
    Validate max tokens parameter.
    
    Args:
        max_tokens: Max tokens to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If max tokens is invalid
    """
    if not isinstance(max_tokens, int):
        raise ValidationError("Max tokens must be an integer")
    
    if max_tokens <= 0:
        raise ValidationError("Max tokens must be positive")
    
    if max_tokens > 100000:
        raise ValidationError("Max tokens is too high")
    
    return True
