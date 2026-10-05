# Autopilot Modes

Select one or more modes after reading the user's goal.

## PPT / Deck Mode

Use for company introductions, BP, product decks, sales decks, and roadshows.

Route to `deck-studio-loop` and `Presentations`.

Minimum loop:

1. Define audience and communication job.
2. Build narrative and section rhythm.
3. Create visual system; avoid generic templates.
4. Produce real PPTX.
5. Render slides, inspect contact sheet, run overflow checks.
6. Run product/sales/investor/domain/visual/copy review.
7. Revise and deliver PPTX plus preview path.

## PDF / Document Mode

Use for reports, proposals, policies, white papers, redlines, and formal documents.

Route to `documents` or `pdf` as appropriate.

Minimum loop:

1. Define audience, document purpose, and required sections.
2. Gather source material and citations.
3. Draft structure and write concise copy.
4. Generate DOCX/PDF.
5. Render pages and inspect layout.
6. Check citations, tables, headings, page breaks, and final file accessibility.

## Research / Strategy Mode

Use for market research,方案调研, competitive analysis, technical selection, regulatory review, and industry synthesis.

Minimum loop:

1. Define research question and decision to support.
2. Browse primary/current sources when needed.
3. Track source date, credibility, and contradiction.
4. Separate facts, inference, and recommendation.
5. Deliver a structured report or deck with citations.

## Website / App Development Mode

Use for frontend, backend, full-stack, UI, dashboards, and app features.

Minimum loop:

1. Inspect project structure and existing patterns.
2. Define user flow and acceptance tests.
3. If visual taste is unsettled, route to `frontend-design-lab` for a bounded comparison; otherwise use `advanced-frontend-design` to define one direction.
4. Persist generated concepts and record how the selected direction translates into tokens, layout, states, and motion.
5. Implement in small disjoint changes.
6. Run install/build/test/typecheck/lint where available.
7. Use browser screenshots for frontend QA.
8. Review accessibility, responsiveness, error states, and logs.
9. Reconcile design docs, QA records, screenshots, and actual runtime files before handoff.

## Engineering / Code System Mode

Use for APIs, CLIs, refactors, automations, data pipelines, and infrastructure.

Minimum loop:

1. Inspect architecture and dependencies.
2. Identify write scope and risks.
3. Implement with tests or smoke scripts.
4. Validate idempotency, errors, and edge cases.
5. Avoid destructive commands and preserve user changes.

## Quant Trading / Financial Engineering Mode

Use for strategies, backtests, data pipelines, factor research, execution systems, and risk dashboards.

Minimum loop:

1. Define market, asset universe, timeframe, data sources, and benchmark.
2. Verify data quality, survivorship bias, look-ahead bias, timezone/session handling, corporate actions, and fees.
3. Implement reproducible research notebook/script or app.
4. Backtest with transaction costs and slippage assumptions.
5. Report returns, volatility, Sharpe, max drawdown, turnover, exposure, and failure modes.
6. Label outputs as research, not financial advice.

## Hybrid Mode

For large goals, combine modes and sequence outputs:

1. Research/report first.
2. Prototype/build second.
3. Deck/document third.
4. QA and integration last.
