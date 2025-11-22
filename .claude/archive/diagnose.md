---
name: diagnose
description: Diagnose the issue and provide a diagnosis report
argument-hint: <instructions> <file_path>
model: claude-opus-4-1-20250805
---

<context>
  <goal>Diagnose the issue and provide a diagnosis report</goal>
  <user_instructions>${1:-"Ask the user for instructions"}</user_instructions>
  <file_path>${2:-"No file path"}</file_path>
</context>


<tasks>
<important_note>Instuct the debugging_specialist subagent to do the following tasks</important_note>
<task order="1" title="Gather symptoms">Document all observed issues, behaviors, and error patterns</task>
<task order="2" title="Collect baseline data">Record normal operating parameters for comparison</task>
<task order="3" title="Review history">Check maintenance records, past issues, and recent changes</task>
<task order="4" title="Run diagnostic tests">Execute built-in diagnostics, scans, or testing tools</task>
<task order="5" title="Measure key metrics">Monitor performance indicators, resource usage, and outputs</task>
<task order="6" title="Compare against standards">Check specifications, benchmarks, and expected values</task>
<task order="7" title="Analyze patterns">Identify correlations between symptoms and conditions</task>
<task order="8" title="Form hypothesis">Develop theories about root cause based on evidence</task>
<task order="9" title="Validate findings">Test hypothesis through targeted verification steps</task>
<task order="10" title="Generate report">Document diagnosis, confidence level, and recommended actions</task>
<output_path>tmp/session_[session_id]/troubleshoot/diagnosis_report.md</output_path>
</tasks>

