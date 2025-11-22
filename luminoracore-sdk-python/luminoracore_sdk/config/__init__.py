"""Configuration utilities for LuminoraCore SDK."""

import json
from pathlib import Path
from typing import Dict, Optional

_config_cache: Optional[Dict] = None


def get_provider_urls() -> Dict[str, Dict[str, str]]:
    """
    Load provider URLs from configuration file.
    
    Returns:
        Dictionary with provider configurations
    """
    global _config_cache
    
    if _config_cache is not None:
        return _config_cache
    
    config_path = Path(__file__).parent / "provider_urls.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            _config_cache = config.get("providers", {})
            
            # Merge custom providers if any
            custom = config.get("custom_providers", {})
            for key, value in custom.items():
                if not key.startswith("_"):  # Skip comments
                    _config_cache[key] = value
            
            return _config_cache
    except Exception as e:
        # Fallback to empty dict if config file is missing
        print(f"Warning: Could not load provider_urls.json: {e}")
        return {}


def get_provider_base_url(provider_name: str) -> Optional[str]:
    """
    Get base URL for a specific provider.
    
    Args:
        provider_name: Name of the provider (e.g., 'openai', 'anthropic')
    
    Returns:
        Base URL string or None if not found
    """
    urls = get_provider_urls()
    provider_config = urls.get(provider_name.lower())
    
    if provider_config:
        return provider_config.get("base_url")
    
    return None


def get_provider_default_model(provider_name: str) -> Optional[str]:
    """
    Get default model for a specific provider.
    
    Args:
        provider_name: Name of the provider (e.g., 'openai', 'anthropic')
    
    Returns:
        Default model string or None if not found
    """
    urls = get_provider_urls()
    provider_config = urls.get(provider_name.lower())
    
    if provider_config:
        return provider_config.get("default_model")
    
    return None


__all__ = [
    "get_provider_urls",
    "get_provider_base_url",
    "get_provider_default_model",
]

