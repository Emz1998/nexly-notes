# /strategize Command Template

## Command
`/strategize <instructions>`

## Purpose
Create implementation strategy based on research findings

## Output Structure

### Implementation Strategy
**Location**: `tmp/session_[session_id]/strategies/implementation_strategy.md`

```markdown
# Implementation Strategy

## Executive Summary
[2-3 sentence overview of strategy]

## Context Analysis
### Codebase State
- **Architecture**: [Current state]
- **Technologies**: [In use]
- **Patterns**: [Established]

### Research Synthesis
- **Key Finding 1**: [Impact on strategy]
- **Key Finding 2**: [Impact on strategy]
- **Key Finding 3**: [Impact on strategy]

## Strategic Approach

### Phase 1: Foundation
**Timeline**: [Duration]
**Objectives**:
1. [Objective 1]
2. [Objective 2]

**Tasks**:
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

**Dependencies**: [What's needed]
**Risks**: [Potential issues]

### Phase 2: Core Implementation
**Timeline**: [Duration]
**Objectives**:
1. [Objective 1]
2. [Objective 2]

**Tasks**:
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

**Dependencies**: [What's needed]
**Risks**: [Potential issues]

### Phase 3: Integration & Testing
**Timeline**: [Duration]
**Objectives**:
1. [Objective 1]
2. [Objective 2]

**Tasks**:
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Technical Decisions

### Architecture Choices
- **Decision 1**: [Choice] because [Rationale]
- **Decision 2**: [Choice] because [Rationale]

### Technology Stack
- **Frontend**: [Choices and reasons]
- **Backend**: [Choices and reasons]
- **Database**: [Choices and reasons]

### Design Patterns
- **Pattern 1**: [Where and why]
- **Pattern 2**: [Where and why]

## Implementation Guidelines

### Code Organization
```
src/
├── components/
├── services/
├── utils/
└── types/
```

### Naming Conventions
- Components: PascalCase
- Functions: camelCase
- Constants: UPPER_SNAKE_CASE

### Testing Strategy
- Unit tests for utilities
- Integration tests for services
- E2E tests for critical paths

## Risk Mitigation

### Technical Risks
- **Risk 1**: [Description] → [Mitigation]
- **Risk 2**: [Description] → [Mitigation]

### Schedule Risks
- **Risk 1**: [Description] → [Mitigation]
- **Risk 2**: [Description] → [Mitigation]

## Success Criteria
1. [Measurable criterion]
2. [Measurable criterion]
3. [Measurable criterion]

## Resource Requirements
- **Development Time**: [Estimate]
- **Tools**: [List]
- **Dependencies**: [List]

## Alternative Approaches

### Alternative 1
- **Description**: [What]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Why not chosen**: [Reason]

## Next Steps
1. Review and approve strategy
2. Begin Phase 1 implementation
3. Set up monitoring and tracking

## Appendix
### Research Documents Referenced
- [Document 1]
- [Document 2]
- [Document 3]

### Decision Log
- [Date]: [Decision made]
- [Date]: [Decision made]
```

## Process Flow
1. Read all research documents
2. Read exploration findings
3. Synthesize insights
4. Develop phased approach
5. Define technical decisions
6. Identify risks
7. Generate strategy document

## Dependencies
- All research reports from `/research`
- Codebase exploration from `/explore`

## Used By
- `/build` command (implements this strategy)