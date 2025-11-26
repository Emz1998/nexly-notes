---
name: command
description: Creates new commands or updates existing command configurations using the command-management skill
argument-hint: <command-name> <requirements>
model: claude-opus-4-5-20251101
---

<instruction> Use `command-management` skill to create or update command $1 with requirements $2 </instruction>

<rule>`command-management` skill MUST be used for this task.</rule>
