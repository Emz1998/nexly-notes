---
name: explore
description: Analyze codebase structure and state by delegating to codebase-explorer agent
allowed-tools: Read, Glob, Grep, Task
argument-hint: <context>
model: sonnet
---

**Goal**: Explore the codebase to understand project structure, relevant files, and current state

## Context

- User context: $ARGUMENTS
- Tasks reference: @specs/tasks.md

## Tasks

- T001: Delegate to `codebase-explorer` agent to analyze the codebase for context: $ARGUMENTS
- T002: Report exploration findings summary to user

## Subagent Delegation

Delegate to `codebase-explorer` with this prompt:

```
Analyze the codebase for the following context: $ARGUMENTS

Produce a comprehensive status report including:
1. Project structure overview
2. Relevant files and their purposes
3. Dependencies and relationships
4. Current implementation state
5. Technical constraints and considerations

Output: Create exploration/codebase-status_[session]_[date].md
```

## Deliverable

File: `exploration/codebase-status_[session]_[date].md`

## Implementation Strategy

- Focus on understanding, not modifying code
- Identify patterns and conventions in the codebase
- Document technical debt and constraints
- Map dependencies between components

## Prohibited Tasks

- DO NOT modify any source code
- DO NOT create implementation plans
- DO NOT skip the codebase-explorer delegation

## Success Criteria

- codebase-explorer agent invoked with context
- Status file created with all required sections
- Exploration summary reported to user

## Examples

```bash
/explore authentication system
/explore T001 - User registration
/explore SPRINT-001 scope
```
