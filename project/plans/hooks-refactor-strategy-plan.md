# Hooks Refactor Strategy Plan

## Executive Summary

This plan outlines a comprehensive refactoring strategy for the `.claude/hooks/` directory. The goal is to eliminate redundant code patterns, improve maintainability, and enhance code reusability while preserving existing dispatcher logic and ensuring all 65 regression tests continue to pass.

---

## Current State Analysis

### Baseline
- **Regression Tests**: 65/65 passing
- **Total Python Files**: 54 files
- **Mode Modules**: 5 (plan_mode, research_mode, explore_mode, code_mode, code_review_mode)
- **Utility Modules**: 7 (input, output, cache, git, milestone, frontmatter, parser)
- **Deprecated Code**: `.claude/hooks/code/` directory (replaced by `code_mode/`)

### Identified Redundancies

#### 1. Boilerplate Code (HIGH PRIORITY)
Every mode module file repeats:
```python
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

**Files affected**: All 25+ mode module files

#### 2. Activation Pattern Duplication (HIGH PRIORITY)
All 5 `activate.py` files follow the identical pattern:
- `plan_mode/activate.py` (24 lines)
- `research_mode/activate.py` (24 lines)
- `explore_mode/activate.py` (24 lines)
- `code_mode/activate.py` (78 lines) - includes additional logic
- `code_review_mode/activate.py` (71 lines) - includes prerequisite checks

**Common Pattern**:
```python
def activate_<mode>_mode(input_data: dict):
    session_id = input_data.get("session_id", "")
    set_cache("<mode>_mode", "is_active", True)
    set_cache("<mode>_mode", "session_id", session_id)
    print("<Message>")
```

#### 3. Deactivation Pattern Duplication (HIGH PRIORITY)
All 5 `deactivate.py` files are nearly identical:
- `plan_mode/deactivate.py` (24 lines)
- `research_mode/deactivate.py` (19 lines)
- `explore_mode/deactivate.py` (19 lines)
- `code_mode/deactivate.py` (28 lines) - clears 4 cache keys
- `code_review_mode/deactivate.py` (28 lines)

**Common Pattern**:
```python
def deactivate():
    set_cache("<mode>_mode", "is_active", False)
    set_cache("<mode>_mode", "session_id", "")
```

#### 4. Block Premature Agents Pattern (MEDIUM PRIORITY)
Common structure in all 5 `block_premature_agents.py`:
1. Check if tool is "Task"
2. Extract `subagent_type`
3. Check if mode is active
4. Get session_id from cache
5. Validate dependencies
6. Block with `sys.exit(2)` or allow

#### 5. Validate Subagent Stop Pattern (MEDIUM PRIORITY)
Common structure in all 5 `validate_subagent_stop.py`:
1. Check if mode is active
2. Extract `subagent_type`
3. Get session_id from cache
4. Validate completion requirements
5. Block with `sys.exit(2)` or allow

#### 6. Duplicated Helper Functions (MEDIUM PRIORITY)
- `is_code_committed()` duplicated in:
  - `code_review_mode/activate.py`
  - `code_review_mode/block_premature_agents.py`
- `is_tdd_commit_complete()` duplicated in same files

#### 7. Exit Code Inconsistency (LOW PRIORITY)
Some files use `sys.exit(0)` where `return` would be more appropriate:
- `plan_mode/deactivate.py` uses `sys.exit(0)`
- `code_mode/block_premature_agents.py` uses `sys.exit(0)` for allow cases
- Others properly use `return` for allow cases

---

## Refactoring Strategy

### Phase 1: Foundation Improvements

#### 1.1 Create Base Mode Module (`utils/base_mode.py`)
Extract common functionality into a reusable base:

```python
# utils/base_mode.py
class ModeManager:
    """Base class for mode state management."""

    def __init__(self, mode_name: str, cache_keys: list[str] = None):
        self.mode_name = mode_name
        self.namespace = f"{mode_name}_mode"
        self.cache_keys = cache_keys or ["is_active", "session_id"]

    def activate(self, session_id: str, message: str, **extra_cache) -> None:
        """Activate mode with common pattern."""
        set_cache(self.namespace, "is_active", True)
        set_cache(self.namespace, "session_id", session_id)
        for key, value in extra_cache.items():
            set_cache(self.namespace, key, value)
        print(message)

    def deactivate(self) -> None:
        """Deactivate mode and clear cache."""
        for key in self.cache_keys:
            set_cache(self.namespace, key, "" if key != "is_active" else False)

    def is_active(self) -> bool:
        return get_cache(self.namespace, "is_active") or False

    def get_session_id(self) -> str:
        return get_cache(self.namespace, "session_id") or ""
```

**Impact**: Reduces ~200 lines of duplicate code across activate/deactivate files.

#### 1.2 Create Agent Validation Framework (`utils/agent_validation.py`)
Standardize agent blocking and stop validation:

```python
# utils/agent_validation.py
from typing import Callable, Optional

def extract_agent_info(input_data: dict) -> tuple[str, str]:
    """Extract tool name and subagent type from input."""
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    subagent_type = tool_input.get("subagent_type", "")
    return tool_name, subagent_type

def is_task_call(input_data: dict) -> bool:
    """Check if input is a Task tool call."""
    return input_data.get("tool_name") == "Task"

def block_agent(reason: str) -> None:
    """Block agent with standardized error output."""
    log(reason)
    print(reason, file=sys.stderr)
    sys.exit(2)

def create_dependency_validator(
    target_agents: list[str],
    dependency_checks: dict[str, Callable[[], tuple[bool, str]]]
) -> Callable[[dict, str], None]:
    """Factory for creating agent dependency validators."""
    def validator(input_data: dict, session_id: str) -> None:
        if not is_task_call(input_data):
            return
        _, subagent = extract_agent_info(input_data)
        if subagent not in target_agents:
            return
        if subagent in dependency_checks:
            satisfied, reason = dependency_checks[subagent]()
            if not satisfied:
                block_agent(reason)
    return validator
```

**Impact**: Reduces ~150 lines across block_premature_agents files.

### Phase 2: Mode Module Refactoring

#### 2.1 Refactor Simple Modes (plan_mode, research_mode, explore_mode)
Convert to use base classes:

```python
# plan_mode/activate.py (AFTER)
from utils.base_mode import ModeManager

plan_mode = ModeManager("plan")

def activate_plan_mode(input_data: dict) -> None:
    session_id = input_data.get("session_id", "")
    plan_mode.activate(session_id, "Planning Phase. Do not write any code")
```

**Lines reduced**: ~15 lines per file (75 total)

#### 2.2 Refactor Complex Modes (code_mode, code_review_mode)
Preserve custom logic while using base infrastructure:

```python
# code_mode/activate.py (AFTER)
from utils.base_mode import ModeManager

code_mode = ModeManager("code", ["is_active", "session_id", "current_phase", "plan_file"])

def activate_code_mode(input_data: dict) -> None:
    session_id = input_data.get("session_id", "")
    plan_file = find_plan_file(session_id)
    if not plan_file:
        block_agent("Code Mode: Plan file not found.")
    code_mode.activate(
        session_id,
        "TDD Workflow Started. Phase: failing_test",
        current_phase="failing_test",
        plan_file=str(plan_file)
    )
```

### Phase 3: Consolidate Duplicated Functions

#### 3.1 Move Shared Prerequisites to Utils (`utils/prerequisites.py`)
```python
# utils/prerequisites.py
def is_code_committed() -> tuple[bool, str]:
    """Check if code is committed (no uncommitted changes in src/)."""
    modified = get_modified_files()
    src_modified = [f for f in modified if f.startswith("src/")]
    if src_modified:
        return False, f"Uncommitted: {', '.join(src_modified[:3])}"
    return True, ""

def is_tdd_commit_complete() -> bool:
    """Check if TDD workflow reached commit phase."""
    return get_cache("code_mode", "current_phase") == "commit"
```

**Impact**: Removes duplication in 2 files.

### Phase 4: Cleanup and Standardization

#### 4.1 Fix Exit Code Inconsistencies
- Replace `sys.exit(0)` with `return` in validator functions
- Keep `sys.exit(0)` only in activation functions and standalone scripts
- Use `sys.exit(2)` consistently for blocking

#### 4.2 Remove Deprecated Code
Delete `.claude/hooks/code/` directory (replaced by `code_mode/`)

#### 4.3 Standardize Docstrings
Apply consistent docstring format across all files.

### Phase 5: Testing Infrastructure

#### 5.1 Convert to pytest
Create `tests/hooks/` directory with pytest-based tests:

```python
# tests/hooks/conftest.py
import pytest
import json
from pathlib import Path

@pytest.fixture
def mock_cache(tmp_path, monkeypatch):
    """Create isolated cache for testing."""
    cache_file = tmp_path / "cache.json"
    monkeypatch.setattr("utils.cache.CACHE_PATH", cache_file)
    return cache_file

@pytest.fixture
def sample_input():
    """Factory for creating test input data."""
    def _create(tool_name="Task", subagent_type="", **kwargs):
        return {
            "tool_name": tool_name,
            "tool_input": {"subagent_type": subagent_type, **kwargs},
            "session_id": "test-session"
        }
    return _create
```

#### 5.2 Test Coverage Goals
- Unit tests for all utility functions
- Integration tests for mode activation/deactivation
- Integration tests for agent blocking
- Integration tests for subagent stop validation
- Regression tests (preserve existing 65 tests)

---

## Implementation Order

### Sprint 1: Foundation (Days 1-2)
1. Create `utils/base_mode.py`
2. Create `utils/agent_validation.py`
3. Create `utils/prerequisites.py`
4. Update `utils/__init__.py` exports
5. Run regression tests

### Sprint 2: Simple Modes (Days 3-4)
1. Refactor `plan_mode/` using base classes
2. Refactor `research_mode/` using base classes
3. Refactor `explore_mode/` using base classes
4. Run regression tests after each mode

### Sprint 3: Complex Modes (Days 5-6)
1. Refactor `code_mode/` preserving TDD logic
2. Refactor `code_review_mode/` preserving prerequisite checks
3. Run regression tests

### Sprint 4: Cleanup & Testing (Days 7-8)
1. Fix exit code inconsistencies
2. Remove deprecated code
3. Standardize docstrings
4. Create pytest test suite
5. Final regression test run

---

## Risk Mitigation

### Risks
1. **Breaking existing functionality**: Mode dispatchers depend on specific function signatures
2. **Cache namespace changes**: Any namespace change breaks existing cache entries
3. **Import path changes**: Changes to `utils/` imports affect all modules

### Mitigations
1. Run regression tests after every file change
2. Keep cache namespace strings unchanged
3. Add new utilities without removing existing ones initially
4. Use feature flags or parallel implementations during transition

---

## Success Criteria

1. **All 65 regression tests pass**
2. **Code reduction**: ~300-400 lines removed
3. **No duplicate functions**: `is_code_committed()` and `is_tdd_commit_complete()` exist once
4. **Consistent patterns**: All modes use base classes
5. **pytest integration**: Test suite runnable via `pytest tests/hooks/`
6. **Documentation updated**: `hooks-status.md` and `architecture-pattern.md` reflect changes

---

## Files to Create

| File | Purpose |
|------|---------|
| `utils/base_mode.py` | Base class for mode management |
| `utils/agent_validation.py` | Agent blocking/validation helpers |
| `utils/prerequisites.py` | Shared prerequisite check functions |
| `tests/hooks/conftest.py` | pytest fixtures |
| `tests/hooks/test_utils.py` | Unit tests for utilities |
| `tests/hooks/test_modes.py` | Integration tests for modes |

## Files to Modify

| File | Changes |
|------|---------|
| `utils/__init__.py` | Add exports for new utilities |
| `plan_mode/*.py` | Use base classes |
| `research_mode/*.py` | Use base classes |
| `explore_mode/*.py` | Use base classes |
| `code_mode/*.py` | Use base classes, fix exit codes |
| `code_review_mode/*.py` | Use base classes, consolidate helpers |

## Files to Delete

| File | Reason |
|------|--------|
| `.claude/hooks/code/` | Deprecated, replaced by `code_mode/` |

---

## Estimated Impact

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total Lines | ~2000 | ~1600 | -20% |
| Duplicate Functions | 3 | 0 | -100% |
| Boilerplate per file | 5 lines | 1 line | -80% |
| Test Framework | Custom | pytest | Improved |

---

## Approval Required

Before proceeding with implementation:
1. Review the base class design
2. Confirm pytest is acceptable for testing
3. Approve deletion of deprecated `code/` directory
4. Confirm cache namespace strings must remain unchanged
