# /init-new-session Command Template

## Command
`/init-new-session <feature> <instructions>`

## Purpose
Initialize a new development session with structured context

## Output Structure

### Session Progress File
**Location**: `tmp/session_[session_id]/progress/session_progress.md`

```markdown
# Session Progress

## Session Information
- **Session ID**: [Generated ID]
- **Started**: [Timestamp]
- **Feature**: [Feature name]
- **Instructions**: [User instructions]

## Context
- **Goal**: [What to achieve]
- **Scope**: [Boundaries]
- **Priority**: [High/Medium/Low]

## Milestones
### Milestone 1: [Name]
- **Status**: [Not Started/In Progress/Complete]
- **Tasks**: [List]

### Milestone 2: [Name]
- **Status**: [Not Started/In Progress/Complete]
- **Tasks**: [List]

## Progress Tracking
### Phase 1: Discovery
- [ ] Codebase exploration
- [ ] Requirements analysis
- [ ] Research topics identified

### Phase 2: Research
- [ ] Technical research
- [ ] Best practices review
- [ ] Solution design

### Phase 3: Implementation
- [ ] Strategy defined
- [ ] Code implementation
- [ ] Testing complete

## Files Generated
- `explore/`: [List]
- `research/`: [List]
- `strategies/`: [List]
- `build/`: [List]

## Dependencies
- **External**: [Libraries/APIs]
- **Internal**: [Modules/Components]

## Risks & Issues
- **Risk 1**: [Description]
- **Issue 1**: [Description]

## Next Steps
1. [Next action]
2. [Following action]

## Notes
[Any additional context or decisions]
```

## Process Flow
1. Read session context template
2. Generate session ID
3. Fill template with feature info
4. Create directory structure
5. Initialize progress tracking

## Directory Structure Created
```
tmp/session_[id]/
├── progress/
│   └── session_progress.md
├── explore/
├── research/
├── strategies/
├── build/
└── troubleshoot/
```

## Used By
- All subsequent commands in session