# /explore Command Template

## Command
`/explore <instructions>`

## Purpose
Explore the codebase and gather comprehensive context

## Output Structure

### Codebase Exploration Report
**Location**: `tmp/session_[session_id]/explore/codebase_exploration.md`

```markdown
# Codebase Exploration Report

## Project Overview
- **Name**: [Project name]
- **Type**: [Web app/API/Library]
- **Stack**: [Technologies used]
- **Size**: [LOC/Files count]

## Documentation Review
- **README**: [Key points]
- **Architecture Docs**: [Summary]
- **API Docs**: [Available endpoints]

## Directory Structure
```
project/
├── src/
│   ├── components/
│   ├── lib/
│   └── utils/
├── tests/
└── docs/
```

## Entry Points
- **Main**: [File path]
- **Initialization**: [How it starts]
- **Startup Sequence**: [Steps]

## Core Flows
### User Flow 1
- **Path**: [Step by step]
- **Components**: [Involved parts]

### Business Logic
- **Key Functions**: [List]
- **Data Processing**: [How]

## Dependencies
### External Libraries
- **Library 1**: [Purpose]
- **Library 2**: [Purpose]

### Internal Modules
- **Module 1**: [Purpose]
- **Module 2**: [Purpose]

## Data Flow
- **Input Sources**: [Where data comes from]
- **Processing**: [How it's handled]
- **Storage**: [Where it goes]
- **Output**: [Final form]

## Configuration
- **Environment Variables**: [List]
- **Build Settings**: [Important configs]
- **Constants**: [Key values]

## Testing
- **Test Framework**: [Which one]
- **Coverage**: [Percentage]
- **Test Types**: [Unit/Integration/E2E]

## Local Setup
- **Requirements**: [What's needed]
- **Steps**: [How to run]
- **Verification**: [How to check]

## Areas of Attention
- **Technical Debt**: [Issues found]
- **Improvement Areas**: [Suggestions]
- **Security Concerns**: [If any]

## Patterns Observed
- **Design Patterns**: [Which ones]
- **Code Style**: [Conventions]
- **Architecture**: [Type]
```

## Process Flow
1. Read documentation
2. Examine structure
3. Identify entry points
4. Trace core flows
5. Study dependencies
6. Analyze data flow
7. Review configurations
8. Inspect tests
9. Run locally
10. Document findings

## Used By
- `/analyze` command
- `/research-requirements` command
- `/strategize` command