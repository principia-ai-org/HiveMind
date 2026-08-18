# Daily Research Agent (integrated w/ Claude Routines and GitHub)

## What this is

Every morning, Claude researches the topics you care about and files a short
daily briefing into your own copy of this repository on GitHub. Every two
weeks, it writes a longer review of what changed. You read the results in the
Claude app (including on your phone) or on GitHub.

There are no servers to run and no code to install. You set it up once by
clicking through a few screens; after that, everything happens automatically in
the cloud. The engine is a pair of **routines** — scheduled tasks that run
Claude Code in the cloud on your copy of this repository. This page walks you
through the whole setup.

Setting up takes about 15 minutes and never asks you to type a command or
write code. Four steps:

1. **Make your own copy** of this repository on GitHub (two clicks).
2. **Connect Claude to GitHub** (a guided sign-in).
3. **Create the two routines** in the Claude app (copy-paste two prompts).
4. Done — briefings arrive on their own and merge themselves. Later, you can
   optionally add [email delivery](/docs/email-setup.md).

**Want to build your own automation similar to this?** The GitHub repo is just a cloud folder, supplied to your Claude routines, where you can store and categorize skills, persistent memory markdown files, python scripts to be used as tools and so on. You can create your own GitHub repo and follow a very similar workflow below to integrate it to a Claude **cloud** routine -- which runs on the cloud and does not rely on your local machine. 

**Budgeting:** As of 11 Aug 2026, Claude cloud routines are included within standard paid Claude subscriptions and do not incur additional costs. 


## What you need

- A **Claude** account on the **Pro, Max, Team, or Enterprise** plan — sign in
  or upgrade at [claude.ai](https://claude.ai). (Free Claude accounts cannot
  run scheduled routines.) A **personal Pro or Max** account is the smoothest
  path: on a Team or Enterprise seat, an organization owner has to link GitHub
  for everyone before you can finish Step 2.
- A **GitHub** account (free is fine) — GitHub is where your copy of this
  repository, and every briefing, lives. No account yet? Creating one at
  [github.com/signup](https://github.com/signup) takes about two minutes.
- The **Claude desktop app** — download it at
  [claude.ai/download](https://claude.ai/download) — or claude.ai in a web
  browser.
- *(Optional, for later)* a throwaway Gmail address if you want briefings
  emailed to you. You create it during the
  [email setup](/docs/email-setup.md), not now — skip it entirely if you don't
  want email.

## Step 1 — Make your own copy of this repository

1. Open this repository's page on GitHub.
2. Press **Use this template → Create a new repository**.

   ![The "Use this template" button on the GitHub repository page](/docs/images/01-use-this-template.png)

3. Give your copy any name you like, and set it to **Private**.

   ![Create the private repository](/docs/images/02-repo-creation.png)

Repositories created this way have GitHub Actions switched on already, so the
automatic merging in Step 4 works without any further setup.

## Step 2 — Connect Claude to GitHub + set up your Claude cloud environment

This links your Claude account to your GitHub account so routines can read and
update your copy of the repository. You do it once, and it then applies
everywhere you use Claude — desktop, browser, and phone.

1. Open the Claude desktop app and go to the **Code** tab.

   ![The Code tab in the Claude desktop app](/docs/images/03-code-tab.png)

2. If the connection has not been set up, Claude typically raises the GitHub prompt **by itself**: It appears the first time Claude needs GitHub, e.g. when you open the Code tab. If not, you can also install Claude app to your repo directly by visiting [this link](https://github.com/apps/claude).
   - Your web browser opens `github.com`. Sign in if asked. **GitHub may ask for
   your two-factor (2FA) code — this is normal.**
   - Choose your personal account and install Claude app to the repo you set up.
   
   ![Install the Claude app in GitHub](/docs/images/04-github-claude-app.png)

   ![Install the Claude app to the desired GitHub repository](/docs/images/05-github-claude-app-setup.png)


3. If the connection is already set up, you can either select an existing cloud environment (e.g. `Default`) or create a new one. **We recommend creating a new cloud environment** so that you can have a more permissive `Network access` policy (the default `Trusted` blocks e.g. `arxiv.org`, `export.arxiv.org`, `huggingface.co` and `lean-lang.org`):
   
   ![Menu for selecting a cloud environment](/docs/images/06-cloud-env-select.png)

   Note that you can adjust the `Allowed domains` later --- for example, if you notice that certain trusted domains keep getting blocked when you inspect the routine runs. See [here](/docs/allowed-domains-draft.md) for a list of draft allowed domains.
   
   Note also that `Full access` can pose severe security risks: You are exposing a Claude session that has read access to your code and data to prompt injection and data exfiltration risks from untrusted websites.

   ![New cloud environment setup](/docs/images/07-new-cloud-env.png)
   
   Verify that GitHub is successfully integrated by checking that you can select your desired GitHub repository:

   ![Menu for selecting a GitHub repo](/docs/images/08-gh-repo-select.png)


A few things worth knowing:

- Finishing this step also creates a cloud environment named **Default** —
  that is the "Environment" you pick in Step 3, so you don't have to make one.
- The repository list you choose while authorizing decides where the Claude
  GitHub App is *installed*; it is not a lock on what Claude can see. Claude
  cloud sessions can reach any repository your GitHub account can. If that
  matters to you, limit the GitHub account itself rather than the app.
- The authorization can expire after a while. If Claude later says it can't
  reach GitHub, just redo this step.
- If your repository lives in a company **organization**, GitHub may require an
  organization admin to approve the app first.

## Step 3 — Create the two routines

In the Code tab, open **Routines**, press **New routine**, and choose
**Cloud**. (In a browser, go to claude.ai/code/routines.) 

![Select new cloud routine](/docs/images/09-new-cloud-routine.png)

You will create two
routines, one at a time, with the settings below.

### Routine 1 — Daily knowledge update

| Setting | What to pick |
|---|---|
| Repository | Your copy of this repository |
| Environment | The new environment you created with a custom network access policy |
| Trigger | **Schedule → Daily**, a morning time (e.g. 07:00), and **your timezone** |
| Prompt | The text in the box below — copy and paste it exactly |

```
Run the daily knowledge-gathering workflow for this repository.

1. Read skills/knowledge-gathering/CORE.md and follow its `daily` mode exactly, including every file it tells you to read first and its Cloud Run Context section.
2. The run date is today's date in the timezone set in config.yml.
3. Research the active topics and questions with live web research, then write the daily summary to KNOWLEDGE/daily/<year>/<run-date>.md, plus durable topic notes and topic overview updates only when the skill's rules call for them.
4. Run the validators described in the skill and fix anything they report before finishing.
5. Commit every change, push the branch claude/knowledge-daily-<run-date>, and open a pull request titled "Daily knowledge update: <run-date>".
6. End your final message with the daily summary's Overview section, reproduced as written with its bullets and line breaks intact, then the pull request link.

If live web research is unavailable, write the failure output the skill describes instead — never invent findings.
```

  ![Routine 1 with daily cadence, time, and timezone pickers](/docs/images/10-routine-1-form.png)

### Routine 2 — Fortnightly knowledge review

| Setting | What to pick |
|---|---|
| Repository | Your copy of this repository (same as above) |
| Environment | The new environment you created with a custom network access policy |
| Trigger | **Schedule → Weekly on Monday**, a morning time, and **your timezone** |
| Prompt | The text in the box below — copy and paste it exactly |

```
Run the fortnightly knowledge-review workflow for this repository.

1. The run date is today's date in the timezone set in config.yml.
2. Cadence check: read fortnightly.anchor_date and fortnightly.interval_days from config.yml. If the number of days from anchor_date to the run date is not an exact multiple of interval_days, stop now and reply only: "Off-cadence date — fortnightly review skipped." Do not write, commit, or push anything.
3. Otherwise read skills/knowledge-gathering/CORE.md and follow its `fortnightly` mode exactly, including every file it tells you to read first and its Cloud Run Context section. Write the report to KNOWLEDGE/fortnightly/<year>/<start>_to_<end>.md.
4. Run the validators described in the skill and fix anything they report before finishing.
5. Commit every change, push the branch claude/knowledge-fortnightly-<run-date>, and open a pull request titled "Fortnightly knowledge review: <start> to <end>".
6. End your final message with the report's Overview section, reproduced as written with its bullets and line breaks intact, then the pull request link.

If required reading or scanning fails, write the failure output the skill describes instead — never invent findings.
```

This routine runs weekly but only writes a report every second week — on off
weeks it simply replies **"Off-cadence date — fortnightly review skipped."**,
which is normal, not an error.

  ![Routine 2 with daily cadence, time, and timezone pickers](/docs/images/11-routine-2-form.png)

### Before you save each routine

- **Connectors:** the form lists connectors (other tools the routine is allowed
  to use). Review the list and remove any you don't want the routine to touch.
  - Alternatively, if you want to make your own customization, e.g. integration with Notion and Slack, you can add additional connectors here. **SECURITY RISK:** There's *technically* nothing preventing Claude from reading some malicious text on the internet (via arxiv, GitHub...) that contains prompt injection. Access to Notion and Slack means Claude *technically* can leak company information to the internet.
  - **Possible Claude bug (11 Aug 2026):** Even if you created the routine with no connectors, Claude somehow adds back two connectors. Manually edit the routines and remove them.
- **Try it now:** you don't have to wait for tomorrow morning — use **Run now**
  (a one-off run) on the daily routine to trigger a first test immediately.

When both routines are saved, your Routines list should look like this:

![The Routines list showing both routines enabled](/docs/images/12-routine-list.png)

You can adjust the model choice if necessary, or click `Run now` to test the routines.

## Step 4 — Updates merge themselves

Each run delivers its work as a **pull request** ("PR") — GitHub's way of
proposing a change so it can be reviewed before it becomes part of the
repository. Think of it as an "accept this update?" envelope.

You normally don't have to do anything with these: this repository includes a
small GitHub workflow that automatically accepts (merges) routine pull requests,
as long as they only touch the `KNOWLEDGE/` folder where briefings live.

If a pull request doesn't merge on its own (for example, your repository
protects its main branch), open it on github.com and press **Merge pull
request** yourself.

![A routine pull request on GitHub, merged](/docs/images/13-merged-PR.png)

## Reading your briefings

- **In the Claude app:** every finished run ends with a message containing the
  day's Overview — a few bullets you can skim — and a link to the full text. You
  get the same thing on your phone with the Claude mobile app.

  You can also **ask follow-up questions** in the Claude session.

   ![A finished run's final message with the Overview and pull request link](/docs/images/14-run-result.png)

- **On GitHub:** the full archive lives in the `KNOWLEDGE/` folder of your
  repository — daily briefings under `KNOWLEDGE/daily/`, fortnightly reviews
  under `KNOWLEDGE/fortnightly/`, and a living overview per topic under
  `KNOWLEDGE/topics/`.

   ![A finished run's research note](/docs/images/15-research-note.png)

  **Note on the screenshots:** They were taken during testing, where two runs were performed for the daily research.

## Get your briefings by email (optional)

Your daily and fortnightly briefings can also arrive by email. They are sent
from a dummy Gmail account you create just for this purpose, never using your
personal Gmail login. Setup takes only a few clicks; follow the
[email setup guide](/docs/email-setup.md). If you do not set it up, nothing
changes.

## Making it yours

The topics and questions the assistant researches are just files in your
repository — and you change them by asking Claude in plain language. Open a
Claude Code session on your repository (desktop app → **Code** tab → new
session, pick your repository) and ask, for example:

- *"Use the update-topics skill to add a topic about quantum computing."*
- *"Use the update-questions skill to add a question: which open models run
  well on a laptop?"*
- *"Change the timezone in config.yml to Europe/Paris."*

More copy-paste examples live in [`example_prompt.md`](example_prompt.md).
Claude makes the change and opens a pull request; merge it on github.com.
(Edits like these touch configuration files, so they are deliberately **not**
auto-merged — you get the final say.)

The `.claude` folder contains skills that mirror the `skills` folder, which is useful if you want to update your knowledge base from your local Claude Code cli.

## Troubleshooting

| Problem | What to do |
|---|---|
| Claude says the GitHub authorization expired, or can't reach the repository | Reconnect: redo Step 2. |
| "GitHub access is required for Claude Code on the web. Please contact an organization owner." | Your Claude account is a Team/Enterprise seat, where GitHub is linked once for the whole organization. See the note in Step 2 — or use a personal Pro/Max account. |
| GitHub says organization approval is required | Use a copy under your personal account, or ask the organization admin to approve the Claude GitHub App. |
| A routine didn't run | Check claude.ai/settings/usage (routine runs count against a daily cap) and confirm the routine is still enabled in the Routines list. |
| Pull requests aren't merged automatically | Open the pull request on github.com and press Merge. If it keeps happening, check **Settings → Actions → General → Workflow permissions** is set to "Read and write permissions". |
| A briefing merged, but no email arrived | See the troubleshooting steps in the [email setup guide](/docs/email-setup.md#8-troubleshooting). |
| The first email went to spam | Open it and press **Not spam**. |
| Cloud sessions are blocked on a company account or network | Organizations with IP allowlisting block cloud sessions entirely — ask your IT team or Anthropic support. |
| The fortnightly routine replies "Off-cadence date — fortnightly review skipped." | Normal off-week behavior — it runs weekly but only writes a report every second week. |

## For developers

Everything above needs no local tooling; this section is only for working on
the repository's code.

- Python environment: `environment.yml` creates the conda env
  `agent_daily_research` (PyYAML, pytest).
- Tests: `pytest -q`.
- Validators (routines run these; you can run them locally too):
  `scripts/validate_inputs.py`, `scripts/check_knowledge_links.py`,
  `scripts/purge_recyclebin.py`.
- A working `git` is a hard requirement for every skill in this repository:
  skills cache human changes, commit their own work, and hard-stop if git
  cannot run.
- Design rationale and open follow-ups:
  [`docs/design-decisions-and-open-followups.md`](/docs/design-decisions-and-open-followups.md).

Notes for maintainers:

- The email-sending `run` block is duplicated between the two workflows in
  [`.github/workflows/`](.github/workflows/); comments in both files mark the
  copies — keep them in sync.
- The no-double-send guarantee relies on auto-merge using the default
  `github.token`, whose events never start other workflow runs. Merging with a
  PAT or GitHub App token instead would make both email paths fire.
- Contingencies: if `gh pr diff` misbehaves on a just-merged PR, fall back to
  `gh api repos/<repo>/pulls/<n>/files --paginate`; if Google drops App
  Passwords, choose a replacement deliberately (the design doc records the
  rejected alternatives) rather than improvising in a workflow.
- The git tag `local-cron-final` preserves the pre-cloud local-cron
  implementation; recover files with `git show local-cron-final:<path>`.
