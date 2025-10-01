"""Configuration validation for LuminoraCore CLI."""

from typing import Dict, Any, List
from .settings import Settings


def validate_config(config_data: Dict[str, Any]) -> List[str]:
    """
    Validate configuration data.
    
    Args:
        config_data: Configuration dictionary to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Validate cache settings
    if "cache_dir" in config_data:
        try:
            from pathlib import Path
            Path(config_data["cache_dir"]).resolve()
        except Exception:
            errors.append("Invalid cache_dir path")
    
    if "max_cache_size" in config_data:
        if not isinstance(config_data["max_cache_size"], int) or config_data["max_cache_size"] <= 0:
            errors.append("max_cache_size must be a positive integer")
    
    if "cache_ttl" in config_data:
        if not isinstance(config_data["cache_ttl"], int) or config_data["cache_ttl"] <= 0:
            errors.append("cache_ttl must be a positive integer")
    
    # Validate repository settings
    if "repository_url" in config_data:
        if not isinstance(config_data["repository_url"], str) or not config_data["repository_url"]:
            errors.append("repository_url must be a non-empty string")
    
    if "timeout" in config_data:
        if not isinstance(config_data["timeout"], int) or config_data["timeout"] <= 0:
            errors.append("timeout must be a positive integer")
    
    if "max_retries" in config_data:
        if not isinstance(config_data["max_retries"], int) or config_data["max_retries"] < 0:
            errors.append("max_retries must be a non-negative integer")
    
    # Validate validation settings
    if "strict_validation" in config_data:
        if not isinstance(config_data["strict_validation"], bool):
            errors.append("strict_validation must be a boolean")
    
    # Validate compilation settings
    if "default_provider" in config_data:
        valid_providers = ["openai", "anthropic", "mistral", "cohere", "google", "llama"]
        if config_data["default_provider"] not in valid_providers:
            errors.append(f"default_provider must be one of: {', '.join(valid_providers)}")
    
    if "default_model" in config_data:
        if not isinstance(config_data["default_model"], str) or not config_data["default_model"]:
            errors.append("default_model must be a non-empty string")
    
    if "include_metadata" in config_data:
        if not isinstance(config_data["include_metadata"], bool):
            errors.append("include_metadata must be a boolean")
    
    # Validate server settings
    if "default_port" in config_data:
        if not isinstance(config_data["default_port"], int) or not (1024 <= config_data["default_port"] <= 65535):
            errors.append("default_port must be an integer between 1024 and 65535")
    
    if "default_host" in config_data:
        if not isinstance(config_data["default_host"], str) or not config_data["default_host"]:
            errors.append("default_host must be a non-empty string")
    
    if "auto_reload" in config_data:
        if not isinstance(config_data["auto_reload"], bool):
            errors.append("auto_reload must be a boolean")
    
    # Validate UI settings
    if "theme" in config_data:
        valid_themes = ["default", "dark", "light", "monokai"]
        if config_data["theme"] not in valid_themes:
            errors.append(f"theme must be one of: {', '.join(valid_themes)}")
    
    if "color_output" in config_data:
        if not isinstance(config_data["color_output"], bool):
            errors.append("color_output must be a boolean")
    
    if "progress_bars" in config_data:
        if not isinstance(config_data["progress_bars"], bool):
            errors.append("progress_bars must be a boolean")
    
    if "table_style" in config_data:
        if not isinstance(config_data["table_style"], str) or not config_data["table_style"]:
            errors.append("table_style must be a non-empty string")
    
    # Validate logging settings
    if "log_level" in config_data:
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if config_data["log_level"].upper() not in valid_levels:
            errors.append(f"log_level must be one of: {', '.join(valid_levels)}")
    
    if "log_file" in config_data and config_data["log_file"] is not None:
        try:
            from pathlib import Path
            Path(config_data["log_file"]).resolve()
        except Exception:
            errors.append("Invalid log_file path")
    
    return errors
