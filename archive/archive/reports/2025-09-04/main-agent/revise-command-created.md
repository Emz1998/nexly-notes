# Revise Command Creation Report

**Date**: 2025-09-04  
**Task**: Create revision command for file improvements  
**Status**: Complete

## Summary

Created flexible file revision command that orchestrates specialized agents to analyze and improve files based on user requirements.

## Key Features

1. **Flexible Arguments**: Supports file path, revision instructions, scope, and style preferences
2. **Multi-Phase Workflow**: Analysis, planning, implementation, validation, documentation
3. **Agent Orchestration**: Delegates to specialized agents based on file type
4. **Standards Compliance**: Enforces project coding and documentation rules
5. **Comprehensive Validation**: Ensures improvements don't break functionality

## Command Structure

- **Name**: revise
- **Tools**: 9 essential tools for file analysis and modification
- **Arguments**: 4 parameters (2 required, 2 optional)
- **Phases**: 6 workflow phases from analysis to reporting
- **Agents**: 6 specialized agents for different improvement types

## Usage Examples

```bash
/revise @docs/example.md "improve clarity and structure"
/revise /src/component.tsx "optimize performance" full modernize
/revise @prototype/styles.css "fix inconsistencies" partial maintain
```

## Deliverables

- Command file: `.claude/commands/revise.md`
- Supports code, documentation, config, and style files
- Generates detailed revision reports
- Maintains version control best practices

## Next Steps

- Test command with various file types
- Refine agent selection logic
- Add support for batch revisions
- Integrate with CI/CD workflows

---
*Report generated: 2025-09-04*