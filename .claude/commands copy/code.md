---
name: code
description: Implement code using TDD workflow - delegates to test-engineer and troubleshooter agents
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite
argument-hint: <task-id>
model: sonnet
---

**Goal**: Implement code following TDD (Test-Driven Development) workflow

## Context

- Plan context: @project/_/plans/plan_.md (most recent consulted)

## Tasks

1. Use `SlashCommand` Tool to invoke this slash commands in sequence:
   - `/tdd:create-failing-tests <file-paths>` -> `/tdd:write-code <file-paths>` -> `/tdd:refactor <file-paths>`
1. If file paths are not provided, invoke `AskUserQuestion` Tool to ask the user for the file paths.
1. Provide a summary of the what has been implemented and the results.

## Prohibited Tasks

- DO NOT implement code yourself. Only invoke `SlashCommand` Tool.
- DO NOT invoke `SlashCommand` Tool in parallel. Only invoke one at a time.
- DO NOT write tests directly (delegate to test-engineer)
- DO NOT commit anything

## Examples

```bash
/code
/code T001
/code T001-T003
```
