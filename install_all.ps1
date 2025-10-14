# LuminoraCore - Complete Installation Script (Windows)
# Installs: Base Engine + CLI + SDK with all providers

$ErrorActionPreference = "Stop"

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "LuminoraCore - Complete Installation (Windows)" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Check virtual environment
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  WARNING: No virtual environment detected" -ForegroundColor Yellow
    Write-Host "   Recommendation: Create and activate a virtual environment first" -ForegroundColor Yellow
    Write-Host "   python -m venv venv" -ForegroundColor Gray
    Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Continue anyway? (y/n)" -ForegroundColor Yellow
    $continue = Read-Host
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        Write-Host "Installation cancelled." -ForegroundColor Red
        exit 1
    }
}

# Function to install component
function Install-Component {
    param(
        [string]$Name,
        [string]$Path,
        [string]$Command,
        [string]$Description
    )
    
    Write-Host "Installing $Name..." -ForegroundColor Green
    Write-Host "   $Description" -ForegroundColor Gray
    
    Push-Location $Path
    
    try {
        Invoke-Expression $Command
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ $Name installed successfully" -ForegroundColor Green
            return $true
        } else {
            Write-Host "   ❌ $Name installation failed" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "   ❌ Error installing $Name`: $_" -ForegroundColor Red
        return $false
    }
    finally {
        Pop-Location
    }
}

# Installation steps
$success = $true

Write-Host "Step 1: Installing Base Engine (luminoracore)..." -ForegroundColor Yellow
Write-Host "⚠️  Windows: Using normal mode (not editable) to avoid permission issues" -ForegroundColor Gray
$success = $success -and (Install-Component `
    -Name "Base Engine" `
    -Path "luminoracore" `
    -Command "pip install ." `
    -Description "Core personality management engine")

Write-Host "`nStep 2: Installing CLI (luminoracore-cli)..." -ForegroundColor Yellow
$success = $success -and (Install-Component `
    -Name "CLI" `
    -Path "luminoracore-cli" `
    -Command "pip install ." `
    -Description "Command-line interface")

Write-Host "`nStep 3: Installing SDK (luminoracore-sdk-python)..." -ForegroundColor Yellow
Write-Host "⚠️  CRITICAL: Installing with [all] to include all LLM providers" -ForegroundColor Gray
$success = $success -and (Install-Component `
    -Name "SDK" `
    -Path "luminoracore-sdk-python" `
    -Command "pip install `".[all]`"" `
    -Description "Python SDK with all providers")

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "INSTALLATION SUMMARY" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

if ($success) {
    Write-Host "✅ ALL COMPONENTS INSTALLED SUCCESSFULLY" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Setup v1.1 database: .\scripts\setup-v1_1-database.ps1" -ForegroundColor Gray
    Write-Host "2. Verify installation: python verify_installation.py" -ForegroundColor Gray
    Write-Host "3. Verify v1.1: .\scripts\verify-v1_1-installation.ps1" -ForegroundColor Gray
    Write-Host "4. Configure API keys if needed" -ForegroundColor Gray
    Write-Host "5. Test: luminoracore --help" -ForegroundColor Gray
    Write-Host "6. Test v1.1: python examples\v1_1_quick_example.py" -ForegroundColor Gray
    Write-Host "7. Read: QUICK_START.md and mejoras_v1.1\QUICK_START_V1_1.md" -ForegroundColor Gray
} else {
    Write-Host "❌ INSTALLATION FAILED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Make sure you're in a virtual environment" -ForegroundColor Gray
    Write-Host "2. Try running PowerShell as Administrator" -ForegroundColor Gray
    Write-Host "3. Check INSTALLATION_GUIDE.md for detailed instructions" -ForegroundColor Gray
}

Write-Host ""

