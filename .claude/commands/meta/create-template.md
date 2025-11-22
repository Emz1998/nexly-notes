---
name: create-template
description: Generates comprehensive, flexible templates by delegating to the template-writer agent
argument-hint: <template-type> <special-instructions>
allowed-tools: Task
model: sonnet
---

Deploy @agent-template-writer to create a $1 template with the following requirements: $2

## 1. Context

This command streamlines template creation by delegating to the specialized template-writer agent.

- Purpose: Automate template generation with industry-standard patterns and best practices
- Use case: When needing document templates, code scaffolding, configuration files, project structures, or procedural workflows
- Dependencies: @agent-template-writer located at .claude/agents/planning/template-writer.md
- Requirements: Must launch the template-writer agent to handle all template design and implementation

## 2. Goal / Intent

Generate well-structured, documented templates that follow industry conventions and are ready for immediate use.

- Primary objective: Deploy template-writer agent to create $1 template following $2 specifications
- Expected outcome: Complete template with clear placeholders, inline documentation, and usage examples
- Deliverables: Template file with comprehensive comments, customization instructions, and validation guidance

## 3. Constraints / Rules

Technical and quality requirements for template generation.

- Technical constraints: Must use Task tool to invoke template-writer agent
- Scope boundaries: No direct implementation, always delegate to template-writer agent
- Quality standards: Templates must follow industry standards, use consistent placeholder syntax, include inline documentation
- Always provide comprehensive reports back to main agent
- **DO NOT IMPLEMENT THE TASK YOURSELF**. You have to delegate the task to the @agent-template-writer.

## 4. Output Format

How to present results after template generation.

- Report structure: Confirm template created with file path, template type, and key features
- File locations: Templates saved to appropriate project directory based on type
- Response style: Concise confirmation with usage instructions and customization guidance
- Save to `.claude/templates/` folder
- File name: $1-template.md

## 5. Examples

Sample usage and delegation patterns.

- Good approach: Deploy template-writer agent with clear template type and requirements, let agent research standards and create comprehensive template
- Bad approach: Manually writing template without researching conventions or delegating to specialized agent
- Sample usage: /create-template "API endpoint" "RESTful service with error handling and validation"
- Sample usage: /create-template "React component" "TypeScript functional component with props interface and documentation"
- Sample usage: /create-template "GitHub workflow" "CI/CD pipeline for Node.js with testing and deployment stages"
