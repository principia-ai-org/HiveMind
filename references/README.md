# References

One file per paper cited by a problem. Each is a one-page summary formatted for quick
reading (by people and by LLMs): title, authors, link, and a faithful summary.

These summaries are **faithful compressions, checked against the source — not
endorsements or reviews.** Corrections are welcome via pull request.

## How these files get created

You normally don't write these by hand. When a pull request adds or changes a problem in
[`problems/`](../problems/), an automated job reads the citations, generates a summary for
any paper that doesn't already have one, and commits it here. See
[`docs/problem-processing.md`](../docs/problem-processing.md) for the exact procedure
and [`TEMPLATE.md`](TEMPLATE.md) for the format.

## Naming

Files are keyed `firstauthor` + `year`, lowercase — e.g. `richens2024.md`. Same-author,
same-year collisions get a suffix (`richens2024b.md`) or topic tag (`levine2025-mais.md`).

## Index

| Key | Title |
|-----|-------|
| [richens2024](richens2024.md) | Robust agents learn causal world models |
