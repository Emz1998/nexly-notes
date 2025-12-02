---
name: plan
description: Create implementation plan by delegating to strategic-planner and consulting-expert agents
allowed-tools: Read, Write, Glob, Grep, Task
argument-hint: <plan-type> <plan-name> <description>
model: sonnet
---

**Goal**: Create a detailed implementation plan based on research findings

## Context

- Plan type: $1 (e.g., feature, refactor, migration)
- Plan name: $2
- Description: $3
- Research context: @project/*/research/research*.md (most recent validated)

## Tasks

- T001: Delegate to `strategic-planner` agent to create the implementation plan
- T002: Delegate to `consulting-expert` agent to review and consult on the plan
- T003: Report plan summary to user

## Subagent Delegations

### Step 1: Strategic Planner

Delegate to `strategic-planner` with this prompt:

```
Create implementation plan for: $2 - $3
Plan type: $1

Using the validated research findings, create:
1. Executive summary
2. Implementation phases with task breakdowns
3. Risk mitigation strategies
4. Success criteria and acceptance tests
5. Dependencies and constraints

Output: Create project/[milestone]/plans/plan_[session]_[date].md
```

### Step 2: Consulting Expert

Delegate to `consulting-expert` with this prompt:

```
Review the implementation plan at:
project/[milestone]/plans/plan_[session]_[date].md

Evaluate:
1. Technical feasibility
2. Risk assessment accuracy
3. Resource allocation
4. Alternative approaches considered
5. Potential blind spots

Update frontmatter with: consulted_by: consulting-expert
Provide actionable feedback and recommendations.
```

## Deliverable

File: `project/[milestone]/plans/plan_[session]_[date].md`

Required frontmatter after consultation:
```yaml
consulted_by: consulting-expert
```

## Implementation Strategy

- Base plan on validated research findings
- Break down into atomic, testable tasks
- Include clear success criteria for each phase
- Document dependencies between tasks

## Prohibited Tasks

- DO NOT implement any code
- DO NOT skip the consulting-expert review
- DO NOT create plans without research context

## Success Criteria

- strategic-planner agent produced implementation plan
- consulting-expert reviewed and consulted on the plan
- Frontmatter contains consulted_by field
- Plan includes phased task breakdown

## Examples

```bash
/plan feature user-auth "User authentication with OAuth2"
/plan refactor state-management "Migrate to Zustand"
/plan migration database "Upgrade to Prisma v5"
```
