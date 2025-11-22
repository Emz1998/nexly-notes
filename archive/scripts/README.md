# Scripts Directory

## Purpose
Automation scripts for Claude Code workflow and session management.

## Available Scripts

### Claude Launch Scripts

#### 1. launch-new-claude.sh
**Purpose**: Start a new Claude Code session
```bash
./scripts/launch-new-claude.sh
```

#### 2. launch-resume-claude.sh
**Purpose**: Resume an existing Claude Code session
```bash
./scripts/launch-resume-claude.sh
```

#### 3. launch-new-claude-yolo.sh
**Purpose**: Start Claude with auto-yes mode (skips permission prompts)
```bash
./scripts/launch-new-claude-yolo.sh
```

#### 4. launch-resume-claude-yolo.sh
**Purpose**: Resume Claude session with auto-yes mode
```bash
./scripts/launch-resume-claude-yolo.sh
```

### Setup Scripts

#### 5. setup-yolo-aliases.sh
**Purpose**: Configure shell aliases for quick Claude commands
```bash
source ./scripts/setup-yolo-aliases.sh
```

Adds the following aliases:
- `yolo` - Run Claude with `--dangerously-skip-permissions`
- `yolo-r` - Resume Claude with auto-yes mode
- Additional worktree navigation shortcuts

## Integration with Development Container

These scripts are integrated with the development container through `.devcontainer/init-shortcuts.sh`, which automatically sets up:
- YOLO aliases for quick Claude operations
- Git worktree navigation functions
- Shell shortcuts for common tasks

## Prerequisites
- Bash shell
- Claude CLI installed and configured
- Git (for worktree scripts)

## Usage Notes

### YOLO Mode
The YOLO (You Only Launch Once) variants automatically accept all permission prompts, useful for:
- Automated workflows
- Experienced users who understand the risks
- Development environments where permissions are pre-approved

⚠️ **Warning**: YOLO mode skips safety prompts. Use with caution in production environments.

### Session Management
- New sessions start fresh with no prior context
- Resume sessions continue from the last saved state
- Sessions are automatically saved when Claude exits normally

## Troubleshooting

If scripts fail to execute:
1. Ensure execute permissions: `chmod +x scripts/*.sh`
2. Verify Claude CLI is installed: `which claude`
3. Check shell compatibility (scripts require Bash)

---
*Last updated: 2025-09-07*