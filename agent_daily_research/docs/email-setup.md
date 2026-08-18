# Get your briefings by email

Email delivery is optional. If you turn it on, briefings are sent from a
fresh Gmail account created only for this job — not from your personal Gmail
account. Your personal password never leaves your hands.

Everything below is done by clicking through Google and GitHub screens. You
do not need to install or run anything.

## 1. Why use a dummy Gmail account?

The dummy account keeps the automated sender separate from the account you
use every day. GitHub receives an App Password for this dedicated sender, not
the password for your personal account.

## 2. Create the dummy Gmail account

Create a fresh Gmail account by following Google's guide:
<https://support.google.com/mail/answer/56256>.

Choose any available address, for example `my-agent-news@gmail.com`. This
account only ever *sends*; your briefings can still arrive in your normal
inbox.

## 3. Turn on 2-Step Verification

While signed in to the dummy account, turn on 2-Step Verification by following
Google's guide: <https://support.google.com/accounts/answer/185839>.

Google requires 2-Step Verification before it will offer App Passwords. Do
not enrol this account in Advanced Protection, which prevents App Passwords
from being used.

## 4. Create an App Password

Still signed in to the dummy account, open
<https://myaccount.google.com/apppasswords>. Google's App Password help is at
<https://support.google.com/mail/answer/185833>.

Create a new App Password and give it a recognizable name, such as
`Knowledge briefings`. Google shows a 16-character password once. Copy all 16
characters **without spaces** and keep them ready for the next step.

## 5. Add three repository secrets

Open your repository on github.com, then click **Settings → Secrets and
variables → Actions → New repository secret**. Add each of these secrets one
at a time:

| Name | Value |
|---|---|
| `GMAIL_ADDRESS` | The full address of the dummy Gmail account. |
| `GMAIL_APP_PASSWORD` | The 16 App Password characters, with no spaces. |
| `KNOWLEDGE_EMAIL_TO` | The email address where you want to read your briefings. |


  ![GitHub repo secrets page](/docs/images/E01-gh-repo-secrets.png)

## 6. Choose the name your briefings are signed off with

Each email ends with `— <name>`. Set that name in `config.yml` at the root of
your repository:

```yaml
email:
  agent_name: "Le petit Kev"
```

Ask Claude to change it for you (*"Change email.agent_name in config.yml to
Research Bot"*) or edit the file on github.com. This is the only place the
sign-off is configured.

## 7. Verify the setup

Either wait for the next daily or fortnightly briefing to merge, or manually trigger the runs in Claude. Then, open your repository's **Actions** tab. The email run or step beginning **Email…** should be green, and the message should arrive at `KNOWLEDGE_EMAIL_TO`.

Check your spam folder the first time. If the message is there, open it and
press **Not spam**.

## 8. Troubleshooting

| Problem | What to do |
|---|---|
| `535 Username and Password not accepted` | Make sure you used the App Password, not the dummy account's normal password; remove any spaces; and confirm 2-Step Verification is on. Then repeat steps 3 and 4. |
| The App Passwords page is missing | Turn on 2-Step Verification and make sure the dummy account is not enrolled in Advanced Protection. |
| A briefing merged but no email arrived | Check that all three repository secrets exist. Open the run in the **Actions** tab: a missing secret produces a notice in the log. |
| The message went to spam | Open it and press **Not spam**. You should only need to do this once. |

## 9. Security and turning email off

The three secrets live only in GitHub's encrypted secret store — never in the
repository, never in Claude's sandbox. Delete all three repository secrets to
turn email off.
