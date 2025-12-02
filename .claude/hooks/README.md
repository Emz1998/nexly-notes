# Claude Code Hooks

Validation hooks for enforcing workflow discipline in Claude Code sessions.

## Validation Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          VALIDATION WORKFLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  /explore ────► EXPLORE ──► RESEARCH ──► PLAN ──► CODE ──► CODE-REVIEW     │
│                   │            │          │        │           │            │
│                   ▼            ▼          ▼        ▼           ▼            │
│              codebase-    research-   strategic  TDD       code-           │
│              explorer     specialist  -planner   phases    reviewer        │
│                   │            │          │        │           │            │
│                   ▼            ▼          ▼        ▼           ▼            │
│              codebase-    research-   consulting test →    review          │
│              status.md    report.md   -expert    impl →    report.md       │
│                                           │      refactor                   │
│                                           ▼                                 │
│                                       plan.md                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Mode Activation Commands

| Command        | Mode             | Purpose                               |
| -------------- | ---------------- | ------------------------------------- |
| `/explore`     | explore_mode     | Analyze codebase before research      |
| `/research`    | research_mode    | Research before planning              |
| `/plan`        | plan_mode        | Create implementation plan            |
| `/code`        | code_mode        | TDD workflow (Red → Green → Refactor) |
| `/code-review` | code_review_mode | Review committed code                 |

## Validation Sequences

### Explore Mode (`/explore`)

```
Prerequisites:
  └── specs/tasks.md must exist

Workflow:
  1. [PreToolUse] Block codebase-explorer if tasks.md missing
  2. [SubagentStop] Validate codebase-status file created

Output:
  └── exploration/codebase-status_[session]_[date].md
```

### Research Mode (`/research`)

```
Prerequisites:
  └── Codebase status file must exist (from explore)

Workflow:
  1. [PreToolUse] Block research-specialist without codebase status
  2. [SubagentStop] Validate research report created
  3. [PreToolUse] Block research-consultant without research report
  4. [SubagentStop] Validate frontmatter: validated_by: research-consultant
  5. [SubagentStop] Validate research file committed

Output:
  └── project/[milestone]/research/research_[session]_[date].md
```

### Plan Mode (`/plan`)

```
Prerequisites:
  └── Research report must exist (from research)

Workflow:
  1. [PreToolUse] Block strategic-planner without research report
  2. [SubagentStop] Validate plan file created
  3. [PreToolUse] Block consulting-expert without plan file
  4. [SubagentStop] Validate frontmatter: consulted_by: consulting-expert

Output:
  └── project/[milestone]/plans/plan_[session]_[date].md
```

### Code Mode (`/code`)

```
Prerequisites:
  └── Plan file must exist (from plan)

TDD Phases:
  ┌─────────────────┬────────────────────┬─────────────────────┐
  │ Phase           │ Agent Required     │ Validation          │
  ├─────────────────┼────────────────────┼─────────────────────┤
  │ failing_test    │ test-engineer      │ Tests exist & fail  │
  │ passing_test    │ (main agent)       │ Tests pass          │
  │ refactor        │ (main agent)       │ Tests still pass    │
  │ troubleshoot    │ troubleshooter     │ Issues resolved     │
  │ commit          │ (direct)           │ Changes committed   │
  └─────────────────┴────────────────────┴─────────────────────┘

Workflow:
  1. [UserPromptSubmit] Block /code without plan file
  2. [PreToolUse] Block wrong agents per phase
  3. [SubagentStop] Validate phase completion, advance to next
```

### Code Review Mode (`/code-review`)

```
Prerequisites (either):
  └── No uncommitted changes in src/, OR
  └── code_mode.current_phase == "commit"

Workflow:
  1. [PreToolUse] Block code-reviewer if code not committed
  2. [SubagentStop] Validate review report created
  3. [SubagentStop] Validate required sections (summary, findings)
  4. [SubagentStop] Validate minimum content length (200 chars)

Output:
  └── project/[milestone]/reviews/review_[session]_[date].md
```

## Architecture

### Dispatcher Pattern

```
Event Handler (root)          Mode Modules
─────────────────────         ────────────────────────────
pre_tool_use.py        ──►    {mode}/block_premature_agents.py
subagent_stop.py       ──►    {mode}/validate_subagent_stop.py
user_prompt_submit.py  ──►    {mode}/activate.py
stop.py                ──►    {mode}/deactivate.py
```

### Directory Structure

```
.claude/hooks/
├── README.md                    # This file
├── cache.json                   # Shared state (namespaced)
│
├── # Root Event Handlers
├── session_start.py             # Initialize session
├── pre_tool_use.py              # Dispatch to mode validators
├── subagent_stop.py             # Dispatch to stop validators
├── user_prompt_submit.py        # Mode activation
├── stop.py                      # Mode deactivation
│
├── # Mode Modules
├── plan_mode/
│   ├── activate.py
│   ├── deactivate.py
│   ├── block_premature_agents.py
│   └── validate_subagent_stop.py
├── research_mode/               # Same structure
├── explore_mode/                # Same structure
├── code_mode/                   # Same structure + TDD phases
├── code_review_mode/            # Same structure
│
├── # Shared Utilities
├── utils/
│   ├── __init__.py              # All exports
│   ├── input.py                 # read_stdin_json()
│   ├── output.py                # log(), block_response()
│   ├── cache.py                 # get_cache(), set_cache()
│   ├── git.py                   # Git operations
│   ├── milestone.py             # Path builders
│   ├── frontmatter.py           # YAML frontmatter parsing
│   ├── base_mode.py             # ModeManager class
│   ├── agent_validation.py      # Agent helpers
│   └── prerequisites.py         # Shared checks
│
├── # Other Modules
├── security/                    # Security validation
├── notification/                # Push notifications
└── tests/                       # Pytest test suite
```

## Shared Utilities

### ModeManager

```python
from utils import plan_mode, code_mode

# Check mode state
plan_mode.is_active()        # True/False
plan_mode.get_session_id()   # "abc-123"

# Activate/deactivate
plan_mode.activate(session_id, "Message")
plan_mode.deactivate()

# Extra state (code_mode)
code_mode.get("current_phase")  # "failing_test"
code_mode.set("current_phase", "passing_test")
```

### Agent Validation

```python
from utils import is_task_call, extract_agent_info, block_agent

if is_task_call(input_data):
    tool_name, subagent = extract_agent_info(input_data)
    if subagent == "forbidden-agent":
        block_agent("Reason for blocking")
```

### Prerequisites

```python
from utils import is_code_committed, is_tdd_commit_complete

committed, msg = is_code_committed()  # Check src/ clean
tdd_done = is_tdd_commit_complete()   # Check TDD phase
```

## Exit Codes

| Code | Meaning | Effect                                    |
| ---- | ------- | ----------------------------------------- |
| 0    | ALLOW   | Operation proceeds                        |
| 2    | BLOCK   | Operation blocked, stderr shown to Claude |

## Cache Namespaces

State is stored in `cache.json` with namespace isolation:

```json
{
  "plan_mode": {
    "is_active": true,
    "session_id": "abc-123"
  },
  "code_mode": {
    "is_active": false,
    "current_phase": "commit",
    "plan_file": "/path/to/plan.md"
  }
}
```

## Testing

```bash
# Run pytest suite
pytest .claude/hooks/tests/

# Run regression tests
python3 .claude/hooks/hooks_test/test-hooks.py
```
