---
name: implement
description: Build a production-ready feature with thorough planning and structured context gathering
argument-hint: Build a <feature> that will <functionality>
---

Build a $1 that will $2

## 1. Context

This command orchestrates feature development for the NEXLY RN nursing education platform, transforming user requirements into production-ready implementations through systematic planning, development, and validation.

- Purpose: Coordinate end-to-end feature implementation with proper planning and testing
- Use case: When adding new functionality to the NEXLY RN platform
- Dependencies: Relies on engineering agents, Firebase services, and React/TypeScript stack
- Requirements: Clear feature description, acceptance criteria, and technical specifications

## 2. Goal / Intent

Transform feature requirements into deployed, tested code that meets NEXLY RN's quality standards and user needs.

- Primary objective: Deliver a fully functional feature based on $1 specifications
- Expected outcome: Working code with tests, proper error handling, and documentation
- Deliverables: Implementation files, test suites, updated components, and completion report

## 3. Constraints / Rules

Maintain high code quality while building for MVP with lean, efficient approaches.

- Technical constraints: React/TypeScript, Firebase backend, Tauri desktop, TDD methodology
- Scope boundaries: Focus only on requested feature, avoid scope creep or premature optimization
- Quality standards: 80% test coverage, proper error handling, accessibility compliance
- Always provide comprehensive reports back to main agent

## 4. Output Format

Provide structured progress updates and final implementation summary.

- Report structure: Phase completion status, files created/modified, test results, next steps
- File locations: Save implementations to /home/emhar/nexly/src, tests to /home/emhar/nexly/tests
- Response style: Clear phase announcements, concise technical updates, actionable next steps

## 5. Examples

Effective patterns for building different feature types.

- Good approach: Plan → Write tests → Implement → Refactor → Document → Report completion
- Bad approach: Jump to coding without planning, skip tests, overcomplicate for MVP
- Sample usage: /build "note editor with auto-save and markdown support"
