---
name: build
description: Build features, sprint features, or components based on instructions
allowed-tools: Bash(npm:*), Bash(git:*), Bash(ls:*), Bash(grep:*), Bash(find:*)
argument-hint: <build-type> <target-name> <instructions>
model: claude-sonnet-4-20250514

---
## 1. Arguments Analysis

- `build-type`: ${1:-feature}
- `target-name`: ${2:-unnamed-feature}
- `instructions`: ${3:-"Build a standard feature implementation"}

- If `build-type` is `feature`, then build a single feature based on instructions
- If `build-type` is `sprint-feature`, then build multiple related features for a sprint
- If `build-type` is `component`, then build a reusable component

## 2. Workflow

**Important!** Create a TODO list to track the tasks that need to be completed using `TodoWrite` tool:
```TodoWrite
- [ ] Phase 1: Gather Context
- [ ] Phase 2: Plan
- [ ] Phase 3: Execute
- [ ] Phase 4: Validate
```

### Phase 1: Gather Context

**Important!** Delegate the context gathering tasks to the agents below:

**Agent 1**: `system-architect` 
- Research codebase and identify architectural patterns
- Find similar implementations in codebase
- Catalog reusable components and patterns
- Document relevant specifications and context
- Assess technical feasibility
- Store findings in `.claude/context/agent-docs/`

### Phase 2: Plan

**Important!** Delegate the planning tasks to the agents below:

**Agent 1**: `design-system-architect` 
- Design component architecture and integration strategy
- Define component structure and interfaces
- Identify integration points with existing code
- Document design patterns to apply
- Create UI/UX consistency plan
- Save architectural decisions in `.claude/context/agent-docs/`

### Phase 3: Execute

- **Important!** Read the documentations in the @.claude/context/agent-docs from subagents implemented in  `Phase 1` and `Phase 2`
- Receive and synthesize outputs from Phase 0-2 agents
- Implement core functionality based on architectural design
- Build required components following design system
- Integrate with existing systems per architecture plan
- Apply identified design patterns and best practices
- Ensure FERPA/HIPAA compliance in implementation
- Maintain accessibility standards (WCAG)
- Update context memory with implementation details

### Phase 4: Validate

**Important!** Delegate the validation tasks to the agents below:

**Agent 1**: `code-reviewer`
- Verify functionality against requirements
- Validate code quality and standards compliance
- Check error handling implementation
- Verify integration points
- Perform security and compliance checks
- Document validation results in `.claude/context/agent-docs/`

## 3. **Important** Rules

- **Important!** Follow existing code conventions and patterns
- **Important!** Ensure FERPA/HIPAA compliance for healthcare education features
- **Important!** Maintain accessibility standards (WCAG)
- Use existing libraries and utilities before adding new dependencies
- Implement proper error handling and validation
- Follow security best practices
- All subagents must update their documentation in `.claude/context/agent-docs/`

## 4. Quality Gates

**Important!** Quality gates are a set of criteria that must be met for the command to complete the task successfully.

- Feature functionality matches the provided instructions
- Code follows project conventions and style guide
- Implementation is accessible and compliant
- Proper error handling is in place
- Code is modular and maintainable
- Integration points are properly tested
- All agent documentation is complete

## 5. Agents Scope

**Important!** You are limited to the agents listed below for this command

- **prd-architect**: Product requirements analysis and feature planning
- **system-architect**: System design and architecture decisions
- **react-specialist**: React component architecture and patterns
- **typescript-specialist**: TypeScript implementation and type safety
- **design-system-architect**: Design system integration and consistency
- **code-reviewer**: Code quality and standards validation
- **documentation-specialist**: Technical documentation and knowledge capture

## 6. Useful Documentation

- **Product Requirements Document(PRD)**: @docs/planning/prd.md
- **Project Overview**: @CLAUDE.md
- **Agent System**: @.claude/agents/CLAUDE.md
- **Commands Registry**: @.claude/commands/CLAUDE.md
- **Design System**: @prototype/
- **Development Rules**: @docs/development/
- **Architecture Patterns**: @docs/templates/

## 7. Context Memory Management

**Important!** Before starting tasks, read these relevant documentations first:
- Read `Main Context` documentation @.claude/context/main-context/context-memory_[session-id].md
- Read system-architect documentation @.claude/context/agent-docs/system-architect/[task-description]-[session-id].md
- Read design-system-architect documentation @.claude/context/agent-docs/design-system-architect/[task-description]-[session-id].md
- Read code-reviewer documentation @.claude/context/agent-docs/code-reviewer/[task-description]-[session-id].md

## 8. Deliverables

- Implemented feature files in appropriate directories
- Updated or new components as required
- Integration with existing codebase
- Context memory update with build outcomes
- Complete agent documentation in `.claude/context/agent-docs/`

---