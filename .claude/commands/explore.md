---
name: explore
description: Analyze codebase structure and state by delegating to codebase-explorer agent
allowed-tools: Read, Glob, Grep, Task
argument-hint: <context>
model: sonnet
---

**Goal**: Explore the codebase to understand project structure, relevant files, and current state

## Workflow

- Invoke `codebase-explorer` agent to analyze the codebase for context: $ARGUMENTS
- Revise the quality of the exploration report
- Iterate and re-invoke the `codebase-explorer` agent until the exploration report is satisfactory

## Subagent Prompts

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
