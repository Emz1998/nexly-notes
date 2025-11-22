# Agent Reports Directory - MOVED

## ⚠️ IMPORTANT: Reports Have Been Relocated

**This directory is DEPRECATED as of 2025-09-07**

All reports have been migrated to a new domain-driven structure for better organization and discoverability.

## 📍 New Location: `/workspace/reports/`

The new structure organizes reports by purpose and domain rather than by date:

```
/workspace/reports/
├── features/           # Feature-specific development reports
├── operations/         # Operational and maintenance reports  
├── planning/           # Strategic planning and architecture
├── agents/             # AI agent lifecycle documentation
└── archive/            # Historical reports by year
```

### Category Guidelines

**explore/**

- Research and discovery reports
- Market analysis reports
- Technology exploration reports
- Requirement gathering reports
- Feasibility studies

**planning/**

- Project planning reports
- Sprint planning reports
- Architecture planning reports
- Task breakdown reports
- Strategy development reports

**execution/**

- Feature implementation reports
- Component development reports
- API development reports
- Integration development reports
- Test creation and execution reports
- Bug fixing reports
- Code writing reports

**revision/**

- File revision reports
- Code update reports
- Document modification reports
- Refactoring reports
- Optimization reports

**validation/**

- Requirements validation reports
- Code review reports
- Test validation reports
- Quality assurance reports
- Compliance verification reports

**reflection/**

- Main agent self-assessment reports
- Task completion analysis
- Performance evaluation reports
- Lessons learned reports
- Process improvement suggestions

## Report Types

- **Exploration Reports**: Research findings and discovery outcomes
- **Planning Reports**: Strategic plans and task breakdowns
- **Execution Reports**: Development and implementation outcomes
- **Revision Reports**: Documentation of file/code changes
- **Validation Reports**: Quality checks and verification results
- **Reflection Reports**: Self-assessment and performance analysis

## Naming Convention

### Folder Structure

- Date folder: `YYYY-MM-DD` (always use current date)
- Category folder: Use one of the 6 defined categories (explore, planning, execution, revision, validation, reflection)
- No additional subdirectories unless explicitly required

### File Naming

- Pattern: `[descriptive-name]-[type]-[timestamp].md`
- Examples:
  - `auth-service-test-1430.md`
  - `api-documentation-docs-1615.md`
  - `login-component-refactor-0930.md`
  - `pr-123-git-1200.md`
  - `memory-leak-debug-1845.md`
- Use lowercase with hyphens
- Include timestamp for uniqueness (HHMM format)

## Report Components

- Sequential thinking process
- Task evaluation (strengths/improvements)
- Performance metrics (0-100 scores)
- Actionable recommendations
- Confidence levels

## Usage

### Creating Reports

```bash
# All agents and commands must create reports
# Save to appropriate category folder:
.claude/agent-reports/[YYYY-MM-DD]/[category]/

# Example paths:
.claude/agent-reports/2025-08-17/explore/market-research-1430.md
.claude/agent-reports/2025-08-17/planning/sprint-plan-0900.md
.claude/agent-reports/2025-08-17/execution/auth-implementation-1600.md
.claude/agent-reports/2025-08-17/revision/api-update-1400.md
.claude/agent-reports/2025-08-17/validation/code-review-1700.md
.claude/agent-reports/2025-08-17/reflection/performance-analysis-1800.md
```

### Report Creation Rules

1. **Mandatory**: Every task completion requires a report
2. **Immediate**: Create report before marking task complete
3. **Categorized**: Use the correct category folder
4. **Timestamped**: Include time in filename for uniqueness
5. **Comprehensive**: Include all relevant metrics and outcomes

## Key Metrics Tracked

- Task Completion Score
- Quality Score
- Efficiency Score
- Best Practices Adherence

## Review Schedule

- Daily: Review new reports
- Weekly: Pattern analysis
- Monthly: Agent performance trends

## Access Reports

- Navigate to date folder for daily reports
- Browse category folders for specific report types
- Use grep to search across all reports
- Review patterns for agent improvements
- Generate summaries from category aggregations

## References

- @.claude/agents/quality-assurance/feedback-agent.md - Feedback agent configuration
- @.claude/commands/factory/create-command.md - Command creation with reporting
- @README.md - Detailed documentation

## Compliance

### Report Requirements

- **Every agent task** must generate a report
- **Every command execution** must generate a report
- **Every revision** must document changes
- **Every debug session** must record findings

### Quality Standards

- Clear, actionable content
- Metrics and measurements where applicable
- Recommendations for improvements
- Links to related files or commits

### Enforcement

- Commands include reporting in their templates
- Agents have reporting as final step
- Task completion requires report creation
- Folder structure must be maintained exactly as specified
