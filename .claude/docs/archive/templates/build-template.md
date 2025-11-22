# /build Command Template

## Command
`/build <instructions> <workflow>`

## Purpose
Build a production-ready feature using TDD or EPE (Explore-Plan-Execute) workflow

## Workflows

### TDD (Test-Driven Development)
```
Red Phase → Green Phase → Refactor Phase
```

### EPE (Explore-Plan-Execute)
```
Explore Phase → Plan Phase → Execute Phase
```

## Output Structure

### Implementation Files
**Location**: Project source directories

### Test Files (TDD)
**Location**: `/tests/` directory

### Implementation Log
**Location**: `tmp/session_[session_id]/build/implementation.log`

```markdown
# Implementation Log

## Strategy Used
[TDD/EPE]

## Phase 1: [Red/Explore]
- **Actions**: [What was done]
- **Findings**: [What was discovered]
- **Files Created**: [List]

## Phase 2: [Green/Plan]
- **Actions**: [What was done]
- **Decisions**: [Key decisions made]
- **Files Modified**: [List]

## Phase 3: [Refactor/Execute]
- **Actions**: [What was done]
- **Improvements**: [What was improved]
- **Final Files**: [List]

## Verification
- **Tests Passing**: [Yes/No]
- **Coverage**: [Percentage]
- **Performance**: [Metrics]
```

## Process Flow
1. Read implementation strategy
2. Choose workflow (TDD or EPE)
3. Execute workflow phases
4. Verify implementation
5. Document results

## Dependencies
- Implementation strategy from `/strategize`
- Codebase context from `/explore`