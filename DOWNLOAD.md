# Download LuminoraCore

Multiple installation options to fit your needs.

---

## 🚀 Quick Install (Recommended)

### For Developers & Most Users

```bash
pip install luminoracore
pip install luminoracore-cli
pip install luminoracore-sdk
```

**Requirements:** Python 3.8+

**Works on:** Windows, Linux, macOS

---

## 📦 Installation Options

### Option 1: PyPI (Python Package Index) ⭐

**Best for:** Developers, Python users, production deployments

```bash
# Install all components
pip install luminoracore
pip install luminoracore-cli
pip install "luminoracore-sdk[all]"

# Or use automated installer
# Windows:
.\install_all.ps1

# Linux/Mac:
./install_all.sh
```

**Advantages:**
- ✅ Official packages
- ✅ Automatic dependency management
- ✅ Easy updates: `pip install --upgrade luminoracore`
- ✅ Works everywhere

---

### Option 2: Wheel Files (.whl)

**Best for:** Offline installation, private networks, testing

**Download wheels:**
- [luminoracore-1.0.0-py3-none-any.whl](releases/luminoracore-1.0.0-py3-none-any.whl) (~2 MB)
- [luminoracore_cli-1.0.0-py3-none-any.whl](releases/luminoracore_cli-1.0.0-py3-none-any.whl) (~500 KB)
- [luminoracore_sdk-1.0.0-py3-none-any.whl](releases/luminoracore_sdk-1.0.0-py3-none-any.whl) (~3 MB)

**Install:**
```bash
pip install luminoracore-1.0.0-py3-none-any.whl
pip install luminoracore_cli-1.0.0-py3-none-any.whl
pip install luminoracore_sdk-1.0.0-py3-none-any.whl
```

**Advantages:**
- ✅ Works offline
- ✅ No PyPI dependency
- ✅ Exact version control

---

### Option 3: From Source (GitHub)

**Best for:** Contributors, customization, latest development version

```bash
# Clone repository
git clone https://github.com/rulyaltamira/luminoracore.git
cd luminoracore

# Install
.\install_all.ps1  # Windows
./install_all.sh   # Linux/Mac
```

**Install from GitHub without cloning:**
```bash
pip install git+https://github.com/rulyaltamira/luminoracore.git#subdirectory=luminoracore
pip install git+https://github.com/rulyaltamira/luminoracore.git#subdirectory=luminoracore-cli
pip install git+https://github.com/rulyaltamira/luminoracore.git#subdirectory=luminoracore-sdk-python
```

**Advantages:**
- ✅ Latest code
- ✅ Can modify source
- ✅ Contribute back

---

### Option 4: Docker Image

**Best for:** Containerized deployments, microservices, serverless

```bash
# Pull image
docker pull ereace/luminoracore:v1.0.0

# Run
docker run -it ereace/luminoracore:v1.0.0 luminoracore --version

# Use in docker-compose
services:
  luminoracore:
    image: ereace/luminoracore:v1.0.0
```

**Advantages:**
- ✅ Isolated environment
- ✅ No local Python needed
- ✅ Perfect for backends

---

## 💻 Platform-Specific Instructions

### Windows

```powershell
# 1. Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install LuminoraCore
pip install luminoracore
pip install luminoracore-cli
pip install "luminoracore-sdk[all]"

# 3. Verify
python verify_installation.py
```

### Linux/Mac

```bash
# 1. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# 2. Install LuminoraCore
pip install luminoracore
pip install luminoracore-cli
pip install "luminoracore-sdk[all]"

# 3. Verify
python verify_installation.py
```

---

## ✅ Verify Installation

After installation, run:

```bash
python verify_installation.py
```

**Expected output:**
```
🎉 INSTALLATION COMPLETE AND CORRECT

Installed components:
  ✅ Base Engine/SDK (luminoracore)
  ✅ CLI (luminoracore-cli)
  ✅ Complete SDK (with providers and client)
```

---

## 📚 What's Included?

### Core Engine (luminoracore)
- Personality management
- Validation engine
- Compilation for 7 LLM providers
- PersonaBlend™ technology

### CLI Tool (luminoracore-cli)
- `luminoracore validate` - Validate personalities
- `luminoracore compile` - Compile to prompts
- `luminoracore create` - Interactive wizard
- `luminoracore test` - Test with real APIs
- `luminoracore blend` - Blend personalities
- `luminoracore serve` - Development server

### SDK (luminoracore-sdk)
- Session management
- Real LLM API calls
- 7 LLM providers
- 6 storage backends
- Async/await API

---

## 🆘 Need Help?

### Installation Issues?
1. Run: `python verify_installation.py`
2. Read: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
3. Check: [Troubleshooting](https://github.com/rulyaltamira/luminoracore/wiki/Troubleshooting)

### Questions?
- 📖 [Documentation](DOCUMENTATION_INDEX.md)
- 🐛 [Report Issue](https://github.com/rulyaltamira/luminoracore/issues)
- 📧 [Email](mailto:contact@luminoracore.com)

---

## 📊 Version History

### v1.0.0 (Current - Production Ready)
- First stable release
- 7 LLM providers
- 6 storage backends
- 179/179 tests passing (v1.1)
- Complete documentation

---

<div align="center">

**Made with ❤️ by Ereace - Ruly Altamirano**

[⭐ Star on GitHub](https://github.com/rulyaltamira/luminoracore) • [📖 Documentation](https://github.com/rulyaltamira/luminoracore/wiki) • [🐛 Report Issue](https://github.com/rulyaltamira/luminoracore/issues)

</div>

