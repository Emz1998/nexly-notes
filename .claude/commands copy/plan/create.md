---
name: plan-create
description: Create implementation plan from research and codebase exploration reports by delegating to strategic-planner agent
allowed-tools: Task, Glob, Read
argument-hint: <user-instructions>
model: sonnet
---

**Goal**: Invoke the strategic-planner agent to create a comprehensive implementation plan based on validated research reports from the research-specialist
**User Instructions**: $ARGUMENTS

## Tasks

1. Locate the most recent validated research report in `project/*/research/research_*.md`
2. Verify the research report has `validated_by: research-consultant` in frontmatter
3. Invoke @agent-strategic-planner to create the implementation plan based on the research
4. Invoke @agent-plan-consultant to review the plan quality and completeness
5. Report the plan summary and location to user

## Subagent Delegation Prompt

Delegate to `strategic-planner` with this prompt:

```
Create an implementation plan for: $ARGUMENTS

## Required Research Input

Read and incorporate findings from the validated research report:
- Location: project/[MS-NNN]_[milestone-name]/research/research_[session-id]_[MMDDYY].md
- Ensure the report has validated_by: research-consultant in frontmatter

## Plan Requirements

Using the research findings, create a comprehensive implementation plan that includes:

1. **Objective & Scope**
   - Clear objective statement based on research conclusions
   - In-scope and out-of-scope boundaries

2. **Technical Setup & Requirements**
   - Dependencies and library recommendations from research
   - Configuration and environment setup

3. **Implementation Phases**
   - Break down into logical phases (3-5 phases)
   - Each phase with specific, actionable tasks
   - Consider deprecated patterns identified in research
   - Apply best practices from research findings

4. **Quality Gates**
   - Testing requirements at each phase
   - Code review checkpoints
   - Success criteria for phase completion

5. **Files to Be Modified/Created**
   - List all files that will be touched
   - New files to be created

6. **Risks & Mitigations**
   - Incorporate risks identified in research
   - Add implementation-specific risks
   - Provide mitigation strategies

## Output

Save the plan to: project/[MS-NNN]_[milestone-name]/plans/plan_[session-id]_[MMDDYY].md

Add frontmatter:
---
based_on_research: [path to research file]
created_by: strategic-planner
status: pending_review
---
```

## Prohibited Tasks

- DO NOT create plans without validated research input
- DO NOT skip the plan-consultant review
- DO NOT implement any code
- DO NOT modify research files
- DO NOT create plans that deviate from research recommendations without justification

## Success Criteria

- Research report located and verified as validated
- strategic-planner created comprehensive implementation plan
- Plan incorporates key findings from research (deprecated patterns, best practices)
- plan-consultant reviewed and rated the plan
- Plan file saved with proper frontmatter and location

## Examples

```bash
/plan:create offline-first sync implementation
/plan:create Supabase authentication flow
/plan:create Tiptap editor with AI autocomplete
```
