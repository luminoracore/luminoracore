# LuminoraCore

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/luminoracore/luminoracore)

**LuminoraCore** is a comprehensive AI personality management platform consisting of three powerful components that work together to provide advanced AI personality systems, command-line tools, and Python SDK integration.

## 🏗️ Architecture Overview

LuminoraCore is built as a modular platform with three core components:

```
LuminoraCore Platform
├── 🧠 luminoracore/          # Core personality engine
├── 🛠️ luminoracore-cli/      # Command-line interface
└── 🐍 luminoracore-sdk-python/ # Python SDK
```

## 🧠 LuminoraCore (Core Engine)

The foundational personality engine that powers the entire platform.

### Key Features
- **Advanced Personality Management**: Create, validate, and manage AI personalities
- **JSON Schema Validation**: Robust validation using JSON Schema standards
- **Personality Blending**: Real-time personality blending with custom weights
- **LLM Provider Integration**: Support for multiple LLM providers
- **Compilation Engine**: Convert personalities to optimized prompts
- **Type Safety**: Comprehensive type definitions and validation

### Quick Start
```python
from luminoracore import Personality, PersonalityCompiler

# Load a personality
personality = Personality("path/to/personality.json")

# Compile to prompt
compiler = PersonalityCompiler()
prompt = compiler.compile(personality)
```

### Documentation
- 📚 [API Reference](luminoracore/docs/api_reference.md)
- 📖 [Best Practices](luminoracore/docs/best_practices.md)
- 🎯 [Examples](luminoracore/examples/)

---

## 🛠️ LuminoraCore CLI

Professional command-line interface for personality management and validation.

### Key Features
- **Personality Validation**: Validate personality files against schemas
- **Batch Processing**: Process multiple personalities at once
- **Interactive Testing**: Test personalities in real-time
- **Development Server**: Local development server with hot reload
- **Personality Creation**: Guided personality creation wizard
- **Blending Tools**: Command-line personality blending

### Quick Start
```bash
# Install CLI
pip install luminoracore-cli

# Validate personalities
luminoracore validate personalities/*.json

# Start development server
luminoracore serve --port 8000

# Create new personality
luminoracore create --name "my_personality"

# Test personality interactively
luminoracore test --personality "my_personality"
```

### Available Commands
- `validate` - Validate personality files
- `compile` - Compile personalities to prompts
- `create` - Create new personalities
- `list` - List available personalities
- `test` - Test personalities interactively
- `serve` - Start development server
- `blend` - Blend multiple personalities
- `update` - Update personality cache
- `init` - Initialize new project
- `info` - Show personality information

### Documentation
- 📚 [CLI Documentation](luminoracore-cli/README.md)
- 🎯 [Examples](luminoracore-cli/examples/)

---

## 🐍 LuminoraCore SDK Python

Official Python SDK for building AI applications with personality systems.

### Key Features
- **Session Management**: Stateful conversations with persistent memory
- **Multi-Provider Support**: OpenAI, Anthropic, Mistral, Cohere, Google, Llama
- **PersonaBlend™ Technology**: Real-time personality blending
- **Flexible Storage**: Redis, PostgreSQL, MongoDB, in-memory
- **Async/Await Support**: Full asynchronous API
- **Monitoring & Metrics**: Built-in observability
- **Type Safety**: Comprehensive type definitions

### Quick Start
```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig

async def main():
    # Initialize client
    client = LuminoraCoreClient()
    await client.initialize()
    
    # Create provider
    provider_config = ProviderConfig(
        name="openai",
        api_key="your-api-key",
        model="gpt-3.5-turbo"
    )
    
    # Create session
    session_id = await client.create_session(
        personality_name="helpful_assistant",
        provider_config=provider_config
    )
    
    # Send message
    response = await client.send_message(
        session_id=session_id,
        message="Hello! Can you help me?"
    )
    
    print(response.content)
    await client.cleanup()

asyncio.run(main())
```

### Documentation
- 📚 [API Reference](luminoracore-sdk-python/docs/api_reference.md)
- 🎯 [Examples](luminoracore-sdk-python/examples/)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

#### Install All Components
```bash
# Clone the repository
git clone https://github.com/luminoracore/luminoracore.git
cd luminoracore

# Install core engine
pip install -e luminoracore/

# Install CLI
pip install -e luminoracore-cli/

# Install SDK
pip install -e luminoracore-sdk-python/
```

#### Install Individual Components
```bash
# Core engine only
pip install -e luminoracore/

# CLI only
pip install -e luminoracore-cli/

# SDK only
pip install -e luminoracore-sdk-python/
```

### Quick Example

1. **Create a personality** using the CLI:
```bash
luminoracore create --name "creative_writer"
```

2. **Validate the personality**:
```bash
luminoracore validate personalities/creative_writer.json
```

3. **Use in your Python application**:
```python
from luminoracore import LuminoraCoreClient

client = LuminoraCoreClient()
await client.initialize()
# ... use the personality in your app
```

## 🏢 Use Cases

### For Developers
- **AI Application Development**: Build apps with sophisticated personality systems
- **Personality Research**: Experiment with different personality configurations
- **Multi-Model Applications**: Use different LLMs with consistent personality interfaces

### For Researchers
- **Personality Studies**: Research AI personality behavior and blending
- **Prompt Engineering**: Advanced prompt compilation and optimization
- **Model Comparison**: Test different LLMs with the same personality

### For Enterprises
- **Customer Service**: Deploy consistent AI personalities across channels
- **Content Generation**: Create branded content with specific personality traits
- **Training Data**: Generate training data with controlled personality characteristics

## 🔧 Development

### Project Structure
```
LuminoraCore/
├── luminoracore/              # Core personality engine
│   ├── luminoracore/          # Main package
│   ├── examples/              # Usage examples
│   ├── docs/                  # Documentation
│   └── tests/                 # Unit tests
├── luminoracore-cli/          # Command-line interface
│   ├── luminoracore_cli/      # CLI package
│   ├── examples/              # CLI examples
│   └── tests/                 # CLI tests
├── luminoracore-sdk-python/   # Python SDK
│   ├── luminoracore/          # SDK package
│   ├── examples/              # SDK examples
│   ├── docs/                  # SDK documentation
│   └── tests/                 # SDK tests
└── README.md                  # This file
```

### Running Tests
```bash
# Test all components
pytest luminoracore/tests/
pytest luminoracore-cli/tests/
pytest luminoracore-sdk-python/tests/

# Test specific component
pytest luminoracore/tests/ -v
```

### Contributing
We welcome contributions! Please see our [Contributing Guide](luminoracore/CONTRIBUTING.md) for details.

## 📊 Component Comparison

| Feature | Core Engine | CLI | SDK |
|---------|-------------|-----|-----|
| Personality Management | ✅ | ✅ | ✅ |
| Validation | ✅ | ✅ | ✅ |
| Blending | ✅ | ✅ | ✅ |
| Session Management | ❌ | ❌ | ✅ |
| Multi-Provider | ✅ | ❌ | ✅ |
| Interactive Testing | ❌ | ✅ | ❌ |
| Batch Processing | ❌ | ✅ | ❌ |
| Development Server | ❌ | ✅ | ❌ |
| Python Integration | ✅ | ❌ | ✅ |

## 🤝 Integration Examples

### CLI + Core Engine
```bash
# Create personality with CLI
luminoracore create --name "assistant"

# Validate with CLI
luminoracore validate personalities/assistant.json

# Use in Python with Core Engine
from luminoracore import Personality
personality = Personality("personalities/assistant.json")
```

### SDK + Core Engine
```python
# Use Core Engine for personality management
from luminoracore import PersonalityCompiler
from luminoracore import LuminoraCoreClient

# Use SDK for session management
client = LuminoraCoreClient()
# ... session management
```

### Full Stack
```bash
# 1. Create personality with CLI
luminoracore create --name "customer_service"

# 2. Validate with CLI
luminoracore validate personalities/customer_service.json

# 3. Use in application with SDK
from luminoracore import LuminoraCoreClient
# ... full application
```

## 📈 Roadmap

- [ ] **Web Dashboard**: Web interface for personality management
- [ ] **REST API**: HTTP API for remote personality management
- [ ] **Docker Support**: Containerized deployment options
- [ ] **Kubernetes**: Cloud-native deployment
- [ ] **Monitoring**: Advanced observability and metrics
- [ ] **Personality Marketplace**: Share and discover personalities

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](luminoracore/LICENSE) file for details.

## 🆘 Support

- 📚 [Documentation](https://docs.luminoracore.com)
- 💬 [Discord Community](https://discord.gg/luminoracore)
- 🐛 [Issue Tracker](https://github.com/luminoracore/luminoracore/issues)
- 📧 [Email Support](mailto:support@luminoracore.com)

## 🙏 Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude models
- The open-source community for inspiration and contributions

---

**LuminoraCore** - Empowering AI with Personality 🚀
