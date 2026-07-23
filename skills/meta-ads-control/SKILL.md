---
name: meta-ads-control
description: Analyze Meta Ads performance, inspect campaigns/ad sets/ads, export API reports, and safely pause or activate delivery with the installed meta-ads CLI. Use when Codex needs Meta Marketing API account discovery, campaign analysis, reporting, status inspection, or controlled ad delivery management.
---

# Meta Ads Control

Use the installed `meta-ads` command. Return structured JSON for analysis.

## Start

Verify the command and configuration:

```bash
command -v meta-ads
meta-ads --json doctor
```

If credentials are missing, request configuration of `META_ACCESS_TOKEN` and `META_AD_ACCOUNT_ID`. Never ask the user to paste a token into chat, source files, command flags, or committed configuration.

## Discover and read

Run discovery before assuming object IDs:

```bash
meta-ads --json accounts list
meta-ads --json campaigns list --status ACTIVE,PAUSED
meta-ads --json adsets list --limit 100
meta-ads --json ads list --limit 100
```

Read an exact object when its ID is known:

```bash
meta-ads --json ads get AD_ID
```

## Analyze and report

Prefer campaign-level data for account summaries and ad-level data for creative decisions:

```bash
meta-ads --json insights get --level campaign --date-preset last_30d
meta-ads --json insights get --level ad --date-preset last_7d --time-increment 1
meta-ads --json reports export --level ad --date-preset last_30d --out ./reports/meta-ads.json
```

Report spend, impressions, reach, frequency, clicks, CTR, CPC, CPM, actions and cost per action. State when conversion attribution or action mappings are unavailable.

## Manage delivery

Preview every status change first:

```bash
meta-ads --json delivery set AD_ID --status PAUSED
```

Only after the user explicitly authorizes the exact object and target status, execute:

```bash
meta-ads --json delivery set AD_ID --status PAUSED --apply --confirm
```

Treat `ACTIVE` as publishing/enabling delivery. Do not activate, pause, or change a live object based only on an optimization suggestion.

## Raw API reads

Use the read-only escape hatch only when a high-level command lacks a field:

```bash
meta-ads --json request get /OBJECT_ID --fields id,name,effective_status
```

Do not create a generic raw write path. Add a narrow reviewed CLI command instead.

## Safety rules

- Never expose access tokens in output, files, logs, flags, or chat.
- Do not perform live writes without explicit user approval.
- Resolve names to stable Meta IDs before writes.
- Stop on ambiguous duplicate names or account mismatch.
- Read back the object after a successful status change before declaring completion.
- Do not delete objects, adjust budgets, or modify targeting using the delivery command.
