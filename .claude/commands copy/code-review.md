---
name: code-review
description: Review committed code by delegating to code-reviewer agent
allowed-tools: Read, Glob, Grep, Task, Bash
argument-hint: <file-path>
model: sonnet
---

**Goal**: Review committed code for quality, security, and best practices

## Requirements

<file-paths> $ARGUMENTS </file-paths>

## Tasks

1. Use `SlashCommand` Tool to invoke this slash commands in sequence:
   - `/review:code <file-paths>` -> `/review:security <file-paths>` -> `/review:performance <file-paths>`
2. If file paths are not provided, invoke `AskUserQuestion` Tool to ask the user for the file paths.
3. Provide a summary of the what has been reviewed and the findings.

## Prohibited Tasks

- DO NOT implement and changes yourself. Only invoke `SlashCommand` Tool.

## Examples of Valid Inputs

```bash
/code-review
/code-review src/components/Button.tsx
/code-review src/components/Button.tsx, src/components/Input.tsx
/code-review main..feature-branch
/code-review HEAD~3..HEAD
```
