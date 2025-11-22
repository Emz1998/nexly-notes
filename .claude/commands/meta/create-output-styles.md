---
name: create-output-styles
description: Generate new output styles using the meta-output-styles agent
argument-hint: <output-style-name> <instructions>
---

## 1. Context

You are creating a new output style configuration for the Claude AI system.

- Needs: An output style that will solve the following needs: $2
- Purpose: Generate structured output style configurations that define how agents format their responses
- Use case: When a specific formatting pattern is needed for agent outputs
- Dependencies: Delegates to @agent-meta-output-styles for generation logic

## 2. Goal / Intent

Create a properly formatted output style configuration file.

- Primary objective: Generate an output style that defines formatting patterns
- Expected outcome: A complete output style saved to .claude/output-styles/
- Deliverables: Generated output style file following project standards

## 3. Constraints / Rules

Technical and operational boundaries for output style creation.

- Technical constraints: Must follow existing output style format in project
- Scope boundaries: Only create output style configuration, not implementation
- Quality standards: Output must be concise and follow project patterns
- Always provide comprehensive reports back to main agent
- **DO NOT IMPLEMENT THE TASK YOURSELF**. You have to delegate the task to the @agent-meta-output-styles.

## 4. Output Format

How to structure and present the output style creation results.

- Report structure: Summary of created output style with key formatting rules
- File locations: Save to /workspace/.claude/output-styles/[$1].md
- Response style: Brief confirmation with output style highlights

## 5. Examples

Examples of proper command usage and execution.

- Good approach: Analyze requirements, delegate to meta-output-styles, save result
- Bad approach: Creating verbose or overly complex output styles
- Sample usage: /create-output-styles orchestrate-build "Define formatting for build orchestration tasks"