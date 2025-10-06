"""Test configuration and fixtures."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock

from luminoracore_cli.config.settings import Settings


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_personality():
    """Sample personality data for testing."""
    return {
        "name": "Test Personality",
        "version": "1.0.0",
        "description": "A test personality for unit testing",
        "author": "Test Author",
        "tags": ["test", "example"],
        "persona": {
            "name": "Test Personality",
            "description": "A test personality for unit testing",
            "archetype": "assistant",
            "version": "1.0.0",
            "author": "Test Author",
            "tags": ["test", "example"]
        },
        "core_traits": [
            "helpful",
            "friendly",
            "accurate",
            "informative"
        ],
        "linguistic_profile": {
            "tone": ["friendly", "helpful"],
            "vocabulary": ["help", "assist", "provide", "explain"],
            "speech_patterns": ["I can help you", "Let me assist"],
            "formality_level": "casual",
            "response_length": "moderate"
        },
        "behavioral_rules": [
            "Be helpful and friendly",
            "Provide accurate information",
            "Ask clarifying questions when needed"
        ],
        "advanced_parameters": {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 500,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
    }


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    return Settings(
        cache_dir=Path("/tmp/test_cache"),
        repository_url="https://test.api.com/v1",
        api_key="test-key",
        timeout=30,
        max_retries=3,
        strict_validation=False,
        default_provider="openai",
        default_model="gpt-3.5-turbo",
        include_metadata=True,
        default_port=8000,
        default_host="127.0.0.1",
        auto_reload=True,
        theme="default",
        color_output=True,
        progress_bars=True,
        table_style="default",
        log_level="INFO"
    )


@pytest.fixture
def mock_client():
    """Mock LuminoraCore client for testing."""
    client = Mock()
    client.validate_personality.return_value = {"valid": True, "errors": []}
    client.compile_personality.return_value = "Test compiled prompt"
    client.get_personality.return_value = {"id": "test", "name": "Test"}
    client.list_personalities.return_value = [{"id": "test", "name": "Test"}]
    return client


@pytest.fixture
def personality_file(temp_dir, sample_personality):
    """Create a temporary personality file for testing."""
    import json
    
    personality_path = temp_dir / "test_personality.json"
    with open(personality_path, "w") as f:
        json.dump(sample_personality, f, indent=2)
    
    return personality_path
