# ⚡ LuminoraCore CheatSheet

## 🚀 Quick Installation

```bash
# All-in-one
.\instalar_todo.ps1        # Windows
./instalar_todo.sh         # Linux/Mac

# Manual - Core only
cd luminoracore && pip install -e . && cd ..

# Manual - Core + CLI
cd luminoracore && pip install -e . && cd ..
cd luminoracore-cli && pip install -e . && cd ..

# Manual - Core + SDK
cd luminoracore && pip install -e . && cd ..
cd luminoracore-sdk-python && pip install -e ".[openai]" && cd ..
```

---

## ✅ Verification

```bash
python ejemplo_quick_start_core.py
python ejemplo_quick_start_cli.py
python ejemplo_quick_start_sdk.py
```

---

## 🧠 Base Engine (Python)

```python
# Basic imports
from luminoracore import (
    Personality,
    PersonalityValidator,
    PersonalityCompiler,
    PersonalityBlender,
    LLMProvider
)

# Load personality
p = Personality("file.json")

# Validate
validator = PersonalityValidator()
result = validator.validate(p)
print(result.is_valid)

# Compile
compiler = PersonalityCompiler()
compiled = compiler.compile(p, LLMProvider.OPENAI)
print(compiled.prompt)

# Blend
blender = PersonalityBlender()
blended = blender.blend([p1, p2], [0.6, 0.4])
```

---

## 🛠️ CLI

```bash
# Help
luminoracore --help

# List
luminoracore list
luminoracore list --detailed

# Validate
luminoracore validate file.json
luminoracore validate folder/ --strict

# Compile
luminoracore compile file.json --provider openai
luminoracore compile file.json --provider anthropic -o out.txt

# Create
luminoracore create --interactive
luminoracore create --name "My Bot" --archetype helper

# Blend
luminoracore blend file1.json:0.7 file2.json:0.3
luminoracore blend p1.json:0.5 p2.json:0.3 p3.json:0.2 -o mix.json

# Server
luminoracore serve
luminoracore serve --port 3000
```

---

## 🐍 SDK (Applications)

```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig
from luminoracore.types.session import StorageConfig

async def main():
    # Client
    client = LuminoraCoreClient(
        storage_config=StorageConfig(storage_type="memory")
    )
    await client.initialize()
    
    # Load personality
    await client.load_personality("name", {
        "name": "name",
        "system_prompt": "Your prompt here",
        "metadata": {"version": "1.0.0"}
    })
    
    # Provider
    config = ProviderConfig(
        name="openai",
        api_key="your-key",
        model="gpt-3.5-turbo"
    )
    
    # Session
    session_id = await client.create_session(
        personality_name="name",
        provider_config=config
    )
    
    # Message
    response = await client.send_message(
        session_id=session_id,
        message="Hello"
    )
    print(response.content)
    
    # Memory
    await client.store_memory(session_id, "key", "value")
    memory = await client.get_memory(session_id, "key")
    
    # Cleanup
    await client.cleanup()

asyncio.run(main())
```

---

## 🔑 API Keys

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-..."
$env:ANTHROPIC_API_KEY="sk-ant-..."
$env:COHERE_API_KEY="..."

# Linux/Mac
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export COHERE_API_KEY="..."
```

---

## 📦 Supported Providers

| Provider | Example Model | SDK Installation |
|----------|---------------|------------------|
| OpenAI | gpt-3.5-turbo, gpt-4 | `pip install -e ".[openai]"` |
| Anthropic | claude-3-sonnet | `pip install -e ".[anthropic]"` |
| Cohere | command | `pip install -e ".[cohere]"` |
| Google | gemini-pro | `pip install -e ".[google]"` |
| Mistral | mistral-large | Included |
| Llama | llama-2 | Included |

---

## 🎯 Decision Table

| I need | Use |
|--------|-----|
| Just validate files | **CLI** |
| Create personalities interactively | **CLI** |
| Blend personalities | **Core** or **CLI** |
| Compile prompts in Python | **Core** |
| Chatbot with real API | **SDK** |
| Web interface for testing | **CLI** `serve` |
| Production app | **SDK** |

---

## 🔧 Quick Problem Solving

```bash
# ModuleNotFoundError
.\venv\Scripts\Activate.ps1  # Activate venv
cd luminoracore && pip install -e . && cd ..

# Command not found (CLI)
cd luminoracore-cli && pip install -e . && cd ..

# Permission denied (Windows)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📂 Personality JSON Structure

```json
{
  "persona": {
    "name": "Name",
    "version": "1.0.0",
    "description": "Description",
    "author": "Author",
    "language": "en",
    "tags": ["tag1", "tag2"],
    "compatibility": ["openai", "anthropic"]
  },
  "core_traits": {
    "archetype": "helper",
    "temperament": "friendly",
    "primary_motivation": "help",
    "expertise_areas": ["area1"],
    "communication_style": "clear"
  },
  "linguistic_profile": {
    "tone": ["friendly"],
    "formality_level": "semi-formal",
    "syntax": "structured",
    "vocabulary": ["clear"],
    "fillers": [],
    "humor_style": "light"
  },
  "behavioral_rules": [
    "Rule 1",
    "Rule 2"
  ],
  "constraints": {
    "topics_to_avoid": ["topic"],
    "ethical_guidelines": ["guideline"],
    "prohibited_behaviors": ["behavior"]
  },
  "examples": {
    "sample_responses": [
      {
        "input": "Question",
        "output": "Answer"
      }
    ],
    "tone_examples": ["Example"],
    "boundary_examples": ["Boundary"]
  }
}
```

---

## 🔗 Quick Links

- **Start:** [QUICK_START.md](QUICK_START.md)
- **Complete Guide:** [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- **Reference:** [CREATING_PERSONALITIES.md](CREATING_PERSONALITIES.md)
- **Index:** [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)

---

## 🎨 Quick Examples

### Validate file
```bash
luminoracore validate my_file.json
```

### Create chatbot
```python
# See ejemplo_quick_start_sdk.py
```

### Web server
```bash
luminoracore serve
```

### Blend personalities
```bash
luminoracore blend p1.json:0.6 p2.json:0.4 -o mix.json
```

---

**Print or save this file for quick reference! 📄**

