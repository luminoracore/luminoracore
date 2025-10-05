# 🐍 LuminoraCore SDK Python

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/luminoracore/sdk-python)
[![Status](https://img.shields.io/badge/status-v1.0_ready-brightgreen.svg)](#)
[![Tests](https://img.shields.io/badge/tests-37%2F37_passing-brightgreen.svg)](#)

**✅ OFFICIAL PYTHON SDK - v1.0 PRODUCTION READY**

**LuminoraCore SDK Python** is the official Python client for advanced AI personality management. Provides a complete toolkit for building AI applications with sophisticated personality systems, session management, and multi-provider LLM support.

## Key Features

- **✅ Advanced Personality Management**: Create, blend, and manage AI personalities with ease
- **✅ Session Management**: Stateful conversations with persistent memory
- **✅ Multi-Provider Support**: Integration with OpenAI, Anthropic, DeepSeek, Mistral, Cohere, Google, Llama
- **✅ PersonaBlend™ Technology**: Real-time personality blending with custom weights
- **✅ Flexible Storage**: Memory, JSON File, SQLite, Redis, PostgreSQL, MongoDB
- **✅ Monitoring & Metrics**: Integrated observability with distributed tracing
- **✅ Async/Await Support**: Fully asynchronous API for high-performance applications
- **✅ Type Safety**: Comprehensive type definitions and validation
- **✅ Real API Connections**: Real APIs to all LLM providers
- **✅ Robust Error Handling**: Automatic retries and fallbacks
- **✅ Token Usage Tracking**: Real-time token monitoring and metrics

## Installation

```bash
pip install -e luminoracore-sdk-python/
```

## Quick Start

```python
import asyncio
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.types.session import StorageConfig

async def main():
    # Initialize the client
    client = LuminoraCoreClient()
    await client.initialize()
    
    # Configure storage (Redis, PostgreSQL, etc.)
    storage_config = StorageConfig(
        storage_type="redis",
        connection_string="redis://localhost:6379"
    )
    await client.configure_storage(storage_config)
    
    # Create provider configuration
    provider_config = ProviderConfig(
        name="openai",
        api_key="your-api-key",
        model="gpt-3.5-turbo",
        extra={"timeout": 30, "max_retries": 3}
    )
    
    # Create a session
    session_id = await client.create_session(
        personality_name="dr_luna",
        provider_config=provider_config
    )
    
    # Send a message (real connection to OpenAI)
    response = await client.send_message(
        session_id=session_id,
        message="Hello! Can you help me with quantum physics?"
    )
    
    print(f"Response: {response.content}")
    print(f"Tokens: {response.usage}")
    
    # Get metrics
    metrics = await client.get_session_metrics(session_id)
    print(f"Total messages: {metrics.total_messages}")
    
    # Cleanup
    await client.cleanup()

# Run the example
asyncio.run(main())
```

## Advanced Usage

### Personality Blending

```python
# Blend multiple personalities
blended_personality = await client.blend_personalities(
    personality_names=["creative_writer", "technical_expert"],
    weights=[0.3, 0.7],
    blend_name="creative_technical_expert"
)

# Create a session with the blended personality
session_id = await client.create_session(
    personality_name="creative_technical_expert",
    provider_config=provider_config
)
```

### Memory Management

```python
# Store session memory
await client.store_memory(
    session_id=session_id,
    key="user_preference",
    value="interested in AI personality blending",
    ttl=3600
)

# Retrieve memory
memory = await client.get_memory(session_id, "user_preference")
```

### Streaming Responses

```python
# Stream a response
async for chunk in client.stream_message(
    session_id=session_id,
    message="Tell me a story"
):
    print(chunk.content, end="", flush=True)
```

## Configuration

### Storage Configuration

```python
from luminoracore_sdk.types.session import StorageConfig

# In-memory storage (default - fastest)
storage_config = StorageConfig(
    storage_type="memory"
)

# JSON File storage (simple, portable)
storage_config = StorageConfig(
    storage_type="json",
    connection_string="./sessions.json"
)

# SQLite storage (perfect for mobile apps)
storage_config = StorageConfig(
    storage_type="sqlite",
    connection_string="./sessions.db"
)

# Redis storage (production-ready)
storage_config = StorageConfig(
    storage_type="redis",
    connection_string="redis://localhost:6379"
)

# PostgreSQL storage (enterprise-ready)
storage_config = StorageConfig(
    storage_type="postgres",
    connection_string="postgresql://user:password@localhost/db"
)

# MongoDB storage (document-based)
storage_config = StorageConfig(
    storage_type="mongodb",
    connection_string="mongodb://localhost:27017/db"
)
```

### Memory Configuration

```python
from luminoracore_sdk.types.session import MemoryConfig

memory_config = MemoryConfig(
    enabled=True,
    max_entries=1000,
    decay_factor=0.1,
    importance_threshold=0.5,
    track_topics=True,
    track_preferences=True,
    track_context=True,
    track_emotions=False
)
```

## Supported Providers (7 Total)

- **OpenAI**: GPT-3.5, GPT-4, and other OpenAI models
- **Anthropic**: Claude-3 Sonnet, Claude-3 Haiku, and other Claude models
- **DeepSeek**: DeepSeek Chat (Cost-effective option)
- **Mistral**: Mistral Tiny, Mistral Small, and other Mistral models
- **Cohere**: Command, Command Light, and other Cohere models
- **Google**: Gemini Pro, Gemini Ultra, and other Google models
- **Llama**: Llama-2, Llama-3, and other Llama models

## Examples

Check out the `examples/` directory for comprehensive examples:

- `basic_usage.py` - Basic usage examples
- `simple_usage.py` - Simple usage examples
- `personality_blending.py` - Personality blending examples
- `integrations/fastapi_integration.py` - FastAPI integration
- `integrations/streamlit_app.py` - Streamlit web app

## Testing

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run all tests with coverage
pytest --cov=luminoracore tests/
```

## Development

```bash
# Clone the repository
git clone https://github.com/luminoracore/sdk-python.git
cd sdk-python

# Install development dependencies
pip install -e ".[dev]"

# Run linting
black luminoracore/
isort luminoracore/
mypy luminoracore/

# Run tests
pytest
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## API Documentation

- 📚 [API Reference](docs/api_reference.md) - Complete API documentation
- 📖 [Examples](examples/) - Code examples and tutorials

## Support

- 📚 [Documentation](https://docs.luminoracore.com)
- 💬 [Discord Community](https://discord.gg/luminoracore)
- 🐛 [Issue Tracker](https://github.com/luminoracore/sdk-python/issues)
- 📧 [Email Support](mailto:support@luminoracore.com)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.
