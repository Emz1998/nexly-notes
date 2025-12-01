Create a workflow validation hook

This must validate the following tasks:

- Check if the following phases have been completed:

  - Explore: Codebase exploration completed by codebase-explorer agent and created`codebase-status.md` file
  - Research: Research completed by research-specialist agent and created `research-report.md` file
  - Research Consult: Research consultation completed by research-consultant agent and created `research-consultation.md` file
  - Plan: Strategic plan created by strategic-planner agent and created `implementation-plan.md` file
  - Plan Consult: Plan consultation completed by strategic-planner agent and created `implementation-plan-consultation.md` file
  - Failing tests: Failing tests created by test-engineer agent by checking the .src/tests directory
  - Passing tests: Passing test by writing minimal code to make tests pass by `The main agent`
  - Refactoring: Refactoring code to improve code quality by `The main agent`
  - Code review: Code review completed by code-reviewer agent and created `quality-report.md` file
  - Tasks Checkoff: Check if all tasks have been completed by project-manager agent by checking the `specs/tasks.md` file and by checking the codebase.
