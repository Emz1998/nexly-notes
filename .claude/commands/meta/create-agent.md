---
name: create-agent
description: Creates new agents or updates existing agent configurations using the meta-agent specialist
argument-hint: <agent-name> <expertise>
---

## 1. Context

This command streamlines the creation of new agents or updates to existing agents by delegating to the meta-agent specialist.

- Purpose: Automate agent creation and updates with consistent configuration
- Use case: When needing new specialized agents for specific tasks or updating existing agents with new capabilities
- Dependencies: @agent-meta-agent, agent configuration rules, subagent structure
- User Instruction: "$2"

## 2. Goal / Intent

Generate or update properly configured agents that follow established patterns and rules.

- Primary objective: Create new or update existing valid agent configuration files
- Expected outcome: New or updated agent saved to appropriate subfolder with backup created if updating
- Deliverables: Agent file with correct frontmatter and specialized sections, backup file if updating existing agent

## 3. Constraints / Rules

- Technical constraints: Must follow subagent configuration rules
- Scope boundaries: Creates new agents or updates existing ones while preserving functionality
- Quality standards: Agents must be focused, include context-memory management
- When updating: meta-agent must create backup before modifying existing agent
- When updating: meta-agent must preserve existing functionality unless explicitly requested to change
- Always provide comprehensive reports back to main agent
- **DO NOT IMPLEMENT THE TASK YOURSELF**. You have to delegate the task to the @agent-meta-agent.

## 4. Output Format

- Report structure: Summary of created or updated agent with location, capabilities, and changes made (if updating)
- File locations: Save to .claude/agents/ appropriate subdirectory
- Backup file location: Same directory as agent with .backup.md extension (if updating)
- Response style: Concise confirmation with agent details, changes (if updating), and usage
- Name of the agent file: $1.md
- Name of the backup file (if updating): $1.backup.md

## 5. Examples

- Good approach: Single-purpose agent with clear expertise domain
- Bad approach: Generic agent trying to handle multiple unrelated domains
- Sample usage (create new): /create-agent test-engineer "specialized in TDD and test automation"
- Sample usage (update existing): /create-agent test-engineer "specialized in TDD, test automation, and performance testing"
