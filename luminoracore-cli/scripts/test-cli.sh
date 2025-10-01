#!/bin/bash

# Test script for LuminoraCore CLI
# Runs comprehensive tests to verify CLI functionality

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Running LuminoraCore CLI tests...${NC}"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] || [ ! -d "luminoracore_cli" ]; then
    echo -e "${RED}Error: Please run this script from the luminoracore-cli root directory${NC}"
    exit 1
fi

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -e "${YELLOW}Running: $test_name${NC}"
    
    if eval "$test_command"; then
        echo -e "${GREEN}✓ $test_name passed${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ $test_name failed${NC}"
        ((TESTS_FAILED++))
    fi
    echo ""
}

# Test 1: Check if CLI can be imported
run_test "Import Test" "python -c 'import luminoracore_cli; print(\"CLI imported successfully\")'"

# Test 2: Check if main module can be imported
run_test "Main Module Import" "python -c 'from luminoracore_cli.main import app; print(\"Main module imported successfully\")'"

# Test 3: Check CLI help
run_test "CLI Help" "python -m luminoracore_cli --help"

# Test 4: Check version
run_test "Version Check" "python -m luminoracore_cli --version"

# Test 5: Check validate command help
run_test "Validate Command Help" "python -m luminoracore_cli validate --help"

# Test 6: Check compile command help
run_test "Compile Command Help" "python -m luminoracore_cli compile --help"

# Test 7: Check create command help
run_test "Create Command Help" "python -m luminoracore_cli create --help"

# Test 8: Check list command help
run_test "List Command Help" "python -m luminoracore_cli list --help"

# Test 9: Check test command help
run_test "Test Command Help" "python -m luminoracore_cli test --help"

# Test 10: Check serve command help
run_test "Serve Command Help" "python -m luminoracore_cli serve --help"

# Test 11: Check blend command help
run_test "Blend Command Help" "python -m luminoracore_cli blend --help"

# Test 12: Check update command help
run_test "Update Command Help" "python -m luminoracore_cli update --help"

# Test 13: Check init command help
run_test "Init Command Help" "python -m luminoracore_cli init --help"

# Test 14: Check info command help
run_test "Info Command Help" "python -m luminoracore_cli info --help"

# Test 15: Test list command (should work even without personalities)
run_test "List Command Execution" "python -m luminoracore_cli list"

# Test 16: Test init command (should create project structure)
echo -e "${YELLOW}Testing init command...${NC}"
TEST_DIR="test_project_$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

if python -m luminoracore_cli init --name "test-project" --template basic --non-interactive; then
    echo -e "${GREEN}✓ Init command passed${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ Init command failed${NC}"
    ((TESTS_FAILED++))
fi

cd ..
rm -rf "$TEST_DIR"
echo ""

# Test 17: Check if templates are accessible
run_test "Templates Access" "python -c 'from luminoracore_cli.templates import get_all_templates; templates = get_all_templates(); print(f\"Found {len(templates)} templates\")'"

# Test 18: Check configuration loading
run_test "Configuration Loading" "python -c 'from luminoracore_cli.config import load_settings; settings = load_settings(); print(\"Configuration loaded successfully\")'"

# Test 19: Check utility functions
run_test "Utility Functions" "python -c 'from luminoracore_cli.utils import console, HTTPClient; print(\"Utility functions imported successfully\")'"

# Test 20: Check core modules
run_test "Core Modules" "python -c 'from luminoracore_cli.core import LuminoraCoreClient, PersonalityValidator; print(\"Core modules imported successfully\")'"

# Test 21: Check server module
run_test "Server Module" "python -c 'from luminoracore_cli.server import create_app; print(\"Server module imported successfully\")'"

# Test 22: Run pytest if available
if command -v pytest >/dev/null 2>&1; then
    echo -e "${YELLOW}Running pytest tests...${NC}"
    if pytest tests/ -v; then
        echo -e "${GREEN}✓ Pytest tests passed${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ Pytest tests failed${NC}"
        ((TESTS_FAILED++))
    fi
    echo ""
else
    echo -e "${YELLOW}Skipping pytest tests (pytest not installed)${NC}"
    echo ""
fi

# Test 23: Check code formatting with black
if command -v black >/dev/null 2>&1; then
    echo -e "${YELLOW}Checking code formatting...${NC}"
    if black --check luminoracore_cli/ tests/; then
        echo -e "${GREEN}✓ Code formatting is correct${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ Code formatting issues found${NC}"
        ((TESTS_FAILED++))
    fi
    echo ""
else
    echo -e "${YELLOW}Skipping code formatting check (black not installed)${NC}"
    echo ""
fi

# Test 24: Check import sorting with isort
if command -v isort >/dev/null 2>&1; then
    echo -e "${YELLOW}Checking import sorting...${NC}"
    if isort --check-only luminoracore_cli/ tests/; then
        echo -e "${GREEN}✓ Import sorting is correct${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ Import sorting issues found${NC}"
        ((TESTS_FAILED++))
    fi
    echo ""
else
    echo -e "${YELLOW}Skipping import sorting check (isort not installed)${NC}"
    echo ""
fi

# Test 25: Check type hints with mypy
if command -v mypy >/dev/null 2>&1; then
    echo -e "${YELLOW}Checking type hints...${NC}"
    if mypy luminoracore_cli/ --ignore-missing-imports; then
        echo -e "${GREEN}✓ Type hints are correct${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ Type hint issues found${NC}"
        ((TESTS_FAILED++))
    fi
    echo ""
else
    echo -e "${YELLOW}Skipping type hints check (mypy not installed)${NC}"
    echo ""
fi

# Summary
echo -e "${BLUE}=== Test Summary ===${NC}"
echo -e "${GREEN}Tests passed: $TESTS_PASSED${NC}"
echo -e "${RED}Tests failed: $TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please check the output above.${NC}"
    exit 1
fi
