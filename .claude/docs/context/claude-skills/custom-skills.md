# Agent Skills - Complete Guide

## Overview

Agent Skills are modular capabilities that extend Claude's functionality through organized instructions, scripts, and resources. They package domain-specific expertise into discoverable, reusable capabilities that Claude uses automatically when relevant.

### Key Benefits

- **Specialize Claude**: Tailor capabilities for domain-specific tasks
- **Reduce repetition**: Create once, use automatically across conversations
- **Compose capabilities**: Combine Skills to build complex workflows
- **Share expertise**: Distribute knowledge across teams via git or plugins

### Core Principle: Progressive Disclosure

Skills leverage a three-level loading system to minimize context usage:

1. **Level 1 - Metadata (always loaded)**: Name and description from YAML frontmatter (~100 tokens per Skill)
2. **Level 2 - Instructions (loaded when triggered)**: SKILL.md body content (under 5k tokens recommended)
3. **Level 3 - Resources (loaded as needed)**: Additional files, scripts, and data (effectively unlimited)

Claude loads only what's needed for each specific task, keeping context usage efficient.

---

## How Skills Work

### Architecture

Skills run in a virtual machine with filesystem access, bash commands, and code execution. Think of Skills as directories containing:

- **Instructions**: Markdown files with procedural knowledge
- **Code**: Executable scripts that run without loading into context
- **Resources**: Reference materials, templates, schemas, examples

### Discovery and Invocation

**Model-invoked**: Claude autonomously decides when to use Skills based on the task and the Skill's description. Unlike slash commands (user-invoked), you don't explicitly call Skills—Claude discovers and uses them automatically.

**Example flow**:
1. User: "Extract text from this PDF"
2. Claude checks metadata and sees "pdf-processing" matches
3. Claude reads SKILL.md via bash
4. Claude optionally loads additional files if needed (FORMS.md, scripts, etc.)
5. Claude executes the task using Skill instructions

---

## Where Skills Work

### Claude Code
- **Custom Skills only** (no pre-built Skills)
- Filesystem-based: `~/.claude/skills/` (personal) or `.claude/skills/` (project)
- Full network access available
- Can install packages locally
- Shared via git or plugins

### Claude API
- **Pre-built Skills**: pptx, xlsx, docx, pdf
- **Custom Skills**: Upload via `/v1/skills` endpoint (workspace-wide)
- Requires beta headers: `code-execution-2025-08-25`, `skills-2025-10-02`, `files-api-2025-04-14`
- **No network access**, no runtime package installation

### Claude.ai
- **Pre-built Skills**: Automatic (pptx, xlsx, docx, pdf)
- **Custom Skills**: Upload as zip files (individual user only, not org-wide)
- Varying network access based on settings
- Available on Pro, Max, Team, Enterprise plans

### Claude Agent SDK
- **Custom Skills only**
- Place in `.claude/skills/`
- Enable by including `"Skill"` in `allowed_tools` configuration

---

## Creating Custom Skills

### Required Structure

Every Skill requires a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
[Clear, step-by-step guidance for Claude to follow]

## Examples
[Concrete examples of using this Skill]
```

### Field Requirements

**name**:
- Maximum 64 characters
- Must contain only lowercase letters, numbers, and hyphens
- Cannot contain XML tags or reserved words ("anthropic", "claude")
- Use gerund form (verb + -ing): `processing-pdfs`, `analyzing-spreadsheets`

**description**:
- Maximum 1024 characters
- Must be non-empty, no XML tags
- **Critical for discovery**: Include both what the Skill does AND when to use it
- Use third person: "Processes Excel files" not "I can help you process files"
- Include specific trigger terms and keywords

### File Organization

**Simple Skill** (single file):
```
my-skill/
└── SKILL.md
```

**Multi-file Skill** (with progressive disclosure):
```
my-skill/
├── SKILL.md              # Main instructions (loaded when triggered)
├── FORMS.md              # Form-filling guide (loaded as needed)
├── reference.md          # API reference (loaded as needed)
├── examples.md           # Usage examples (loaded as needed)
└── scripts/
    ├── analyze_form.py   # Utility script (executed, not loaded)
    ├── fill_form.py      # Form filling script
    └── validate.py       # Validation script
```

---

## Best Practices

### Writing Effective Descriptions

**Good - Specific with triggers**:
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Bad - Too vague**:
```yaml
description: Helps with documents
```

### Keep SKILL.md Concise

- Default assumption: Claude is already very smart
- Only add context Claude doesn't already have
- Keep SKILL.md body under 500 lines for optimal performance
- Challenge each piece of information: "Does Claude really need this explanation?"

**Good - Concise** (~50 tokens):
````markdown
## Extract PDF text

Use pdfplumber for text extraction:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

**Bad - Too verbose** (~150 tokens):
```markdown
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available...
```

### Set Appropriate Degrees of Freedom

Match specificity to task fragility:

**High freedom** (text instructions): Multiple approaches valid, decisions depend on context
**Medium freedom** (pseudocode/scripts with parameters): Preferred pattern exists, some variation acceptable
**Low freedom** (specific scripts, no parameters): Operations fragile, consistency critical

### Progressive Disclosure Patterns

**Pattern 1 - High-level guide with references**:
```markdown
# PDF Processing

## Quick start
[Basic instructions]

## Advanced features
**Form filling**: See [FORMS.md](FORMS.md)
**API reference**: See [REFERENCE.md](REFERENCE.md)
```

**Pattern 2 - Domain-specific organization**:
```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    └── marketing.md (campaigns, attribution)
```

**Pattern 3 - Conditional details**:
```markdown
## Creating documents
Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents
For simple edits, modify XML directly.
**For tracked changes**: See [REDLINING.md](REDLINING.md)
```

**Important**: Keep references one level deep from SKILL.md. Avoid deeply nested references.

---

## Workflows and Validation

### Use Workflows for Complex Tasks

Provide clear, sequential steps with checklists:

````markdown
## PDF form filling workflow

Copy this checklist and check off items as you complete them:

```
Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill the form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

**Step 1: Analyze the form**
Run: `python scripts/analyze_form.py input.pdf`

[Continue with detailed steps...]
````

### Implement Feedback Loops

**Pattern**: Run validator → fix errors → repeat

```markdown
## Document editing process

1. Make your edits to `word/document.xml`
2. **Validate immediately**: `python ooxml/scripts/validate.py unpacked_dir/`
3. If validation fails:
   - Review the error message carefully
   - Fix the issues in the XML
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild: `python ooxml/scripts/pack.py unpacked_dir/ output.docx`
```

---

## Advanced: Skills with Executable Code

### Solve, Don't Punt

Scripts should handle error conditions rather than punting to Claude:

**Good - Handle errors explicitly**:
```python
def process_file(path):
    """Process a file, creating it if it doesn't exist."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
    except PermissionError:
        print(f"Cannot access {path}, using default")
        return ''
```

### Provide Utility Scripts

Benefits of pre-made scripts:
- More reliable than generated code
- Save tokens (no code in context)
- Save time (no code generation)
- Ensure consistency across uses

**Make execution intent clear**:
- "Run `analyze_form.py` to extract fields" (execute)
- "See `analyze_form.py` for the extraction algorithm" (read as reference)

### Create Verifiable Intermediate Outputs

Use the "plan-validate-execute" pattern for complex operations:

```markdown
## Workflow
1. Analyze → **create plan file** → **validate plan** → execute → verify
2. Catches errors early with machine-verifiable validation
3. Reversible planning: iterate on plan without touching originals
```

---

## Evaluation and Iteration

### Build Evaluations First

**Evaluation-driven development**:
1. Identify gaps: Run Claude on tasks without a Skill, document failures
2. Create evaluations: Build 3+ scenarios testing these gaps
3. Establish baseline: Measure Claude's performance without the Skill
4. Write minimal instructions: Just enough to pass evaluations
5. Iterate: Execute evaluations, compare, refine

**Example evaluation**:
```json
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads the PDF file using appropriate library",
    "Extracts text from all pages without missing any",
    "Saves extracted text to output.txt in readable format"
  ]
}
```

### Develop Skills Iteratively with Claude

**Claude A** (expert) helps create/refine Skills → **Claude B** (agent) tests them in real tasks

**Creating a new Skill**:
1. Complete a task without a Skill, noting what context you provide
2. Identify the reusable pattern
3. Ask Claude A: "Create a Skill that captures this pattern"
4. Review for conciseness
5. Improve information architecture
6. Test with Claude B on similar tasks
7. Iterate based on observation

**Improving existing Skills**:
1. Use the Skill with Claude B in real workflows
2. Observe Claude B's behavior (struggles, successes, unexpected choices)
3. Return to Claude A with observations: "Claude B forgot to filter test accounts when..."
4. Review Claude A's suggestions
5. Apply and test changes
6. Repeat based on usage

---

## Claude Code Specifics

### Personal vs Project Skills

**Personal Skills** (`~/.claude/skills/`):
- Available across all your projects
- Your individual workflows and preferences
- Experimental Skills you're developing

**Project Skills** (`.claude/skills/`):
- Shared with your team via git
- Team workflows and conventions
- Project-specific expertise

**Plugin Skills**:
- Bundled with Claude Code plugins
- Automatically available when plugin is installed

### Tool Restrictions with allowed-tools

Limit which tools Claude can use when a Skill is active:

```yaml
---
name: safe-file-reader
description: Read files without making changes. Use when you need read-only file access.
allowed-tools: Read, Grep, Glob
---
```

Useful for:
- Read-only Skills that shouldn't modify files
- Limited scope workflows
- Security-sensitive operations

### Viewing and Testing Skills

**View available Skills**:
```bash
# Ask Claude directly
"What Skills are available?"

# Or check filesystem
ls ~/.claude/skills/
ls .claude/skills/
```

**Test a Skill**:
Ask questions matching your description—Claude autonomously decides to use the Skill if it matches.

### Sharing Skills

**Recommended**: Distribute through plugins

**Alternative**: Share via project repositories
```bash
# Add to project
mkdir -p .claude/skills/team-skill
# Create SKILL.md

# Commit to git
git add .claude/skills/
git commit -m "Add team Skill"
git push

# Team members get automatically on pull
git pull
```

---

## Common Patterns

### Template Pattern

**For strict requirements**:
````markdown
## Report structure

ALWAYS use this exact template structure:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
```
````

**For flexible guidance**:
````markdown
## Report structure

Here is a sensible default format, but use your best judgment:

```markdown
# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]
```

Adjust sections as needed for the specific analysis type.
````

### Examples Pattern

Provide input/output pairs:

````markdown
## Commit message format

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

Follow this style: type(scope): brief description, then detailed explanation.
````

### Conditional Workflow Pattern

```markdown
## Document modification workflow

1. Determine the modification type:

   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow:
   - Use docx-js library
   - Build document from scratch
   - Export to .docx format

3. Editing workflow:
   - Unpack existing document
   - Modify XML directly
   - Validate after each change
   - Repack when complete
```

---

## Anti-Patterns to Avoid

### Avoid

- **Windows-style paths**: Use forward slashes (`scripts/helper.py`), not backslashes
- **Offering too many options**: Provide a default with escape hatch, not endless choices
- **Time-sensitive information**: Use "old patterns" section instead of dates
- **Inconsistent terminology**: Choose one term and stick to it
- **Deeply nested references**: Keep all references one level deep from SKILL.md
- **Vague names**: Use descriptive names like `pdf-processing`, not `helper` or `utils`
- **Assuming tools are installed**: Explicitly list dependencies and installation

---

## Security Considerations

**Only use Skills from trusted sources**: those you created or obtained from Anthropic.

**Key security considerations**:
- Audit thoroughly: Review all files, scripts, images, resources
- External sources are risky: Skills fetching data from external URLs pose particular risk
- Tool misuse: Malicious Skills can invoke tools in harmful ways
- Data exposure: Skills with access to sensitive data could leak information
- Treat like installing software: Only use Skills from trusted sources

**Exercise extreme caution** with Skills from untrusted or unknown sources.

---

## Troubleshooting

### Claude doesn't use my Skill

**Check description**: Is it specific enough? Include both what it does AND when to use it.

**Check YAML syntax**:
```bash
cat SKILL.md | head -n 10
# Ensure opening/closing ---, valid YAML, no tabs
```

**Check location**:
```bash
ls ~/.claude/skills/*/SKILL.md  # Personal
ls .claude/skills/*/SKILL.md     # Project
```

### Skill has errors

**Check dependencies**: Claude will auto-install or ask permission for required packages

**Check script permissions**:
```bash
chmod +x .claude/skills/my-skill/scripts/*.py
```

**Check file paths**: Use forward slashes (Unix style) in all paths

### Multiple Skills conflict

Make descriptions specific with distinct trigger terms:

**Instead of**:
```yaml
description: For data analysis
description: For analyzing data
```

**Use**:
```yaml
description: Analyze sales data in Excel files and CRM exports. Use for sales reports, pipeline analysis, and revenue tracking.
description: Analyze log files and system metrics data. Use for performance monitoring, debugging, and system diagnostics.
```

---

## Quick Reference

### Minimum SKILL.md Template

```yaml
---
name: my-skill-name
description: What this does and when to use it with specific trigger keywords
---

# My Skill Name

## Instructions
[Clear steps for Claude to follow]

## Examples
[Concrete examples]
```

### Checklist for Effective Skills

**Core quality**:
- [ ] Description specific with both what and when
- [ ] SKILL.md body under 500 lines
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Examples concrete, not abstract
- [ ] File references one level deep

**Code and scripts**:
- [ ] Scripts solve problems, don't punt to Claude
- [ ] Error handling explicit and helpful
- [ ] No magic numbers (all values justified)
- [ ] Required packages listed
- [ ] No Windows-style paths

**Testing**:
- [ ] At least 3 evaluations created
- [ ] Tested with real usage scenarios
- [ ] Team feedback incorporated

### Key Locations

- **Personal Skills**: `~/.claude/skills/`
- **Project Skills**: `.claude/skills/`
- **Plugin Skills**: Bundled with plugins

### Resources

- [Agent Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Best Practices Guide](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Quickstart Tutorial](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart)
- [Skills Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/skills)
- [Engineering Blog: Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
