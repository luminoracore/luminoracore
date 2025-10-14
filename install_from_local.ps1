# Install LuminoraCore from local wheels
# Use this to test the packages before publishing to PyPI

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "LuminoraCore Local Installer" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# Check if releases directory exists
if (-not (Test-Path "releases")) {
    Write-Error "No releases directory found. Run .\build_all_packages.ps1 first"
    exit 1
}

# Find wheel files
$coreWheel = Get-ChildItem releases/luminoracore-*.whl | Where-Object { $_.Name -notmatch "cli|sdk" } | Select-Object -First 1
$cliWheel = Get-ChildItem releases/luminoracore*cli*.whl | Select-Object -First 1
$sdkWheel = Get-ChildItem releases/luminoracore*sdk*.whl | Select-Object -First 1

if (-not $coreWheel -or -not $cliWheel -or -not $sdkWheel) {
    Write-Error "Wheel files not found. Run .\build_all_packages.ps1 first"
    exit 1
}

Write-Host "`n📦 Found packages:" -ForegroundColor Yellow
Write-Host "  - $($coreWheel.Name)" -ForegroundColor Gray
Write-Host "  - $($cliWheel.Name)" -ForegroundColor Gray
Write-Host "  - $($sdkWheel.Name)" -ForegroundColor Gray

# Uninstall existing versions
Write-Host "`n🧹 Uninstalling existing versions..." -ForegroundColor Yellow
pip uninstall -y luminoracore luminoracore-cli luminoracore-sdk 2>$null

# Install from wheels
Write-Host "`n📥 Installing from local wheels..." -ForegroundColor Yellow

Write-Host "`n[1/3] Installing luminoracore..." -ForegroundColor Cyan
pip install $coreWheel.FullName
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install luminoracore"
    exit 1
}

Write-Host "`n[2/3] Installing luminoracore-cli..." -ForegroundColor Cyan
pip install $cliWheel.FullName
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install luminoracore-cli"
    exit 1
}

Write-Host "`n[3/3] Installing luminoracore-sdk..." -ForegroundColor Cyan
pip install "$($sdkWheel.FullName)[all]"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install luminoracore-sdk"
    exit 1
}

# Verify installation
Write-Host "`n===============================================" -ForegroundColor Cyan
Write-Host "INSTALLATION COMPLETE" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan

Write-Host "`n✅ Verifying installation..." -ForegroundColor Yellow
pip show luminoracore luminoracore-cli luminoracore-sdk

Write-Host "`n🧪 Test the installation:" -ForegroundColor White
Write-Host "  luminoracore --version" -ForegroundColor Gray
Write-Host "  luminoracore list" -ForegroundColor Gray
Write-Host "  python verify_installation.py" -ForegroundColor Gray

Write-Host "`n✅ Installation successful!" -ForegroundColor Green
Write-Host "If everything works, you can publish to PyPI: .\publish_to_pypi.ps1" -ForegroundColor Cyan

