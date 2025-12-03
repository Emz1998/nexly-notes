#!/usr/bin/env python3
"""
Script to setup YOLO Claude aliases for both bash and zsh.
"""

from pathlib import Path

# ANSI colors for output
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"  # No Color

ALIASES_BLOCK = """
# YOLO Claude aliases
alias yolo="claude --dangerously-skip-permissions"
alias yolo-r="claude --continue --dangerously-skip-permissions"
alias yolo-wt="/workspace/scripts/launch-new-claude-yolo.sh"
alias yolo-wt-r="/workspace/scripts/launch-resume-claude-yolo.sh"
"""


def add_aliases(shell_config: Path, shell_name: str) -> None:
    """Add aliases to a shell config file."""
    if not shell_config.exists():
        print(f"{YELLOW}{shell_name} config not found at {shell_config}{NC}")
        return

    content = shell_config.read_text()

    # Check if aliases already exist
    if "# YOLO Claude aliases" in content:
        print(f"{YELLOW}YOLO aliases already exist in {shell_name}, skipping...{NC}")
        return

    print(f"{GREEN}Adding YOLO aliases to {shell_name}...{NC}")
    with shell_config.open("a") as f:
        f.write(ALIASES_BLOCK)


def main():
    print(f"{YELLOW}Setting up YOLO Claude aliases...{NC}")

    home = Path.home()

    # Add aliases to bash
    add_aliases(home / ".bashrc", "bash")

    # Add aliases to zsh
    add_aliases(home / ".zshrc", "zsh")

    print(f"{GREEN}Setup complete!{NC}")
    print()
    print("Aliases added:")
    print("  yolo       - Run claude with --dangerously-skip-permissions")
    print("  yolo-r     - Resume claude with --dangerously-skip-permissions")
    print("  yolo-wt    - Launch new claude in worktree (YOLO mode)")
    print("  yolo-wt-r  - Resume claude in worktree (YOLO mode)")
    print()
    print("To activate the aliases, run one of:")
    print("  source ~/.bashrc  (for bash)")
    print("  source ~/.zshrc   (for zsh)")


if __name__ == "__main__":
    main()
