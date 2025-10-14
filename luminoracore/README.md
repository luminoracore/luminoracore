# 🧠 LuminoraCore - Motor Principal

[![Build Status](https://github.com/luminoracore/luminoracore/workflows/Tests/badge.svg)](https://github.com/luminoracore/luminoracore/actions)
[![Coverage](https://codecov.io/gh/luminoracore/luminoracore/branch/main/graph/badge.svg)](https://codecov.io/gh/luminoracore/luminoracore)
[![Version](https://img.shields.io/pypi/v/luminoracore.svg)](https://pypi.org/project/luminoracore/)
[![License](https://img.shields.io/pypi/l/luminoracore.svg)](https://github.com/luminoracore/luminoracore/blob/main/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/luminoracore.svg)](https://pypi.org/project/luminoracore/)
[![Status](https://img.shields.io/badge/status-v1.1_ready-brightgreen.svg)](#)
[![Tests](https://img.shields.io/badge/tests-99%2F99_passing-brightgreen.svg)](#)

**✅ AI PERSONALITY MANAGEMENT ENGINE - v1.1 PRODUCTION READY**

LuminoraCore is the core AI personality management engine that powers the entire platform. Provides a complete system for creating, validating, compiling, and blending AI personalities with advanced memory, affinity tracking, and relationship management for use with OpenAI, Anthropic, DeepSeek, Llama, Mistral, Cohere, Google, and other LLM providers.

## ✨ Key Features

### Core Features (v1.0)
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

### New in v1.1 - Memory & Relationships
- **✅ Hierarchical Personality System** - Relationship levels that evolve (stranger → friend → soulmate)
- **✅ Affinity Management** - Track relationship points (0-100) with automatic progression
- **✅ Fact Extraction** - Automatically learn from conversations with 9 fact categories
- **✅ Episodic Memory** - Remember memorable moments with 7 episode types
- **✅ Memory Classification** - Smart organization by importance and category
- **✅ Feature Flags** - Safe, gradual feature rollout with JSON configuration
- **✅ Database Migrations** - Structured schema management with 5 new tables
- **✅ Dynamic Compilation** - Runtime personality adjustment based on affinity

## 🚀 Quick Start

### Installation

```bash
pip install -e luminoracore/
```

### Basic Usage (v1.0)

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

### v1.1 Quick Example

```python
from luminoracore.core.affinity_manager import AffinityManager
from luminoracore.core.fact_extractor import FactExtractor
from luminoracore.core.episodic_memory import EpisodicMemoryManager

# Initialize v1.1 components
affinity_mgr = AffinityManager(storage)
fact_extractor = FactExtractor()
memory_mgr = EpisodicMemoryManager(storage)

# Track affinity
affinity_mgr.update_affinity(
    session_id="user_123",
    interaction_type="positive",
    points=5
)

# Extract facts from conversation
facts = fact_extractor.extract_facts(
    message="I love playing guitar on weekends",
    session_id="user_123"
)

# Store memorable moments
memory_mgr.create_episode(
    session_id="user_123",
    episode_type="achievement",
    content="User completed first coding project",
    importance=0.9
)
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

### Core Documentation
- [Getting Started](docs/getting_started.md) - Complete setup guide
- [Personality Format](docs/personality_format.md) - JSON schema documentation
- [API Reference](docs/api_reference.md) - Complete API documentation
- [Best Practices](docs/best_practices.md) - Guidelines for creating personalities

### v1.1 Documentation
- [v1.1 Features Guide](docs/v1_1_features.md) - Complete v1.1 API guide
- [Quick Start v1.1](../mejoras_v1.1/QUICK_START_V1_1.md) - 5-minute tutorial
- [v1.1 Features Summary](../mejoras_v1.1/V1_1_FEATURES_SUMMARY.md) - Complete feature list
- [Technical Architecture](../mejoras_v1.1/TECHNICAL_ARCHITECTURE.md) - Database schema and design

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
# v1.0 Examples
python examples/basic_usage.py
python examples/personality_switching.py
python examples/blending_demo.py
python examples/multi_llm_demo.py

# v1.1 Examples
python examples/v1_1_quick_example.py
python ../examples/v1_1_affinity_demo.py
python ../examples/v1_1_memory_demo.py
python ../examples/v1_1_dynamic_personality_demo.py
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

### ✅ v1.1.0 - Memory & Relationships (CURRENT - October 2025)
- [x] 7 LLM providers (OpenAI, Anthropic, DeepSeek, Mistral, Llama, Cohere, Google)
- [x] PersonaBlend™ technology
- [x] JSON Schema validation
- [x] **NEW:** Hierarchical personality system with relationship levels
- [x] **NEW:** Affinity management (0-100 points)
- [x] **NEW:** Fact extraction from conversations (9 categories)
- [x] **NEW:** Episodic memory for memorable moments (7 types)
- [x] **NEW:** Memory classification by importance
- [x] **NEW:** Feature flags for safe rollout
- [x] **NEW:** Database migrations system (5 new tables)
- [x] **NEW:** Dynamic compilation based on affinity
- [x] 99/99 tests passing (100%)
- [x] Comprehensive documentation
- [x] 100% backward compatible
- [x] Production-ready stable release

### 🔮 Future Releases
- [ ] **v1.2.0** (Q1 2026) - Mood System & Vector Search
- [ ] **v1.3.0** (Q2 2026) - Enterprise Features: Analytics dashboard, A/B testing
- [ ] **v2.0.0** (Q3 2026) - AI-Native: Self-learning personalities, multi-modal support

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
