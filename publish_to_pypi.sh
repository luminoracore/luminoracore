#!/bin/bash
# Publish LuminoraCore to PyPI (Linux/Mac version)
# Make the packages available worldwide via: pip install luminoracore

set -e

echo "==============================================="
echo "LuminoraCore PyPI Publisher"
echo "==============================================="

# Check if packages are built
if [ ! -d "luminoracore/dist" ] || [ ! -d "luminoracore-cli/dist" ] || [ ! -d "luminoracore-sdk-python/dist" ]; then
    echo "ERROR: Packages not built. Run ./build_all_packages.sh first"
    exit 1
fi

# Check if twine is installed
if ! command -v twine &> /dev/null; then
    echo "Installing twine..."
    pip install --upgrade twine
fi

# Verify packages before upload
echo -e "\n🔍 Verifying packages..."
echo -e "\n[1/3] Checking luminoracore..."
twine check luminoracore/dist/*

echo -e "\n[2/3] Checking luminoracore-cli..."
twine check luminoracore-cli/dist/*

echo -e "\n[3/3] Checking luminoracore-sdk..."
twine check luminoracore-sdk-python/dist/*

echo -e "\n✅ All packages verified successfully!"

# Confirm with user
echo -e "\n==============================================="
echo "READY TO PUBLISH TO PyPI"
echo "==============================================="
echo -e "\nThis will make your packages available worldwide at:"
echo "  - https://pypi.org/project/luminoracore/"
echo "  - https://pypi.org/project/luminoracore-cli/"
echo "  - https://pypi.org/project/luminoracore-sdk/"
echo -e "\nUsers will install with:"
echo "  pip install luminoracore"
echo "  pip install luminoracore-cli"
echo "  pip install luminoracore-sdk"

echo -e "\n⚠️  IMPORTANT:"
echo "  - You need a PyPI account (https://pypi.org/account/register/)"
echo "  - Create API token at: https://pypi.org/manage/account/token/"
echo "  - You can only upload each version ONCE (can't overwrite)"

read -p $'\nDo you want to continue? (yes/no): ' confirm
if [ "$confirm" != "yes" ]; then
    echo -e "\n❌ Publication cancelled"
    exit 0
fi

# Upload to PyPI
echo -e "\n📤 Publishing to PyPI..."
echo -e "\nYou will be prompted for your PyPI credentials or token."
echo "(Username: __token__  Password: your-api-token)"

echo -e "\n[1/3] Publishing luminoracore..."
twine upload luminoracore/dist/*
echo "✅ luminoracore published!"

echo -e "\n[2/3] Publishing luminoracore-cli..."
twine upload luminoracore-cli/dist/*
echo "✅ luminoracore-cli published!"

echo -e "\n[3/3] Publishing luminoracore-sdk..."
twine upload luminoracore-sdk-python/dist/*
echo "✅ luminoracore-sdk published!"

# Success
echo -e "\n==============================================="
echo "🎉 PUBLISHED TO PyPI SUCCESSFULLY!"
echo "==============================================="

echo -e "\n🌐 Your packages are now live at:"
echo "  https://pypi.org/project/luminoracore/"
echo "  https://pypi.org/project/luminoracore-cli/"
echo "  https://pypi.org/project/luminoracore-sdk/"

echo -e "\n📦 Installation command:"
echo "  pip install luminoracore"
echo "  pip install luminoracore-cli"
echo "  pip install luminoracore-sdk"

echo -e "\n🚀 Next steps:"
echo "  1. Update README.md with PyPI badges"
echo "  2. Create GitHub Release (v1.0.0)"
echo "  3. Announce on social media"
echo "  4. Update documentation with pip install instructions"

echo -e "\n💡 Tip: It may take a few minutes for packages to appear in PyPI search"

