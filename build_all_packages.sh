#!/bin/bash
# Build All LuminoraCore Packages (Linux/Mac version)
# Creates .whl files for distribution

set -e

echo "==============================================="
echo "LuminoraCore Package Builder"
echo "==============================================="

# Check if build tools are installed
echo -e "\nChecking dependencies..."
if ! command -v pip &> /dev/null; then
    echo "ERROR: pip not found. Please install Python."
    exit 1
fi

# Install build tools if needed
echo "Installing/upgrading build tools..."
pip install --upgrade build twine wheel setuptools

# Clean previous builds
echo -e "\nCleaning previous builds..."
for component in luminoracore luminoracore-cli luminoracore-sdk-python; do
    rm -rf "$component/dist"
    rm -rf "$component/build"
    rm -rf "$component"/*.egg-info
done

# Build packages
echo -e "\n==============================================="
echo "Building packages..."
echo "==============================================="

# 1. Build luminoracore (base engine)
echo -e "\n[1/3] Building luminoracore (Base Engine)..."
cd luminoracore
python -m build
echo "✅ luminoracore built successfully"
cd ..

# 2. Build luminoracore-cli
echo -e "\n[2/3] Building luminoracore-cli..."
cd luminoracore-cli
python -m build
echo "✅ luminoracore-cli built successfully"
cd ..

# 3. Build luminoracore-sdk-python
echo -e "\n[3/3] Building luminoracore-sdk-python..."
cd luminoracore-sdk-python
python -m build
echo "✅ luminoracore-sdk built successfully"
cd ..

# Create releases directory
echo -e "\nOrganizing releases..."
mkdir -p releases

# Copy all wheels and source distributions to releases
cp luminoracore/dist/*.whl releases/
cp luminoracore-cli/dist/*.whl releases/
cp luminoracore-sdk-python/dist/*.whl releases/

cp luminoracore/dist/*.tar.gz releases/ 2>/dev/null || true
cp luminoracore-cli/dist/*.tar.gz releases/ 2>/dev/null || true
cp luminoracore-sdk-python/dist/*.tar.gz releases/ 2>/dev/null || true

# Summary
echo -e "\n==============================================="
echo "BUILD COMPLETE"
echo "==============================================="

echo -e "\n📦 Packages created:"
for file in releases/*.whl; do
    size=$(du -h "$file" | cut -f1)
    echo "  ✅ $(basename "$file") ($size)"
done

echo -e "\n📁 Location: releases/"
echo -e "\n🚀 Next steps:"
echo "  1. Test locally: ./install_from_local.sh"
echo "  2. Publish to PyPI: ./publish_to_pypi.sh"

echo -e "\n💡 To install in another project:"
echo "  pip install path/to/releases/luminoracore-*.whl"

