# LuminoraCore SDK Python

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/luminoracore/sdk-python)

**LuminoraCore SDK Python** is the official Python client for advanced AI personality management. It provides a comprehensive toolkit for building AI applications with sophisticated personality systems, session management, and multi-LLM provider support.

## Features

- 🧠 **Advanced Personality Management**: Create, blend, and manage AI personalities with ease
- 🔄 **Session Management**: Stateful conversations with persistent memory and context
- 🌐 **Multi-Provider Support**: Integrate with OpenAI, Anthropic, Mistral, Cohere, Google, and more
- 🎭 **PersonaBlend™ Technology**: Real-time personality blending with custom weights
- 💾 **Flexible Storage**: Support for Redis, PostgreSQL, MongoDB, and in-memory storage
- 📊 **Monitoring & Metrics**: Built-in observability with distributed tracing
- 🚀 **Async/Await Support**: Full asynchronous API for high-performance applications
- 🔒 **Type Safety**: Comprehensive type definitions and validation

## Installation

```bash
pip install luminoracore-sdk
```

## Quick Start

```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig

async def main():
    # Initialize the client
    client = LuminoraCoreClient()
    await client.initialize()
    
    # Create a provider configuration
    provider_config = ProviderConfig(
        name="openai",
        api_key="your-api-key",
        model="gpt-3.5-turbo"
    )
    
    # Create a session
    session_id = await client.create_session(
        personality_name="helpful_assistant",
        provider_config=provider_config
    )
    
    # Send a message
    response = await client.send_message(
        session_id=session_id,
        message="Hello! Can you help me?"
    )
    
    print(response.content)
    
    # Clean up
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
from luminoracore.types.session import StorageConfig

# Redis storage
storage_config = StorageConfig(
    storage_type="redis",
    redis_url="redis://localhost:6379",
    ttl=3600
)

# PostgreSQL storage
storage_config = StorageConfig(
    storage_type="postgresql",
    postgres_url="postgresql://user:password@localhost/db",
    ttl=3600
)

# MongoDB storage
storage_config = StorageConfig(
    storage_type="mongodb",
    mongodb_url="mongodb://localhost:27017/db",
    ttl=3600
)
```

### Memory Configuration

```python
from luminoracore.types.session import MemoryConfig

memory_config = MemoryConfig(
    max_tokens=10000,
    max_messages=100,
    ttl=1800
)
```

## Supported Providers

- **OpenAI**: GPT-3.5, GPT-4, and other OpenAI models
- **Anthropic**: Claude-3 Sonnet, Claude-3 Haiku, and other Claude models
- **Mistral**: Mistral Tiny, Mistral Small, and other Mistral models
- **Cohere**: Command, Command Light, and other Cohere models
- **Google**: Gemini Pro, Gemini Ultra, and other Google models
- **Llama**: Llama-2, Llama-3, and other Llama models

## Examples

Check out the `examples/` directory for comprehensive examples:

- `basic_usage.py` - Basic usage examples
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

## Support

- 📚 [Documentation](https://docs.luminoracore.com)
- 💬 [Discord Community](https://discord.gg/luminoracore)
- 🐛 [Issue Tracker](https://github.com/luminoracore/sdk-python/issues)
- 📧 [Email Support](mailto:support@luminoracore.com)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.
