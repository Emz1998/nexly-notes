---
name: review-security
description: Review security vulnerabilities for files or directories by delegating to security-expert agent
allowed-tools: Read, Glob, Grep, Task
model: sonnet
---

**Goal**: Identify security vulnerabilities, anti-patterns, and attack vectors for specified files or directories
**User Instructions**: $ARGUMENTS (optional)

## Tasks

- T001: Validate the provided path exists and identify files to review
- T002: Delegate to `security-expert` agent to perform security analysis
- T003: Report security findings and remediation recommendations to user

## Subagent Delegation

Delegate to `security-expert` with this prompt:

```
Perform security review for: $ARGUMENTS

Analyze:
1. Hardcoded credentials, API keys, and sensitive tokens
2. SQL injection, XSS, and command injection vulnerabilities
3. Authentication and authorization flaws
4. Input validation and sanitization gaps
5. Insecure data handling and storage patterns
6. Dependency vulnerabilities and CVEs
7. API endpoint security (missing auth, rate limiting)
8. Configuration exposures and environment secrets

Produce a security report with:
- Overview of files and attack surface analyzed
- Vulnerabilities classified by OWASP/CWE categories
- Severity ratings (Critical, High, Medium, Low, Informational)
- Specific file locations and line numbers
- Exploitation scenarios and business impact
- Actionable remediation recommendations (without implementing fixes)
```

## Implementation Strategy

- Validate path exists before delegating to agent
- For directories, analyze all source files recursively
- Focus on OWASP Top 10 vulnerabilities
- Verify context to minimize false positives
- Provide specific line numbers for each finding
- Include both technical details and business impact

## Prohibited Tasks

- DO NOT modify any code during review
- DO NOT execute suspicious code or run dangerous commands
- DO NOT log or display actual values of hardcoded secrets
- DO NOT test exploits or attempt to trigger vulnerabilities
- DO NOT skip any of the analysis categories
- DO NOT review node_modules, dist, or build directories

## Success Criteria

- Target path validated and files identified
- security-expert agent completed analysis
- Vulnerabilities categorized by OWASP/CWE with severity ratings
- Specific file and line references provided for each finding
- Remediation recommendations documented
- Security summary reported to user

## Examples

```bash
# Review a specific file
/review:security src/lib/auth/session.ts

# Review a directory
/review:security src/lib/firebase/

# Review API routes
/review:security src/app/api/

# Review authentication flows
/review:security src/hooks/auth/
```
