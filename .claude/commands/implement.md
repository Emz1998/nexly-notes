---
name: implement
description: Implement tasks, milestones, or phases from specs/tasks.md using the full workflow
allowed-tools: Read, Bash, SlashCommand, TodoWrite, AskUserQuestion
argument-hint: <T001|T001-T003|MS-001|Phase 1>
model: sonnet
---

**Goal**: Implement specified task(s), milestone(s), or phase(s) from `@project/v0.1.0/release-plan/release-plan.md` using Contract-First, Mock-Driven Development

## Context

- Release Plan: `@project/v0.1.0/release-plan/release-plan.md`
- Workflow: `/explore` → `/research` → `/plan` → `/code` → `/code-review` -> `/validate` -> `/commit`
- Task Status Legend:
  - `x` - Completed
  - `!` - Blocked

## Workflow

### Phase 1: Parse and Validate

- Read release plan from `project/v0.1.0/release-plan/release-plan.md`
- Parse `$ARGUMENTS` to check if the input is valid
- Extract all task IDs including suffix tasks (T010A, T010B, etc.)
- Check for blocked tasks `!` and report to user
- Validate milestone prerequisites before proceeding

### Phase 2: Setup Working Environment

- Create git branch: `[MS-NNN]/[milestone-description]`
- Create project directory: `project/v0.1.0/milestones/[MS-NNN]_[Milestone-Description]/`
- Create verification checklist from milestone acceptance criteria
- Initialize todo list with extracted tasks using `TodoWrite`
- Identify parallel [P] and subagent [SA] tasks for optimization

### Phase 3: Implementation Workflow

_Call the following commands in sequence:_

- Call `/explore <task-descriptions>` for codebase context
- Call `/research <task-descriptions>` for best practices
- Call `/plan implementation <task-descriptions>` for strategy
- Call `/code <task-id>` for each task sequentially
- Call `/code-review` to review all changes
- Call `/validate` to validate the work completion
- Call `/commit` to commit the changes

### Phase 4: Final Verification and Report

- Perform a final verification of the work done.
- Rerun tests to ensure there are no regressions.
- Recheck if we missed anything.
- Report the implementation summary with completion status

## Rules

- **NEVER** accept free-form feature descriptions (use `/plan` for that)
- **NEVER** bypass the workflow by calling agents directly
- **NEVER** skip steps in the workflow sequence
- **NEVER** call `/code` without completing `/plan` and `/explore` first
- **NEVER** implement tasks beyond the specified scope
- **NEVER** mark tasks as `x` without verifying acceptance criteria
- **NEVER** ignore blocked (`!`) tasks without user acknowledgment

## Acceptance Criteria

- [ ] Input correctly parsed as Task, Milestone, or Phase
- [ ] Blocked tasks (`!`) identified and handled
- [ ] Prerequisites validated for milestone(s)
- [ ] Git branch created with format `[MS-NNN]/[milestone-description]`
- [ ] Project directory created at `project/v0.1.0/milestones/[MS-NNN]_[Description]/`
- [ ] All workflow commands executed in sequence
- [ ] Acceptance criteria verified from release plan
- [ ] Task status updated in release plan to `x` if successful, `!` if blocked

## Input Format

This command accepts the following input formats: `MS-NNN` - For example: `MS-001`, `MS-001-MS-003`, `MS-001 MS-005`

**Example:**

```
/implement MS-001
```

```
/implement MS-001-MS-003
```

```
/implement MS-001 MS-005
```
