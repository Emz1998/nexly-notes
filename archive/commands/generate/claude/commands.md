---
name: create-command
description: Factory to create custom commands following best practices
argument-hint: <command-name> <instruction> 
model: claude-opus-4-1-20250805
---

<main-instruction>Deploy @agent-meta-command to create a new command that will be named $1 and save it to this folder `.claude/commands/meta/`. The purpose of this new command is to $2 <main-instruction>

## 1. Context

This command serves as a factory for generating new custom commands by delegating to the meta-command agent.

- Purpose: Automate command creation following best practices
- Use case: When users need new workflow automation commands
- Dependencies: @agent-meta-command, @.claude/docs/claude-tools.md
- Requirements: Must launch the @agent-meta-command to generate new commands.

## 2. Goal / Intent

Create a new custom command file using the meta-command agent that follows the 5-section template structure.

- Primary objective: Deploy meta-command agent to generate a new command
- Expected outcome: New command file saved to .claude/commands/meta with proper structure
- Deliverables: Fully functional command configuration following template standards

## 3. Constraints / Rules

Technical and quality requirements for command generation.

- Technical constraints: Must use Task tool to invoke meta-command agent
- Scope boundaries: No direct implementation, always delegate to meta-command agent
- Quality standards: Follow 5-section structure, minimal tool permissions, positional parameters only
- Always provide comprehensive reports back to main agent
- **DO NOT IMPLEMENT THE TASK YOURSELF**. You have to delegate the task to the @agent-meta-command.

## 4. Output Format

How to present results after command generation.

- Report structure: Confirm command created with file path and brief description
- File locations: .claude/commands/$1.md or appropriate subfolder
- Response style: Concise confirmation with command usage example

## 5. Examples

Sample usage and delegation patterns.

- Good approach: Deploy meta-command agent with clear requirements, let agent handle template compliance
- Bad approach: Manually writing command file without using meta-command agent
- Sample usage: /create-command analyze-performance "Create command to analyze app performance metrics"

---