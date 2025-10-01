#!/bin/bash

# Build binary distribution for LuminoraCore CLI
# Creates standalone executables using PyInstaller

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Building LuminoraCore CLI binary distribution...${NC}"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] || [ ! -d "luminoracore_cli" ]; then
    echo -e "${RED}Error: Please run this script from the luminoracore-cli root directory${NC}"
    exit 1
fi

# Create build directory
BUILD_DIR="dist"
mkdir -p "$BUILD_DIR"

# Install PyInstaller if not already installed
echo -e "${YELLOW}Installing PyInstaller...${NC}"
pip install pyinstaller

# Create PyInstaller spec file
echo -e "${YELLOW}Creating PyInstaller spec file...${NC}"
cat > luminoracore-cli.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['luminoracore_cli/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('luminoracore_cli/templates', 'luminoracore_cli/templates'),
        ('luminoracore_cli/completion', 'luminoracore_cli/completion'),
    ],
    hiddenimports=[
        'luminoracore_cli.config',
        'luminoracore_cli.commands',
        'luminoracore_cli.core',
        'luminoracore_cli.utils',
        'luminoracore_cli.server',
        'luminoracore_cli.templates',
        'luminoracore_cli.interactive',
        'luminoracore_cli.completion',
        'rich',
        'typer',
        'click',
        'questionary',
        'httpx',
        'pydantic',
        'pyyaml',
        'jinja2',
        'fastapi',
        'uvicorn',
        'websockets',
        'textual',
        'aiofiles',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='luminoracore-cli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
EOF

# Build for current platform
echo -e "${YELLOW}Building binary for current platform...${NC}"
pyinstaller --clean luminoracore-cli.spec

# Create platform-specific builds
PLATFORM=$(uname -s)
ARCH=$(uname -m)

case "$PLATFORM" in
    Linux)
        PLATFORM_NAME="linux"
        ;;
    Darwin)
        PLATFORM_NAME="macos"
        ;;
    CYGWIN*|MINGW*|MSYS*)
        PLATFORM_NAME="windows"
        ;;
    *)
        PLATFORM_NAME="unknown"
        ;;
esac

BINARY_NAME="luminoracore-cli-${PLATFORM_NAME}-${ARCH}"
BINARY_DIR="$BUILD_DIR/$BINARY_NAME"

echo -e "${YELLOW}Creating distribution package...${NC}"
mkdir -p "$BINARY_DIR"

# Copy binary
cp "dist/luminoracore-cli" "$BINARY_DIR/" 2>/dev/null || cp "dist/luminoracore-cli.exe" "$BINARY_DIR/" 2>/dev/null || {
    echo -e "${RED}Error: Could not find built binary${NC}"
    exit 1
}

# Copy additional files
cp README.md "$BINARY_DIR/"
cp LICENSE "$BINARY_DIR/" 2>/dev/null || echo "# License information" > "$BINARY_DIR/LICENSE"
cp requirements.txt "$BINARY_DIR/"

# Create installation script
cat > "$BINARY_DIR/install.sh" << 'EOF'
#!/bin/bash

# Install LuminoraCore CLI binary

set -e

BINARY_NAME="luminoracore-cli"
INSTALL_DIR="/usr/local/bin"

# Check if running as root for system-wide installation
if [ "$EUID" -eq 0 ]; then
    echo "Installing LuminoraCore CLI system-wide..."
    cp "$BINARY_NAME" "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/$BINARY_NAME"
    echo "Installation complete!"
    echo "Run 'luminoracore-cli --help' to get started."
else
    echo "Installing LuminoraCore CLI for current user..."
    USER_BIN="$HOME/.local/bin"
    mkdir -p "$USER_BIN"
    cp "$BINARY_NAME" "$USER_BIN/"
    chmod +x "$USER_BIN/$BINARY_NAME"
    
    # Add to PATH if not already there
    if ! echo "$PATH" | grep -q "$USER_BIN"; then
        echo "Adding $USER_BIN to PATH in ~/.bashrc"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    fi
    
    echo "Installation complete!"
    echo "You may need to restart your shell or run: source ~/.bashrc"
    echo "Run 'luminoracore-cli --help' to get started."
fi
EOF

chmod +x "$BINARY_DIR/install.sh"

# Create Windows installation script
cat > "$BINARY_DIR/install.bat" << 'EOF'
@echo off
REM Install LuminoraCore CLI binary for Windows

set BINARY_NAME=luminoracore-cli.exe
set INSTALL_DIR=%USERPROFILE%\AppData\Local\Programs\luminoracore-cli

echo Creating installation directory...
mkdir "%INSTALL_DIR%" 2>nul

echo Copying binary...
copy "%BINARY_NAME%" "%INSTALL_DIR%\"

echo Adding to PATH...
setx PATH "%PATH%;%INSTALL_DIR%" /M >nul 2>&1 || setx PATH "%PATH%;%INSTALL_DIR%"

echo Installation complete!
echo Run 'luminoracore-cli --help' to get started.
pause
EOF

# Create archive
echo -e "${YELLOW}Creating archive...${NC}"
cd "$BUILD_DIR"
if command -v tar >/dev/null 2>&1; then
    tar -czf "${BINARY_NAME}.tar.gz" "$BINARY_NAME"
    echo -e "${GREEN}Created ${BINARY_NAME}.tar.gz${NC}"
fi

if command -v zip >/dev/null 2>&1; then
    zip -r "${BINARY_NAME}.zip" "$BINARY_NAME"
    echo -e "${GREEN}Created ${BINARY_NAME}.zip${NC}"
fi

cd ..

# Clean up
echo -e "${YELLOW}Cleaning up...${NC}"
rm -rf build/
rm -rf *.spec

echo -e "${GREEN}Binary build complete!${NC}"
echo -e "${BLUE}Distribution files created in: $BUILD_DIR/$BINARY_NAME${NC}"
echo -e "${YELLOW}To test the binary:${NC}"
echo -e "  ./$BUILD_DIR/$BINARY_NAME/luminoracore-cli --help"
