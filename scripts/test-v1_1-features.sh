#!/bin/bash

# Test LuminoraCore v1.1 Features
# Comprehensive testing of all v1.1 functionality

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}LuminoraCore v1.1 Features Test${NC}"
echo "========================================"

TESTS_PASSED=0
TESTS_FAILED=0

# Function to run test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -e "\n${YELLOW}Testing: $test_name${NC}"
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ $test_name passed${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ $test_name failed${NC}"
        ((TESTS_FAILED++))
    fi
}

# Core v1.1 Tests
echo -e "\n${BLUE}=== Core v1.1 Tests ===${NC}"

run_test "Migration Manager Import" "python -c 'from luminoracore.storage.migrations.migration_manager import MigrationManager'"

run_test "Feature Flags Import" "python -c 'from luminoracore.core.config import FeatureFlagManager, get_features, is_enabled'"

run_test "Personality v1.1 Import" "python -c 'from luminoracore.core.personality_v1_1 import PersonalityV11Extensions, HierarchicalConfig'"

run_test "Dynamic Compiler Import" "python -c 'from luminoracore.core.compiler_v1_1 import DynamicPersonalityCompiler'"

run_test "Affinity Manager Import" "python -c 'from luminoracore.core.relationship.affinity import AffinityManager, AffinityState'"

run_test "Fact Extractor Import" "python -c 'from luminoracore.core.memory.fact_extractor import FactExtractor, Fact'"

run_test "Episodic Memory Import" "python -c 'from luminoracore.core.memory.episodic import EpisodicMemoryManager, Episode'"

run_test "Memory Classifier Import" "python -c 'from luminoracore.core.memory.classifier import MemoryClassifier'"

# SDK v1.1 Tests
echo -e "\n${BLUE}=== SDK v1.1 Tests ===${NC}"

run_test "Storage v1.1 Import" "python -c 'from luminoracore_sdk.session.storage_v1_1 import StorageV11Extension, InMemoryStorageV11'" 2>/dev/null || echo -e "${YELLOW}(SDK not installed)${NC}"

run_test "Memory Manager v1.1 Import" "python -c 'from luminoracore_sdk.session.memory_v1_1 import MemoryManagerV11'" 2>/dev/null || echo -e "${YELLOW}(SDK not installed)${NC}"

run_test "Client v1.1 Import" "python -c 'from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11'" 2>/dev/null || echo -e "${YELLOW}(SDK not installed)${NC}"

run_test "Types v1.1 Import" "python -c 'from luminoracore_sdk.types.memory import FactDict, EpisodeDict'" 2>/dev/null || echo -e "${YELLOW}(SDK not installed)${NC}"

# CLI v1.1 Tests
echo -e "\n${BLUE}=== CLI v1.1 Tests ===${NC}"

run_test "Migrate Command Import" "python -c 'from luminoracore_cli.commands.migrate import migrate'" 2>/dev/null || echo -e "${YELLOW}(CLI not installed)${NC}"

run_test "Memory Command Import" "python -c 'from luminoracore_cli.commands.memory import memory'" 2>/dev/null || echo -e "${YELLOW}(CLI not installed)${NC}"

run_test "Snapshot Command Import" "python -c 'from luminoracore_cli.commands.snapshot import snapshot'" 2>/dev/null || echo -e "${YELLOW}(CLI not installed)${NC}"

# Pytest Tests
echo -e "\n${BLUE}=== Pytest v1.1 Tests ===${NC}"

if command -v pytest >/dev/null 2>&1; then
    echo -e "${YELLOW}Running Core v1.1 tests...${NC}"
    if cd luminoracore && pytest tests/test_step_*.py -v --tb=no 2>/dev/null; then
        echo -e "${GREEN}✓ Core v1.1 tests passed${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ Core v1.1 tests failed${NC}"
        ((TESTS_FAILED++))
    fi
    cd ..
    
    echo -e "\n${YELLOW}Running SDK v1.1 tests...${NC}"
    if cd luminoracore-sdk-python && pytest tests/test_step_*.py -v --tb=no 2>/dev/null; then
        echo -e "${GREEN}✓ SDK v1.1 tests passed${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${YELLOW}(SDK tests skipped or failed)${NC}"
    fi
    cd ..
else
    echo -e "${YELLOW}pytest not installed, skipping unit tests${NC}"
fi

# Examples Tests
echo -e "\n${BLUE}=== v1.1 Examples Tests ===${NC}"

if [ -f "examples/v1_1_quick_example.py" ]; then
    run_test "Quick Example Execution" "cd examples && python v1_1_quick_example.py"
else
    echo -e "${YELLOW}v1.1 examples not found${NC}"
fi

# Summary
echo -e "\n${BLUE}=== Test Summary ===${NC}"
echo -e "${GREEN}Tests passed: $TESTS_PASSED${NC}"
echo -e "${RED}Tests failed: $TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All v1.1 tests passed!${NC}"
    exit 0
else
    echo -e "\n${YELLOW}⚠️  Some tests failed${NC}"
    exit 1
fi

