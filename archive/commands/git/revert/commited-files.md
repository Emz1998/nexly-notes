---
name: revert commited files
description: Revert specific commited files
allowed-tools: Bash(git restore:*)
argument-hint: <file-path>
---

!`git restore --source=HEAD~1 $ARGUMENTS`
