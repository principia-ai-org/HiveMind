# Update Questions Core

These are the canonical shared instructions for changing `QUESTIONS.md`. Use this
skill to add, edit, reprioritize, archive, or remove questions from a free-text
request. Never edit a file before the user has confirmed the complete resulting
configuration, and route every physical deletion through the recycle protocol.

## Read First

Before proposing any change, read:

- `QUESTIONS.md` — the current questions and their exact format.
- `TOPICS.md` — the set of **existing topic ids** a question may reference.
- `config.yml` — for the `timezone` (used to resolve "today" for the
  `created` date and new question ids).
- The format rules enforced by `scripts/validate_inputs.py`, restated concretely
  below. These are the rules your edit must satisfy.

## Format Rules (Enforced by `scripts/validate_inputs.py`)

Each question is a `## Q-YYYY-MM-DD-NNN: <title>` section in `QUESTIONS.md`
containing **exactly one** ` ```yaml ` code block followed by a details paragraph.

- **Heading** — must be `## <id>: <title>` with a literal colon-space (`: `)
  separator. The id must match `^Q-\d{4}-\d{2}-\d{2}-\d{3}$`: `Q-`, a four-digit
  year, two-digit month, two-digit day, and a three-digit sequence, e.g.
  `Q-2026-07-16-001`. Ids must be **unique** across all questions.
- `status` — a string. Allowed values: **`active`, `inactive`, `paused`,
  `answered`, `archived`**. Any other value fails validation.
- `priority` — integer from **1 to 10** inclusive (not a boolean).
- `topics` — a **non-empty** list of strings, each an **existing** topic id from
  `TOPICS.md`, with **no duplicates**.
- `created` — an ISO date in `YYYY-MM-DD` form (a plain `2026-07-16` is fine; a
  date-time is not).
- **title** (after the `: ` in the heading) and the **details** paragraph must
  both be non-empty.

Note: `priority`, `topics`, `created`, title, and details are strictly validated
only when `status: active`. For other statuses the validator checks just the id
format and the status value, but keep the full set of fields present and correct
so a question can be reactivated without further edits. Match the existing
convention: every field above on every question.

## Parse The Request

Read the user's free-text request and classify it into one or more operations:

- **add** — a new question.
- **edit** — change a field (title, details, `topics`, `created`) on an existing
  question.
- **reprioritize** — change `priority` and/or `status` on an existing question.
  This is an edit; treat it the same way.
- **archive** — set `status: answered` or `status: archived` (a non-destructive
  edit that stops the question from affecting scoring).
- **remove** — physically delete a question from the file.

If the request is ambiguous (a question that matches no existing id/title, or an
unclear intent), stop and ask before proceeding.

## Infer And Confirm

For any field the user did **not** specify:

1. Infer a sensible value from the existing questions and the request. For a new
   question, default `status` to `active`, set `created` to today in the
   `config.yml` timezone, infer `priority` from the stated importance
   relative to existing questions, and pick `topics` from the existing topic ids
   the question relates to. For an edit, keep the current value unless the request
   implies otherwise.
2. Present the **complete** resulting configuration — the full heading plus every
   yaml field (including inherited or unchanged ones) and the details paragraph —
   exactly as it will appear in `QUESTIONS.md`. For an edit, show the full
   resulting section, not just the changed lines.
3. **Wait for explicit user confirmation** of that block before editing any file.
   Do not write anything on inference alone.

## Adding A Question

New ids use today's date (in the `config.yml` timezone) plus the next
free `NNN`:

1. Determine today's date as `YYYY-MM-DD`.
2. Scan `QUESTIONS.md` for existing ids with that date prefix (`Q-YYYY-MM-DD-`).
   Take the highest `NNN` among them and add 1; if there are none, start at `001`.
   Zero-pad to three digits (`001`, `002`, …). Confirm the resulting full id is
   unique across the file.
3. After the user confirms the full configuration, append the new
   `## Q-YYYY-MM-DD-NNN: <title>` section: the confirmed yaml block followed by the
   confirmed non-empty details paragraph.

## Editing, Reprioritizing, And Archiving

After the user confirms the full resulting section:

- Apply the change in place in `QUESTIONS.md`, preserving the rest of the section.
- Do **not** change a question's id when editing; the id is stable. (Renumbering a
  question means recycling the old one and adding a new one.)
- Archiving is just setting `status` to `answered` or `archived` — a normal edit,
  still shown and confirmed as a full block.

## Removing A Question

"Remove" often means "stop this from affecting scoring." Offer the
**non-destructive** option first: set `status: answered` or `status: archived`
(an edit) instead of deleting, so the question is retained.

For a **physical** removal, never delete without explicit permission naming the
question. All physical deletions go through the recycle protocol: **follow
`skills/recycle/CORE.md`** (the single source of truth for deletion mechanics, the
deletion-date `.recyclebin/` layout, name-collision handling, restore, and
retention). Do not duplicate that mechanics here.

## Post-Check

After editing:

1. Run `python scripts/validate_inputs.py`.
2. `scripts/check_knowledge_links.py` is not needed for question edits (they do
   not touch `KNOWLEDGE/`); a physical removal via the recycle protocol runs its
   own post-check.
3. Show the user the result. If validation fails, fix the edit (or, for a recycle,
   restore from the bin per `skills/recycle/CORE.md`) and re-run until it passes.
   Do not leave the repository in a broken state.
