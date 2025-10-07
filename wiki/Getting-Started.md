# Getting Started with LuminoraCore

This guide will help you install and start using LuminoraCore in less than 10 minutes.

---

## ⚡ Express Installation

### Prerequisites
- ✅ Python 3.8 or higher
- ✅ pip (Python package manager)
- ✅ git (to clone repository)
- ✅ Virtual environment (recommended)

### Quick Install (1 Command)

```bash
# Windows
.\install_all.ps1

# Linux/Mac
./install_all.sh
```

This installs all three components:
1. **Base Engine** (luminoracore) - Core personality management
2. **CLI** (luminoracore-cli) - Command-line interface
3. **SDK** (luminoracore-sdk-python) - Python SDK with all providers

---

## ✅ Verify Installation

After installation, run:

```bash
python verify_installation.py
```

**Expected output:**
```
🎉 INSTALLATION COMPLETE AND CORRECT

Installed components:
  ✅ Base Engine/SDK (luminoracore)
  ✅ CLI (luminoracore-cli)
  ✅ Complete SDK (with providers and client)
```

**If you see this, you're ready to go!**

---

## 🎯 What Can You Do Now?

### Option 1: Use the CLI (Command-line)

```bash
# List available personalities
luminoracore list

# Validate a personality
luminoracore validate luminoracore/luminoracore/personalities/dr_luna.json

# Compile for OpenAI
luminoracore compile luminoracore/luminoracore/personalities/dr_luna.json --provider openai

# Create a new personality (interactive wizard)
luminoracore create --interactive

# Start development server with web UI
luminoracore serve
```

### Option 2: Use the Core Engine (Python Library)

```python
from luminoracore import Personality, PersonalityCompiler, LLMProvider

# Load a personality
personality = Personality("luminoracore/luminoracore/personalities/dr_luna.json")

# Compile for OpenAI
compiler = PersonalityCompiler()
result = compiler.compile(personality, LLMProvider.OPENAI)

print(f"Prompt: {result.prompt[:200]}...")
print(f"Tokens: {result.token_estimate}")
```

### Option 3: Use the SDK (Full Application)

```python
import asyncio
import os
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.provider import ProviderConfig

async def main():
    # Initialize client
    client = LuminoraCoreClient()
    await client.initialize()
    
    # Configure provider (DeepSeek - most economical)
    provider_config = ProviderConfig(
        name="deepseek",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        model="deepseek-chat"
    )
    
    # Create session
    session_id = await client.create_session(
        personality_name="dr_luna",
        provider_config=provider_config
    )
    
    # Send message (REAL API call)
    response = await client.send_message(
        session_id=session_id,
        message="Can you explain quantum entanglement?"
    )
    
    print(f"Response: {response.content}")
    print(f"Tokens: {response.usage}")
    
    await client.cleanup()

asyncio.run(main())
```

---

## 🔑 Configure API Keys (Optional)

API keys are only needed if you want to make **real calls to LLMs**.

### Windows PowerShell
```powershell
$env:DEEPSEEK_API_KEY="sk-your-api-key"
$env:OPENAI_API_KEY="sk-your-api-key"
$env:ANTHROPIC_API_KEY="sk-ant-your-api-key"
```

### Linux/Mac
```bash
export DEEPSEEK_API_KEY="sk-your-api-key"
export OPENAI_API_KEY="sk-your-api-key"
export ANTHROPIC_API_KEY="sk-ant-your-api-key"
```

### Where to Get API Keys?
- **DeepSeek** (💰 cheapest): https://platform.deepseek.com/
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/

---

## 📖 Next Steps

### For Beginners
1. ✅ Read: [QUICK_START.md](https://github.com/luminoracore/luminoracore/blob/main/QUICK_START.md)
2. ✅ Try: Run the included examples (`quick_start_core.py`, `quick_start_cli.py`, `quick_start_sdk.py`)
3. ✅ Explore: List and validate the 11 included personalities
4. ✅ Create: Make your first custom personality with `luminoracore create --interactive`

### For Advanced Users
1. 📖 Read: [INSTALLATION_GUIDE.md](https://github.com/luminoracore/luminoracore/blob/main/INSTALLATION_GUIDE.md) (complete details)
2. 📖 Read: [CREATING_PERSONALITIES.md](https://github.com/luminoracore/luminoracore/blob/main/CREATING_PERSONALITIES.md)
3. 🧪 Explore: Run the examples in `luminoracore/examples/`
4. 🔧 Build: Integrate LuminoraCore into your application

### For Developers
1. 📖 Read: Component READMEs (Core, CLI, SDK)
2. 🧪 Run: `pytest tests/ -v` (90/91 tests)
3. 🔍 Explore: Source code structure
4. 🤝 Contribute: See [Contributing Guide](https://github.com/luminoracore/luminoracore/blob/main/CONTRIBUTING.md)

---

## ❓ Common Questions

**Q: Do I need a database?**  
A: No. By default everything works in memory. Databases are optional for persistence.

**Q: Do I need to install all LLM providers?**  
A: No. Install only what you need. For example: `pip install ".[deepseek]"` for just DeepSeek.

**Q: Which storage should I use?**  
A: 
- Testing/demos → `memory`
- Mobile apps → `sqlite`
- Simple apps → `json`
- Production web → `redis`
- Enterprise → `postgres`

**Q: Is it production ready?**  
A: Yes. 90/91 tests passing (100% executable), comprehensive documentation, and battle-tested.

---

## 🆘 Need Help?

### Installation Problems?
1. Run: `python verify_installation.py`
2. Read: [INSTALLATION_VERIFICATION.md](https://github.com/luminoracore/luminoracore/blob/main/INSTALLATION_VERIFICATION.md)
3. Check: [Troubleshooting Wiki Page](Troubleshooting)

### General Questions?
1. Check: [FAQ Wiki Page](FAQ)
2. Read: [DOCUMENTATION_INDEX.md](https://github.com/luminoracore/luminoracore/blob/main/DOCUMENTATION_INDEX.md)
3. Ask: [GitHub Issues](https://github.com/luminoracore/luminoracore/issues)

### Want Examples?
1. Quick starts: `quick_start_core.py`, `quick_start_cli.py`, `quick_start_sdk.py`
2. Advanced examples: `luminoracore/examples/`
3. SDK examples: `luminoracore-sdk-python/examples/`

---

## 🎓 Learning Path

### Week 1: Basics
- Day 1: Install and verify
- Day 2: Try the CLI commands
- Day 3: Explore included personalities
- Day 4: Create your first custom personality
- Day 5: Test with real LLM (DeepSeek recommended)

### Week 2: Intermediate
- Day 1: Blend two personalities
- Day 2: Use the SDK for a simple chatbot
- Day 3: Try different storage backends
- Day 4: Test multiple providers
- Day 5: Build a small application

### Week 3+: Advanced
- Deploy to production
- Custom storage backends
- Performance optimization
- Advanced blending strategies
- Contribute to the project

---

## 🌟 Popular Workflows

### 1. Create and Test a Personality
```bash
# Create
luminoracore create --interactive

# Validate
luminoracore validate my_personality.json

# Test with real API
luminoracore test my_personality.json --provider deepseek
```

### 2. Blend Personalities
```bash
# Blend 60% scientist + 40% motivator
luminoracore blend \
  "luminoracore/luminoracore/personalities/dr_luna.json:0.6" \
  "luminoracore/luminoracore/personalities/rocky_inspiration.json:0.4" \
  --output my_blend.json

# Validate the blend
luminoracore validate my_blend.json
```

### 3. Build a Chatbot with SDK
```python
import asyncio
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.types.session import StorageConfig

async def chatbot():
    client = LuminoraCoreClient(
        storage_config=StorageConfig(storage_type="json", json_file_path="./chat_history.json")
    )
    await client.initialize()
    
    provider = ProviderConfig(name="deepseek", api_key="sk-...", model="deepseek-chat")
    session_id = await client.create_session("dr_luna", provider)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        
        response = await client.send_message(session_id, user_input)
        print(f"AI: {response.content}")
    
    await client.cleanup()

asyncio.run(chatbot())
```

---

**Ready to dive deeper? Check out our [Core Concepts](Core-Concepts) page!**

**Having issues? Visit our [Troubleshooting](Troubleshooting) page!**

---

_Last updated: October 2025 | LuminoraCore v1.0.0_

