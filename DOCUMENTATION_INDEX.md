# 📚 Documentation Index - LuminoraCore

**All project documentation organized by categories.**

---

## 🚀 Getting Started (START HERE)

### 1. [QUICK_START.md](QUICK_START.md) ⭐
**First time? Start here.**
- Express installation in 1 command
- Quick verification
- Common use cases
- Command summary

### 2. [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) ⭐⭐
**Complete step-by-step guide.**
- Detailed installation of each component
- Dependency explanation
- Complete practical examples
- Troubleshooting
- API key configuration

### 3. [CREATING_PERSONALITIES.md](CREATING_PERSONALITIES.md) ⭐⭐
**Complete guide for creating AI personalities.**
- JSON file location and structure
- Detailed explanation of each section
- Complete schema and validations
- Step-by-step examples
- 11 example personalities included

### 4. [INSTALLATION_VERIFICATION.md](INSTALLATION_VERIFICATION.md) ⭐
**How to use the verification script.**
- What the script automatically verifies
- When and how to use it
- Result interpretation
- Common troubleshooting
- Practical use cases

---

## 📦 Project Components

### Base Engine (luminoracore)

| Document | Description |
|----------|-------------|
| `luminoracore/README.md` | Base engine documentation |
| `luminoracore/docs/getting_started.md` | Getting started guide |
| `luminoracore/docs/api_reference.md` | API reference |
| `luminoracore/docs/personality_format.md` | Personality format |
| `luminoracore/docs/best_practices.md` | Best practices |

### CLI (luminoracore-cli)

| Document | Description |
|----------|-------------|
| `luminoracore-cli/README.md` | CLI documentation |
| `luminoracore-cli/luminoracore_cli/commands/` | Command source code |

### SDK (luminoracore-sdk-python)

| Document | Description |
|----------|-------------|
| `luminoracore-sdk-python/README.md` | SDK documentation |
| `luminoracore-sdk-python/docs/api_reference.md` | Complete API reference |

---

## 🎯 Guides by Use Case

### For New Developers

1. **First contact**
   - [QUICK_START.md](QUICK_START.md) - Installation and verification
   
2. **Learn more**
   - [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) - Complete guide
   - `luminoracore/examples/basic_usage.py` - Basic example
   
3. **Understand the project**
   - [ESTADO_ACTUAL_PROYECTO.md](ESTADO_ACTUAL_PROYECTO.md) - Current status
   - [CARACTERISTICAS_TECNICAS_LUMINORACORE.md](CARACTERISTICAS_TECNICAS_LUMINORACORE.md) - Technical features

### For Working with Personalities

1. **Understand the format**
   - `luminoracore/docs/personality_format.md` - JSON format
   - `luminoracore/luminoracore/personalities/*.json` - Real examples
   
2. **Create personalities**
   - [CREATING_PERSONALITIES.md](CREATING_PERSONALITIES.md) - Complete guide
   - `luminoracore create --interactive` - CLI command
   
3. **Validate and compile**
   - [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) - CLI section
   - `luminoracore/docs/best_practices.md` - Best practices

### For Building Applications

1. **Basic SDK**
   - `luminoracore-sdk-python/examples/simple_usage.py` - Simple example
   - `luminoracore-sdk-python/README.md` - Complete documentation
   
2. **Integrations**
   - `luminoracore-sdk-python/examples/integrations/` - FastAPI, Streamlit
   
3. **Advanced**
   - `luminoracore-sdk-python/docs/api_reference.md` - Complete API
   - `luminoracore/examples/blending_demo.py` - PersonaBlend

---

## 📋 Helper Scripts

### Installation

| Script | Platform | Description |
|--------|---------|-------------|
| `instalar_todo.ps1` | Windows PowerShell | Automatically installs everything |
| `instalar_todo.sh` | Linux/Mac | Automatically installs everything |

### Verification

| Script | Verifies |
|--------|----------|
| `ejemplo_quick_start_core.py` | Base engine (luminoracore) |
| `ejemplo_quick_start_cli.py` | CLI (luminoracore-cli) |
| `ejemplo_quick_start_sdk.py` | SDK (luminoracore-sdk) |
| `verify_installation.py` | Complete installation |

### Tests

| Script | Description |
|--------|-------------|
| `test_wizard_simple.py` | Tests creation wizard |
| `luminoracore/examples/*.py` | Base engine examples |
| `luminoracore-sdk-python/examples/*.py` | SDK examples |

---

## 📖 Technical Documentation

### Architecture and Design

| Document | Content |
|----------|---------|
| [CARACTERISTICAS_TECNICAS_LUMINORACORE.md](CARACTERISTICAS_TECNICAS_LUMINORACORE.md) | Detailed technical features |
| [ESTADO_ACTUAL_PROYECTO.md](ESTADO_ACTUAL_PROYECTO.md) | Current development status |
| `Docs/LuminoraCore.txt` | Original specification |
| `Docs/PersonaCore funcionamiento.txt` | PersonaCore functioning |

### Planning

| Document | Content |
|----------|---------|
| [PLAN_LIDERAZGO_LUMINORACORE.md](PLAN_LIDERAZGO_LUMINORACORE.md) | Leadership plan |
| [PROGRESO_LIDERAZGO.md](PROGRESO_LIDERAZGO.md) | Plan progress |
| [ROADMAP_IMPLEMENTACION.md](ROADMAP_IMPLEMENTACION.md) | Implementation roadmap |

### Additional Documentation

| Document | Content |
|----------|---------|
| [GUIA_VISUAL_LUMINORACORE.md](GUIA_VISUAL_LUMINORACORE.md) | Project visual guide |
| `Docs/mejoras.txt` | Proposed improvements list |

---

## 🌍 Documentation in English

### Core

| Document | Content |
|----------|---------|
| `Docs/EnglishLuminoraCore.txt` | LuminoraCore in English |
| `Docs/EnglishLuminoraCli.txt` | CLI in English |
| `Docs/EnglishLuminoraSDK.txt` | SDK in English |

### CLI Versions

| Document | Content |
|----------|---------|
| `Docs/LuminoraCoreCliV1.txt` | CLI version 1 |
| `Docs/LuminoraCoreCLIv2.txt` | CLI version 2 |

---

## 🗂️ Folder Structure

```
luminoracore/
├── 🚀 QUICK_START.md                    ⭐ START HERE
├── 📘 INSTALLATION_GUIDE.md            ⭐ COMPLETE GUIDE
├── 🎭 CREATING_PERSONALITIES.md        ⭐ PERSONALITY GUIDE
├── 🧪 INSTALLATION_VERIFICATION.md     ⭐ VERIFICATION GUIDE
├── 📚 DOCUMENTATION_INDEX.md           ← You are here
│
├── 📦 luminoracore/                    Base Engine
│   ├── README.md
│   ├── docs/
│   ├── examples/
│   └── luminoracore/
│
├── 🛠️ luminoracore-cli/                CLI
│   ├── README.md
│   └── luminoracore_cli/
│
├── 🐍 luminoracore-sdk-python/         SDK
│   ├── README.md
│   ├── docs/
│   ├── examples/
│   └── luminoracore_sdk/
│
├── 🎭 luminoracore/luminoracore/personalities/  Example personalities
│   ├── dr_luna.json
│   ├── rocky_inspiration.json
│   └── ...
│
├── 🔧 Installation Scripts
│   ├── instalar_todo.ps1               Windows
│   └── instalar_todo.sh                Linux/Mac
│
├── ✅ Verification Scripts
│   ├── verify_installation.py
│   ├── ejemplo_quick_start_core.py
│   ├── ejemplo_quick_start_cli.py
│   └── ejemplo_quick_start_sdk.py
│
└── 📄 Docs/                            Additional documentation
    ├── LuminoraCore.txt
    ├── personality_format.md
    └── ...
```

---

## 🎯 Recommended Workflows

### 1. First Time (New User)

```
QUICK_START.md
    ↓
instalar_todo.ps1 / instalar_todo.sh
    ↓
verify_installation.py
    ↓
INSTALLATION_GUIDE.md
    ↓
Explore examples in luminoracore/examples/
```

### 2. Create a Personality

```
CREATING_PERSONALITIES.md
    ↓
luminoracore create --interactive
    ↓
luminoracore validate my_personality.json
    ↓
luminoracore/docs/best_practices.md
```

### 3. Build an Application

```
INSTALLATION_GUIDE.md (SDK Section)
    ↓
luminoracore-sdk-python/examples/simple_usage.py
    ↓
luminoracore-sdk-python/docs/api_reference.md
    ↓
luminoracore-sdk-python/examples/integrations/
```

---

## 📞 Support

### First, check:

1. [QUICK_START.md](QUICK_START.md) - "Common Issues" section
2. [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) - "Troubleshooting" section
3. [ESTADO_ACTUAL_PROYECTO.md](ESTADO_ACTUAL_PROYECTO.md) - Project status

### Then:

- Review examples in `examples/`
- Read component-specific documentation
- Create an issue on the repository

---

## 🔄 Updates

This document is updated with each major change in the documentation structure.

**Last updated:** 2025-10-05

---

## ✨ Express Summary

| I need... | Document |
|-----------|----------|
| **Quick installation** | [QUICK_START.md](QUICK_START.md) |
| **Complete guide** | [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) |
| **Understand the project** | [ESTADO_ACTUAL_PROYECTO.md](ESTADO_ACTUAL_PROYECTO.md) |
| **Create personalities** | [CREATING_PERSONALITIES.md](CREATING_PERSONALITIES.md) |
| **Use base engine** | `luminoracore/README.md` |
| **Use CLI** | `luminoracore-cli/README.md` |
| **Use SDK** | `luminoracore-sdk-python/README.md` |
| **See examples** | `*/examples/*.py` |
| **Personality format** | `luminoracore/docs/personality_format.md` |

---

**Find everything you need in this index! 📚**

