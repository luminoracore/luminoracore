# Frequently Asked Questions (FAQ)

---

## 📦 Installation & Setup

### Q: Do I need to install all three components?

**A: No.** Install only what you need:

- **Just exploring?** → Install Core Engine only
- **Want terminal commands?** → Install Core + CLI
- **Building an app?** → Install Core + SDK
- **Want everything?** → Use `install_all.ps1` or `install_all.sh`

### Q: Do I need a database?

**A: No.** LuminoraCore offers multiple storage options:

| Storage | Persistent | Requires | Best For |
|---------|-----------|----------|----------|
| `memory` | ❌ No | Nothing | Testing, demos |
| `json` | ✅ Yes | Only disk | Simple apps, portability |
| `sqlite` | ✅ Yes | Only disk | Mobile apps, desktop |
| `redis` | ✅ Yes | Redis server | Production web |
| `postgres` | ✅ Yes | PostgreSQL | Enterprise |
| `mongodb` | ✅ Yes | MongoDB | Document-based |

**Default is `memory` (no DB required).**

### Q: Which Python version do I need?

**A: Python 3.8 or higher.** Recommended: Python 3.11.

Tested on:
- ✅ Python 3.8
- ✅ Python 3.9
- ✅ Python 3.10
- ✅ Python 3.11 (recommended)
- ✅ Python 3.12

### Q: Can I use this on Windows?

**A: Yes.** LuminoraCore is fully compatible with:
- ✅ Windows 10/11
- ✅ Linux (Ubuntu, Debian, etc.)
- ✅ macOS

**Note:** Windows has specific installation requirements (no `-e` flag for Base Engine). See [INSTALLATION_GUIDE.md](https://github.com/luminoracore/luminoracore/blob/main/INSTALLATION_GUIDE.md).

### Q: Do I need a virtual environment?

**A: Highly recommended.** While not strictly required, using a virtual environment avoids dependency conflicts.

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source venv/bin/activate
```

---

## 🔑 API Keys & Providers

### Q: Do I need API keys to use LuminoraCore?

**A: Not for basic functionality.**

- **Without API keys:** You can create, validate, compile, and blend personalities
- **With API keys:** You can make real calls to LLMs (for chatbots, apps, etc.)

### Q: Which LLM provider should I use?

**A: Depends on your needs:**

| Provider | Best For | Cost | Quality |
|----------|----------|------|---------|
| **DeepSeek** 💰 | Budget, development | 💰 Cheapest (~$0.14/1M tokens) | Good |
| **OpenAI** | General purpose | 💰💰 Medium | Excellent |
| **Anthropic** | Long contexts, safety | 💰💰💰 Higher | Excellent |
| **Google Gemini** | Multimodal | 💰💰 Medium | Very Good |
| **Mistral** | EU data residency | 💰💰 Medium | Good |
| **Cohere** | Embeddings, search | 💰💰 Medium | Good |
| **Llama** | Open source | 💰 Low | Good |

**Recommendation for getting started: DeepSeek** (cheapest, good quality)

### Q: How do I get API keys?

**A:** Visit these links:

- **DeepSeek**: https://platform.deepseek.com/
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Mistral**: https://console.mistral.ai/
- **Cohere**: https://dashboard.cohere.ai/
- **Google**: https://makersuite.google.com/app/apikey

**Then configure as environment variables:**

```bash
# Windows PowerShell
$env:DEEPSEEK_API_KEY="sk-your-key"

# Linux/Mac
export DEEPSEEK_API_KEY="sk-your-key"
```

### Q: Do I need to install ALL LLM providers?

**A: No.** Install only what you need:

```bash
# Just DeepSeek (recommended for dev)
pip install ".[deepseek]"

# Just OpenAI
pip install ".[openai]"

# Multiple providers
pip install ".[deepseek,openai,anthropic]"

# All providers (for production/testing)
pip install ".[all]"
```

---

## 🎭 Personalities

### Q: What is a "personality"?

**A:** A JSON file that defines how an AI should behave:

```json
{
  "persona": {
    "name": "Dr. Luna",
    "description": "Enthusiastic scientist who explains concepts clearly"
  },
  "core_traits": {
    "archetype": "scientist",
    "temperament": "enthusiastic",
    "communication_style": "educational"
  },
  "linguistic_profile": {
    "tone": ["enthusiastic", "friendly", "professional"],
    "vocabulary_level": "intermediate"
  }
}
```

### Q: How many personalities are included?

**A: 11 personalities** are included by default:

- 🧪 Dr. Luna (Scientific Enthusiast)
- ⚓ Captain Hook Digital (Adventurous Leader)
- 😏 Marcus Sarcasmus (Sarcastic Wit)
- 💪 Rocky Inspiration (Motivational Coach)
- 💼 Victoria Sterling (Professional Executive)
- 👵 Grandma Hope (Caring Mentor)
- 🎨 Lila Charm (Creative Artist)
- 📚 Prof. Rigoberto (Academic Expert)
- 💻 Zero Cool (Tech Hacker)
- 🤖 Alex Digital (AI Assistant)
- 🎯 AI Assistant (General Purpose)

**Location:** `luminoracore/luminoracore/personalities/`

### Q: Can I create my own personalities?

**A: Yes!** Use the interactive wizard:

```bash
luminoracore create --interactive
```

Or manually create a JSON file following the schema. See [CREATING_PERSONALITIES.md](https://github.com/luminoracore/luminoracore/blob/main/CREATING_PERSONALITIES.md).

### Q: What is PersonaBlend™?

**A:** A technology that lets you blend multiple personalities with custom weights:

```bash
# 70% scientist + 30% motivator = Enthusiastic Scientist Coach
luminoracore blend \
  "dr_luna.json:0.7" \
  "rocky_inspiration.json:0.3" \
  --output blend.json
```

**How it works:**
- Mathematical fusion of personality traits
- Weighted average of numerical values
- Smart combination of text fields
- Deterministic results (no randomness)

**More details:** [Core Concepts - PersonaBlend](Core-Concepts#personablend-technology)

---

## 🐍 Python & Development

### Q: Is the SDK asynchronous?

**A: Yes.** The SDK is fully asynchronous using `async/await`:

```python
import asyncio

async def main():
    client = LuminoraCoreClient()
    await client.initialize()
    # ... async operations
    await client.cleanup()

asyncio.run(main())
```

### Q: Can I use this in a Lambda function?

**A: Yes.** LuminoraCore SDK works perfectly in AWS Lambda:

```python
import os
import asyncio
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.provider import ProviderConfig

client = LuminoraCoreClient()  # Reuse between invocations

async def _handle(event):
    await client.initialize()
    # ... your logic
    return response

def handler(event, context):
    return asyncio.run(_handle(event))
```

**Tip:** Create a Lambda Layer with the SDK to reduce deployment size.

### Q: Does it work with Docker?

**A: Yes.** Each component includes a Dockerfile:

```bash
# Core Engine
cd luminoracore
docker build -t luminoracore .

# SDK
cd luminoracore-sdk-python
docker-compose up
```

### Q: Can I use this in mobile apps?

**A: Yes.** Use SQLite storage for mobile:

```python
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="sqlite",
        sqlite_path="./app_data/luminoracore.db"
    )
)
```

---

## 🔧 Features & Functionality

### Q: What does "compile" mean?

**A:** Converting a personality JSON to a text prompt for an LLM:

```python
# Input: personality JSON (structured data)
personality = Personality("dr_luna.json")

# Output: text prompt optimized for the provider
compiler = PersonalityCompiler()
result = compiler.compile(personality, LLMProvider.OPENAI)
# → "You are Dr. Luna, an enthusiastic scientist who..."
```

**Different providers need different prompt formats.** LuminoraCore handles this automatically.

### Q: Can I switch personalities mid-conversation?

**A: Yes** (with SDK):

```python
# Start with one personality
session_id = await client.create_session("dr_luna", provider_config)

# Switch to another
await client.switch_personality(session_id, "rocky_inspiration")
```

### Q: Does it support streaming?

**A: Yes** (SDK):

```python
async for chunk in client.stream_message(session_id, "Tell me a story"):
    print(chunk.content, end="", flush=True)
```

### Q: Can I use custom LLM endpoints?

**A: Yes.** Override `base_url`:

```python
provider_config = ProviderConfig(
    name="openai",
    api_key="your-key",
    base_url="http://localhost:11434/v1",  # Ollama, for example
    model="llama2"
)
```

---

## 🧪 Testing & Development

### Q: How do I run the tests?

**A:**

```bash
# All tests
pytest tests/ -v

# Specific component
pytest tests/test_1_motor_base.py -v   # Core (28 tests)
pytest tests/test_2_cli.py -v          # CLI (26 tests)
pytest tests/test_3_sdk.py -v          # SDK (37 tests)
```

**Expected result:** 90 passed, 1 skipped

### Q: Why is 1 test skipped?

**A:** The skipped test requires a real API key for external validation. All executable tests (100%) pass.

### Q: Can I test without API keys?

**A: Yes.** Most functionality works without API keys:
- ✅ Create personalities
- ✅ Validate JSON
- ✅ Compile prompts
- ✅ Blend personalities
- ❌ Make real LLM calls (requires API key)

---

## 🚀 Deployment & Production

### Q: Is it production-ready?

**A: Yes.**
- ✅ 179/179 tests passing (v1.1 production ready)
- ✅ Comprehensive error handling
- ✅ Type safety (Pydantic)
- ✅ Async/await support
- ✅ Multiple storage backends
- ✅ Monitoring and logging

### Q: How do I deploy to production?

**A:** Multiple options:

1. **AWS Lambda** (recommended for serverless)
   - Create Lambda Layer with SDK
   - Use environment variables for API keys
   - Configure storage (Redis/PostgreSQL)

2. **Docker/Kubernetes**
   - Use included Dockerfiles
   - Configure via environment variables
   - Scale horizontally

3. **Traditional Server**
   - Install via pip
   - Use systemd/supervisor
   - Configure storage backend

**See:** [INSTALLATION_GUIDE.md - Advanced Configuration](https://github.com/luminoracore/luminoracore/blob/main/INSTALLATION_GUIDE.md)

### Q: How do I handle errors in production?

**A:** The SDK provides comprehensive error handling:

```python
from luminoracore_sdk.utils.exceptions import ProviderError, SessionError, StorageError

try:
    response = await client.send_message(session_id, message)
except ProviderError as e:
    # LLM API error
    logger.error(f"Provider error: {e}")
except SessionError as e:
    # Session/conversation error
    logger.error(f"Session error: {e}")
except StorageError as e:
    # Storage backend error
    logger.error(f"Storage error: {e}")
```

---

## 💰 Cost & Performance

### Q: How much does it cost to use?

**A:** LuminoraCore itself is **free and open source**. You only pay for:

1. **LLM API calls** (depends on provider and usage)
2. **Storage** (if using cloud databases like Redis/PostgreSQL)

**Cost comparison (per 1M tokens):**
- DeepSeek: ~$0.14 💰 (cheapest)
- GPT-3.5: ~$2.00
- GPT-4: ~$30.00
- Claude 3: ~$15.00

**Tip:** Use DeepSeek for development and testing.

### Q: How can I reduce costs?

**A:**
1. Use **DeepSeek** instead of OpenAI
2. Use **caching** (enabled by default in compiler)
3. Use **shorter prompts** (optimize personality JSON)
4. Use **lower temperature** (more deterministic = less retries)
5. Use **max_tokens** limits

### Q: Is there token usage tracking?

**A: Yes.** The SDK tracks token usage in real-time:

```python
response = await client.send_message(session_id, message)
print(f"Tokens used: {response.usage}")
# → {'prompt_tokens': 150, 'completion_tokens': 50, 'total_tokens': 200}
```

---

## 🔧 Technical Questions

### Q: What's the difference between Core, CLI, and SDK?

**A:**

| Component | What It Is | Use When |
|-----------|-----------|----------|
| **Core Engine** | Python library | Building apps, need programmatic access |
| **CLI** | Terminal tool | Quick testing, development, automation |
| **SDK** | Full client | Production apps, real LLM calls, sessions |

**All three use the same Core Engine internally.**

### Q: Can I use this without the CLI or SDK?

**A: Yes.** The Core Engine works standalone:

```python
from luminoracore import Personality, PersonalityCompiler, LLMProvider

personality = Personality("path/to/personality.json")
compiler = PersonalityCompiler()
result = compiler.compile(personality, LLMProvider.OPENAI)
```

### Q: Does the Core Engine make LLM calls?

**A: No.** The Core Engine only:
- ✅ Loads and validates personalities
- ✅ Compiles to prompts
- ✅ Blends personalities

**Only the SDK makes real LLM API calls.**

### Q: Why are there nested directories (luminoracore/luminoracore/)?

**A:** Standard Python package structure:

```
luminoracore/              ← Repository root
└── luminoracore/          ← Python package (with setup.py)
    └── luminoracore/      ← Source code
        ├── __init__.py
        ├── core/
        └── tools/
```

**This is normal Python convention.** Install from the middle directory (where `setup.py` is).

---

## 🎨 Personality Creation

### Q: How do I create a personality?

**A:** Three ways:

1. **Interactive wizard** (easiest):
   ```bash
   luminoracore create --interactive
   ```

2. **From template**:
   ```bash
   luminoracore create --template assistant --name "My Assistant"
   ```

3. **Manual JSON** (advanced):
   - Copy `_template.json`
   - Edit the fields
   - Validate with `luminoracore validate my_personality.json`

**See:** [CREATING_PERSONALITIES.md](https://github.com/luminoracore/luminoracore/blob/main/CREATING_PERSONALITIES.md)

### Q: What fields are required in a personality JSON?

**A:** 9 main sections:

1. `persona` - Basic info (name, description)
2. `core_traits` - Archetype, temperament, communication style
3. `linguistic_profile` - Tone, vocabulary, expressions
4. `behavioral_rules` - Do's and don'ts
5. `response_patterns` - How to respond
6. `context_adaptation` - Context awareness
7. `examples` - Sample conversations
8. `advanced_parameters` - Temperature, max_tokens, etc.
9. `metadata` - Version, author, tags

**All fields are validated against JSON Schema.**

### Q: Can I modify included personalities?

**A: Yes.** But we recommend:
- Copy the personality to a new file
- Modify the copy
- Keep originals for reference

---

## 🔄 Blending & Advanced Features

### Q: How does PersonaBlend™ work?

**A:** Mathematical fusion of personality traits:

1. **Numerical values** → Weighted average
2. **Categories** (e.g., archetype) → Majority vote with weights
3. **Lists** (e.g., tone) → Ranked combination (top N)
4. **Text** → Base from highest weight + key elements from others

**Example:**
```python
# 70% Dr. Luna (scientist) + 30% Rocky (motivator)
blender = PersonalityBlender()
result = blender.blend_personalities(
    [dr_luna, rocky],
    weights=[0.7, 0.3]
)
# → Enthusiastic scientist who also motivates
```

### Q: Can I blend more than 2 personalities?

**A: Yes.** Blend as many as you want:

```bash
luminoracore blend \
  "personality1.json:0.5" \
  "personality2.json:0.3" \
  "personality3.json:0.2" \
  --output blend.json
```

### Q: Is blending deterministic?

**A: Yes.** Same personalities + same weights = same result (always).

---

## 🐛 Troubleshooting

### Q: "ModuleNotFoundError: No module named 'luminoracore'"

**A:** Solutions:
1. Make sure virtual environment is activated
2. Reinstall: `cd luminoracore && pip install .`
3. Check you're in the right directory

### Q: "ImportError: cannot import name 'Personality' from 'luminoracore'"

**A:** (Windows only) - Base Engine was installed incorrectly:

```powershell
# Uninstall and reinstall in normal mode
pip uninstall luminoracore -y
cd luminoracore
pip install .  # WITHOUT -e
```

### Q: "Command 'luminoracore' not found"

**A:** CLI not installed or not in PATH:

```bash
# Reinstall CLI
cd luminoracore-cli
pip install .

# Or use Python module syntax
python -m luminoracore_cli --help
```

### Q: Installation fails with "neither 'setup.py' nor 'pyproject.toml' found"

**A:** You're in the wrong directory. Navigate to where `setup.py` exists:

```bash
# Check current location
pwd  # or 'cd' on Windows

# Look for setup.py
ls | grep setup.py  # Linux/Mac
dir | findstr setup.py  # Windows

# If you don't see setup.py, go up one level
cd ..
```

---

## 📚 Learning & Resources

### Q: Where should I start?

**A:** Follow this path:

1. ✅ Install: `.\install_all.ps1` (Windows) or `./install_all.sh` (Linux/Mac)
2. ✅ Verify: `python verify_installation.py`
3. ✅ Read: [QUICK_START.md](https://github.com/luminoracore/luminoracore/blob/main/QUICK_START.md) (5 min)
4. ✅ Try: `luminoracore list` and explore personalities
5. ✅ Create: Your first personality with `luminoracore create --interactive`
6. ✅ Build: A simple app with the SDK

### Q: Where is the complete documentation?

**A:**
- **Installation**: [INSTALLATION_GUIDE.md](https://github.com/luminoracore/luminoracore/blob/main/INSTALLATION_GUIDE.md)
- **Creating Personalities**: [CREATING_PERSONALITIES.md](https://github.com/luminoracore/luminoracore/blob/main/CREATING_PERSONALITIES.md)
- **Quick Reference**: [CHEATSHEET.md](https://github.com/luminoracore/luminoracore/blob/main/CHEATSHEET.md)
- **All Docs**: [DOCUMENTATION_INDEX.md](https://github.com/luminoracore/luminoracore/blob/main/DOCUMENTATION_INDEX.md)

### Q: Are there examples?

**A: Yes.** Multiple examples:

**Quick starts:**
- `quick_start_core.py` - Core Engine basics
- `quick_start_cli.py` - CLI verification
- `quick_start_sdk.py` - SDK basics

**Advanced examples:**
- `luminoracore/examples/basic_usage.py`
- `luminoracore/examples/blending_demo.py`
- `luminoracore/examples/multi_llm_demo.py`
- `luminoracore/examples/performance_demo.py`
- `luminoracore/examples/personality_switching.py`

**SDK examples:**
- `luminoracore-sdk-python/examples/basic_usage.py`
- `luminoracore-sdk-python/examples/personality_blending.py`

---

## 🤝 Contributing & Community

### Q: How can I contribute?

**A:** Many ways:

1. 🐛 **Report bugs** - Create an issue
2. 💡 **Suggest features** - Create a feature request
3. 🎭 **Submit personalities** - Share your creations
4. 📚 **Improve docs** - Fix typos, add examples
5. 🧪 **Add tests** - Improve coverage
6. 🔧 **Fix issues** - Submit PRs

**See:** [Contributing Guide](https://github.com/luminoracore/luminoracore/blob/main/CONTRIBUTING.md)

### Q: Can I submit my own personalities?

**A: Yes!** We welcome personality submissions:

1. Create your personality JSON
2. Validate: `luminoracore validate your_personality.json`
3. Test: `luminoracore test your_personality.json --provider deepseek`
4. Submit: Create a PR or issue with [PERSONALITY] tag

### Q: Is there a community?

**A:** We're building it! Join us:
- 🐛 [GitHub Issues](https://github.com/luminoracore/luminoracore/issues)
- 📖 [Wiki](https://github.com/luminoracore/luminoracore/wiki)
- ⭐ Star the project to stay updated

---

## 📄 License & Usage

### Q: What license is LuminoraCore?

**A: MIT License.** You can:
- ✅ Use commercially
- ✅ Modify the code
- ✅ Distribute
- ✅ Use in proprietary software
- ✅ No attribution required (but appreciated!)

### Q: Can I use this in commercial products?

**A: Yes, absolutely.** MIT license allows commercial use without restrictions.

### Q: Do I need to credit LuminoraCore?

**A: Not required,** but appreciated:

```
Powered by LuminoraCore - https://github.com/luminoracore/luminoracore
```

---

## ❓ Still Have Questions?

1. **Check:** [Troubleshooting Wiki Page](Troubleshooting)
2. **Read:** [Complete Documentation Index](https://github.com/luminoracore/luminoracore/blob/main/DOCUMENTATION_INDEX.md)
3. **Ask:** [Create an Issue](https://github.com/luminoracore/luminoracore/issues/new)

---

**Can't find your answer? [Ask us on GitHub Issues](https://github.com/luminoracore/luminoracore/issues/new)**

---

_Last updated: October 2025 | LuminoraCore v1.0.0_

