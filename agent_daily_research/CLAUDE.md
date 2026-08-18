# CLAUDE.md

This repository is a personal AI research assistant template. Claude cloud
routines research the topics and questions defined here, write daily summaries
and fortnightly reviews into `KNOWLEDGE/`, and deliver every change as a
GitHub pull request.

Rules for any session working in this repo:

- **Contract files (human-owned inputs):** `TOPICS.md`, `QUESTIONS.md`,
  `config.yml`, and `examples/`. Treat them as inputs, not output.
- **`KNOWLEDGE/` is generated output.** Only the `knowledge-gathering`
  workflow (`skills/knowledge-gathering/CORE.md`) writes it.
- **Edit topics and questions only via the skills:** `update-topics` for
  `TOPICS.md`, `update-questions` for `QUESTIONS.md`, and `recycle` for any
  deletion (it moves files into the dated `.recyclebin/`, never hard-deletes).
- **Never fabricate research.** If live research or required reading fails,
  write the visible failure output the skills describe — no invented findings.
- **Delivery:** every change ends in a commit; in cloud sessions, push a
  `claude/`-prefixed branch and open a pull request. Never push to `main`.
