# Output Rules

Use these rules with `skills/knowledge-gathering/CORE.md`. Match the examples in
`examples/` for tone and compactness.

## Readability

These apply to every section of every generated output. A briefing that is
correct but unreadable has failed.

- Prefer bullets to prose. Write a paragraph only when the ideas are connected
  by an argument; when they are merely a list, make them a list.
- One idea per bullet, at most two sentences. If a bullet needs a third
  sentence, split it.
- Never write a paragraph longer than about 80 words. When several ideas are
  present, break them into several paragraphs separated by a blank line.
- Open a bullet or paragraph with a **bold lead-in** naming its subject, so the
  text can be skimmed.
- Separate major groupings inside a long section with a `---` divider on its own
  line, with a blank line either side.
- Keep a blank line between blocks; never run a heading, a paragraph, and a
  bullet list together.
- Cut filler. "It is worth noting that" and "In this run, we observed" carry no
  information — state the fact instead.
- Prefer several short sentences to one sentence with three subordinate clauses.
  Long semicolon chains and stacked em-dashes are the usual symptom of a
  sentence that should have been a bullet list.

## Daily Summary

Path: `KNOWLEDGE/daily/YYYY/YYYY-MM-DD.md`

Required sections:

- `# Daily Knowledge Summary: YYYY-MM-DD`
- `## Overview`
- `## Highlights`
- `## By Topic`
- `## Topic Notes Created`
- `## Sources and Confidence`
- `## Run Notes`

Rules:

- `Overview` is the text that reaches the run's final message and the optional
  email, so it must be skimmable and under 150 words:
  - one short scene-setting sentence about the kind of day this was, then
  - at most six bullets, one idea each, at most two sentences each
  - a `---` divider between bullet groups only when the ideas fall into distinct
    groupings
  - no restatement of every topic and no duplication of the `Highlights`
    wording — detail belongs in `Highlights` and `By Topic`
- Each highlight should include a topic label, source link, and confidence label.
- Keep unresolved items out of `Highlights` unless the uncertainty itself is the
  important update.
- `By Topic` should summarize what changed, what did not change, and what to
  watch — as bullets with **bold lead-ins**, not as one paragraph per topic.
- `Topic Notes Created` should list local links or `None.`
- `Sources and Confidence` should summarize why each confidence level was used.
- `Run Notes` should mention live research status, skipped topics, source-access
  issues, and limit decisions.

## Topic Notes

Path: `KNOWLEDGE/topics/<topic-id>/notes/YYYY-MM-DD-<short-slug>.md`

Required sections:

- `# <Title>`
- `## Summary`
- `## Why It Matters`
- `## Evidence`
- `## Uncertainties`
- `## Related Questions`

Rules:

- Create a note only for information likely to remain useful after the day.
- Use concise prose; do not make a note for a link plus a couple of sentences.
- Evidence bullets must include source links and confidence labels.
- List active question IDs when the note bears on them.
- Use the note date as the date of capture, not necessarily the event date.

## Topic Overviews

Path: `KNOWLEDGE/topics/<topic-id>/OVERVIEW.md`

Required sections:

- `# <Topic Name>`
- `## Short Summary`
- `## Durable Takeaways`
- `## Open Questions`
- `## Notes Index`

Rules:

- Keep `Short Summary` under `quality.max_overview_words` from
  `config.yml`, and write it as a few short paragraphs or bullets rather than
  one block — it is read for orientation, not as a narrative.
- Add durable takeaways only when supported by source-backed notes or repeated
  daily evidence.
- Keep the notes index append-friendly and reverse chronological.
- Link to local topic notes with relative links from the overview file.

## Fortnightly Report

Path: `KNOWLEDGE/fortnightly/YYYY/YYYY-MM-DD_to_YYYY-MM-DD.md`

Required sections:

- `# Fortnightly Knowledge Review: YYYY-MM-DD to YYYY-MM-DD`
- `## Overview`
- `## What Was Gathered`
- `## Conflicts or Tensions`
- `## Stale or Answered Questions`
- `## Suggested Condensation`
- `## Suggested Future Focus`
- `## Source Coverage Gaps`

Rules:

- `Overview` is the text that reaches the run's final message and the optional
  email, so it must be skimmable and under 200 words:
  - one short sentence naming the window and the headline judgement, then
  - bullets grouped by theme, one idea each, at most two sentences each
  - a `---` divider between themes when there is more than one
  - no retelling of the daily summaries — the sections below carry the detail
- Name the exact window scanned.
- If no conflicts are found, say so and name the scope scanned.
- Every section below `Overview` is a bulleted list, not prose. A finding that
  needs more than two sentences gets a **bold lead-in** and its own bullet.
- Suggestions should be written for future agents as concrete maintenance actions.
- Do not add unsourced new claims while summarizing old outputs.

## Failure Output

When live research is unavailable, write a visible failure output instead of a
normal newsletter or report.

Required sections:

- normal title for the requested mode and output path
- `## Overview`
- `## Failure`
- `## Attempted Scope`
- `## Run Notes`

Rules:

- State the exact run date and mode.
- State that live research was unavailable.
- Do not include normal highlights, durable conclusions, or topic notes.
- Make the overview suitable as the run's final status message.
