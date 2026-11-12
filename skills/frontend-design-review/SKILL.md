---
name: frontend-design-review
description: Second-pass design critique of an existing page, screenshot, or frontend code, producing prioritized findings (P0 blocking / P1 / P2) with evidence, fix, and effort per finding, plus a scored 0-5 rubric. Use when the user says 设计评审, 审一下这个页面, 二审, 看着像AI做的, 太模板了, 有AI味, design review, critique this page/UI, review the design, "does this look AI-generated", or wants a quality gate after a frontend was built. Review only: does not rewrite code unless the user asks.
---

# Frontend Design Review (二审)

Skill version: `2026.11.12`

A critic, not a builder. Take an existing page (URL, HTML/code, or screenshot) and return findings a team can act on, ordered by user impact. Written from scratch; the idea of a dedicated review pass is surveyed in `frontend-web-tools-comparison-20260718.md` (Microsoft `frontend-design-review`), which this skill does not copy.

## 何时用 / 何时不用

Use when: a page was just generated and needs a skeptical second look; the user suspects an AI/template look; before shipping or before choosing what to fix first; comparing a result against the original brief.

Do not use when: the user wants the page built or redesigned (use `advanced-frontend-design`), wants several directions explored (use `frontend-design-lab`), or wants landing-page generation rules (use `design-taste-frontend`).

**This skill does not rewrite code unless asked.** Output is a report. Offer the fix list, and wait. If the user says "fix the P0s", then switch to `advanced-frontend-design` conventions and make the smallest change per finding.

## 相关 skill

- `advanced-frontend-design`: builds and fixes; owns `scripts/verify_frontend.py`, which this skill reuses (do not copy it) and the references `quality-gate.md`, `states-and-a11y.md`, `chinese-product-ui.md`.
- `frontend-design-lab`: when the review concludes the direction itself is wrong, propose a multi-direction experiment.
- `design-taste-frontend`: its section 9 "AI Tells" is the detailed ban list to cross-check generic-look findings.
- `playwright` / `playwright-interactive`: capture screenshots and exercise interactions when `verify_frontend.py` has no browser.
- `local-image-generator`: only if a finding is "hero lacks real imagery" and the user wants an asset generated.

## Inputs and Evidence Rules

Accept any of: URL, local HTML/project path, screenshot(s), or code snippet. Say which you got; evidence quality depends on it.

- Code available: cite `file:line` or selector.
- Screenshot only: cite the region ("hero, top-right quarter", "mobile 390px, second stat row") and do not claim facts only code can show (focus styles, console errors, real contrast values).
- Never invent. If a check could not run, list it under "Not verified".

## Workflow

1. **Frame.** State the page class (product, operations, commerce, editorial, brand, portfolio), audience, and primary job in one line. If the brief is unknown, infer it from the page and say so.
2. **Run the automated pass** (if there is code or a URL):
   ```bash
   python3 <skills>/advanced-frontend-design/scripts/verify_frontend.py <path-or-url> --out ./review-shots
   ```
   Report its mode honestly (browser vs static fallback). Treat its findings as inputs, not the review.
3. **Look at it.** Open at about 1440x900 and 390x844 (via the verify script screenshots, `playwright`, or the provided images). Do a 10-second squint test: what do you notice first, second, third? Is it what the page needs?
4. **Walk the ten axes** in [review-rubric.md](references/review-rubric.md): generic/AI-template tells, hierarchy, typography, color/contrast, spacing/rhythm, responsive, interaction states, accessibility, performance, content realism. Score each 0-5 with one-sentence evidence.
5. **Write findings** using [report-template.md](references/report-template.md). Each has: ID, severity, axis, evidence, why it matters, fix, effort (S under 1h, M half day, L day or more). Merge duplicates; one root cause is one finding.
6. **Recommend.** Name the smallest redesign that fixes the P0s and the highest-leverage P1s. State what to keep. If three or more AI-template tells coincide with a generic structure, recommend recomposition (not restyling).

## Severity

- **P0 blocking:** task cannot be completed or understood, content unreadable, broken layout at a supported size, inaccessible critical path (no keyboard, no names), console errors that break features, contrast failure on primary text.
- **P1 should fix before ship:** weak hierarchy, template-looking structure, missing states, mobile only stacked, inconsistent spacing system, body text below baseline, motion without reduced-motion handling.
- **P2 polish:** secondary alignment, copy rhythm, icon consistency, minor performance wins, subtle motion tuning.

Do not pad. A review with three real P0/P1 findings beats twenty P2s. Praise only what should be preserved, in the "Keep" list.

## Tone and Boundaries

- Concrete and specific: say "the four equal stat cards under the hero repeat one structure" rather than "layout feels generic".
- Separate taste from defect. Mark taste opinions as such ("preference") and keep them out of P0/P1 unless they contradict the brief.
- Do not review business logic or copy legalities. Flag factual or fake-looking content only as a realism issue.
- Free-first: recommend free/open-source fixes only.

## Completion Format

Return the report from the template: summary verdict (one paragraph), scorecard table, findings by severity, Keep list, Not verified list, and recommended next step. Keep the chat summary under about 15 lines when the full report is long; save the full report to a file only if the user asked for one.

## 变更记录 / Changelog

- `2026.11.12`: initial version.
