# /research Command Template

## Command
`/research <instructions>`

## Purpose
Conduct comprehensive parallel research using multiple specialist agents

## Output Structure

### Individual Research Reports
**Location**: `tmp/session_[session_id]/research/[topic_name].md`

```markdown
# Research: [Topic Name]

## Research Agent
- **Agent**: [agent-name]
- **Specialization**: [agent expertise]
- **Date**: [timestamp]

## Executive Summary
[Brief 2-3 sentence overview]

## Context7 Documentation
### Library: [library-name]
- **Version**: [version]
- **Key APIs**: [relevant APIs]
- **Best Practices**: [from docs]

## Research Findings

### Current State of Art
- **Industry Standards**: [What's common]
- **Latest Trends**: [What's emerging]
- **Best Practices**: [Recommended approaches]

### Technical Analysis
- **Approach 1**: [Description, Pros, Cons]
- **Approach 2**: [Description, Pros, Cons]
- **Approach 3**: [Description, Pros, Cons]

### Implementation Considerations
- **Complexity**: [Low/Medium/High]
- **Time Estimate**: [Hours/Days]
- **Dependencies**: [What's needed]
- **Risks**: [Potential issues]

### Recommendations
1. **Primary**: [Most recommended]
2. **Alternative**: [Backup option]
3. **Avoid**: [What not to do]

### Code Examples
```typescript
// Example implementation
```

### Resources
- **Documentation**: [Links]
- **Tutorials**: [Links]
- **Examples**: [Links]

### Integration Notes
- **With Existing Code**: [How to integrate]
- **Migration Path**: [If replacing something]
- **Testing Strategy**: [How to test]

## Conclusions
- **Key Takeaways**: [Main points]
- **Decision Factors**: [What to consider]
- **Next Steps**: [What to do next]
```

## Process Flow
1. Read required research topics
2. Launch agents in parallel
3. Each agent uses context7 first
4. Agents conduct deep research
5. Generate individual reports
6. Store in session directory

## Parallel Execution
- All agents run simultaneously
- Each produces independent report
- No blocking between agents

## Dependencies
- Required research topics from `/analyze`
- Context7 MCP server for documentation

## Used By
- `/strategize` command (reads all research)