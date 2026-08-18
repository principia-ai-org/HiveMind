# Update Topics Core

These are the canonical shared instructions for changing `TOPICS.md`. Use this
skill to add, edit, reweight, or remove topics from a free-text request. Never
edit a file before the user has confirmed the complete resulting configuration,
and route every deletion through the recycle protocol.

## Read First

Before proposing any change, read:

- `TOPICS.md` — the current topics and their exact format.
- `QUESTIONS.md` — needed for the cross-reference guard when removing a topic.
- `config.yml` — for the `timezone` (used to resolve "today") and
  `quality.max_overview_words` (the `Short Summary` limit in a topic overview).
- The format rules enforced by `scripts/validate_inputs.py`, restated concretely
  below. These are the rules your edit must satisfy.

## Format Rules (Enforced by `scripts/validate_inputs.py`)

Each topic is a `## <Topic Title>` section in `TOPICS.md` containing **exactly one**
` ```yaml ` code block followed by a **non-empty** plain-language description
(the text outside the yaml block must not be empty). The yaml block is a mapping
with these fields:

- `id` — required. A string in lowercase kebab-case matching
  `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`: it must start with a lowercase letter,
  contain only lowercase letters, digits, and single hyphens, with no leading,
  trailing, or consecutive hyphens and no uppercase. Must be **unique** across
  all topics.
- `default_weight` — required. Integer from **0 to 10** inclusive (not a boolean).
- `weekday_weights` — required. A mapping with **all seven** day keys
  (`monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, `sunday`);
  each value is an integer from **0 to 10**. Missing or unknown day keys fail
  validation.
- `daily_min_items` — optional. Integer from **0 to 100**.
- `daily_max_items` — optional. Integer from **0 to 100**. If both are present,
  `daily_min_items` must be **≤** `daily_max_items`.
- `source_preferences` — optional. A mapping; its `primary` and `avoid` keys, when
  present, must each be a **list of strings**.

Note: only `id`, `default_weight`, and `weekday_weights` are strictly required by
the validator, but every existing topic also sets `daily_min_items`,
`daily_max_items`, and `source_preferences`. Match that convention unless the user
asks otherwise.

Every topic id in `TOPICS.md` must also have a
`KNOWLEDGE/topics/<id>/OVERVIEW.md` file, or `scripts/check_knowledge_links.py`
fails. This is why adding a topic must also create that overview (see below).

## Parse The Request

Read the user's free-text request and classify it into one or more operations:

- **add** — a new topic that does not yet exist.
- **edit** — change a field (description, item limits, source preferences, id) on
  an existing topic.
- **reweight** — change `default_weight` and/or `weekday_weights` on an existing
  topic. This is just an edit of the weight fields; treat it the same way.
- **remove** — delete an existing topic entirely.

If the request is ambiguous (for example a topic name that matches no existing
title/id, or that could mean either edit or add), stop and ask before proceeding.

## Infer And Confirm

For any field the user did **not** specify:

1. Infer a sensible value from the existing topics and the request. For a new
   topic, base weights and limits on the closest existing topic and the stated
   importance; derive `id` from the title in kebab-case (unique). For an edit,
   keep the current value unchanged unless the request implies otherwise.
2. Present the **complete** resulting configuration — every field, including
   inherited or unchanged ones — as a single yaml block (plus the description
   text), exactly as it will appear in `TOPICS.md`. For an edit, show the full
   resulting section, not just the changed lines.
3. **Wait for explicit user confirmation** of that block before editing any file.
   Do not write anything on inference alone.

## Adding A Topic

After the user confirms the full configuration:

1. Append (or insert in a sensible position) the new `## <Topic Title>` section to
   `TOPICS.md`: the confirmed yaml block followed by the confirmed non-empty
   description.
2. Create the topic-overview skeleton at `KNOWLEDGE/topics/<id>/OVERVIEW.md` with
   the required sections from
   `skills/knowledge-gathering/references/output-rules.md`:

   ```markdown
   # <Topic Name>

   ## Short Summary

   ## Durable Takeaways

   ## Open Questions

   ## Notes Index
   ```

   `check_knowledge_links.py` strictly requires the `Short Summary` and
   `Notes Index` sections; include all five to match the overview format. Keep
   `Short Summary` under `quality.max_overview_words` from `config.yml`
   as content is added later. Since this creates a file under `KNOWLEDGE/`, run
   `check_knowledge_links.py` in the post-check.

## Editing And Reweighting

After the user confirms the full resulting section:

- Apply the change in place in `TOPICS.md`, preserving the rest of the section.
- Changing a topic's `id` also requires renaming
  `KNOWLEDGE/topics/<old-id>/` to `KNOWLEDGE/topics/<new-id>/` (the overview must
  match the id) and updating that id anywhere it appears in a question's `topics:`
  list in `QUESTIONS.md`. Treat an id change like a removal for the
  cross-reference guard below, and run `check_knowledge_links.py` in the
  post-check because `KNOWLEDGE/` changed.
- Reweighting only touches `default_weight` / `weekday_weights`; still show and
  confirm the full section.

## Removing A Topic

Never delete without explicit permission naming the topic. All deletions go
through the recycle protocol: **follow `skills/recycle/CORE.md`** (the single
source of truth for deletion mechanics, the deletion-date `.recyclebin/` layout,
name-collision handling, restore, and retention). Do not duplicate that mechanics
here.

The recycle protocol includes the cross-reference guard: recycling a topic whose
id appears in any active question's `topics:` list breaks validation, so those
questions must be edited (via `update-questions`) or recycled too before
proceeding.

## Post-Check

After editing:

1. Run `python scripts/validate_inputs.py`.
2. Run `python scripts/check_knowledge_links.py` **when `KNOWLEDGE/` changed**
   (adding a topic, changing an id, or any removal, which the recycle protocol
   handles).
3. Show the user the result. If validation fails, fix the edit (or, for a recycle,
   restore from the bin per `skills/recycle/CORE.md`) and re-run until it passes.
   Do not leave the repository in a broken state.
