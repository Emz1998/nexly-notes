---
name: create-agent
description: Generates agent configurations using the meta-agent specialist
allowed-tools: all
argument-hint: <agent-name> <expertise>
model: claude-3-5-haiku-latest
---

## 1. Context

This command streamlines the creation of new agents by delegating to the meta-agent specialist.

- Purpose: Automate agent generation with consistent configuration
- Use case: When needing new specialized agents for specific tasks
- Dependencies: @agent-meta-agent, agent configuration rules, subagent structure
- Main Instruction: "Create an agent that is expert in @2"

## 2. Goal / Intent

Generate properly configured agents that follow established patterns and rules.

- Primary objective: Create valid agent configuration files
- Expected outcome: New agent saved to appropriate subfolder
- Deliverables: Agent file with correct frontmatter and specialized sections

## 3. Constraints / Rules

- Technical constraints: Must follow subagent configuration rules
- Scope boundaries: Only creates agents, doesn't modify existing ones
- Quality standards: Agents must be focused, include context-memory management
- Always provide comprehensive reports back to main agent
- **DO NOT IMPLEMENT THE TASK YOURSELF**. You have to delegate the task to the @agent-meta-agent.

## 4. Output Format

- Report structure: Summary of created agent with location and capabilities
- File locations: Save to .claude/agents/ appropriate subdirectory
- Response style: Concise confirmation with agent details and usage
- Name of the agent file: $1.md

## 5. Examples

- Good approach: Single-purpose agent with clear expertise domain
- Bad approach: Generic agent trying to handle multiple unrelated domains
- Sample usage: /create-agent test-engineer "specialized in TDD and test automation"