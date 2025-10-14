# LuminoraCore Scripts

Utility scripts for development, testing, and deployment.

## Available Scripts

### Development & Setup

#### `setup-v1_1-database.sh`
**Purpose:** Initialize and migrate v1.1 database tables

**Usage:**
```bash
# Use default database (luminora.db)
./scripts/setup-v1_1-database.sh

# Specify custom database path
./scripts/setup-v1_1-database.sh /path/to/database.db
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

#### `test-v1_1-features.sh`
**Purpose:** Comprehensive testing of all v1.1 features

**Usage:**
```bash
./scripts/test-v1_1-features.sh
```

**What it tests:**
- Core v1.1 imports (8 modules)
- SDK v1.1 imports (4 modules)
- CLI v1.1 commands (3 commands)
- Pytest unit tests (82+ Core, 22+ SDK)
- Example scripts execution

**Output:**
- Pass/fail for each test
- Summary statistics
- Exit code 0 if all pass

---

### Deployment

#### `create-lambda-layer-deepseek.ps1`
**Purpose:** Build AWS Lambda Layer with LuminoraCore SDK + DeepSeek

**Usage:**
```powershell
.\scripts\create-lambda-layer-deepseek.ps1
```

**What it does:**
- Builds SDK in Docker (Python 3.11)
- Includes DeepSeek dependencies
- Creates Lambda Layer ZIP
- Publishes to AWS Lambda
- Stores ARN in SSM Parameter Store

**Prerequisites:**
- Docker running
- AWS CLI configured
- Correct AWS permissions

**v1.1 Status:** ⚠️ Needs update to include v1.1 features

---

## CLI Scripts

Located in `luminoracore-cli/scripts/`:

### `build-binary.sh`
**Purpose:** Build standalone CLI executable using PyInstaller

**Usage:**
```bash
cd luminoracore-cli
./scripts/build-binary.sh
```

**Output:**
- Binary for current platform
- Platform-specific archive (.tar.gz, .zip)
- Installation scripts (install.sh, install.bat)

---

### `install-completions.sh`
**Purpose:** Install shell completions (bash, zsh, fish)

**Usage:**
```bash
cd luminoracore-cli
./scripts/install-completions.sh
```

**Supports:**
- Bash (system-wide or user)
- Zsh (Oh My Zsh or system)
- Fish

---

### `setup-dev.sh`
**Purpose:** Setup development environment for CLI

**Usage:**
```bash
cd luminoracore-cli
./scripts/setup-dev.sh
```

**What it does:**
- Creates virtual environment
- Installs dev dependencies
- Installs package in editable mode
- Sets up git hooks
- Creates dev config

---

### `test-cli.sh`
**Purpose:** Comprehensive CLI testing (v1.0 + v1.1)

**Usage:**
```bash
cd luminoracore-cli
./scripts/test-cli.sh
```

**Tests:**
- 25+ CLI tests
- v1.0 commands (validate, compile, blend, etc.)
- v1.1 commands (migrate, memory, snapshot)
- Code formatting (black, isort)
- Type checking (mypy)
- Pytest unit tests

---

## Quick Reference

### First Time Setup
```bash
# 1. Setup v1.1 database
./scripts/setup-v1_1-database.sh

# 2. Test v1.1 features
./scripts/test-v1_1-features.sh

# 3. Setup CLI development (if needed)
cd luminoracore-cli && ./scripts/setup-dev.sh
```

### Before Commit
```bash
# Test everything
./scripts/test-v1_1-features.sh
cd luminoracore-cli && ./scripts/test-cli.sh
```

### Build for Production
```bash
# Build CLI binary
cd luminoracore-cli && ./scripts/build-binary.sh

# Build Lambda Layer
pwsh ./scripts/create-lambda-layer-deepseek.ps1
```

---

## Platform Support

| Script | Linux | macOS | Windows |
|--------|-------|-------|---------|
| setup-v1_1-database.sh | ✅ | ✅ | ✅ (Git Bash/WSL) |
| test-v1_1-features.sh | ✅ | ✅ | ✅ (Git Bash/WSL) |
| create-lambda-layer-deepseek.ps1 | ❌ | ❌ | ✅ (PowerShell) |
| build-binary.sh | ✅ | ✅ | ✅ (Git Bash) |
| install-completions.sh | ✅ | ✅ | ❌ |
| setup-dev.sh | ✅ | ✅ | ✅ (Git Bash) |
| test-cli.sh | ✅ | ✅ | ✅ (Git Bash) |

---

## Exit Codes

All scripts follow standard exit codes:
- `0` - Success
- `1` - Error

---

## Troubleshooting

### "Permission denied"
```bash
chmod +x scripts/*.sh
chmod +x luminoracore-cli/scripts/*.sh
```

### "Module not found"
```bash
# Install Core
cd luminoracore && pip install -e .

# Install SDK
cd luminoracore-sdk-python && pip install -e .

# Install CLI
cd luminoracore-cli && pip install -e .
```

### "Docker not running" (Lambda Layer)
```powershell
# Start Docker Desktop on Windows
# Or: docker-machine start (if using Docker Machine)
```

---

## Contributing

When adding new scripts:
1. Add to this README
2. Include help/usage info
3. Follow existing patterns
4. Test on multiple platforms
5. Add to CI/CD if applicable

---

**Last Updated:** October 14, 2025 (v1.1 release)

