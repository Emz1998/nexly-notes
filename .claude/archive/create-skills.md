---
name: create-skills
description: Generates Agent Skills for Claude Code using the skills-generator specialist
allowed-tools: Task
argument-hint: <skill-name> <purpose>
model: sonnet
---

Deploy @agent-skills-generator to create a new Agent Skill named "$1" that will $2

## 1. Context

This command streamlines the creation of Agent Skills by delegating to the skills-generator specialist.

- Purpose: Automate Skills generation following Anthropic's standards
- Use case: When needing new Skills to extend Claude's capabilities
- Dependencies: @agent-skills-generator, custom-skills context documentation
- Requirements: Must launch the skills-generator agent to create Skills

## 2. Goal / Intent

Generate properly configured Agent Skills that follow Anthropic's documented best practices.

- Primary objective: Deploy skills-generator agent to create Skill with name "$1"
- Expected outcome: New Skill saved to .claude/skills/$1/ with SKILL.md
- Deliverables: Valid Skill with YAML frontmatter, progressive disclosure structure

## 3. Constraints / Rules

Technical and quality requirements for Skill generation.

- Technical constraints: Must use Task tool to invoke skills-generator agent
- Scope boundaries: Only creates Skills, doesn't modify existing ones
- Quality standards: Follow progressive disclosure, keep SKILL.md under 500 lines
- Always provide comprehensive reports back to main agent
- **DO NOT IMPLEMENT THE TASK YOURSELF**. You have to delegate the task to @agent-skills-generator

## 4. Output Format

How to present results after Skill generation.

- Report structure: Confirm Skill created with file path and description
- File locations: .claude/skills/$1/SKILL.md and any additional resources
- Response style: Concise confirmation with Skill usage instructions

## 5. Examples

Sample usage and delegation patterns.

- Good approach: Deploy skills-generator with clear Skill name and purpose
- Bad approach: Manually creating Skill files without using skills-generator agent
- Sample usage: /create-skills pdf-processing "extract text and tables from PDF files"