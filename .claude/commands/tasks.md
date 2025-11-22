---
name: tasks
description: Generate tasks.md from PRD and tech specs with intelligent assessment
allowed-tools: Read, Write, Glob, Grep
argument-hint: <project-goal>
model: sonnet
---

Create a comprehensive task breakdown document for: $1

## 1. Context

- Main Objective: Generate a complete tasks.md document from @.claude/templates/tasks.md based on specs/prd.md and specs/tech-specs.md
- Secondary Objective: Intelligently assess required phases, sprints, tasks, dependencies, and parallel opportunities from existing specifications
- Output Location: Save the generated tasks.md to `specs/tasks.md`
- User Input: [$1 = project goal or initiative description]

**Critical Requirements:**

- **MUST validate specs/prd.md and specs/tech-specs.md exist first** - Exit with error message if either file doesn't exist
- Base ALL task breakdown on requirements and technical decisions documented in the specs
- Extract tech stack, architecture patterns, and feature requirements from specs
- Phase 1, 2, and 3 are mandatory (Foundation, Build, Deployment)
- Only add additional phases if absolutely necessary based on project complexity in specs
- Avoid overengineering - lean and precise approach over complex and bloated
- Identify all task dependencies and parallel opportunities
- Mark parallel tasks with `[P]` notation
- Allocate appropriate subagents from `.claude/agents/` for independent tasks
- Work for ANY project type (web, mobile, desktop, backend, ML, data pipeline, etc.)

## 2. Tasks

### Phase 1: Validation & Spec Analysis

- T001: Check if `specs/prd.md` exists
  - If NOT exist: Exit with error "❌ specs/prd.md not found. Create PRD first using /specs prd <description>"
- T002: Check if `specs/tech-specs.md` exists
  - If NOT exist: Exit with error "❌ specs/tech-specs.md not found. Create tech specs first using /specs tech-specs <description>"
- T003 [P]: Read and parse `specs/prd.md` to extract:
  - Product requirements and features
  - User stories and workflows
  - Success criteria and constraints
  - Non-functional requirements
- T004 [P]: Read and parse `specs/tech-specs.md` to extract:
  - Technology stack and frameworks
  - Architecture patterns and decisions
  - Data models and schemas
  - API specifications
  - Testing strategy
  - Deployment approach
- T005: Read the tasks template from `.claude/templates/tasks.md`
- T006: Analyze project goal $1 in context of PRD and tech specs to determine scope

### Phase 2: Foundation Phase Planning

- T007: Identify environment setup requirements based on tech stack from specs:
  - Programming languages and runtime versions
  - Package managers and dependency tools
  - Development tools and IDEs
  - Environment variables and configuration
- T008: Identify dependency installation requirements:
  - Core libraries and frameworks (from tech specs)
  - Development dependencies
  - Testing frameworks
  - Build tools and bundlers
- T009: Identify type/contract definition requirements:
  - Data models (from tech specs data section)
  - API contracts (from tech specs API section)
  - Validation schemas
  - Interface definitions
- T010: Identify test infrastructure setup requirements:
  - Unit testing framework
  - Integration testing approach
  - E2E testing tools
  - Test database/environment setup
- T011: Define SPRINT-001 and SPRINT-002 for Phase 1 (Foundation) with specific goals and tasks

### Phase 3: Build Phase Planning

- T012: Extract feature list from PRD functional requirements
- T013: Identify feature dependencies and logical grouping
- T014: Determine appropriate number of sprints (3-7 sprints typical)
- T015: For each feature group, identify:
  - Backend/API work (if applicable)
  - Frontend/UI work (if applicable)
  - Database schema changes
  - Integration requirements
  - Testing needs
- T016: Assign features to sprints based on dependencies and complexity
- T017: Define all Build phase sprints with goals, tasks, and acceptance criteria

### Phase 4: Deployment Phase Planning

- T018: Identify deployment requirements from tech specs:
  - Hosting platform and infrastructure
  - CI/CD pipeline setup
  - Environment configuration (dev/staging/prod)
  - Monitoring and logging setup
  - Performance testing requirements
- T019: Define deployment phase sprints (typically 1-2 sprints)
- T020: Add deployment verification and rollback procedures

### Phase 5: Dependencies & Parallel Opportunities

- T021: Identify sprint-level dependencies:
  - Which sprints must complete before others
  - Why (shared types, API contracts, etc.)
- T022: Identify task-level dependencies:
  - Which tasks block other tasks
  - Critical path (longest dependency chain)
- T023: Mark all independent tasks with `[P]` notation
- T024: Identify parallel sprint opportunities (different domains/teams)
- T025: Allocate subagents for parallel independent work:
  - frontend-engineer: UI/component work
  - backend-engineer: API/server/database work
  - test-engineer: Test infrastructure and test suites
  - system-architect: Architecture decisions and documentation
  - strategic-planner: Complex planning and strategy
  - prototype-engineer: POC and experimental features
- T026: Document all dependencies and parallel opportunities

### Phase 6: Documentation & Output

- T027: Fill out Overview section:
  - Project title (from $1 or PRD)
  - Related documentation links (prd.md, tech-specs.md, etc.)
  - Task Status Legend
- T028: Fill out all sprint sections with:
  - Sprint goal
  - Task list with IDs
  - Acceptance criteria
  - Verification steps
- T029: Complete Implementation Strategy section
- T030: Add Risks & Blockers section based on PRD challenges/risks
- T031: Ensure all template sections are filled (no empty placeholders)
- T032: Write completed tasks.md to `specs/tasks.md`
- T033: Verify file was created successfully

## 3. Implementation Strategy

- **Specs-Driven**: Extract ALL information from specs/prd.md and specs/tech-specs.md - don't guess or assume
- **Conservative Approach**: Start with minimal viable task breakdown, avoid unnecessary complexity
- **Tech Stack Aware**: Use actual tech stack from specs (don't assume Next.js, React, etc.)
- **Feature-Based Sprints**: Group related features into logical sprints
- **Realistic Dependencies**: Map actual technical dependencies from specs
- **Smart Parallelization**: Identify truly independent work based on architecture
- **Subagent Delegation**: Assign specialized agents to domain-specific parallel tasks
- **Quality Over Quantity**: Fewer precise tasks are better than many vague ones
- **Foundation First**: Ensure strong Phase 1 foundation before building features

## 4. Constraints

**CRITICAL: Follow these rules exactly:**

### Spec Dependency

- **MUST check for specs/prd.md and specs/tech-specs.md existence FIRST**
- If either file missing: Exit with clear error message and instructions
- ALL task breakdown must be derived from specs content, not assumptions
- Tech stack must match what's in specs/tech-specs.md exactly
- Features must match what's in specs/prd.md functional requirements

### Phase Requirements

- Phase 1, 2, and 3 are MANDATORY
- Only add Phase 4+ if specs indicate complex multi-stage needs
- Phase 1 MUST include (adapt to tech stack):
  - Environment setup (language, tools, configs)
  - Dependency installation
  - Type/contract definitions (if applicable to stack)
  - Test infrastructure setup
- Each phase must have clear completion criteria

### Task Quality

- Each task must be atomic and actionable (one clear deliverable)
- Task descriptions must be specific, not vague
- Use consistent task numbering (T001, T002... or decade-based per sprint)
- Mark parallel tasks with `[P]` only if they have NO dependencies on other sprint tasks
- Tasks must reference actual components/features from specs

### Dependencies

- Document ALL critical dependencies between sprints (from specs architecture)
- Document ALL blocking relationships between tasks
- Identify the critical path (longest dependency chain)
- Be realistic - don't create false dependencies, but don't miss real ones from specs

### Parallel Opportunities

- Only mark tasks as parallel `[P]` if truly independent
- Allocate subagents from `.claude/agents/` for parallel work
- Specify WHY tasks can run in parallel (different domains, no shared resources)
- Examples of good parallel opportunities:
  - Frontend + Backend (if separate codebases in specs)
  - Documentation + Implementation (different outputs)
  - Independent features (no shared state per specs)
  - Different platform targets (iOS + Android, etc.)

### Generic Compatibility

- DO NOT assume specific tech stack (Next.js, React, etc.) - read from specs
- Work for any project type:
  - Web apps (frontend, backend, fullstack)
  - Mobile apps (iOS, Android, cross-platform)
  - Desktop apps
  - Backend APIs
  - Data pipelines
  - ML/AI projects
  - CLI tools
  - Libraries/SDKs
- Adapt Phase 1 tasks to actual tech stack:
  - Web: Node.js setup, npm/yarn, webpack/vite
  - Python: venv setup, pip, requirements.txt
  - Mobile: Xcode/Android Studio, CocoaPods/Gradle
  - ML: Jupyter, conda, model environment
  - etc.

### Output Quality

- Save to `specs/tasks.md` (NOT `.claude/templates/tasks.md`)
- All template sections must be filled (no empty placeholders)
- Include concrete examples from specs in each section
- Task Status Legend must be present
- Related Documentation links must point to actual spec files

## 5. Success Criteria

- ✅ specs/prd.md and specs/tech-specs.md validated before proceeding
- ✅ File created at `specs/tasks.md` with complete content
- ✅ All 3 mandatory phases (Foundation, Build, Deployment) are defined
- ✅ Tech stack in Phase 1 matches specs/tech-specs.md exactly
- ✅ Features in Phase 2 match specs/prd.md functional requirements
- ✅ Each sprint has: Goal, Tasks, Acceptance Criteria, Verification
- ✅ Dependencies section documents sprint and task blocking relationships from specs
- ✅ Parallel Opportunities section identifies concurrent work with subagent allocations
- ✅ All parallel tasks marked with `[P]` notation
- ✅ Implementation Strategy is concrete and actionable
- ✅ Risks & Blockers section reflects challenges from PRD
- ✅ No overengineering - lean and focused task breakdown
- ✅ Conservative approach - only necessary complexity

## 6. Patterns

### Good Pattern: Spec Validation

```markdown
T001: Check if specs/prd.md exists
If NOT exist: Exit with error message

T002: Check if specs/tech-specs.md exists
If NOT exist: Exit with error message

✅ Both specs exist → Proceed with task generation
```

### Good Pattern: Tech Stack Extraction

```markdown
From specs/tech-specs.md:

# Python + FastAPI + PostgreSQL Project

### Phase 1: Foundation

#### SPRINT-001: Environment Setup

**Goal:** Python development environment configured
**Tasks:**

- T001 [P]: Set up Python 3.11 virtual environment
- T002 [P]: Install FastAPI and dependencies via requirements.txt
- T003: Configure PostgreSQL database
- T004: Set up pytest for testing
```

### Good Pattern: Feature-Based Sprints

```markdown
From specs/prd.md Functional Requirements:

### Phase 2: Build

#### SPRINT-003: User Authentication (FR-001, FR-002)

**Goal:** Users can sign up and log in
**Tasks:**

- T020: Implement JWT token generation
- T021: Create user registration endpoint
- T022: Create login endpoint
- T023: Add password hashing with bcrypt

#### SPRINT-004: Dashboard UI (FR-005, FR-006)

**Goal:** Users can view and manage their dashboard
**Tasks:**

- T030: Create dashboard layout component
- T031: Implement data fetching hooks
- T032: Add filtering and sorting
```

### Good Pattern: Clear Dependencies

```markdown
## Dependencies and Execution Order

**Sprint Dependencies:**

- SPRINT-002 (Define API contracts) must complete before SPRINT-003 (Auth API) because endpoint schemas required
- SPRINT-003 (Auth API) must complete before SPRINT-004 (Dashboard UI) because auth endpoints must exist

**Task Dependencies:**

- T015 (User model definition) blocks T020 (JWT token generation)
- T020 (JWT implementation) blocks T021 (Registration endpoint)

**Critical Path:**

- T001 → T015 → T020 → T021 → T031 (auth required for dashboard data fetch)
```

### Good Pattern: Subagent Allocation (Generic)

```markdown
**Subagent Allocation:**

- T020-T023: backend-engineer - API endpoints isolated from frontend
- T030-T032: frontend-engineer - UI components independent of API work
- T040-T045: test-engineer - Test suite creation in parallel with feature development
- T050: system-architect - Database schema design requires architectural decisions
```

### Bad Pattern: Assumptions Without Specs

```markdown
❌ Assuming Next.js when specs say Django
❌ Creating React component tasks when it's a CLI tool
❌ Adding mobile app tasks when specs only mention web
❌ Ignoring actual features from PRD and inventing new ones
```

### Bad Pattern: Overengineering

```markdown
❌ Creating 10 phases with 50 micro-tasks
❌ Tasks like "T001: Research best practices" (too vague)
❌ Unnecessary dependencies ("Frontend blocks backend" when they're independent per specs)
❌ Marking all tasks as parallel when clear dependencies exist in specs
```

## 7. References

- @.claude/templates/tasks.md (template to fill out)
- @specs/prd.md (REQUIRED - product requirements and features)
- @specs/tech-specs.md (REQUIRED - technical architecture and stack)
- `specs/ui-ux.md` (optional - UI requirements if exists)
- `.claude/agents/` (available subagents for delegation)
- @CLAUDE.md (project structure and workflow)
