# Design decisions & open follow-ups

Rationale, hard-won gotchas, and deferred feature ideas for the cloud
knowledge workflow (Claude cloud routines + a GitHub repository). **Read the
design decisions before changing the workflow.** User-facing setup lives in
[README.md](../README.md).

## Design decisions & gotchas

- **Fail visibly, never fabricate.** If the agent can't produce a verified
  output (live research unavailable, required reading or scanning fails), the
  run writes a visible failure output at the normal output path rather than a
  fake newsletter or report. Findings are never invented from memory.
- **Output sections are owned by `output-rules.md`.**
  `skills/knowledge-gathering/references/output-rules.md` is the single source
  of truth for the required sections of daily and fortnightly outputs —
  including the `Overview` section and the failure outputs. Prompts,
  examples, and validators must not define competing section lists. Its
  `## Readability` rules (bullets over prose, short paragraphs, blank lines,
  `---` dividers) apply to every generated section.
- **The `Overview` is structured, and nothing may flatten it.** It was once
  required to be exactly one paragraph, which produced unreadable walls of
  text in both the routine's final message and the email. It is now a short
  lead sentence plus bullets, so `scripts/extract_overview.py` returns the
  section **verbatim** — it still rejects a missing, duplicated, or empty
  `Overview`, but never reformats one. Anything consuming the Overview
  (`send_email.py`, the routine prompts) must preserve its line breaks.
- **Delivery is PR-based.** Cloud sessions can always push to branches
  prefixed `claude/`, but not to protected branches or branches with others'
  commits — so no design may depend on pushing `main`. Every run commits,
  pushes `claude/knowledge-<mode>-<run-date>`, and opens a pull request; the
  routine's final message ends with the output's `Overview` section and the
  PR link.
- **Auto-merge is doubly scoped.** The included workflow
  (`.github/workflows/auto-merge-knowledge.yml`) merges a PR only if the head
  branch starts with `claude/knowledge-` **and** every changed file is under
  `KNOWLEDGE/` or `.recyclebin/` — so a maintenance-session PR that edits
  `TOPICS.md`, `QUESTIONS.md`, or any script is never auto-merged. The
  workflow-level `permissions:` block grants the token merge rights regardless
  of the repository's default workflow permissions. If the user protects
  `main`, `gh pr merge` fails visibly and they merge by hand.
- **The fortnightly routine is scheduled weekly and self-skips.** Cron
  expressions can't say "every 14 days", and routine runs count against a
  daily quota — a daily schedule with self-skip would waste ~13 routine runs
  per fortnight, while a weekly schedule on the anchor weekday wastes one tiny
  run. Cadence is gated by `fortnightly.anchor_date` + `interval_days` in
  `config.yml`; on an off-cadence date the run stops immediately and
  replies only "Off-cadence date — fortnightly review skipped." — no writes,
  no commits.
- **`.recyclebin/` is tracked in git.** Cloud runs happen in a fresh
  clone-per-run sandbox, so anything recycled only in the working tree would
  silently vanish. A recycle sticks only once the move is committed and merged
  (in a cloud session: a `claude/` branch + PR, like any other change).
- **The recycle-bin purge is best-effort housekeeping.** Each knowledge run
  executes `python3 scripts/purge_recyclebin.py` early; a non-zero exit is a
  warning and the run **continues** — housekeeping must never kill the
  newsletter. Only immediate children of `.recyclebin/` whose names parse as
  `YYYY-MM-DD` (the deletion date) are ever purged; anything else is warned
  about and left alone. Stdlib only — Send2Trash was evaluated and rejected
  (OS-level trash, no retention control).
- **Email is sent by GitHub Actions, never by the agent.** Sending happens
  after a briefing pull request merges. The
  [email setup guide](email-setup.md) keeps the sender credentials in GitHub
  Secrets, so they never enter the routine sandbox: an agent that browses the
  live web must not hold send-capable credentials because prompt injection
  would widen the blast radius. Raw SMTP egress from the routine sandbox is
  unverified anyway; its documented network path is an HTTP(S)-proxy
  allowlist. Auto-merged pull requests send inline from
  `auto-merge-knowledge.yml` because `GITHUB_TOKEN`-driven events do not start
  workflow runs; manually merged pull requests use the separate
  `pull_request: closed` workflow. The two triggers are mutually exclusive, so
  nothing double-sends. Email is opt-in solely when the three secrets
  (`GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD`, and `KNOWLEDGE_EMAIL_TO`) exist;
  there is no config key. Alternatives were rejected for these reasons:
  - **B — Email MCP server in the sandbox:** OAuth is
    interactive-browser-first, headless use would inject credentials into
    every fresh sandbox, the web-browsing agent would gain send capability,
    and each run would need an `npx` install.
  - **C — Official Gmail connector:** it can create drafts but cannot send.
  - **D — Transactional email API:** it breaks the dummy-Gmail requirement,
    needs another third-party signup, and still puts secrets in the sandbox.
- **No run lock.** The old local design serialized runs with a file lock; the
  cloud design needs none. The two routines are scheduled at different times,
  each run works in its own fresh clone on its own `claude/` branch, and the
  PR flow makes a rare collision harmless (two pull requests instead of a
  corrupted working tree).
- **`check_knowledge_links.py`** validates daily links (external URL or existing
  topic note), fortnightly links (also allows existing daily summaries), topic
  overview sections, and — via `--topics-file` (CLI default `TOPICS.md`) — that
  every topic id has an `OVERVIEW.md`. Note the deliberate asymmetry: the
  `topics_file` **function** default is `None` (skip) so unit tests aren't
  coupled to the real tree, while the **CLI** default runs the check.

## Open follow-ups

- **Deterministic source adapters** (arXiv / GitHub releases / RSS) are
  intentionally deferred — add only if agent-led browsing proves unreliable or
  too costly, kept opt-in with offline fixtures.
- **Output validation is intentionally shallow** and could be extended (enforce
  required daily/fortnightly sections, `quality.max_overview_words`, and
  source-link/confidence-label presence) if generated output quality drifts.
