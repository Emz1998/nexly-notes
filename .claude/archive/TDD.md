---
name: TDD (Test-Driven Development)
description: Test Driven Development Workflow for software development
---

# TDD (Test-Driven Development)

## Core Workflow

### Phase 1: Test Creation
- Write comprehensive tests based on expected input/output pairs
- Ensure tests cover edge cases, error conditions, and happy paths
- Tests must fail initially (no mock implementations)
- Confirm all tests fail before proceeding
- Commit tests when complete

### Phase 2: Implementation
- Write minimal code to pass tests
- Do not modify existing tests during implementation
- Iterate: write code → run tests → adjust code → repeat
- Continue until all tests pass
- Keep implementation focused on test requirements

### Phase 3: Verification
- Use independent subagents to verify implementation quality
- Check that implementation isn't overfitting to tests
- Ensure code meets broader requirements beyond test cases
- Commit code once verified and approved

## Workflow Rules

### Test Writing Guidelines
- **Explicit TDD Mode**: Always acknowledge when doing TDD to avoid creating mock implementations
- **Test First**: Never write implementation before tests are committed
- **Test Independence**: Each test should be isolated and not depend on other tests
- **Clear Assertions**: Use descriptive test names and clear failure messages
- **Coverage Goals**: Aim for comprehensive coverage of functionality

### Implementation Guidelines
- **Incremental Progress**: Show test results after each iteration
- **No Test Modification**: Tests are the spec - don't change them during implementation
- **Minimal Implementation**: Write only enough code to pass tests
- **Refactoring**: Only refactor after tests pass, keeping tests green

### Commit Strategy
- **Commit 1**: Tests only (must be failing)
- **Commit 2**: Implementation that passes tests
- **Clear Messages**: Use descriptive commit messages indicating TDD phase

## Key Rules and Principles

### Test-Driven Development
- **Red**: Write failing tests first
- **Green**: Write minimal code to pass
- **Refactor**: Improve code while keeping tests green

### Clear Targets
- Tests provide unambiguous success criteria
- Implementation has clear goals to achieve
- Verification ensures quality beyond tests

### Iterative Improvement
- Each iteration brings measurable progress
- Failures guide next steps
- Success is clearly defined by passing tests

