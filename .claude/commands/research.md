---
name: research
description: Conduct a comprehensive research based on the required research topics
argument-hint: <instructions>
model: claude-opus-4-1-20250805
---

<context>
  <goal>Conduct a comprehensive research based on the required research topics</goal>
  <special_instructions>${1:-"No instructions"}</special_instructions>
</context>

<tasks>
<task order="1">Read <path>.claude/commands/research-requirements.md</path> and save it to <research-requirements> tags</task>
<task order="2">Run: research-requirements</task>
<task order="3">Read <path>tmp/session_[session_id]/research/required_research_topics.md</path> and save it to <required_research_topics> tags</task>
<task order="4">Launch all the agents to do a research on the required_research_topics in parallel</task>
<task order="5">Instruct all the agents to use context7 MCP server to gather context first</task>
<output_path_for_every_subagent>tmp/session_[session_id]/research/[research_topic_name].md</output_path_for_every_subagent>
</tasks>

<important_note>Give every subagents the session id you are currently in and run them in parallel</important_note>