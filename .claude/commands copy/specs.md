---
name: specs
description: Generate specification documents (prd, tech-specs, or ux-specs)
allowed-tools: Read, Write, Glob, Grep
argument-hint: <specs-type>
model: sonnet
---

<specs-type> $ARGUMENTS </specs-type>

<instruction>

- Use `specs-creator` skill to generate <specs-type> specification document
- If <specs-type> is not specified, generate all specification documents (prd, tech-specs, and ux-specs)

</instruction>

<rules> Must use `specs-creator` skill to generate <specs-type> specification document </rules>
