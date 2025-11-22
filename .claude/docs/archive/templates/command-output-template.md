# Command Output Template

## Command Metadata
- **Command Name**: `[command-name]`
- **Timestamp**: `[ISO-8601 timestamp]`
- **Session ID**: `[session-id]`
- **Execution Time**: `[duration in ms]`
- **Status**: `[success|failure|partial]`

## Input Parameters
- **Primary Input**: `[main parameter or target]`
- **Options/Flags**:
  - `[option-name]`: `[value]`
  - `[flag-name]`: `[enabled/disabled]`
- **Context Path**: `[working directory or scope]`

## Execution Summary
### Pre-Execution State
- **Prerequisites Met**: `[yes/no]`
- **Validation Results**: `[passed/failed - details]`
- **Environment Check**: `[status]`

### Main Execution
- **Actions Performed**:
  1. `[action-1 description]`
  2. `[action-2 description]`
  3. `[action-n description]`
- **Files Modified**:
  - `[file-path]`: `[operation-type]`
- **Dependencies Handled**: `[list or none]`

## Results
### Primary Output
```
[main command output or generated content]
[max 50 lines - truncate if longer]
```

### Metrics
- **Lines Processed**: `[count]`
- **Files Affected**: `[count]`
- **Tokens Used**: `[count if applicable]`
- **Memory Peak**: `[MB if relevant]`

### Generated Artifacts
- **Created Files**:
  - `[file-path]`: `[size, type]`
- **Modified Files**:
  - `[file-path]`: `[changes summary]`
- **Deleted Files**:
  - `[file-path]`: `[reason]`

## Validation
### Post-Execution Checks
- **Syntax Validation**: `[passed/failed]`
- **Lint Results**: `[clean/warnings/errors]`
- **Type Check**: `[passed/failed/n/a]`
- **Test Status**: `[passed/failed/skipped]`

### Warnings
- `[warning-1 if any]`
- `[warning-2 if any]`

### Errors
- `[error-1 if any]`
- `[error-2 if any]`

## Side Effects
- **State Changes**: `[description or none]`
- **External Calls**: `[APIs/services contacted or none]`
- **Cache Updates**: `[yes/no - details]`
- **Hooks Triggered**: `[list or none]`

## Recommendations
### Next Steps
1. `[recommended action 1]`
2. `[recommended action 2]`

### Optimization Opportunities
- `[suggestion if applicable]`

### Potential Issues
- `[risk or concern if identified]`

## Debug Information
### Environment
- **Node Version**: `[version if relevant]`
- **OS**: `[platform]`
- **Memory Available**: `[GB]`
- **CPU Load**: `[percentage]`

### Stack Trace (if error)
```
[error stack trace if applicable]
[max 15 lines]
```

### Raw Logs (if verbose mode)
```
[detailed logs if requested]
[max 20 lines]
```

## Rollback Information
- **Rollback Available**: `[yes/no]`
- **Backup Location**: `[path or n/a]`
- **Rollback Command**: `[command or n/a]`

## Performance Analysis
- **Bottlenecks Identified**: `[description or none]`
- **Optimization Applied**: `[yes/no - details]`
- **Cache Hit Rate**: `[percentage if applicable]`

## Compliance Check
- **Standards Met**: `[list applicable standards]`
- **Security Scan**: `[passed/issues found]`
- **License Compliance**: `[ok/review needed]`

## User Feedback Required
- **Confirmations Needed**: `[list or none]`
- **Manual Steps**: `[list or none]`
- **Review Points**: `[list or none]`

## Summary
**Result**: `[one-line summary of outcome]`
**Impact**: `[description of changes made]`
**Success Rate**: `[percentage if measurable]`
**Quality Score**: `[A-F rating if applicable]`

---
*Template Version: 1.0.0*
*Max Lines: 150*