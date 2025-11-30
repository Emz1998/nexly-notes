# Task: Create a Claude Custom Hook for Phase Validation

## Objective

Build a custom hook that prevents workflow phases from proceeding until their required tasks are completed. The hook validates phase completion by checking for the existence of specific deliverables.

## Context

- Phase state is stored in `.claude/hooks/implement/state.json`
- The hook should use the `PostToolUse` event to perform validation
- Different phases have different completion requirements

---

## Phase Completion Requirements

### Documentation Phases

Each documentation phase requires a specific markdown file to exist:

| Phase | Required File |
|-------|---------------|
| Explore | `codebase-status.md` |
| Research | `research-report.md` |
| Research Consult | `research-report-feedback.md` |
| Plan | `implementation-plan.md` |
| Plan Consult | `implementation-plan-feedback.md` |

**Validation Method:** Use `PostToolUse` to check if the required markdown file exists in the expected location.

### Coding Phase

Applies to code files (`.py`, `.js`, `.ts`, `.test.*`, and similar extensions).

**Validation Methods (choose one or combine):**

1. **Timestamp Check:** Compare file modification timestamps against phase start time
2. **Git Status Check:** Use subprocess to run `git status` and verify new/modified code files

### Code Review & Refactoring Phases

These phases require detecting changes to existing files.

**Validation Methods (choose one or combine):**

1. **File Open Flag:** Track whether relevant files were opened during the phase
2. **Timestamp + Git Comparison:**
   - Record the timestamp when the phase state changes
   - Use `git status` (via subprocess) to detect modifications after this timestamp

### Commit Phase

**Validation Method:** Use subprocess to check `git status` for uncommitted changes, or verify that a new commit was created.

---

## Implementation Guidelines

<guidelines>

1. **Hook Event:** Use `PostToolUse` as the primary trigger for validation checks

2. **State Reference:** Read current phase from `.claude/hooks/implement/state.json`

3. **Subprocess Usage:** For git operations, use subprocess to execute:
   - `git status` for detecting changes
   - `git log` for verifying commits

4. **Blocking Behavior:** When validation fails, the hook should prevent phase transition and provide a clear message indicating what task remains incomplete

5. **File Existence Checks:** For documentation phases, verify the required markdown file exists before allowing progression

</guidelines>

---

## Decision Points for Implementation

Please determine the optimal approach for each phase type:

1. **Coding Phase:** Should we use timestamp checks, git status, or both?
2. **Code Review/Refactoring:** Which combination of flag tracking and timestamp/git comparison works best?
3. **Error Handling:** How should the hook respond when validation fails?

## Expected Deliverable

A functional Claude custom hook that:
- Monitors phase state from `.claude/hooks/implement/state.json`
- Validates completion requirements for each phase type
- Blocks phase transitions when requirements are not met
- Provides informative feedback about incomplete tasks
- Save this new hook in .claude/hooks/implement/phase-completion-check.py