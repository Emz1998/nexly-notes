---
name: refactor
description: Refactor and clean up code while keeping tests in src/tests/ passing
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite
argument-hint: [file-or-directory]
model: sonnet
---

**Goal**: Refactor and clean up the specified code while ensuring all tests in `src/tests/` continue to pass

## Context

- Target to refactor: $ARGUMENTS
- Test directory: @src/tests/

## Tasks

### Phase 1: Analysis

- T001: Identify the file(s) or directory to refactor from `$ARGUMENTS`
- T002: Read and analyze the target code structure
- T003: Run existing tests to establish baseline (all must pass before refactoring)
- T004: Identify code smells, duplication, and areas for improvement

### Phase 2: Refactoring

- T005: Extract duplicated code into reusable functions/utilities
- T006: Improve naming for variables, functions, and classes
- T007: Simplify complex conditionals and nested logic
- T008: Apply consistent formatting and structure
- T009: Remove dead code and unused imports

### Phase 3: Validation

- T010: Run all tests in `src/tests/` to verify no regressions
- T011: If tests fail, revert changes and fix the issue
- T012: Repeat T010-T011 until all tests pass

### Phase 4: Finalization

- T013: Report refactoring changes made
- T014: Summarize improvements and any remaining technical debt

## Implementation Strategy

- Run tests BEFORE making any changes to establish passing baseline
- Make small, incremental changes (one refactoring at a time)
- Run tests AFTER each significant change
- Preserve public API contracts unless explicitly requested
- Focus on readability and maintainability over cleverness

## Prohibited Tasks

- DO NOT change functionality or add new features
- DO NOT refactor if baseline tests are failing
- DO NOT break existing public interfaces
- DO NOT over-engineer or add unnecessary abstractions
- DO NOT commit with failing tests
- DO NOT refactor test files unless explicitly requested

## Success Criteria

- All tests in `src/tests/` pass after refactoring
- Code is cleaner and more maintainable
- No functional changes introduced
- Refactoring changes are documented in the summary

## Examples

```bash
# Refactor a specific file
/refactor src/lib/helpers.ts

# Refactor a directory
/refactor src/components/editor/

# Refactor entire src folder
/refactor src/

# Refactor without arguments (will prompt for target)
/refactor
```

## References

- Test location: `src/tests/components/`, `src/tests/hooks/`, `src/tests/lib/`
- Run tests with: `npm test`
