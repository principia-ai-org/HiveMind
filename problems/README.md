# Problems

Each file here is one research question collected from Principia. One problem per file.

## Index

| ID | Title | Tags | Status |
|----|-------|------|--------|
| [HM-001](HM-001-causal-world-models-and-robustness.md) | Do robustly-generalizing agents necessarily learn causal world models? | interpretability, generalization | open |

## How to add a problem

1. Copy [`TEMPLATE.md`](TEMPLATE.md) to `HM-NEXT-<short-slug>.md`, where `<short-slug>` is
   a few hyphenated words from the title. Leave the `HM-NEXT` prefix as-is: it becomes the
   next free permanent ID (`HM-007`, …) when your PR is processed, and the file is renamed
   to match. The ID stays stable even if the title changes later.
2. Fill in the title, `## Problem statement`, and `## Potential resources`. Leave the
   `added: YYYY-MM-DD` and `tags: <auto>` placeholders alone — the date is stamped and
   the tags are assigned automatically when your PR is processed (see [tags](#tags)).
3. Cite papers inline with bracketed numbers — `[1]`, or grouped `[2, 3]` — and under
   `## References` list each number with just a link: `[1] <url>` (arXiv / DOI / URL). You
   don't write authors, titles, or years: when your PR is processed the numbers are
   converted to author-year links `[[firstauthor2024]](../references/firstauthor2024.md)`,
   the list is rewritten, and the summaries are generated. See [reference keys](#reference-keys).
4. Open a pull request. **You do not need to write the paper summaries, pick the ID, or
   update this index** — when your PR touches a problem file, an automated job assigns the
   ID, stamps the date, assigns tags, generates the missing `references/*.md` summaries
   with Claude, updates the index tables, and commits it all onto your branch. See
   [`docs/problem-processing.md`](../docs/problem-processing.md).

## Reference keys

The author-year links the pipeline produces use a key that is `firstauthor` + `year`,
lowercase, no punctuation — e.g. Richens & Everitt 2024 → `richens2024`. If two papers
collide (same first author and year), it adds a short disambiguator: `richens2024b` or a
topic tag like `levine2025-mais`. Deterministic keys are what let the automation skip
papers that already have a summary. You don't pick keys yourself — you just give the
numbered links.

## Tags

Tags come from a fixed list in [`TAGS.md`](TAGS.md) so the vocabulary can't sprawl. Leave
`tags: <auto>` in your problem and the pipeline picks 1–3 tags from that list based on
your problem statement; or set them yourself, using only tags from the list. CI fails on
any tag not in `TAGS.md`. To introduce a genuinely new tag, add it to `TAGS.md` in the
same pull request.
