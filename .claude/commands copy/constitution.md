---
name: constitution
description: Generate the project constitution by delegating to the rules-enforcer agent
allowed-tools: Task, Read
argument-hint:
model: sonnet
---

**Goal**: Generate the project constitution file at `.claude/rules/constitution.md` by delegating to the rules-enforcer agent

## Tasks

### Phase 1: Preparation

- T001: Read the existing constitution file at `.claude/rules/constitution.md` (if it exists) to understand current state
- T002: Verify the rules-enforcer agent exists at `.claude/agents/architect/rules-enforcer.md`
- T003: Read CLAUDE.md to gather project context (tech stack, structure, workflows)

### Phase 2: Agent Delegation

- T004: Deploy the rules-enforcer agent using the Task tool with subagent_type='rules-enforcer'
- T005: Pass comprehensive context to the agent including project name, tech stack, development philosophy, and existing patterns
- T006: Monitor agent execution and handle any clarification questions from the agent

### Phase 3: Validation & Finalization

- T007: Review the generated constitution for completeness and alignment with project goals
- T008: Verify all placeholders have been replaced with specific project values
- T009: Confirm the constitution file is saved at `.claude/rules/constitution.md`
- T010: Provide summary of constitutional principles established

## Implementation Strategy

- Delegate constitution generation to the specialized rules-enforcer agent rather than implementing manually
- Use the agent's pattern analysis capabilities to discover codebase conventions
- Leverage the agent's user interview feature for ambiguous preferences
- Ensure comprehensive context handoff including: NEXLY RN project name, React 19 + Next.js + Tailwind v4 + TypeScript tech stack, TDD development philosophy, desktop-first priority
- Validate generated output against quality standards before finalizing

## Constraints

### Delegation Requirements

- **DO NOT IMPLEMENT THE TASK YOURSELF** - You must delegate to the rules-enforcer agent
- The agent is responsible for: analyzing existing codebase patterns, interviewing the user about coding preferences (if needed), filling the constitution template with specific actionable rules, ensuring no placeholders remain in the final document

### Constitutional Principles

- The constitution is the highest authority in project documentation
- All other specs, rules, and documentation must align with constitutional values
- Constitutional principles override all other guidelines in case of conflict
- Changes to the constitution require explicit documentation and version increment

### Quality Standards

- Constitution must contain real code examples from the codebase (not generic examples)
- All rules must be specific, enforceable, and verifiable
- Decision trees must reflect actual scenarios developers will encounter
- Include explicit hierarchy: Constitution > PRD > Tech Specs > UI/UX Specs > QA Specs > Coding Rules

### Scope Boundaries

- Focus on establishing foundational principles and values
- Include technical standards (type safety, security, performance)
- Define collaboration and communication expectations
- Specify governance structure and change management processes

## Success Criteria

- [ ] Constitution file created at `.claude/rules/constitution.md`
- [ ] Rules-enforcer agent was used (not manual implementation)
- [ ] All template placeholders replaced with NEXLY RN specific values
- [ ] Real code examples extracted from the codebase are included
- [ ] Core values and development philosophy sections completed
- [ ] Technical standards reflect project's actual tech stack
- [ ] Document hierarchy established (Constitution > PRD > Tech Specs > etc.)
- [ ] Summary of established principles provided to user

## Patterns

### Agent Delegation Pattern

```
1. Gather context (CLAUDE.md, existing files, codebase patterns)
2. Deploy rules-enforcer agent via Task tool
3. Pass structured context to agent
4. Monitor execution and handle clarifications
5. Validate output quality
6. Report results to user
```

### Expected Agent Workflow

1. **Discovery Phase:** Read CLAUDE.md and project structure, scan src/ directories for patterns, extract representative code samples
2. **Interview Phase (if needed):** Present discovered patterns for validation, ask clarifying questions, confirm priority ordering
3. **Constitution Generation:** Fill all sections with specific values, include real code examples, create decision trees

## References

- @.claude/agents/architect/rules-enforcer.md (specialized constitution architect agent)
- `.claude/rules/constitution.md` (target output location - highest authority document)
- `CLAUDE.md` (project overview, structure, tech stack reference)
- `.claude/templates/` (constitution template and structure references)
- Existing codebase in `src/` (for pattern extraction and examples)

## Output Format

```markdown
✅ Constitution Generated Successfully

**Location:** .claude/rules/constitution.md
**Status:** Active
**Version:** 1.0

**Core Principles Established:**
- [List 3-5 key constitutional principles]

**Technical Standards Defined:**
- [List key technical mandates]

**Governance Structure:**
- Constitutional supremacy confirmed
- Specification hierarchy established
- Change management process defined

**Next Steps:**
- Review constitution for team alignment
- Ensure all project members understand constitutional principles
- Reference constitution when making technical decisions or resolving conflicts
```
