"""Helper utilities for LuminoraCore SDK."""

import uuid
import json
from datetime import datetime
from typing import Any, Dict, Optional, Union
from pathlib import Path


def generate_session_id() -> str:
    """Generate a unique session ID."""
    return str(uuid.uuid4())


def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """Format a timestamp for display."""
    if timestamp is None:
        timestamp = datetime.utcnow()
    return timestamp.isoformat()


def parse_config(config: Union[str, Dict, Path]) -> Dict[str, Any]:
    """
    Parse configuration from various formats.
    
    Args:
        config: Configuration as string (JSON), dict, or Path to file
        
    Returns:
        Parsed configuration dictionary
        
    Raises:
        ValueError: If configuration format is invalid
    """
    if isinstance(config, dict):
        return config
    
    if isinstance(config, str):
        try:
            return json.loads(config)
        except json.JSONDecodeError:
            # Try as file path
            config_path = Path(config)
            if config_path.exists():
                return parse_config(config_path)
            else:
                raise ValueError(f"Invalid configuration: {config}")
    
    if isinstance(config, Path):
        if not config.exists():
            raise ValueError(f"Configuration file not found: {config}")
        
        suffix = config.suffix.lower()
        if suffix == '.json':
            with open(config, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported configuration file format: {suffix}")
    
    raise ValueError(f"Invalid configuration type: {type(config)}")


def sanitize_api_key(api_key: str, show_chars: int = 4) -> str:
    """
    Sanitize API key for logging.
    
    Args:
        api_key: API key to sanitize
        show_chars: Number of characters to show at the end
        
    Returns:
        Sanitized API key
    """
    if not api_key or len(api_key) <= show_chars:
        return "***"
    
    return "*" * (len(api_key) - show_chars) + api_key[-show_chars:]


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two dictionaries, with dict2 taking precedence.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary (takes precedence)
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    result.update(dict2)
    return result


def deep_merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary (takes precedence)
        
    Returns:
        Deep merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes into human readable format.
    
    Args:
        bytes_value: Number of bytes
        
    Returns:
        Formatted string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"


def validate_url(url: str) -> bool:
    """
    Validate if a string is a valid URL.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid URL, False otherwise
    """
    try:
        from urllib.parse import urlparse
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_personality_data(data: Dict[str, Any]) -> bool:
    """
    Validate personality data structure.
    
    Args:
        data: Personality data to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = [
        'name', 'version', 'description', 'persona', 
        'core_traits', 'linguistic_profile', 'behavioral_rules'
    ]
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            return False
    
    # Check data types
    if not isinstance(data.get('name'), str):
        return False
    if not isinstance(data.get('version'), str):
        return False
    if not isinstance(data.get('description'), str):
        return False
    if not isinstance(data.get('persona'), dict):
        return False
    if not isinstance(data.get('core_traits'), list):
        return False
    if not isinstance(data.get('linguistic_profile'), dict):
        return False
    if not isinstance(data.get('behavioral_rules'), list):
        return False
    
    return True