# Knowledge Gathering Core

These are the canonical shared instructions for the repository knowledge workflow.
Cloud routines and Claude Code sessions load this file from the repository root
and run one mode: `daily` or `fortnightly`. No runner supplies run context — the
run computes its own, as defined in `## Cloud Run Context` below.

## Required Reference Files

Read these detailed rules before producing or editing any knowledge output:

- `skills/knowledge-gathering/references/output-rules.md`
- `skills/knowledge-gathering/references/source-quality.md`
- `skills/knowledge-gathering/references/condensation-rules.md`

## Global Rules

- Run from the repository root.
- Use exact calendar dates in `YYYY-MM-DD` form for the run date, source dates,
  event dates, windows, and "as of" statements.
- Treat `TOPICS.md`, `QUESTIONS.md`, `config.yml`, and `examples/`
  as inputs, not generated output.
- Treat `KNOWLEDGE/` as the generated knowledge base.
- Include source links for factual claims, or mark the claim unresolved and explain
  what evidence is missing.
- Use confidence labels consistently: `high`, `medium`, `low`, or `unresolved`.
- State uncertainty explicitly for time-sensitive, contested, incomplete, or
  single-source claims.
- Prefer primary sources and reproducible artifacts. Do not inflate confidence
  because a claim is interesting or repeated without evidence.
- If live research is unavailable, fail visibly. Do not fabricate a newsletter,
  report, source list, or topic note from memory.
- Do not create topic notes unless the information is likely to matter beyond the
  day.
- Keep changes narrow: update only the dated output, new durable topic notes, and
  topic overviews affected by the run.

## Cloud Run Context

Each run happens in a fresh cloud sandbox with a clean clone of the repository.
Compute the run context yourself:

- **Run date:** today's date in the `timezone` set in `config.yml`.
- **Output paths:** `daily` mode writes `KNOWLEDGE/daily/YYYY/YYYY-MM-DD.md`;
  `fortnightly` mode writes
  `KNOWLEDGE/fortnightly/YYYY/YYYY-MM-DD_to_YYYY-MM-DD.md`; topic notes go under
  `KNOWLEDGE/topics/<topic-id>/notes/` and topic overviews at
  `KNOWLEDGE/topics/<topic-id>/OVERVIEW.md`.
- **Fortnightly cadence self-check:** the number of days between
  `fortnightly.anchor_date` and the run date must be an exact non-negative
  multiple of `fortnightly.interval_days`. Otherwise stop immediately and reply
  only "Off-cadence date — fortnightly review skipped." — no writes, no commits.
- **Lookback window:** the previous `fortnightly.lookback_days` days, ending at
  the run date.
- **Housekeeping:** after starting, run `python3 scripts/purge_recyclebin.py`.
  If it fails, warn and continue — a purge failure is never a run-killer.
- **Validation:** if `import yaml` fails, run
  `python3 -m pip install --quiet pyyaml`. Then both
  `python3 scripts/validate_inputs.py` and
  `python3 scripts/check_knowledge_links.py` must pass before finishing.
- **Delivery:** commit all changes. When running in a cloud session or routine,
  push the branch `claude/knowledge-<mode>-<run-date>` and open a pull request.
  End the final message with the output's `Overview` section — reproduced as
  written, keeping its bullets, blank lines, and dividers — and the pull
  request link.

## Live Research Failure

At the start of a run, confirm that live source research is available if the mode
requires fresh source checking. Daily mode always requires live research.

If live research is unavailable:

1. Stop evidence gathering immediately.
2. Write a visible failure output at the normal mode output path when possible.
3. Include an `Overview` section stating that the run failed because live
   research was unavailable.
4. Include the exact run date, mode, attempted scope, and what could not be
   accessed.
5. Do not include normal highlights, claims, source-confidence summaries, or topic
   notes unless they are explicitly marked as not generated due to failure.

## Mode: `daily`

Daily mode creates one dated daily summary and, only when warranted, topic notes
and updates to topic overviews.

Before researching, read all of the following:

- `TOPICS.md`
- `QUESTIONS.md`
- `config.yml`
- `examples/daily-summary.example.md`
- `examples/topic-note.example.md`
- `examples/topic-overview.example.md`
- `examples/fortnightly-report.example.md`
- the three reference files listed above

Then:

1. Determine the run date in the timezone configured by `config.yml`.
2. Parse active topics from `TOPICS.md`, including topic IDs, weekday weights,
   daily item limits, descriptions, and source preferences.
3. Parse active questions from `QUESTIONS.md`; only `status: active` questions
   should bias scoring.
4. Apply the weekday limits from `config.yml` for total items and topic
   notes.
5. Research each active topic and active question using live sources.
6. Prefer fresh, primary, source-backed updates that answer active questions or
   alter durable understanding of a topic.
7. Select only enough items to satisfy the configured limits and topic importance.
8. Write `KNOWLEDGE/daily/YYYY/YYYY-MM-DD.md`.
9. Create topic notes under `KNOWLEDGE/topics/<topic-id>/notes/` only for durable
   items.
10. Update only the affected `KNOWLEDGE/topics/<topic-id>/OVERVIEW.md` files.
11. Self-check the output against the examples and reference rules before
   finishing.

Daily output must make source quality visible. Every highlight and durable note
must include source links, confidence, exact dates where relevant, and explicit
uncertainty for contested or time-sensitive claims.

## Mode: `fortnightly`

Fortnightly mode synthesizes the configured lookback window and writes one review
report. It should not invent new facts to fill gaps. Before anything else, apply
the fortnightly cadence self-check from `## Cloud Run Context`; on an off-cadence
date stop as described there.

Before writing, read all of the following:

- `TOPICS.md`
- `QUESTIONS.md`
- `config.yml`
- `examples/fortnightly-report.example.md`
- `examples/daily-summary.example.md`
- `examples/topic-note.example.md`
- `examples/topic-overview.example.md`
- the three reference files listed above

Then:

1. Determine the run date in the configured timezone.
2. Read `fortnightly.lookback_days` from `config.yml`.
3. Define the reviewed window as the previous `lookback_days`, using exact start
   and end dates in the report title.
4. Scan `KNOWLEDGE/daily/` for daily summaries inside that window.
5. Scan every `KNOWLEDGE/topics/*/OVERVIEW.md`.
6. Scan recent topic notes under `KNOWLEDGE/topics/*/notes/` whose note date falls
   inside the reviewed window.
7. Identify what was gathered, repeated themes, conflicts or tensions, stale or
   answered questions, useful condensation opportunities, future focus, and source
   coverage gaps.
8. Write `KNOWLEDGE/fortnightly/YYYY/YYYY-MM-DD_to_YYYY-MM-DD.md`.
9. Self-check that the report names the scanned scope and uses exact dates,
   source links when citing specific claims, confidence labels, and explicit
   uncertainty.

If the scanned local knowledge base is sparse, say so plainly. If no conflicts are
found, say that no conflicts were found and name the exact scope scanned.

## Completion Checklist

Before declaring the run complete:

- The correct mode output exists at the expected path.
- Required sections match `skills/knowledge-gathering/references/output-rules.md`.
- Every factual claim has a source link or is marked unresolved.
- Confidence labels are present where claims are evaluated.
- Time-sensitive or contested claims include exact dates and uncertainty.
- Topic notes and overviews follow
  `skills/knowledge-gathering/references/condensation-rules.md`.
- Any live-research failure is visible and not disguised as a normal successful
  newsletter or report.
