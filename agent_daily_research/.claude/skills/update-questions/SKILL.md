---
name: update-questions
description: Add, edit, reprioritize, archive, or remove questions in QUESTIONS.md with infer-and-confirm, full-config confirmation, validation, and recycle-based deletion.
---

# Update Questions

**Before anything else — cache human changes.** From the repository root, run `git status --porcelain`. If the working tree is clean, proceed. Otherwise run `git add -A && git commit -m "cache human changes before update-questions"`. If git cannot be run (git missing, not a git repository, or the command fails), HARD STOP: report the problem and do not run any part of this skill — a working git is a requirement (see `## For developers` in README.md).

Load and follow `skills/update-questions/CORE.md` from the repository root.

Use it for every change to QUESTIONS.md; confirm the complete resulting
configuration before editing and route every deletion through the recycle protocol.

**Final step — commit the result.** After all other steps have completed, run `git add -A && git commit -m "Performed update-questions"` from the repository root. If there is nothing to commit, skip the commit and note it.
