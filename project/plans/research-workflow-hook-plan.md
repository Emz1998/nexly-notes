# Research Workflow Validation Hook - Implementation Plan

## Overview

Create a validation hook system for the `/research` command that enforces workflow dependencies similar to the existing `/plan` command workflow in `plan_mode/`.

## Dependencies Analysis

Based on the requirements:

1. **research/** must depend on **exploration/** (specifically `codebase-status_[session-id]_[MMDDYY].md`)
2. **research-specialist** must run first, then **research-consultant** in sequence
3. **research-consultant** depends on research-specialist's report
4. Research report path: `project/[MS-NN]:[MS-Description]/researches/research_[session-id]_[MMDDYY].md`
5. **research-consultant** must modify the research report metadata (frontmatter)
6. **Commit** after research-consultant finishes
7. Stop validation: research md must exist, commit must be successful

## Validation Sequence (Similar to plan_mode)

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
│   codebase-status.md              codebase-status.md         │
│   EXISTS                          NOT FOUND                  │
│   exit(0) ALLOW                   exit(2) BLOCK              │
│                         "codebase-status.md not found.       │
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
│   exit(0) ALLOW STOP             exit(2) BLOCK STOP          │
│                         "Research not validated.             │
│                          Add frontmatter."                   │
└─────────────────────────────────────────────────────────────┘

Step 5: Git Commit Validation (Stop or SubagentStop)
┌─────────────────────────────────────────────────────────────┐
│  Main agent or subagent attempts to stop                     │
│                          │                                   │
│                          ▼                                   │
│  stop.py ─► validate_research_commit(input_data)             │
│                          │                                   │
│          ┌───────────────┴───────────────┐                   │
│          │                               │                   │
│          ▼                               ▼                   │
│   Research file committed        Research NOT committed      │
│   exit(0) ALLOW STOP             exit(2) BLOCK STOP          │
│                         "Research not committed.             │
│                          Commit changes first."              │
└─────────────────────────────────────────────────────────────┘
```

## File Changes Required

### 1. New Module: `.claude/hooks/research_mode/`

```
research_mode/
├── __init__.py                    # Exports: activate_research_mode, deactivate, block_premature_agents, validate_subagent_stop
├── activate.py                    # Internal: activation logic
├── deactivate.py                  # Internal: deactivation logic
├── block_premature_agents.py      # Internal: blocks agents without dependencies
└── validate_subagent_stop.py      # Internal: validates subagent work completion
```

### 2. Utility Updates: `.claude/hooks/utils/`

**milestone.py additions:**
- `find_explore_status_file(session_id)` - Find codebase-status.md
- `build_research_path(session_id)` - Already exists, verify it works

**frontmatter.py additions:**
- `has_research_validation_marker(file_path)` - Check for `validated_by: research-consultant`

**git.py additions:**
- `is_file_committed(file_path)` - Check if file is committed in git

### 3. Dispatcher Updates

**pre_tool_use.py:**
- Import `research_mode.block_premature_agents`
- Add call to research validation

**subagent_stop.py:**
- Import `research_mode.validate_subagent_stop`
- Add call to research validation

**user_prompt_submit.py:**
- Import `research_mode.activate_research_mode`
- Detect `/research` command and activate research mode

**stop.py:**
- Add commit validation for research workflow

## Implementation Steps

### Phase 1: Utility Extensions

1. Add `find_explore_status_file()` to `milestone.py`
2. Add `has_research_validation_marker()` to `frontmatter.py`
3. Add `is_file_committed()` to `git.py`
4. Update `utils/__init__.py` with new exports

### Phase 2: research_mode Module

1. Create `research_mode/__init__.py`
2. Create `research_mode/activate.py`
3. Create `research_mode/deactivate.py`
4. Create `research_mode/block_premature_agents.py`
5. Create `research_mode/validate_subagent_stop.py`

### Phase 3: Dispatcher Integration

1. Update `pre_tool_use.py` - add research validation
2. Update `subagent_stop.py` - add research validation
3. Update `user_prompt_submit.py` - add research mode activation
4. Update `stop.py` - add commit validation

### Phase 4: Testing

1. Test with echo for all validation paths
2. Test edge cases (missing files, missing markers)
3. Test cache state management

### Phase 5: Documentation

1. Update `hooks-status.md`
2. Update `architecture-pattern.md`

## Cache Namespace

Use `research_mode` namespace in `cache.json`:

```json
{
  "research_mode": {
    "is_active": true,
    "session_id": "abc-123",
    "research_file_path": "project/MS-001_Foundation/researches/research_abc-123_120125.md"
  }
}
```

## Agents to Validate

| Agent | Dependency | Output |
|-------|------------|--------|
| research-specialist | codebase-status.md exists | research_[session-id]_[MMDDYY].md |
| research-consultant | research file exists | validated_by frontmatter |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | ALLOW - proceed normally |
| 2 | BLOCK - show stderr message to Claude |

## Notes

- Follow the dispatcher pattern: root handlers dispatch to modules
- Use shared utils for all common operations
- Keep modules self-contained with clear public APIs
- Fail-safe design: allow on error to avoid blocking legitimate work
