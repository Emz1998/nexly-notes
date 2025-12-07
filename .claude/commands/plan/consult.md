---
name: plan-consult
description: Review implementation plans and provide feedback with quality rating (1-10 scale)
allowed-tools: Task, Glob, Read
argument-hint: <plan-file-path>
model: sonnet
---

**Goal**: Invoke the plan-consultant agent to review an implementation plan and provide comprehensive feedback with a quality rating (1-10)
**User Instructions**: $ARGUMENTS

## Context

- Plan file to review: `$ARGUMENTS`
- Plan files follow the naming pattern: `project/[MS-NNN]_[milestone-name]/plans/plan_[session-id]_[MMDDYY].md`
- This command delegates the actual review to the `plan-consultant` agent

## Tasks

1. Validate the plan file path is provided in `$ARGUMENTS`
2. If no argument provided, use Glob to find the most recent plan file in `project/*/plans/plan_*.md`
3. Invoke @agent-plan-consultant to review the plan and provide structured feedback
4. Present the plan-consultant's review to the user

## Subagent Delegation Prompt

Delegate to `plan-consultant` with this prompt:

```
Review the implementation plan at: $ARGUMENTS

Perform the following analysis:

1. **Plan Structure Analysis**
   - Evaluate organization, clarity, and logical flow
   - Assess completeness of requirements coverage
   - Identify missing sections or underdeveloped areas
   - Verify alignment with stated project objectives

2. **Best Practices Research**
   - Research best practices for the technologies and patterns proposed
   - Identify common pitfalls and anti-patterns for the approach
   - Evaluate whether the plan follows or deviates from standards

3. **Technical Feasibility Assessment**
   - Evaluate proposed architecture and design patterns
   - Assess complexity and implementation risk levels
   - Identify potential technical blockers or challenges
   - Review dependency management and integration points

4. **Provide Structured Feedback**
   - Generate a quality score (1-10) based on assessment criteria
   - Document strengths with specific examples from the plan
   - List improvement areas with research-backed recommendations
   - Determine readiness to proceed to implementation phase

Output the review using the Plan Review Report format with sources cited.
```

## Rating Criteria

| Score | Description |
|-------|-------------|
| 9-10 | Excellent: Comprehensive, follows best practices, ready for implementation |
| 7-8 | Good: Solid plan aligned with standards, minor gaps |
| 5-6 | Adequate: Covers basics but deviates from best practices in areas |
| 3-4 | Needs Work: Significant gaps, unclear approach, missing critical considerations |
| 1-2 | Insufficient: Major deficiencies, requires substantial rework |

## Prohibited Tasks

- DO NOT modify the plan file being reviewed
- DO NOT implement any code from the plan
- DO NOT skip delegating to the plan-consultant agent
- DO NOT provide ratings without the agent's analysis

## Success Criteria

- Plan file successfully located and validated
- plan-consultant agent invoked with proper context
- Quality score (1-10) clearly presented with justification
- Structured feedback with research-backed recommendations provided
- Clear verdict (APPROVED/NEEDS REVISION) communicated to user

## Examples

```bash
/plan:consult project/MS-001_auth/plans/plan_abc123_120325.md
/plan:consult  # Reviews most recent plan file
```
