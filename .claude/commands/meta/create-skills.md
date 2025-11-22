---
name: create-skills
description: Generate custom Agent Skills with effective triggers and progressive disclosure
allowed-tools: Write, Read, Grep, Bash
argument-hint: <skill-name> <description-and-requirements>
model: sonnet
---

Create a new Agent Skill named $1 with requirements: $2

## 1. Context

- Purpose: Generate custom Agent Skills following Anthropic's standards for Claude Code
- Primary objective: Create `.claude/skills/$1/SKILL.md` with proper structure and trigger-rich descriptions
- Expected outcome: Functional Agent Skill that Claude automatically discovers and uses when relevant
- Skills must follow three-level loading pattern (metadata → instructions → resources)

## 2. Instructions

- Read Anthropic's skill standards from `.claude/context/claude-skills/` documentation
- Validate skill name ($1) against naming rules (gerund form, lowercase-hyphen, ≤64 chars)
- Craft trigger-rich description from $2 requirements (max 1024 chars, includes capabilities and use cases)
- Generate SKILL.md with valid YAML frontmatter and concise body (under 500 lines)
- Create skill directory structure with required `SKILL.md` and `references/` folder
- Run validation checklist to ensure all standards are met

## 3. Workflow

### Phase 1: Preparation and Validation

- Must Read @.claude/context/claude-skills/custom-skills.md for complete standards
- Read PROACTIVELY `.claude/context/claude-skills/best-practices.md`
- Read PROACTIVELY `.claude/context/claude-skills/claude-code-skills.md`
- Read PROACTIVELY `.claude/context/claude-skills/quickstart.md`
- Read PROACTIVELY `.claude/context/claude-skills/overview.md`
- Read PROACTIVELY `.claude/context/claude-skills/creating-custom-skills.md`
- Validate skill name ($1): check length ≤ 64 chars, lowercase-hyphen format, gerund form
- Verify no reserved words (XML tags, "anthropic", "claude")

### Phase 2: Content Creation

- Craft trigger-rich description from $2 requirements
- Include what the skill does (capabilities)
- Include when to use it (trigger keywords and specific use cases)
- Ensure description is maximum 1024 characters
- Design SKILL.md structure with proper YAML frontmatter:

```markdown
---
name: [validated $1]
description: [trigger-rich description]
---

# [Title Case Name]

## Instructions

[Concise, step-by-step guidance - assume Claude is smart]

## Examples

[Concrete input/output examples]

## [Optional sections as needed]
```

### Phase 3: File Generation and Validation

- Create directory: `mkdir -p .claude/skills/$1`
- Write SKILL.md to `.claude/skills/$1/SKILL.md`
- Create `references/` subdirectory
- Run validation checklist:
  - [ ] YAML frontmatter valid (opening/closing ---)
  - [ ] Name meets all naming rules
  - [ ] Description specific with triggers
  - [ ] Body under 500 lines
  - [ ] No time-sensitive information
  - [ ] Consistent terminology
  - [ ] Concrete examples included
  - [ ] File references one level deep

## 4. Constraints / Rules

**CRITICAL: Follow these requirements exactly:**

### Naming Rules (for $1 parameter)

- Maximum 64 characters
- Lowercase letters, numbers, hyphens only
- Use gerund form (verb + -ing): `processing-pdfs`, `analyzing-data`, `writing-tests`
- Cannot contain: XML tags, "anthropic", "claude"

### Description Rules (in YAML frontmatter)

- Maximum 1024 characters
- Must include BOTH what it does AND when to use it
- Use third person: "Processes Excel files" not "I can help you"
- Include specific trigger terms and keywords
- No XML tags

### SKILL.md Structure

- YAML frontmatter with `name` and `description`
- Concise body under 500 lines (challenge every explanation)
- Only add context Claude doesn't already have
- Use concrete examples, not abstract explanations
- Keep file references one level deep from SKILL.md

### File Organization

- Create directory: `.claude/skills/$1/`
- Required: `SKILL.md` and `references/` folder
- Optional: `scripts/`, `templates/`, `README.md`
- Use Unix-style paths (forward slashes)
- File Structure:

```
.claude/skills/$1/
├── SKILL.md
├── references/
├── scripts/                           # Optional: scripts for the skill
├── README.md                          # Optional: README for the skill
├── templates/                         # Optional: templates folder for the skill
└── [Optional folder]/                 # Optional: any other folder for the skill
```

## 5. Examples

**Good usage:**

```
/create-skills analyzing-spreadsheets "Process Excel files to extract insights, generate reports, and identify trends. Use when working with .xlsx files, data analysis, or financial reports."
```

**Creates:**

- Specific triggers: "Excel", "spreadsheets", ".xlsx", "data analysis"
- Gerund name: "analyzing-spreadsheets"
- Clear use case in description

**Bad usage:**

```
/create-skills helper "Helps with stuff"
```

**Problems:**

- Vague name (not gerund, not specific)
- No triggers in description
- No clear use case

## 6. References

- `.claude/context/claude-skills/custom-skills.md` - Complete skill standards
- `.claude/context/claude-skills/best-practices.md` - Best practices for skill creation
- `.claude/context/claude-skills/claude-code-skills.md` - Claude Code skill guidelines
- `.claude/context/claude-skills/quickstart.md` - Quick start guide
- `.claude/context/claude-skills/overview.md` - Skill system overview
- `.claude/context/claude-skills/creating-custom-skills.md` - Detailed creation guide

## 7. Output Format

After creating the skill, provide:

```markdown
## ✅ Skill Created Successfully

**Location:** `.claude/skills/$1/SKILL.md`

**Name:** $1

**Description:** [The trigger-rich description you wrote]

**Trigger Keywords:** [List key terms that will activate this skill]

**Test Phrase:** "[A sample user query that should trigger this skill]"

**Structure:**

- SKILL.md (XXX lines)
- [List any additional files created]

**Validation:**
✅ Name valid (gerund form, lowercase-hyphen)
✅ Description under 1024 chars with triggers
✅ Body under 500 lines
✅ YAML frontmatter valid
[Additional checks...]
```
