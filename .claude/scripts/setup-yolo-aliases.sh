#!/bin/bash

# Script to setup YOLO Claude aliases for both bash and zsh

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up YOLO Claude aliases...${NC}"

# Function to add aliases to a shell config file
add_aliases() {
    local shell_config="$1"
    local shell_name="$2"
    
    if [ -f "$shell_config" ]; then
        # Check if aliases already exist
        if grep -q "# YOLO Claude aliases" "$shell_config"; then
            echo -e "${YELLOW}YOLO aliases already exist in $shell_name, skipping...${NC}"
        else
            echo -e "${GREEN}Adding YOLO aliases to $shell_name...${NC}"
            {
                echo ""
                echo "# YOLO Claude aliases"
                echo 'alias yolo="claude --dangerously-skip-permissions"'
                echo 'alias yolo-r="claude --continue --dangerously-skip-permissions"'
                echo 'alias yolo-wt="/workspace/scripts/launch-new-claude-yolo.sh"'
                echo 'alias yolo-wt-r="/workspace/scripts/launch-resume-claude-yolo.sh"'
            } >> "$shell_config"
        fi
    else
        echo -e "${YELLOW}$shell_name config not found at $shell_config${NC}"
    fi
}

# Add aliases to bash
add_aliases "$HOME/.bashrc" "bash"

# Add aliases to zsh
add_aliases "$HOME/.zshrc" "zsh"

echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo "Aliases added:"
echo "  yolo       - Run claude with --dangerously-skip-permissions"
echo "  yolo-r     - Resume claude with --dangerously-skip-permissions"
echo "  yolo-wt    - Launch new claude in worktree (YOLO mode)"
echo "  yolo-wt-r  - Resume claude in worktree (YOLO mode)"
echo ""
echo "To activate the aliases, run one of:"
echo "  source ~/.bashrc  (for bash)"
echo "  source ~/.zshrc   (for zsh)"