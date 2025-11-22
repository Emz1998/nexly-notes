# New Command Created: Research

**Date:** 2025-08-26
**Command Name:** research
**Location:** `.claude/commands/research.md`

## Command Overview

Created a comprehensive research command that leverages the research-specialist agent to conduct systematic research using the Firecrawl MCP server.

### Purpose
Conduct comprehensive research on specified topics, analyze findings from multiple sources, and produce detailed research reports that are automatically saved to the appropriate documentation directory.

### Key Features
- Utilizes Firecrawl MCP server for all web searching and scraping operations
- Supports multiple research modes: quick, deep, trends, and best-practices
- Auto-determines appropriate subfolder (guides/ or best-practices/) based on content type
- Generates well-structured markdown reports with proper citations
- Provides actionable conclusions and recommendations

## Command Modes

### 1. Quick Mode (`--quick`)
- Fast research scan of top 5 sources
- Executive summary focus
- Simplified report (max 500 words)
- Ideal for quick overviews

### 2. Deep Mode (`--deep`) [Default]
- Comprehensive research from 10-15 sources
- Cross-referenced findings
- Detailed analysis and synthesis
- Full documentation with citations

### 3. Trends Mode (`--trends`)
- Focus on current developments (last 12 months)
- Timeline of key innovations
- Market analysis and predictions
- Saved as trend analysis guides

### 4. Best Practices Mode (`--best-practices`)
- Industry standards collection
- Implementation examples
- Security and compliance considerations
- Saved to best-practices subfolder

## Usage Examples

```bash
/research "React state management" --deep
/research "AI in healthcare trends" --trends  
/research "API security" --best-practices
/research "Firebase authentication" --quick docs/custom/auth-guide.md
```

## Integration Points

- **Research Specialist Agent:** Leveraged via Task tool for deep research capabilities
- **Firecrawl MCP Server:** Primary tool for web searching and content extraction
- **Sequential Thinking:** Used for systematic research approach
- **Documentation Standards:** Follows project documentation rules and templates

## File Organization

Reports are saved in two locations:
1. **Session Report:** `.claude/reports/YYYY-MM-DD/research-team/research-[topic].md`
2. **Final Document:** `docs/references/[guides|best-practices]/[topic]-[type].md`

## Tools Required

- Task (for research-specialist agent)
- Firecrawl MCP tools (search, scrape, extract)
- WebSearch and WebFetch (fallback)
- Read/Write/MultiEdit (document management)
- Sequential Thinking (research methodology)
- TodoWrite (task tracking)

## Compliance

✅ Follows command template structure
✅ Includes all mandatory rules and guidelines
✅ Uses Sequential Thinking for all tasks
✅ Auto-generates reports after completion
✅ Respects 150-line documentation limit
✅ Properly references project documentation

## Success Metrics

- Comprehensive coverage of research topics
- Multiple authoritative sources cited
- Well-structured, actionable output
- Appropriate categorization (guides vs best-practices)
- Clear citations and references

---

**Command Status:** Successfully created and ready for use