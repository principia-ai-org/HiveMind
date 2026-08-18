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
  them from that list when a problem is submitted with the `<auto>` placeholder.
- Local checks: `python3 scripts/check_references.py` and `python3 scripts/check_problems.py`
  validate that every cited reference exists and is well-formed and that problem IDs are
  unique and all tags are in the allowed list.

## Setup (one-time, maintainer)

The Action authenticates with the Principia Claude Team plan — no per-token API billing.
On a Team-plan account, run `claude setup-token`, then add the printed token as a
repository secret named `CLAUDE_CODE_OAUTH_TOKEN`
(`Settings → Secrets and variables → Actions`). That account acts as the bot identity;
rotate the token (valid ~1 year) if that person leaves. Contributors need no Claude
access of their own.

Note: the pipeline runs on same-repo branch PRs only (fork PRs can't read the secret).
