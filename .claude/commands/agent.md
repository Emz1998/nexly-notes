---
name: agent
description: Creates new agents or updates existing agent configurations using the meta-agent specialist
argument-hint: <agent-name> <requirements>
---

<instruction> Use create-agent skills to create or update subagent $1 with requirements $2 </instruction>

<rule>`agent-management` skill MUST be used for this task.</rule>
