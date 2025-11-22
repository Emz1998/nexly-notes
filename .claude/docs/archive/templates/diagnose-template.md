# /diagnose Command Template

## Command
`/diagnose <instructions> <file_path>`

## Purpose
Diagnose issues and provide comprehensive diagnosis report

## Output Structure

### Diagnosis Report
**Location**: `tmp/session_[session_id]/troubleshoot/diagnosis_report.md`

```markdown
# Diagnosis Report

## Issue Summary
- **Description**: [Brief description]
- **Severity**: [Critical/High/Medium/Low]
- **Impact**: [What's affected]

## Symptoms
- **Observed Behavior**: [What's happening]
- **Expected Behavior**: [What should happen]
- **Error Messages**: [Any errors]

## Baseline Comparison
- **Normal Parameters**: [Expected values]
- **Current Parameters**: [Actual values]
- **Deviations**: [Differences]

## History Review
- **Recent Changes**: [What changed]
- **Past Issues**: [Similar problems]
- **Maintenance Records**: [Related fixes]

## Diagnostic Tests
- **Test 1**: [Result]
- **Test 2**: [Result]
- **Test 3**: [Result]

## Key Metrics
- **Performance**: [Metrics]
- **Resource Usage**: [CPU/Memory/Disk]
- **Response Times**: [Measurements]

## Pattern Analysis
- **Correlations**: [Related issues]
- **Triggers**: [What causes it]
- **Frequency**: [How often]

## Root Cause Hypothesis
- **Primary Cause**: [Most likely]
- **Secondary Causes**: [Other possibilities]
- **Confidence Level**: [High/Medium/Low]

## Validation Results
- **Hypothesis Test**: [Pass/Fail]
- **Evidence**: [Supporting data]

## Recommendations
1. [Action 1]
2. [Action 2]
3. [Action 3]
```

## Process Flow
1. Gather symptoms
2. Collect baseline data
3. Review history
4. Run diagnostic tests
5. Measure key metrics
6. Analyze patterns
7. Form hypothesis
8. Validate findings
9. Generate report

## Used By
- `/fix` command (reads this diagnosis)