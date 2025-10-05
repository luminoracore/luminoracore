# 🧠 LuminoraCore - Motor Principal

[![Build Status](https://github.com/luminoracore/luminoracore/workflows/Tests/badge.svg)](https://github.com/luminoracore/luminoracore/actions)
[![Coverage](https://codecov.io/gh/luminoracore/luminoracore/branch/main/graph/badge.svg)](https://codecov.io/gh/luminoracore/luminoracore)
[![Version](https://img.shields.io/pypi/v/luminoracore.svg)](https://pypi.org/project/luminoracore/)
[![License](https://img.shields.io/pypi/l/luminoracore.svg)](https://github.com/luminoracore/luminoracore/blob/main/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/luminoracore.svg)](https://pypi.org/project/luminoracore/)
[![Status](https://img.shields.io/badge/status-v1.0_ready-brightgreen.svg)](#)
[![Tests](https://img.shields.io/badge/tests-28%2F28_passing-brightgreen.svg)](#)

**✅ AI PERSONALITY MANAGEMENT ENGINE - v1.0 PRODUCTION READY**

LuminoraCore is the core AI personality management engine that powers the entire platform. Provides a complete system for creating, validating, compiling, and blending AI personalities for use with OpenAI, Anthropic, DeepSeek, Llama, Mistral, Cohere, Google, and other LLM providers.

## ✨ Key Features

- **✅ 10 Pre-built Personalities** - Ready-to-use personality archetypes
- **✅ Multi-LLM Support** - Compile personalities for OpenAI, Anthropic, Llama, Mistral, Cohere, Google
- **✅ PersonaBlend™ Technology** - Mix multiple personalities with advanced strategies
- **✅ Robust Validation** - JSON Schema validation with quality checks
- **✅ Compilation Engine** - Convert personalities to optimized prompts
- **✅ Intelligent Cache** - LRU system with performance statistics
- **✅ Performance Validations** - Automatic detection of efficiency issues
- **✅ Type Safety** - Comprehensive type definitions
- **✅ Complete Examples** - Learn with practical examples
- **✅ Full Test Coverage** - Extensive unit tests and CI/CD

## 🚀 Quick Start

### Installation

```bash
pip install -e luminoracore/
```

### Basic Usage

```python
from luminoracore import Personality, PersonalityCompiler, LLMProvider

# Load a personality
personality = Personality("personalities/dr_luna.json")

# Compile with intelligent cache
compiler = PersonalityCompiler(cache_size=128)
result = compiler.compile(personality, LLMProvider.OPENAI)

# Use the compiled prompt
print(result.prompt)
print(f"Estimated tokens: {result.token_estimate}")
print(f"Metadata: {result.metadata}")

# Cache statistics
stats = compiler.get_cache_stats()
print(f"Hit rate: {stats['hit_rate']}%")
```

### Advanced Usage

```python
from luminoracore import PersonalityBlender

# Blend personalities
blender = PersonalityBlender()
blended = blender.blend(
    personalities=[personality1, personality2],
    weights=[0.7, 0.3],
    strategy="weighted_average"
)

# Validate with performance checks
from luminoracore import PersonalityValidator
validator = PersonalityValidator(enable_performance_checks=True)
result = validator.validate(personality)
```

## 🎭 Built-in Personalities

LuminoraCore comes with 10 carefully crafted personalities:

1. **Dr. Luna** - Enthusiastic Scientist 🔬
2. **Captain Hook Digital** - Adventurous Pirate 🏴‍☠️
3. **Grandma Hope** - Caring Grandmother 👵
4. **Marcus Sarcasmus** - Cynical Observer 😏
5. **Alex Digital** - Gen Z Trendy 📱
6. **Victoria Sterling** - Business Leader 💼
7. **Rocky Inspiration** - Motivational Coach 💪
8. **Zero Cool** - Ethical Hacker 💻
9. **Professor Stern** - Rigorous Academic 🎓
10. **Lila Charm** - Playful Flirt 💕

## 📖 Documentation

- [Getting Started](docs/getting_started.md) - Complete setup guide
- [Personality Format](docs/personality_format.md) - JSON schema documentation
- [API Reference](docs/api_reference.md) - Complete API documentation
- [Best Practices](docs/best_practices.md) - Guidelines for creating personalities

## 🛠️ Development

### Setup Development Environment

```bash
git clone https://github.com/luminoracore/luminoracore.git
cd luminoracore
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/ -v --cov=luminoracore
```

### Run Examples

```bash
python examples/basic_usage.py
python examples/personality_switching.py
python examples/blending_demo.py
python examples/multi_llm_demo.py
```

## 🎯 Use Cases

- **Chat Applications** - Add consistent personality to your chatbots
- **Educational Tools** - Create engaging learning experiences
- **Content Generation** - Generate content with specific voice and tone
- **Customer Service** - Deploy AI assistants with appropriate personalities
- **Creative Writing** - Use AI personalities as writing assistants
- **Research & Development** - Experiment with different AI behaviors

## 🔧 Supported LLM Providers (7 Total)

- **OpenAI** - GPT-3.5, GPT-4, GPT-4 Turbo
- **Anthropic** - Claude 3 Sonnet, Claude 3 Opus
- **DeepSeek** - DeepSeek Chat (Cost-effective option)
- **Meta** - Llama 2, Llama 3
- **Mistral** - Mistral Large, Mistral Medium
- **Cohere** - Command, Command Light
- **Google** - Gemini Pro, Gemini Ultra

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 🎭 Submit new personalities
- 📚 Improve documentation
- 🧪 Add tests
- 🔧 Fix issues

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Inspired by the need for standardized AI personality management
- Built with the Python community in mind
- Thanks to all contributors and the open-source ecosystem

## 📊 Status & Roadmap

### ✅ v1.0.0 - Production Ready (CURRENT)
- [x] 7 LLM providers (OpenAI, Anthropic, DeepSeek, Mistral, Llama, Cohere, Google)
- [x] PersonaBlend™ technology
- [x] JSON Schema validation
- [x] 28/28 tests passing (100%)
- [x] Comprehensive documentation
- [x] Production-ready stable release

### 🔮 Future Releases
- [ ] **v1.1.0** - Additional LLM provider support
- [ ] **v1.2.0** - Personality marketplace
- [ ] **v1.3.0** - Advanced blending algorithms
- [ ] **v2.0.0** - Real-time personality adaptation

## 📞 Support

- 📧 Email: team@luminoracore.dev
- 💬 Discord: [Join our community](https://discord.gg/luminoracore)
- 🐛 Issues: [GitHub Issues](https://github.com/luminoracore/luminoracore/issues)
- 📖 Wiki: [GitHub Wiki](https://github.com/luminoracore/luminoracore/wiki)

---

<div align="center">

**Made with ❤️ by the LuminoraCore Team**

[⭐ Star us on GitHub](https://github.com/luminoracore/luminoracore) • [🐛 Report Issues](https://github.com/luminoracore/luminoracore/issues) • [💬 Join Discord](https://discord.gg/luminoracore)

</div>
