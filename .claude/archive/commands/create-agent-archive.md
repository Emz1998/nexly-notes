---
name: create-agent
description: Generate a new AI agent following the strict template structure
tools: Read, Write, Grep, Glob, mcp__sequentialthinking__sequentialthinking, TodoWrite
argument-hint: <agent-name> <role-description> <instructions>
model: claude-opus-4-1-20250805
---
## 1. Arguments Description

- **Name of the agent to be created**: $1
- **Role Description of the agent to be created**: $2
- **User Instructions**: ${3:-none}

## 2. Workflow

### Phase 1: Analyze Arguments & Requirements

- Parse and validate arguments from $ARGUMENTS
- Extract agent name, role description, and category
- If missing arguments, generate appropriate defaults or prompt user
- Use sequential thinking (minimum 5 thoughts) to understand agent purpose
- Determine appropriate tools and responsibilities based on role

### Phase 2: Validate Agent Configuration

- Check for existing agents with similar names using Glob
- Verify category directory exists and aligns with role
- Validate agent name follows kebab-case convention
- Ensure role description is meaningful and specific
- Analyze existing agents for overlap and integration points
- Validate tool requirements comprehensively
- Ensure no duplicate responsibilities across agents
- Check for naming conflicts across all categories

### Phase 3: Generate Agent Content

- Read and parse agent template from @docs/templates/agent-template.md
- Use sequential thinking for comprehensive agent design
- Create detailed YAML frontmatter with all required fields:
    - name, description, tools, model
    - proactive flag if applicable
- Choose appropriate tools based on role from @.claude/docs/claude-tools
- Generate 4-5 core responsibilities with detailed subtasks
- Add 3 comprehensive use case examples with full context
- Include complete instructions and deliverables sections
- Ensure all sections follow template structure strictly

### Phase 4: Finalize and Save

- Write agent file to `.claude/agents/[category]/[agent-name].md`
- Update or create CLAUDE.md in category directory
- Add agent information to registry
- Verify file follows all documentation rules
- Ensure no emojis per project standards

### Phase 5: Generate Report

- Create completion report using reporting template
- Document agent creation details and specifications
- Save report to `reports/`
- Include summary of agent capabilities and use cases

## 3. Rules and Guidelines




- Agent names must be kebab-case and descriptive
- Place agents in correct category directories under .claude/agents/
- Validate no existing agent with same name before creation
- Tools list must be minimal and necessary for agent's role
- Use cases must be specific and actionable
- Don't use brackets "[]" in the YAML frontmatter
- Follow documentation rules from @rules/documentation-rules.md for agent documentation
- Generate 4-5 core responsibilities, 3 comprehensive use cases, complete instructions per section
- If a `CLAUDE.md` file exists in the category directory, update it with the new agent information. If not, create a new `CLAUDE.md` file in the category directory and fill up with appropriate information.
- Choose the most appropriate folder inside @.claude/agents to place the generated agent.

## 4. References    

### Project Documentation

- **Agent Template:** @docs/templates/agent-template.md
- **Reporting Template:** @.claude/docs/templates/reporting-template.md
- **Agent Registry:** @.claude/agents/CLAUDE.md
- **Documentation Rules:** @rules/documentation-rules.md
- **Coding Rules:** @rules/coding-rules.md
- **Project Overview:** @CLAUDE.md
- **Claude Tools List:** @.claude/docs/claude-tools.md
- **Best Practices:** @.claude/references/research-ai-agent-coding-standards-20250109.md

## 5. Deliverables

- New agent file at `.claude/agents/[category]/[agent-name].md`
- Report at `/reports/`

---