---
name: create-command
description: Factory to create custom commands following best practices
allowed-tools: Read, Write, Glob
argument-hint: <command-name> <instruction>
model: sonnet
---

Create a new custom command named $1 with the purpose: $2

## 1. Context

- Purpose: Automate command creation following best practices and template standards
- Primary objective: Generate a new custom command file with proper structure and documentation
- Expected outcome: New command file saved to .claude/commands/ with complete template structure
- User Instructions: [$1 = command name, $2 = instruction/purpose of the command]

## 2. Tasks

**IMPORTANT !** Use TodoWrite tool to track the tasks that need to be completed. Include the ticket codes for each To Do item.

```TodoWrite
- [ ] T001: Read the command template from `.claude/templates/command-template.md`
- [ ] T002: Determine the appropriate command category/folder location (meta/, git/, etc.)
- [ ] T003: Parse the user's instruction to understand the command's purpose and scope
- [ ] T004: Identify required tools and permissions based on command functionality
- [ ] T005: Create the YAML frontmatter with metadata (name, description, allowed-tools, argument-hint, model)
- [ ] T006: Write the main instruction section with positional parameter references ($1, $2, etc.)
- [ ] T007: Generate the Context section with purpose, objectives, and user instructions
- [ ] T008: Create the Tasks section with logical phases and numbered task IDs (T001, T002, etc.)
- ... (Continue with the tasks that need to be completed)
```

### Phase 1: Preparation

- T001: Read the command template from `.claude/templates/command-template.md`
- T002: Determine the appropriate command category/folder location (meta/, git/, etc.)
- T003: Parse the user's instruction to understand the command's purpose and scope
- T004: Identify required tools and permissions based on command functionality

### Phase 2: Command Generation

- T005: Create the YAML frontmatter with metadata (name, description, allowed-tools, argument-hint, model)
- T006: Write the main instruction section with positional parameter references ($1, $2, etc.)
- T007: Generate the Context section with purpose, objectives, and user instructions
- T008: Create the Tasks section with logical phases and numbered task IDs (T001, T002, etc.)
- T009: Define Constraints/Rules section with critical requirements and quality standards

### Phase 3: Documentation & Validation

- T010: Add Examples section with good/bad patterns and concrete sample usage
- T011: Include References section with relevant file paths and dependencies
- T012: Define Output Format section with expected result structure
- T013: Write the command file to the determined location
- T014: Confirm successful creation with usage example and file path

## 3. Constraints / Rules

**CRITICAL: Follow these requirements exactly:**

### File Structure

- Must use the 6-section template structure (Context, Tasks, Constraints, Examples, References, Output Format)
- YAML frontmatter must include: name, description, allowed-tools, argument-hint, model
- Use positional parameters ($1, $2, $3) for arguments as defined in argument-hint
- Save to `.claude/commands/` or appropriate subfolder (e.g., `.claude/commands/meta/`, `.claude/commands/git/`)

### Tool Permissions

- Minimize tool permissions - only grant what's absolutely necessary
- Common patterns: Read/Write for file operations, Bash for git/npm/system commands, Task for agent delegation
- Use 'all' only when command truly needs unrestricted tool access
- Default to 'sonnet' model unless command is trivial (then use 'haiku')

### Task Organization

- Break down workflow into 3-5 logical phases (e.g., Preparation, Execution, Validation)
- Use sequential task IDs starting from T001, T002, T003, etc.
- Each task should be atomic, actionable, and clearly describe one operation
- Tasks should flow logically from preparation → execution → validation/completion

### Quality Standards

- Description should be concise and clear (1-2 lines maximum)
- Main instruction should clearly state what happens with each positional parameter
- All 6 sections must be present and properly populated (even if brief)
- Include at least one concrete usage example showing actual parameter values
- Constraints should specify both technical requirements and quality expectations

## 4. Examples

### Good Usage Pattern

```bash
/create-command analyze-performance "Analyze app performance metrics and identify bottlenecks"
```

**Result:** Creates `.claude/commands/analyze-performance.md` with:

- Proper 6-section template structure
- Clear phases for gathering metrics, analyzing data, generating reports
- Minimal tool permissions (Read, Glob, Bash)
- Concrete examples with actual file paths and commands

### Bad Patterns to Avoid

❌ Creating command file manually without using template structure
❌ Granting 'all' tools when only Read/Write are needed
❌ Missing critical sections like Tasks or Constraints
❌ Using vague task descriptions like "Do the thing" or "Handle it"
❌ No examples or only abstract examples without concrete values

### Pattern for Agent Delegation Commands

If creating a command that should delegate to a specialized agent:

- Add 'Task' to allowed-tools in frontmatter
- Include task in Phase 1 to invoke the appropriate agent (e.g., "T001: Deploy meta-command agent")
- Specify agent type clearly with @ syntax (e.g., "@agent-meta-command")
- Add constraint: "DO NOT IMPLEMENT THE TASK YOURSELF - delegate to [agent-name]"
- Example: create-hooks, create-agent, create-skills commands

## 5. References

- @.claude/templates/command-template.md (official command template structure)
- `.claude/commands/` (existing commands for reference and patterns)
- `.claude/commands/meta/` (meta-level commands that generate other artifacts)
- `.claude/docs/claude-tools.md` (comprehensive tool permissions reference)
- `.claude/agents/` (available agents for delegation patterns)

## 6. Output Format

```markdown
✅ Created new command: .claude/commands/{command-name}.md

**Command:** /{command-name}
**Description:** {brief description of what the command does}
**Usage:** /{command-name} {argument-hints}

Example:
/{command-name} {example-args}
```
