"""Settings management for LuminoraCore CLI."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Dict, Any
import json
import yaml

from pydantic import BaseModel, Field, field_validator, ConfigDict
from .defaults import DEFAULT_SETTINGS


class Settings(BaseModel):
    """CLI settings configuration."""
    
    # Cache settings
    cache_dir: Path = Field(default_factory=lambda: Path.home() / ".luminoracore" / "cache")
    max_cache_size: int = Field(default=1024 * 1024 * 1024)  # 1GB
    cache_ttl: int = Field(default=86400)  # 24 hours
    
    # Repository settings
    repository_url: str = Field(default="https://api.luminoracore.com/v1")
    api_key: Optional[str] = Field(default=None)
    timeout: int = Field(default=30)
    max_retries: int = Field(default=3)
    
    # Validation settings
    strict_validation: bool = Field(default=False)
    schema_url: Optional[str] = Field(default=None)
    
    # Compilation settings
    default_provider: str = Field(default="openai")
    default_model: str = Field(default="gpt-3.5-turbo")
    include_metadata: bool = Field(default=True)
    
    # Server settings
    default_port: int = Field(default=8000)
    default_host: str = Field(default="127.0.0.1")
    auto_reload: bool = Field(default=True)
    
    # UI settings
    theme: str = Field(default="default")
    color_output: bool = Field(default=True)
    progress_bars: bool = Field(default=True)
    table_style: str = Field(default="default")
    
    # Logging settings
    log_level: str = Field(default="INFO")
    log_file: Optional[Path] = Field(default=None)
    
    @field_validator('cache_dir')
    @classmethod
    def validate_cache_dir(cls, v):
        """Ensure cache directory exists."""
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log level: {v}")
        return v.upper()
    
    @field_validator('theme')
    @classmethod
    def validate_theme(cls, v):
        """Validate theme."""
        valid_themes = ['default', 'dark', 'light', 'monokai']
        if v.lower() not in valid_themes:
            raise ValueError(f"Invalid theme: {v}")
        return v.lower()
    
    @field_validator('timeout')
    @classmethod
    def validate_timeout(cls, v):
        """Validate timeout value."""
        if v < 0:
            raise ValueError("Timeout must be non-negative")
        return v
    
    @field_validator('max_retries')
    @classmethod
    def validate_max_retries(cls, v):
        """Validate max_retries value."""
        if v < 0:
            raise ValueError("Max retries must be non-negative")
        return v
    
    @field_validator('default_port')
    @classmethod
    def validate_default_port(cls, v):
        """Validate default_port value."""
        if v < 1 or v > 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v
    
    model_config = ConfigDict(
        env_prefix="LUMINORACORE_",
        case_sensitive=False
    )


def load_settings(config_file: Optional[Path] = None) -> Settings:
    """
    Load settings from file or environment.
    
    Args:
        config_file: Optional path to configuration file (str or Path)
        
    Returns:
        Settings object
    """
    # Start with defaults
    settings_data = DEFAULT_SETTINGS.copy()
    
    # Convert string to Path if needed
    if config_file and isinstance(config_file, str):
        config_file = Path(config_file)
    
    # Load from file if provided
    if config_file and config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                if config_file.suffix.lower() in ['.yaml', '.yml']:
                    file_data = yaml.safe_load(f)
                else:
                    file_data = json.load(f)
                
                if file_data:
                    settings_data.update(file_data)
        except Exception as e:
            raise ValueError(f"Failed to load config file {config_file}: {e}")
    
    # Load from default config locations
    default_config_paths = [
        Path.cwd() / "luminoracore.yaml",
        Path.cwd() / "luminoracore.yml", 
        Path.cwd() / "luminoracore.json",
        Path.home() / ".luminoracore" / "config.yaml",
        Path.home() / ".luminoracore" / "config.yml",
        Path.home() / ".luminoracore" / "config.json",
    ]
    
    for config_path in default_config_paths:
        if config_path.exists() and config_path != config_file:
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    if config_path.suffix.lower() in ['.yaml', '.yml']:
                        file_data = yaml.safe_load(f)
                    else:
                        file_data = json.load(f)
                    
                    if file_data:
                        settings_data.update(file_data)
                        break
            except Exception:
                continue  # Skip invalid config files
    
    # Override with environment variables
    env_settings = {}
    for key, value in os.environ.items():
        if key.startswith("LUMINORACORE_"):
            setting_key = key[13:].lower()  # Remove prefix and convert to lowercase
            
            # Convert string values to appropriate types
            if setting_key in ['cache_dir', 'log_file']:
                env_settings[setting_key] = Path(value)
            elif setting_key in ['max_cache_size', 'cache_ttl', 'timeout', 'max_retries', 'default_port']:
                env_settings[setting_key] = int(value)
            elif setting_key in ['strict_validation', 'include_metadata', 'auto_reload', 'color_output', 'progress_bars']:
                env_settings[setting_key] = value.lower() in ['true', '1', 'yes', 'on']
            else:
                env_settings[setting_key] = value
    
    settings_data.update(env_settings)
    
    # Expand cache_dir if it's a string with ~
    if 'cache_dir' in settings_data and isinstance(settings_data['cache_dir'], str):
        settings_data['cache_dir'] = Path(settings_data['cache_dir']).expanduser()
    
    # Create settings object
    try:
        return Settings(**settings_data)
    except Exception as e:
        raise ValueError(f"Invalid configuration: {e}")


def save_settings(settings: Settings, config_file: Path) -> None:
    """
    Save settings to file.
    
    Args:
        settings: Settings object to save
        config_file: Path to save configuration to
    """
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    settings_dict = settings.dict()
    
    # Convert Path objects to strings for JSON serialization
    for key, value in settings_dict.items():
        if isinstance(value, Path):
            settings_dict[key] = str(value)
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            if config_file.suffix.lower() in ['.yaml', '.yml']:
                yaml.dump(settings_dict, f, default_flow_style=False, indent=2)
            else:
                json.dump(settings_dict, f, indent=2)
    except Exception as e:
        raise ValueError(f"Failed to save config file {config_file}: {e}")
