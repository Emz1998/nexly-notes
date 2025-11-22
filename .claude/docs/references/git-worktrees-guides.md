# Git Worktrees with Claude Code

Git worktrees enable running multiple Claude Code sessions in parallel, each working on different features or tasks with complete isolation. This has become a standard workflow pattern in 2025 for complex development projects.

## What are Git Worktrees?

Git worktrees allow you to check out multiple branches from the same repository into separate directories, sharing the same Git history while maintaining independent file states.

## Why Use Worktrees with Claude Code?

- **Parallel Development**: Work on multiple features simultaneously without context switching
- **Isolated Sessions**: Each Claude session has its own focused context and file state
- **Non-Deterministic AI Workflows**: Run multiple AI agents in parallel and select the best implementation
- **Long-Running Processes**: Treat AI coding sessions as persistent, focused dialogues

## Basic Implementation

### 1. Create a Worktree

```bash
# Create a new worktree for a feature branch
git worktree add ../project-feature-a -b feature-a

# Or use an existing branch
git worktree add ../project-hotfix hotfix/urgent-bug
```

### 2. Set Up Environment

```bash
cd ../project-feature-a

# Initialize development environment
npm install  # or yarn, pip install -r requirements.txt, etc.
cp .env.local ../project-feature-a/  # Copy environment variables
```

### 3. Launch Claude Code

```bash
# In each worktree directory
claude
```

## Advanced Workflow Patterns

### Multiple AI Perspectives

Run different approaches in parallel:
- One Claude writes code while another reviews it
- Multiple implementations of the same feature for comparison
- Separate sessions for different components of a large feature

### Task-Specific Worktrees

Create worktrees organized by task type:
```bash
git worktree add ../project-frontend -b feature/ui-overhaul
git worktree add ../project-backend -b feature/api-refactor
git worktree add ../project-tests -b feature/test-coverage
```

### Session Management Tools

**CCManager**: TUI application for managing multiple Claude Code sessions across worktrees:
```bash
# Install and use ccmanager for streamlined workflow
w core some-feature claude  # Creates worktree and launches Claude
```

## Best Practices

### Environment Setup
- Minimize complex environment configurations
- Use simple setup commands (npm install, copy .env files)
- Ensure each worktree can run independently

### Task Documentation
- Create ISSUE.md files with clear requirements
- Document what needs implementation, fixing, and rules to follow
- Claude will execute detailed instructions faithfully

### Context Management
- Use descriptive directory names for worktrees
- Keep focused, single-purpose sessions per worktree
- Maintain clear separation of concerns

### Resource Management
- Monitor system resources when running multiple sessions
- Close unused worktrees to free up memory
- Use `git worktree prune` to clean up removed worktrees

## Common Commands

### Create and Manage Worktrees
```bash
# List all worktrees
git worktree list

# Create new worktree
git worktree add <path> [-b <branch>]

# Remove worktree
git worktree remove <path>

# Clean up deleted worktree references
git worktree prune
```

### Workflow Integration
```bash
# Quick setup script example
create_worktree() {
  git worktree add "../$1" -b "$1"
  cd "../$1"
  npm install
  cp ../.env.local .
  claude
}

# Usage: create_worktree feature-dashboard
```

## Use Cases

### Feature Development
- Frontend and backend development in parallel
- UI components and business logic separation
- Different approaches to the same problem

### Code Review and Testing
- One session for implementation, another for testing
- Simultaneous development and documentation
- Experimental changes without affecting main work

### Hotfixes and Maintenance
- Emergency fixes while continuing feature work
- Dependency updates in isolation
- Performance optimizations as separate experiments

## Integration with Claude Code Features

### Memory and Context
- Each worktree maintains its own CLAUDE.md context
- Session history is preserved per worktree
- Custom commands and agents work independently

### Tool Access
- File operations are scoped to the specific worktree
- Git operations affect the shared repository
- Build and test commands run in isolation

## Troubleshooting

### Common Issues
- **Environment inconsistencies**: Ensure all worktrees have proper setup
- **Resource constraints**: Monitor CPU and memory usage with multiple sessions
- **Git conflicts**: Coordinate merges between parallel branches

### Performance Tips
- Use SSDs for better I/O performance with multiple worktrees
- Limit concurrent sessions based on system capabilities
- Close inactive sessions to free resources

## Official Support

This workflow is officially documented in Anthropic's Claude Code best practices as a recommended pattern for parallel development, reflecting its adoption as a standard practice in the Claude Code community.