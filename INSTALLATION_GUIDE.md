# 📘 Complete Installation and Usage Guide - LuminoraCore

This guide will take you step-by-step from zero to using LuminoraCore in your local project.

## ⚠️ Important Clarification About Storage

**Common question:** "Do I need my own database?"

**Answer:** NOT necessarily. LuminoraCore offers MULTIPLE options:

```
┌──────────────────────────────────────────────────┐
│  🎯 OPTION 1: No Database (Default)              │
├──────────────────────────────────────────────────┤
│  • Storage: In RAM memory                        │
│  • Persistent: NO (lost when closed)             │
│  • Installation: 0 steps                         │
│  • Ideal for: Tests, demos                       │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  💾 OPTION 2: JSON File (Simple)  ✨ NEW         │
├──────────────────────────────────────────────────┤
│  • Storage: .json or .json.gz file               │
│  • Persistent: YES (file on disk)                │
│  • Installation: 0 steps                         │
│  • Ideal for: Personal bots, backups             │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  📱 OPTION 3: SQLite (Mobile)  ✨ NEW            │
├──────────────────────────────────────────────────┤
│  • Storage: .db file (SQLite)                    │
│  • Persistent: YES (perfect for mobile)          │
│  • Installation: 0 steps                         │
│  • Ideal for: iOS/Android apps, desktop          │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  🚀 OPTION 4+: With Database (Optional)          │
├──────────────────────────────────────────────────┤
│  • Storage: Redis/PostgreSQL/MongoDB             │
│  • Persistent: YES                               │
│  • Installation: Requires DB server              │
│  • Ideal for: Web production, high scale         │
└──────────────────────────────────────────────────┘
```

**👉 To start, you don't need anything. Everything works in memory.**

**👉 For mobile apps use SQLite (included, no additional installation).**

**👉 For simple persistence use JSON (no DB server).**

Full details in: [Conversation Storage Section](#-conversation-storage)

---

## 🏗️ Project Architecture

LuminoraCore is composed of **3 main components**:

```
┌──────────────────────────────────────────────────────┐
│  1. luminoracore (Base Engine / Core Engine)         │
│     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│     • Personality management                         │
│     • Validation and compilation                     │
│     • PersonaBlend™ Technology                       │
│     • NO interface (it's a library)                  │
└──────────────────┬───────────────────────────────────┘
                   │
                   │ BOTH USE THE BASE ENGINE
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌───────────────┐    ┌─────────────────────────┐
│  2. CLI       │    │  3. SDK                 │
│  (Terminal)   │    │  (Python Apps)          │
│───────────────│    │─────────────────────────│
│ • Commands    │    │ • Client API            │
│ • Wizard      │    │ • Sessions              │
│ • Testing     │    │ • Real LLM calls        │
│ • Server      │    │ • Multi-provider        │
│               │    │                         │
│ DEPENDS ON:   │    │ DEPENDS ON:             │
│ luminoracore  │    │ luminoracore            │
└───────────────┘    └─────────────────────────┘
```

**⚠️ IMPORTANT - Installation Order:**

```
1. FIRST: luminoracore (base engine)
           ↓
2. AFTER: luminoracore-cli (uses the engine)
           ↓
3. AFTER: luminoracore-sdk (uses the engine)
```

**Why this order?**
- The **CLI** imports `from luminoracore import Personality, PersonalityCompiler`
- The **SDK** imports `from luminoracore import Personality, PersonalityBlender`
- If you install CLI or SDK **without** the base engine, you'll get `ModuleNotFoundError`

**Technical dependencies:**
```python
# luminoracore-cli/setup.py
install_requires=[
    'luminoracore>=0.1.0',  # ← Requires base engine
    'click>=8.0.0',
    ...
]

# luminoracore-sdk-python/setup.py
install_requires=[
    'luminoracore>=0.1.0',  # ← Requires base engine
    'aiohttp>=3.8.0',
    ...
]
```

---

## 🤔 What is Each Component?

### 1️⃣ **luminoracore** (Base Engine)

**It is:** A Python library (no interface)

**Does:**
- Loads personality JSON files
- Validates that JSON is correct
- Compiles personalities for different LLMs
- Blends personalities (PersonaBlend)

**Does NOT:**
- ❌ NO terminal commands
- ❌ NO API calls to LLM
- ❌ NO graphical interface
- ❌ NO session management

**Typical usage:**
```python
# In your Python code
from luminoracore import Personality, PersonalityCompiler

personality = Personality("dr_luna.json")
compiler = PersonalityCompiler()
result = compiler.compile(personality, "openai")
```

**Analogy:** It's like a car's "engine". It works, but you need the rest of the car to drive.

---

### 2️⃣ **luminoracore-cli** (Terminal Tool)

**It is:** A command-line tool that **USES** the base engine

**Does:**
- ✅ Execute commands from terminal
- ✅ Validate files: `luminoracore validate file.json`
- ✅ Compile: `luminoracore compile file.json`
- ✅ Create personalities: `luminoracore create --interactive`
- ✅ List: `luminoracore list`
- ✅ Basic testing

**Internally:**
```python
# Inside luminoracore-cli
from luminoracore import Personality, PersonalityCompiler  # ← USES THE ENGINE

def validate_command(file_path):
    personality = Personality(file_path)  # ← Uses base engine
    # ... rest of code
```

**Analogy:** It's like the car's "steering wheel and pedals". It lets you USE the engine from the terminal.

---

### 3️⃣ **luminoracore-sdk** (SDK for Apps)

**It is:** A complete client for building applications that **USES** the base engine

**Does:**
- ✅ Manage conversation sessions
- ✅ Make REAL API calls to LLMs (OpenAI, DeepSeek, etc.)
- ✅ Store conversation history
- ✅ Manage session memory
- ✅ Analytics and metrics

**Internally:**
```python
# Inside luminoracore-sdk
from luminoracore import Personality, PersonalityCompiler  # ← USES THE ENGINE

class LuminoraCoreClient:
    async def create_session(self, personality_name, provider_config):
        personality = Personality(f"{personality_name}.json")  # ← Uses base engine
        # ... rest of code for sessions, LLM calls, etc.
```

**Analogy:** It's like a "complete car with GPS and audio". It has the engine + everything needed for a complete app.

---

## 📊 Comparison Table

| Feature | Base Engine | CLI | SDK |
|---------|------------|-----|-----|
| **Load personalities** | ✅ | ✅ (uses engine) | ✅ (uses engine) |
| **Validate JSON** | ✅ | ✅ (uses engine) | ✅ (uses engine) |
| **Compile prompts** | ✅ | ✅ (uses engine) | ✅ (uses engine) |
| **Terminal commands** | ❌ | ✅ | ❌ |
| **LLM calls** | ❌ | ❌ | ✅ |
| **Session management** | ❌ | ❌ | ✅ |
| **Python interface** | ✅ | ❌ | ✅ |
| **Interactive wizard** | ❌ | ✅ | ❌ |

---

## 🎯 Answer to Your Question

**Your question:** 
> "Does CLI need to have luminoracore compiled or compile luminoracore like the SDK?"

**Answer:**

**YES, exactly.** The CLI:

1. ✅ **Needs you to install `luminoracore` first** (the base engine)
2. ✅ **Imports and uses the base engine internally**
3. ✅ **Won't work if you don't have the base engine installed**

**The same applies to the SDK:**
- Also needs base engine installed
- Also imports `from luminoracore import ...`

**Correct installation order:**
```bash
# 1. FIRST the engine (required)
cd luminoracore
pip install -e .

# 2. THEN the CLI (optional - only if you want terminal commands)
cd ../luminoracore-cli
pip install -e .

# 3. THEN the SDK (optional - only if you're building apps)
cd ../luminoracore-sdk-python
pip install ".[all]"  # Normal installation (recommended)
# Or for development: pip install -e ".[all]" (may fail on Windows)
```

**If you try to install CLI without the engine:**
```bash
cd luminoracore-cli
pip install -e .

# ❌ ERROR when executing commands:
luminoracore validate file.json
# ModuleNotFoundError: No module named 'luminoracore'
```

---

## 📋 Prerequisites

Before starting, make sure you have:

- ✅ **Python 3.8 or higher** installed
- ✅ **pip** (Python package manager)
- ✅ **git** (to clone repository)
- ✅ A code editor (VS Code, PyCharm, etc.)
- ✅ Terminal or command console

### Verify installed versions:

```bash
python --version
# Should show: Python 3.8.x or higher

pip --version
# Should show: pip x.x.x

git --version
# Should show: git version x.x.x
```

---

## 🚀 Option 1: Development Mode Installation (Recommended)

This option lets you edit source code and see changes immediately.

### Step 1: Clone or locate the repository

If you already have the project downloaded, navigate to its folder:

```bash
cd luminoracore
```

If you don't have it, clone it first:

```bash
git clone https://github.com/your-user/luminoracore.git
cd luminoracore
```

### Step 2: Create a virtual environment (Recommended)

This isolates project dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows PowerShell
.\venv\Scripts\Activate.ps1

# Activate on Windows CMD
.\venv\Scripts\activate.bat

# Activate on Linux/Mac
source venv/bin/activate
```

When activated, you'll see `(venv)` at the start of your command line.

### Step 3: Install Base Engine (luminoracore)

⚠️ **IMPORTANT: Verify you're in the right place**

```
luminoracore/                     ← Cloned repo
└── luminoracore/                 ← ⭐ YOU SHOULD BE HERE
    ├── setup.py                  ← ✅ This file MUST exist
    ├── pyproject.toml
    ├── venv/                     ← Your virtual environment
    └── luminoracore/             ← ❌ DON'T enter here (source code)
```

This is the fundamental component that all others need.

#### 🪟 WINDOWS (Normal Installation - Recommended)

```powershell
# Navigate to base engine folder
cd luminoracore

# ⚠️ VISUAL VERIFICATION:
dir     # MUST show setup.py

# ❌ If you DON'T see setup.py: cd .. and try again

# ✅ WINDOWS: Install in NORMAL mode (DON'T use -e)
pip install .

# ✅ SUCCESS IF YOU SEE: "Successfully installed luminoracore-X.X.X"

# Return to root
cd ..
```

**🚨 IMPORTANT FOR WINDOWS:**  
On Windows, the Base Engine must be installed in **normal mode** (`pip install .`) instead of editable (`pip install -e .`) due to issues with pip's editable finder. CLI and SDK can be installed in editable mode without problems.

#### 🐧 LINUX / MAC (Editable Installation)

```bash
# Navigate to base engine folder
cd luminoracore

# ⚠️ VISUAL VERIFICATION:
ls      # MUST show setup.py

# ❌ If you DON'T see setup.py: cd .. and try again

# ✅ LINUX/MAC: Install in editable mode
pip install -e .

# ✅ SUCCESS IF YOU SEE: "Successfully installed luminoracore-X.X.X"

# Optional: Install development dependencies
pip install -e ".[dev]"

# Return to root
cd ..
```

**What does `-e` do?** 
- Installs in "editable" mode
- Code changes reflect immediately
- You don't need to reinstall after each modification

**💡 Note:** If you need to modify Base Engine code on Windows, after making changes run `pip install --force-reinstall --no-deps .` to update it.

### Step 4: Install CLI (luminoracore-cli)

```bash
# Navigate to CLI folder
cd luminoracore-cli

# Install in development mode
pip install -e .

# Optional: Extra dependencies for server
pip install -e ".[server]"

# Return to root
cd ..
```

### Step 5: Install SDK (luminoracore-sdk-python)

```bash
# Navigate to SDK folder
cd luminoracore-sdk-python

# ⚠️ IMPORTANT: On Windows, editable mode (-e) can cause problems
# Recommended: Normal installation
pip install ".[all]"

# Alternative (only if you need to modify code):
# pip install -e ".[all]"  # NOTE: May fail on Windows

# Optional: Only specific providers
pip install ".[openai]"      # Only OpenAI
pip install ".[anthropic]"   # Only Anthropic
pip install ".[deepseek]"    # Only DeepSeek (economical)
pip install ".[mistral]"     # Only Mistral AI
pip install ".[llama]"       # Only Llama (via Replicate)
pip install ".[cohere]"      # Only Cohere
pip install ".[google]"      # Only Google Gemini

# Return to root
cd ..
```

### Step 6: Verify installation

#### ✅ Option 1: Automatic Script (Recommended)

**Download the script:**
```bash
# If you're in the cloned repository, download the script:
curl -O https://raw.githubusercontent.com/your-user/luminoracore/main/verificar_instalacion.py

# Or copy manually from repository
```

**Run verification:**
```bash
python verificar_instalacion.py
```

**Expected output:**
```
==================================================================
INSTALLATION VERIFICATION - LUMINORACORE
==================================================================

✅ Virtual environment activated
   Python: 3.11.0
   Path: /path/to/your/venv/bin/python

1. BASE ENGINE (luminoracore)
----------------------------------------------------------------------
✅ Installed correctly (v1.0.0)
   - Personality: OK
   - PersonalityValidator: OK
   - PersonalityCompiler: OK
   - LLMProvider: OK

2. CLI (luminoracore-cli)
----------------------------------------------------------------------
✅ Installed correctly (v1.0.0)
   - Command 'luminoracore': OK

3. SDK (luminoracore-sdk-python)
----------------------------------------------------------------------
✅ Installed correctly
   - LuminoraCoreClient: OK
   - ProviderConfig: OK
   - StorageConfig: OK

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

5. OPTIONAL DEPENDENCIES
----------------------------------------------------------------------
  ✅ openai       - OpenAI API
  ⚪ anthropic    - Anthropic Claude API (not installed)
  ⚪ redis        - Redis storage (not installed)
  ⚪ asyncpg      - PostgreSQL storage (not installed)
  ⚪ motor        - MongoDB storage (not installed)

6. CONFIGURATION
----------------------------------------------------------------------
  ✅ OPENAI_API_KEY
  ⚪ ANTHROPIC_API_KEY (not configured)
  ⚪ DEEPSEEK_API_KEY (not configured)
  ⚪ MISTRAL_API_KEY (not configured)
  ⚪ COHERE_API_KEY (not configured)
  ⚪ GOOGLE_API_KEY (not configured)

✅ 1 API key(s) configured

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

**This script automatically verifies:**
- ✅ Which components are installed (Engine, CLI, SDK)
- ✅ Which providers are available (7 total)
- ✅ Which API keys are configured
- ✅ If virtual environment is active
- ❌ What's missing to install or configure

**Expected output if everything is OK:**
```
🎉 INSTALLATION COMPLETE AND CORRECT

All main components installed:
  ✅ Base Engine (luminoracore)
  ✅ CLI (luminoracore-cli)
  ✅ SDK (luminoracore-sdk)
```

#### Option 2: Manual Verification

```bash
# Verify luminoracore is installed
python -c "import luminoracore; print(luminoracore.__version__)"

# Verify CLI is available
luminoracore --help

# You can also use the short alias
lc --help

# Verify SDK
python -c "from luminoracore import LuminoraCoreClient; print('SDK OK')"
```

---

## 🎯 Option 2: Installation from PyPI (When Published)

When packages are published to PyPI, installation will be simpler:

```bash
# Base engine
pip install luminoracore

# CLI
pip install luminoracore-cli

# SDK with all providers
pip install luminoracore-sdk[all]
```

---

## 📝 Practical Usage - Case 1: Using Base Engine (luminoracore)

### Example 1: Load and Validate a Personality

Create a file `my_example_core.py`:

```python
from luminoracore import Personality, PersonalityValidator, PersonalityCompiler, LLMProvider

# 1. Load a personality
print("1. Loading personality...")
personality = Personality("luminoracore/luminoracore/personalities/dr_luna.json")
print(f"✅ Personality loaded: {personality.persona.name}")

# 2. Validate personality
print("\n2. Validating personality...")
validator = PersonalityValidator()
result = validator.validate(personality)

if result.is_valid:
    print("✅ Validation successful")
    print(f"   - Warnings: {len(result.warnings)}")
    print(f"   - Suggestions: {len(result.suggestions)}")
else:
    print("❌ Validation failed:")
    for error in result.errors:
        print(f"   - {error}")

# 3. Compile for OpenAI
print("\n3. Compiling for OpenAI...")
compiler = PersonalityCompiler()
compiled = compiler.compile(personality, LLMProvider.OPENAI)
print(f"✅ Compiled successfully")
print(f"   - Estimated tokens: {compiled.token_estimate}")
print(f"   - Prompt (first 200 chars):\n{compiled.prompt[:200]}...")

# 4. Compile for other providers
print("\n4. Compiling for other providers...")
for provider in [LLMProvider.ANTHROPIC, LLMProvider.DEEPSEEK, LLMProvider.LLAMA, LLMProvider.MISTRAL]:
    result = compiler.compile(personality, provider)
    print(f"✅ {provider.value}: {result.token_estimate} tokens")
```

**Execute:**

```bash
python my_example_core.py
```

### Example 2: Blend Personalities (PersonaBlend)

```python
from luminoracore import Personality, PersonalityBlender

# Load two personalities
print("Loading personalities...")
dr_luna = Personality("luminoracore/luminoracore/personalities/dr_luna.json")
rocky = Personality("luminoracore/luminoracore/personalities/rocky_inspiration.json")

# Blend personalities
print("\nBlending personalities...")
blender = PersonalityBlender()
blended = blender.blend(
    personalities=[dr_luna, rocky],
    weights=[0.7, 0.3],
    strategy="weighted_average"
)

print(f"✅ Blended personality created: {blended.persona.name}")
print(f"   Description: {blended.persona.description}")
print(f"   Archetype: {blended.core_traits.archetype}")
```

---

## 🛠️ Practical Usage - Case 2: Using CLI (luminoracore-cli)

The CLI lets you manage personalities from the terminal.

### Basic Commands:

```bash
# 1. See all available personalities
luminoracore list

# With details
luminoracore list --detailed

# 2. Validate a personality
luminoracore validate "luminoracore/luminoracore/personalities/dr_luna.json"

# Validate all personalities in a folder
luminoracore validate luminoracore/luminoracore/personalities/ --strict

# 3. Compile a personality
luminoracore compile "luminoracore/luminoracore/personalities/dr_luna.json" --provider openai

# Save to file
luminoracore compile "luminoracore/luminoracore/personalities/rocky_inspiration.json" --provider anthropic --output rocky_prompt.txt

# 4. Create a new personality (interactive mode)
luminoracore create --interactive

# 5. Blend personalities
luminoracore blend "luminoracore/luminoracore/personalities/dr_luna.json:0.6" "luminoracore/luminoracore/personalities/rocky_inspiration.json:0.4" --output blend.json

# 6. Start development server with web interface
luminoracore serve

# On custom port
luminoracore serve --port 3000

# 7. Get personality information
luminoracore info "luminoracore/luminoracore/personalities/victoria_sterling.json"
```

### Practical Example: Complete Workflow

```bash
# Step 1: Create a new personality
luminoracore create --interactive

# Step 2: Validate it's correct
luminoracore validate my_new_personality.json

# Step 3: Test compilation for different providers
luminoracore compile my_new_personality.json --provider openai
luminoracore compile my_new_personality.json --provider anthropic

# Step 4: Start server for visual testing
luminoracore serve
# Open http://localhost:8000 in your browser
```

---

## 🐍 Practical Usage - Case 3: Using SDK (luminoracore-sdk)

The SDK is for building complete AI applications.

### Example 1: Basic Application with OpenAI

Create a file `my_sdk_app.py`:

```python
import asyncio
import os
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig
from luminoracore.types.session import StorageConfig

async def main():
    # 1. Create client configuration
    print("1. Initializing client...")
    
    # IMPORTANT: storage_type defines WHERE conversations are saved
    # - "memory": In RAM (lost when closed, perfect for tests)
    # - "redis": In Redis (persistent, requires Redis server)
    # - "postgres": In PostgreSQL (persistent, requires DB)
    # - "mongodb": In MongoDB (persistent, requires DB)
    
    client = LuminoraCoreClient(
        storage_config=StorageConfig(
            storage_type="memory"  # 👈 Default: RAM memory (NOT persistent)
        )
    )
    
    await client.initialize()
    print("✅ Client initialized")
    
    # 2. Configure LLM provider (OpenAI)
    print("\n2. Configuring OpenAI...")
    provider_config = ProviderConfig(
        name="openai",
        api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"),
        model="gpt-3.5-turbo",
        extra={
            "timeout": 30,
            "max_retries": 3
        }
    )
    print("✅ Provider configured")
    
    # 3. Create a custom personality
    print("\n3. Loading personality...")
    personality_data = {
        "name": "programming_assistant",
        "description": "An expert Python programming assistant",
        "system_prompt": "You are a Python programming expert. You explain concepts clearly and concisely. You always provide code examples when relevant.",
        "metadata": {
            "version": "1.0.0",
            "author": "My Company",
            "tags": ["programming", "python", "educational"]
        }
    }
    
    await client.load_personality("programming_assistant", personality_data)
    print("✅ Personality loaded")
    
    # 4. Create a session
    print("\n4. Creating session...")
    session_id = await client.create_session(
        personality_name="programming_assistant",
        provider_config=provider_config
    )
    print(f"✅ Session created: {session_id}")
    
    # 5. Send messages (THIS MAKES REAL API CALLS)
    print("\n5. Sending message to OpenAI...")
    
    # IMPORTANT: This will consume tokens from your OpenAI account
    try:
        response = await client.send_message(
            session_id=session_id,
            message="Can you explain what list comprehensions are in Python?"
        )
        
        print("✅ Response received:")
        print(f"   Content: {response.content[:200]}...")
        print(f"   Tokens: {response.usage}")
        
    except Exception as e:
        print(f"⚠️  Error calling API: {e}")
        print("   (Make sure you have a valid API key in OPENAI_API_KEY)")
    
    # 6. View conversation history
    print("\n6. Getting history...")
    messages = await client.get_conversation(session_id)
    print(f"✅ Conversation has {len(messages)} messages")
    
    # 7. Save custom information in session
    print("\n7. Saving user preferences...")
    # NOTE: This saves ADDITIONAL data about the user
    # (level, preferences, custom context)
    # Saved in the same storage as conversations
    await client.store_memory(
        session_id=session_id,
        key="experience_level",
        value="intermediate"
    )
    print("✅ Memory saved (will be lost when closed if using 'memory')")
    
    # 8. Cleanup
    print("\n8. Cleaning up...")
    await client.cleanup()
    print("✅ Cleanup completed")

# Execute
if __name__ == "__main__":
    asyncio.run(main())
```

**Execute:**

```bash
# Configure your API key
export OPENAI_API_KEY="sk-your-api-key-here"  # Linux/Mac
set OPENAI_API_KEY=sk-your-api-key-here       # Windows CMD
$env:OPENAI_API_KEY="sk-your-api-key-here"    # Windows PowerShell

# Execute
python my_sdk_app.py
```

### Example 2: Blend Personalities at Runtime

```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig

async def main():
    client = LuminoraCoreClient()
    await client.initialize()
    
    # Load two different personalities
    scientist_data = {
        "name": "scientist",
        "system_prompt": "You are a rigorous scientist who explains everything with evidence and data.",
        "metadata": {"version": "1.0.0"}
    }
    
    creative_data = {
        "name": "creative",
        "system_prompt": "You are a creative thinker who finds innovative solutions.",
        "metadata": {"version": "1.0.0"}
    }
    
    await client.load_personality("scientist", scientist_data)
    await client.load_personality("creative", creative_data)
    
    # Blend personalities (60% scientist, 40% creative)
    blended = await client.blend_personalities(
        personality_names=["scientist", "creative"],
        weights=[0.6, 0.4],
        blend_name="creative_scientist"
    )
    
    print(f"✅ Blended personality: {blended}")
    
    # Use blended personality
    provider_config = ProviderConfig(
        name="openai",
        api_key="your-api-key",
        model="gpt-3.5-turbo"
    )
    
    session_id = await client.create_session(
        personality_name="creative_scientist",
        provider_config=provider_config
    )
    
    print(f"✅ Session with blended personality: {session_id}")
    
    await client.cleanup()

asyncio.run(main())
```

---

## 💾 Conversation Storage

### Where are conversations saved?

**Short answer:** It depends on you. LuminoraCore offers 6 options:

| Storage | Persistent | Requires | When to use |
|---------|-----------|----------|-------------|
| **memory** | ❌ NO | Nothing | Tests, demos |
| **json** | ✅ YES | Only disk | Simple apps, backups |
| **sqlite** | ✅ YES | Only disk | Mobile apps, desktop |
| **redis** | ✅ YES | Redis server | Web production, high speed |
| **postgres** | ✅ YES | PostgreSQL | Production, relational data |
| **mongodb** | ✅ YES | MongoDB | Production, flexible data |

### Option 1: Memory (Default - No DB)

```python
from luminoracore import LuminoraCoreClient
from luminoracore.types.session import StorageConfig

client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="memory"  # 👈 In RAM
    )
)
```

**✅ Advantages:**
- Don't need to install anything
- Ideal for tests and development
- Very fast

**❌ Disadvantages:**
- Everything lost when app closes
- Not for production
- Doesn't share data between processes

**When to use:**
- Demos and prototypes
- Testing
- Single-execution scripts

---

### Option 2: JSON File (Simple and Portable) ✨ NEW

```python
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="json",
        json_file_path="./sessions/conversations.json"  # Or .json.gz compressed
    )
)
```

**✅ Advantages:**
- Persistent (file on disk)
- No need for DB server
- Portable (can move file)
- Easy backups
- Readable (can view JSON)
- Ideal for development

**❌ Disadvantages:**
- Slow with many sessions (>1000)
- Not suitable for multiple concurrent processes
- No complex queries

**When to use:**
- Desktop apps
- Personal bots
- Periodically executed scripts
- Prototyping without complications
- Backups and portability

**Example with compression:**
```python
# Saves compressed (saves space)
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="json",
        json_file_path="./sessions/conversations.json.gz",
        compress=True  # Compress with gzip
    )
)
```

---

### Option 3: SQLite (Perfect for Mobile) 📱 NEW

```python
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="sqlite",
        sqlite_path="./data/luminoracore.db"
    )
)
```

**✅ Advantages:**
- Persistent (.db file)
- **PERFECT for mobile apps** (iOS/Android)
- Fast SQL queries
- Lightweight (single file)
- No external server
- ACID transactions

**❌ Disadvantages:**
- Not suitable for high concurrency
- No horizontal scalability

**When to use:**
- **Mobile apps (iOS/Android)** ⭐
- Desktop apps
- Prototypes needing SQL
- Single-user apps

**Example for mobile:**
```python
# On Android/iOS
import os
from pathlib import Path

# Path in app storage
if platform.system() == "Android":
    db_path = Path("/data/data/com.yourapp/databases/luminoracore.db")
else:  # iOS
    db_path = Path.home() / "Documents" / "luminoracore.db"

client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="sqlite",
        sqlite_path=str(db_path)
    )
)
```

---

### Option 4: Redis (Recommended for web production)

```python
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="redis",
        redis_url="redis://localhost:6379",
        redis_db=0
    )
)
```

**✅ Advantages:**
- Persistent
- Very fast (in memory)
- Perfect for sessions
- Automatic TTL

**❌ Disadvantages:**
- Requires Redis server

**Redis installation:**
```bash
# Linux/Mac (with Homebrew)
brew install redis
redis-server

# Windows (with Docker)
docker run -d -p 6379:6379 redis

# Install Python client
pip install redis
```

**When to use:**
- Chatbots in production
- Apps with multiple users
- Need speed + persistence

---

### Option 5: PostgreSQL

```python
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="postgres",
        postgres_url="postgresql://user:password@localhost/luminoracore"
    )
)
```

**✅ Advantages:**
- Persistent
- Complex SQL queries
- Easy backups

**❌ Disadvantages:**
- Slower than Redis
- Requires PostgreSQL DB

**When to use:**
- Already have PostgreSQL
- Need SQL analysis
- Backups and auditing important

---

### Option 6: MongoDB

```python
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="mongodb",
        mongodb_url="mongodb://localhost:27017",
        mongodb_database="luminoracore"
    )
)
```

**✅ Advantages:**
- Persistent
- Flexible schema
- Good performance

**❌ Disadvantages:**
- Requires MongoDB server

**When to use:**
- Already have MongoDB
- Unstructured data
- Horizontal scalability

---

### What exactly is saved?

**In the chosen storage, these are saved:**

1. **Message history**
   ```python
   [
     {"role": "user", "content": "Hello"},
     {"role": "assistant", "content": "Hi!"}
   ]
   ```

2. **Session context**
   ```python
   {
     "session_id": "abc123",
     "personality_name": "dr_luna",
     "created_at": "2024-10-03T10:00:00Z"
   }
   ```

3. **Custom memory**
   ```python
   {
     "experience_level": "intermediate",
     "preferences": {"language": "en"},
     "context": {...}
   }
   ```

**NOT saved:**
- ❌ Personality JSON file (it's static)
- ❌ Your Python code (it's your application)
- ❌ API keys (in environment variables)

---

### Complete Example: No DB vs With Redis

#### Without DB (Memory):
```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.session import StorageConfig

async def main():
    # Option 1: Memory (lost when closed)
    client = LuminoraCoreClient(
        storage_config=StorageConfig(storage_type="memory")
    )
    
    await client.initialize()
    session_id = await client.create_session(...)
    await client.send_message(session_id, "Hello")
    
    # ⚠️ When app closes, everything is lost
    await client.cleanup()

asyncio.run(main())
```

#### With Redis (Persistent):
```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.session import StorageConfig

async def main():
    # Option 2: Redis (persistent)
    client = LuminoraCoreClient(
        storage_config=StorageConfig(
            storage_type="redis",
            redis_url="redis://localhost:6379"
        )
    )
    
    await client.initialize()
    
    # Can resume previous sessions
    existing_session_id = "session_from_yesterday"
    await client.send_message(existing_session_id, "Hello again")
    
    # ✅ When closed, data remains in Redis
    await client.cleanup()

asyncio.run(main())
```

---

### Quick Decision

**Testing?** → Use `memory` (no DB)

**Mobile app (iOS/Android)?** → Use `sqlite` ⭐ **RECOMMENDED**

**Simple desktop app?** → Use `json` or `sqlite`

**Personal bot or script?** → Use `json` (easy and portable)

**Web production with many users?** → Use `redis` (fast + persistent)

**Already have PostgreSQL?** → Use `postgres`

**Already have MongoDB?** → Use `mongodb`

---

## 🔑 API Key Configuration

### OpenAI

```bash
# Get your API key at: https://platform.openai.com/api-keys

# Linux/Mac
export OPENAI_API_KEY="sk-..."

# Windows PowerShell
$env:OPENAI_API_KEY="sk-..."

# Windows CMD
set OPENAI_API_KEY=sk-...
```

### Anthropic (Claude)

```bash
# Get your API key at: https://console.anthropic.com/

# Linux/Mac
export ANTHROPIC_API_KEY="sk-ant-..."

# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

### DeepSeek (Very Economical) 💰 ✨ NEW

```bash
# Get your API key at: https://platform.deepseek.com/
# 🌟 ULTRA CHEAP Model: ~$0.14 per 1M tokens
# Popular among developers for its price

# Linux/Mac
export DEEPSEEK_API_KEY="sk-..."

# Windows PowerShell
$env:DEEPSEEK_API_KEY="sk-..."

# Windows CMD
set DEEPSEEK_API_KEY=sk-...
```

**Why DeepSeek?**
- 💰 **Price:** ~20x cheaper than GPT-4
- ⚡ **Speed:** Fast responses
- 🎯 **Quality:** Competitive with GPT-3.5
- 🔥 **Popular:** Developer favorite

**SDK usage:**
```python
provider_config = ProviderConfig(
    name="deepseek",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    model="deepseek-chat"  # Most economical model
)
```

### Cohere

```bash
# Get your API key at: https://dashboard.cohere.ai/

export COHERE_API_KEY="..."
```

### Mistral AI

```bash
# Get your API key at: https://console.mistral.ai/

export MISTRAL_API_KEY="..."
```

### Google Gemini

```bash
# Get your API key at: https://makersuite.google.com/app/apikey

export GOOGLE_API_KEY="..."
```

### Llama (via Replicate)

```bash
# Get your API key at: https://replicate.com/account/api-tokens

export REPLICATE_API_KEY="..."
```

---

## 🔧 Advanced Provider Configuration

### 📍 Custom Provider URLs

**IMPORTANT:** All provider URLs are configurable in a central JSON file:

📁 **Location:** `luminoracore-sdk-python/luminoracore_sdk/config/provider_urls.json`

This file contains base URLs for all providers:

```json
{
  "providers": {
    "openai": {
      "base_url": "https://api.openai.com/v1",
      "default_model": "gpt-3.5-turbo"
    },
    "anthropic": {
      "base_url": "https://api.anthropic.com/v1",
      "default_model": "claude-3-sonnet-20240229"
    },
    "deepseek": {
      "base_url": "https://api.deepseek.com/v1",
      "default_model": "deepseek-chat"
    },
    "mistral": {
      "base_url": "https://api.mistral.ai/v1",
      "default_model": "mistral-tiny"
    }
  }
}
```

### ✨ Why is this important?

1. **URLs Change:** If a provider changes endpoint, just edit JSON file
2. **New Providers:** Easily add new LLMs without modifying code
3. **Proxies/Mirrors:** Use alternative URLs or proxies to access LLMs
4. **Self-hosted:** Connect to local model instances (Ollama, LocalAI, etc.)

### 🛠️ How to Customize URLs

#### Option 1: Edit configuration file

```json
// luminoracore-sdk-python/luminoracore_sdk/config/provider_urls.json
{
  "custom_providers": {
    "my-local-llm": {
      "name": "My Local LLM",
      "base_url": "http://localhost:8000/v1",
      "default_model": "local-model",
      "chat_endpoint": "/chat/completions"
    }
  }
}
```

#### Option 2: Override at runtime (Python)

```python
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig

# Create provider with custom URL
provider_config = ProviderConfig(
    name="openai",
    api_key="sk-...",
    base_url="https://my-proxy.com/openai/v1",  # Custom URL
    model="gpt-4"
)

client = LuminoraCoreClient(provider_config=provider_config)
```

### 📋 Available Providers

| Provider | Base URL | Default Model | Installation |
|----------|----------|--------------|--------------|
| **OpenAI** | `https://api.openai.com/v1` | `gpt-3.5-turbo` | `pip install ".[openai]"` |
| **Anthropic** | `https://api.anthropic.com/v1` | `claude-3-sonnet-20240229` | `pip install ".[anthropic]"` |
| **DeepSeek** 💰 | `https://api.deepseek.com/v1` | `deepseek-chat` | `pip install ".[deepseek]"` |
| **Mistral** | `https://api.mistral.ai/v1` | `mistral-tiny` | `pip install ".[mistral]"` |
| **Cohere** | `https://api.cohere.ai/v1` | `command` | `pip install ".[cohere]"` |
| **Google** | `https://generativelanguage.googleapis.com/v1` | `gemini-pro` | `pip install ".[google]"` |
| **Llama** | `https://api.replicate.com/v1` | `llama-2-7b-chat` | `pip install ".[llama]"` |

### 🎯 Use Cases

**1. Use Ollama locally:**
```python
provider_config = ProviderConfig(
    name="openai",  # OpenAI API compatible
    api_key="ollama",  # Dummy key
    base_url="http://localhost:11434/v1",
    model="llama2"
)
```

**2. Use Azure OpenAI:**
```python
provider_config = ProviderConfig(
    name="openai",
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    base_url="https://YOUR-RESOURCE.openai.azure.com",
    model="gpt-35-turbo"
)
```

**3. Use corporate proxy:**
```python
provider_config = ProviderConfig(
    name="openai",
    api_key="sk-...",
    base_url="https://proxy.company.com/openai/v1",
    model="gpt-4"
)
```

---

## 📂 Typical Project Structure

```
my-project/
├── venv/                          # Virtual environment
├── my_personalities/              # Your custom personalities
│   ├── sales_assistant.json
│   ├── tech_support.json
│   └── creative_marketing.json
├── config/
│   └── providers.yaml            # Provider configuration
├── src/
│   ├── main.py                   # Your main application
│   ├── handlers.py               # Business logic
│   └── utils.py                  # Utilities
├── tests/
│   └── test_personalities.py    # Tests
├── requirements.txt              # Dependencies
└── README.md                     # Documentation
```

**requirements.txt:**

```txt
# To use only base engine
luminoracore>=0.1.0

# To use CLI
luminoracore-cli>=1.0.0

# To use complete SDK with OpenAI
luminoracore-sdk[openai]>=1.0.0

# Or with all providers
luminoracore-sdk[all]>=1.0.0
```

---

## 🐛 Common Troubleshooting

### Problem 1: "neither 'setup.py' nor 'pyproject.toml' found"

**❌ Symptom:**
```
ERROR: file:///D:/luminoracore/luminoracore/luminoracore does not appear to be a Python project
```

**🔍 Cause:** You're in the wrong directory (too deep or too high)

**✅ Solution:**

```bash
# 1. Verify where you are
pwd      # Linux/Mac
cd       # Windows (without arguments shows current path)

# 2. Look for setup.py
ls | grep setup.py      # Linux/Mac
dir | findstr setup.py  # Windows

# 3. If you DON'T see setup.py:
# Option A: If you're too deep (ex: luminoracore/luminoracore/luminoracore/)
cd ..
cd ..
ls  # Verify you now see setup.py

# Option B: If you're too high (ex: only luminoracore/)
cd luminoracore
ls  # Verify you see setup.py

# 4. Now yes, install
pip install -e .
```

**📍 Correct place:**
```
D:\luminoracore\luminoracore\          ← HERE (with setup.py)
├── setup.py                            ← ✅ Must exist
├── pyproject.toml
├── venv/
└── luminoracore/                       ← Source code (DON'T enter)
```

### Problem 2: "ModuleNotFoundError: No module named 'luminoracore'"

**🔍 Cause:** Virtual environment not activated or incorrect installation

**✅ Solution:**

```bash
# Make sure you're in the correct virtual environment
.\venv\Scripts\Activate.ps1   # Windows
source venv/bin/activate      # Linux/Mac

# You should see (venv) at start of your prompt

# Reinstall package
cd luminoracore
pip install -e .
cd ..
```

### Problem 3: "Command 'luminoracore' not found"

**Solution:**

```bash
# Reinstall CLI
cd luminoracore-cli
pip install -e .
cd ..

# Verify it's in PATH
pip show luminoracore-cli
```

### Problem 4: "ImportError: cannot import name 'Personality' from 'luminoracore'" (Windows)

**🔍 Cause:** Base Engine was installed in editable mode (`-e`) on Windows, causing import system conflicts.

**✅ Solution:**

```powershell
# 1. Uninstall everything
pip uninstall luminoracore luminoracore-sdk -y

# 2. Reinstall Base Engine in NORMAL mode (without -e)
cd luminoracore
pip install .
cd ..

# 3. Reinstall SDK normally
cd luminoracore-sdk-python
pip install ".[all]"
cd ..

# 4. Verify
python -c "from luminoracore import Personality; print('OK')"
```

### Problem 5: Error importing SDK or providers

**Solution:**

```bash
# Install dependencies for provider you're using
cd luminoracore-sdk-python
pip install ".[openai]"  # For OpenAI
pip install ".[anthropic]"  # For Anthropic
pip install ".[deepseek]"  # For DeepSeek
pip install ".[all]"  # For all (recommended)
cd ..

# Note: If you see import errors, DON'T use -e (editable mode) on Windows
```

### Problem 6: "Permission denied" activating virtual environment on Windows

**Solution:**

```powershell
# Run this in PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem 7: Personalities not found

**Solution:**

```python
# Use correct absolute or relative paths
from pathlib import Path

# Get project path
PROJECT_ROOT = Path(__file__).parent
PERSONALITIES_DIR = PROJECT_ROOT / "luminoracore" / "luminoracore" / "personalities"

# Load personality
personality_path = PERSONALITIES_DIR / "Dr. Luna Científica Entusiasta.json"
personality = Personality(str(personality_path))
```

---

## 📚 Additional Resources

### Official Documentation

- **Base Engine:** `luminoracore/docs/`
- **CLI:** `luminoracore-cli/README.md`
- **SDK:** `luminoracore-sdk-python/docs/api_reference.md`

### Included Examples

```bash
# Base engine examples
python luminoracore/examples/basic_usage.py
python luminoracore/examples/blending_demo.py

# SDK examples
python luminoracore-sdk-python/examples/basic_usage.py
python luminoracore-sdk-python/examples/personality_blending.py
```

### Reference Files

- `ESTADO_ACTUAL_PROYECTO.md` - Project status
- `CARACTERISTICAS_TECNICAS_LUMINORACORE.md` - Technical features
- `CREATING_PERSONALITIES.md` - Guide to creating personalities

---

## ✅ Checklist for New Developers

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] `luminoracore` installed
- [ ] `luminoracore-cli` installed (if you need it)
- [ ] `luminoracore-sdk` installed (if you need it)
- [ ] API keys configured (if making real calls)
- [ ] First example executed successfully
- [ ] Documentation read

---

## 🎓 Next Steps

1. **Explore included personalities** in `luminoracore/luminoracore/personalities/`
2. **Read complete guide:** `CREATING_PERSONALITIES.md`
3. **Run examples** in `luminoracore/examples/`
4. **Create your first custom personality**
5. **Integrate LuminoraCore into your application**
6. **Share your personalities with the community**

---

## 💡 Recommended Use Cases

### Case 1: Customer Service Chatbot

```python
# Use SDK with friendly support personality
# Redis storage for persistence
# Metrics and analytics included
```

### Case 2: Educational Assistant

```python
# Use base engine to switch between personalities
# Rigorous professor for exams
# Friendly tutor for learning
```

### Case 3: Content Generator

```python
# Blend creative with analytical personalities
# Generate content with consistent brand voice
```

---

## 📞 Support

If you have problems or questions:

1. Review this complete guide
2. Check `ESTADO_ACTUAL_PROYECTO.md`
3. Review examples in `examples/`
4. Create an issue on the repository

---

**Ready! Now you have everything you need to start using LuminoraCore in your projects.** 🚀

