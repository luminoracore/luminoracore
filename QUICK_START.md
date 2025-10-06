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

## ✨ Next Steps

1. ✅ **Install**: `.\install_all.ps1` or `./install_all.sh`
2. ✅ **Verify**: Run the 3 quick start scripts
3. ✅ **Explore**: Read [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
4. ✅ **Practice**: Run examples in `luminoracore/examples/`
5. ✅ **Create**: Make your first personality with `luminoracore create --interactive`

---

**Need help?** Read the [Complete Guide](INSTALLATION_GUIDE.md) or check [ESTADO_ACTUAL_PROYECTO.md](ESTADO_ACTUAL_PROYECTO.md)

**Ready to start! 🚀**

