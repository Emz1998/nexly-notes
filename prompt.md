Create a command that will fill out the @.claude/templates/tasks.md. Phase 1, 2, 3 are mandatory.

- You must assess what tasks, sprint's descriptions are appropriate and necessary to complete the overall goal. You can adjust the number of tasks and sprints as deemed necessary.

- You can also add more phases beyond the 3 mandatory phases only if absolutely necessary. You must act conservative as much as possible.

- Avoid overengineering. It's better to have less tasks but more precise and efficient than more tasks but complex and overbloated.

- You must also identify the dependencies and sequencing requirements between the tasks and sprints as well as any parallel opportunities.

- You must also identify which subagents are appropriate to delegate parallel independent/isolated tasks to.

- You must identify any parallel opportunities for any tasks and mark it with `[P]`

- Phase 1 should be about foundational stuff like setting up project environment, installing dependencies, establishing test environment, defining contracts and type.

- Your main goal should be to complete filling up the template in @.claude/templates/tasks.md.

- The generate tasks.md must be save in @specs/tasks.md

- The tasks command has to be dependent to @specs/prd.md and @specs/tech-specs.md . If these
  two specs are still not created, no specs/task.md should be created. The tasks documentation creation should be based on these two specs.

- The prd.md and tech-specs can be anything so you have to think overall in GENERAL not specific only to this
  project. In other words, This must accomodate other projects specs as well.
