# Build All LuminoraCore Packages
# Creates .whl files for distribution

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "LuminoraCore Package Builder" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# Check if build tools are installed
Write-Host "`nChecking dependencies..." -ForegroundColor Yellow
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Error "pip not found. Please install Python."
    exit 1
}

# Install build tools if needed
Write-Host "Installing/upgrading build tools..." -ForegroundColor Yellow
pip install --upgrade build twine wheel setuptools

# Clean previous builds
Write-Host "`nCleaning previous builds..." -ForegroundColor Yellow
$components = @("luminoracore", "luminoracore-cli", "luminoracore-sdk-python")
foreach ($component in $components) {
    if (Test-Path "$component/dist") {
        Remove-Item -Recurse -Force "$component/dist"
    }
    if (Test-Path "$component/build") {
        Remove-Item -Recurse -Force "$component/build"
    }
    if (Test-Path "$component/*.egg-info") {
        Remove-Item -Recurse -Force "$component/*.egg-info"
    }
}

# Build packages
Write-Host "`n===============================================" -ForegroundColor Cyan
Write-Host "Building packages..." -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# 1. Build luminoracore (base engine)
Write-Host "`n[1/3] Building luminoracore (Base Engine)..." -ForegroundColor Yellow
cd luminoracore
python -m build
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to build luminoracore"
    exit 1
}
Write-Host "✅ luminoracore built successfully" -ForegroundColor Green
cd ..

# 2. Build luminoracore-cli
Write-Host "`n[2/3] Building luminoracore-cli..." -ForegroundColor Yellow
cd luminoracore-cli
python -m build
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to build luminoracore-cli"
    exit 1
}
Write-Host "✅ luminoracore-cli built successfully" -ForegroundColor Green
cd ..

# 3. Build luminoracore-sdk-python
Write-Host "`n[3/3] Building luminoracore-sdk-python..." -ForegroundColor Yellow
cd luminoracore-sdk-python
python -m build
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to build luminoracore-sdk-python"
    exit 1
}
Write-Host "✅ luminoracore-sdk built successfully" -ForegroundColor Green
cd ..

# Create releases directory
Write-Host "`nOrganizing releases..." -ForegroundColor Yellow
$releasesDir = "releases"
if (-not (Test-Path $releasesDir)) {
    New-Item -ItemType Directory -Path $releasesDir | Out-Null
}

# Copy all wheels to releases
Copy-Item luminoracore/dist/*.whl $releasesDir/
Copy-Item luminoracore-cli/dist/*.whl $releasesDir/
Copy-Item luminoracore-sdk-python/dist/*.whl $releasesDir/

# Copy source distributions too
Copy-Item luminoracore/dist/*.tar.gz $releasesDir/ -ErrorAction SilentlyContinue
Copy-Item luminoracore-cli/dist/*.tar.gz $releasesDir/ -ErrorAction SilentlyContinue
Copy-Item luminoracore-sdk-python/dist/*.tar.gz $releasesDir/ -ErrorAction SilentlyContinue

# Summary
Write-Host "`n===============================================" -ForegroundColor Cyan
Write-Host "BUILD COMPLETE" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan

Write-Host "`n📦 Packages created:" -ForegroundColor White
Get-ChildItem $releasesDir/*.whl | ForEach-Object {
    $size = [math]::Round($_.Length / 1MB, 2)
    Write-Host "  ✅ $($_.Name) ($size MB)" -ForegroundColor Green
}

Write-Host "`n📁 Location: $releasesDir/" -ForegroundColor Cyan
Write-Host "`n🚀 Next steps:" -ForegroundColor White
Write-Host "  1. Test locally: .\install_from_local.ps1" -ForegroundColor Gray
Write-Host "  2. Publish to PyPI: .\publish_to_pypi.ps1" -ForegroundColor Gray

Write-Host "`n💡 To install in another project:" -ForegroundColor White
Write-Host "  pip install path/to/releases/luminoracore-*.whl" -ForegroundColor Gray

