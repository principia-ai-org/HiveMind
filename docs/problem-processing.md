# Problem processing procedure

This is the canonical procedure for processing a problem file after it is added or
changed: stamping its date, assigning its tags, converting its numbered citations into
author-year links, and generating summaries for the papers it cites. The CI workflow
([`.github/workflows/populate-references.yml`](../.github/workflows/populate-references.yml))
runs it; anyone can also follow it by hand. Keep this file as the single source of truth —
the workflow prompt should stay a thin pointer to it.

## Inputs

A list of changed problem files (paths under `problems/`). In CI these come from the diff
of the pull request.

## 1. ID and date (handled by CI, not by Claude)

Before Claude runs, a deterministic workflow step:

- renames any `problems/HM-NEXT-<slug>.md` to `problems/HM-<NNN>-<slug>.md` using the next
  free number, and replaces `HM-NEXT` with that ID inside the file; and
- replaces the literal `added: YYYY-MM-DD` placeholder with the current date.

No action needed here — treat the ID and date as fixed. Do not change an ID or a date
that is already filled in.

## 2. Tags

If a problem's `tags:` field is the `<auto>` placeholder, assign 1–3 tags **chosen only
from the allowed list in [`../problems/TAGS.md`](../problems/TAGS.md)**, based on the
problem statement, and replace `<auto>` with them (comma-separated). If the contributor
already set real tags, leave them; if any of their tags is not in `TAGS.md`, that is a
validation failure they must resolve — do not silently invent a new tag. Never add a tag
that is not in `TAGS.md`.

## 3. Citations and references

Problems are authored with **numbered** citations: inline markers like `[1]`, `[2, 3]`,
and a `## References` list of `[N] <url>` lines (URL only — no author/title/year). Convert
these into the repository's author-year form and generate the summaries.

1. **Parse the numbered list.** Read each `[N] <url>` entry under `## References` to build
   a map from citation number to URL.

2. **Compute the key** for each URL. The key is `firstauthor` + `year`, lowercase,
   punctuation stripped — e.g. Richens & Everitt 2024 → `richens2024`. For
   same-first-author + same-year collisions, append a short disambiguator: `richens2024b`,
   or a topic tag such as `levine2025-mais`. (Determining the author and year requires
   fetching the source — see step 4.)

3. **Deduplicate.** Skip any key that already has a `references/<key>.md` file. Only
   generate summaries for missing ones. This keeps the job idempotent.

4. **Fetch and summarize** each missing paper. Retrieve the real title, author list, and
   abstract from its URL (arXiv, DOI, or publisher/blog page). Write `references/<key>.md`
   following [`../references/TEMPLATE.md`](../references/TEMPLATE.md): `# <title>`, an
   `*Authors:*` line, a `*Link:*` line, and a `## Summary` section.

   The summary must be a **faithful compression checked against the source** — the
   problem, method, key result(s), and why it matters for the citing problem. It is a
   summary, not an endorsement or review. **Never fabricate.** If the source can't be
   retrieved, do not invent a summary: leave the reference file out and note the failure
   in the run output so a human can add it. (Fail visibly, never fabricate.)

5. **Rewrite the citations in place.** In the problem body, replace every inline numeric
   marker with the corresponding author-year link(s): `[1]` → `[[key]](../references/key.md)`,
   and a group `[2, 3]` → `[[key2]](../references/key2.md), [[key3]](../references/key3.md)`.
   Then rewrite the `## References` list from `[N] <url>` lines into keyed bullets, one per
   cited paper in ascending order:

   ```
   - [[key]](../references/key.md) — Author(s), *Title*, Venue Year. <url>
   ```

   No numbered markers or bare `[N] <url>` lines should remain. Do not otherwise alter the
   problem's prose.

## 4. Backlinks (handled by CI, not by Claude)

After citations are converted, a deterministic step runs `scripts/update_backlinks.py`,
which rewrites the `## Cited by` section of each `references/*.md` to list the problems
that cite it. No action needed here — do not hand-edit `## Cited by`.

## 5. Update indexes

Add each new reference to the table in
[`../references/README.md`](../references/README.md). If a new problem was added, add a row
for it (using its now-assigned ID) to [`../problems/README.md`](../problems/README.md).

## 6. Validate and loop

Run both validators from the repo root and fix issues until they pass:

```
python3 scripts/check_references.py
python3 scripts/check_problems.py
```

## Output

New/updated files staged for commit: the tag assignment and converted citations on the
problem, `references/<key>.md` for each previously-missing citation, and index updates. In
CI these are committed to the pull request branch so the author and reviewer see
everything in the same diff.
