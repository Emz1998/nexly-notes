---
name: constitution
description: Generate the project constitution by delegating to the rules-enforcer agent
allowed-tools: Task, Read
argument-hint:
model: sonnet
---

Generate the project constitution file at `.claude/rules/constitution.md` by delegating to the rules-enforcer agent.

## 1. Context

This command creates the highest-level governance document for the NEXLY RN project by leveraging the specialized rules-enforcer agent.

- Purpose: Establish foundational principles, values, and constraints that govern all development
- Use case: When initializing project governance or updating constitutional rules
- Dependencies: @.claude/agents/architect/rules-enforcer.md, constitution template, existing codebase patterns
- Authority: The constitution serves as the ultimate reference for resolving conflicts or ambiguities

## 2. Tasks

**IMPORTANT !** Use TodoWrite tool to track the tasks that need to be completed.

### Phase 1: Preparation

- T001: Read the existing constitution file at `.claude/rules/constitution.md` (if it exists) to understand current state
- T002: Verify the rules-enforcer agent exists at `.claude/agents/architect/rules-enforcer.md`
- T003: Read CLAUDE.md to gather project context (tech stack, structure, workflows)

### Phase 2: Agent Delegation

- T004: Deploy the rules-enforcer agent using the Task tool with subagent_type='rules-enforcer'
- T005: Pass comprehensive context to the agent including:
  - Project name: NEXLY RN
  - Tech stack: React 19, Next.js, Tailwind v4, TypeScript, Dexie, Firebase
  - Development philosophy: TDD, MVP mindset, Desktop-first
  - Existing patterns from codebase analysis
- T006: Monitor agent execution and handle any clarification questions from the agent

### Phase 3: Validation & Finalization

- T007: Review the generated constitution for completeness and alignment with project goals
- T008: Verify all placeholders have been replaced with specific project values
- T009: Confirm the constitution file is saved at `.claude/rules/constitution.md`
- T010: Provide summary of constitutional principles established

## 3. Constraints / Rules

**CRITICAL: Follow these requirements exactly:**

### Delegation Requirements

- **DO NOT IMPLEMENT THE TASK YOURSELF** - You must delegate to the rules-enforcer agent
- The agent is responsible for:
  - Analyzing existing codebase patterns
  - Interviewing the user about coding preferences (if needed)
  - Filling the constitution template with specific, actionable rules
  - Ensuring no placeholders remain in the final document

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

## 4. Examples

### Good Usage Pattern

```bash
/constitution
```

**Result:**
- Deploys rules-enforcer agent to analyze NEXLY RN codebase
- Agent discovers patterns: TDD workflow, desktop-first approach, strict TypeScript usage
- Agent interviews user about ambiguous preferences (e.g., comment style, naming conventions)
- Generates comprehensive constitution with:
  - Core values: Simplicity, Evidence-based decisions, User value first, Quality non-negotiable
  - Development philosophy: TDD mandate, MVP mindset, No improvisation, Desktop-first
  - Technical standards: Type safety, Code clarity, Security by default, Performance consciousness
  - Real TypeScript/React patterns extracted from src/ directory
- Saves to `.claude/rules/constitution.md`

### Bad Patterns to Avoid

❌ Creating constitution manually without agent analysis
❌ Using generic rules that could apply to any project
❌ Leaving placeholder text like [PROJECT_NAME] or [EXAMPLE_CODE]
❌ Implementing the constitution yourself instead of delegating
❌ Skipping codebase pattern analysis or user preference gathering
❌ Creating contradictory or unenforceable rules

### Expected Agent Behavior

The rules-enforcer agent will:

1. **Discovery Phase:**
   - Read CLAUDE.md and project structure
   - Scan src/, components/, hooks/, lib/ for patterns
   - Extract 3-5 representative code samples
   - Identify ambiguous areas requiring clarification

2. **Interview Phase (if needed):**
   - Present discovered patterns to user for validation
   - Ask clarifying questions about preferences
   - Confirm priority ordering (type safety vs brevity, etc.)
   - Gather examples of preferred vs discouraged approaches

3. **Constitution Generation:**
   - Fill all sections with specific NEXLY RN values
   - Include real code examples from codebase
   - Create decision trees for common scenarios
   - Generate validation checklist based on TDD requirements

## 5. References

- @.claude/agents/architect/rules-enforcer.md (specialized constitution architect agent)
- `.claude/rules/constitution.md` (target output location - highest authority document)
- `CLAUDE.md` (project overview, structure, tech stack reference)
- `.claude/templates/` (constitution template and structure references)
- Existing codebase in `src/` (for pattern extraction and examples)

## 6. Output Format

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
