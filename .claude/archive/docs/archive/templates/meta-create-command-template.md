# /meta/create-command Template

## Command
`/create-command <command-name> <subfolder-name> <task-instructions> <task-complexity>`

## Purpose
Intelligent factory to create custom commands following best practices

## Output Structure

### Generated Command File
**Location**: `.claude/commands/[subfolder]/[command-name].md`

```yaml
---
name: [command-name]
description: [Clear purpose statement]
argument-hint: <arg1> <arg2> ...
model: [claude-model-id]
allowed-tools: [Only if bash required]
---

[Command content based on complexity]
```

### Command Documentation Update
**Location**: `.claude/commands/CLAUDE.md`

```markdown
## [Command Name]
- **Location**: `.claude/commands/[subfolder]/[command-name].md`
- **Purpose**: [Description]
- **Arguments**: [List]
- **Complexity**: [Simple/Complex]
- **Model**: [Model used]
```

## Complexity Analysis

### Simple Tasks
- Single file/module changes
- Can be explained in one sentence
- Low risk of breaking production
- < 5 minutes execution time
- No coordination required

### Complex Tasks
- Multi-module changes
- Requires detailed explanation
- High risk if done wrong
- Multiple steps/retries needed
- Requires coordination

## Model Selection
- **claude-opus-4-1**: High-level planning/strategy
- **claude-sonnet-4**: Regular coding tasks
- **claude-3-7-sonnet**: Simple coding tasks
- **claude-3-5-haiku**: Non-coding tasks

## Process Flow
1. Analyze task complexity
2. Read custom commands guide
3. Determine arguments needed
4. Select appropriate model
5. Create command from template
6. Update documentation

## Rules
- Use positional parameters
- Support multiple modes per parameter
- Follow template structure
- Minimize tool permissions
- Keep prompts concise
- Focus on research/planning (not coding)

## Prohibited
- Sections beyond template
- Headers > 3 levels deep
- Emojis or tables
- Verbose prompts
- Excessive permissions
- Multiple unrelated functions
- Code implementation in subagents