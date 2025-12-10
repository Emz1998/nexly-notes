---
name: implement
description: Implement tasks, milestones, or phases from specs/tasks.md using the full workflow
allowed-tools: Read, Bash, SlashCommand, TodoWrite, AskUserQuestion
argument-hint: <T001|T001-T003|MS-001|Phase 1>
model: sonnet
---

**Goal**: Implement specified task(s), milestone(s), or phase(s) from `@specs/tasks.md` by orchestrating the workflow commands

## Context

- Tasks file: `@specs/tasks.md`
- User input: $ARGUMENTS
- Workflow: `/explore` → `/research` → `/plan` → `/code` → `/code-review`

## Task Notation Guide

From `specs/tasks.md`:

- **[P]** = Parallel Task - has NO dependencies on other tasks in same milestone
- **[SA]** = Subagent Task - isolated task that can be delegated without context
- Tasks without [P] have dependencies on previous tasks

## Task Status Legend

- ⏳ Not Started
- 🔄 In Progress
- ✅ Completed
- ⚠️ Blocked (includes blocker ID)
- ❌ Cancelled

## Input Format

This command accepts ONLY one of the following formats:

### Tasks

- Single task: `T001`
- Task range: `T001-T003`
- Multiple tasks: `T001 T005 T010`

### Milestones

- Single milestone: `MS-001`
- Milestone range: `MS-001-MS-003`
- Multiple milestones: `MS-001 MS-005`

### Phases

- Single phase: `Phase 1` or `P1`
- Phase range: `Phase 1-3` or `P1-P3`

## Workflow Steps

### Step 1: Parse Input and Extract Tasks

1. Read `specs/tasks.md` to understand project structure
2. Parse `$ARGUMENTS` to determine input type (Task, Milestone, or Phase)
3. **Check for blocked tasks (⚠️)** - if any tasks in scope are blocked:
   - Report the blocker ID and description
   - Ask user whether to skip blocked tasks or abort
4. Extract all task IDs that fall under the specified scope:
   - If Task(s): Use the task IDs directly
   - If Milestone: Extract all tasks within that milestone (e.g., MS-001 contains T001-T010)
   - If Phase: Extract all milestones and their tasks within that phase
5. **Identify parallel tasks [P]** - these can potentially run concurrently
6. **Identify subagent tasks [SA]** - these are isolated and can be delegated
7. Determine the primary milestone for the scope:
   - If Task(s): Find the milestone containing the first task
   - If Milestone: Use that milestone directly
   - If Phase: Use the first milestone in the phase
8. **Extract acceptance criteria** for the milestone from `specs/tasks.md`
9. Create a todo list with all extracted tasks using `TodoWrite`

### Step 2: Validate Prerequisites

Before proceeding, verify milestone prerequisites are complete:

| Milestone | Prerequisite                    |
| --------- | ------------------------------- |
| MS-001    | None (starting point)           |
| MS-002    | MS-001 complete                 |
| MS-003    | MS-002 complete                 |
| MS-004    | MS-003 complete                 |
| MS-005    | MS-003 complete                 |
| MS-006    | MS-005 (T046-T047) complete     |
| MS-007    | MS-005 (T046-T047) complete     |
| MS-008    | MS-003 complete                 |
| MS-009    | MS-003 complete                 |
| MS-010    | MS-009 (T088-T091) complete     |
| MS-011    | MS-009 (T088-T091) complete     |
| MS-012    | MS-003 complete                 |
| MS-013    | MS-003 complete                 |
| MS-014    | MS-005 complete                 |
| MS-015    | MS-004 through MS-014 complete  |
| MS-016    | MS-004 through MS-014 complete  |
| MS-017    | MS-009 complete                 |
| MS-018    | MS-017 complete                 |
| MS-019    | MS-017 complete                 |
| MS-020    | MS-019 complete                 |
| MS-021    | MS-017 complete                 |
| MS-022    | MS-018 complete                 |
| MS-023    | All feature milestones complete |
| MS-024    | MS-023 complete                 |
| MS-025    | MS-024 complete                 |

If prerequisites are not met, report to user and ask whether to proceed anyway.

### Step 3: Create Milestone Branch

1. Format the milestone description from `specs/tasks.md` (e.g., "Environment Setup" → "environment-setup")
   - Convert to lowercase
   - Replace spaces with hyphens
   - Remove special characters
2. Create a new git branch with the naming convention: `[MS-NNN]/[milestone-description]`
   - Example: `MS-001/environment-setup`
   - Use `git checkout -b MS-001/environment-setup` via Bash tool
3. If multiple milestones are being implemented, use the first milestone for the branch name

### Step 4: Create Project Directory

1. Create a project directory with the naming convention: `project/[MS-NNN]_[Milestone-Description]/`
   - Example: `project/MS-001_Environment-Setup/`
   - Use Title Case for the description (capitalize first letter of each word)
   - Replace spaces with hyphens in the description
2. Use `mkdir -p` via Bash tool to create the directory
3. This directory will contain milestone-specific artifacts, notes, or temporary files

### Step 5: Explore Codebase

- Call `/explore <extracted-task-descriptions>` using `SlashCommand` tool
- Focus exploration on files and patterns relevant to the tasks
- Include context about acceptance criteria

### Step 6: Research Best Practices

- Call `/research <extracted-task-descriptions>` using `SlashCommand` tool
- Gather patterns and approaches specific to the implementation needs

### Step 7: Create Implementation Plan

- Call `/plan implementation <extracted-task-descriptions>` using `SlashCommand` tool
- Use `AskUserQuestion` to validate approach if there are ambiguities
- Include acceptance criteria and verification steps in the plan

### Step 8: Implement with TDD

- Call `/code <task-id>` using `SlashCommand` tool for each task sequentially
- For [P] parallel tasks without dependencies, note they can be reordered
- Mark each task as 🔄 In Progress when starting
- Mark each task as ✅ Completed when finished

### Step 9: Code Review

- Call `/code-review` using `SlashCommand` tool to review all changes
- Address any critical issues before proceeding

### Step 10: Verify Acceptance Criteria

Before finalizing, verify all acceptance criteria from `specs/tasks.md` are met:

- Run verification steps listed for the milestone
- If any criteria fail, address issues before marking complete

### Step 11: Finalize

- Update task status in `specs/tasks.md` from ⏳ to ✅
- If task was blocked (⚠️), update to ✅ when resolved
- Report implementation summary including:
  - Tasks completed
  - Acceptance criteria status
  - Any issues encountered

## Task Mapping Reference

| Phase                         | Milestones                                                                                             | Task Range |
| ----------------------------- | ------------------------------------------------------------------------------------------------------ | ---------- |
| Phase 1: Foundation           | MS-001, MS-002, MS-003                                                                                 | T001-T035  |
| Phase 2: UI Development       | MS-004, MS-005, MS-006, MS-007, MS-008, MS-009, MS-010, MS-011, MS-012, MS-013, MS-014, MS-015, MS-016 | T036-T160  |
| Phase 3: Backend Integration  | MS-017, MS-018, MS-019, MS-020, MS-021, MS-022                                                         | T161-T215  |
| Phase 4: Testing & Deployment | MS-023, MS-024, MS-025                                                                                 | T216-T245  |

## Milestone Task Ranges

| Milestone | Tasks     | Goal                                |
| --------- | --------- | ----------------------------------- |
| MS-001    | T001-T010 | Environment Setup                   |
| MS-002    | T011-T023 | Core Type Definitions & Zod Schemas |
| MS-003    | T024-T035 | Mock Infrastructure & API Layer     |
| MS-004    | T036-T045 | Authentication UI                   |
| MS-005    | T046-T057 | Tiptap Editor Integration           |
| MS-006    | T058-T066 | Auto-Save & Local Storage           |
| MS-007    | T067-T077 | Slash Command System                |
| MS-008    | T078-T087 | AI Autocomplete UI                  |
| MS-009    | T088-T098 | Note CRUD UI                        |
| MS-010    | T099-T106 | Note Organization UI                |
| MS-011    | T107-T114 | Trash System UI                     |
| MS-012    | T115-T124 | Settings & Subscription UI          |
| MS-013    | T125-T133 | Onboarding Flow UI                  |
| MS-014    | T134-T140 | Export Functionality                |
| MS-015    | T141-T150 | Responsive Design & Dark Mode       |
| MS-016    | T151-T160 | Accessibility                       |
| MS-017    | T161-T168 | Supabase Setup                      |
| MS-018    | T169-T177 | Real Authentication Integration     |
| MS-019    | T178-T186 | PowerSync Offline Sync              |
| MS-020    | T187-T193 | Sync Conflict Resolution            |
| MS-021    | T194-T203 | Real AI Integration                 |
| MS-022    | T204-T215 | Stripe Integration                  |
| MS-023    | T216-T226 | Testing Suite                       |
| MS-024    | T227-T234 | Performance Optimization            |
| MS-025    | T235-T245 | Deployment & Monitoring             |

## Subagent Tasks Reference

These 16 tasks are isolated and can be delegated to subagents:

| Milestone | SA Tasks                                       |
| --------- | ---------------------------------------------- |
| MS-002    | T011, T012, T013, T014, T018, T019, T020, T021 |
| MS-007    | T070, T071                                     |
| MS-009    | T097                                           |
| MS-011    | T112                                           |
| MS-014    | T134, T135                                     |
| MS-015    | T142                                           |
| MS-023    | T219                                           |

## Milestone Descriptions Reference

| Milestone | Description                         | Branch Name                                | Directory Name                                      |
| --------- | ----------------------------------- | ------------------------------------------ | --------------------------------------------------- |
| MS-001    | Environment Setup                   | `MS-001/environment-setup`                 | `project/MS-001_Environment-Setup/`                 |
| MS-002    | Core Type Definitions & Zod Schemas | `MS-002/core-type-definitions-zod-schemas` | `project/MS-002_Core-Type-Definitions-Zod-Schemas/` |
| MS-003    | Mock Infrastructure & API Layer     | `MS-003/mock-infrastructure-api-layer`     | `project/MS-003_Mock-Infrastructure-API-Layer/`     |
| MS-004    | Authentication UI                   | `MS-004/authentication-ui`                 | `project/MS-004_Authentication-UI/`                 |
| MS-005    | Tiptap Editor Integration           | `MS-005/tiptap-editor-integration`         | `project/MS-005_Tiptap-Editor-Integration/`         |
| MS-006    | Auto-Save & Local Storage           | `MS-006/auto-save-local-storage`           | `project/MS-006_Auto-Save-Local-Storage/`           |
| MS-007    | Slash Command System                | `MS-007/slash-command-system`              | `project/MS-007_Slash-Command-System/`              |
| MS-008    | AI Autocomplete UI                  | `MS-008/ai-autocomplete-ui`                | `project/MS-008_AI-Autocomplete-UI/`                |
| MS-009    | Note CRUD UI                        | `MS-009/note-crud-ui`                      | `project/MS-009_Note-CRUD-UI/`                      |
| MS-010    | Note Organization UI                | `MS-010/note-organization-ui`              | `project/MS-010_Note-Organization-UI/`              |
| MS-011    | Trash System UI                     | `MS-011/trash-system-ui`                   | `project/MS-011_Trash-System-UI/`                   |
| MS-012    | Settings & Subscription UI          | `MS-012/settings-subscription-ui`          | `project/MS-012_Settings-Subscription-UI/`          |
| MS-013    | Onboarding Flow UI                  | `MS-013/onboarding-flow-ui`                | `project/MS-013_Onboarding-Flow-UI/`                |
| MS-014    | Export Functionality                | `MS-014/export-functionality`              | `project/MS-014_Export-Functionality/`              |
| MS-015    | Responsive Design & Dark Mode       | `MS-015/responsive-design-dark-mode`       | `project/MS-015_Responsive-Design-Dark-Mode/`       |
| MS-016    | Accessibility                       | `MS-016/accessibility`                     | `project/MS-016_Accessibility/`                     |
| MS-017    | Supabase Setup                      | `MS-017/supabase-setup`                    | `project/MS-017_Supabase-Setup/`                    |
| MS-018    | Real Authentication Integration     | `MS-018/real-authentication-integration`   | `project/MS-018_Real-Authentication-Integration/`   |
| MS-019    | PowerSync Offline Sync              | `MS-019/powersync-offline-sync`            | `project/MS-019_PowerSync-Offline-Sync/`            |
| MS-020    | Sync Conflict Resolution            | `MS-020/sync-conflict-resolution`          | `project/MS-020_Sync-Conflict-Resolution/`          |
| MS-021    | Real AI Integration                 | `MS-021/real-ai-integration`               | `project/MS-021_Real-AI-Integration/`               |
| MS-022    | Stripe Integration                  | `MS-022/stripe-integration`                | `project/MS-022_Stripe-Integration/`                |
| MS-023    | Testing Suite                       | `MS-023/testing-suite`                     | `project/MS-023_Testing-Suite/`                     |
| MS-024    | Performance Optimization            | `MS-024/performance-optimization`          | `project/MS-024_Performance-Optimization/`          |
| MS-025    | Deployment & Monitoring             | `MS-025/deployment-monitoring`             | `project/MS-025_Deployment-Monitoring/`             |

## Prohibited Actions

- DO NOT accept free-form feature descriptions (use `/plan` for that)
- DO NOT bypass the workflow by calling agents directly
- DO NOT skip steps in the workflow sequence
- DO NOT call `/code` without completing `/plan` first
- DO NOT call `/code-review` with uncommitted changes
- DO NOT implement tasks beyond the specified scope
- DO NOT mark tasks as ✅ without verifying acceptance criteria
- DO NOT ignore blocked (⚠️) tasks without user acknowledgment

## Success Criteria

- [ ] Input correctly parsed as Task, Milestone, or Phase
- [ ] Blocked tasks (⚠️) identified and handled
- [ ] Prerequisites validated for milestone(s)
- [ ] All relevant task IDs extracted from specs/tasks.md
- [ ] Parallel [P] and subagent [SA] tasks identified
- [ ] Acceptance criteria extracted from specs/tasks.md
- [ ] Git branch created with format `[MS-NNN]/[milestone-description]`
- [ ] Project directory created at `project/[MS-NNN]_[Milestone-Description]/`
- [ ] `/explore` completed for the scope
- [ ] `/research` completed for the scope
- [ ] `/plan` completed with implementation strategy
- [ ] `/code` completed with passing tests and committed changes
- [ ] `/code-review` completed with no critical issues
- [ ] All acceptance criteria verified
- [ ] Task status updated in specs/tasks.md to ✅

## Examples

```bash
# Implement a single task
/implement T001

# Implement a range of tasks
/implement T001-T010

# Implement multiple specific tasks
/implement T001 T005 T010

# Implement a milestone
/implement MS-001

# Implement multiple milestones
/implement MS-001 MS-002

# Implement a phase (short form)
/implement P1

# Implement a phase (long form)
/implement Phase 1

# Implement phase range
/implement P1-P2
```

## Error Handling

### Invalid Input Format

If input does not match expected format, respond with:

```
Invalid input format. This command accepts:
- Tasks: T001, T001-T003, or T001 T005
- Milestones: MS-001, MS-001-MS-003, or MS-001 MS-005
- Phases: Phase 1, P1, Phase 1-3, or P1-P3

For free-form feature implementation, use /plan instead.
```

### Blocked Tasks

If tasks in scope have ⚠️ status, respond with:

```
Blocked tasks detected in scope:
- T[XXX]: [Description] - Blocked by [Blocker ID]

Options:
1. Skip blocked tasks and implement remaining
2. Abort and resolve blockers first

Which would you like to do?
```

### Prerequisites Not Met

If milestone prerequisites are not complete, respond with:

```
Prerequisites not met for [MS-XXX]:
- Required: [Prerequisite milestone(s)]
- Status: [Current status]

Options:
1. Proceed anyway (not recommended)
2. Implement prerequisites first

Which would you like to do?
```

### Acceptance Criteria Failed

If acceptance criteria verification fails, respond with:

```
Acceptance criteria not met:
- [ ] [Failed criterion 1]
- [ ] [Failed criterion 2]

The following verification steps failed:
- [Verification step and result]

Address these issues before marking tasks as complete.
```
