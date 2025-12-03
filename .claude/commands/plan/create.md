---
name: plan-create
description: Create implementation plan from research and codebase exploration reports by delegating to strategic-planner agent
allowed-tools: Read, Write, Glob, Grep, Task
argument-hint: <user-instructions>
model: sonnet
---

**Goal**: Create a detailed implementation plan by analyzing research and codebase exploration reports for a specific milestone

## Context

- Milestone ID: $1 (e.g., MS-001, MS-002)
- Research reports: `project/$1_*/research/research_*_*.md`
- Codebase exploration reports: `project/$1_*/explore/explore_*_*.md`

## Tasks

### Phase 1: Report Discovery

- T001: Locate the milestone folder matching pattern `project/$1_*`
- T002: Find the most recent research report in `project/$1_*/research/research_*_*.md`
- T003: Find the most recent codebase exploration report in `project/$1_*/explore/explore_*_*.md`
- T004: Validate that both reports exist before proceeding

### Phase 2: Report Analysis

- T005: Read and analyze the research report content
- T006: Read and analyze the codebase exploration report content
- T007: Extract key findings, recommendations, and constraints from both reports

### Phase 3: Plan Generation

- T008: Delegate to `strategic-planner` agent with combined research and exploration context
- T009: Verify the plan was created at `project/$1_*/plans/plan_[session-id]_[MMDDYY].md`
- T010: Report plan summary to user

## Subagent Delegation

### Strategic Planner

Delegate to `strategic-planner` agent with this prompt:

```
Create an implementation plan based on the following research and codebase exploration findings.

## Research Report
[Content from research_[session-id]_[MMDDYY].md]

## Codebase Exploration Report
[Content from explore_[session-id]_[MMDDYY].md]

## Instructions
Using these validated findings:
1. Synthesize key insights from both research and exploration reports
2. Identify implementation opportunities and constraints
3. Create phased implementation plan with task breakdowns
4. Define success criteria and acceptance tests
5. Document dependencies and risk mitigations

Output: Create plan at project/[milestone]/plans/plan_[session-id]_[date].md
```

## Implementation Strategy

- Always verify both reports exist before delegating to strategic-planner
- Use glob patterns to find most recent reports when multiple exist
- Pass full content of both reports to strategic-planner for comprehensive analysis
- Ensure plan references source reports in its metadata

## Prohibited Tasks

- DO NOT create a plan if research report is missing
- DO NOT create a plan if codebase exploration report is missing
- DO NOT implement any code
- DO NOT modify the source reports

## Success Criteria

- Research report located and read successfully
- Codebase exploration report located and read successfully
- strategic-planner agent created implementation plan
- Plan saved to `project/[milestone]/plans/plan_[session-id]_[MMDDYY].md`
- Plan references both source reports

## Examples

```bash
# Create plan from MS-001 reports
/plan-from-reports MS-001

# Create plan from MS-002 reports
/plan-from-reports MS-002

# Create plan from MS-010 reports
/plan-from-reports MS-010
```

## References

- Research reports: `project/[MS-NNN]_[milestone-name]/research/research_[session-id]_[MMDDYY].md`
- Exploration reports: `project/[MS-NNN]_[milestone-name]/explore/explore_[session-id]_[MMDDYY].md`
- Output location: `project/[MS-NNN]_[milestone-name]/plans/plan_[session-id]_[MMDDYY].md`

## Output Format

The command will:

1. Report which research and exploration files were found
2. Confirm delegation to strategic-planner
3. Provide path to the generated plan file
4. Display brief summary of the plan's key phases
