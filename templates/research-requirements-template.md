# /research-requirements Command Template

## Command
`/research-requirements <instructions>`

## Purpose
Identify and document research topics with agent assignments

## Output Structure

### Required Research Topics
**Location**: `tmp/session_[session_id]/research/required_research_topics.md`

```markdown
# Required Research Topics

## Codebase Analysis
[Summary from exploration]
- **Architecture**: [Type]
- **Stack**: [Technologies]
- **Patterns**: [Observed]

## Research Topics Identified

### Topic 1: [Name]
- **Category**: [Technical/Design/Architecture]
- **Description**: [What to research]
- **Rationale**: [Why needed]
- **Priority**: [High/Medium/Low]
- **Assigned Agent**: [specialist-name]
- **Estimated Time**: [Duration]

### Topic 2: [Name]
- **Category**: [Technical/Design/Architecture]
- **Description**: [What to research]
- **Rationale**: [Why needed]
- **Priority**: [High/Medium/Low]
- **Assigned Agent**: [specialist-name]
- **Estimated Time**: [Duration]

## Agent Assignments

### Technical Research
- **react-typescript-specialist**: [Topics]
- **firebase-specialist**: [Topics]
- **ai-integration-specialist**: [Topics]

### Design Research
- **ui-design-researcher**: [Topics]
- **ux-specialist**: [Topics]
- **design-system-architect**: [Topics]

### Architecture Research
- **system-architect**: [Topics]
- **database-architect**: [Topics]

## Research Dependencies
- **Sequential**: [Topics that depend on others]
- **Parallel**: [Topics that can run together]
- **Blockers**: [What must complete first]

## Expected Outputs
- **Reports**: [Number] individual reports
- **Format**: Markdown documents
- **Location**: `tmp/session_[id]/research/`

## Success Criteria
- All topics have assigned agents
- Research covers all identified gaps
- Documentation is comprehensive
- Best practices are identified

## Timeline
- **Start**: [When]
- **Duration**: [Estimated total time]
- **Completion**: [Expected finish]
```

## Process Flow
1. Read codebase exploration
2. Analyze gaps and needs
3. Identify research topics
4. Match topics to agents
5. Define dependencies
6. Generate assignment report

## Used By
- `/research` command (executes these assignments)