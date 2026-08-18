---
name: knowledge-gathering
description: Run the repository workflow for a daily newsletter, topic overview updates, a fortnightly report, and QUESTIONS.md-guided knowledge gathering.
---

# Knowledge Gathering

**Before anything else — cache human changes.** From the repository root, run `git status --porcelain`. If the working tree is clean, proceed. Otherwise run `git add -A && git commit -m "cache human changes before knowledge-gathering"`. If git cannot be run (git missing, not a git repository, or the command fails), HARD STOP: report the problem and do not run any part of this skill — a working git is a requirement (see `## For developers` in README.md).

Load and follow `skills/knowledge-gathering/CORE.md` from the repository root.

Use the requested mode, usually `daily` or `fortnightly`, and keep the shared core
as the single source of truth.

**Final step — commit the result.** After all other steps have completed, run `git add -A && git commit -m "Performed knowledge-gathering"` from the repository root. If there is nothing to commit, skip the commit and note it. When running in a cloud session or routine, then push the branch `claude/knowledge-<mode>-<run-date>` and open a pull request, and end the final message with the output's `Overview` section and the pull request link, per the Delivery bullet in the core file's `## Cloud Run Context`.
