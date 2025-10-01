#!/bin/bash

# Install shell completions for LuminoraCore CLI
# Supports bash, zsh, and fish shells

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Installing LuminoraCore CLI completions...${NC}"

# Get the installation directory
INSTALL_DIR=$(python -c "import luminoracore_cli; print(luminoracore_cli.__file__.replace('__init__.py', ''))" 2>/dev/null || echo "")

if [ -z "$INSTALL_DIR" ]; then
    echo -e "${RED}Error: Could not find luminoracore_cli installation${NC}"
    echo "Please install luminoracore_cli first: pip install luminoracore-cli"
    exit 1
fi

echo -e "${YELLOW}Found luminoracore_cli at: $INSTALL_DIR${NC}"

# Function to install bash completion
install_bash_completion() {
    local completion_file="$INSTALL_DIR/completion/bash_completion.sh"
    local bash_completion_dir="/usr/local/etc/bash_completion.d"
    local user_bash_completion_dir="$HOME/.local/share/bash-completion/completions"
    
    if [ -f "$completion_file" ]; then
        # Try system-wide installation first
        if [ -w "$bash_completion_dir" ]; then
            cp "$completion_file" "$bash_completion_dir/luminoracore-cli"
            echo -e "${GREEN}Bash completion installed system-wide${NC}"
        elif [ -d "$(dirname "$user_bash_completion_dir")" ]; then
            mkdir -p "$user_bash_completion_dir"
            cp "$completion_file" "$user_bash_completion_dir/luminoracore-cli"
            echo -e "${GREEN}Bash completion installed for user${NC}"
        else
            echo -e "${YELLOW}Manual bash completion setup required:${NC}"
            echo "Add this line to your ~/.bashrc:"
            echo "source $completion_file"
        fi
    else
        echo -e "${YELLOW}Bash completion file not found${NC}"
    fi
}

# Function to install zsh completion
install_zsh_completion() {
    local completion_file="$INSTALL_DIR/completion/zsh_completion.sh"
    local zsh_completion_dir="$HOME/.oh-my-zsh/completions"
    local zsh_site_functions="/usr/local/share/zsh/site-functions"
    
    if [ -f "$completion_file" ]; then
        # Try Oh My Zsh installation first
        if [ -d "$zsh_completion_dir" ]; then
            cp "$completion_file" "$zsh_completion_dir/_luminoracore-cli"
            echo -e "${GREEN}Zsh completion installed for Oh My Zsh${NC}"
        elif [ -w "$zsh_site_functions" ]; then
            cp "$completion_file" "$zsh_site_functions/_luminoracore-cli"
            echo -e "${GREEN}Zsh completion installed system-wide${NC}"
        else
            echo -e "${YELLOW}Manual zsh completion setup required:${NC}"
            echo "Add this line to your ~/.zshrc:"
            echo "source $completion_file"
        fi
    else
        echo -e "${YELLOW}Zsh completion file not found${NC}"
    fi
}

# Function to install fish completion
install_fish_completion() {
    local completion_file="$INSTALL_DIR/completion/fish_completion.sh"
    local fish_completion_dir="$HOME/.config/fish/completions"
    
    if [ -f "$completion_file" ]; then
        mkdir -p "$fish_completion_dir"
        cp "$completion_file" "$fish_completion_dir/luminoracore-cli.fish"
        echo -e "${GREEN}Fish completion installed${NC}"
    else
        echo -e "${YELLOW}Fish completion file not found${NC}"
    fi
}

# Detect shell and install appropriate completion
case "$SHELL" in
    */bash)
        install_bash_completion
        ;;
    */zsh)
        install_zsh_completion
        ;;
    */fish)
        install_fish_completion
        ;;
    *)
        echo -e "${YELLOW}Unknown shell: $SHELL${NC}"
        echo "Available completions:"
        echo "  - Bash: $INSTALL_DIR/completion/bash_completion.sh"
        echo "  - Zsh:  $INSTALL_DIR/completion/zsh_completion.sh"
        echo "  - Fish: $INSTALL_DIR/completion/fish_completion.sh"
        ;;
esac

echo -e "${GREEN}Completion installation complete!${NC}"
echo -e "${YELLOW}Restart your shell or run 'source ~/.bashrc' (or equivalent) to activate completions.${NC}"
