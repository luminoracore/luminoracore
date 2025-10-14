# 🚀 Quick Start - LuminoraCore

**First time using LuminoraCore? Start here!**

---

## ⚡ Express Installation (1 command)

### Windows (PowerShell)

```powershell
.\install_all.ps1
```

### Linux/Mac

```bash
chmod +x install_all.sh
./install_all.sh
```

**This will install:**
- ✅ luminoracore (base engine)
- ✅ luminoracore-cli (CLI tool)
- ✅ luminoracore-sdk (complete SDK)

---

## ✅ Verify Installation

### Option 1: Automatic Script (Recommended)

```bash
# Download the script (if you don't have it)
curl -O https://raw.githubusercontent.com/your-user/luminoracore/main/verify_installation.py

# Run complete verification
python verify_installation.py
```

**Expected output:** `🎉 INSTALLATION COMPLETE AND CORRECT`

### Option 2: Example Scripts (Step by Step)

```bash
# 1. Test base engine
python ejemplo_quick_start_core.py

# 2. Test CLI
python ejemplo_quick_start_cli.py

# 3. Test SDK
python ejemplo_quick_start_sdk.py
```

If all show ✅, you're ready!

---

## 📚 Which Component Do I Need?

### 🧠 **luminoracore** (Base Engine)

**Use it if you need:**
- Load and validate AI personalities
- Compile personalities for different LLMs
- Blend personalities (PersonaBlend™)
- No external API connections

**Example:**
```python
from luminoracore import Personality, PersonalityValidator

personality = Personality("my_personality.json")
validator = PersonalityValidator()
result = validator.validate(personality)
```

---

### 🛠️ **luminoracore-cli** (CLI Tool)

**Use it if you need:**
- Work with personalities from the terminal
- Create personalities with interactive wizard
- Development server with web interface
- Validate and compile without writing code

**Example:**
```bash
# List personalities
luminoracore list

# Validate a personality
luminoracore validate my_personality.json

# Start web server
luminoracore serve
```

---

### 🐍 **luminoracore-sdk** (Complete SDK)

**Use it if you need:**
- Build complete AI applications
- REAL connections to OpenAI, Anthropic, etc.
- Session and conversation management
- Persistent memory (Redis, PostgreSQL, MongoDB)
- Monitoring and metrics

**Example:**
```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig

async def main():
    client = LuminoraCoreClient()
    await client.initialize()
    
    # Configure OpenAI
    provider_config = ProviderConfig(
        name="openai",
        api_key="your-api-key",
        model="gpt-3.5-turbo"
    )
    
    # Create session
    session_id = await client.create_session(
        personality_name="assistant",
        provider_config=provider_config
    )
    
    # Send message (REAL CONNECTION!)
    response = await client.send_message(
        session_id=session_id,
        message="Hello, how are you?"
    )
    
    print(response.content)
    await client.cleanup()

asyncio.run(main())
```

---

## 🎯 Common Use Cases

### 1. I just want to validate personality files
👉 Use **luminoracore-cli**
```bash
luminoracore validate personalities/*.json
```

### 2. I want to create a chatbot with personality
👉 Use **luminoracore-sdk**
```python
# See ejemplo_quick_start_sdk.py
```

### 3. I want to blend two personalities
👉 Use **luminoracore** (code) or **luminoracore-cli** (terminal)
```bash
# CLI
luminoracore blend persona1.json:0.6 persona2.json:0.4

# Code
from luminoracore import PersonalityBlender
blender = PersonalityBlender()
blended = blender.blend(personalities=[p1, p2], weights=[0.6, 0.4])
```

### 4. I need a graphical interface for testing
👉 Use **luminoracore-cli serve**
```bash
luminoracore serve
# Open http://localhost:8000
```

---

## 🔑 Configure API Keys (SDK Only)

If you're making REAL API calls to LLMs:

### OpenAI

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-api-key-here"

# Linux/Mac
export OPENAI_API_KEY="sk-your-api-key-here"
```

### Anthropic

```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-your-api-key-here"

# Linux/Mac
export ANTHROPIC_API_KEY="sk-ant-your-api-key-here"
```

**Get API keys:**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
- Cohere: https://dashboard.cohere.ai/

---

## 📖 Complete Documentation

- **Complete Guide**: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- **Project Status**: [ESTADO_ACTUAL_PROYECTO.md](ESTADO_ACTUAL_PROYECTO.md)
- **Technical Features**: [CARACTERISTICAS_TECNICAS_LUMINORACORE.md](CARACTERISTICAS_TECNICAS_LUMINORACORE.md)

---

## 🆘 Common Issues

### Error: "ModuleNotFoundError: No module named 'luminoracore'"

```bash
# Activate virtual environment
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate

# Reinstall
cd luminoracore && pip install -e . && cd ..
```

### Error: "Command 'luminoracore' not found"

```bash
cd luminoracore-cli
pip install -e .
cd ..
```

### Error: "Permission denied" on Windows

```powershell
# Run in PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🎓 Learn More

### Included Examples

```bash
# Base engine
python luminoracore/examples/basic_usage.py
python luminoracore/examples/blending_demo.py

# SDK
python luminoracore-sdk-python/examples/simple_usage.py
python luminoracore-sdk-python/examples/personality_blending.py
```

### Interactive CLI

```bash
# Interactive mode for creating personalities
luminoracore create --interactive

# Explore available personalities
luminoracore list --detailed

# Development server
luminoracore serve
```

---

## 📊 Command Summary

```bash
# Installation
.\install_all.ps1          # Windows
./install_all.sh           # Linux/Mac

# Verification
python ejemplo_quick_start_core.py
python ejemplo_quick_start_cli.py
python ejemplo_quick_start_sdk.py

# CLI
luminoracore --help          # See help
luminoracore list            # List personalities
luminoracore validate <file> # Validate
luminoracore compile <file>  # Compile
luminoracore serve           # Web server

# Python
from luminoracore import Personality, PersonalityValidator
from luminoracore import LuminoraCoreClient  # SDK
```

---

## 🎉 What's New in v1.1 - Memory & Relationships

LuminoraCore v1.1 adds powerful memory and relationship features! Here's how to get started:

### 🚀 Quick v1.1 Setup

```bash
# 1. Setup v1.1 database
.\scripts\setup-v1_1-database.ps1  # Windows
./scripts/setup-v1_1-database.sh   # Linux/Mac

# 2. Run v1.1 examples
python examples/v1_1_affinity_demo.py
python examples/v1_1_memory_demo.py
python examples/v1_1_dynamic_personality_demo.py
```

### ✨ v1.1 Features

- **🎭 Hierarchical Personalities** - Relationship levels that evolve (stranger → friend → soulmate)
- **💝 Affinity Tracking** - Track relationship points (0-100)
- **🧠 Fact Extraction** - Automatically learn from conversations (9 categories)
- **📖 Episodic Memory** - Remember memorable moments (7 types)
- **🏷️ Memory Classification** - Smart organization by importance
- **🚩 Feature Flags** - Safe, gradual feature rollout
- **🗄️ Database Migrations** - Structured schema management

### 🔧 v1.1 CLI Commands

```bash
# Database migrations
luminora-cli migrate --status
luminora-cli migrate up

# Memory management
luminora-cli memory facts --session-id user_123
luminora-cli memory episodes --session-id user_123

# Snapshots
luminora-cli snapshot create --session-id user_123 --output backup.json
luminora-cli snapshot restore --input backup.json
```

### 📚 v1.1 Documentation

- **[Quick Start v1.1](mejoras_v1.1/QUICK_START_V1_1.md)** - 5-minute tutorial
- **[v1.1 Features Summary](mejoras_v1.1/V1_1_FEATURES_SUMMARY.md)** - Complete feature list
- **[v1.1 API Guide](luminoracore/docs/v1_1_features.md)** - API reference
- **[Technical Architecture](mejoras_v1.1/TECHNICAL_ARCHITECTURE.md)** - Database schema

---

## ✨ Next Steps

### For v1.0 (Getting Started)
1. ✅ **Install**: `.\install_all.ps1` or `./install_all.sh`
2. ✅ **Verify**: Run the 3 quick start scripts
3. ✅ **Explore**: Read [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
4. ✅ **Practice**: Run examples in `luminoracore/examples/`
5. ✅ **Create**: Make your first personality with `luminoracore create --interactive`

### For v1.1 (Advanced Features)
6. ✅ **Setup v1.1**: Run `./scripts/setup-v1_1-database.sh`
7. ✅ **Try v1.1**: Run v1.1 examples
8. ✅ **Learn v1.1**: Read [v1.1 Quick Start](mejoras_v1.1/QUICK_START_V1_1.md)
9. ✅ **Explore Memory**: Test fact extraction and episodic memory
10. ✅ **Track Affinity**: Implement relationship tracking

---

**Need help?** Read the [Complete Guide](INSTALLATION_GUIDE.md) or check [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)

**Ready to start! 🚀**

**v1.1 Production Ready:** 179 tests passing • 100% backward compatible

