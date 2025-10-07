# Troubleshooting Guide

This page covers common problems and their solutions.

---

## 🔧 Installation Issues

### Problem 1: "neither 'setup.py' nor 'pyproject.toml' found"

**❌ Symptom:**
```
ERROR: file:///D:/luminoracore/luminoracore/luminoracore does not appear to be a Python project
```

**🔍 Cause:** You're in the wrong directory (too deep or too high in the folder structure)

**✅ Solution:**

```bash
# 1. Check where you are
pwd      # Linux/Mac
cd       # Windows (shows current path)

# 2. Look for setup.py
ls | grep setup.py      # Linux/Mac
dir | findstr setup.py  # Windows

# 3. Navigate to correct location
# If you're too deep (luminoracore/luminoracore/luminoracore/):
cd ..

# If you're too high (only one luminoracore/):
cd luminoracore

# 4. Verify you see setup.py
ls  # or 'dir' on Windows

# 5. Now install
pip install .  # Windows: without -e
pip install -e .  # Linux/Mac: with -e
```

**📍 Correct structure:**
```
luminoracore/              ← Cloned repo
└── luminoracore/          ← ⭐ YOU SHOULD BE HERE
    ├── setup.py           ← ✅ This file MUST exist
    ├── pyproject.toml
    └── luminoracore/      ← Source code (DON'T enter)
```

---

### Problem 2: "ModuleNotFoundError: No module named 'luminoracore'"

**🔍 Cause:** Virtual environment not activated or package not installed

**✅ Solution:**

```bash
# 1. Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1   # Windows PowerShell
.\venv\Scripts\activate.bat   # Windows CMD
source venv/bin/activate      # Linux/Mac

# You should see (venv) at the start of your prompt

# 2. Verify installation
pip list | grep luminoracore  # Linux/Mac
pip list | findstr luminoracore  # Windows

# 3. If not installed, reinstall
cd luminoracore
pip install .  # Windows
pip install -e .  # Linux/Mac
```

---

### Problem 3: "ImportError: cannot import name 'Personality' from 'luminoracore'" (Windows)

**🔍 Cause:** Base Engine installed in editable mode (`-e`) on Windows, causing namespace conflicts

**✅ Solution:**

```powershell
# 1. Uninstall everything
pip uninstall luminoracore luminoracore-sdk -y

# 2. Reinstall Base Engine in NORMAL mode (without -e)
cd luminoracore
pip install .  # ← WITHOUT -e
cd ..

# 3. Reinstall SDK
cd luminoracore-sdk-python
pip install ".[all]"
cd ..

# 4. Verify
python -c "from luminoracore import Personality; print('✅ OK')"
```

**🚨 IMPORTANT FOR WINDOWS:**
- Base Engine MUST be installed with `pip install .` (no `-e`)
- SDK can use normal installation: `pip install ".[all]"`

---

### Problem 4: "Command 'luminoracore' not found"

**🔍 Cause:** CLI not installed or not in PATH

**✅ Solution:**

```bash
# 1. Reinstall CLI
cd luminoracore-cli
pip install .
cd ..

# 2. Verify it's installed
pip show luminoracore-cli

# 3. Try alternative invocation
python -m luminoracore_cli --help

# 4. If still not working, check PATH
# Windows: where luminoracore
# Linux/Mac: which luminoracore
```

**Alternative:** Use `lc` alias instead of `luminoracore`:
```bash
lc --help
```

---

### Problem 5: Permission denied activating venv on Windows

**❌ Error:**
```
cannot be loaded because running scripts is disabled on this system
```

**✅ Solution:**

```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again:
```powershell
.\venv\Scripts\Activate.ps1
```

---

### Problem 6: "ERROR: Could not install packages due to an OSError: [WinError 2]"

**🔍 Cause:** Windows permission issues with pip trying to replace executables

**✅ Solution:**

```powershell
# 1. Close all PowerShell/CMD windows
# 2. Open NEW PowerShell
# 3. Activate venv
.\venv\Scripts\Activate.ps1

# 4. Uninstall and reinstall
pip uninstall luminoracore-cli -y
pip install luminoracore-cli

# If still fails, use normal installation instead of editable:
cd luminoracore-cli
pip install .  # Instead of pip install -e .
```

---

## 🐍 Runtime Issues

### Problem 7: "Schema validation failed"

**❌ Error:**
```
ValidationError: 'linguistic_profile' is a required property
```

**🔍 Cause:** Personality JSON is missing required fields or has invalid values

**✅ Solution:**

```bash
# 1. Validate to see all errors
luminoracore validate your_personality.json --strict

# 2. Check against template
# Compare your JSON with: luminoracore/luminoracore/personalities/_template.json

# 3. Common issues:
# - Missing required sections (persona, core_traits, linguistic_profile, etc.)
# - Invalid enum values (archetype, temperament, tone)
# - Wrong data types (string instead of array, etc.)
```

**Valid enum values:**
- `archetype`: scientist, adventurer, caregiver, sage, explorer, rebel, magician, hero, lover, jester, ruler, creator, innocent, assistant, coach, creative, teacher
- `temperament`: calm, energetic, balanced, serious, playful
- `communication_style`: formal, casual, technical, conversational, storytelling
- `tone`: warm, professional, friendly, enthusiastic, calm, confident, playful, serious, empathetic, direct, humble, wise, cool, mysterious, adventurous

---

### Problem 8: Provider API Errors

**❌ Error:**
```
ProviderError: OpenAI API error: Incorrect API key provided
```

**✅ Solution:**

```bash
# 1. Verify API key is set
# Windows
echo $env:OPENAI_API_KEY

# Linux/Mac
echo $OPENAI_API_KEY

# 2. If empty, set it
# Windows
$env:OPENAI_API_KEY="sk-your-real-key"

# Linux/Mac
export OPENAI_API_KEY="sk-your-real-key"

# 3. Verify the key is valid
# Visit: https://platform.openai.com/api-keys

# 4. Test with CLI
luminoracore test your_personality.json --provider openai
```

---

### Problem 9: Storage Connection Errors

**❌ Error:**
```
StorageError: Connection to Redis failed
```

**✅ Solution:**

```bash
# 1. Verify service is running
# Redis:
redis-cli ping  # Should return "PONG"

# PostgreSQL:
psql -U your_user -d your_db -c "SELECT 1"

# MongoDB:
mongosh --eval "db.adminCommand('ping')"

# 2. Check connection string
# Redis:
redis://localhost:6379

# PostgreSQL:
postgresql://user:password@localhost/database

# MongoDB:
mongodb://localhost:27017

# 3. For development, use memory storage instead:
client = LuminoraCoreClient(
    storage_config=StorageConfig(storage_type="memory")
)
```

---

### Problem 10: "Personality file not found"

**✅ Solution:**

```python
# Use absolute paths
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
PERSONALITIES_DIR = PROJECT_ROOT / "luminoracore" / "luminoracore" / "personalities"

personality_path = PERSONALITIES_DIR / "dr_luna.json"
personality = Personality(str(personality_path))
```

Or use the correct relative path from your current working directory.

---

## ⚡ Performance Issues

### Problem 11: Slow compilation

**✅ Solutions:**

```python
# 1. Enable caching (enabled by default)
compiler = PersonalityCompiler(cache_size=128)

# 2. Reduce personality complexity
# - Shorter descriptions
# - Fewer examples
# - Simpler behavioral rules

# 3. Check cache statistics
stats = compiler.get_cache_stats()
print(f"Hit rate: {stats['hit_rate']:.2%}")
```

---

### Problem 12: High token usage

**✅ Solutions:**

```python
# 1. Use compact compilation
compiler.compile(personality, provider, include_examples=False)

# 2. Set max_tokens in personality
"advanced_parameters": {
    "max_tokens": 500  # Limit response length
}

# 3. Use cheaper provider
provider_config = ProviderConfig(
    name="deepseek",  # ~20x cheaper than GPT-4
    model="deepseek-chat"
)
```

---

## 🔄 Migration Issues

### Problem 13: Updating from development clone

**✅ Solution:**

```bash
# 1. Check current branch
git branch

# 2. Pull latest changes
git pull origin main

# 3. Reinstall all components
# Windows
.\install_all.ps1

# Linux/Mac
./install_all.sh

# 4. Verify
python verify_installation.py
```

---

### Problem 14: Conflicting package versions

**✅ Solution:**

```bash
# 1. Create fresh virtual environment
python -m venv venv_new

# 2. Activate new environment
.\venv_new\Scripts\Activate.ps1  # Windows
source venv_new/bin/activate     # Linux/Mac

# 3. Clean install
pip install --upgrade pip
.\install_all.ps1  # Windows
./install_all.sh   # Linux/Mac
```

---

## 🧪 Testing Issues

### Problem 15: Tests fail locally

**✅ Solution:**

```bash
# 1. Make sure virtual environment is activated
# You should see (venv) in your prompt

# 2. Install test dependencies
pip install pytest pytest-asyncio

# 3. Run tests from project root
pytest tests/ -v

# 4. If specific tests fail, run individually:
pytest tests/test_1_motor_base.py -v
pytest tests/test_2_cli.py -v
pytest tests/test_3_sdk.py -v

# 5. Check for missing dependencies
pip install -e "luminoracore/[dev]"
pip install -e "luminoracore-cli/[dev]"
pip install -e "luminoracore-sdk-python/[all]"
```

---

## 🌐 Network & API Issues

### Problem 16: Timeout errors

**✅ Solution:**

```python
# Increase timeout in provider config
provider_config = ProviderConfig(
    name="openai",
    api_key="your-key",
    model="gpt-3.5-turbo",
    extra={
        "timeout": 60,  # Increase from default 30s
        "max_retries": 5  # Increase retries
    }
)
```

---

### Problem 17: Rate limiting errors

**✅ Solution:**

```python
# 1. Add delays between requests
import asyncio
await asyncio.sleep(1)  # 1 second delay

# 2. Use batch processing (SDK)
# Instead of sequential calls, batch them

# 3. Reduce request frequency
# - Cache responses
# - Combine multiple questions
# - Use cheaper providers for testing
```

---

## 🔑 Configuration Issues

### Problem 18: Environment variables not working

**✅ Solution:**

```bash
# Windows PowerShell - Must use $env:
$env:DEEPSEEK_API_KEY="sk-your-key"  # ✅ Correct
DEEPSEEK_API_KEY="sk-your-key"       # ❌ Wrong

# Linux/Mac - Use export
export DEEPSEEK_API_KEY="sk-your-key"  # ✅ Correct
DEEPSEEK_API_KEY="sk-your-key"         # ❌ Wrong (only for current command)

# Verify it's set
# Windows:
echo $env:DEEPSEEK_API_KEY

# Linux/Mac:
echo $DEEPSEEK_API_KEY
```

**Persistent configuration:**

```bash
# Windows: Add to PowerShell profile
# Linux/Mac: Add to ~/.bashrc or ~/.zshrc
export DEEPSEEK_API_KEY="sk-your-key"
```

---

## 🐛 Still Having Problems?

### Step 1: Run Verification Script

```bash
python verify_installation.py
```

This will tell you exactly what's wrong.

### Step 2: Check Documentation

1. [INSTALLATION_GUIDE.md](https://github.com/luminoracore/luminoracore/blob/main/INSTALLATION_GUIDE.md) - Complete installation guide
2. [INSTALLATION_VERIFICATION.md](https://github.com/luminoracore/luminoracore/blob/main/INSTALLATION_VERIFICATION.md) - Verification details
3. [FAQ](FAQ) - Common questions

### Step 3: Clean Reinstall

If all else fails, do a clean reinstall:

```bash
# 1. Deactivate and delete virtual environment
deactivate
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# 2. Create new virtual environment
python -m venv venv

# 3. Activate
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/Mac

# 4. Clean install
.\install_all.ps1  # Windows
./install_all.sh   # Linux/Mac

# 5. Verify
python verify_installation.py
```

### Step 4: Report an Issue

If the problem persists:

1. **Gather information:**
   - OS and version
   - Python version (`python --version`)
   - Error message (full stack trace)
   - Steps to reproduce

2. **Create an issue:**
   - Go to: https://github.com/luminoracore/luminoracore/issues/new
   - Use template: "Bug report"
   - Include all gathered information

---

## 📊 Quick Diagnostic

Run this diagnostic script to check your setup:

```python
# diagnostic.py
import sys
import os

print("=" * 60)
print("LUMINORACORE DIAGNOSTIC")
print("=" * 60)

print(f"\n1. Python: {sys.version}")
print(f"   Executable: {sys.executable}")

print(f"\n2. Virtual environment:")
print(f"   Active: {bool(os.environ.get('VIRTUAL_ENV'))}")
if os.environ.get('VIRTUAL_ENV'):
    print(f"   Path: {os.environ['VIRTUAL_ENV']}")

print(f"\n3. Installed packages:")
try:
    import luminoracore
    print(f"   ✅ luminoracore: {getattr(luminoracore, '__version__', 'unknown')}")
except ImportError as e:
    print(f"   ❌ luminoracore: {e}")

try:
    import luminoracore_cli
    print(f"   ✅ luminoracore-cli: {getattr(luminoracore_cli, '__version__', 'unknown')}")
except ImportError as e:
    print(f"   ❌ luminoracore-cli: {e}")

try:
    import luminoracore_sdk
    print(f"   ✅ luminoracore-sdk: {getattr(luminoracore_sdk, '__version__', 'unknown')}")
except ImportError as e:
    print(f"   ❌ luminoracore-sdk: {e}")

print(f"\n4. API Keys:")
keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "DEEPSEEK_API_KEY", "MISTRAL_API_KEY"]
for key in keys:
    status = "✅ Set" if os.environ.get(key) else "⚪ Not set"
    print(f"   {status}: {key}")

print("\n" + "=" * 60)
```

Save as `diagnostic.py` and run:
```bash
python diagnostic.py
```

---

## 🆘 Emergency Support

### If Nothing Works

1. **Check system requirements:**
   - Python 3.8+ installed
   - pip working (`pip --version`)
   - Virtual environment activated

2. **Try manual step-by-step installation:**
   - Follow [INSTALLATION_GUIDE.md](https://github.com/luminoracore/luminoracore/blob/main/INSTALLATION_GUIDE.md) exactly
   - Don't skip steps
   - Verify each step works before continuing

3. **Check for conflicts:**
   - No other `luminoracore` installations
   - No conda environments active
   - No conflicting packages

4. **Ask for help:**
   - Create detailed issue on GitHub
   - Include diagnostic output
   - Include full error messages

---

## 📞 Get Help

- 🐛 **Report Bug**: [GitHub Issues](https://github.com/luminoracore/luminoracore/issues/new?template=bug_report.md)
- ❓ **Ask Question**: [GitHub Discussions](https://github.com/luminoracore/luminoracore/discussions) (if enabled)
- 📖 **Read Docs**: [Documentation Index](https://github.com/luminoracore/luminoracore/blob/main/DOCUMENTATION_INDEX.md)

---

_Last updated: October 2025 | LuminoraCore v1.0.0_

