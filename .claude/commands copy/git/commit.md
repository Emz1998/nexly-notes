---
name: commit
description: Create a git commit by delegating to version-control-manager agent
allowed-tools: Task, Bash(git status:*), Bash(git diff:*), Bash(git log:*)
argument-hint: [commit-message]
model: sonnet
---

**Goal**: Create a well-formed git commit by delegating to the version-control-manager agent

## Context

- Commit message (optional): $ARGUMENTS
- Current git status: !`git status --short`
- Current branch: !`git branch --show-current`

## Tasks

- T001: Delegate to `version-control-manager` agent to create the commit
- T002: Report commit status and hash to user

## Subagent Delegation

Delegate to `version-control-manager` with this prompt:

```
Create a git commit for the current changes.

User-provided message: $ARGUMENTS (if empty, generate message from changes)

Your tasks:
1. Review staged and unstaged changes via git status and git diff
2. Stage appropriate files (exclude .env, credentials, secrets)
3. Generate a conventional commit message if none provided
4. Create the commit following project conventions
5. Report the commit hash and summary

Commit message format:
- Use conventional commits (feat:, fix:, docs:, refactor:, test:, chore:)
- Keep subject line under 72 characters
- Add body for complex changes

Safety rules:
- NEVER commit files containing secrets or credentials
- NEVER force push or use destructive git commands
- NEVER commit generated files (node_modules, .next, dist)
```

## Implementation Strategy

- Review all changes before staging
- Follow conventional commit format
- Keep commits atomic and focused
- Generate meaningful commit messages

## Prohibited Tasks

- DO NOT commit files containing secrets (.env, credentials, API keys)
- DO NOT use `git push` - only create local commits
- DO NOT use `--force` or destructive git operations
- DO NOT commit without reviewing changes first
- DO NOT commit node_modules, .next, or build artifacts

## Success Criteria

- version-control-manager agent created the commit
- Commit follows conventional commit format
- No secrets or credentials were committed
- Commit hash and summary reported to user

## Examples

```bash
# Create commit with auto-generated message
/commit

# Create commit with custom message
/commit feat: add user authentication

# Create commit with detailed message
/commit fix: resolve login redirect loop
```
