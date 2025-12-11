---
name: code
description: Implement code using TDD workflow - delegates to test-engineer and troubleshooter agents
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite
argument-hint: <task-id>
model: sonnet
---

**Goal**: Implement code following TDD (Test-Driven Development) workflow

## Workflow

1. Invoke @agent-test-engineer to create failing tests
2. Invoke @agent-version-manager to commit the changes
3. Invoke @agent-fullstack-developer to write the initial code
4. Invoke @agent-code-reviewer to perform a peer review of the code
5. Read the code review report and make necessary changes till the feedback rating is at least 9/10
6. Once the code is reviewed and approved, invoke @agent-version-manager to commit the changes

**Important**: If there are errors, bugs, or issues, invoke @agent-troubleshooter to fix the issues.

**Important**: If the code review feedback rating is less than 9/10, make the necessary changes, invoke @agent-code-reviewer to review the code again and repeat the process until the feedback rating is at least 9/10.

**Important**: agent-fullstack-developer is only responsible for writing the initial code, therefore, should only be invoked once. All subsequent code fixes, modifications, improvements, etc. should be done by yourself (The Main Agent)
