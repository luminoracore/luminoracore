# LuminoraCore

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/luminoracore/luminoracore)
[![Tests](https://img.shields.io/badge/tests-90%2F91_passing-brightgreen.svg)](#)
[![Core Status](https://img.shields.io/badge/core-v1.0_ready-brightgreen.svg)](#)
[![CLI Status](https://img.shields.io/badge/cli-v1.0_ready-brightgreen.svg)](#)
[![SDK Status](https://img.shields.io/badge/sdk-v1.0_ready-brightgreen.svg)](#)

**✅ AI PERSONALITY MANAGEMENT PLATFORM - v1.0 PRODUCTION READY**

**LuminoraCore** is a comprehensive AI personality management platform consisting of three powerful components that work together to provide advanced AI personality systems, command-line tools, and Python SDK integration.

---

## 🚀 First Time Here? START HERE

### ⚡ Quick Installation (1 command)

```bash
# Windows
.\instalar_todo.ps1

# Linux/Mac
./instalar_todo.sh
```

### ✅ Verify Installation

```bash
# 1. Download the verification script (if you don't have it)
curl -O https://raw.githubusercontent.com/your-user/luminoracore/main/verify_installation.py

# 2. Run the verification
python verify_installation.py
```

**This script automatically verifies:**
- ✅ All components installed (Core, CLI, SDK)
- ✅ Available providers (7 total)
- ✅ Configured API keys
- ✅ Active virtual environment

**Expected result:** `🎉 INSTALLATION COMPLETE AND CORRECT`

### 📚 Getting Started Guides

| Document | Time | Description |
|----------|------|-------------|
| **[QUICK_START.md](QUICK_START.md)** ⭐⭐⭐ | 5 min | Express installation and first steps |
| **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** ⭐⭐⭐ | 30 min | Complete step-by-step guide with verifications |
| **[CREATING_PERSONALITIES.md](CREATING_PERSONALITIES.md)** ⭐⭐ | 15 min | How to create your own AI personalities |
| **[CHEATSHEET.md](CHEATSHEET.md)** | 2 min | Quick reference cheatsheet |

**Don't know where to start?** → Read [QUICK_START.md](QUICK_START.md) first.

**Want all the details?** → Read [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md).

**Installation problems?** → Run `python verify_installation.py` (see [INSTALLATION_VERIFICATION.md](INSTALLATION_VERIFICATION.md))

**Looking for something specific?** → Check [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md).

---

## 🏗️ Architecture Overview

LuminoraCore is built as a modular platform with three main components:

```
LuminoraCore Platform
├── 🧠 luminoracore/          # Personality Engine (v1.0 ready)
├── 🛠️ luminoracore-cli/      # Command-line Interface (v1.0 ready)
└── 🐍 luminoracore-sdk-python/ # Python SDK (v1.0 ready)
```

---

## 🧠 LuminoraCore (Core Engine) - ✅ v1.0 READY

The fundamental personality engine that powers the entire platform.

### Key Features
- **✅ Advanced Personality Management**: Create, validate, and manage AI personalities
- **✅ JSON Schema Validation**: Robust validation using JSON Schema standards
- **✅ PersonaBlend™ Technology**: Real-time personality blending with custom weights
- **✅ Multi-Provider Integration**: Support for OpenAI, Anthropic, DeepSeek, Google, Cohere, Mistral, Llama
- **✅ Compilation Engine**: Convert personalities to optimized prompts
- **✅ Type Safety**: Comprehensive type definitions and validation
- **✅ Intelligent Cache**: LRU system with performance statistics
- **✅ Performance Validations**: Automatic detection of efficiency issues

### Quick Start
```python
from luminoracore import Personality, PersonalityCompiler, LLMProvider

# Load a personality
personality = Personality("path/to/personality.json")

# Compile to prompt with cache
compiler = PersonalityCompiler(cache_size=128)
result = compiler.compile(personality, LLMProvider.OPENAI)

print(result.prompt)
```

**[📖 Complete Documentation](luminoracore/README.md)** | **[📦 View Code](luminoracore/)**

---

## 🛠️ LuminoraCore CLI - ✅ v1.0 READY

Professional command-line tool for AI personality management.

### Key Features
- **✅ Validate** - Validate personality files against official schema
- **✅ Compile** - Compile personalities to provider-specific prompts
- **✅ Create** - Interactive wizard for creating personalities
- **✅ Test** - Test personalities with real LLM providers
- **✅ Blend** - Blend multiple personalities with custom weights
- **✅ Serve** - Local development server with web interface

### Quick Start
```bash
# Validate a personality
luminoracore validate my_personality.json

# Compile for OpenAI
luminoracore compile my_personality --provider openai

# Create new personality
luminoracore create --interactive

# Start development server
luminoracore serve
```

**[📖 Complete Documentation](luminoracore-cli/README.md)** | **[📦 View Code](luminoracore-cli/)**

---

## 🐍 LuminoraCore SDK Python - ✅ v1.0 READY

Official Python SDK for advanced AI personality management.

### Key Features
- **✅ Session Management**: Stateful conversations with persistent memory
- **✅ Multi-Provider Support**: OpenAI, Anthropic, DeepSeek, Mistral, Cohere, Google, Llama
- **✅ Flexible Storage**: Memory, JSON File, SQLite, Redis, PostgreSQL, MongoDB
- **✅ PersonaBlend™ Technology**: Real-time personality blending
- **✅ Async/Await Support**: Fully asynchronous API
- **✅ Real API Connections**: Real connections to all LLM providers
- **✅ Token Usage Tracking**: Real-time token monitoring and metrics

### Quick Start
```python
import asyncio
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.provider import ProviderConfig

async def main():
    client = LuminoraCoreClient()
    await client.initialize()
    
    provider_config = ProviderConfig(
        name="openai",
        api_key="your-api-key",
        model="gpt-3.5-turbo"
    )
    
    session_id = await client.create_session(
        personality_name="dr_luna",
        provider_config=provider_config
    )
    
    response = await client.send_message(
        session_id=session_id,
        message="Hello! Can you help me with quantum physics?"
    )
    
    print(f"Response: {response.content}")
    await client.cleanup()

asyncio.run(main())
```

**[📖 Complete Documentation](luminoracore-sdk-python/README.md)** | **[📦 View Code](luminoracore-sdk-python/)**

---

## 🔧 Supported LLM Providers (7 Total)

| Provider | Status | Models |
|----------|--------|--------|
| **OpenAI** | ✅ Ready | GPT-3.5, GPT-4, GPT-4 Turbo |
| **Anthropic** | ✅ Ready | Claude 3 Sonnet, Claude 3 Opus |
| **DeepSeek** | ✅ Ready | DeepSeek Chat (Cost-effective) |
| **Mistral** | ✅ Ready | Mistral Large, Mistral Medium |
| **Cohere** | ✅ Ready | Command, Command Light |
| **Google** | ✅ Ready | Gemini Pro, Gemini Ultra |
| **Llama** | ✅ Ready | Llama 2, Llama 3 |

---

## 💾 Storage Backends (6 Options)

| Backend | Best For | Status |
|---------|----------|--------|
| **Memory** | Development, testing | ✅ Ready |
| **JSON File** | Simple apps, portability | ✅ Ready |
| **SQLite** | Mobile apps, single-user | ✅ Ready |
| **Redis** | Production, high-performance | ✅ Ready |
| **PostgreSQL** | Enterprise, complex queries | ✅ Ready |
| **MongoDB** | Document-based, flexibility | ✅ Ready |

---

## 📊 Test Coverage

| Component | Tests | Status |
|-----------|-------|--------|
| **Core Engine** | 28/28 (100%) | ✅ All Passing |
| **CLI** | 25/26 (100%*) | ✅ All Executable Passing |
| **SDK** | 37/37 (100%) | ✅ All Passing |
| **TOTAL** | 90/91 (99%) | ✅ **Production Ready** |

\* *1 skipped test (conditional API key required)*

---

## 🎯 Use Cases

- **Chat Applications** - Add consistent personalities to chatbots
- **Educational Tools** - Create engaging learning experiences
- **Content Generation** - Generate content with specific voice and tone
- **Customer Service** - Deploy AI assistants with appropriate personalities
- **Creative Writing** - Use AI personalities as writing assistants
- **Research & Development** - Experiment with different AI behaviors

---

## 📦 Installation

### Option 1: Automated Installation (Recommended)

```bash
# Windows
.\instalar_todo.ps1

# Linux/Mac
./instalar_todo.sh
```

### Option 2: Manual Installation

```bash
# 1. Install Core Engine
cd luminoracore
pip install -e .

# 2. Install CLI
cd ../luminoracore-cli
pip install -e .

# 3. Install SDK
cd ../luminoracore-sdk-python
pip install -e ".[all]"
```

### Option 3: Individual Components

```bash
# Just the Core Engine
pip install -e luminoracore/

# Just the CLI
pip install luminoracore-cli

# Just the SDK
pip install -e luminoracore-sdk-python/
```

---

## 🧪 Testing

```bash
# Run all tests
python run_tests.py

# Run specific test suite
pytest tests/test_1_motor_base.py -v    # Core Engine (28 tests)
pytest tests/test_2_cli.py -v           # CLI (26 tests)
pytest tests/test_3_sdk.py -v           # SDK (37 tests)

# Expected result:
# 90 passed, 1 skipped in ~12s
```

**[📖 Complete Testing Guide](tests/README.md)**

---

## 📖 Documentation

### 📚 Main Guides
- **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Quick start (5 min)
- **[GUIA_INSTALACION_USO.md](GUIA_INSTALACION_USO.md)** - Complete installation guide (30 min)
- **[GUIA_CREAR_PERSONALIDADES.md](GUIA_CREAR_PERSONALIDADES.md)** - Creating personalities (15 min)
- **[GUIA_VERIFICACION_INSTALACION.md](GUIA_VERIFICACION_INSTALACION.md)** - Installation verification
- **[CHEATSHEET.md](CHEATSHEET.md)** - Quick reference (2 min)

### 📋 Technical Documentation
- **[MASTER_TEST_SUITE.md](MASTER_TEST_SUITE.md)** - Complete testing documentation
- **[tests/ESTRATEGIA_TESTS.md](tests/ESTRATEGIA_TESTS.md)** - Testing strategy
- **[INDICE_DOCUMENTACION.md](INDICE_DOCUMENTACION.md)** - Complete documentation index

### 🔧 Component Documentation
- **[luminoracore/README.md](luminoracore/README.md)** - Core Engine
- **[luminoracore-cli/README.md](luminoracore-cli/README.md)** - CLI Tool
- **[luminoracore-sdk-python/README.md](luminoracore-sdk-python/README.md)** - Python SDK

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](luminoracore/CONTRIBUTING.md) for details.

### Ways to Contribute
- 🐛 Report bugs
- 💡 Suggest new features
- 🎭 Submit new personalities
- 📚 Improve documentation
- 🧪 Add tests
- 🔧 Fix issues

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](luminoracore/LICENSE) file for details.

---

## 🌟 Project Status

### ✅ v1.0.0 - Production Ready (CURRENT)
- [x] 7 LLM providers (OpenAI, Anthropic, DeepSeek, Mistral, Llama, Cohere, Google)
- [x] 6 storage backends (Memory, JSON, SQLite, Redis, PostgreSQL, MongoDB)
- [x] PersonaBlend™ technology
- [x] 90/91 tests passing (100% executable)
- [x] Comprehensive documentation
- [x] Production-ready stable release

### 🔮 Future Releases
- [ ] **v1.1.0** - Additional LLM providers
- [ ] **v1.2.0** - Personality marketplace
- [ ] **v1.3.0** - Advanced blending algorithms
- [ ] **v2.0.0** - Real-time personality adaptation

---

## 📞 Support

- 📧 **Email**: team@luminoracore.dev
- 💬 **Discord**: [Join our community](https://discord.gg/luminoracore)
- 🐛 **Issues**: [GitHub Issues](https://github.com/luminoracore/luminoracore/issues)
- 📖 **Wiki**: [GitHub Wiki](https://github.com/luminoracore/luminoracore/wiki)

---

## 🙏 Acknowledgments

- Inspired by the need for standardized AI personality management
- Built with the Python community in mind
- Thanks to all contributors and the open-source ecosystem

---

<div align="center">

**Made with ❤️ by the LuminoraCore Team**

[⭐ Star us on GitHub](https://github.com/luminoracore/luminoracore) • [🐛 Report Issues](https://github.com/luminoracore/luminoracore/issues) • [💬 Join Discord](https://discord.gg/luminoracore)

**✅ v1.0 PRODUCTION READY - 90/91 Tests Passing (100% Executable)**

</div>
