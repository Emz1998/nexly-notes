# /specs Command Template

## Command
`/specs <specs-needed> <requirements>`

## Purpose
Create specification documents for different project aspects

## Spec Types
- **technical-specs**: System architecture and tech stack
- **database-architecture**: Data models and storage
- **design-system**: UI/UX standards and components
- **prd-architecture**: Product requirements document
- **ci-cd-specs**: Deployment and automation

## Output Structure

### Technical Specifications
**Location**: `docs/specs/tech-specs.md`

```markdown
# Technical Specifications

## Architecture Overview
- **Pattern**: [Microservices/Monolithic/Serverless]
- **Stack**: [Frontend/Backend/Database]
- **Deployment**: [Cloud/On-premise]

## Technology Stack
### Frontend
- **Framework**: React + TypeScript
- **Styling**: Tailwind + Shadcn
- **State**: Context API / Zustand
- **Build**: Vite

### Backend
- **Platform**: Firebase
- **Functions**: Cloud Functions
- **Auth**: Firebase Auth
- **Storage**: Firestore + Cloud Storage

### AI Integration
- **Provider**: Claude API
- **Context**: Vector DB
- **Processing**: Edge Functions

## System Requirements
- **Performance**: [Metrics]
- **Scalability**: [Targets]
- **Security**: [Standards]
- **Compliance**: FERPA/HIPAA
```

### Database Architecture
**Location**: `docs/specs/database-architecture.md`

```markdown
# Database Architecture

## Data Models
### Users Collection
- id: string
- email: string
- profile: object
- created: timestamp

### Content Collection
- id: string
- type: string
- data: object
- metadata: object

## Relationships
- One-to-Many: [Examples]
- Many-to-Many: [Examples]

## Indexing Strategy
- Primary indexes
- Composite indexes
- Full-text search

## Security Rules
- Read permissions
- Write permissions
- Validation rules
```

### Design System
**Location**: `docs/specs/design-system.md`

```markdown
# Design System Specifications

## Brand Guidelines
- **Colors**: [Palette]
- **Typography**: [Fonts]
- **Spacing**: [System]
- **Icons**: [Library]

## Component Library
- Buttons
- Forms
- Cards
- Modals
- Navigation

## Patterns
- Layout grids
- Responsive breakpoints
- Animation standards
- Accessibility requirements
```

### PRD Architecture
**Location**: `docs/specs/prd-architecture.md`

```markdown
# Product Requirements Document

## Product Vision
[Vision statement]

## User Stories
### Story 1
- **As a**: [User type]
- **I want**: [Action]
- **So that**: [Benefit]

## Features
### Feature 1
- **Description**: [What]
- **Priority**: [P0/P1/P2]
- **Acceptance Criteria**: [List]

## Success Metrics
- KPI 1: [Metric]
- KPI 2: [Metric]

## Timeline
- Phase 1: [Features]
- Phase 2: [Features]
```

### CI/CD Specifications
**Location**: `docs/specs/ci-cd-specs.md`

```markdown
# CI/CD Specifications

## Pipeline Architecture
- **Source Control**: GitHub
- **CI Platform**: GitHub Actions
- **Deployment**: Firebase Hosting

## Build Process
1. Lint and format
2. Type check
3. Unit tests
4. Integration tests
5. Build artifacts

## Deployment Strategy
- **Environments**: Dev/Staging/Prod
- **Triggers**: [Conditions]
- **Rollback**: [Process]

## Quality Gates
- Code coverage > 80%
- No critical vulnerabilities
- Performance benchmarks met
```

## Process Flow
1. Read app vision document
2. Deploy appropriate specialist
3. Research best practices
4. Generate specification
5. Write to docs/specs/

## Agents Used
- **system-architect**: Technical specs
- **database-architect**: Database design
- **design-system-architect**: Design system
- **prd-architect**: Product requirements
- **ci-cd-specialist**: CI/CD pipeline