"""Default configuration for LuminoraCore CLI."""

DEFAULT_SETTINGS = {
    # Cache settings
    "cache_dir": "~/.luminoracore/cache",
    "max_cache_size": 1024 * 1024 * 1024,  # 1GB
    "cache_ttl": 86400,  # 24 hours
    
    # Repository settings
    "repository_url": "https://api.luminoracore.com/v1",
    "api_key": None,
    "timeout": 30,
    "max_retries": 3,
    
    # Validation settings
    "strict_validation": False,
    "schema_url": None,
    
    # Compilation settings
    "default_provider": "openai",
    "default_model": "gpt-3.5-turbo",
    "include_metadata": True,
    
    # Server settings
    "default_port": 8000,
    "default_host": "127.0.0.1",
    "auto_reload": True,
    
    # UI settings
    "theme": "default",
    "color_output": True,
    "progress_bars": True,
    "table_style": "default",
    
    # Logging settings
    "log_level": "INFO",
    "log_file": None,
}
