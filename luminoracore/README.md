# 🧠 LuminoraCore - Motor Principal

[![Build Status](https://github.com/luminoracore/luminoracore/workflows/Tests/badge.svg)](https://github.com/luminoracore/luminoracore/actions)
[![Coverage](https://codecov.io/gh/luminoracore/luminoracore/branch/main/graph/badge.svg)](https://codecov.io/gh/luminoracore/luminoracore)
[![Version](https://img.shields.io/pypi/v/luminoracore.svg)](https://pypi.org/project/luminoracore/)
[![License](https://img.shields.io/pypi/l/luminoracore.svg)](https://github.com/luminoracore/luminoracore/blob/main/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/luminoracore.svg)](https://pypi.org/project/luminoracore/)
[![Status](https://img.shields.io/badge/status-100%25_complete-brightgreen.svg)](#)

**✅ ESTÁNDAR UNIVERSAL DE GESTIÓN DE PERSONALIDADES DE IA - 100% COMPLETO**

LuminoraCore es el motor principal de personalidades de IA que impulsa toda la plataforma. Proporciona un sistema completo para crear, validar, compilar y mezclar personalidades de IA para uso con OpenAI, Anthropic, Llama, Mistral, Cohere, Google y otros proveedores de LLM.

## ✨ Características Principales

- **✅ 10 Personalidades Pre-construidas** - Arquetipos de personalidad listos para usar
- **✅ Soporte Multi-LLM** - Compilar personalidades para OpenAI, Anthropic, Llama, Mistral, Cohere, Google
- **✅ PersonaBlend™ Technology** - Mezclar múltiples personalidades con estrategias avanzadas
- **✅ Validación Robusta** - Validación JSON Schema con verificaciones de calidad
- **✅ Motor de Compilación** - Convertir personalidades a prompts optimizados
- **✅ Caché Inteligente** - Sistema LRU con estadísticas de rendimiento
- **✅ Validaciones de Rendimiento** - Detección automática de problemas de eficiencia
- **✅ Seguridad de Tipos** - Definiciones de tipos comprehensivas
- **✅ Ejemplos Completos** - Aprender con ejemplos prácticos
- **✅ Cobertura de Pruebas Completa** - Pruebas unitarias extensas y CI/CD

## 🚀 Inicio Rápido

### Instalación

```bash
pip install -e luminoracore/
```

### Uso Básico

```python
from luminoracore import Personality, PersonalityCompiler, LLMProvider

# Cargar una personalidad
personality = Personality("personalities/dr_luna.json")

# Compilar con caché inteligente
compiler = PersonalityCompiler(cache_size=128)
result = compiler.compile(personality, LLMProvider.OPENAI)

# Usar el prompt compilado
print(result.prompt)
print(f"Tokens estimados: {result.token_estimate}")
print(f"Metadatos: {result.metadata}")

# Estadísticas de caché
stats = compiler.get_cache_stats()
print(f"Tasa de aciertos: {stats['hit_rate']}%")
```

### Uso Avanzado

```python
from luminoracore import PersonalityBlender

# Mezclar personalidades
blender = PersonalityBlender()
blended = blender.blend(
    personalities=[personality1, personality2],
    weights=[0.7, 0.3],
    strategy="weighted_average"
)

# Validar con verificaciones de rendimiento
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

## 🔧 Supported LLM Providers

- **OpenAI** - GPT-3.5, GPT-4, GPT-4 Turbo
- **Anthropic** - Claude 3 Sonnet, Claude 3 Opus
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

## 📊 Roadmap

- [ ] **v0.2.0** - Additional LLM provider support
- [ ] **v0.3.0** - Personality marketplace
- [ ] **v0.4.0** - Advanced blending algorithms
- [ ] **v0.5.0** - Real-time personality adaptation
- [ ] **v1.0.0** - Production-ready stable release

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
