---
name: plan
description: Create a plan based on user's instructions
allowed-tools: Read, Write, Glob
argument-hint: <plan-type> <plan-name> <plan-description>
model: sonnet
---

Create a plan based on user's instructions

## Tasks

- T001: Read the user's instructions
- T002: Create a plan based on user's instructions

## Instructions

- Write the plan in the `.claude/plans/[plan-name].md` file first using the `Write` tool
- Save the plan to `.claude/plans/[plan-name].md`
