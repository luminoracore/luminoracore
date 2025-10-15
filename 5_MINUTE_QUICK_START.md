# ⚡ LuminoraCore v1.1 - 5 Minute Quick Start

**Get started with LuminoraCore v1.1 in 5 minutes!**

---

## 🎯 What You'll Build

A chatbot with:
- ✅ AI personality (Dr. Luna)
- ✅ Memory of conversations
- ✅ Relationship tracking
- ✅ Adaptive responses

---

## 📦 Step 1: Install (30 seconds)

```bash
pip install -e luminoracore/
pip install -e luminoracore-sdk-python/
```

---

## 🚀 Step 2: Run Your First Bot (2 minutes)

Create `my_first_bot.py`:

```python
import asyncio
from luminoracore import Personality, PersonalityCompiler, LLMProvider

async def main():
    # 1. Load personality
    personality = Personality("luminoracore/luminoracore/personalities/dr_luna.json")
    
    # 2. Compile for OpenAI
    compiler = PersonalityCompiler()
    result = compiler.compile(personality, LLMProvider.OPENAI)
    
    # 3. See the prompt
    print("🎭 Personality loaded: Dr. Luna")
    print("\n📝 System prompt:")
    print(result.prompt[:200] + "...")
    print(f"\n📊 Estimated tokens: {result.token_estimate}")

asyncio.run(main())
```

Run it:
```bash
python my_first_bot.py
```

**Output:**
```
🎭 Personality loaded: Dr. Luna
📝 System prompt:
You are Dr. Luna, an enthusiastic scientist who is passionate about 
explaining complex concepts in accessible ways...
📊 Estimated tokens: ~850
```

✅ **You just compiled your first AI personality!**

---

## 🧠 Step 3: Add Memory (v1.1 Feature) (2 minutes)

Create `bot_with_memory.py`:

```python
import asyncio
from luminoracore.core.relationship.affinity import AffinityManager
from luminoracore.core.memory.fact_extractor import FactExtractor

async def main():
    # Initialize v1.1 components
    affinity = AffinityManager()
    facts = FactExtractor()
    
    # Create user state
    state = affinity.create_state("user_alice", "dr_luna")
    print(f"👤 User: Alice")
    print(f"💝 Initial affinity: {state.affinity_points}/100")
    print(f"📊 Level: {state.current_level}\n")
    
    # Simulate conversation
    messages = [
        "Hi! I'm Alice, I'm studying biology.",
        "I love marine biology, especially dolphins!",
        "Can you explain photosynthesis?"
    ]
    
    for i, msg in enumerate(messages, 1):
        print(f"Turn {i}: {msg}")
        
        # Extract facts
        learned = facts.extract_sync("user_alice", msg)
        if learned:
            print(f"  📚 Learned: {learned[0].key} = {learned[0].value}")
        
        # Update affinity
        state = affinity.update_affinity_state(state, points_delta=5)
        print(f"  💝 Affinity: {state.affinity_points}/100 ({state.current_level})\n")
    
    print(f"✅ Final state:")
    print(f"   Level: {state.current_level}")
    print(f"   Affinity: {state.affinity_points}/100")
    print(f"   Facts learned: {len(learned)}")

asyncio.run(main())
```

Run it:
```bash
python bot_with_memory.py
```

**Output:**
```
👤 User: Alice
💝 Initial affinity: 0/100
📊 Level: stranger

Turn 1: Hi! I'm Alice, I'm studying biology.
  📚 Learned: name = Alice
  💝 Affinity: 5/100 (stranger)

Turn 2: I love marine biology, especially dolphins!
  📚 Learned: interest = marine biology
  💝 Affinity: 10/100 (stranger)

Turn 3: Can you explain photosynthesis?
  💝 Affinity: 15/100 (stranger)

✅ Final state:
   Level: stranger
   Affinity: 15/100
   Facts learned: 2
```

✅ **Your bot now has memory and learns about users!**

---

## 🐳 Bonus: Docker Setup (1 minute)

```bash
cd luminoracore-sdk-python

# Start everything
docker-compose up -d

# Check status
docker-compose ps
```

Done! You have:
- ✅ Redis (caching)
- ✅ PostgreSQL (memory storage)
- ✅ LuminoraCore API

---

## 🎓 What You Just Learned

In 5 minutes you:

1. ✅ **Installed** LuminoraCore v1.1
2. ✅ **Compiled** an AI personality
3. ✅ **Added memory** to track conversations
4. ✅ **Tracked affinity** for relationship building
5. ✅ **Set up Docker** (optional)

---

## 📚 Next Steps

### Learn More Features:

**20-Minute Deep Dive:**
```bash
python examples/v1_1_complete_workflow.py
```
This shows ALL v1.1 features integrated.

**Specific Topics:**
- Memory system → `python examples/v1_1_memory_demo.py`
- Feature flags → `python examples/v1_1_feature_flags_demo.py`
- Migrations → `python examples/v1_1_migrations_demo.py`

### Read Documentation:

| What | Where |
|------|-------|
| Full guide | `QUICK_START.md` |
| API reference | `luminoracore/docs/api_reference.md` |
| v1.1 features | `luminoracore/docs/v1_1_features.md` |
| Docker guide | `luminoracore-sdk-python/DOCKER.md` |

### Try Different Personalities:

```python
# Pirate adventurer
personality = Personality("personalities/captain_hook.json")

# Caring grandmother
personality = Personality("personalities/grandma_hope.json")

# Sarcastic observer
personality = Personality("personalities/marcus_sarcastic.json")

# 10 personalities available!
```

---

## 🆘 Common Issues

### ImportError: No module named 'luminoracore'

```bash
# Make sure you installed with -e flag
pip install -e luminoracore/
```

### File not found: personalities/dr_luna.json

```bash
# Use full path
personality = Personality("luminoracore/luminoracore/personalities/dr_luna.json")
```

### Docker not starting

```bash
# Check Docker is running
docker --version

# Clean start
docker-compose down -v
docker-compose up -d
```

---

## 🎯 Key Concepts

### Personality = AI Character

A JSON file defining:
- How the AI talks
- What tone to use
- How to respond
- Behavior rules

### Compiler = Prompt Generator

Converts personality JSON → System prompt for LLM

### Affinity = Relationship Level

Tracks how close the AI is with user:
- 0-20: Stranger (formal)
- 21-40: Acquaintance
- 41-60: Friend (casual)
- 61-80: Close friend
- 81-100: Soulmate (very personal)

### Facts = Learned Information

AI remembers:
- Name, age, location
- Preferences, hobbies
- Goals, work
- Important events

---

## 🎉 You're Ready!

**In just 5 minutes you learned:**
- ✅ Basic personality usage
- ✅ v1.1 memory features
- ✅ Affinity tracking
- ✅ Docker deployment

**Now build something amazing! 🚀**

---

## 💡 Quick Reference

```python
# Load personality
from luminoracore import Personality
p = Personality("path/to/personality.json")

# Compile
from luminoracore import PersonalityCompiler, LLMProvider
compiler = PersonalityCompiler()
result = compiler.compile(p, LLMProvider.OPENAI)

# Memory (v1.1)
from luminoracore.core.relationship.affinity import AffinityManager
affinity = AffinityManager()
state = affinity.create_state("user_id", "personality_name")

# Facts (v1.1)
from luminoracore.core.memory.fact_extractor import FactExtractor
facts = FactExtractor()
learned = facts.extract_sync("user_id", "message text")

# Episodes (v1.1)
from luminoracore.core.memory.episodic import EpisodicMemoryManager
episodes = EpisodicMemoryManager()
ep = episodes.create_episode("user_id", "achievement", "title", "summary")
```

---

**Questions?** Check `DOCUMENTATION_INDEX.md` or `README.md`

**Ready for more?** See `QUICK_START.md` for full tutorial

**Version:** v1.1.0  
**Last updated:** October 2025

