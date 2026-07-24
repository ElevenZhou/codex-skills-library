---
name: meta-ads-auto-publish
description: "Publish already-prepared Meta/Facebook Ads drafts through the user's existing Chrome session using Codex-native Chrome control, with limited Computer Use fallback, and verify the resulting delivery or review status. Use when Codex is explicitly asked to 自动发布广告, 发布 Meta 广告, publish prepared Facebook ad drafts, submit selected ads for Meta review, or retry a failed publish operation. This skill is publish-only: do not create ads, replace media, rewrite copy, change targeting, or repair campaign configuration; stop and report any pre-publish mismatch instead."
---

# Meta Ads Auto Publish

Skill version: `2026.07.25`

Publish existing, prepared ads only. Treat the live Meta Ads Manager selection and the user's explicit publish request as the source of authorization.

## Browser control

Use Codex-native browser control in this order:

1. Use the Codex Chrome Plugin to control the user's existing Chrome tab, profile, login state, and extensions.
2. If the Chrome Plugin is unavailable or cannot initialize, use Codex Computer Use only when the user explicitly permits that fallback.
3. Do not silently fall back to standalone Playwright, a separate automated Chrome profile, shell browser automation, AppleScript, or Marketing API writes.

Keep browser use limited:

- Perform one read-only preflight pass before any publish action.
- Re-read the live UI after navigation, selection changes, dialogs, or submission.
- Stop after the first backend-flow failure, persistent loading screen, login wall, checkpoint, CAPTCHA, permission error, or account restriction.
- Do not refresh repeatedly, change URLs to bypass a failure, reopen profiles, or retry the same Meta flow without a new explicit user instruction.
- Never inspect cookies, passwords, browser storage, or profile files.

## Establish the publish scope

Extract the intended campaign, ad set, ad names or expected ad count from the user's request and available project files. If the scope cannot be identified safely, inspect Meta Ads Manager and project documentation; ask only when ambiguity remains material.

Do not expand the scope beyond the named campaign, ad set, selection, or exact ad list.

## Perform read-only preflight

Before clicking a publish action:

1. Open the target campaign and ad set.
2. Switch to the Ads level.
3. Select only the intended draft ads.
4. Confirm every selected item is a draft or contains unpublished changes.
5. Confirm the selected count and exact names match the intended scope.
6. Inspect Meta's review summary for unexpected campaign, ad-set, budget, targeting, identity, creative, or tracking changes.

Do not edit mismatches. Stop and report them because this skill is publish-only.

## Publish

Read [publish-workflow.md](references/publish-workflow.md) before live execution.

Once preflight matches the authorized scope:

1. Click `发布`, `Publish`, `检查并发布`, or `Review and publish` as required by the current UI.
2. Re-snapshot after the review drawer, dialog, or page opens.
3. Reconfirm the pending object count and scope in the final confirmation UI.
4. Request action-time confirmation immediately before the final publish/submit click when the active UI-control policy requires it. Treat prior scope authorization as permission to prepare the submission, not as permission to bypass a required final confirmation.
5. Wait for Meta's completion response and verify each target item's resulting status.

The explicit request to use this skill for a defined scope is publish authorization. Authentication, CAPTCHA, account restrictions, duplicate/ambiguous selections, or changed scope still require human intervention.

## Prohibited actions

Do not:

- create or duplicate ads
- modify names, media, copy, URLs, UTM, identity, targeting, schedule, bid, or budget
- toggle creative enhancements
- publish objects outside the authorized scope
- report success based only on clicks or local logs

## Report results

Report each target as one of:

- `submitted_for_review`
- `processing`
- `published_active`
- `published_scheduled`
- `failed`
- `needs_human`

Include the account, campaign, ad set, selected count, visible Meta status, and any error message. Save evidence under the workspace `output/browser/` directory when local artifacts are needed; otherwise rely on the verified live UI state.
