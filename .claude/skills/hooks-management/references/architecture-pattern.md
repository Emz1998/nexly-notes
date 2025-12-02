# Hooks Architecture Pattern Reference

## Overview

The `.claude/hooks/` folder implements an event-driven architecture for Claude Code automation.

---

## Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Code Events                       │
├─────────────────────────────────────────────────────────────┤
│  SessionStart │ PreToolUse │ PostToolUse │ Stop │ etc.      │
└───────┬───────┴─────┬──────┴──────┬──────┴──┬───┴───────────┘
        │             │              │         │
        ▼             ▼              ▼         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Root Event Handlers                        │
│  session_start.py │ pre_tool_use.py │ stop.py │ etc.        │
└───────┬───────────┴────────┬────────┴────┬──────────────────┘
        │                    │             │
        ▼                    ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Specialized Modules                       │
│  plan_mode/ │ research_mode/ │ explore_mode/ │ code_mode/   │
│  code_review_mode/ │ security/                               │
└───────┬─────┴─────┬─────┴───────┬───────┴───────────────────┘
        │           │             │
        ▼           ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                     Shared Utilities                         │
│        utils/input │ utils/output │ utils/cache │ utils/git │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Shared State (cache.json)                  │
│  { "plan_mode": {...}, "implement": {...}, ... }            │
└─────────────────────────────────────────────────────────────┘
```

---

## Design Patterns

### 1. Dispatcher Pattern

Root-level handlers act as dispatchers that delegate to specialized modules:

```python
# pre_tool_use.py (dispatcher)
from plan_mode import validate_plan

def main():
    validate_plan()  # Delegates to module
```

### 2. Module Encapsulation

Each subdirectory is a self-contained module with:
- `__init__.py` - Public API exports
- Internal implementation files
- Uses shared `utils/` for common operations

```
plan_mode/
├── __init__.py                  # Exports: activate_plan_mode, deactivate, block_premature_agents, validate_subagent_stop
├── activate.py                  # Internal: activation logic (uses utils/)
├── deactivate.py                # Internal: deactivation logic (uses utils/)
├── block_premature_agents.py    # Internal: blocks agents without required dependencies
└── validate_subagent_stop.py    # Internal: validates subagent work completion

research_mode/
├── __init__.py                  # Exports: activate_research_mode, deactivate, block_premature_agents, validate_subagent_stop
├── activate.py                  # Internal: activation logic (uses utils/)
├── deactivate.py                # Internal: deactivation logic (uses utils/)
├── block_premature_agents.py    # Internal: blocks agents without required dependencies (explore, research)
└── validate_subagent_stop.py    # Internal: validates research subagent work completion + commit

explore_mode/
├── __init__.py                  # Exports: activate_explore_mode, deactivate, block_premature_agents, validate_subagent_stop
├── activate.py                  # Internal: activation logic on /implement command (uses utils/)
├── deactivate.py                # Internal: deactivation logic (uses utils/)
├── block_premature_agents.py    # Internal: blocks codebase-explorer if specs/tasks.md missing
└── validate_subagent_stop.py    # Internal: validates codebase-status file created

code_review_mode/
├── __init__.py                  # Exports: activate_code_review_mode, deactivate, block_premature_agents, validate_subagent_stop
├── activate.py                  # Internal: activation logic on /code-review command (uses utils/)
├── deactivate.py                # Internal: deactivation logic (uses utils/)
├── block_premature_agents.py    # Internal: blocks code-reviewer if code not committed
└── validate_subagent_stop.py    # Internal: validates review report created with required content
```

### 3. Shared Utilities Pattern

All hooks import from `utils/` for common operations:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import read_stdin_json, set_cache, get_cache, log
```

**Available utilities:**

| Module | Functions | Purpose |
|--------|-----------|---------|
| `utils/input.py` | `read_stdin_json()` | Parse JSON from stdin |
| `utils/output.py` | `log()`, `success_response()`, `block_response()` | Hook output helpers |
| `utils/cache.py` | `get_cache()`, `set_cache()` | Namespaced state persistence |
| `utils/git.py` | `get_git_status()`, `get_modified_files()`, `is_file_committed()` | Git operations |
| `utils/milestone.py` | Path builders and file finders | Milestone path helpers |
| `utils/frontmatter.py` | `parse_frontmatter()`, `has_consultation_marker()` | YAML frontmatter parsing |
| `utils/base_mode.py` | `ModeManager`, `plan_mode`, `research_mode`, etc. | Mode state management |
| `utils/agent_validation.py` | `is_task_call()`, `extract_agent_info()`, `block_agent()` | Agent validation helpers |
| `utils/prerequisites.py` | `is_code_committed()`, `is_tdd_commit_complete()` | Shared prerequisite checks |

### 4. Namespaced Cache Management

State is persisted in a shared `cache.json` with namespace isolation:

```python
from utils import get_cache, set_cache

# Write with namespace
set_cache("plan_mode", "is_active", True)
set_cache("plan_mode", "session_id", "abc-123")

# Read with namespace
is_active = get_cache("plan_mode", "is_active")
session_id = get_cache("plan_mode", "session_id")
```

**Resulting `cache.json`:**
```json
{
  "plan_mode": {
    "is_active": true,
    "session_id": "abc-123"
  },
  "implement": {
    "current_phase": "explore"
  }
}
```

### 5. Exit Code Conventions

| Exit Code | Meaning |
|-----------|---------|
| 0 | ALLOW - Tool proceeds normally |
| 2 | BLOCK - Tool blocked, message shown to Claude |

```python
from utils import log, block_response

def validate():
    if not valid:
        log("Validation failed")  # stderr
        block_response("Reason")  # exits with code 2
    sys.exit(0)  # allow
```

### 6. Hook Response Format

Hooks communicate via JSON on stdout:

```python
from utils import success_response

# Add context (SessionStart, UserPromptSubmit)
success_response("SessionStart", "Session initialized with ID: abc-123")

# Block with reason (PreToolUse)
response = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Security Policy Violation"
    }
}
print(json.dumps(response))

# Allow silently
print(json.dumps({"suppressOutput": True}))
```

---

## Event Flow Examples

### Session Start Flow

```
SessionStart Event
    │
    ▼
session_start.py
    │
    ├── read_stdin_json() ─► utils/input.py
    │
    ├── get_milestone() ─► project/status.json
    │
    ├── set_cache("plan_mode", "session_id", id) ─► cache.json
    │
    └── Return additionalContext with session info
```

### Pre-Tool Validation Flow

```
PreToolUse Event
    │
    ▼
pre_tool_use.py
    │
    ├── validate_security() ─► security/security.py
    │                              │
    │                              ├── check_dangerous_path()
    │                              │
    │                              ├── check_dangerous_command()
    │                              │
    │                              └── exit(0) or exit(2)
    │
    └── block_premature_agents() ─► plan_mode/block_premature_agents.py
                                        │
                                        ├── Check if tool_name == "Task"
                                        │
                                        ├── Check if subagent_type in (strategic-planner, consulting-expert)
                                        │
                                        ├── get_cache("plan_mode", "is_active")
                                        │
                                        ├── strategic-planner: Check research file exists
                                        │
                                        ├── consulting-expert: Check plan file exists
                                        │
                                        └── exit(0) or exit(2)
```

### Plan Mode Activation Flow

```
UserPromptSubmit Event (prompt starts with "/plan")
    │
    ▼
user_prompt_submit.py
    │
    ├── activate_plan_mode() ─► plan_mode/activate.py
    │                               │
    │                               ├── read_stdin_json() ─► utils/input.py
    │                               │
    │                               ├── Check prompt.startswith("/plan")
    │                               │
    │                               ├── set_cache("plan_mode", "is_active", True)
    │                               │
    │                               └── Print "Planning Phase" message
    │
    └── exit(0)
```

### Plan Command Validation Sequence

```
/plan command triggers validation sequence:

Step 1: Research Report Validation (PreToolUse:Task)
┌─────────────────────────────────────────────────────────────┐
│  User requests strategic-planner via Task tool              │
│                          │                                  │
│                          ▼                                  │
│  pre_tool_use.py ─► block_premature_agents(input_data)      │
│                          │                                  │
│          ┌───────────────┴───────────────┐                  │
│          │                               │                  │
│          ▼                               ▼                  │
│   Research EXISTS              Research NOT FOUND           │
│   exit(0) ALLOW                exit(2) BLOCK                │
│                         "Research report not found.         │
│                          Call research-specialist first."   │
└─────────────────────────────────────────────────────────────┘

Step 2: Plan Creation Validation (SubagentStop)
┌─────────────────────────────────────────────────────────────┐
│  strategic-planner attempts to stop                         │
│                          │                                  │
│                          ▼                                  │
│  subagent_stop.py ─► validate_subagent_stop(input_data)     │
│                          │                                  │
│          ┌───────────────┴───────────────┐                  │
│          │                               │                  │
│          ▼                               ▼                  │
│   Plan file EXISTS               Plan NOT CREATED           │
│   exit(0) ALLOW STOP             exit(2) BLOCK STOP         │
│                         "Plan not created.                  │
│                          Continue working."                 │
└─────────────────────────────────────────────────────────────┘

Step 3: Plan Dependency Validation (PreToolUse:Task)
┌─────────────────────────────────────────────────────────────┐
│  User requests consulting-expert via Task tool              │
│                          │                                  │
│                          ▼                                  │
│  pre_tool_use.py ─► block_premature_agents(input_data)      │
│                          │                                  │
│          ┌───────────────┴───────────────┐                  │
│          │                               │                  │
│          ▼                               ▼                  │
│   Plan file EXISTS               Plan NOT FOUND             │
│   exit(0) ALLOW                  exit(2) BLOCK              │
│                         "Plan file not found.               │
│                          Call strategic-planner first."     │
└─────────────────────────────────────────────────────────────┘

Step 4: Plan Consultation Validation (SubagentStop)
┌─────────────────────────────────────────────────────────────┐
│  consulting-expert attempts to stop                         │
│                          │                                  │
│                          ▼                                  │
│  subagent_stop.py ─► validate_subagent_stop(input_data)     │
│                          │                                  │
│          ┌───────────────┴───────────────┐                  │
│          │                               │                  │
│          ▼                               ▼                  │
│   Frontmatter has              Frontmatter MISSING          │
│   consulted_by marker          consulted_by marker          │
│   exit(0) ALLOW STOP           exit(2) BLOCK STOP           │
│                         "Plan not consulted.                │
│                          Add frontmatter."                  │
└─────────────────────────────────────────────────────────────┘
```

### Research Command Validation Sequence

```
/research command triggers validation sequence:

Step 1: Explore Dependency Check (PreToolUse:Task)
┌─────────────────────────────────────────────────────────────┐
│  User requests research-specialist via Task tool             │
│                          │                                   │
│                          ▼                                   │
│  pre_tool_use.py ─► block_premature_agents(input_data)       │
│                          │                                   │
│          ┌───────────────┴───────────────┐                   │
│          │                               │                   │
│          ▼                               ▼                   │
│   codebase-status_*     codebase-status_* file               │
│   file EXISTS           NOT FOUND in exploration/            │
│   exit(0) ALLOW                   exit(2) BLOCK              │
│                         "codebase-status file not found.     │
│                          Run explore phase first."           │
└─────────────────────────────────────────────────────────────┘

Step 2: Research Report Creation (SubagentStop)
┌─────────────────────────────────────────────────────────────┐
│  research-specialist attempts to stop                        │
│                          │                                   │
│                          ▼                                   │
│  subagent_stop.py ─► validate_subagent_stop(input_data)      │
│                          │                                   │
│          ┌───────────────┴───────────────┐                   │
│          │                               │                   │
│          ▼                               ▼                   │
│   Research file EXISTS           Research NOT CREATED        │
│   exit(0) ALLOW STOP             exit(2) BLOCK STOP          │
│                         "Research report not created.        │
│                          Continue working."                  │
└─────────────────────────────────────────────────────────────┘

Step 3: Research Dependency Check (PreToolUse:Task)
┌─────────────────────────────────────────────────────────────┐
│  User requests research-consultant via Task tool             │
│                          │                                   │
│                          ▼                                   │
│  pre_tool_use.py ─► block_premature_agents(input_data)       │
│                          │                                   │
│          ┌───────────────┴───────────────┐                   │
│          │                               │                   │
│          ▼                               ▼                   │
│   Research file EXISTS           Research NOT FOUND          │
│   exit(0) ALLOW                  exit(2) BLOCK               │
│                         "Research report not found.          │
│                          Call research-specialist first."    │
└─────────────────────────────────────────────────────────────┘

Step 4: Research Validation Marker (SubagentStop)
┌─────────────────────────────────────────────────────────────┐
│  research-consultant attempts to stop                        │
│                          │                                   │
│                          ▼                                   │
│  subagent_stop.py ─► validate_subagent_stop(input_data)      │
│                          │                                   │
│          ┌───────────────┴───────────────┐                   │
│          │                               │                   │
│          ▼                               ▼                   │
│   Frontmatter has                Frontmatter MISSING         │
│   validated_by marker            validated_by marker         │
│   exit(0) continue               exit(2) BLOCK STOP          │
│          │                       "Research not validated.    │
│          ▼                        Add frontmatter."          │
│   Check if committed                                         │
│          │                                                   │
│          ▼                                                   │
│   Committed? ─► YES ─► exit(0) ALLOW STOP                    │
│          │                                                   │
│          ▼                                                   │
│   NO ─► exit(2) BLOCK STOP                                   │
│         "Research not committed."                            │
└─────────────────────────────────────────────────────────────┘
```

### Explore Command Validation Sequence

```
/implement command triggers explore validation sequence:

Step 1: Tasks Dependency Check (PreToolUse:Task)
┌─────────────────────────────────────────────────────────────┐
│  User requests codebase-explorer via Task tool              │
│                          │                                  │
│                          ▼                                  │
│  pre_tool_use.py ─► block_premature_agents(input_data)      │
│                          │                                  │
│          ┌───────────────┴───────────────┐                  │
│          │                               │                  │
│          ▼                               ▼                  │
│   specs/tasks.md EXISTS         specs/tasks.md NOT FOUND    │
│   exit(0) ALLOW                        exit(2) BLOCK        │
│                         "specs/tasks.md file not found.     │
│                          Generate tasks first."             │
└─────────────────────────────────────────────────────────────┘

Step 2: Codebase Status Creation (SubagentStop)
┌─────────────────────────────────────────────────────────────┐
│  codebase-explorer attempts to stop                         │
│                          │                                  │
│                          ▼                                  │
│  subagent_stop.py ─► validate_subagent_stop(input_data)     │
│                          │                                  │
│          ┌───────────────┴───────────────┐                  │
│          │                               │                  │
│          ▼                               ▼                  │
│   codebase-status_*       codebase-status_* file            │
│   file EXISTS             NOT FOUND in exploration/         │
│   exit(0) ALLOW STOP      exit(2) BLOCK STOP                │
│                         "codebase-status file not created.  │
│                          Continue exploration."             │
└─────────────────────────────────────────────────────────────┘
```

### Code Review Command Validation Sequence

```
/code-review command triggers code review validation sequence:

Step 1: Prerequisites Check (UserPromptSubmit)
┌─────────────────────────────────────────────────────────────┐
│  User enters /code-review command                           │
│                          │                                  │
│                          ▼                                  │
│  user_prompt_submit.py ─► activate_code_review_mode()       │
│                          │                                  │
│          ┌───────────────┴───────────────┐                  │
│          │                               │                  │
│          ▼                               ▼                  │
│   No uncommitted src/     Uncommitted src/ changes          │
│   changes (git-based)     found                             │
│   exit(0) ACTIVATE             │                            │
│                                ▼                            │
│                     code_mode.current_phase                 │
│                     == "commit"?                            │
│                          │                                  │
│          ┌───────────────┴───────────────┐                  │
│          │                               │                  │
│          ▼                               ▼                  │
│   YES ─► exit(0)              NO ─► exit(2) BLOCK           │
│          ACTIVATE             "Code not committed.          │
│                                Complete coding first."      │
└─────────────────────────────────────────────────────────────┘

Step 2: Code-Reviewer Agent Check (PreToolUse:Task)
┌─────────────────────────────────────────────────────────────┐
│  User requests code-reviewer via Task tool                  │
│                          │                                  │
│                          ▼                                  │
│  pre_tool_use.py ─► block_premature_agents(input_data)      │
│                          │                                  │
│          ┌───────────────┴───────────────┐                  │
│          │                               │                  │
│          ▼                               ▼                  │
│   code_review_mode        code_review_mode                  │
│   is_active == True       is_active != True                 │
│   return (ALLOW)                │                           │
│                                 ▼                           │
│                     No uncommitted src/ changes?            │
│                          │                                  │
│          ┌───────────────┴───────────────┐                  │
│          │                               │                  │
│          ▼                               ▼                  │
│   YES ─► return            NO ─► Check TDD commit phase     │
│          (ALLOW)                   │                        │
│                    ┌───────────────┴───────────────┐        │
│                    │                               │        │
│                    ▼                               ▼        │
│              YES ─► return         NO ─► exit(2) BLOCK      │
│                    (ALLOW)         "Code not committed."    │
└─────────────────────────────────────────────────────────────┘

Step 3: Review Report Validation (SubagentStop)
┌─────────────────────────────────────────────────────────────┐
│  code-reviewer agent attempts to stop                       │
│                          │                                  │
│                          ▼                                  │
│  subagent_stop.py ─► validate_subagent_stop(input_data)     │
│                          │                                  │
│          ┌───────────────┴───────────────┐                  │
│          │                               │                  │
│          ▼                               ▼                  │
│   code_review_mode        code_review_mode                  │
│   is_active == True       is_active != True                 │
│          │                return (ALLOW)                    │
│          ▼                                                  │
│   Review file exists?                                       │
│          │                                                  │
│          ▼                                                  │
│   YES ─► Validate content                                   │
│          │                                                  │
│          ▼                                                  │
│   Contains "summary"        NO ─► exit(2) BLOCK             │
│   and "findings"?           "Review file not found."        │
│          │                                                  │
│          ▼                                                  │
│   Length >= 200 chars?                                      │
│          │                                                  │
│          ▼                                                  │
│   YES ─► Deactivate mode                                    │
│          return (ALLOW STOP)                                │
│          "Code review complete."                            │
│                                                             │
│   NO ─► exit(2) BLOCK                                       │
│         "Review incomplete. Missing sections/content."      │
└─────────────────────────────────────────────────────────────┘
```

---

## Best Practices

### 1. Always Use Utils

Import from `utils/` for standard operations:
```python
from utils import read_stdin_json, set_cache, get_cache, log
```

### 2. Namespace Your Cache Keys

Always use your module name as namespace:
```python
set_cache("my_module", "key", value)  # Good
set_cache("key", value)                # Bad - no namespace
```

### 3. Fail-Safe Design

Hooks should never crash Claude Code:
```python
try:
    # Hook logic
except Exception as e:
    log(f"Error: {e}")
    sys.exit(0)  # Allow on error
```

### 4. Minimal Output

Only output when necessary:
```python
# Suppress output for allow decisions
print(json.dumps({"suppressOutput": True}))
```

### 5. Path Independence

Use `sys.path.insert` for utils imports:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import read_stdin_json
```

### 6. Logging Strategy

- User-facing messages: `print()` to stdout
- Debug/error messages: `log()` to stderr
- Security events: Dedicated log files

---

## File Organization

```
.claude/hooks/
├── cache.json               # Shared state with namespaced keys
├── [event]_[action].py      # Root handlers (snake_case)
├── plan_mode/               # Plan mode feature module
│   ├── __init__.py          # Public exports
│   ├── activate.py          # Activation logic
│   ├── deactivate.py        # Deactivation logic
│   ├── block_premature_agents.py   # Blocks agents without dependencies
│   └── validate_subagent_stop.py   # Validates subagent work completion
├── research_mode/           # Research mode feature module
│   ├── __init__.py          # Public exports
│   ├── activate.py          # Activation logic
│   ├── deactivate.py        # Deactivation logic
│   ├── block_premature_agents.py   # Blocks agents without dependencies
│   └── validate_subagent_stop.py   # Validates subagent work + commit
├── explore_mode/            # Explore mode feature module
│   ├── __init__.py          # Public exports
│   ├── activate.py          # Activation logic on /implement command
│   ├── deactivate.py        # Deactivation logic
│   ├── block_premature_agents.py   # Blocks codebase-explorer if tasks.md missing
│   └── validate_subagent_stop.py   # Validates codebase-status file created
├── code_review_mode/        # Code review mode feature module
│   ├── __init__.py          # Public exports
│   ├── activate.py          # Activation logic on /code-review command
│   ├── deactivate.py        # Deactivation logic
│   ├── block_premature_agents.py   # Blocks code-reviewer if code not committed
│   └── validate_subagent_stop.py   # Validates review report with required content
└── utils/                   # Shared utilities
    ├── __init__.py          # Module exports
    ├── input.py             # read_stdin_json()
    ├── output.py            # log(), success_response(), block_response()
    ├── cache.py             # get_cache(), set_cache()
    ├── git.py               # get_git_status(), get_modified_files(), is_file_committed()
    ├── milestone.py         # get_milestone_info(), find_research_file(), find_plan_file(), find_explore_status_file(), find_review_file()
    └── frontmatter.py       # parse_frontmatter(), has_consultation_marker(), has_research_validation_marker()
```
