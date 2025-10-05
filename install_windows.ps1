# LuminoraCore Windows Installation Script
# This script handles Windows-specific installation issues

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "LUMINORACORE WINDOWS INSTALLATION" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in a virtual environment
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  WARNING: No virtual environment detected" -ForegroundColor Yellow
    Write-Host "   Recommendation: Create and activate a virtual environment first" -ForegroundColor Yellow
    Write-Host "   python -m venv venv" -ForegroundColor Gray
    Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host ""
}

# Function to install with error handling
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
        # For Windows, use normal installation to avoid permission issues
        if ($Command -like "*pip install -e*") {
            $Command = $Command -replace "pip install -e", "pip install"
        }
        
        Invoke-Expression $Command
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ $Name installed successfully" -ForegroundColor Green
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
    
    return $true
}

# Installation steps
$success = $true

Write-Host "Step 1: Installing Base Engine (luminoracore)..." -ForegroundColor Yellow
$success = $success -and (Install-Component -Name "Base Engine" -Path "luminoracore" -Command "pip install ." -Description "Core personality management engine")

Write-Host "Step 2: Installing CLI (luminoracore-cli)..." -ForegroundColor Yellow
$success = $success -and (Install-Component -Name "CLI" -Path "luminoracore-cli" -Command "pip install ." -Description "Command-line interface")

Write-Host "Step 3: Installing SDK (luminoracore-sdk-python)..." -ForegroundColor Yellow
$success = $success -and (Install-Component -Name "SDK" -Path "luminoracore-sdk-python" -Command "pip install `".[all]`" -Description "Python SDK with all providers")

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "INSTALLATION SUMMARY" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

if ($success) {
    Write-Host "✅ ALL COMPONENTS INSTALLED SUCCESSFULLY" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Run: python verify_installation.py" -ForegroundColor Gray
    Write-Host "2. Configure API keys if needed" -ForegroundColor Gray
    Write-Host "3. Test: luminoracore --help" -ForegroundColor Gray
} else {
    Write-Host "❌ INSTALLATION FAILED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Make sure you're in a virtual environment" -ForegroundColor Gray
    Write-Host "2. Try running PowerShell as Administrator" -ForegroundColor Gray
    Write-Host "3. Check INSTALLATION_GUIDE.md for detailed instructions" -ForegroundColor Gray
}

Write-Host ""
