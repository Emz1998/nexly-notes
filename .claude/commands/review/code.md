---
name: review-code
description: Review code quality for files or directories by delegating to code-reviewer agent
allowed-tools: Read, Glob, Grep, Task
argument-hint: <file-paths>
model: sonnet
---

**Goal**: Analyze code quality, security vulnerabilities, and best practices for specified files or directories

## Context

- Instructions: $ARGUMENTS (required - instructions for the code review)

## Tasks

- T001: Validate the provided path exists and identify files to review
- T002: Delegate to `code-reviewer` agent to analyze the code
- T003: Report review findings and recommendations to user

## Subagent Delegation

Delegate to `code-reviewer` with this prompt:

```
Review code quality for: $ARGUMENTS

Analyze:
1. Security vulnerabilities (injection, XSS, auth flaws, data exposure)
2. Code quality (SOLID principles, DRY, code smells, anti-patterns)
3. Performance issues (bottlenecks, inefficient algorithms, memory leaks)
4. Error handling and edge case coverage
5. Framework-specific best practices adherence

Produce a quality report with:
- Overview of files analyzed
- Findings categorized by severity (Critical, High, Medium, Low)
- Specific line references for each issue
- Actionable recommendations with code examples
- Quality score summary

Output: Create sessions/session_[MMDDYY]_[session-id]/code-reviews/code-review_[NNN].md
Sample File Path: `sessions/session_120325_ABCDE-123456-789012/code-reviews/code-review_001.md`

```

## Implementation Strategy

- Validate path exists before delegating to agent
- For directories, analyze all source files recursively
- Prioritize security issues in findings
- Provide specific line numbers for each finding
- Include concrete code examples for recommendations

## Prohibited Tasks

- DO NOT modify any code during review
- DO NOT skip security analysis
- DO NOT provide vague recommendations without line references
- DO NOT review node_modules, dist, or build directories

## Success Criteria

- Target path validated and files identified
- code-reviewer agent completed analysis
- Findings categorized by severity with line references
- Actionable recommendations provided
- Quality summary reported to user
