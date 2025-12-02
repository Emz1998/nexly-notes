---
name: skills
description: Generate custom Agent Skills with effective triggers and progressive disclosure
allowed-tools: Write, Read, Grep, Bash
argument-hint: <requirements>
model: sonnet
---

**Goal**: Create a new Agent Skill with requirements: $ARGUMENTS

## Tasks

### Phase 1: Read Standards

- T001: Read @.claude/templates/skills.md for template structure
- T002: Read @.claude/context/claude-skills/custom-skills.md for complete standards
- T003: Read `.claude/context/claude-skills/best-practices.md`

### Phase 2: Validate & Create

- T004: Validate name ($1): gerund form, lowercase-hyphen, ≤64 chars, no reserved words
- T005: Craft description: what it does + when to use it, ≤1024 chars, third person, specific triggers
- T006: Generate directory structure: `mkdir -p .claude/skills/[skill-name]/references`
- T007: Write SKILL.md to `.claude/skills/$1/SKILL.md` following template

### Phase 3: Validate Output

- T008: Verify valid YAML frontmatter (opening/closing ---)
- T009: Verify name meets all naming rules
- T010: Verify description has triggers + use cases, ≤1024 chars
- T011: Verify body <500 lines with concrete examples
- T012: Verify all sections present: Context, Workflow, Implementation Strategy, Constraints, Success Criteria

## Implementation Strategy

- Name must use gerund form: `processing-pdfs`, `analyzing-data`, `writing-tests`
- Name: lowercase letters, numbers, hyphens only (≤64 chars)
- Name forbidden words: XML tags, "anthropic", "claude"
- Description: third person ("Processes Excel files" not "I can help you")
- Description: include capabilities AND trigger keywords
- File structure:
  ```
  .claude/skills/$1/
  ├── SKILL.md          # Required
  ├── references/       # Required
  ├── scripts/          # Optional
  └── templates/        # Optional
  ```

## Prohibited Tasks

- Do not use first person in descriptions
- Do not exceed 64 chars for name or 1024 chars for description
- Do not create skills without trigger-rich descriptions
- Do not use vague names (must be gerund and specific)
- Do not skip reading the template and standards first

## Success Criteria

- SKILL.md created at `.claude/skills/[skill-name]/SKILL.md`
- Name is gerund form, lowercase-hyphen, ≤64 chars
- Description contains triggers and use cases, ≤1024 chars
- Body is <500 lines with concrete examples
- All required sections populated
- Output format provided:

  ```markdown
  ## Skill Created

  **Location:** `.claude/skills/[skill-name]/SKILL.md`
  **Name:** $1
  **Description:** [trigger-rich description]
  **Triggers:** [key activation terms]
  **Test:** "[sample query to trigger this skill]"

  **Validation:**

  - Name: gerund, lowercase-hyphen
  - Description: <1024 chars with triggers
  - Body: <500 lines
  - Structure: follows template
  ```

## Examples

**Good:**

```
/create-skills analyzing-spreadsheets "Process Excel files to extract insights and generate reports. Use for .xlsx files, data analysis, or financial reports."
```

Creates: gerund name, specific triggers (Excel, .xlsx, data analysis), clear use case

**Bad:**

```
/create-skills helper "Helps with stuff"
```

Problems: not gerund, no triggers, vague
