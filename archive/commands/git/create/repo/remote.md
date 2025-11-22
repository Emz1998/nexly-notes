---
name: create remote repo
description: Create a new repository
allowed-tools: Bash(gh:*)
argument-hint: <repository-name>
---

!`gh auth login && gh repo create $ARGUMENTS --public --source=. --remote=origin`
