# Source Quality Rules

Use these rules whenever a claim is selected, summarized, or promoted into a
durable note or overview.

## Source Preference

Prefer sources in this order:

1. Primary sources: official project posts, papers, preprints, release notes,
   repositories, datasets, policy documents, grants, and direct artifacts.
2. High-quality secondary sources: expert analysis that links to primary evidence
   and distinguishes fact from interpretation.
3. Commentary or social sources: useful for leads, not enough for high confidence
   unless they point to stronger evidence.

Avoid:

- unsourced reposts
- rumor threads
- vague summaries without links
- old pages presented as current
- claims that cannot be dated

Follow topic-specific source preferences in `TOPICS.md` when they are stricter.

## Dates

- Use exact dates in `YYYY-MM-DD` form for source publication, event timing,
  report windows, and "as of" statements.
- If a source lacks a visible publication date, say that the publication date was
  not found and lower confidence when timing matters.
- For "latest", "new", "current", or similar wording, verify against live sources
  and include the date of verification.
- Do not imply recency from search order or popularity.

## Confidence Labels

Use one of these labels for evaluated claims:

- `high`: supported by primary evidence or multiple credible sources, with no
  serious unresolved contradiction.
- `medium`: supported by one credible primary source or multiple decent secondary
  sources, but scope, replication, or interpretation remains uncertain.
- `low`: plausible but thinly sourced, preliminary, vendor-framed, or dependent on
  a single weak source.
- `unresolved`: not enough evidence to state as fact, or sources conflict in a way
  that cannot be resolved during the run.

Never use a confidence label to hide uncertainty. State the reason for the label.

## Contested or Time-Sensitive Claims

For contested, fast-moving, or high-stakes claims:

- Link the sources that disagree or describe the missing evidence.
- State what is known, what is disputed, and what remains unknown.
- Use exact dates for each source and for the run.
- Prefer `medium`, `low`, or `unresolved` unless the evidence is clearly strong.
- Do not smooth disagreement into a single confident narrative.

## Live Research Requirement

If live source research cannot be performed when fresh evidence is required:

- stop the normal run
- write the failure output described in `output-rules.md`
- do not backfill sources from memory
- do not fabricate a normal newsletter, topic note, or fortnightly report

Existing local Markdown can be quoted or summarized only as local prior knowledge,
not as proof that a current external claim is true.
