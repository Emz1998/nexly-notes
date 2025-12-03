---
name: create-failing-tests
description: Create failing tests in src/tests/ by delegating to test-engineer agent (TDD Red phase)
allowed-tools: Task
argument-hint: <feature-or-component-description>
model: sonnet
---

**Goal**: Invoke the test-engineer agent to write failing tests for the specified feature or component in `@src/tests/` following TDD methodology (Red phase)

## Context

- Target test directory: `@src/tests/`
- Testing framework: Vitest
- TDD Phase: Red (write failing tests first)
- This command focuses ONLY on creating failing tests - implementation comes later

## Tasks

- T001: Analyze the provided feature/component description from `$ARGUMENTS`
- T002: Delegate to test-engineer agent to write failing tests in `@src/tests/`
- T003: Ensure tests follow the existing directory structure (`components/`, `hooks/`, `lib/`)
- T004: Verify tests are syntactically correct but fail due to missing implementation
- T005: Report the created test files and their locations

## Implementation Strategy

- Use the Task tool with `subagent_type: test-engineer` to delegate test creation
- Tests should be placed in the appropriate subdirectory based on what they test
- Each test should have clear descriptive names following: what is tested, conditions, expected outcome
- Tests must be isolated and independent
- Use existing test helpers and patterns from `@src/tests/`

## Prohibited Tasks

- Implementing production code - only tests should be written
- Running tests to make them pass (this is the Red phase only)
- Modifying existing production code
- Creating tests that pass without implementation

## Success Criteria

- Failing tests created in appropriate `@src/tests/` subdirectory
- Tests are syntactically correct and executable
- Test names clearly describe the expected behavior
- Tests follow TDD best practices (testing behavior, not implementation)
- Report includes list of created test files

## Examples

```bash
/create-failing-tests useAuth hook for handling user authentication state
/create-failing-tests NoteCard component with edit and delete actions
/create-failing-tests formatDate utility function with timezone support
```
