# Welcome to LuminoraCore Wiki

![LuminoraCore Banner](https://img.shields.io/badge/LuminoraCore-v1.0-blue?style=for-the-badge)
![Production Ready](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-179%2F179%20Passing-brightgreen?style=for-the-badge)

---

## 🎯 What is LuminoraCore?

**LuminoraCore** is a comprehensive AI personality management platform that allows you to create, validate, blend, and deploy AI personalities across multiple LLM providers.

### Why LuminoraCore?

- 🎭 **Standardized Personalities**: JSON-based personality definitions with schema validation
- 🔄 **PersonaBlend™ Technology**: Blend multiple personalities with custom weights
- 🚀 **Multi-Provider Support**: Works with 7 major LLM providers
- 💾 **Flexible Storage**: From in-memory to enterprise databases
- ⚡ **Production Ready**: 179/179 tests passing (v1.1), battle-tested

---

## 🚀 Quick Start

### 1️⃣ Install Everything (1 command)

```bash
# Windows
.\install_all.ps1

# Linux/Mac
./install_all.sh
```

### 2️⃣ Verify Installation

```bash
python verify_installation.py
```

Expected output: **🎉 INSTALLATION COMPLETE AND CORRECT**

### 3️⃣ Try Your First Command

```bash
# List available personalities
luminoracore list

# Validate a personality
luminoracore validate luminoracore/luminoracore/personalities/dr_luna.json

# Compile for OpenAI
luminoracore compile luminoracore/luminoracore/personalities/dr_luna.json --provider openai
```

### 4️⃣ Use in Python

```python
from luminoracore import Personality, PersonalityCompiler, LLMProvider

personality = Personality("path/to/personality.json")
compiler = PersonalityCompiler()
result = compiler.compile(personality, LLMProvider.OPENAI)
print(result.prompt)
```

---

## 📚 Documentation Structure

### 🌟 Essential Guides (START HERE)

| Guide | Time | What You'll Learn |
|-------|------|-------------------|
| **[QUICK_START.md](https://github.com/luminoracore/luminoracore/blob/main/QUICK_START.md)** ⭐⭐⭐ | 5 min | Installation and first steps |
| **[INSTALLATION_GUIDE.md](https://github.com/luminoracore/luminoracore/blob/main/INSTALLATION_GUIDE.md)** ⭐⭐⭐ | 30 min | Complete step-by-step guide |
| **[CREATING_PERSONALITIES.md](https://github.com/luminoracore/luminoracore/blob/main/CREATING_PERSONALITIES.md)** ⭐⭐ | 15 min | How to create AI personalities |

### 📖 Wiki Pages

- **[Getting Started](Getting-Started)** - Installation and setup
- **[Core Concepts](Core-Concepts)** - Personalities, blending, compilation
- **[FAQ](FAQ)** - Frequently asked questions
- **[Troubleshooting](Troubleshooting)** - Common problems and solutions
- **[Tutorials](Tutorials)** - Step-by-step guides (coming soon)
- **[API Reference](API-Reference)** - Complete API documentation (coming soon)

### 🔧 Component Documentation

- **[luminoracore/README.md](https://github.com/luminoracore/luminoracore/blob/main/luminoracore/README.md)** - Core Engine
- **[luminoracore-cli/README.md](https://github.com/luminoracore/luminoracore/blob/main/luminoracore-cli/README.md)** - CLI Tool
- **[luminoracore-sdk-python/README.md](https://github.com/luminoracore/luminoracore/blob/main/luminoracore-sdk-python/README.md)** - Python SDK

---

## 🏗️ Platform Architecture

```
┌──────────────────────────────────────────────────┐
│  🧠 luminoracore (Base Engine)                   │
│     • Personality management                     │
│     • Validation & compilation                   │
│     • PersonaBlend™ Technology                   │
└──────────────┬───────────────────────────────────┘
               │
               │ BOTH USE THE BASE ENGINE
               │
        ┌──────┴──────┐
        ▼             ▼
┌───────────┐  ┌─────────────────┐
│ 🛠️ CLI    │  │ 🐍 SDK          │
│ Terminal  │  │ Python Apps     │
│ Commands  │  │ Sessions        │
│ Wizard    │  │ Real LLM calls  │
└───────────┘  └─────────────────┘
```

---

## 🎯 Use Cases

- 🤖 **Chat Applications** - Add consistent personalities to chatbots
- 📚 **Educational Tools** - Create engaging learning experiences
- ✍️ **Content Generation** - Generate content with specific voice and tone
- 💼 **Customer Service** - Deploy AI assistants with appropriate personalities
- 🎨 **Creative Writing** - Use AI personalities as writing assistants
- 🔬 **Research & Development** - Experiment with different AI behaviors

---

## 🔧 Supported Technologies

### LLM Providers (7)
- ✅ OpenAI (GPT-3.5, GPT-4)
- ✅ Anthropic (Claude 3)
- ✅ DeepSeek (Cost-effective)
- ✅ Mistral AI
- ✅ Cohere
- ✅ Google Gemini
- ✅ Llama (via Replicate)

### Storage Backends (6)
- ✅ Memory (RAM)
- ✅ JSON File (Simple persistence)
- ✅ SQLite (Mobile apps)
- ✅ Redis (Production)
- ✅ PostgreSQL (Enterprise)
- ✅ MongoDB (Flexible)

---

## 📊 Project Status

| Component | Version | Tests | Status |
|-----------|---------|-------|--------|
| **Core Engine** | v1.0.0 | 28/28 (100%) | ✅ Production Ready |
| **CLI** | v1.0.0 | 25/26 (100%*) | ✅ Production Ready |
| **SDK** | v1.0.0 | 37/37 (100%) | ✅ Production Ready |
| **TOTAL** | v1.0.0 | 90/91 (99%) | ✅ **Production Ready** |

_* 1 skipped test (conditional API key required)_

---

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](https://github.com/luminoracore/luminoracore/blob/main/CONTRIBUTING.md).

### Ways to Contribute
- 🐛 Report bugs
- 💡 Suggest features
- 🎭 Submit personalities
- 📚 Improve docs
- 🧪 Add tests
- 🔧 Fix issues

---

## 📞 Support & Community

- 📧 **Email**: team@luminoracore.dev
- 🐛 **Issues**: [GitHub Issues](https://github.com/luminoracore/luminoracore/issues)
- 📖 **Documentation**: [Complete Index](DOCUMENTATION_INDEX.md)

---

## 🔗 Quick Links

### For Users
- [Quick Start Guide](https://github.com/luminoracore/luminoracore/blob/main/QUICK_START.md)
- [Installation Guide](https://github.com/luminoracore/luminoracore/blob/main/INSTALLATION_GUIDE.md)
- [Creating Personalities](https://github.com/luminoracore/luminoracore/blob/main/CREATING_PERSONALITIES.md)
- [Cheatsheet](https://github.com/luminoracore/luminoracore/blob/main/CHEATSHEET.md)

### For Developers
- [Core Engine Docs](https://github.com/luminoracore/luminoracore/tree/main/luminoracore/docs)
- [CLI Source Code](https://github.com/luminoracore/luminoracore/tree/main/luminoracore-cli)
- [SDK Source Code](https://github.com/luminoracore/luminoracore/tree/main/luminoracore-sdk-python)
- [Test Suite](https://github.com/luminoracore/luminoracore/tree/main/tests)

### For Contributors
- [Contributing Guide](https://github.com/luminoracore/luminoracore/blob/main/CONTRIBUTING.md)
- [Code of Conduct](https://github.com/luminoracore/luminoracore/blob/main/CODE_OF_CONDUCT.md)
- [Testing Strategy](https://github.com/luminoracore/luminoracore/blob/main/tests/ESTRATEGIA_TESTS.md)

---

## 🌟 Featured

### Included Personalities (11)
- 🧪 **Dr. Luna** - Scientific Enthusiast
- ⚓ **Captain Hook Digital** - Adventurous Leader
- 😏 **Marcus Sarcasmus** - Sarcastic Wit
- 💪 **Rocky Inspiration** - Motivational Coach
- 💼 **Victoria Sterling** - Professional Executive
- 👵 **Grandma Hope** - Caring Mentor
- 🎨 **Lila Charm** - Creative Artist
- 📚 **Prof. Rigoberto** - Academic Expert
- 💻 **Zero Cool** - Tech Hacker
- 🤖 **Alex Digital** - AI Assistant
- 🎯 **AI Assistant** - General Purpose

### PersonaBlend™ Examples
- 70% Dr. Luna + 30% Rocky = Enthusiastic Scientist Coach
- 50% Victoria + 50% Grandma Hope = Wise Professional Mentor
- 60% Zero Cool + 40% Prof. Rigoberto = Academic Hacker

---

## 📈 Roadmap

### ✅ v1.0.0 (Current)
- 7 LLM providers
- 6 storage backends
- PersonaBlend™ technology
- 179/179 tests passing (v1.1)
- Complete documentation

### 🔮 Coming Soon
- **v1.1.0** - Additional LLM providers (Gemini 1.5, Claude 3.5)
- **v1.2.0** - Personality marketplace
- **v1.3.0** - Advanced blending algorithms
- **v2.0.0** - Real-time personality adaptation

---

**Made with ❤️ by the LuminoraCore Team**

**⭐ Star us on GitHub • 🐛 Report Issues**

**✅ v1.1 PRODUCTION READY - 179/179 Tests Passing (100%)**

