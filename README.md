# LuminoraCore v1.1 - AI Personality Framework

**Build consistent, evolving AI personalities with memory and relationship tracking.**

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/luminoracore/luminoracore)
[![Tests](https://img.shields.io/badge/tests-179%20passing-green.svg)](https://github.com/luminoracore/luminoracore)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://python.org)

---

## 🚀 Quick Start (5 Minutes)

```bash
# Install all components
pip install -e luminoracore/
pip install -e luminoracore-sdk-python/
pip install -e luminoracore-cli/

# Run your first intelligent bot
python examples/luminoracore_v1_1_complete_demo.py
```

## ✨ What's New in v1.1

### 🧠 **Advanced Memory System**
- **Fact Extraction**: Automatically learns about users
- **Episodic Memory**: Remembers conversation context
- **Semantic Search**: Intelligent memory retrieval
- **Affinity Tracking**: Relationship level progression

### 🔄 **Dynamic Personality Evolution**
- **Adaptive Responses**: Personalities evolve based on interactions
- **Affinity-Based Changes**: Relationship affects personality traits
- **Context Awareness**: Responses consider conversation history

### 💾 **Flexible Storage**
- **Multiple Databases**: SQLite, PostgreSQL, DynamoDB, Redis, MongoDB
- **Flexible Configuration**: Works with any existing database schema
- **No Hardcoded Values**: Fully configurable for any project

### 🛠 **Enhanced CLI & Tools**
- **Memory Management**: View and manage conversation memory
- **Database Migrations**: Easy schema updates
- **Storage Configuration**: Interactive setup for any database

---

## 📖 Documentation

| Component | Description | Documentation |
|-----------|-------------|---------------|
| **Core** | Personality engine and memory system | [Core Docs](luminoracore/docs/) |
| **SDK** | Python client library | [SDK Docs](luminoracore-sdk-python/docs/) |
| **CLI** | Command-line tools | [CLI Guide](luminoracore-cli/README.md) |

### Key Guides
- [Installation Guide](INSTALLATION_GUIDE.md) - Complete setup instructions
- [Creating Personalities](CREATING_PERSONALITIES.md) - Build custom personalities
- [Business Case](CEO_BUSINESS_CASE.md) - Why choose LuminoraCore
- [Building Modular AI](BUILDING_MODULAR_AI_PERSONALITIES.md) - Architecture guide

---

## 🎯 Core Features

### Memory & Context
```python
# Automatic fact extraction and storage
await client.save_fact(
    user_id="user123",
    category="personal_info", 
    key="name",
    value="Carlos",
    confidence=0.95
)

# Context-aware conversations
response = await client.send_message_with_memory(
    session_id="session123",
    user_message="Hello, what do you remember about me?",
    personality_name="assistant"
)
```

### Dynamic Personalities
```python
# Personalities evolve based on affinity
affinity = await client.update_affinity(
    user_id="user123",
    personality_name="assistant", 
    points_delta=5,
    interaction_type="positive"
)
```

### Flexible Storage
```python
# Works with any database configuration
storage = FlexibleSQLiteStorageV11(
    database_path="your_database.db",
    facts_table="your_facts_table"
)

storage = FlexibleDynamoDBStorageV11(
    table_name="your_table",
    region_name="your_region"
)
```

---

## 🏗 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LuminoraCore  │    │   SDK Python    │    │      CLI        │
│                 │    │                 │    │                 │
│ • Personality   │◄───┤ • Client v1.1   │◄───┤ • Memory Mgmt   │
│   Engine        │    │ • Storage       │    │ • Migrations    │
│ • Memory System │    │   Management    │    │ • Validation    │
│ • Evolution     │    │ • Context API   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🚀 Use Cases

- **Customer Support**: Intelligent bots that remember customer history
- **Educational AI**: Tutors that adapt to student progress
- **Gaming NPCs**: Characters with evolving personalities
- **Personal Assistants**: AI that learns user preferences
- **Therapeutic AI**: Bots that build emotional connections

---

## 📊 Performance

- **Memory Operations**: < 50ms average
- **Context Retrieval**: < 100ms average  
- **Personality Evolution**: Real-time adaptation
- **Storage Flexibility**: Works with any database

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

See [Contributing Guide](luminoracore/CONTRIBUTING.md) for details.

---

## 📄 License

MIT License - see [LICENSE](luminoracore/LICENSE) for details.

---

## 🆘 Support

- **Documentation**: Check the [docs](luminoracore/docs/) directory
- **Examples**: See [examples](examples/) directory
- **Issues**: [GitHub Issues](https://github.com/luminoracore/luminoracore/issues)

---

**Built with ❤️ for the AI community**