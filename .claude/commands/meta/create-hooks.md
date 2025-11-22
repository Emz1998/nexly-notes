---
name: create-hooks
description: Deploy hook-generator agent to create Claude hooks for various editor events
allowed-tools: task, write
argument-hint: <hook-name> <instructions>
model: claude-opus-4-1-20250805
---

## 1. Context

This command deploys the hook-generator agent to create Claude hooks that respond to specific editor events and automate workflows.

- Purpose: Streamline hook creation through specialized agent delegation
- Use case: When needing to create hooks for file changes, save events, or custom triggers
- Dependencies: hook-generator agent configuration
- Requirements: $2 contains detailed instructions for the hook's behavior

## 2. Goal / Intent

Create a properly formatted Claude hook that integrates with the editor's event system.

- Primary objective: Generate a functional hook based on $1 name and $2 instructions
- Expected outcome: A valid hook file in python saved to .claude/hooks/[$1].py
- Deliverables: Single hook configuration file with proper event triggers and actions

## 3. Constraints / Rules

Define boundaries and standards for hook creation.

- Technical constraints: Must follow Claude hook syntax and event system
- Scope boundaries: Only create one hook per invocation
- Quality standards: Hook must be valid YAML frontmatter with clear instructions
- Always provide comprehensive reports back to main agent

## 4. Output Format

Structure for presenting the generated hook.

- Report structure: Summary of created hook with event triggers and actions
- File locations: Save to /workspace/.claude/hooks/[$1].py
- Response style: Concise confirmation with hook details

## 5. Examples

Proper execution patterns for hook creation.

- Good approach: /create-hooks "on-save-format" "Format code when files are saved in src/ directory"
- Bad approach: Creating multiple hooks in one command or modifying existing hooks
- Sample usage: /create-hooks test-runner "Run tests when test files change"