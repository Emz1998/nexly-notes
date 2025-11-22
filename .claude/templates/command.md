<!--

Important Instructions:

- This is a template for creating a new command.

- See @.claude/docs/claude-tools.md for the list of tools available to use.

- Add Examples/ Patterns here to help Claude understand the tasks

- Model should be either haiku or sonnet. Sonnet is more intelligent than haiku so decide accordingly which one fit the task best.
-->

---

name: <command-name>
description: <brief description of what the command does>
allowed-tools: <comma-separated list of tools>
argument-hint: <arg1-name> <arg2-name> <arg3-name>
model: <haiku|sonnet>

---

## 1. Context

- Main Objective: [Main objective] [Example: Create a new Agent Skill named $1 with requirements: $2]
- Secondary Objective: [Secondary objective]
- User Input: [$1, $2, $3,etc.] (Positional parameters depending on the arguments hint)

<!-- Add more instructions as needed -->

## 2. Tasks

<!-- Add Code `[P]` to signify that can be run in parallel -->

### Phase 1: [Phase 1 Name]

- T001: [Task 1] [P]
- T002: [Task 2] [P]
- T003: [Task 3]
- T004: [Task 4]
- T005: [Task 5]

### Phase 2: [Phase 2 Name]

- T006: [Task 1]
- T007: [Task 2]
- T008: [Task 3]
- T009: [Task 4]
- T010: [Task 5]

### Phase 3: [Phase 3 Name]

- T013: [Task 1]
- T014: [Task 2]
- T015: [Task 3]
- T016: [Task 4]
- T017: [Task 5]

...

<!-- Add more phases and tasks as needed -->

## 3. Implementation Strategy

- [Implementation Strategy 1]
- [Implementation Strategy 2]
- [Implementation Strategy 3]
- [Implementation Strategy 4]
- [Implementation Strategy 5]
- ...

<!-- Add more implementation strategies as needed -->

## 4. Constraints

- [Constraint 1]
- [Constraint 2]
- [Constraint 3]
- [Constraint 4]
- [Constraint 5]
- ...

<!-- Add more constraints as needed -->

## 5. Success Criteria

- [Success Criteria 1]
- [Success Criteria 2]
- [Success Criteria 3]
- [Success Criteria 4]
- [Success Criteria 5]
- ...

<!-- Add more success criteria as needed -->

## 6. Patterns

<!-- Add common patterns here to help Claude understand the tasks -->

## 7. References

<!-- Add references to give more context. Use `@` if the file must be read AT ALl TIMES. Use double ticks `` if the path should only be read PROACTIVELY -->

- [Path to reference 1]
- [Path to reference 2]
- [Path to reference 3]
- [Path to reference 4]
- [Path to reference 5]

<!-- Add more references as needed -->
