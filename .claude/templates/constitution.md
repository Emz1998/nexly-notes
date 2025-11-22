# Project Constitution

**Project**: [PROJECT_NAME]  
**Tech Stack**: [TECHNOLOGIES]  
**Last Updated**: [DATE]

---

## Core Instructions

### Primary Objective

[DESCRIBE_MAIN_GOAL]

### Code Generation Principles

1. [PRINCIPLE_1] (e.g., Always write TypeScript with strict types)
2. [PRINCIPLE_2] (e.g., Prefer functional components over class components)
3. [PRINCIPLE_3] (e.g., Follow existing patterns in codebase)

---

## File Operations

### When Creating Files

```

IF [CONDITION]:

- Create at: [PATH_PATTERN]
- Use template: [TEMPLATE_NAME]
- Include: [REQUIRED_ELEMENTS]

```

### When Modifying Files

```

ALWAYS:

- [ACTION_1] (e.g., Preserve existing imports order)
- [ACTION_2] (e.g., Match surrounding code style)

NEVER:

- [RESTRICTION_1] (e.g., Remove existing comments without explicit instruction)
- [RESTRICTION_2] (e.g., Change file structure without confirmation)

```

---

## Code Patterns

### Component Structure

```typescript
// REQUIRED PATTERN:
// FORBIDDEN PATTERN:
[EXAMPLE_CODE_STRUCTURE][ANTI_PATTERN_EXAMPLE];
```

### Function Naming

```
PATTERN: [NAMING_PATTERN]

Examples:
✓ [GOOD_EXAMPLE_1]
✓ [GOOD_EXAMPLE_2]
✗ [BAD_EXAMPLE_1]
✗ [BAD_EXAMPLE_2]
```

### Import Organization

```typescript
// ORDER:
1. [IMPORT_TYPE_1] (e.g., React/external libraries)
2. [IMPORT_TYPE_2] (e.g., Internal components)
3. [IMPORT_TYPE_3] (e.g., Types)
4. [IMPORT_TYPE_4] (e.g., Utils/helpers)
5. [IMPORT_TYPE_5] (e.g., Styles/assets)
```

---

## Decision Trees

### Adding New Feature

```
1. Check if [CONDITION_1]:
   YES → [ACTION_A]
   NO → Proceed to step 2

2. Does it require [CONDITION_2]:
   YES → [ACTION_B] then [ACTION_C]
   NO → [ACTION_D]

3. [FINAL_STEP]
```

### Handling Errors

```
IF [ERROR_TYPE_1]:
  - [HANDLING_METHOD_1]

IF [ERROR_TYPE_2]:
  - [HANDLING_METHOD_2]

DEFAULT:
  - [DEFAULT_HANDLING]
```

---

## Explicit Do's and Don'ts

### ALWAYS Do

- [ ] [ACTION_1]
- [ ] [ACTION_2]
- [ ] [ACTION_3]

### NEVER Do

- [ ] [RESTRICTION_1]
- [ ] [RESTRICTION_2]
- [ ] [RESTRICTION_3]

### ASK Before

- [ ] [UNCERTAIN_ACTION_1]
- [ ] [UNCERTAIN_ACTION_2]

---

## Type Safety

### Type Requirements

```typescript
// REQUIRED:
// PREFERRED:
// FORBIDDEN:
[TYPE_REQUIREMENT_1][TYPE_ANTI_PATTERN][TYPE_BEST_PRACTICE];
```

### When to Use

- `type`: [USAGE_CONDITION]
- `interface`: [USAGE_CONDITION]
- `enum`: [USAGE_CONDITION]
- `const`: [USAGE_CONDITION]

---

## Testing Requirements

### Test Coverage Rules

```
IF [FILE_TYPE]:
  - Must include: [TEST_REQUIREMENTS]
  - Test pattern: [PATTERN]

IF [FEATURE_TYPE]:
  - Required tests: [TEST_LIST]
```

### Test Naming

```
PATTERN: [DESCRIPTION_PATTERN]

Template:
describe('[COMPONENT/FUNCTION]', () => {
  it('should [EXPECTED_BEHAVIOR] when [CONDITION]', () => {
    // test
  });
});
```

---

## Error Handling

### Standard Pattern

```typescript
[ERROR_HANDLING_TEMPLATE];
```

### Error Messages

- Format: `[MESSAGE_FORMAT]`
- Must include: `[REQUIRED_INFO]`
- User-facing: `[USER_MESSAGE_STYLE]`
- Developer-facing: `[DEV_MESSAGE_STYLE]`

---

## Comments & Documentation

### When to Comment

```
REQUIRED for:
- [SCENARIO_1]
- [SCENARIO_2]

OPTIONAL for:
- [SCENARIO_3]

NEVER for:
- [SCENARIO_4]
```

### Comment Format

```typescript
// [FORMAT_EXAMPLE]

/**
 * [JSDOC_EXAMPLE]
 */
```

---

## Context Awareness

### Project-Specific Terms

- `[TERM_1]` means: [DEFINITION]
- `[TERM_2]` means: [DEFINITION]
- `[TERM_3]` refers to: [DEFINITION]

### Existing Patterns to Follow

Location: `[FILE_PATH]`
Pattern: `[DESCRIPTION]`

---

## Validation Checklist

Before submitting code, verify:

- [ ] [CHECK_1]
- [ ] [CHECK_2]
- [ ] [CHECK_3]
- [ ] [CHECK_4]
- [ ] [CHECK_5]

---

## Communication Protocol

### When Uncertain

1. [CLARIFICATION_APPROACH]
2. [DEFAULT_ASSUMPTION] if no response

### Presenting Options

Format:

```
Option 1: [APPROACH_A]
Pros: [PROS]
Cons: [CONS]

Option 2: [APPROACH_B]
Pros: [PROS]
Cons: [CONS]

Recommendation: [CHOICE] because [REASONING]
```

### Flagging Issues

When encountering:

- [ISSUE_TYPE_1]: [REPORTING_METHOD]
- [ISSUE_TYPE_2]: [REPORTING_METHOD]

---

## Special Instructions

### [SPECIFIC_SCENARIO_1]

```
Context: [DESCRIPTION]
Action: [SPECIFIC_INSTRUCTION]
Reason: [EXPLANATION]
```

### [SPECIFIC_SCENARIO_2]

```
Context: [DESCRIPTION]
Action: [SPECIFIC_INSTRUCTION]
Reason: [EXPLANATION]
```

---

## Examples

### Complete Example 1: [SCENARIO_NAME]

```typescript
[FULL_CODE_EXAMPLE];
```

### Complete Example 2: [SCENARIO_NAME]

```typescript
[FULL_CODE_EXAMPLE];
```

---

## Version Control

### Commit Message Format

```
[TYPE]: [DESCRIPTION]

[OPTIONAL_BODY]

[OPTIONAL_FOOTER]
```

### When to Suggest Commits

- After: [TRIGGER_1]
- Before: [TRIGGER_2]
- Every: [FREQUENCY]

---

## Priority Matrix

When conflicts arise, prioritize in this order:

1. [PRIORITY_1] (e.g., Type safety)
2. [PRIORITY_2] (e.g., User experience)
3. [PRIORITY_3] (e.g., Code readability)
4. [PRIORITY_4] (e.g., Performance)
5. [PRIORITY_5] (e.g., Brevity)

---

## Emergency Protocols

### If Build Fails

1. [STEP_1]
2. [STEP_2]
3. [STEP_3]

### If Tests Fail

1. [STEP_1]
2. [STEP_2]

### If Uncertain About Major Change

1. [ESCALATION_PROCEDURE]

---

**Compliance**: LLM must acknowledge understanding of these rules before beginning work.

```

This template is optimized for LLM interpretation with clear decision trees, explicit examples, and unambiguous instructions!
```
