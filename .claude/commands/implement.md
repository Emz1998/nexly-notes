---
name: implement
description: Build a production-ready feature with thorough planning and structured context gathering
allowed-tools: Read, SlashCommand, TodoWrite, AskUserQuestion
argument-hint: Build a <feature> that will <functionality>
model: sonnet
---

**Goal**: Implement task(s) from `@specs/tasks.md` by orchestrating the workflow commands

## Context

- Tasks file: `@specs/tasks.md`
- User request: $ARGUMENTS
- Workflow: `/explore` → `/research` → `/plan` → `/code` → `/code-review`

## Tasks

### Phase 1: Explore Codebase

- T001: Parse user request to identify task IDs (T001, T002, etc.) from `specs/tasks.md`
- T002: Call `/explore $ARGUMENTS` using `SlashCommand` tool to analyze project structure

### Phase 2: Research Best Practices

- T003: Call `/research $ARGUMENTS` using `SlashCommand` tool to gather patterns and approaches

### Phase 3: Create Implementation Plan

- T004: Call `/plan implementation $ARGUMENTS` using `SlashCommand` tool to create strategy
- T005: Use `AskUserQuestion` to validate approach with user if needed

### Phase 4: Implement with TDD

- T006: Call `/code $ARGUMENTS` using `SlashCommand` tool to start TDD workflow

### Phase 5: Code Review

- T007: Call `/code-review` using `SlashCommand` tool to review implementation
- T008: Address any critical issues flagged before marking task complete

### Phase 6: Finalize

- T009: Update task status in `specs/tasks.md` to completed
- T010: Report implementation summary to user

## Implementation Strategy

- Use `SlashCommand` tool to call each workflow command in sequence
- Each phase must complete before proceeding to the next
- Track progress using TodoWrite throughout the workflow

## Prohibited Tasks

- DO NOT bypass the workflow by calling agents directly
- DO NOT skip phases in the workflow sequence
- DO NOT call `/code` without completing `/plan` first
- DO NOT call `/code-review` with uncommitted changes

## Success Criteria

- [ ] Task IDs correctly identified from specs/tasks.md
- [ ] `/explore` completed
- [ ] `/research` completed
- [ ] `/plan` completed
- [ ] `/code` completed with passing tests and committed changes
- [ ] `/code-review` completed
- [ ] Task status updated in specs/tasks.md

## Examples

```bash
# Implement a single task
/implement T001

# Implement a feature
/implement Build user authentication that will allow users to sign in with email

# Implement multiple sequential tasks
/implement T001-T003

# Implement sprint tasks
/implement SPRINT-001 tasks
```
