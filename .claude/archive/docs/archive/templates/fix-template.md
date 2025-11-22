# /fix Command Template

## Command
`/fix <special_instructions>`

## Purpose
Fix diagnosed issues and provide comprehensive fix report

## Output Structure

### Fix Report
**Location**: `tmp/session_[session_id]/troubleshoot/fix_report.md`

```markdown
# Fix Report

## Issue Fixed
- **Original Problem**: [What was broken]
- **Root Cause**: [From diagnosis]
- **Fix Applied**: [What was done]

## Repair Plan
- **Tools Required**: [What was needed]
- **Resources Used**: [Files/Libraries]
- **Downtime**: [If any]
- **Risk Level**: [Low/Medium/High]

## Backup Status
- **Git Status**: [Clean/Committed]
- **Backup Location**: [Path]
- **Rollback Plan**: [How to revert]

## Implementation Details
### Changes Made
- **File 1**: [What changed]
- **File 2**: [What changed]

### Code Modifications
```diff
- old code
+ new code
```

## Testing Results
- **Immediate Test**: [Pass/Fail]
- **Regression Test**: [Pass/Fail]
- **Performance Test**: [Metrics]

## Side Effects Check
- **New Issues**: [None/List]
- **Dependencies**: [Affected/None]
- **Compatibility**: [Maintained/Issues]

## Stability Monitoring
- **Runtime**: [Duration tested]
- **Errors**: [None/Count]
- **Performance**: [Normal/Degraded]

## Preventive Measures
1. [Safeguard 1]
2. [Safeguard 2]
3. [Monitoring added]

## Documentation Updates
- **Code Comments**: [Added/Updated]
- **README**: [Updated sections]
- **Changelog**: [Entry added]

## Lessons Learned
- **Root Cause**: [Why it happened]
- **Prevention**: [How to avoid]
- **Detection**: [How to catch early]

## Post-Fix Instructions
- **Verification Steps**: [How to verify]
- **Monitoring**: [What to watch]
- **Maintenance**: [Future tasks]

## Status
- **Fix Status**: [Complete/Partial]
- **Confidence**: [High/Medium/Low]
- **Follow-up Required**: [Yes/No]
```

## Process Flow
1. Confirm diagnosis
2. Plan repair
3. Create backup
4. Implement fix
5. Test immediately
6. Check side effects
7. Monitor stability
8. Apply preventive measures
9. Update documentation
10. Communicate completion

## Dependencies
- Diagnosis report from `/diagnose`