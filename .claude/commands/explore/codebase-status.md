---
name: codebase-status
description: Generate codebase status report by delegating to codebase-explorer agent
allowed-tools: Read, Glob, Grep, Task, Bash, Write
argument-hint: [additional-context]
model: sonnet
---

**Goal**: Invoke the codebase-explorer agent to analyze the codebase and generate a status report file

## Context

- Additional context: $ARGUMENTS
- Session ID: !`cat /tmp/claude_session_id 2>/dev/null || echo "unknown"`
- Current date: !`date +%m%d%y`
- Milestone info: !`cat project/status.json 2>/dev/null | head -10`

## Tasks

### Phase 1: Setup

- T001: Read `project/status.json` to extract current milestone ID and description
- T002: Determine session ID from environment or generate placeholder
- T003: Build output path: `project/[MS-NNN]_[milestone-description]/exploration/codebase-status_[session-id]_[MMDDYY].md`
- T004: Create the exploration directory if it doesn't exist

### Phase 2: Analysis Delegation

- T005: Delegate to `codebase-explorer` agent with comprehensive analysis prompt
- T006: Collect exploration findings from the agent

### Phase 3: Report Generation

- T007: Write the codebase-status report to the determined path
- T008: Report success with file location to user

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
```

## Implementation Strategy

- Extract milestone info from `project/status.json`
- Use format `[MS-NNN]_[Description]` for milestone directory
- Use format `codebase-status_[session-id]_[MMDDYY].md` for filename
- Ensure exploration directory exists before writing
- Delegate comprehensive analysis to codebase-explorer agent
- Write final report to the milestone's exploration folder

## Prohibited Tasks

- DO NOT modify any source code files
- DO NOT run build scripts or test suites
- DO NOT expose sensitive information from environment files
- DO NOT skip the codebase-explorer agent delegation
- DO NOT write report outside the project/[milestone]/exploration/ directory

## Success Criteria

- [ ] Milestone info extracted from project/status.json
- [ ] Output path correctly formatted with milestone, session, and date
- [ ] Exploration directory created if needed
- [ ] codebase-explorer agent successfully invoked
- [ ] Status report file created at the correct location
- [ ] User informed of the report file path

## Output Format

The generated report should be saved to:
`project/[MS-NNN]_[milestone-name]/exploration/codebase-status_[session-id]_[MMDDYY].md`

Example: `project/MS-001_Foundation/exploration/codebase-status_18e00b6f_120325.md`

## Examples

```bash
# Generate status report with default analysis
/codebase-status

# Generate status report focusing on authentication
/codebase-status authentication system changes

# Generate status report for specific feature area
/codebase-status editor components and styling
```
