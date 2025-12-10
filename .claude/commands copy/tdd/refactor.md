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

## Prohibited Tasks

- DO NOT refactor by yourself. Only refactor after doing the final review if deemed necessary.
- Implementing production code.
- Running tests to make them pass (this is the Refactor phase only)
- Modifying existing production code
- Creating tests yourself

## Success Criteria

- All tests in `src/tests/` pass after refactoring
- Code is cleaner and more maintainable
- No functional changes introduced
- Refactoring changes are documented in the summary

## Skills to Use

- Use `refactoring` skills PROACTIVELY when refactoring the code(Only if deemed necessary)
