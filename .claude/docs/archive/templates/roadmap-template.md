# /roadmap Command Template

## Command
`/roadmap <action> <scope> <deadline>`

## Purpose
Generate, revise, or track project roadmaps with timeline management

## Actions
- **generate**: Create new roadmap
- **revise**: Update existing roadmap
- **show-progress**: Display progress report

## Output Structure

### Generated Roadmap
**Location**: `docs/plans/roadmap.md`

```markdown
# Project Roadmap

## Overview
- **Project**: NEXLY RN
- **Timeline**: [Start] - [End]
- **Last Updated**: [Date]
- **Version**: [Number]

## Phases

### Phase 1: Foundation (Q1 2025)
#### Sprint 1-2
- [ ] Setup development environment
- [ ] Initialize project structure
- [ ] Configure CI/CD pipeline

#### Sprint 3-4
- [ ] Core authentication system
- [ ] User management
- [ ] Basic UI components

### Phase 2: Core Features (Q2 2025)
#### Sprint 5-6
- [ ] Study planning module
- [ ] Content management
- [ ] AI integration baseline

#### Sprint 7-8
- [ ] Practice questions
- [ ] Progress tracking
- [ ] Performance analytics

### Phase 3: Advanced Features (Q3 2025)
#### Sprint 9-10
- [ ] AI tutoring system
- [ ] Adaptive learning
- [ ] Collaboration tools

### Phase 4: Launch Preparation (Q4 2025)
#### Sprint 11-12
- [ ] Beta testing
- [ ] Performance optimization
- [ ] Security audit
- [ ] Documentation

## Milestones

### M1: MVP Ready
- **Date**: [Target date]
- **Deliverables**: [List]
- **Success Criteria**: [Metrics]

### M2: Beta Launch
- **Date**: [Target date]
- **Deliverables**: [List]
- **Success Criteria**: [Metrics]

### M3: Production Release
- **Date**: [Target date]
- **Deliverables**: [List]
- **Success Criteria**: [Metrics]

## Dependencies
- **External**: [APIs, Services]
- **Internal**: [Components]
- **Critical Path**: [Key dependencies]

## Risk Mitigation
- **Risk 1**: [Description] → [Mitigation]
- **Risk 2**: [Description] → [Mitigation]
- **Buffer Time**: 15% included

## Compliance Checkpoints
### FERPA Compliance
- [ ] Data privacy audit
- [ ] Access control review
- [ ] Documentation complete

### HIPAA Compliance
- [ ] Security assessment
- [ ] Encryption verification
- [ ] Audit trail implementation

## Resource Allocation
- **Development**: [Team size]
- **Design**: [Team size]
- **QA**: [Team size]
- **DevOps**: [Team size]

## Progress Tracking
- **Completed**: [X]%
- **In Progress**: [Y]%
- **Not Started**: [Z]%

## Version History
- **v1.0**: Initial roadmap
- **v1.1**: [Changes made]
- **v1.2**: [Current version]
```

### Progress Report
**Location**: `docs/plans/progress/[date].md`

```markdown
# Progress Report - [Date]

## Executive Summary
- **Overall Progress**: [X]%
- **On Schedule**: [Yes/No/At Risk]
- **Key Achievements**: [List]
- **Blockers**: [List]

## Milestone Status
- **M1**: [Status] - [Completion %]
- **M2**: [Status] - [Completion %]
- **M3**: [Status] - [Completion %]

## Sprint Progress
- **Current Sprint**: [Number]
- **Sprint Goals**: [Achieved/Partial/Missed]
- **Velocity**: [Story points]

## Detailed Progress
[Phase-by-phase breakdown]

## Next Period Focus
[Upcoming priorities]
```

## Process Flow
1. Gather existing context
2. Execute action (generate/revise/show)
3. Validate with expert-consultant
4. Generate output documents

## Agents Used
- **agile-coordinator**: Sprint planning
- **timeline-coordinator**: Milestone tracking
- **progress-tracker**: Progress monitoring
- **expert-consultant**: Validation