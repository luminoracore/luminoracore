# Scripts

This directory contains essential utility scripts for LuminoraCore v1.1.

## Available Scripts

### Installation & Setup

#### `setup-v1_1-database.ps1`
**Purpose:** Initialize and migrate v1.1 database tables

**Usage:**
```powershell
# Use default database (luminora.db)
.\scripts\setup-v1_1-database.ps1

# Specify custom database path
.\scripts\setup-v1_1-database.ps1 -DatabasePath "C:\path\to\database.db"
```

**What it does:**
- Checks Core installation
- Runs v1.1 migrations
- Verifies table creation
- Shows migration status

**Prerequisites:**
- `luminoracore` installed
- Migration files in place

---

#### `verify-v1_1-installation.ps1`
**Purpose:** Verify complete LuminoraCore v1.1 installation

**Usage:**
```powershell
.\scripts\verify-v1_1-installation.ps1
```

**What it verifies:**
- Core v1.1 installation
- SDK v1.1 installation
- CLI v1.1 installation
- All dependencies
- Basic functionality

**Output:**
- Pass/fail for each component
- Summary statistics
- Exit code 0 if all pass

---

## Quick Reference

### First Time Setup
```powershell
# 1. Verify installation
.\scripts\verify-v1_1-installation.ps1

# 2. Setup database
.\scripts\setup-v1_1-database.ps1
```

### Troubleshooting
```powershell
# Check installation status
.\scripts\verify-v1_1-installation.ps1

# Reset database
.\scripts\setup-v1_1-database.ps1 -Force
```

---

## Platform Support

| Script | Windows | Linux | macOS |
|--------|---------|-------|-------|
| setup-v1_1-database.ps1 | ✅ | ❌ | ❌ |
| verify-v1_1-installation.ps1 | ✅ | ❌ | ❌ |

**Note:** PowerShell scripts are Windows-specific. For Linux/macOS, use the equivalent shell scripts in the project root.

---

## Exit Codes

All scripts follow standard exit codes:
- `0` - Success
- `1` - Error

---

## Troubleshooting

### "Execution Policy" Error
```powershell
# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Module not found" Error
```powershell
# Install all components
pip install -e luminoracore/
pip install -e luminoracore-cli/
pip install -e luminoracore-sdk-python/
```

### "Database locked" Error
```powershell
# Force database reset
.\scripts\setup-v1_1-database.ps1 -Force
```

---

## Professional Scripts

These scripts are designed to be:
- **Reliable**: Consistent results across environments
- **User-friendly**: Clear output and error messages
- **Maintainable**: Easy to understand and modify
- **Professional**: Production-ready quality