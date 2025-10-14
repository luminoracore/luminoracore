# Publish LuminoraCore to PyPI
# Make the packages available worldwide via: pip install luminoracore

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "LuminoraCore PyPI Publisher" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# Check if packages are built
if (-not (Test-Path "luminoracore/dist") -or 
    -not (Test-Path "luminoracore-cli/dist") -or 
    -not (Test-Path "luminoracore-sdk-python/dist")) {
    Write-Error "Packages not built. Run .\build_all_packages.ps1 first"
    exit 1
}

# Check if twine is installed
if (-not (Get-Command twine -ErrorAction SilentlyContinue)) {
    Write-Host "Installing twine..." -ForegroundColor Yellow
    pip install --upgrade twine
}

# Verify packages before upload
Write-Host "`n🔍 Verifying packages..." -ForegroundColor Yellow
Write-Host "`n[1/3] Checking luminoracore..." -ForegroundColor Cyan
twine check luminoracore/dist/*
if ($LASTEXITCODE -ne 0) {
    Write-Error "luminoracore package verification failed"
    exit 1
}

Write-Host "`n[2/3] Checking luminoracore-cli..." -ForegroundColor Cyan
twine check luminoracore-cli/dist/*
if ($LASTEXITCODE -ne 0) {
    Write-Error "luminoracore-cli package verification failed"
    exit 1
}

Write-Host "`n[3/3] Checking luminoracore-sdk..." -ForegroundColor Cyan
twine check luminoracore-sdk-python/dist/*
if ($LASTEXITCODE -ne 0) {
    Write-Error "luminoracore-sdk package verification failed"
    exit 1
}

Write-Host "`n✅ All packages verified successfully!" -ForegroundColor Green

# Confirm with user
Write-Host "`n===============================================" -ForegroundColor Yellow
Write-Host "READY TO PUBLISH TO PyPI" -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Yellow
Write-Host "`nThis will make your packages available worldwide at:" -ForegroundColor White
Write-Host "  - https://pypi.org/project/luminoracore/" -ForegroundColor Cyan
Write-Host "  - https://pypi.org/project/luminoracore-cli/" -ForegroundColor Cyan
Write-Host "  - https://pypi.org/project/luminoracore-sdk/" -ForegroundColor Cyan
Write-Host "`nUsers will install with:" -ForegroundColor White
Write-Host "  pip install luminoracore" -ForegroundColor Gray
Write-Host "  pip install luminoracore-cli" -ForegroundColor Gray
Write-Host "  pip install luminoracore-sdk" -ForegroundColor Gray

Write-Host "`n⚠️  IMPORTANT:" -ForegroundColor Red
Write-Host "  - You need a PyPI account (https://pypi.org/account/register/)" -ForegroundColor Yellow
Write-Host "  - Create API token at: https://pypi.org/manage/account/token/" -ForegroundColor Yellow
Write-Host "  - You can only upload each version ONCE (can't overwrite)" -ForegroundColor Yellow

$confirm = Read-Host "`nDo you want to continue? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "`n❌ Publication cancelled" -ForegroundColor Red
    exit 0
}

# Upload to PyPI
Write-Host "`n📤 Publishing to PyPI..." -ForegroundColor Cyan
Write-Host "`nYou will be prompted for your PyPI credentials or token." -ForegroundColor Yellow
Write-Host "(Username: __token__  Password: your-api-token)" -ForegroundColor Gray

Write-Host "`n[1/3] Publishing luminoracore..." -ForegroundColor Cyan
twine upload luminoracore/dist/*
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to publish luminoracore"
    exit 1
}
Write-Host "✅ luminoracore published!" -ForegroundColor Green

Write-Host "`n[2/3] Publishing luminoracore-cli..." -ForegroundColor Cyan
twine upload luminoracore-cli/dist/*
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to publish luminoracore-cli"
    exit 1
}
Write-Host "✅ luminoracore-cli published!" -ForegroundColor Green

Write-Host "`n[3/3] Publishing luminoracore-sdk..." -ForegroundColor Cyan
twine upload luminoracore-sdk-python/dist/*
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to publish luminoracore-sdk"
    exit 1
}
Write-Host "✅ luminoracore-sdk published!" -ForegroundColor Green

# Success
Write-Host "`n===============================================" -ForegroundColor Cyan
Write-Host "🎉 PUBLISHED TO PyPI SUCCESSFULLY!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan

Write-Host "`n🌐 Your packages are now live at:" -ForegroundColor White
Write-Host "  https://pypi.org/project/luminoracore/" -ForegroundColor Cyan
Write-Host "  https://pypi.org/project/luminoracore-cli/" -ForegroundColor Cyan
Write-Host "  https://pypi.org/project/luminoracore-sdk/" -ForegroundColor Cyan

Write-Host "`n📦 Installation command:" -ForegroundColor White
Write-Host "  pip install luminoracore" -ForegroundColor Gray
Write-Host "  pip install luminoracore-cli" -ForegroundColor Gray
Write-Host "  pip install luminoracore-sdk" -ForegroundColor Gray

Write-Host "`n🚀 Next steps:" -ForegroundColor White
Write-Host "  1. Update README.md with PyPI badges" -ForegroundColor Gray
Write-Host "  2. Create GitHub Release (v1.0.0)" -ForegroundColor Gray
Write-Host "  3. Announce on social media" -ForegroundColor Gray
Write-Host "  4. Update documentation with pip install instructions" -ForegroundColor Gray

Write-Host "`n💡 Tip: It may take a few minutes for packages to appear in PyPI search" -ForegroundColor Yellow

