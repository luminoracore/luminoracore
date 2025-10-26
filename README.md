# LuminoraCore - AI Personality Framework

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-v1.1_production_ready-brightgreen.svg)](#)

**Professional AI personality framework with intelligent memory, relationship tracking, and contextual conversations.**

## 🚀 Quick Start

### Installation

```bash
# Install core framework
pip install luminoracore

# Install SDK for applications
pip install luminoracore-sdk-python

# Install CLI for development
pip install luminoracore-cli
```

### Basic Usage

```python
from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11

# Initialize client
client = LuminoraCoreClient()
await client.initialize()

# Create session and chat
session_id = await client.create_session("dr_luna")
response = await client.send_message(session_id, "Hello!")

# Use advanced memory features
client_v11 = LuminoraCoreClientV11(client)
await client_v11.save_fact("user123", "personal", "name", "Alice")
facts = await client_v11.get_facts("user123")
```

## 🧠 Key Features

### **Intelligent Memory System**
- **Automatic Fact Extraction** - AI learns about users from conversations
- **Relationship Tracking** - Affinity levels evolve based on interactions
- **Contextual Conversations** - Full conversation history awareness
- **Multi-Storage Support** - SQLite, PostgreSQL, DynamoDB, Redis, MongoDB

### **Dynamic Personality Evolution**
- **Relationship-Based Adaptation** - Personalities evolve as relationships deepen
- **Context Awareness** - Every response considers full conversation history
- **Real-time Evolution** - Changes happen instantly during conversations

### **Enterprise Ready**
- **Universal Database Support** - Works with any existing database schema
- **Flexible Configuration** - Adapts to any enterprise environment
- **Cloud-Native** - Optimized for AWS, Azure, Google Cloud
- **Professional Tooling** - CLI, migration system, monitoring

## 📚 Documentation

- **[Installation Guide](INSTALLATION_GUIDE.md)** - Complete setup instructions
- **[Memory System Guide](MEMORY_SYSTEM_DEEP_DIVE.md)** - Deep dive into memory capabilities
- **[Quick Start Guide](QUICK_START.md)** - Get started in minutes
- **[API Reference](luminoracore-sdk-python/docs/api_reference.md)** - Complete API documentation

## 🛠 Components

### **Core Framework** (`luminoracore/`)
- Independent core engine
- Memory and personality systems
- Storage interfaces
- No external dependencies

### **SDK** (`luminoracore-sdk-python/`)
- Python SDK for applications
- Client implementations
- Storage backends
- Provider integrations

### **CLI** (`luminoracore-cli/`)
- Command-line tools
- Memory management
- Database migrations
- Development utilities

## 🔧 CLI Commands

```bash
# Validate personalities
luminoracore validate my_personality.json

# Test with real LLM
luminoracore test scientist --provider openai

# Manage memory
luminoracore memory facts --session-id user123

# Database migrations
luminoracore migrate --status
```

## 🏗 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LuminoraCore  │    │   SDK Python    │    │      CLI        │
│                 │    │                 │    │                 │
│ • Standalone    │◄───┤ • Uses Core     │◄───┤ • Uses Core     │
│ • Core Engine   │    │ • Client Layer  │    │ • Tools Layer   │
│ • Memory System │    │ • API Wrapper   │    │ • Management    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Storage Providers

- **InMemoryStorageV11** - Development and testing
- **FlexibleSQLiteStorageV11** - Local development
- **FlexibleDynamoDBStorageV11** - AWS production
- **FlexiblePostgreSQLStorageV11** - Enterprise databases
- **FlexibleRedisStorageV11** - Caching and sessions
- **FlexibleMongoDBStorageV11** - Document storage

## 🔄 Version Compatibility

**100% Backward Compatible** - Existing code continues to work unchanged.

```python
# Your existing code works without changes
from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11

client = LuminoraCoreClient()
client_v11 = LuminoraCoreClientV11(client)
# All functions work exactly the same
```

## 📈 Performance

- **Optimized Architecture** - Core independence improves performance
- **Intelligent Caching** - Memory system reduces LLM calls
- **Flexible Storage** - Choose optimal backend for your use case
- **Async Support** - Non-blocking operations throughout

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the guides above
- **Issues**: Report bugs and feature requests
- **Discussions**: Ask questions and share ideas

---

**LuminoraCore** - Building intelligent AI personalities with memory and relationships.