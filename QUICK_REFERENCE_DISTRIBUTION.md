# Quick Reference: Distribution & Publishing

## 🎯 To use LuminoraCore in another LOCAL project

### Option 1: From local wheels (WITHOUT publishing to PyPI)

```bash
# 1. Build packages (once only)
.\build_all_packages.ps1

# 2. Install from local wheels
.\install_from_local.ps1

# 3. Verify installation
python verify_installation.py
```

### Option 2: From source (development mode)

```bash
# 1. Clone the repository
git clone https://github.com/your-user/luminoracore.git
cd luminoracore

# 2. Install in development mode
pip install -e luminoracore/
pip install -e luminoracore-cli/
pip install -e luminoracore-sdk-python/

# 3. Verify installation
python verify_installation.py
```

---

## 🚀 To publish to PyPI (public distribution)

### Step 1: Prepare for publishing

```bash
# 1. Update version numbers (if needed)
# Check: luminoracore/__init__.py, luminoracore-cli/__version__.py, etc.

# 2. Build packages
.\build_all_packages.ps1

# 3. Test locally
.\install_from_local.ps1
python verify_installation.py
```

### Step 2: Publish to PyPI

```bash
# 1. Publish all packages
.\publish_to_pypi.ps1

# 2. Verify on PyPI
# Check: https://pypi.org/project/luminoracore/
# Check: https://pypi.org/project/luminoracore-cli/
# Check: https://pypi.org/project/luminoracore-sdk/
```

### Step 3: Test public installation

```bash
# 1. Create new virtual environment
python -m venv test_public
.\test_public\Scripts\activate

# 2. Install from PyPI
pip install luminoracore
pip install luminoracore-cli
pip install luminoracore-sdk

# 3. Verify installation
python verify_installation.py
```

---

## 📋 Distribution Checklist

### ✅ Before Publishing

- [ ] All tests passing (179/179)
- [ ] Version numbers updated to 1.1.0
- [ ] Documentation in English
- [ ] All examples working
- [ ] Docker configuration updated
- [ ] Environment variables documented

### ✅ After Publishing

- [ ] Packages available on PyPI
- [ ] Installation from PyPI works
- [ ] All components functional
- [ ] Documentation accessible
- [ ] Examples executable

---

## 🎯 Quick Commands Summary

```bash
# Build everything
.\build_all_packages.ps1

# Install locally
.\install_from_local.ps1

# Publish to PyPI
.\publish_to_pypi.ps1

# Verify installation
python verify_installation.py

# Run examples
python examples/basic_example.py
python examples/advanced_example.py
```

---

## 📞 Support

If you encounter any issues:

1. **Check documentation**: `DOCUMENTATION_INDEX.md`
2. **Run verification**: `python verify_installation.py`
3. **Check examples**: `examples/` directory
4. **Review logs**: Check console output for errors

---

**Status**: ✅ Ready for distribution  
**Version**: 1.1.0  
**Last Updated**: October 2025