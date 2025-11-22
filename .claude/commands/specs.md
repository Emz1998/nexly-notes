---
name: specs
description: Generate specification documents (tech-specs, prd, ui-ux, qa-specs) for features or projects
allowed-tools: Task, Read, Write, Glob, Grep
argument-hint: <spec-type> <feature-description>
model: sonnet
---

Generate a $1 specification document for: $2

## 1. Context

- Purpose: Automate the creation of comprehensive specification documents following project standards
- Primary objective: Generate well-structured specification documents tailored to the chosen spec type
- Expected outcome: Complete specification document saved to `.claude/docs/specs/` directory
- User Instructions: $2

## 2. Tasks

### Phase 1: Validation & Context Gathering

- T001: Validate that $1 is one of the allowed spec types: tech-specs, prd, ui-ux, qa-specs [P]
- T002: Read existing spec files from `.claude/docs/specs/` to understand format and structure [P]
- T003: Parse $2 to understand the feature scope, requirements, and objectives
- T004: Identify relevant codebase files and dependencies related to the feature

### Phase 2: Spec Generation

- T005: Generate the specification document based on the selected type
  - **tech-specs**: Technical architecture, system design, API contracts, data models, implementation approach
  - **prd**: Product requirements, user stories, acceptance criteria, success metrics, business objectives
  - **ui-ux**: User interface design, user flows, wireframes, accessibility requirements, interaction patterns
  - **qa-specs**: Test strategy, test cases, quality criteria, validation checklist, acceptance testing
- T006: Include sections appropriate to the spec type with comprehensive detail
- T007: Reference relevant existing documentation and codebase patterns
- T008: Add diagrams, code examples, or mockups where applicable

### Phase 3: Validation & Storage

- T009: Review generated spec for completeness and alignment with project standards
- T010: Ensure all critical sections are present and well-documented
- T011: Save the specification to `.claude/docs/specs/{spec-type}.md`
- T012: Provide summary of generated spec with key sections and next steps

## 3. Constraints / Rules

**CRITICAL: Follow these requirements exactly:**

### Spec Type Validation

- MUST validate that $1 matches exactly one of: `tech-specs`, `prd`, `ui-ux`, `qa-specs`
- If invalid spec type provided, HALT and inform user of valid options
- Spec type is case-sensitive and must use hyphen notation (not camelCase or snake_case)

### Document Structure Requirements

- **tech-specs** MUST include: Overview, Architecture, Data Models, API Contracts, Implementation Plan, Security Considerations, Testing Strategy
- **prd** MUST include: Executive Summary, Problem Statement, User Stories, Requirements, Success Metrics, Timeline, Dependencies
- **ui-ux** MUST include: Design Principles, User Flows, Component Specifications, Accessibility Requirements, Responsive Behavior, Design Tokens
- **qa-specs** MUST include: Test Objectives, Test Scope, Test Cases, Quality Criteria, Test Data, Validation Checklist, Bug Triage Process

### Quality Standards

- All specs MUST be written in clear, professional markdown
- Include practical examples, code snippets, or mockups where relevant
- Reference existing codebase patterns and project conventions from CLAUDE.md
- Align with project structure defined in `.claude/docs/specs/` directory
- Ensure specs are actionable and provide clear guidance for implementation

### File Management

- Save all specs to `.claude/docs/specs/` directory
- Use consistent naming: `{spec-type}.md` (e.g., `tech-specs.md`, `prd.md`)
- If spec already exists, ASK user if they want to overwrite or append
- Never delete existing specs without explicit user confirmation

## 4. Examples

### Good Usage Pattern

```bash
/specs tech-specs "Offline-first note synchronization with conflict resolution"
```

**Result:** Creates `.claude/docs/specs/tech-specs.md` with:

- Comprehensive technical architecture for offline sync
- Data models for conflict resolution
- API contracts for sync endpoints
- Implementation plan with phases
- Security considerations for data encryption

```bash
/specs prd "AI-powered nursing term autocomplete in note editor"
```

**Result:** Creates `.claude/docs/specs/prd.md` with:

- User stories for nursing students using autocomplete
- Acceptance criteria for term suggestion accuracy
- Success metrics (adoption rate, time saved)
- Dependencies on AI service and term dictionary

```bash
/specs ui-ux "Dark mode theme system with per-note preferences"
```

**Result:** Creates `.claude/docs/specs/ui-ux.md` with:

- User flow for toggling dark mode
- Component-level color token specifications
- Accessibility contrast requirements (WCAG AA)
- Responsive behavior across devices

```bash
/specs qa-specs "User authentication and session management"
```

**Result:** Creates `.claude/docs/specs/qa-specs.md` with:

- Test cases for login, logout, token refresh
- Security validation checklist
- Performance criteria (auth latency < 500ms)
- Edge cases and error handling tests

### Bad Patterns to Avoid

❌ `/specs technical "Add dark mode"` - Invalid spec type (use `tech-specs`)
❌ `/specs prd` - Missing feature description
❌ `/specs ui-ux design` - Too vague, needs specific feature description
❌ Creating specs manually without using this command
❌ Mixing multiple spec types in one document

## 5. References

- `.claude/docs/specs/` (existing specification documents)
- @CLAUDE.md (project structure, rules, and conventions)
- `.claude/docs/specs/prd.md` (product requirements reference)
- `.claude/docs/specs/tech-specs.md` (technical specifications reference)
- `.claude/docs/specs/ui-ux.md` (UI/UX design specifications reference)
- `.claude/docs/specs/qa-specs.md` (QA and testing specifications reference)

## 6. Output Format

**IMPORTANT !** Use TodoWrite tool to track the tasks that need to be completed.

```TodoWrite
- [ ] T001: Validate spec type parameter
- [ ] T002: Read existing spec files for format reference
- [ ] T003: Parse feature description
- [ ] T004: Identify relevant codebase dependencies
- [ ] T005: Generate specification document
- [ ] T006: Include all required sections
- [ ] T007: Reference relevant documentation
- [ ] T008: Add diagrams/examples
- [ ] T009: Review for completeness
- [ ] T010: Ensure alignment with standards
- [ ] T011: Save specification file
- [ ] T012: Provide summary and next steps
```

After completion, output:

```markdown
✅ Generated specification: .claude/docs/specs/{spec-type}.md

**Spec Type:** {spec-type}
**Feature:** {feature-description}
**File Location:** `.claude/docs/specs/{spec-type}.md`

**Key Sections Included:**

- {Section 1}
- {Section 2}
- {Section 3}
- ...

**Next Steps:**

- Review the specification for accuracy and completeness
- Share with relevant stakeholders for feedback
- Use as reference during implementation
- Update as requirements evolve
```
