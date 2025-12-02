---
name: research
description: Research best practices and patterns by delegating to research-specialist and research-consultant agents
allowed-tools: Read, Glob, Grep, Task, WebSearch, WebFetch
argument-hint: <topic>
model: sonnet
---

**Goal**: Research best practices, patterns, and implementation approaches for a given topic

## Context

- Research topic: $ARGUMENTS
- Codebase context: @exploration/codebase-status*.md (most recent)

## Tasks

- T001: Delegate to `research-specialist` agent to research: $ARGUMENTS
- T002: Delegate to `research-consultant` agent to validate the research report
- T003: Commit the validated research file
- T004: Report research summary to user

## Subagent Delegations

### Step 1: Research Specialist

Delegate to `research-specialist` with this prompt:

```
Research topic: $ARGUMENTS

Using the codebase context from exploration, research:
1. Best practices for this domain
2. Implementation patterns and approaches
3. Library/framework recommendations
4. Potential risks and mitigations

Output: Create project/[milestone]/research/research_[session]_[date].md
```

### Step 2: Research Consultant

Delegate to `research-consultant` with this prompt:

```
Review and validate the research report at:
project/[milestone]/research/research_[session]_[date].md

Evaluate:
1. Research quality and completeness
2. Source reliability
3. Conclusion validity
4. Recommendation feasibility

Update frontmatter with: validated_by: research-consultant
```

## Deliverable

File: `project/[milestone]/research/research_[session]_[date].md`

Required frontmatter after validation:
```yaml
validated_by: research-consultant
```

## Implementation Strategy

- Use web search for current best practices
- Cross-reference multiple sources
- Consider project-specific constraints from exploration
- Ensure recommendations are actionable

## Prohibited Tasks

- DO NOT modify source code
- DO NOT create implementation plans
- DO NOT skip the research-consultant validation

## Success Criteria

- research-specialist agent produced research report
- research-consultant validated the report
- Frontmatter contains validated_by field
- Research file committed to version control

## Examples

```bash
/research OAuth2 vs JWT authentication
/research real-time sync patterns
/research state management libraries
```
