---
name: write-code
description: Write minimal code to pass existing failing tests (TDD Green Phase)
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, TodoWrite
argument-hint: [test-file-path]
model: sonnet
---

**Goal**: Write the minimal implementation code needed to make failing tests pass (TDD Green Phase)

## Context

- Test file path (optional): $ARGUMENTS
- Default test location: @src/tests/
- Test structure:
  - @src/tests/components/ - Component tests
  - @src/tests/hooks/ - Hook tests
  - @src/tests/lib/ - Library/utility tests

## Tasks

### Phase 1: Discover Failing Tests

- T001: If no argument provided, scan `src/tests/` for all test files
- T002: Run the test suite to identify failing tests
- T003: Analyze each failing test to understand what implementation is expected

### Phase 2: Implement Minimal Code

- T004: For each failing test, identify the target implementation file
- T005: Write the minimal code required to make the test pass
- T006: Run tests after each implementation to verify the test passes
- T007: Repeat until all failing tests pass

### Phase 3: Validate

- T008: Run the full test suite to confirm no regressions
- T009: Report the results (tests passed/failed, files created/modified)

## Implementation Strategy

- Focus on one failing test at a time
- Write the absolute minimum code to make each test pass
- Avoid adding functionality beyond what tests require
- Match the expected interface/signature from the test
- Follow existing project patterns and conventions
- Do not refactor or optimize - just make tests pass

## Prohibited Tasks

- DO NOT write new tests (this command is for implementation only)
- DO NOT add features not covered by tests
- DO NOT refactor existing code unless required to pass a test
- DO NOT add error handling beyond what tests validate
- DO NOT add documentation or comments unless required by tests
- DO NOT over-engineer - minimal viable implementation only

## Success Criteria

- All previously failing tests now pass
- No new test failures introduced
- Implementation matches exactly what tests expect
- Code follows project conventions
- No unnecessary code added

## Examples

```bash
# Run against all tests in src/tests/
/write-code

# Run against a specific test file
/write-code src/tests/components/Button.test.ts

# Run against tests in a specific directory
/write-code src/tests/hooks/
```
