# Autopilot Loop Contract

Use this reference for broad, high-value, multi-artifact, or multi-hour goals. Keep the contract short enough to guide execution without becoming a report.

## Goal Contract

Create a working contract with these fields:

- **Objective:** the concrete outcome to deliver.
- **Audience/user:** who the result is for and what they need to understand or do.
- **Inputs:** local files, docs, data, URLs, credentials, examples, and assumptions.
- **Deliverables:** files, URLs, commands, reports, screenshots, decks, apps, or commits.
- **Constraints:** style, language, tools, privacy, budget, time, compatibility, and must-avoid items.
- **Acceptance checks:** observable tests that prove the deliverable is good enough.
- **Fallbacks:** what to try if the preferred tool or data source fails.
- **Roles/lanes:** planner, researcher, builder, verifier, critic, integrator; specify which are real subagents vs internal roles.
- **Stop condition:** exact condition for "done enough" and what still requires user preference.

## Loop Ledger

For substantial work, keep a lightweight ledger in the workspace:

```text
Objective:
Deliverables:
Assumptions:
Plan:
Parallel lanes:
QA gates:
Findings:
Fixes applied:
Residual risks:
Final artifacts:
```

Do not over-document. The ledger is for continuity and quality, not ceremony.

## Acceptance Check Patterns

Use artifact-appropriate checks:

- **Code/app:** install/build/test/lint, typecheck, smoke test, browser screenshot, error-log review.
- **PPT/document/PDF:** render to images, inspect layout, confirm page/slide count, check text overflow, verify key sections.
- **Spreadsheet/data:** row counts, formula recalculation, sample checks, totals, schema validation.
- **Research/report:** source quality, recency, citations, contradiction checks, assumptions labeled.
- **Images/design:** dimensions, visual inspection, prompt fit, brand consistency, no broken text or obvious artifacts.
- **Quant/trading:** data provenance, no look-ahead bias, transaction costs, benchmark comparison, drawdown, overfit warnings, reproducible backtest.
- **Automation/workflow:** dry run, idempotency, failure modes, logs, clear user handoff.

## Iteration Heuristic

Run at least one improvement pass when:

- The first output is structurally correct but not polished.
- Visual hierarchy, wording, or usability can clearly improve.
- Verification reveals any concrete issue.
- The task is strategic, client-facing, commercial, or high leverage.

Stop when:

- Acceptance checks pass.
- Further changes are mostly subjective or would require user preference.
- A true blocker remains after reasonable fallbacks.

## Escalation Policy

Escalate to user only when:

- A missing credential or paid service is required.
- A destructive or irreversible action is required.
- The tradeoff changes business intent, legal exposure, financial risk, or security posture.
- A required external system is down and local fallbacks cannot produce a useful result.

## Final Handoff Template

Report:

- What was completed.
- Where the artifact lives.
- How it was checked.
- Any assumptions or residual risks that matter.
- The most useful next action, if there is one.
