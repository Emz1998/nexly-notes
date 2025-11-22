# /analyze Command Template

## Command
`/analyze <instructions>`

## Purpose
Research specific requirements for a feature and identify research topics with agent assignments

## Output Structure

### Required Research Topics Report
**Location**: `tmp/session_[session_id]/research/required_research_topics.md`

```markdown
# Required Research Topics

## Codebase Context
[Summary from codebase_exploration.md]

## Research Topics

### Topic 1: [Topic Name]
- **Description**: [What needs to be researched]
- **Rationale**: [Why this research is needed]
- **Agent**: [Assigned specialist agent]
- **Priority**: [High/Medium/Low]

### Topic 2: [Topic Name]
- **Description**: [What needs to be researched]
- **Rationale**: [Why this research is needed]
- **Agent**: [Assigned specialist agent]
- **Priority**: [High/Medium/Low]

## Agent Assignments

### Research Team
- **Agent 1**: [agent-name] - [research topic]
- **Agent 2**: [agent-name] - [research topic]
- **Agent 3**: [agent-name] - [research topic]

## Dependencies
- [List any dependencies between research topics]

## Timeline
- **Estimated Duration**: [Time estimate]
- **Parallel Tasks**: [Which can run simultaneously]

## Success Criteria
- [How to know research is complete]
```

## Process Flow
1. Read codebase exploration document
2. Identify research topics based on exploration
3. Match topics with appropriate specialist agents
4. Generate research requirements report

## Used By
- `/research` command (reads this output)