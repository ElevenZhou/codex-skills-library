# Meta Ads publish-only workflow

## State machine

```text
locate_authorized_scope
  -> select_exact_drafts
  -> inspect_pending_changes
  -> open_publish_review
  -> verify_final_count_and_scope
  -> confirm_publish
  -> wait_for_meta_response
  -> verify_each_result
```

## Browser control

- Prefer the Codex Chrome Plugin connected to the user's existing Chrome session.
- Use Codex Computer Use only as an explicitly authorized fallback.
- Do not use standalone Playwright or launch a separate automated browser profile by default.
- Read the current accessibility/UI state before every interaction sequence.
- Re-read state after navigation, selection changes, drawers, dialogs, and submission.
- Prefer current accessible element references; use coordinates only when Computer Use exposes no usable accessibility element.
- Stop after the first Meta-flow failure or persistent loading state. Do not refresh or retry repeatedly.

## Scope verification

Verify all of the following before final submission:

- advertising account
- campaign
- ad set
- exact selected ad names
- selected object count
- draft/unpublished-change status
- absence of unrelated campaign or ad-set changes in the review summary

If an exact name list is available, compare every selected name. If only an expected count is available, combine count verification with the campaign/ad-set boundary and visible selection.

## Mismatch policy

This workflow does not repair data. Stop when:

- the selected count differs
- extra objects appear in the publish review
- an intended draft is missing
- Meta includes budget, targeting, schedule, bid, identity, creative, URL, or tracking changes that were not explicitly included
- an item has a blocking validation error

Report the mismatch precisely so a separate editing workflow can fix it.

## Submission and verification

Immediately before the final publish click, obtain any confirmation required by the active Computer Use policy and the repository gate. After confirmation, wait for Meta's response. A successful click is not sufficient evidence.

Accept visible outcomes such as:

- submitted/in review
- processing
- active
- scheduled

Record failures and validation messages per item. Capture the final result screen or ads list under `output/browser/` when an artifact is required.
