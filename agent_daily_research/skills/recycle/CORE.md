# Recycle Core

These are the canonical shared instructions for safely removing topics, questions,
and knowledge files from this repository. Deletions are never permanent: everything
is moved into a date-stamped `.recyclebin/` directory and purged only after a
retention period. The `update-topics` and `update-questions` skills defer to this
file as the single source of truth for all deletions.

## Inputs

The user names one or more things to recycle:

- **Topics** — by id (e.g. `formalisation`) or by title (the `## <title>` heading in
  `TOPICS.md`).
- **Questions** — by id (e.g. `Q-2026-07-08-001`) or by title.
- **Knowledge paths** — any file or directory under `KNOWLEDGE/`, given as a
  repo-relative path.

Resolve every named item to a concrete target before doing anything else. If a name
is ambiguous or does not match an existing item, stop and ask — do not guess.

## Confirmation Is Mandatory

Before touching any file:

1. List exactly what will be moved — every `TOPICS.md`/`QUESTIONS.md` section that
   will be cut and every file or directory that will be moved, with its source and
   destination path.
2. Get explicit user approval for that exact list.
3. Never recycle on inference. If the user did not name an item, it is not in scope.

## Mechanics

The deletion date is today in the timezone configured by `config.yml`
(`timezone`), formatted `YYYY-MM-DD`. All destinations live under
`.recyclebin/<date>/`. Create `.recyclebin/` and the dated subdirectory on demand.

- **Topic** (id `<topic-id>`, title `<title>`):
  - Cut the whole `## <title>` section from `TOPICS.md` (the heading through the last
    line before the next `##` heading or end of file) and write it to
    `.recyclebin/<date>/TOPICS/<topic-id>.md`.
  - Move the directory `KNOWLEDGE/topics/<topic-id>/` to
    `.recyclebin/<date>/KNOWLEDGE/topics/<topic-id>/`.
- **Question** (id `<question-id>`):
  - Cut the whole `## <question-id>: <title>` section from `QUESTIONS.md` and write
    it to `.recyclebin/<date>/QUESTIONS/<question-id>.md`.
- **Knowledge file or directory**:
  - Move it to `.recyclebin/<date>/<repo-relative-path>`, preserving its full
    repo-relative path (e.g. `KNOWLEDGE/daily/2026/2026-07-16.md` →
    `.recyclebin/<date>/KNOWLEDGE/daily/2026/2026-07-16.md`).
- **Name collision** inside today's bin: if a destination already exists, suffix the
  entry name with `-2`, then `-3`, and so on until it is unique.

Use moves (not copies followed by deletes) so every step is reversible.

## Cross-Reference Guard

Recycling a topic whose id appears in any active question's `topics:` list will
break validation. Before recycling a topic:

1. Scan `QUESTIONS.md` for questions whose `topics:` list contains the topic id.
2. If any are found, surface them to the user and make them choose:
   - edit those questions to drop the topic id (via `update-questions`), or
   - recycle those questions too (add them to this recycle batch).
3. Do not proceed until the conflict is resolved.

## Post-Check

After moving everything:

1. Run `python scripts/validate_inputs.py`.
2. Run `python scripts/check_knowledge_links.py`.
3. Report the output of both.

If either fails, restore the moved entries from `.recyclebin/<date>/` back to their
original locations (the moves are reversible) and report what failed. Do not leave
the repository in a broken state.

In a cloud session the sandbox is discarded after the run, so a recycle only sticks
once it is committed and merged. After the post-checks pass, commit the move — and,
in a cloud session, push a `claude/` branch and open a pull request like any other
change.

## Retention Notice

Tell the user:

- Recycled entries are kept for `recyclebin.retention_days` (currently 30) days,
  per `config.yml`.
- After that they are purged automatically by the next scheduled knowledge run.
- To restore an entry, move it back from `.recyclebin/<date>/` to its original
  location manually before the retention window expires.
