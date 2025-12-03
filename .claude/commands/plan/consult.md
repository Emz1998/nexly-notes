---
name: plan-consult
description: Review implementation plans and provide feedback with quality rating (1-10 scale)
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
argument-hint: <plan-file-path>
model: sonnet
---

**Goal**: Review an implementation plan from `project/[MS-NNN]_[milestone-name]/plans/plan_[session-id]_[MMDDYY].md` and provide comprehensive feedback with a quality rating from 1-10.

## Context

- Plan file to review: `$ARGUMENTS`
- If no argument provided, search for the most recent plan file in `project/*/plans/plan_*.md`

## Tasks

### Phase 1: Plan Discovery and Loading

- T001: If `$ARGUMENTS` is provided, read the specified plan file directly
- T002: If no argument provided, use Glob to find all plan files matching `project/*/plans/plan_*.md`
- T003: Sort discovered plans by date (from filename MMDDYY) and select the most recent
- T004: Read the plan file contents completely

### Phase 2: Plan Analysis

- T005: Analyze the plan's structure (sections, organization, clarity)
- T006: Evaluate technical approach and architectural decisions
- T007: Identify potential risks, gaps, or missing considerations
- T008: Research industry best practices relevant to the plan's domain using WebSearch
- T009: Cross-reference with project specs in `specs/` directory if applicable

### Phase 3: Feedback Generation

- T010: Document strengths of the plan
- T011: Document areas for improvement
- T012: Provide specific, actionable recommendations
- T013: Calculate and assign quality rating (1-10 scale)
- T014: Generate structured feedback report

## Implementation Strategy

- Use a holistic approach: evaluate clarity, feasibility, completeness, and alignment with best practices
- Provide constructive feedback that enables improvement rather than just criticism
- Research current best practices to ensure recommendations are up-to-date
- Consider the project context from CLAUDE.md and specs when evaluating

## Rating Criteria

| Score | Description |
|-------|-------------|
| 9-10 | Excellent: Comprehensive, well-structured, addresses all concerns, ready for implementation |
| 7-8 | Good: Solid plan with minor gaps or areas for improvement |
| 5-6 | Adequate: Acceptable plan but missing significant considerations or clarity |
| 3-4 | Needs Work: Major gaps, unclear structure, or questionable technical decisions |
| 1-2 | Insufficient: Incomplete, unclear, or fundamentally flawed approach |

## Prohibited Tasks

- DO NOT modify the plan file being reviewed
- DO NOT implement any code from the plan
- DO NOT skip the research phase for best practices
- DO NOT provide ratings without justification

## Success Criteria

- [ ] Plan file successfully located and read
- [ ] All plan sections analyzed for quality and completeness
- [ ] Industry best practices researched and referenced
- [ ] Specific strengths identified with examples
- [ ] Specific improvement areas identified with actionable recommendations
- [ ] Quality rating provided with clear justification
- [ ] Feedback formatted in structured report format

## Output Format

```markdown
# Plan Review Report

## Plan Details
- **File**: [plan file path]
- **Date**: [date from filename]
- **Milestone**: [milestone from path]

## Quality Rating: [X]/10

### Rating Justification
[Explanation of the rating]

## Strengths
1. [Strength 1 with specific example]
2. [Strength 2 with specific example]
...

## Areas for Improvement
1. [Issue 1]
   - **Impact**: [How this affects the plan]
   - **Recommendation**: [Specific actionable fix]
2. [Issue 2]
   - **Impact**: [How this affects the plan]
   - **Recommendation**: [Specific actionable fix]
...

## Best Practices Alignment
- [How the plan aligns or deviates from industry best practices]

## Risk Assessment
- [Identified risks and mitigation suggestions]

## Summary
[Brief overall assessment and next steps]
```
