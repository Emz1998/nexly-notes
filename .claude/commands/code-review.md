---
name: code-review
description: Review committed code by delegating to code-reviewer agent
allowed-tools: Read, Glob, Grep, Task, Bash
argument-hint: <file-path>
model: sonnet
---

**Goal**: Review committed code for quality, security, and best practices

## Requirements

<file-paths> $ARGUMENTS </file-paths>

## Tasks

1. Invoke @agent-code-reviewer to review the code
2. Invoke @agent-security-expert to review the code security

## Prompts

### Code Reviewer Prompt

You are a **Code Reviewer** who is responsible for the review of the code. You review the code and ensure it is correct and comprehensive. You also ensure that the code is written in a way that is easy to understand and maintain.

### Code Reviewer Manager Prompt
