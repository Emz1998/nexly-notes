---
name: hooks-management
description: Use PROACTIVELY when you need to create, update, configure, or validate Claude hooks for various events and integrations
---

**Goal**: Create, update or troubleshoot Claude Code hook scripts

## Workflow

### Phase 1: Pre-flight Check

- T000: **Run tests FIRST** to verify baseline:
  ```bash
  # Unit tests (fast, isolated)
  .claude/hooks/.venv/bin/pytest .claude/hooks/tests/ -v

  # Integration tests (full hook execution)
  python3 .claude/skills/hooks-management/scripts/test-hooks-regression.py
  ```
  - If tests fail, investigate and fix before proceeding
  - Document any pre-existing failures

### Phase 2: Exploration & Analysis

- T001: Read hook docs from `.claude/skills/hooks-management/references/hooks.md`
- T001b: Read input patterns from `.claude/skills/hooks-management/references/input-patterns.md` (JSON structures for all hook events)
- T002: Analyze the request and identify if the task is to create, update or troubleshoot a hook.
- T003: Choose the appropriate task to perform based on the request in `.claude/skills/hooks-management/tasks/`
- T004: Check existing hooks in `.claude/hooks/` and settings configuration in `.claude/settings.local.json`

### Phase 3: Implementation

- T005: Perform the task
- T006: Test the hook execution and edge cases using `echo` (see Testing Strategy)
- T007: Review security and performance

### Phase 4: Documentation & Validation

- T008: Update `.claude/skills/hooks-management/references/hooks-status.md` to reflect changes
- T009: Update `.claude/skills/hooks-management/references/architecture-pattern.md` if architectural changes were made (new modules, utils, patterns)
- T010: **Update regression test script** if hooks were added/modified/deleted:
  - Add new test cases for new hooks
  - Modify test cases for updated hooks
  - Remove test cases for deleted hooks
  - Location: `.claude/skills/hooks-management/scripts/test-hooks-regression.py`
- T011: **Run tests AGAIN** to verify all hooks work:
  ```bash
  # Unit tests (fast, isolated)
  .claude/hooks/.venv/bin/pytest .claude/hooks/tests/ -v

  # Integration tests (full hook execution)
  python3 .claude/skills/hooks-management/scripts/test-hooks-regression.py
  ```
  - All tests must pass before completing the task
  - If tests fail, fix issues and re-run
- T012: Provide comprehensive report to main agent

## Implementation Strategy

- For new hooks: Create script file in `.claude/hooks/` following naming convention
- If the task is to troubleshoot, follow the troubleshooting task in `.claude/skills/hooks-management/tasks/troubleshooting.md`
- If the task is to update, follow the update task in `.claude/skills/hooks-management/tasks/update-hook.md`
- If the task is to create, follow the create task in `.claude/skills/hooks-management/tasks/create-new-hook.md`
- Prefer Python over shell scripts if possible.
- Implement idempotent operations where possible

**IMPORTANT - Dispatcher Pattern:**
- Use root entry point handlers (e.g., `pre_tool_use.py`, `subagent_stop.py`) as dispatchers
- Add new functionality by creating modules in subdirectories (e.g., `plan_mode/`) and importing them in root handlers
- **DO NOT** add new entries to `settings.local.json` for new hook logic - modify existing root handlers instead
- If unsure about the architecture, consult `.claude/skills/hooks-management/references/architecture-pattern.md`

## Testing Strategy

Use `echo` to pipe test input directly to hook scripts without creating test files:

```bash
# Test with sample JSON input
echo '{"session_id": "test-123", "tool": "Read", "result": "sample output"}' | python .claude/hooks/your-hook.py

# Test with minimal input
echo '{}' | python .claude/hooks/your-hook.py

# Test error handling with malformed input
echo 'invalid json' | python .claude/hooks/your-hook.py

# Test with specific event data
echo '{"event": "stop", "reason": "user_request"}' | python .claude/hooks/your-hook.py
```

**Testing Checklist:**

- [ ] Hook accepts valid JSON input via stdin
- [ ] Hook handles empty input gracefully
- [ ] Hook handles malformed input without crashing
- [ ] Hook returns appropriate exit codes (0 for success, non-zero for errors)
- [ ] Hook output is valid JSON when required by the event type

## Constraints

- **Must** use root entry point handlers as dispatchers - do NOT add new entries to `settings.local.json`
- **Must** test hooks after generation without creating test files
- **Never** create hooks that modify critical system files
- **Never** implement hooks with hardcoded credentials
- **Never** write hooks that can cause infinite loops
- **Never** bypass security validations or access controls
- **Never** create hooks without proper error handling
- **Never** create test files when testing hooks
- **Never** write complicated hooks with complex logic. Keep it simple and straightforward.

## Regression Testing

Two test suites validate hooks are working correctly:

```bash
# Unit tests (pytest) - fast, isolated, mock cache
.claude/hooks/.venv/bin/pytest .claude/hooks/tests/ -v

# Integration tests - full hook execution as subprocess
python3 .claude/skills/hooks-management/scripts/test-hooks-regression.py
```

**Pytest Unit Tests** (`tests/`):
- `test_utils.py` - Cache, base_mode, agent_validation, frontmatter
- `test_security.py` - Security validation functions
- `test_modes.py` - Mode activation/deactivation

**Integration Tests** (`scripts/test-hooks-regression.py`):
- Utility functions (cache, frontmatter, milestone, git)
- Security validation (dangerous commands/paths blocking)
- Plan/Research/Explore/Code/Code-Review mode workflows
- Root dispatchers (pre_tool_use, subagent_stop, user_prompt_submit)
- Session hooks (session_start)

**When to Update Tests:**
- **New hook**: Add pytest unit tests + integration test cases
- **Modified hook**: Update existing test cases to match new behavior
- **Deleted hook**: Remove test cases for the deleted hook
- **New utility function**: Add pytest unit tests

## Success Criteria

- Hook script exists and is syntactically valid
- Hook is properly linked in `settings.local.json`
- Hook executes successfully on target event
- Error handling covers common failure scenarios
- No security vulnerabilities detected
- `hooks-status.md` reference updated to reflect current hook state
- `architecture-pattern.md` updated if architectural changes were made
- **All tests pass (37 pytest unit tests + 65 integration tests)**
- **Regression test script updated if hooks changed**
- Comprehensive report provided to main agent upon completion
- Code is readable and concise.
