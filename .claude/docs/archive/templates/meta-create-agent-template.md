# /meta/create-agent Template

## Command
`/create-agent <agent-name> <target-department> <user-requirements> <required-tools>`

## Purpose
Create new specialized agents based on user requirements

## Output Structure

### Generated Agent File
**Location**: `.claude/agents/[department]/[agent-name].md`

```markdown
# [Agent Name]

## Purpose
[Clear description of agent's specialization]

## Department
[Engineering/QA/DevOps/Planning/etc.]

## Capabilities
- [Capability 1]
- [Capability 2]
- [Capability 3]

## Tools
### Required
- [Tool 1]: [Purpose]
- [Tool 2]: [Purpose]

### Restricted
- [Tool]: [Why restricted]

## Usage
### When to Use
- [Scenario 1]
- [Scenario 2]

### When NOT to Use
- [Scenario 1]
- [Scenario 2]

## Proactive Usage
[When to use without user prompt]

## Examples
### Example 1
user: "[Request]"
agent: [Response/Action]

### Example 2
user: "[Request]"
agent: [Response/Action]

## Integration
- **Works With**: [Other agents]
- **Preceded By**: [Agents]
- **Followed By**: [Agents]

## Performance
- **Model**: [claude-model]
- **Execution Time**: [Estimate]
- **Complexity**: [Low/Medium/High]
```

### Registry Update
**Location**: `.claude/agents/CLAUDE.md`

```markdown
### [Department]
- **[agent-name]**: [Purpose]
  - Tools: [List]
  - Proactive: [Yes/No]
```

## Department Structure
- **engineering**: Technical implementation
- **quality-assurance**: Testing and validation
- **devops**: Infrastructure and deployment
- **planning**: Project management
- **architect**: System design
- **research-strategy**: Analysis and research

## Process Flow
1. Validate agent name uniqueness
2. Parse user requirements
3. Determine department alignment
4. Validate tool requirements
5. Create agent from template
6. Update agent registry
7. Create department README

## Rules
- Unique kebab-case names
- Minimal tool permissions
- Clear, concise descriptions
- Well-defined proactive usage
- Seamless ecosystem integration
- Research/planning focus only

## Quality Gates
- Name follows conventions
- Purpose clearly defined
- Tools appropriately scoped
- Proactive guidelines clear
- Department integration smooth
- Documentation comprehensive
- No syntax errors