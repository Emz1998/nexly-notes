---
name: plan
description: Create a plan (project)
allowed-tools: Read, Glob, Grep, TodoWrite, Task
argument-hint: <special_instructions>
model: sonnet
---

Create a comprehensive implementation plan for the given task or feature: $1

## 1. Context

- Purpose: Formulate strategic plans for complex development tasks and features
- Primary objective: Break down requirements into actionable phases with clear dependencies
- Expected outcome: Structured plan with phases, tasks, constraints, and success criteria
- User Instructions: [$1 = special instructions or feature requirements to plan]

## 2. Tasks

**IMPORTANT !** Use TodoWrite tool to track the planning process.

### Phase 1: Analysis & Context Gathering

- T001: Parse user requirements and identify core objectives [P]
- T002: Search codebase for related implementations and patterns [P]
- T003: Identify technical dependencies and constraints [P]
- T004: Review project specs (PRD, tech-specs, UI/UX specs) for alignment
- T005: Determine scope boundaries (MVP vs future enhancements)

### Phase 2: Strategy Formulation

- T006: Define high-level approach and architectural decisions
- T007: Break down work into logical phases (typically 3-5 phases)
- T008: Identify tasks within each phase with sequential IDs (T001, T002, etc.)
- T009: Mark tasks that can be executed in parallel with `[P]` notation
- T010: Define success criteria and validation checkpoints

### Phase 3: Risk & Dependency Analysis

- T011: Identify technical risks and mitigation strategies
- T012: Map dependencies between tasks and phases
- T013: Determine required tools and agent delegations
- T014: Estimate complexity and identify potential blockers
- T015: Define rollback strategies for critical changes

### Phase 4: Documentation & Presentation

- T016: Document constraints and quality requirements
- T017: Provide concrete examples and usage patterns
- T018: List reference files and documentation
- T019: Define expected output format and deliverables
- T020: Present plan for user approval using ExitPlanMode tool

## 3. Constraints / Rules

**CRITICAL: Follow these requirements exactly:**

### MVP-First Approach

- Prioritize simple, lean solutions over complex architectures
- Build for desktop web first, mobile second (as per project rules)
- Focus on core functionality, defer nice-to-haves to future phases
- Avoid over-engineering and premature optimization
- Keep implementation practical and testable

### TDD Compliance

- Every feature must include test planning
- Follow Red-Green-Refactor cycle in task breakdown
- Include test tasks in each implementation phase
- Ensure test coverage for critical business logic
- Plan for both unit and integration tests

### Structured Planning

- Use 3-5 logical phases (e.g., Setup, Implementation, Testing, Validation)
- Number tasks sequentially within phases (T001, T002, T003, etc.)
- Mark parallelizable tasks with [P] notation
- Each task must be atomic and actionable
- Include validation checkpoints between phases

### Agent Delegation

- Use Task tool with appropriate subagent when needed for deep analysis
- Delegate to codebase-explorer for understanding current state
- Delegate to strategic-planner for complex multi-path decisions
- Use Explore agent for codebase pattern discovery
- Clearly specify when agent delegation is required vs optional

### Quality Standards

- Plans must align with project specs (PRD, tech-specs, UI/UX)
- Follow coding rules from @.claude/rules/coding.md
- Never improvise beyond defined scope
- Stop and ask if uncertain about requirements
- Include rollback/recovery strategies for risky changes

## 4. Examples

### Good Planning Pattern

```bash
/plan "Implement offline-first note synchronization with conflict resolution"
```

**Expected Process:**

1. Analyze existing sync mechanisms in codebase
2. Review Dexie and Firebase integration patterns
3. Break down into phases: Schema Updates → Sync Logic → Conflict Resolution → Testing
4. Identify parallel tasks (e.g., schema updates + UI components)
5. Define success criteria (sync latency, conflict handling accuracy)
6. Present structured plan with TodoWrite tracking

### Bad Patterns to Avoid

❌ Creating vague phases like "Implementation" without breaking down tasks
❌ Not identifying which tasks can run in parallel
❌ Skipping risk analysis and dependency mapping
❌ Planning beyond MVP scope without user approval
❌ Ignoring TDD requirements in task breakdown
❌ Not using TodoWrite to track planning progress

### Example Plan Structure

```markdown
## Phase 1: Foundation (3 tasks, 2 parallel)

- T001: Update Dexie schema for sync metadata [P]
- T002: Create sync status UI components [P]
- T003: Write tests for schema changes

## Phase 2: Core Sync Logic (4 tasks, sequential)

- T004: Implement local change detection
- T005: Build Firebase sync orchestrator
- T006: Add network status monitoring
- T007: Write integration tests for sync flow

## Phase 3: Conflict Resolution (3 tasks)

- T008: Design conflict detection algorithm [P]
- T009: Implement three-way merge strategy [P]
- T010: Create conflict resolution UI

## Phase 4: Validation (2 tasks, sequential)

- T011: Run full test suite and fix failures
- T012: Perform manual testing with offline scenarios
```

## 5. References

- @.claude/docs/specs/prd.md (product requirements and scope)
- @.claude/docs/specs/tech-specs.md (technical architecture and standards)
- @.claude/docs/specs/ui-ux.md (design system and user experience guidelines)
- @.claude/rules/coding.md (coding standards and best practices)
- `.claude/agents/` (available agents for delegation)
- `src/lib/dexie/` (IndexedDB implementation patterns)
- `src/lib/firebase/` (Firestore sync patterns)
- `src/hooks/data/` (data management hooks for reference)

## 6. Output Format

Use the ExitPlanMode tool to present the final plan:

```markdown
## Implementation Plan: {Feature Name}

### Overview

- Objective: {Clear statement of what will be built}
- Scope: {MVP boundaries and what's excluded}
- Success Criteria: {Measurable outcomes}

### Phase 1: {Phase Name}

- T001: {Task description} [P if parallel]
- T002: {Task description}
  ...

### Phase 2: {Phase Name}

- T00X: {Task description}
  ...

### Risks & Mitigations

- Risk: {Description} → Mitigation: {Strategy}

### Dependencies

- {Task ID} depends on {Task ID}

### Validation Checkpoints

- After Phase 1: {What to verify}
- After Phase 2: {What to verify}
```
