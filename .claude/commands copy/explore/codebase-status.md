---
name: codebase-status
description: Generate codebase status report by delegating to codebase-explorer agent
allowed-tools: Read, Glob, Grep, Task, Bash, Write
argument-hint: <additional-context>
model: sonnet
---

**Goal**: Invoke the codebase-explorer agent to analyze the codebase and generate a status report file
**User Instructions**: $ARGUMENTS (optional)

## Tasks

1. Read `project/status.json` to extract current milestone ID and description
2. Determine session ID from environment or generate placeholder
3. Create the exploration directory if it doesn't exist
4. Delegate to `codebase-explorer` agent with comprehensive analysis prompt
5. Collect exploration findings from the agent
6. Write the codebase-status report to the determined path
7. Report success with file location to user

## Subagent Delegation

Delegate to `codebase-explorer` agent with this prompt:

```
Perform a comprehensive codebase status analysis.

Additional context from user: $ARGUMENTS

Analyze and report on:

1. **Project Structure Overview**
   - Directory organization and key folders
   - Configuration files and their purposes
   - Build and development tooling

2. **Git Status & Recent Activity**
   - Current branch and staging state
   - Recent commits (last 10-15)
   - Modified, added, and deleted files

3. **Dependencies & Stack**
   - Core dependencies with versions
   - Development dependencies
   - Potential version conflicts or outdated packages

4. **Current Implementation State**
   - Work-in-progress features
   - Incomplete or pending changes
   - Technical debt indicators

5. **Technical Constraints & Considerations**
   - Configuration constraints
   - Integration points
   - Identified issues or warnings

Return a structured markdown report with all findings.
Output path: `project/[MS-NNN]_[milestone-description]/exploration/codebase-status_[session-id]_[MMDDYY].md`
```

## Prohibited Tasks

- DO NOT modify any source code files
- DO NOT run build scripts or test suites
- DO NOT expose sensitive information from environment files
- DO NOT skip the codebase-explorer agent delegation
- DO NOT write report outside the project/[milestone]/exploration/ directory
