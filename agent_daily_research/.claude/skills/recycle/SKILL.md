---
name: recycle
description: Safely move topics, questions, or KNOWLEDGE/ files into the dated .recyclebin/ with mandatory confirmation, validation, and 30-day retention.
---

# Recycle

**Before anything else — cache human changes.** From the repository root, run `git status --porcelain`. If the working tree is clean, proceed. Otherwise run `git add -A && git commit -m "cache human changes before recycle"`. If git cannot be run (git missing, not a git repository, or the command fails), HARD STOP: report the problem and do not run any part of this skill — a working git is a requirement (see `## For developers` in README.md).

Load and follow `skills/recycle/CORE.md` from the repository root.

Use it for every deletion of a topic, question, or knowledge file, and keep the
shared core as the single source of truth.

**Final step — commit the result.** After all other steps have completed, run `git add -A && git commit -m "Performed recycle"` from the repository root. If there is nothing to commit, skip the commit and note it.
