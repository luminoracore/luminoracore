# LuminoraCore Publishing Guide

This guide explains how to build and publish LuminoraCore packages for distribution.

---

## 🎯 Quick Overview

LuminoraCore can be distributed in several ways:

1. **PyPI** (Recommended) - `pip install luminoracore`
2. **Wheel files (.whl)** - Installable packages
3. **GitHub Releases** - Source code + wheels
4. **Docker** - Container images
5. **Executables** - Standalone binaries (advanced)

---

## 📦 Option 1: Build Packages (Wheels)

### Windows

```powershell
# Build all packages
.\build_all_packages.ps1
```

**This creates:**
- `releases/luminoracore-1.0.0-py3-none-any.whl` (~1-2 MB)
- `releases/luminoracore_cli-1.0.0-py3-none-any.whl` (~500 KB)
- `releases/luminoracore_sdk-1.0.0-py3-none-any.whl` (~2-3 MB)

### Linux/Mac

```bash
# Build all packages
chmod +x build_all_packages.sh
./build_all_packages.sh
```

---

## 🧪 Test Locally Before Publishing

### Windows

```powershell
# Install from local wheels
.\install_from_local.ps1

# Verify installation
python verify_installation.py
```

### Linux/Mac

```bash
# Install from local wheels
chmod +x install_from_local.sh
./install_from_local.sh

# Verify installation
python verify_installation.py
```

**Expected result:** `🎉 INSTALLATION COMPLETE AND CORRECT`

---

## 🌐 Option 2: Publish to PyPI (Worldwide Distribution)

### Prerequisites

1. **Create PyPI account**: https://pypi.org/account/register/
2. **Create API token**: https://pypi.org/manage/account/token/
   - Token name: `luminoracore-publisher`
   - Scope: Entire account (or specific project)
   - Copy the token (starts with `pypi-`)

3. **Configure credentials** (optional):
   ```bash
   # Create ~/.pypirc (Linux/Mac) or %USERPROFILE%\.pypirc (Windows)
   [pypi]
   username = __token__
   password = pypi-YOUR-API-TOKEN-HERE
   ```

### Publish

#### Windows

```powershell
# Build and publish
.\build_all_packages.ps1
.\publish_to_pypi.ps1
```

#### Linux/Mac

```bash
# Build and publish
./build_all_packages.sh
./publish_to_pypi.sh
```

**You'll be prompted for:**
- Username: `__token__`
- Password: `pypi-YOUR-API-TOKEN`

### After Publishing

Your packages will be available at:
- https://pypi.org/project/luminoracore/
- https://pypi.org/project/luminoracore-cli/
- https://pypi.org/project/luminoracore-sdk/

**Anyone can install with:**
```bash
pip install luminoracore
pip install luminoracore-cli
pip install luminoracore-sdk
```

---

## 📥 Option 3: Use in Another Local Project

### Method 1: Install from PyPI (if published)

```bash
# In your new project
pip install luminoracore
pip install luminoracore-cli
pip install luminoracore-sdk
```

### Method 2: Install from local wheels

```bash
# Copy wheels to your project
cp releases/*.whl /path/to/your/project/

# In your project
pip install luminoracore-1.0.0-py3-none-any.whl
pip install luminoracore_cli-1.0.0-py3-none-any.whl
pip install luminoracore_sdk-1.0.0-py3-none-any.whl
```

### Method 3: Install from local directory

```bash
# In your project
pip install /path/to/LuminoraCoreBase/luminoracore
pip install /path/to/LuminoraCoreBase/luminoracore-cli
pip install /path/to/LuminoraCoreBase/luminoracore-sdk-python
```

### Method 4: Install from GitHub

```bash
# Install directly from your GitHub repo
pip install git+https://github.com/rulyaltamira/luminoracore.git#subdirectory=luminoracore
pip install git+https://github.com/rulyaltamira/luminoracore.git#subdirectory=luminoracore-cli
pip install git+https://github.com/rulyaltamira/luminoracore.git#subdirectory=luminoracore-sdk-python
```

---

## 🐳 Option 4: Docker Distribution

### Build Docker Image

```bash
# Build image
docker build -t ereace/luminoracore:v1.0.0 -f luminoracore-sdk-python/Dockerfile .

# Test locally
docker run -it ereace/luminoracore:v1.0.0 luminoracore --version

# Publish to Docker Hub
docker login
docker push ereace/luminoracore:v1.0.0
```

### Users Install

```bash
docker pull ereace/luminoracore:v1.0.0
docker run -it ereace/luminoracore:v1.0.0
```

---

## 🚀 Recommended Publishing Workflow

### Step 1: Test Everything Locally

```bash
# Build packages
.\build_all_packages.ps1  # Windows
./build_all_packages.sh   # Linux/Mac

# Test installation
.\install_from_local.ps1  # Windows
./install_from_local.sh   # Linux/Mac

# Verify
python verify_installation.py

# Run tests
pytest tests/ -v
```

### Step 2: Publish to PyPI

```bash
# Publish to PyPI
.\publish_to_pypi.ps1  # Windows
./publish_to_pypi.sh   # Linux/Mac
```

### Step 3: Create GitHub Release

1. Go to: https://github.com/rulyaltamira/luminoracore/releases/new
2. Tag: `v1.0.0`
3. Title: `LuminoraCore v1.0.0 - Production Ready`
4. Description:
   ```markdown
   ## 🎉 LuminoraCore v1.0.0 - Production Ready
   
   ### Installation
   ```bash
   pip install luminoracore
   pip install luminoracore-cli
   pip install luminoracore-sdk
   ```
   
   ### What's New
   - ✅ 7 LLM providers (OpenAI, Anthropic, DeepSeek, Mistral, Cohere, Google, Llama)
   - ✅ 6 storage backends (Memory, JSON, SQLite, Redis, PostgreSQL, MongoDB)
   - ✅ PersonaBlend™ technology
   - ✅ 179/179 tests passing (v1.1)
   
   ### Documentation
   - [Quick Start](QUICK_START.md)
   - [Installation Guide](INSTALLATION_GUIDE.md)
   - [Creating Personalities](CREATING_PERSONALITIES.md)
   ```

5. Attach files:
   - `releases/*.whl` files
   - Source code (auto-generated by GitHub)

### Step 4: Update Documentation

Update README.md with PyPI badges:
```markdown
[![PyPI - luminoracore](https://img.shields.io/pypi/v/luminoracore.svg)](https://pypi.org/project/luminoracore/)
[![PyPI - CLI](https://img.shields.io/pypi/v/luminoracore-cli.svg)](https://pypi.org/project/luminoracore-cli/)
[![PyPI - SDK](https://img.shields.io/pypi/v/luminoracore-sdk.svg)](https://pypi.org/project/luminoracore-sdk/)
```

### Step 5: Announce

- Twitter/X
- LinkedIn
- Reddit (r/Python, r/MachineLearning)
- Hacker News
- Dev.to / Medium article

---

## 🔄 Updating Versions

### When you make changes:

1. **Update version numbers:**
   - `luminoracore/setup.py` → `version="1.0.1"`
   - `luminoracore-cli/luminoracore_cli/__version__.py` → `__version__ = "1.0.1"`
   - `luminoracore-sdk-python/luminoracore_sdk/__version__.py` → `__version__ = "1.0.1"`

2. **Rebuild packages:**
   ```bash
   .\build_all_packages.ps1
   ```

3. **Publish update:**
   ```bash
   .\publish_to_pypi.ps1
   ```

PyPI **does not allow** overwriting versions. If you upload `1.0.0`, you can't upload `1.0.0` again. You must increment to `1.0.1`.

---

## ⚠️ Important Notes

### Before Publishing to PyPI:

1. ✅ **All tests pass** (`pytest tests/ -v`)
2. ✅ **Documentation is complete**
3. ✅ **Version numbers are correct**
4. ✅ **README.md is updated**
5. ✅ **CHANGELOG is updated** (create one if needed)
6. ✅ **No sensitive data** in code (API keys, passwords)
7. ✅ **License file exists** (MIT)

### PyPI Naming Rules:

- Package names are **case-insensitive**
- Cannot use underscores in PyPI name (use hyphens)
- Names are **permanent** (can't change without new project)

### Test PyPI First (Optional):

```bash
# Publish to Test PyPI first
twine upload --repository testpypi luminoracore/dist/*

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ luminoracore
```

---

## 📊 What Users Will See

### After publishing to PyPI:

```bash
# Search for your package
pip search luminoracore

# Install
pip install luminoracore

# View info
pip show luminoracore
# Name: luminoracore
# Version: 1.0.0
# Author: Ruly Altamirano
# Home-page: https://github.com/rulyaltamira/luminoracore
```

### On PyPI website:

- https://pypi.org/project/luminoracore/
  - Description from README.md
  - Installation instructions
  - Download statistics
  - Version history

---

## 🎯 Summary: Choose Your Distribution Method

### For Open Source Project (RECOMMENDED):
1. ✅ **Publish to PyPI** - Makes it easy for everyone
2. ✅ **GitHub Releases** - Source code + wheels
3. ✅ **Docker Hub** - For container users

### For Private/Internal Use:
1. ✅ **Local wheels** - Share .whl files
2. ✅ **Private PyPI** (PyPI server)
3. ✅ **Git install** - Install from your private repo

### For End Users (Non-developers):
1. ✅ **Windows .exe** - No Python required
2. ✅ **Linux AppImage** - No Python required
3. ✅ **macOS .app** - No Python required

---

**Ready to publish? Run `.\build_all_packages.ps1` and then `.\publish_to_pypi.ps1`!** 🚀

---

_Created by: Ereace - Ruly Altamirano_

