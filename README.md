# Hive Mind - Collective Research Questions

Collective gatherings of research questions from Principia. Structure benchmarked against
[MAIS](https://github.com/lionellevine/MAIS).

## Layout

- **[`problems/`](problems/)** — one `.md` per research question: title, problem
  statement, potential resources, and cited references.
- **[`references/`](references/)** — one `.md` per cited paper: title, authors, link, and
  a faithful summary. **These are generated automatically** (see below).

## How the automatic references work

You write a problem file and cite papers by link; you do **not** write the paper
summaries, and you can leave the date and tags as placeholders. When your pull request
adds or changes a file in `problems/`, a GitHub Action stamps the date, assigns tags from
the allowed list, generates a `references/<key>.md` summary for any paper that doesn't
have one yet, and commits everything onto your PR branch — so the problem and its
references land in the same reviewable diff.

- Add a problem: see [`problems/README.md`](problems/README.md).
- The exact procedure the bot follows: [`docs/problem-processing.md`](docs/problem-processing.md).
- Tags come from a fixed list, [`problems/TAGS.md`](problems/TAGS.md); the bot auto-assigns
  them from that list when a problem is submitted with the `<auto>` placeholder. Make PR if you'd like to change the list of the tags.
- Local checks: `python3 scripts/check_references.py` and `python3 scripts/check_problems.py`
  validate that every cited reference exists and is well-formed and that problem IDs are
  unique and all tags are in the allowed list.

## Zotero integration

Every reference in [`references/`](references/) is mirrored into a **Zotero group
library**, under a collection named **`HiveMind`**, so the reading list is available in a
real reference manager. The sync is **one-way** (repo → Zotero).

- **When it runs:** automatically when a change to `references/**.md` lands on `main`, and
  on demand from **Actions → *Sync references to Zotero* → Run workflow**
  (`mode: sync` to upsert, `mode: audit` to just list what's in the group).
- **What each item gets:** title, authors, year, link, item type inferred from the link
  (arXiv → *preprint*, DOI → *journal article*, otherwise *webpage*), the HiveMind summary
  in the `Extra` field, and the tags `HiveMind` and `hm-ref:<key>`.
- **No duplicates:** items are matched by the `hm-ref:<key>` tag, so re-running updates the
  same item; a run also removes any stray duplicate of a reference.
- **Caveat:** because it's one-way, edits made *inside* Zotero to a synced item may be
  overwritten on the next sync.

Script: [`scripts/sync_zotero.py`](scripts/sync_zotero.py) · workflow:
[`.github/workflows/sync-zotero.yml`](.github/workflows/sync-zotero.yml).
