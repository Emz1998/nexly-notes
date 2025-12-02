# Hooks Status Reference

## Overview

Current status of all Claude Code hooks in `.claude/hooks/`.

---

## Root-Level Event Handlers

| File | Event | Status | Description |
|------|-------|--------|-------------|
| `session_start.py` | SessionStart | Implemented | Initializes session ID, loads milestone from `project/status.json` |
| `session_end.py` | SessionEnd | Empty | Not implemented |
| `pre_tool_use.py` | PreToolUse | Implemented | Dispatches to `security/`, `plan_mode/`, `research_mode/`, `explore_mode/`, `code_mode/`, `code_review_mode/` for validation |
| `post_tool_use.py` | PostToolUse | Empty | Not implemented |
| `user_prompt_submit.py` | UserPromptSubmit | Implemented | Activates plan/research/explore/code/code-review mode on `/plan`, `/research`, `/implement`, `/code`, `/code-review` commands |
| `stop.py` | Stop | Implemented | Validates plan completion before stopping |
| `subagent_stop.py` | SubagentStop | Implemented | Dispatches to `plan_mode/`, `research_mode/`, `explore_mode/`, `code_mode/`, `code_review_mode/` for subagent stop validation |
| `permission_request.py` | PermissionRequest | Implemented | Switches to plan mode on permission requests |
| `pre_compact.py` | PreCompact | Empty | Not implemented |
| `notification.py` | Various | Empty | Not implemented |

---

## Module Status

### plan_mode/ - Plan Mode State Management

| File | Status | Purpose |
|------|--------|---------|
| `__init__.py` | Implemented | Exports module functions |
| `activate.py` | Implemented | Activates plan mode on `/plan` command (uses `utils/`) |
| `deactivate.py` | Implemented | Deactivates plan mode (uses `utils/`) |
| `block_premature_agents.py` | Implemented | Blocks agents without required dependencies (strategic-planner needs research, consulting-expert needs plan) |
| `validate_subagent_stop.py` | Implemented | Validates strategic-planner/consulting-expert completed required work |

**Validation Sequence:**
1. Research report must exist before strategic-planner can be called (PreToolUse)
2. Plan file must exist before strategic-planner can stop (SubagentStop)
3. Plan file must exist before consulting-expert can be called (PreToolUse)
4. Plan must have `consulted_by: consulting-expert` frontmatter before consulting-expert can stop (SubagentStop)

**Note:** Cache management moved to shared `utils/cache.py` with namespaced keys (`plan_mode.*`).

### research_mode/ - Research Mode State Management

| File | Status | Purpose |
|------|--------|---------|
| `__init__.py` | Implemented | Exports module functions |
| `activate.py` | Implemented | Activates research mode on `/research` command (uses `utils/`) |
| `deactivate.py` | Implemented | Deactivates research mode (uses `utils/`) |
| `block_premature_agents.py` | Implemented | Blocks agents without required dependencies (research-specialist needs explore status, research-consultant needs research report) |
| `validate_subagent_stop.py` | Implemented | Validates research-specialist/research-consultant completed required work |

**Validation Sequence:**
1. `codebase-status_[session-id]_[MMDDYY].md` must exist in `exploration/` before research-specialist can be called (PreToolUse)
2. Research report must exist before research-specialist can stop (SubagentStop)
3. Research report must exist before research-consultant can be called (PreToolUse)
4. Research must have `validated_by: research-consultant` frontmatter before research-consultant can stop (SubagentStop)
5. Research file must be committed before research-consultant can stop (SubagentStop)

**Note:** Cache management uses shared `utils/cache.py` with namespaced keys (`research_mode.*`).

### explore_mode/ - Explore Mode State Management

| File | Status | Purpose |
|------|--------|---------|
| `__init__.py` | Implemented | Exports module functions |
| `activate.py` | Implemented | Activates explore mode on `/implement` command (uses `utils/`) |
| `deactivate.py` | Implemented | Deactivates explore mode (uses `utils/`) |
| `block_premature_agents.py` | Implemented | Blocks codebase-explorer if `specs/tasks.md` is missing |
| `validate_subagent_stop.py` | Implemented | Validates codebase-explorer created the codebase-status file |

**Validation Sequence:**
1. `specs/tasks.md` must exist before codebase-explorer can be called (PreToolUse)
2. `codebase-status_[session-id]_[MMDDYY].md` must exist in `exploration/` before codebase-explorer can stop (SubagentStop)

**Note:** Cache management uses shared `utils/cache.py` with namespaced keys (`explore_mode.*`).

### security/ - Security Validation

| File | Status | Purpose |
|------|--------|---------|
| `security.py` | Implemented | Blocks critical system-damaging operations (refactored) |

**Features:**
- Uses `sys.exit(2)` to block dangerous operations (Claude sees stderr message)
- Uses shared `utils/` module (read_stdin_json, log)
- Blocks: `rm -rf /`, `rm -rf /*`, `rm -rf /etc`, `dd`, `mkfs`, fork bombs
- Protects: `/etc/passwd`, `/etc/shadow`, `/boot/`, `/sys/`, SSH keys
- Safe directories: `/.claude/`, `/src/`, `/tests/` (operations allowed)
- Fail-safe: allows operations on error to avoid blocking legitimate work

### notification/ - Push Notifications

| File | Status | Purpose |
|------|--------|---------|
| `notify-ntfy.py` | Implemented | ntfy.sh push notifications |

**Features:**
- Sends notifications on Stop/SubagentStop events
- Tracks: files edited, files created, commands run, agents launched
- Stores activity in `session_activity.json`
- Tracks UserPromptSubmit for context

### code_mode/ - TDD Workflow Enforcement (NEW)

| File | Status | Purpose |
|------|--------|---------|
| `__init__.py` | Implemented | Exports module functions |
| `activate.py` | Implemented | Activates code mode on `/code` command (requires plan file) |
| `deactivate.py` | Implemented | Deactivates code mode (uses `utils/`) |
| `block_premature_agents.py` | Implemented | Enforces TDD phase sequence (blocks wrong agents per phase) |
| `validate_subagent_stop.py` | Implemented | Validates subagent completed work, advances to next phase |

**TDD Workflow Phases:**
1. failing_test - Requires `test-engineer` subagent (Red phase)
2. passing_test - Main agent implements code (Green phase)
3. refactor - Main agent refactors code
4. troubleshoot - Requires `troubleshooter` subagent
5. commit - Direct commit (no agent required)

**Validation Sequence:**
1. Plan file must exist before code mode can be activated (UserPromptSubmit)
2. test-engineer must create tests in `src/tests` that fail (SubagentStop)
3. Main agent implements code to pass tests (no Task tool allowed)
4. Main agent refactors code (no Task tool allowed)
5. troubleshooter addresses issues (SubagentStop)
6. Commit phase - direct commit

**Prerequisites:**
- Plan file must exist at: `project/[MS-NN]:[MS-Description]/plans/plan_[session-id]_[MMDDYY].md`

**Note:** Cache management uses shared `utils/cache.py` with namespaced keys (`code_mode.*`).

### code_review_mode/ - Code Review Workflow Enforcement (NEW)

| File | Status | Purpose |
|------|--------|---------|
| `__init__.py` | Implemented | Exports module functions |
| `activate.py` | Implemented | Activates code review mode on `/code-review` command |
| `deactivate.py` | Implemented | Deactivates code review mode (uses `utils/`) |
| `block_premature_agents.py` | Implemented | Blocks code-reviewer if code is not committed |
| `validate_subagent_stop.py` | Implemented | Validates code-reviewer produced a review report |

**Workflow:**
1. Triggered by `/code-review` command
2. Prerequisites check (git-based first, TDD fallback):
   - No uncommitted changes in `src/` directory, OR
   - `code_mode.current_phase == "commit"` (TDD complete)
3. Deploys `code-reviewer` subagent
4. Validates review report before allowing agent to stop

**Validation Sequence:**
1. Git-based check: No uncommitted changes in `src/` directory (PreToolUse, UserPromptSubmit)
2. Fallback: TDD commit phase must be complete (PreToolUse, UserPromptSubmit)
3. Review file must exist at: `project/[MS-NN]:[Description]/reviews/review_[session-id]_[MMDDYY].md` (SubagentStop)
4. Review must contain required sections: `summary`, `findings` (SubagentStop)
5. Review must have minimum content length (200 chars) (SubagentStop)

**Review File Requirements:**
- Location: `project/[MS-NN]:[Description]/reviews/review_[session-id]_[MMDDYY].md`
- Required sections: `summary`, `findings`
- Minimum length: 200 characters

**Note:** Cache management uses shared `utils/cache.py` with namespaced keys (`code_review_mode.*`).

### implement/ & code/ - Legacy TDD Workflow (DELETED)

**Status:** DELETED - These directories have been removed from the codebase.

The legacy `implement/` and `code/` directories have been replaced by the `code_mode/` module following the dispatcher pattern. All TDD workflow logic is now in `code_mode/` using the shared `utils/` infrastructure.

### change_log/ - Change Tracking

| File | Status | Purpose |
|------|--------|---------|
| `change-log.py` | Implemented | Tracks file changes (12KB) |

### compact/ - Compaction

| File | Status | Purpose |
|------|--------|---------|
| `compact-instructions.py` | Implemented | Pre-compact instructions |

### hooks_test/ - Testing

| File | Status | Purpose |
|------|--------|---------|
| `test-hooks.py` | Implemented | Hook testing utilities |

### utils/ - Shared Utilities

| File | Status | Purpose |
|------|--------|---------|
| `__init__.py` | Implemented | Module exports for all utilities |
| `input.py` | Implemented | `read_stdin_json()` - Parse JSON from stdin |
| `output.py` | Implemented | `log()`, `success_response()`, `block_response()` - Hook output helpers |
| `cache.py` | Implemented | `get_cache()`, `set_cache()` - Shared cache with namespaced keys |
| `git.py` | Implemented | `get_git_status()`, `get_modified_files()`, `is_file_committed()` - Git operations |
| `milestone.py` | Implemented | Path builders and file finders for milestone artifacts |
| `frontmatter.py` | Implemented | YAML frontmatter parsing and validation markers |
| `base_mode.py` | **NEW** | `ModeManager` base class + pre-instantiated mode managers |
| `agent_validation.py` | **NEW** | Agent blocking/validation helpers (`is_task_call()`, `extract_agent_info()`, `block_agent()`) |
| `prerequisites.py` | **NEW** | Shared prerequisite checks (`is_code_committed()`, `is_tdd_commit_complete()`) |

**New Infrastructure (Refactor):**

The utils module was expanded with three new files to reduce code duplication across mode modules:

1. **`base_mode.py`** - `ModeManager` class providing common activate/deactivate patterns:
   - Pre-instantiated managers: `plan_mode`, `research_mode`, `explore_mode`, `code_mode`, `code_review_mode`
   - Methods: `activate()`, `deactivate()`, `is_active()`, `get_session_id()`, `get()`, `set()`

2. **`agent_validation.py`** - Common functions for agent validation:
   - `is_task_call()` - Check if input is Task tool call
   - `extract_agent_info()` - Extract tool name and subagent type
   - `get_subagent_type()` - Works for both PreToolUse and SubagentStop
   - `block_agent()` - Standardized blocking with log + stderr + exit(2)

3. **`prerequisites.py`** - Shared prerequisite checks:
   - `is_code_committed()` - Check no uncommitted changes in src/
   - `is_tdd_commit_complete()` - Check if TDD reached commit phase
   - `check_code_prerequisite()` - Combined check with fallback

**Shared Cache:** `cache.json` stores all hook state with namespace isolation (e.g., `plan_mode.is_active`).

### tests/ - Pytest Test Suite (NEW)

| File | Status | Purpose |
|------|--------|---------|
| `conftest.py` | Implemented | Pytest fixtures for isolated testing |
| `test_utils.py` | Implemented | Unit tests for cache, base_mode, agent_validation, frontmatter |
| `test_security.py` | Implemented | Tests for security validation |
| `test_modes.py` | Implemented | Integration tests for mode modules |

**Note:** Run with `pytest .claude/hooks/tests/` (requires pytest installed).

---

## Summary

| Category | Implemented | Empty/Placeholder |
|----------|-------------|-------------------|
| Root handlers | 6 | 4 |
| plan_mode | 5 | 0 |
| research_mode | 5 | 0 |
| explore_mode | 5 | 0 |
| code_mode | 5 | 0 |
| code_review_mode | 5 | 0 |
| security | 1 | 0 |
| notification | 1 | 0 |
| change_log | 1 | 0 |
| compact | 1 | 0 |
| hooks_test | 1 | 0 |
| utils | 10 | 0 |
| tests | 4 | 0 |
| **Total** | **50** | **4** |

**Refactor Notes (2025-12-01):**
- Added `utils/base_mode.py`, `utils/agent_validation.py`, `utils/prerequisites.py`
- All mode modules now use shared infrastructure
- Deprecated `code/` directory deleted
- Pytest test suite added in `tests/`
- All 65 regression tests passing
