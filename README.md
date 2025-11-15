# 🧠 LuminoraCore

> Your AI personality that travels with you. One memory, all models.

[![GitHub stars](https://img.shields.io/github/stars/yourusername/luminoracore?style=social)](https://github.com/yourusername/luminoracore)
[![Tests](https://img.shields.io/github/workflow/status/yourusername/luminoracore/tests?label=tests)](https://github.com/yourusername/luminoracore/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## ⚡ The Problem

Most AI systems today are learning to remember — but each platform remembers in isolation. Your ChatGPT might recall a conversation. Claude or Gemini might, too. None of them know it's still you.

**The result?** You lose your conversation history, context, and the personality you've built when switching between AI platforms or starting fresh.

[![GIF: ChatGPT → lose data → start over](https://via.placeholder.com/800x400?text=GIF+Placeholder:+ChatGPT+%E2%86%92+lose+data+%E2%86%92+start+over)](https://example.com/problem-demo.gif)

## ✨ The Solution

LuminoraCore lets every user build their own portable "AI conversation data lake" and evolve AI personalities over time — independent from any single LLM vendor. Your conversations are your data: capture them, analyze what matters, and use those insights to make your AI personalities grow with you.

**The result?** Continuity across AI platforms. Real evolution through data, persistence, and relationships that survive time, tools, and providers.

[![GIF: ChatGPT → LuminoraCore → Claude → data persists](https://via.placeholder.com/800x400?text=GIF+Placeholder:+ChatGPT+%E2%86%92+LuminoraCore+%E2%86%92+Claude+%E2%86%92+data+persists)](https://example.com/solution-demo.gif)

## 🎯 Quick Start (3 lines of code)

```bash
pip install luminoracore
# 2 more lines → working
```

**Full example:**

```python
from luminoracore import Personality, Session

personality = Personality.load("my-personality.json")
session = Session(personality)
response = session.chat("Hello!")
```

See `QUICK_START.md` for detailed examples and CLI commands.

## 🎬 See It In Action

[![Watch the demo](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)

*Replace VIDEO_ID with your actual YouTube video ID*

## 💡 Use Cases

- **Personal AI companion** — Build a consistent AI assistant that remembers you across all platforms
- **Customer service bots** — Maintain conversation context and personality across sessions
- **Research assistants** — Capture and evolve knowledge from research conversations
- **Educational tutors** — Create personalized learning experiences that adapt over time
- **Creative collaborators** — Develop AI personalities that learn your style and preferences

## 🚀 Live Demo

Try LuminoraCore in action: [demo.luminoracore.com](https://demo.luminoracore.com)

*Replace with your actual demo URL*

## 📦 Installation

### Quick Install

```bash
# Core (required)
cd luminoracore && pip install . && cd ..

# SDK (optional, for sessions and storage)
cd luminoracore-sdk-python && pip install . && cd ..

# CLI (optional, for developer tools)
cd luminoracore-cli && pip install . && cd ..
```

**Windows note:** Install Core without editable mode (no `-e`) to avoid namespace issues.

For detailed installation instructions, see `INSTALLATION_GUIDE.md`.

## 🏗️ Architecture

```
Capture → Analyze → Store → Evolve → Use
```

**The Flow:**

- **Capture:** Conversation messages and metadata from any LLM interaction
- **Analyze:** Extract sentiment, learned facts, memorable episodes, and relationship/affinity signals
- **Store:** Pluggable backends (SQLite, Redis, PostgreSQL, MongoDB, DynamoDB, in-memory)
- **Evolve:** Update personality state and configuration over time based on insights
- **Use:** Core/CLI/SDK interfaces for apps and workflows

**Components:**

- `luminoracore/` (Core): JSON personalities, validation, compilation, blending
- `luminoracore-sdk-python/` (SDK): sessions, storage integrations, analytics, snapshots
- `luminoracore-cli/` (CLI): validate/compile/blend, snapshot export/import, developer tools

**Storage Flexibility:**

Choose your storage backend and swap without touching personality logic. The `FlexibleStorageManager` auto-detects configuration via JSON or environment variables. Export snapshots (facts, episodes, affinity, moods) through the SDK regardless of the backend you choose.

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report bugs** — Open an issue with detailed information
2. **Suggest features** — Share your ideas for improving LuminoraCore
3. **Submit pull requests** — Follow our coding standards and include tests
4. **Improve documentation** — Help make LuminoraCore more accessible

**Development Setup:**

```bash
git clone https://github.com/yourusername/luminoracore.git
cd luminoracore
# Follow installation steps above
```

**Guidelines:**

- Follow existing code style and conventions
- Add tests for new features
- Update documentation as needed
- Keep commits focused and well-described

## 📄 License

MIT — see headers and component licenses as applicable.

---

## 📚 Additional Documentation

- **Installation Guide (EN):** `INSTALLATION_GUIDE.md`
- **Quick Start (EN):** `QUICK_START.md`
- **Memory System Deep Dive (EN):** `MEMORY_SYSTEM_DEEP_DIVE.md`
- **Release Notes v1.1 (EN):** `RELEASE_NOTES_v1.1.md`

## 🔍 Current Status (v1.1)

**Production-Ready:**
- ✅ Personality schema & compilation (100%)
- ✅ Memory system & storage adapters (90%)

**Beta:**
- 🔄 Analytics & snapshots (~60%)

**In Progress:**
- 🚧 Mood System (~40%)
- 🚧 Semantic Search (~15%)

See `RELEASE_NOTES_v1.1.md` for details and migration notes from v1.0.
