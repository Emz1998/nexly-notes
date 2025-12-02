---
name: code-review
description: Review committed code by delegating to code-reviewer agent
allowed-tools: Read, Glob, Grep, Task, Bash
argument-hint: [commit-range]
model: sonnet
---

**Goal**: Review committed code for quality, security, and best practices

## Context

- Commit range (optional): $ARGUMENTS (default: last commit)

## Tasks

- T001: Delegate to `code-reviewer` agent to review the committed changes
- T002: Report review findings and status to user

## Subagent Delegation

Delegate to `code-reviewer` with this prompt:

```
Review the committed changes: $ARGUMENTS (or last commit if not specified)

Evaluate:
1. Code quality and readability
2. Security vulnerabilities (OWASP Top 10)
3. Performance considerations
4. Best practices adherence
5. Test coverage adequacy

Produce a review report with:
- Summary of changes (200+ chars)
- Findings categorized by severity (critical, major, minor)
- Recommendations for improvement
- Approval status: APPROVED | CHANGES_REQUESTED | BLOCKED

Output: Create project/[milestone]/reviews/review_[session]_[date].md
```

## Deliverable

File: `project/[milestone]/reviews/review_[session]_[date].md`

Required sections:
- Summary (minimum 200 characters)
- Findings (categorized by severity)
- Recommendations
- Approval Status

## Review Status Definitions

| Status            | Meaning                          |
| ----------------- | -------------------------------- |
| APPROVED          | Code meets quality standards     |
| CHANGES_REQUESTED | Minor issues need addressing     |
| BLOCKED           | Critical issues prevent approval |

## Implementation Strategy

- Review all changed files systematically
- Check for security issues first (highest priority)
- Evaluate code against project conventions
- Provide actionable feedback

## Prohibited Tasks

- DO NOT modify any code during review
- DO NOT approve code with critical security issues
- DO NOT skip required review sections

## Success Criteria

- code-reviewer agent produced review report
- Report contains summary (200+ chars)
- Findings are categorized by severity
- Approval status is determined
- Review summary reported to user

## Examples

```bash
/code-review
/code-review abc123
/code-review main..feature-branch
/code-review HEAD~3..HEAD
```
