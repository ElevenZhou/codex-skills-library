---
name: claude-daily-training
description: Run real daily Claude.ai creative training sessions through Codex and Chrome for engineering, short drama writing, and video prompt writing. Use when the user asks to run, schedule, operate, or design daily Claude training, node-based Claude browser sessions, Claude.ai Chrome workflows, or recurring creative practice across machines. Also use when creating Codex automations that invoke this workflow.
---

# Claude Daily Training

Skill version: `2026.07.24`

## Purpose

Run a daily Claude.ai session that produces a useful artifact. This skill is for legitimate creative and engineering practice, not account-warming filler.

## Daily Operating Model

- Organize work by Claude account first, then by track.
- Keep one concise daily note per account so the previous day can carry forward cleanly.
- Use English for the session prompt, follow-ups, and log output unless the user explicitly asks for another language.
- If the user references "the accounts", preserve the existing account grouping from memory or the workspace record and do not reshuffle without a reason.
- When today's work depends on yesterday's output, start with the prior artifact, state the continuity explicitly in the prompt, and refine rather than restart.

## Boundaries

- Use the logged-in Chrome profile on the node machine.
- Do not inspect cookies, local storage, passwords, or browser session files.
- Do not automate sign-in, CAPTCHA, OTP, password entry, anti-bot bypass, or payment actions.
- Do not send meaningless filler messages.
- Do not send secrets, credentials, private keys, customer data, or sensitive files to Claude.
- Ask for confirmation before sending a prompt in Claude.ai unless the user already gave explicit permission for that exact session.
- Prefer official APIs for fully unattended programmatic Claude usage.

## Browser Workflow

1. Use the Chrome browser skill/plugin when the user asks to operate an already logged-in Chrome profile.
2. Open or claim a Chrome tab for `https://claude.ai`.
3. If blocked by login, CAPTCHA, OTP, or browser permission prompts, stop and ask the user to handle it.
4. Choose today's track from the rotation below.
5. Read `references/session-prompts.md` for the exact English prompt template for the chosen track.
6. Fill the selected prompt with today's seed and, when relevant, the previous day's artifact or notes.
7. Confirm before sending the first prompt in the browser.
8. Run two follow-ups:
   - make the answer more concrete and less generic
   - ask for the final ready-to-use version
9. Save or report the result log in the thread. Do not silently store sensitive content.

## Track Rotation

| Day | Track | Output |
| --- | --- | --- |
| Monday | Engineering | Code review, API design, test plan, or debugging note |
| Tuesday | Short drama | Conflict outline, scene rewrite, or dialogue polish |
| Wednesday | Video prompt | Prompt variants, shot list, or style bible |
| Thursday | Engineering | Implementation plan or refactor proposal |
| Friday | Short drama | Hook, twist, and retention rewrite |
| Saturday | Video prompt | Batch prompts for a theme |
| Sunday | Review | Improve the best output of the week |

If the user specifies a track, use their track instead of the rotation.

## Node Automation Pattern

For each node machine:

1. Install/enable Codex and the Codex Chrome Extension in that node's Chrome profile.
2. Keep Claude.ai logged in manually in Chrome.
3. Create a Codex cron automation with a prompt like:

```text
Use the claude-daily-training skill to run today's Claude.ai training workflow on this node. Open Chrome, use the logged-in Claude.ai session, select today's track, prepare the exact prompt, ask for confirmation before sending, run two follow-ups after user approval, and report the final result log.
```

4. Stagger schedules by node to avoid simultaneous browser sessions.
5. Keep a per-node record with node id, Chrome profile, Claude account owner, schedule, and last successful session.

## Output Log

Report this after each session:

```text
Date:
Account group:
Node/profile:
Track:
Claude conversation title:
Yesterday's carryover:
Final artifact summary:
Usefulness /10:
Specificity /10:
Can reuse tomorrow: yes/no
Next improvement:
```

## Failure Handling

- Chrome control unavailable: report that the Codex Chrome Extension is missing/disabled or the browser connection is unavailable.
- Claude page unavailable: leave the tab for handoff and ask the user to check Claude.ai.
- Login required: ask the user to log in manually.
- CAPTCHA/OTP required: ask the user to complete it manually.
- Prompt contains sensitive data: redact or ask the user for a safe replacement.
