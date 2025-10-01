#!/bin/bash

# Development setup script for LuminoraCore CLI
# Installs development dependencies and sets up the development environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up LuminoraCore CLI development environment...${NC}"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] || [ ! -d "luminoracore_cli" ]; then
    echo -e "${RED}Error: Please run this script from the luminoracore-cli root directory${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}Error: Python $REQUIRED_VERSION or higher is required. Found: $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}Python version check passed: $PYTHON_VERSION${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate || source venv/Scripts/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install development dependencies
echo -e "${YELLOW}Installing development dependencies...${NC}"
pip install -r requirements-dev.txt

# Install the package in development mode
echo -e "${YELLOW}Installing package in development mode...${NC}"
pip install -e .

# Install pre-commit hooks if available
if [ -f ".pre-commit-config.yaml" ]; then
    echo -e "${YELLOW}Installing pre-commit hooks...${NC}"
    pre-commit install
fi

# Create necessary directories
echo -e "${YELLOW}Creating development directories...${NC}"
mkdir -p tests/fixtures
mkdir -p tests/data
mkdir -p .cache
mkdir -p logs

# Set up git hooks if in a git repository
if [ -d ".git" ]; then
    echo -e "${YELLOW}Setting up git hooks...${NC}"
    
    # Create pre-commit hook
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Run tests before commit
echo "Running tests..."
python -m pytest tests/ -v
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi

# Run linting
echo "Running linting..."
python -m black --check luminoracore_cli/ tests/
python -m isort --check-only luminoracore_cli/ tests/
if [ $? -ne 0 ]; then
    echo "Linting failed. Run 'make format' to fix issues."
    exit 1
fi
EOF
    
    chmod +x .git/hooks/pre-commit
    echo -e "${GREEN}Git pre-commit hook installed${NC}"
fi

# Run initial tests
echo -e "${YELLOW}Running initial tests...${NC}"
python -m pytest tests/ -v || echo -e "${YELLOW}Some tests may have failed - this is normal for initial setup${NC}"

# Create development configuration
echo -e "${YELLOW}Creating development configuration...${NC}"
cat > .env.dev << EOF
# Development environment variables
LUMINORA_CORE_API_URL=http://localhost:8000
LUMINORA_CORE_API_KEY=dev-key
LUMINORA_CORE_CACHE_DIR=.cache
LUMINORA_CORE_LOG_LEVEL=DEBUG
LUMINORA_CORE_TIMEOUT=30
EOF

echo -e "${GREEN}Development environment setup complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo -e "1. Activate the virtual environment: ${YELLOW}source venv/bin/activate${NC}"
echo -e "2. Run tests: ${YELLOW}make test${NC}"
echo -e "3. Run linting: ${YELLOW}make lint${NC}"
echo -e "4. Format code: ${YELLOW}make format${NC}"
echo -e "5. Install completions: ${YELLOW}./scripts/install-completions.sh${NC}"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
