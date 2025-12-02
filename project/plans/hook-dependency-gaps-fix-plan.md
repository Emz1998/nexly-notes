---
title: Hook Dependency Gaps Analysis and Fix Plan
type: plan
status: pending_approval
created: 2025-12-01
author: claude
---

# Hook Dependency Gaps Analysis and Fix Plan

## Executive Summary

Analysis of the plan_mode hooks revealed **1 critical dependency gap** and **2 minor gaps** in the validation chain. The critical gap allows `consulting-expert` to be called without a plan file existing, causing confusing error messages and potential infinite retry loops.

---

## Current State Analysis

### Validation Flow Diagram

```
┌─────────────────────┐
│ research-specialist │ → Creates research report
│                     │   PreToolUse: NONE
│                     │   SubagentStop: NONE ⚠️ (minor gap)
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ strategic-planner   │ → Creates plan file
│                     │   PreToolUse: ✅ Blocked if research missing
│                     │   SubagentStop: ✅ Blocked if plan missing
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ consulting-expert   │ → Adds frontmatter to plan
│                     │   PreToolUse: ❌ NO VALIDATION (CRITICAL GAP)
│                     │   SubagentStop: ✅ Blocked if frontmatter missing
└─────────────────────┘
```

---

## Identified Gaps

### Gap #1: consulting-expert PreToolUse (CRITICAL)

**Location:** `block_strategic_planner.py` - only validates `strategic-planner`

**Problem:**
- `consulting-expert` can be called via Task tool without any plan file existing
- When it tries to stop, `_validate_consulting_expert()` fails because `find_plan_file()` returns None
- Error message says "Add YAML frontmatter..." which is misleading when file doesn't exist

**Impact:**
- Confusing error messages to main agent
- Potential infinite retry loop
- Wasted API calls

**Severity:** HIGH

---

### Gap #2: research-specialist SubagentStop (MEDIUM)

**Location:** `validate_subagent_stop.py` - doesn't validate `research-specialist`

**Problem:**
- `research-specialist` can stop without creating research file
- `strategic-planner` would then be blocked indefinitely

**Impact:**
- Workflow halts with no clear guidance
- Main agent may not understand why strategic-planner is blocked

**Severity:** MEDIUM

---

### Gap #3: Empty Plan File (LOW)

**Location:** `_validate_strategic_planner()` - only checks file existence

**Problem:**
- Plan file could be empty or contain only whitespace
- Validation passes if file exists regardless of content

**Impact:**
- Low practical impact - unlikely to occur in normal operation

**Severity:** LOW

---

## Proposed Fix Plan

### Task 1: Add consulting-expert PreToolUse Validation

**File:** `.claude/hooks/plan_mode/block_strategic_planner.py`

**Change:** Rename to `block_premature_agents.py` and add validation for `consulting-expert`

```python
def block_premature_agents(input_data: dict) -> None:
    """Block agents that don't have their dependencies met."""
    if input_data.get("tool_name") != "Task":
        return

    tool_input = input_data.get("tool_input", {})
    subagent_type = tool_input.get("subagent_type", "")

    if not get_cache("plan_mode", "is_active"):
        return

    session_id = get_cache("plan_mode", "session_id")
    if not session_id:
        return

    # Block strategic-planner if research missing
    if subagent_type == "strategic-planner":
        if not find_research_file(session_id):
            log("Strategic Planner blocked. Research report not found.")
            sys.exit(2)

    # Block consulting-expert if plan missing
    elif subagent_type == "consulting-expert":
        if not find_plan_file(session_id):
            log("Consulting Expert blocked. Plan file not found. "
                "Call strategic-planner first to create the plan.")
            sys.exit(2)
```

**Updates Required:**
- Rename file: `block_strategic_planner.py` → `block_premature_agents.py`
- Update `plan_mode/__init__.py` exports
- Update `pre_tool_use.py` import

---

### Task 2: Add research-specialist SubagentStop Validation (Optional)

**File:** `.claude/hooks/plan_mode/validate_subagent_stop.py`

**Change:** Add validation for `research-specialist`

```python
def _validate_research_specialist(session_id: str) -> bool:
    """Check if research-specialist created the research file."""
    research_file = find_research_file(session_id)
    return research_file is not None and research_file.exists()

def validate_subagent_stop(input_data: dict) -> None:
    # ... existing code ...

    if subagent_type not in ("strategic-planner", "consulting-expert", "research-specialist"):
        return

    # ... existing validations ...

    if subagent_type == "research-specialist":
        if not _validate_research_specialist(session_id):
            log("Research report not created. Continue working on the research document.")
            sys.exit(2)
```

---

### Task 3: Update Imports and Exports

**Files to update:**
1. `.claude/hooks/plan_mode/__init__.py` - Update export name
2. `.claude/hooks/pre_tool_use.py` - Update import

---

## Implementation Order

1. **Task 1** - Critical fix for consulting-expert gap
2. **Task 3** - Update imports/exports
3. **Task 2** - Optional enhancement for research-specialist

---

## Testing Plan

After implementation, test each validation:

```bash
# Test 1: consulting-expert blocked without plan
echo '{"tool_name":"Task","tool_input":{"subagent_type":"consulting-expert"}}' | \
  python3 .claude/hooks/pre_tool_use.py

# Test 2: strategic-planner blocked without research
echo '{"tool_name":"Task","tool_input":{"subagent_type":"strategic-planner"}}' | \
  python3 .claude/hooks/pre_tool_use.py

# Test 3: research-specialist stop validation (if implemented)
echo '{"subagent_type":"research-specialist"}' | \
  python3 .claude/hooks/subagent_stop.py
```

---

## Approval Required

- [ ] Approve Task 1 (Critical - consulting-expert PreToolUse)
- [ ] Approve Task 2 (Optional - research-specialist SubagentStop)
- [ ] Approve Task 3 (Required if Task 1 approved)

---

## Notes

- All changes follow the dispatcher pattern architecture
- No modifications to `settings.local.json` required
- Backward compatible with existing cache structure
