---
name: research-consult
description: Review research in project/[MS-NNN]_[milestone-name]/research/ and provide feedback and rating from 1-10
allowed-tools: Read, Glob, Grep, Task
model: sonnet
---

**Goal**: Review research documents and provide structured feedback with a quality rating (1-10)

## Context

- Research file to review: `$ARGUMENTS`
- Research files follow the naming pattern: `project/[MS-NNN]_[milestone-name]/research/research_[session-id]_[MMDDYY].md`
- This command delegates the actual review to the `research-consultant` agent

## Tasks

### Phase 1: Validation

- T001: Validate the research file path is provided in `$ARGUMENTS`
- T002: Check if the specified research file exists using Glob
- T003: If no argument provided, search for recent research files in `project/*/research/` directories

### Phase 2: Research Review

- T004: Delegate to the `research-consultant` agent using the Task tool with the following prompt:

```
Review the research document at: $ARGUMENTS

Perform the following analysis:

1. **Research Quality Assessment**
   - Review for completeness and accuracy
   - Validate all key questions have been addressed
   - Check for gaps in research coverage
   - Assess credibility and relevance of sources
   - Verify conclusions are supported by evidence

2. **Documentation Verification**
   - Cross-reference research claims against official documentation
   - Validate proposed solutions align with current API versions
   - Identify any outdated or deprecated approaches

3. **Provide Structured Feedback**
   - Generate a quality score (1-10) based on completeness and accuracy
   - List specific gaps, issues, or outdated information found
   - Provide actionable recommendations for improvement
   - Determine readiness to proceed to planning phase

Output the review using the Research Review Summary format.
```

### Phase 3: Report

- T005: Present the research-consultant's review to the user
- T006: Highlight the quality score and key recommendations

## Implementation Strategy

- Use Glob to locate research files if path is ambiguous
- Delegate all analysis work to the research-consultant agent
- Preserve the structured output format from the agent
- Ensure the rating is prominently displayed in the final output

## Prohibited Tasks

- DO NOT modify the research document
- DO NOT conduct new research
- DO NOT skip delegating to the research-consultant agent
- DO NOT provide ratings without the agent's analysis
- DO NOT implement any code changes

## Success Criteria

- Research file successfully located and validated
- research-consultant agent invoked with proper context
- Quality score (1-10) clearly presented
- Structured feedback with actionable recommendations provided
- Clear verdict (APPROVED/NEEDS REVISION) communicated to user
