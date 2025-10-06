"""Tests for configuration management."""

import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
import tempfile
import yaml

from luminoracore_cli.config.settings import Settings, load_settings
from luminoracore_cli.config.defaults import DEFAULT_SETTINGS


class TestSettings:
    """Test cases for the Settings model."""
    
    def test_default_settings(self):
        """Test that default settings are applied correctly."""
        settings = Settings()
        
        # cache_dir gets expanded to full path, so compare with Path expansion
        assert settings.cache_dir == Path(DEFAULT_SETTINGS["cache_dir"]).expanduser()
        assert settings.repository_url == DEFAULT_SETTINGS["repository_url"]
        assert settings.api_key is None
        assert settings.timeout == DEFAULT_SETTINGS["timeout"]
        assert settings.max_retries == DEFAULT_SETTINGS["max_retries"]
        assert settings.strict_validation == DEFAULT_SETTINGS["strict_validation"]
        assert settings.default_provider == DEFAULT_SETTINGS["default_provider"]
        assert settings.default_model == DEFAULT_SETTINGS["default_model"]
    
    def test_custom_settings(self):
        """Test creating settings with custom values."""
        settings = Settings(
            cache_dir=Path("/custom/cache"),
            api_key="custom-key",
            timeout=60,
            strict_validation=True,
            default_provider="anthropic"
        )
        
        assert settings.cache_dir == Path("/custom/cache")
        assert settings.api_key == "custom-key"
        assert settings.timeout == 60
        assert settings.strict_validation is True
        assert settings.default_provider == "anthropic"
    
    def test_settings_validation(self):
        """Test settings validation."""
        # Test invalid timeout
        with pytest.raises(ValueError):
            Settings(timeout=-1)
        
        # Test invalid max_retries
        with pytest.raises(ValueError):
            Settings(max_retries=-1)
        
        # Test invalid port
        with pytest.raises(ValueError):
            Settings(default_port=0)
        
        # Test invalid log level
        with pytest.raises(ValueError):
            Settings(log_level="INVALID")


class TestLoadSettings:
    """Test cases for the load_settings function."""
    
    def test_load_settings_from_file(self, temp_dir):
        """Test loading settings from a YAML file."""
        config_data = {
            "cache_dir": "/custom/cache",
            "api_key": "test-key",
            "timeout": 45,
            "strict_validation": True,
            "default_provider": "anthropic"
        }
        
        config_file = temp_dir / "config.yaml"
        with open(config_file, "w") as f:
            yaml.dump(config_data, f)
        
        settings = load_settings(config_file=str(config_file))
        
        assert settings.cache_dir == Path("/custom/cache")
        assert settings.api_key == "test-key"
        assert settings.timeout == 45
        assert settings.strict_validation is True
        assert settings.default_provider == "anthropic"
    
    def test_load_settings_from_env(self):
        """Test loading settings from environment variables."""
        env_vars = {
            "LUMINORACORE_API_KEY": "env-key",
            "LUMINORACORE_DEFAULT_PROVIDER": "openai",
            "LUMINORACORE_TIMEOUT": "30",
            "LUMINORACORE_STRICT_VALIDATION": "true"
        }
        
        with patch.dict("os.environ", env_vars):
            settings = load_settings()
            
            assert settings.api_key == "env-key"
            assert settings.default_provider == "openai"
            assert settings.timeout == 30
            assert settings.strict_validation is True
    
    def test_load_settings_file_not_found(self):
        """Test loading settings when config file doesn't exist."""
        settings = load_settings(config_file="/nonexistent/config.yaml")
        
        # Should fall back to defaults and environment
        # Note: cache_dir from string doesn't get expanded, so compare as string
        assert str(settings.cache_dir) == str(Path(DEFAULT_SETTINGS["cache_dir"]).expanduser())
        assert settings.repository_url == DEFAULT_SETTINGS["repository_url"]
    
    def test_load_settings_invalid_yaml(self, temp_dir):
        """Test loading settings from invalid YAML file."""
        config_file = temp_dir / "invalid.yaml"
        config_file.write_text("invalid: yaml: content: [")
        
        # Should raise ValueError for invalid YAML
        with pytest.raises(ValueError, match="Failed to load config file"):
            load_settings(config_file=str(config_file))
    
    def test_load_settings_env_override_file(self, temp_dir):
        """Test that environment variables override file settings."""
        config_data = {
            "api_key": "file-key",
            "default_provider": "anthropic"
        }
        
        config_file = temp_dir / "config.yaml"
        with open(config_file, "w") as f:
            yaml.dump(config_data, f)
        
        env_vars = {
            "LUMINORACORE_API_KEY": "env-key",
            "LUMINORACORE_DEFAULT_PROVIDER": "openai"
        }
        
        with patch.dict("os.environ", env_vars):
            settings = load_settings(config_file=str(config_file))
            
            # Environment should override file
            assert settings.api_key == "env-key"
            assert settings.default_provider == "openai"
