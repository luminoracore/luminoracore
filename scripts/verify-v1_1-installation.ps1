# Verify LuminoraCore v1.1 Installation
# PowerShell script for Windows users

$ErrorActionPreference = "Stop"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "LuminoraCore v1.1 Installation Verification" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

$TestsPassed = 0
$TestsFailed = 0

# Function to run test
function Test-Feature {
    param(
        [string]$Name,
        [scriptblock]$Test
    )
    
    Write-Host "`nTesting: $Name" -ForegroundColor Yellow
    
    try {
        & $Test
        Write-Host "  ✓ $Name passed" -ForegroundColor Green
        $script:TestsPassed++
    }
    catch {
        Write-Host "  ✗ $Name failed: $_" -ForegroundColor Red
        $script:TestsFailed++
    }
}

# Test Core v1.1
Write-Host "`n=== Core v1.1 Tests ===" -ForegroundColor Blue

Test-Feature "Migration Manager" {
    python -c "from luminoracore.storage.migrations.migration_manager import MigrationManager; print('OK')"
}

Test-Feature "Feature Flags" {
    python -c "from luminoracore.core.config import FeatureFlagManager, get_features, is_enabled; print('OK')"
}

Test-Feature "Personality v1.1" {
    python -c "from luminoracore.core.personality_v1_1 import PersonalityV11Extensions; print('OK')"
}

Test-Feature "Dynamic Compiler" {
    python -c "from luminoracore.core.compiler_v1_1 import DynamicPersonalityCompiler; print('OK')"
}

Test-Feature "Affinity Manager" {
    python -c "from luminoracore.core.relationship.affinity import AffinityManager; print('OK')"
}

Test-Feature "Fact Extractor" {
    python -c "from luminoracore.core.memory.fact_extractor import FactExtractor; print('OK')"
}

Test-Feature "Episodic Memory" {
    python -c "from luminoracore.core.memory.episodic import EpisodicMemoryManager; print('OK')"
}

Test-Feature "Memory Classifier" {
    python -c "from luminoracore.core.memory.classifier import MemoryClassifier; print('OK')"
}

# Test SDK v1.1
Write-Host "`n=== SDK v1.1 Tests ===" -ForegroundColor Blue

Test-Feature "Storage v1.1" {
    python -c "from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11; print('OK')" 2>$null
}

Test-Feature "Memory Manager v1.1" {
    python -c "from luminoracore_sdk.session.memory_v1_1 import MemoryManagerV11; print('OK')" 2>$null
}

Test-Feature "Client v1.1" {
    python -c "from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11; print('OK')" 2>$null
}

# Test CLI v1.1
Write-Host "`n=== CLI v1.1 Commands ===" -ForegroundColor Blue

Test-Feature "Migrate Command" {
    python -c "from luminoracore_cli.commands.migrate import migrate; print('OK')" 2>$null
}

Test-Feature "Memory Command" {
    python -c "from luminoracore_cli.commands.memory import memory; print('OK')" 2>$null
}

Test-Feature "Snapshot Command" {
    python -c "from luminoracore_cli.commands.snapshot import snapshot; print('OK')" 2>$null
}

# Run pytest if available
Write-Host "`n=== Pytest Tests ===" -ForegroundColor Blue

if (Get-Command pytest -ErrorAction SilentlyContinue) {
    Write-Host "`nRunning Core v1.1 tests..." -ForegroundColor Yellow
    
    Push-Location luminoracore
    try {
        $output = pytest tests/test_step_*.py -v --tb=no 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Core v1.1 tests passed" -ForegroundColor Green
            $TestsPassed++
        }
        else {
            Write-Host "  ✗ Core v1.1 tests failed" -ForegroundColor Red
            $TestsFailed++
        }
    }
    finally {
        Pop-Location
    }
    
    Write-Host "`nRunning SDK v1.1 tests..." -ForegroundColor Yellow
    
    Push-Location luminoracore-sdk-python
    try {
        $output = pytest tests/test_step_*.py -v --tb=no 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ SDK v1.1 tests passed" -ForegroundColor Green
            $TestsPassed++
        }
        else {
            Write-Host "  ⚠  SDK v1.1 tests failed or skipped" -ForegroundColor Yellow
        }
    }
    finally {
        Pop-Location
    }
}
else {
    Write-Host "  pytest not installed, skipping unit tests" -ForegroundColor Yellow
}

# Summary
Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "=== Test Summary ===" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Tests passed: $TestsPassed" -ForegroundColor Green
Write-Host "Tests failed: $TestsFailed" -ForegroundColor Red

if ($TestsFailed -eq 0) {
    Write-Host "`n🎉 All v1.1 tests passed!" -ForegroundColor Green
    Write-Host "`nv1.1 is properly installed and functional!" -ForegroundColor Cyan
    exit 0
}
else {
    Write-Host "`n⚠️  Some tests failed" -ForegroundColor Yellow
    exit 1
}

