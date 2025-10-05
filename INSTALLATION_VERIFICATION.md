# 🧪 Installation Verification Guide

**Version:** 1.0.0  
**Script:** `verificar_instalacion.py`  
**Updated:** October 2025

---

## 📌 What is this script?

`verificar_instalacion.py` is an **automatic diagnostic script** that verifies LuminoraCore is correctly installed and working.

---

## ✅ When to Use It

### Always use it AFTER:
1. ✅ **First installation** - To confirm everything works
2. ✅ **Updating components** - To verify compatibility
3. ✅ **Reinstalling** - To confirm everything was restored
4. ✅ **Changing virtual environment** - To validate the new environment
5. ✅ **Adding providers** - To confirm they're available
6. ✅ **Configuring API keys** - To see which ones are active
7. ✅ **Before reporting an error** - To have diagnostic information

### Also use it IF:
- ❓ You're not sure if something is installed
- ❓ Something doesn't work and you don't know why
- ❓ You want to see what providers you have available
- ❓ You need to verify your API keys without showing them

---

## 📥 How to Get the Script

### Option 1: Clone from GitHub

```bash
# If you cloned the complete repository, you already have it:
cd LuminoraCoreBase
ls verificar_instalacion.py   # Should exist
```

### Option 2: Download Directly

```bash
# Download from GitHub (update URL with your actual repository)
curl -O https://raw.githubusercontent.com/your-user/luminoracore/main/verificar_instalacion.py

# Or with wget:
wget https://raw.githubusercontent.com/your-user/luminoracore/main/verificar_instalacion.py
```

### Option 3: Copy Manually

If you have access to the source code, copy the file from:
```
LuminoraCoreBase/verificar_instalacion.py
```

---

## 🚀 How to Use It

### Step 1: Make sure your virtual environment is active

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### Step 2: Run the script

```bash
python verificar_instalacion.py
```

### Step 3: Review the output

The script will print a detailed report with 6 sections.

---

## 📊 What the Script Verifies

### 1. Virtual Environment

```
✅ Virtual environment activated
   Python: 3.11.0
   Path: /path/to/your/venv/bin/python
```

Or:

```
⚠️  WARNING: Not in a virtual environment
   Recommendation: Activate your venv before continuing
```

**What does it mean?**
- ✅ Green = You're working in an isolated environment (correct)
- ⚠️ Yellow = You're using system Python (not recommended)

---

### 2. Base Engine (luminoracore)

```
1. BASE ENGINE (luminoracore)
----------------------------------------------------------------------
✅ Installed correctly (v1.0.0)
   - Personality: OK
   - PersonalityValidator: OK
   - PersonalityCompiler: OK
   - LLMProvider: OK
```

Or:

```
❌ ERROR: No module named 'luminoracore'
   Solution: cd luminoracore && pip install -e .
```

**What does it mean?**
- ✅ Green = Base engine is installed and functional
- ❌ Red = Need to install base engine

---

### 3. CLI (luminoracore-cli)

```
2. CLI (luminoracore-cli)
----------------------------------------------------------------------
✅ Installed correctly (v1.0.0)
   - Command 'luminoracore': OK
```

Or:

```
❌ ERROR: No module named 'luminoracore_cli'
   Solution: cd luminoracore-cli && pip install -e .
```

**What does it mean?**
- ✅ Green = CLI is installed and command is available
- ❌ Red = Need to install CLI
- ⚠️ Yellow = Package installed but command not found (reinstall)

---

### 4. SDK (luminoracore-sdk-python)

```
3. SDK (luminoracore-sdk-python)
----------------------------------------------------------------------
✅ Installed correctly
   - LuminoraCoreClient: OK
   - ProviderConfig: OK
   - StorageConfig: OK
```

Or:

```
❌ ERROR: cannot import name 'LuminoraCoreClient'
   Solution: cd luminoracore-sdk-python && pip install -e '.[openai]'
```

**What does it mean?**
- ✅ Green = SDK is installed and functional
- ❌ Red = Need to install SDK

---

### 5. Available Providers

```
4. AVAILABLE PROVIDERS
----------------------------------------------------------------------
  ✅ Openai       - OpenAIProvider
  ✅ Anthropic    - AnthropicProvider
  ✅ Deepseek     - DeepSeekProvider
  ✅ Mistral      - MistralProvider
  ✅ Cohere       - CohereProvider
  ✅ Google       - GoogleProvider
  ✅ Llama        - LlamaProvider

✅ All providers (7) available
```

Or:

```
  ✅ Openai       - OpenAIProvider
  ❌ Anthropic    - ERROR: No module named 'anthropic'
  ...
  
⚠️  2 provider(s) with problems
```

**What does it mean?**
- ✅ Green = Provider available and functional
- ❌ Red = Need to install provider dependency

**How to fix it:**
```bash
# Install specific provider
pip install -e ".[anthropic]"

# Or all
pip install -e ".[all]"
```

---

### 6. Optional Dependencies

```
5. OPTIONAL DEPENDENCIES
----------------------------------------------------------------------
  ✅ openai       - OpenAI API
  ⚪ anthropic    - Anthropic Claude API (not installed)
  ⚪ redis        - Redis storage (not installed)
  ⚪ asyncpg      - PostgreSQL storage (not installed)
  ⚪ motor        - MongoDB storage (not installed)
```

**What does it mean?**
- ✅ Green = Dependency installed
- ⚪ White = Optional dependency not installed (not an error)

**These are optional**, only install them if you need them:
```bash
# Only if you need Redis
pip install redis

# Only if you need PostgreSQL
pip install asyncpg

# Only if you need MongoDB
pip install motor
```

---

### 7. Configured API Keys

```
6. CONFIGURATION
----------------------------------------------------------------------
  ✅ OPENAI_API_KEY
  ⚪ ANTHROPIC_API_KEY (not configured)
  ⚪ DEEPSEEK_API_KEY (not configured)
  ⚪ MISTRAL_API_KEY (not configured)
  ⚪ COHERE_API_KEY (not configured)
  ⚪ GOOGLE_API_KEY (not configured)

✅ 1 API key(s) configured
```

**What does it mean?**
- ✅ Green = API key configured in environment variable
- ⚪ White = API key not configured (only configure the ones you need)

**The script DOES NOT show the value** of your API keys (for security), only if they exist.

---

## 📋 Final Summary

### If everything is OK:

```
==================================================================
SUMMARY
==================================================================
🎉 INSTALLATION COMPLETE AND CORRECT

All main components installed:
  ✅ Base Engine (luminoracore)
  ✅ CLI (luminoracore-cli)
  ✅ SDK (luminoracore-sdk)

Next steps:
  1. Configure your API keys (environment variables)
  2. Read: QUICK_START.md
  3. Test: luminoracore --help
  4. Run examples: python ejemplo_quick_start_core.py
==================================================================
```

**Exit code:** `0` (success)

---

### If there are problems:

```
==================================================================
SUMMARY
==================================================================
⚠️  SOME COMPONENTS MISSING

Problems found:
  ❌ Base Engine not installed
  ❌ SDK not installed

Check: INSTALLATION_GUIDE.md section 'Troubleshooting'
==================================================================
```

**Exit code:** `1` (error)

---

## 🐛 Common Troubleshooting

### Problem 1: "python: command not found"

**Solution:**
```bash
# Use python3 instead of python
python3 verificar_instalacion.py
```

---

### Problem 2: "Permission denied"

**Solution:**
```bash
# Give execution permissions (Linux/Mac)
chmod +x verificar_instalacion.py
python verificar_instalacion.py
```

---

### Problem 3: "ModuleNotFoundError: No module named 'luminoracore'"

**Solution:**
1. Make sure virtual environment is active
2. Install components:
```bash
cd luminoracore
pip install -e .
```

---

### Problem 4: "All providers failing"

**Solution:**
```bash
# Reinstall SDK with all providers
cd luminoracore-sdk-python
pip install -e ".[all]"
```

---

### Problem 5: Script doesn't print correctly on Windows

The script includes a fix for Windows, but if you see strange characters:

```bash
# Use PowerShell with UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
python verificar_instalacion.py
```

---

## 📖 Interpreting the Results

### Result: All Green ✅

```
✅ Base Engine: OK
✅ CLI: OK
✅ SDK: OK
✅ 7 Providers available
```

**Action:** Perfect! You can start using LuminoraCore.

---

### Result: Some Components Missing ⚠️

```
✅ Base Engine: OK
❌ CLI: NOT INSTALLED
✅ SDK: OK
```

**Action:** Install missing components according to script instructions.

---

### Result: Providers with Problems ❌

```
✅ OpenAI: OK
❌ Anthropic: ERROR
✅ DeepSeek: OK
```

**Action:** 
```bash
# Install missing provider
cd luminoracore-sdk-python
pip install -e ".[anthropic]"

# Verify again
python verificar_instalacion.py
```

---

### Result: No API Keys ⚪

```
⚪ OPENAI_API_KEY (not configured)
⚪ ANTHROPIC_API_KEY (not configured)
```

**Action:**
```bash
# Configure the API key you need (example: OpenAI)
# Windows
$env:OPENAI_API_KEY="sk-your-api-key"

# Linux/Mac
export OPENAI_API_KEY="sk-your-api-key"

# Verify again
python verificar_instalacion.py
```

---

## 🔄 When to Re-run It

### Always when:
1. ✅ You install or update components
2. ✅ You add a new provider
3. ✅ You configure a new API key
4. ✅ You change virtual environment
5. ✅ Something stops working

### It's your "Doctor" for LuminoraCore:
- 🩺 **Complete diagnosis** in seconds
- 🔍 **Detects problems** automatically
- 💡 **Suggests solutions** specific to your issue
- ✅ **Confirms** everything works

---

## 📝 Real Use Cases

### Case 1: First Installation

```bash
# 1. Clone and install
git clone https://github.com/your-user/luminoracore.git
cd luminoracore
./instalar_todo.sh

# 2. Verify
python verificar_instalacion.py

# ✅ Result: Everything installed correctly
```

---

### Case 2: Add a New Provider

```bash
# Before installing
python verificar_instalacion.py
# ❌ Anthropic Provider: ERROR

# Install
pip install -e ".[anthropic]"

# After installing
python verificar_instalacion.py
# ✅ Anthropic Provider: OK
```

---

### Case 3: Configure API Keys

```bash
# Before configuring
python verificar_instalacion.py
# ⚪ OPENAI_API_KEY (not configured)

# Configure
export OPENAI_API_KEY="sk-..."

# After configuring
python verificar_instalacion.py
# ✅ OPENAI_API_KEY configured
```

---

### Case 4: Report an Error

Before reporting an error on GitHub or asking for help:

```bash
# 1. Run the script
python verificar_instalacion.py > diagnostico.txt

# 2. Attach diagnostico.txt to your report
```

This helps developers understand your configuration.

---

## 🎯 Quick Summary

| When | Command | Purpose |
|------|---------|---------|
| **After installing** | `python verificar_instalacion.py` | Confirm installation |
| **Something doesn't work** | `python verificar_instalacion.py` | Diagnose problem |
| **Add provider** | `python verificar_instalacion.py` | Verify availability |
| **Configure API key** | `python verificar_instalacion.py` | Confirm configuration |
| **Report error** | `python verificar_instalacion.py > diag.txt` | Generate diagnostics |

---

## ✅ Manual Verification Checklist

If you prefer to verify manually:

```bash
# 1. Base Engine
python -c "import luminoracore; print(luminoracore.__version__)"

# 2. CLI
luminoracore --version

# 3. SDK
python -c "from luminoracore import LuminoraCoreClient; print('OK')"

# 4. Provider (example: OpenAI)
python -c "from luminoracore.providers import OpenAIProvider; print('OK')"

# 5. API Key
echo $OPENAI_API_KEY  # Linux/Mac
echo $env:OPENAI_API_KEY  # Windows
```

---

## 📚 References

- **Main documentation:** [INSTALLATION_GUIDE.md](./INSTALLATION_GUIDE.md)
- **Troubleshooting:** [INSTALLATION_GUIDE.md#troubleshooting](./INSTALLATION_GUIDE.md)
- **Quick start:** [QUICK_START.md](./QUICK_START.md)
- **Source script:** `verificar_instalacion.py`

---

**🎓 PRO TIP:**  
Run `python verificar_instalacion.py` after each major change to your environment. It's fast, comprehensive, and saves debugging time!

