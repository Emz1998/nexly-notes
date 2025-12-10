---
name: write-code
description: Write minimal code to pass existing failing tests (TDD Green Phase)
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, TodoWrite
model: sonnet
---

**Goal**: Write the minimal implementation code needed to make failing tests pass (TDD Green Phase)
**User Instructions**: $ARGUMENTS (optional)

## Tasks

1. Locate the specific tests files in `@src/tests/`
2. Run the test suite to identify failing tests
3. Analyze each failing test to understand what implementation is expected
4. For each failing test, identify the target implementation file
5. Write the minimal code required to make the test pass
6. Run tests after each implementation to verify the test passes
7. Repeat until all failing tests pass
8. Run the full test suite to confirm no regressions
9. Report the results (tests passed/failed, files created/modified)

## Implementation Strategy

- Focus on one failing test at a time
- Write the absolute minimum code to make each test pass
- Avoid adding functionality beyond what tests require
- Match the expected interface/signature from the test
- Follow existing project patterns and conventions
- Do not refactor or optimize - just make tests pass

## Prohibited Tasks

- DO NOT write new tests (this command is for implementation only)
- DO NOT add features not covered by tests
- DO NOT refactor existing code unless required to pass a test
- DO NOT add error handling beyond what tests validate
- DO NOT add documentation or comments unless required by tests
- DO NOT over-engineer - minimal viable implementation only

## Skills to Use

- Use `next-js` skills PROACTIVELY if dealing with Next.js framework
- Use `tailwind` skills PROACTIVELY if dealing with Tailwind CSS
- Use `PWA` skills PROACTIVELY if dealing with PWA
- Use `Zod` skills PROACTIVELY if dealing with Zod schemas
- Use `Supabase` skills PROACTIVELY if dealing with Supabase
