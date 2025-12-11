---
paths: .claude/agents/**/*.md
---

# Subagents Configuration Rules

## Directory Structure

```
project-root/
├── /.claude               # Claude Code configuration
│   ├── /agents           # Agents
│   │  ├── /engineering         # Engineering Team
│   │  ├── /quality-assurance         # Quality Assurance Team
│   │  ├── /devops         # DevOps Team
│   │  ├── /architect         # Architect Team
│   │  ├── /research         # Research Team
│   │  ├── /meta         # Meta Agents
│   │  ├── /project-management         # Project Management Team
│   │  ├── /design         # Design Team
│   │  └── /core         # Core Team
```

## Instructions for Writing Configuration

- Analyze patterns of the existing agents in the directory and follow the same structure and approach
- Must be composed of 4 sections: YAML Frontmatter Details, Responsibilities, Workflow and Rules
- Maximum of 3 responsibilities per agent with 5 bullet points explaining the scope of this responsibility
- Maximum of 3 phases workflow with 5 tasks per phase in bullet points
- Rules section should have "Core Principles" and "Prohibited Tasks/Approches" sub-sections with 5 tasks for each in bullet points
- Model options: opus, sonnet, haiku

## Rules by Department

- ONLY the **Engineering Team** is allowed to do any coding tasks
- All other teams should only be used for research tasks, documentation tasks and context gathering tasks
- Each agents should only have one deliverable per task. If the task requires multiple deliverables, then you have to deploy multiple appropriate agents to complete the task
- Always instruct the agents to focus on lean approach. Ensure that they don't overcomplicate the task and always keep it simple and efficient
- When configuring the agents, ensure that you don't overbloat the file with too much information. Keep it concise and to the point. Follow the structure and approach of the existing agents.
