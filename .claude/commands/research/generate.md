---
name: research-strategy
description: Research implementation strategy, deprecated patterns, and best practices by delegating to research-specialist agent
allowed-tools: Task
argument-hint: <task-or-feature-to-research>
model: sonnet
---

**Goal**: Invoke the research-specialist agent to research the optimal implementation strategy for a given task, including deprecated patterns to avoid, best practices, and recommended approaches
**User Instructions**: $ARGUMENTS

## Tasks

1. Invoke @agent-research-specialist to research:

   - Best implementation strategy for the specified task/feature
   - Deprecated APIs, patterns, or libraries that should be avoided
   - Current best practices and industry standards
   - Recommended libraries, frameworks, or approaches
   - Potential pitfalls, anti-patterns, and common mistakes
   - Performance considerations and optimization strategies

2. Invoke @agent-research-consultant to review the research findings for:
   - Completeness of strategy coverage
   - Accuracy of best practice recommendations
   - Validity of deprecated pattern identification
   - Feasibility of recommended approaches for the NEXLY RN project

## Subagent Delegation Prompt

Delegate to `research-specialist` with this prompt:

```
Research implementation strategy for: $ARGUMENTS

Conduct comprehensive research covering:

1. **Implementation Strategy**
   - Optimal architecture and design patterns for this task
   - Step-by-step implementation approach
   - Integration points with existing codebase

2. **Deprecated Patterns to Avoid**
   - Identify deprecated APIs, methods, or libraries related to this task
   - Find official deprecation notices and migration paths
   - Document breaking changes to watch for

3. **Best Practices**
   - Current industry standards and conventions
   - Performance optimization techniques
   - Security considerations and best practices
   - Testing strategies and patterns

4. **Library/Framework Recommendations**
   - Evaluate relevant libraries with pros/cons
   - Check compatibility with React Native/Next.js ecosystem
   - Verify active maintenance and community support

5. **Risk Assessment**
   - Potential pitfalls and anti-patterns
   - Common implementation mistakes to avoid
   - Edge cases and error handling considerations

Output: Comprehensive research report with actionable recommendations
```

## Prohibited Tasks

- Implementing any code changes. Only research and document findings.
- Modifying any production code
- Making assumptions without verification from official sources
- Skipping the research-consultant review
- Creating implementation plans (this is research only)

## Success Criteria

- Implementation strategy is clearly defined with reasoning
- Deprecated patterns are identified with modern alternatives
- Best practices are verified from authoritative sources
- Recommendations are specific to NEXLY RN project context
- Research is reviewed and validated by research-consultant
- Report includes proper citations and credibility assessments

## Examples

```bash
/research:strategy offline-first data sync with Dexie
/research:strategy authentication flow with Supabase
/research:strategy Tiptap editor with AI autocomplete
/research:strategy PWA manifest and service worker setup
```
