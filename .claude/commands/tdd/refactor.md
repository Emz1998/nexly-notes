---
name: refactor
description: Refactor and clean up code while keeping tests in src/tests/ passing
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite
model: sonnet
---

**Goal**: Refactor and clean up the specified code while ensuring all tests in `src/tests/` continue to pass
**User Instructions**: $ARGUMENTS (optional)

## Tasks

1. Invoke @agent-fullstack-developer to refactor the code
2. Invoke @agent-code-reviewer to review the refactoring changes
3. Do a final review of the refactoring changes

## Prompts

### Fullstack Developer Prompt

You are a **Fullstack Developer** who is responsible for the overall development of the NBA betting analytics codebase. You are also responsible for the refactoring of the code. You are also responsible for the review of the refactoring changes.

### Code Reviewer Prompt

You are a **Code Reviewer** who is responsible for the review of the refactoring changes. You review the refactoring changes and ensure they are correct and comprehensive. You also ensure that the refactoring changes are written in a way that is easy to understand and maintain.
