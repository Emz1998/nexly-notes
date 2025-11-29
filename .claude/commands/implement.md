---
name: implement
description: Build a production-ready feature with thorough planning and structured context gathering
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite, AskUserQuestion, WebSearch, WebFetch
argument-hint: Build a <feature> that will <functionality>
---

**Goal**: Implement task(s) from `@specs/tasks.md` following the EPIC workflow (Explore, Plan, Implement, Commit)

## Context

- Tasks file: `@specs/tasks.md`
- User request: $ARGUMENTS

## Tasks

### Phase 1: Explore

- T001: Parse user request to identify task IDs (T001, T002, etc.) from `specs/tasks.md`
- T002: Delegate to `codebase-explorer` agent to understand current project state, relevant files, and dependencies
- T003: Document exploration findings and affected areas

### Phase 2: Plan

- T004: Delegate to `research-specialist` agent to research best practices, patterns, and implementation approaches
- T005: Delegate to `strategic-planner` agent to create detailed implementation strategy
- T006: Review and consolidate plans from both agents into a unified approach
- T007: Use `AskUserQuestion` to validate approach with user if needed

### Phase 2.5: Plan Review (Quality Gate)

- T008: Signal "plan complete" to trigger `implementation-review` skill
- T009: Delegate to `plan-consultant` agent to review the implementation strategy
- T010: Address any critical issues flagged by plan-consultant before proceeding
- T011: If review status is BLOCKED, revise plan and re-review

### Phase 3: Implement (TDD)

- T012: Delegate to `test-engineer` agent to create failing tests for the feature
- T013: Verify tests fail as expected (Red phase)
- T014: Implement minimal code to make tests pass (Green phase)
- T015: Verify all tests pass
- T016: Refactor code while keeping tests passing
- T017: Delegate to `troubleshooter` agent if errors or issues arise
- T018: Run full test suite to ensure no regressions

### Phase 3.5: Code Review (Quality Gate)

- T019: Signal "implementation complete" to trigger `implementation-review` skill
- T020: Delegate to `code-reviewer` agent to review the implementation
- T021: Address any critical issues flagged by code-reviewer before proceeding
- T022: If review status is BLOCKED, fix code and re-review

### Phase 4: Commit

- T023: Delegate to `version-manager` agent to create proper git commit with changes
- T024: Verify commit was created successfully
- T025: Update task status in `specs/tasks.md` to completed

## Implementation Strategy

- Follow TDD strictly: Red (failing test) -> Green (minimal implementation) -> Refactor
- Use specialized agents for their designated roles - do not bypass the workflow
- Main agent handles only the actual implementation code, not tests or commits
- Track progress using TodoWrite throughout the EPIC workflow
- If a task spans multiple sub-tasks, complete one full EPIC cycle per logical unit
- Validate each phase completion before proceeding to the next

## Agent Delegation Map

| Phase       | Agent                 | Purpose                                                |
| ----------- | --------------------- | ------------------------------------------------------ |
| Explore     | `codebase-explorer`   | Analyze project structure, dependencies, relevant code |
| Plan        | `research-specialist` | Research best practices, patterns, libraries           |
| Plan        | `strategic-planner`   | Create implementation roadmap and strategy             |
| Plan Review | `plan-consultant`     | Review and validate implementation strategy            |
| Implement   | `test-engineer`       | Write unit/integration tests following TDD             |
| Implement   | `troubleshooter`      | Debug and resolve implementation issues                |
| Code Review | `code-reviewer`       | Review code quality, security, and best practices      |
| Commit      | `version-manager`     | Create git commits with proper messages                |

## Prohibited Tasks

- DO NOT skip the Explore phase - context is critical
- DO NOT implement code before tests are written (TDD violation)
- DO NOT create git commits directly - delegate to version-manager
- DO NOT modify test files directly - delegate to test-engineer
- DO NOT skip user validation for significant design decisions
- DO NOT proceed to Commit if tests are failing

## Success Criteria

- [ ] Task IDs correctly identified from specs/tasks.md
- [ ] Codebase exploration completed with documented findings
- [ ] Research and strategy plans generated and consolidated
- [ ] Tests written before implementation (TDD Red phase)
- [ ] All tests pass after implementation (TDD Green phase)
- [ ] Code refactored without breaking tests
- [ ] Git commit created with descriptive message
- [ ] Task status updated in specs/tasks.md

## Examples

```bash
# Implement a single task
/implement T001

# Implement multiple sequential tasks
/implement T001-T003

# Implement all tasks in Phase 1
/implement Phase 1

# Implement sprint tasks
/implement SPRINT-001 tasks
```
