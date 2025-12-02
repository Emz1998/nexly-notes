---
name: code
description: Implement code using TDD workflow - delegates to test-engineer and troubleshooter agents
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite
argument-hint: [task-id]
model: sonnet
---

**Goal**: Implement code following TDD (Test-Driven Development) workflow

## Context

- Task ID (optional): $ARGUMENTS
- Plan context: @project/*/plans/plan*.md (most recent consulted)

## TDD Phase Workflow

```
Phase           Agent              Action
─────────────────────────────────────────────────────
failing_test    test-engineer      Write failing tests
passing_test    (main agent)       Implement code to pass tests
refactor        (main agent)       Clean up code, keep tests green
troubleshoot    troubleshooter     Debug issues if they arise
commit          (main agent)       Commit changes
```

## Tasks

### Red Phase (Failing Tests)

- T001: Delegate to `test-engineer` agent to write failing tests based on the plan
- T002: Run tests and verify they fail as expected

### Green Phase (Passing Tests)

- T003: Implement minimal code to make tests pass
- T004: Run tests and verify they pass
- T005: If issues arise, delegate to `troubleshooter` agent

### Refactor Phase

- T006: Refactor implementation while keeping tests passing
- T007: Run full test suite to ensure no regressions

### Commit Phase

- T008: Commit all changes with descriptive message

## Subagent Delegations

### Test Engineer (Red Phase)

Delegate to `test-engineer` with this prompt:

```
Based on the implementation plan, write failing tests for: $ARGUMENTS

Requirements:
1. Write comprehensive unit tests
2. Write integration tests where applicable
3. Tests MUST fail initially (no implementation exists yet)
4. Follow project testing conventions

Run tests and confirm they fail.
```

### Troubleshooter (When Issues Arise)

Delegate to `troubleshooter` with this prompt:

```
Debug the following issue:
[describe the failing test or error]

Identify root cause and provide fix recommendations.
```

## Implementation Strategy

- Follow TDD strictly: Red → Green → Refactor
- Write minimal code to pass tests (no over-engineering)
- Keep refactoring focused on readability and maintainability
- Commit only when all tests pass

## Prohibited Tasks

- DO NOT implement code before tests exist
- DO NOT write tests directly (delegate to test-engineer)
- DO NOT commit with failing tests
- DO NOT skip the refactor phase

## Success Criteria

- test-engineer wrote failing tests (Red)
- Implementation makes tests pass (Green)
- Code refactored without breaking tests
- All tests pass before commit
- Changes committed with descriptive message

## Examples

```bash
/code
/code T001
/code T001-T003
```
