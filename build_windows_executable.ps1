# Build Windows Executable for LuminoraCore CLI
# This creates a standalone .exe that doesn't require Python

Write-Host "Building LuminoraCore CLI Windows Executable..." -ForegroundColor Cyan

# Check if PyInstaller is installed
if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
}

# Navigate to CLI directory
cd luminoracore-cli

# Build executable
Write-Host "Creating standalone executable..." -ForegroundColor Yellow
pyinstaller `
    --onefile `
    --name luminoracore `
    --console `
    --icon=NONE `
    luminoracore_cli/main.py

Write-Host "`n✅ Build complete!" -ForegroundColor Green
Write-Host "Executable location: luminoracore-cli/dist/luminoracore.exe" -ForegroundColor Cyan
Write-Host "Size: ~30-40 MB" -ForegroundColor Gray

# Move to releases folder
$releasesDir = "../releases"
if (-not (Test-Path $releasesDir)) {
    New-Item -ItemType Directory -Path $releasesDir | Out-Null
}

Copy-Item dist/luminoracore.exe "$releasesDir/luminoracore-cli-v1.0.0-windows.exe"
Write-Host "`n✅ Copied to: releases/luminoracore-cli-v1.0.0-windows.exe" -ForegroundColor Green
Write-Host "`nUsers can now double-click this .exe (no Python required!)" -ForegroundColor Cyan

