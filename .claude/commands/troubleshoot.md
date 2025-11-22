---
name: debug
description: Systematically diagnose and analyze issues in the codebase
allowed-tools: Read, Grep, Glob, Bash, mcp__ide__getDiagnostics
argument-hint: <issue-description>
model: sonnet
---

Diagnose and analyze the following issue: $1

## 1. Context

- Purpose: Provide systematic debugging workflow to identify root causes of issues
- Primary objective: Analyze symptoms, gather diagnostic data, and identify the source of problems
- Expected outcome: Clear diagnosis with root cause analysis and suggested fixes
- User Instructions: [$1 = description of the issue or error to debug]

## 2. Tasks

**IMPORTANT:** Use TodoWrite tool track the tasks.

```TodoWrite
- [ ] T001: Parse the issue description to understand the problem domain [P]
- [ ] T002: Get language server diagnostics to identify TypeScript/linting errors [P]
- [ ] T003: Search for recent error logs in console output and log files [P]
- [ ] T004: Check git status and recent changes that might have introduced the issue
- [ ] T005: Identify relevant source files based on error messages or stack traces
- ... (Continue with the tasks that need to be completed)
```

### Phase 1: Information Gathering

- T001: Parse the issue description to understand the problem domain [P]
- T002: Get language server diagnostics to identify TypeScript/linting errors [P]
- T003: Search for recent error logs in console output and log files [P]
- T004: Check git status and recent changes that might have introduced the issue
- T005: Identify relevant source files based on error messages or stack traces

### Phase 2: Analysis & Investigation

- T006: Read the identified source files to understand the code context
- T007: Search for similar error patterns across the codebase
- T008: Check configuration files (tsconfig.json, next.config.js, package.json)
- T009: Verify dependencies and version compatibility
- T010: Run relevant diagnostic commands (type-check, lint, build)

### Phase 3: Root Cause Identification

- T011: Correlate findings to identify the root cause
- T012: Trace the error path through the codebase
- T013: Identify any breaking changes or conflicts
- T014: Document the chain of causation

### Phase 4: Solution Recommendation

- T015: Propose specific fixes based on root cause analysis
- T016: Identify potential side effects of proposed solutions
- T017: Suggest verification steps to confirm the fix
- T018: Document findings in a clear diagnostic report

## 3. Constraints / Rules

**CRITICAL: Follow these requirements exactly:**

### Systematic Approach

- Always start with language server diagnostics before manual investigation
- Follow the error chain from symptom to root cause systematically
- Do not jump to conclusions without gathering sufficient evidence
- Check both obvious and non-obvious related files (configs, types, dependencies)

### Evidence Collection

- Capture exact error messages, stack traces, and line numbers
- Note the context in which errors occur (build-time, runtime, specific actions)
- Check for multiple related errors that might share a common cause
- Verify the current state matches the user's description

### Analysis Quality

- Distinguish between symptoms and root causes
- Consider recent changes (git history) as potential triggers
- Check for environment-specific issues (Node version, missing env vars)
- Look for type mismatches, missing imports, and configuration conflicts

### Reporting Standards

- Provide file paths with line numbers for all identified issues
- Explain the causal chain clearly (A causes B which causes C)
- Suggest specific fixes with code examples where applicable
- Include verification steps to confirm the diagnosis

## 4. Examples

### Good Usage Patterns

```bash
/debug "Build failing with TypeScript error in components/editor"
```

**Expected workflow:**

1. Get IDE diagnostics for TypeScript errors
2. Search for recent changes in components/editor/
3. Check import paths and type definitions
4. Identify missing type export causing the error
5. Report with exact file:line and fix suggestion

```bash
/debug "Application crashes when clicking Save button"
```

**Expected workflow:**

1. Trace the Save button click handler in the code
2. Check console logs for runtime errors
3. Examine event handlers and async operations
4. Identify uncaught promise rejection
5. Report with stack trace analysis and fix

### Bad Patterns to Avoid

- Guessing at solutions without gathering diagnostics first
- Only checking the obvious file without investigating imports/dependencies
- Providing generic suggestions like "check your code" without specifics
- Missing the root cause by only addressing symptoms
- Not checking recent git changes for regression causes

## 5. References

- `src/` (main source code for investigation)
- `package.json` (dependency versions and scripts)
- `tsconfig.json` (TypeScript configuration)
- `next.config.js` (Next.js configuration)
- `.env.local` (environment variables)
- `.next/` (build output for build-time errors)

## 6. Output Format

```markdown
## Debug Report: {Issue Summary}

### Symptoms

- {Observed behavior}
- {Error messages}
- {Affected areas}

### Diagnostics

- Language Server: {TS/lint errors found}
- Build Status: {build output analysis}
- Runtime Logs: {console errors}
- Recent Changes: {relevant git history}

### Root Cause Analysis

**Primary Cause:** {Specific issue identified}
**Location:** {file:line references}
**Explanation:** {Why this causes the observed symptoms}

### Recommended Fixes

1. **Fix:** {Specific change needed}

   - **File:** {path:line}
   - **Change:** {code example or description}
   - **Reason:** {why this fixes the root cause}

2. **Verification Steps:**
   - [ ] {Step to verify fix}
   - [ ] {Step to test no regressions}

### Additional Notes

{Any relevant context, side effects, or follow-up considerations}
```
