#!/bin/bash
# LuminoraCore - Complete Installation Script (Linux/Mac)
# Installs: Base Engine + CLI + SDK with all providers

set -e

echo "==============================================="
echo "LuminoraCore - Complete Installation (Linux/Mac)"
echo "==============================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# Check virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}⚠️  WARNING: No virtual environment detected${NC}"
    echo -e "${YELLOW}   Recommendation: Create and activate a virtual environment first${NC}"
    echo -e "${GRAY}   python -m venv venv${NC}"
    echo -e "${GRAY}   source venv/bin/activate${NC}"
    echo ""
    echo -e "${YELLOW}Continue anyway? (y/n)${NC}"
    read -r continue
    if [ "$continue" != "y" ] && [ "$continue" != "Y" ]; then
        echo -e "${RED}Installation cancelled.${NC}"
        exit 1
    fi
fi

# Function to install component
install_component() {
    local name=$1
    local path=$2
    local command=$3
    local description=$4
    
    echo -e "${GREEN}Installing $name...${NC}"
    echo -e "${GRAY}   $description${NC}"
    
    cd "$path" || return 1
    
    if eval "$command"; then
        echo -e "${GREEN}   ✅ $name installed successfully${NC}"
        cd - > /dev/null || return 1
        return 0
    else
        echo -e "${RED}   ❌ $name installation failed${NC}"
        cd - > /dev/null || return 1
        return 1
    fi
}

# Installation steps
success=true

echo -e "${YELLOW}Step 1: Installing Base Engine (luminoracore)...${NC}"
echo -e "${GRAY}⚠️  Linux/Mac: Using editable mode for development${NC}"
if ! install_component \
    "Base Engine" \
    "luminoracore" \
    "pip install -e ." \
    "Core personality management engine"; then
    success=false
fi

echo ""
echo -e "${YELLOW}Step 2: Installing CLI (luminoracore-cli)...${NC}"
if ! install_component \
    "CLI" \
    "luminoracore-cli" \
    "pip install -e ." \
    "Command-line interface"; then
    success=false
fi

echo ""
echo -e "${YELLOW}Step 3: Installing SDK (luminoracore-sdk-python)...${NC}"
echo -e "${GRAY}⚠️  CRITICAL: Installing with [all] to include all LLM providers${NC}"
if ! install_component \
    "SDK" \
    "luminoracore-sdk-python" \
    "pip install -e \".[all]\"" \
    "Python SDK with all providers"; then
    success=false
fi

echo ""
echo "==============================================="
echo "INSTALLATION SUMMARY"
echo "==============================================="

if [ "$success" = true ]; then
    echo -e "${GREEN}✅ ALL COMPONENTS INSTALLED SUCCESSFULLY${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "${GRAY}1. Run: python verify_installation.py${NC}"
    echo -e "${GRAY}2. Configure API keys if needed${NC}"
    echo -e "${GRAY}3. Test: luminoracore --help${NC}"
    echo -e "${GRAY}4. Read: QUICK_START.md${NC}"
else
    echo -e "${RED}❌ INSTALLATION FAILED${NC}"
    echo ""
    echo -e "${YELLOW}Troubleshooting:${NC}"
    echo -e "${GRAY}1. Make sure you're in a virtual environment${NC}"
    echo -e "${GRAY}2. Check INSTALLATION_GUIDE.md for detailed instructions${NC}"
    echo -e "${GRAY}3. Try manual installation step by step${NC}"
fi

echo ""

