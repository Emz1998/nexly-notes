---
name: create-failing-tests
description: Create failing tests in src/tests/ by delegating to test-engineer agent (TDD Red phase)
allowed-tools: Task
argument-hint: <additional-instructions>
model: sonnet
---

**Goal**: Invoke the test-engineer agent to write failing tests for the specified feature or component in `@src/tests/` following TDD methodology (Red phase)

## Tasks

1. Invoke @agent-test-engineer to write failing tests in `@src/tests/`
2. Invoke @agent-test-manager to review the tests quality and correctness

## Prohibited Tasks

- Implementing production code. Only invoke Subagents to do this.
- Running tests to make them pass (this is the Red phase only)
- Modifying existing production code
- Creating tests yourself
