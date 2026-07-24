# QA Gates

Use the gate that matches the deliverable. Passing tool execution is not enough; inspect the artifact.

## Universal Gate

- Deliverable exists in a durable path.
- User's explicit requirements are covered.
- Old brand names, placeholders, TODOs, and internal notes are removed.
- Assumptions and risks are labeled.
- A revision pass or reason to skip revision is recorded.

## PPT / Slides Gate

- PPTX exists and renders.
- Slide count and required sections match the brief.
- Contact sheet inspected.
- No overflow or clipping remains.
- Chapter rhythm exists for long decks.
- Images are meaningful, not filler.
- Tables/charts are legible and support the slide claim.

## PDF / Document Gate

- DOCX/PDF opens or renders to pages.
- Page breaks, headings, tables, footers, and numbering are correct.
- Citations or source references are present when needed.
- No tracked-change/comment artifacts remain unless requested.

## Research Gate

- Sources are current and credible.
- Primary sources are preferred for technical/legal/financial claims.
- Claims, inference, and recommendations are separated.
- Contradictions or uncertainty are surfaced.
- Links/citations are included.

## Website / App Gate

- Build/test/lint/typecheck run when available.
- App starts or page renders.
- Critical user flow is smoke-tested.
- Browser screenshot or DOM inspection confirms UI.
- Mobile/responsive state is considered for frontend.
- Error states and logs are checked.

## Code / Automation Gate

- Tests or smoke scripts run.
- Idempotency and failure behavior checked.
- No unrelated user changes reverted.
- Commands and environment assumptions documented.

## Quant / Trading Gate

- Data source and cleaning assumptions documented.
- No look-ahead bias or survivorship bias if avoidable; if unknown, explicitly warn.
- Transaction costs/slippage modeled or labeled missing.
- Benchmark comparison included.
- Drawdown, volatility, turnover, and exposure reported.
- Output labeled as research, not investment advice.
