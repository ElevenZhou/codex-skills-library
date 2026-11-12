---
name: advanced-frontend-design
description: Design, build, and refine distinctive production-grade frontend pages and apps with a free-first workflow and a browser/static QA script. Use when asked to build or redesign a landing page, SaaS product, dashboard, internal tool, portfolio, 中文产品/H5/小程序 界面, or component; to avoid generic AI/Codex look (去AI味, 别做成模板); to pick a visual direction, use only free/open-source resources, fix UX states and accessibility, write precise UI specs, add motion, or verify a frontend in the browser. For a critique-only second pass use frontend-design-review; for multi-direction comparison use frontend-design-lab.
---

# Advanced Frontend Design

Skill version: `2026.11.12`

Create frontend work with a clear point of view, complete product behavior, and browser-verified polish. Act as a design director, UX reviewer, and senior frontend engineer in one workflow.

## 何时用 / 何时不用

Use for: building or redesigning pages and apps, choosing a direction, polishing states/motion/a11y, Chinese-language products, writing a precise UI spec.

Do not use for: critique-only requests (use `frontend-design-review`), comparing several finished directions (use `frontend-design-lab`), landing-page aesthetic dials and block library (use `design-taste-frontend`), or tiny one-off components where the project's design system already decides everything.

## 相关 skill

- `frontend-design-review`: second-pass critique with P0/P1/P2 findings; reuses `scripts/verify_frontend.py` from here.
- `frontend-design-lab`: controlled multi-direction experiments; hands the chosen direction back to this skill (see its `handoff-to-production.md`).
- `design-taste-frontend` (taste-skill): anti-slop rules and dials for landing pages, portfolios, redesigns; not for dashboards.
- `playwright` / `playwright-interactive`: browser automation for the visual and interaction checks.
- `local-image-generator`: still images for hero or map assets, only when a bitmap changes comprehension.

## Non-Negotiable Defaults

- Use free and open-source resources by default. Do not depend on paid tiers, premium templates, or credit-based builders unless the user explicitly opts in.
- Preserve the repository's framework, design system, architecture, and conventions when they already exist.
- Build the requested experience as the first screen. Do not replace an app or tool request with a marketing landing page.
- Make one deliberate visual direction fit the audience and content. Do not blend several fashionable styles without a reason.
- Avoid generic AI patterns: purple-blue gradients, interchangeable rounded card grids, excessive pills, glass everywhere, giant empty heroes, decorative blobs, and identical icon-text feature blocks.
- Avoid default typography such as Inter, Roboto, Arial, or a system stack for Latin display and brand text unless the project already requires it. Exception: for Chinese body text a well-chosen system CJK stack is correct (see [chinese-product-ui.md](references/chinese-product-ui.md)).
- Use cards only for real grouped objects, repeated records, modals, or framed tools. Do not put cards inside cards or turn every page section into a floating panel.
- Keep product and operations interfaces dense, calm, scannable, and task-oriented. Reserve expressive editorial composition for brand, campaign, portfolio, and content-led pages.
- Implement real states and interactions. Do not stop at a polished static screenshot.
- Inspect the result in a real browser and revise from evidence before declaring completion.

## Workflow

### 1. Read the Product Before Designing

Inspect the repository, current screen, content, assets, routes, and existing design tokens. Infer what can be learned locally before asking questions.

Identify:

- primary user and job to be done
- page class: product, operations, commerce, editorial, brand, portfolio, or campaign
- primary action and information hierarchy
- technical and accessibility constraints
- assets and component libraries already available

### 2. Write a Design Contract

Before coding, state a compact internal design contract:

```text
Visual thesis: one sentence describing the intended character.
Content hierarchy: the three things users should notice in order.
Interaction thesis: where motion or direct manipulation earns its place.
Signature moment: the single memorable visual or interaction idea.
Anti-template decisions: at least three common AI defaults this design rejects.
```

For a new visual direction, read [design-directions.md](references/design-directions.md). Choose one direction and adapt it to the domain; do not copy it as a fixed theme. Name each layout pattern precisely using [ui-vocabulary.md](references/ui-vocabulary.md) so the spec leaves nothing to guesswork.

### 3. Establish the System

Define or extend tokens before styling isolated components:

- semantic color roles with one restrained accent and supporting neutrals
- a purposeful display/body/mono typography plan where relevant
- spacing, radius, border, shadow, and motion scales
- stable responsive dimensions for boards, toolbars, counters, grids, and controls
- focus, hover, active, disabled, selected, loading, empty, success, warning, and error behavior

Use existing tokens first. Keep card radius at 8px or less unless the established system says otherwise. Keep letter spacing at zero and do not scale text directly with viewport width.

### 4. Route Free Resources Deliberately

Read [free-toolkit.md](references/free-toolkit.md) when selecting inspiration or external resources. Read [component-sources.md](references/component-sources.md) before adding a UI, animation, or component dependency.

Prefer this order:

1. Existing project components and assets
2. Platform primitives and small local CSS/JS implementations
3. Free, accessible primitives that match the current framework
4. Free animation or presentation snippets used only for a signature moment

Do not add a library merely to imitate one component. Verify the license and free-tier boundary before recommending or installing anything not already in the repository.

When available, combine the installed `frontend-design` skill for visual authorship and `ui-ux-pro-max` for product states, accessibility, and UX critique. This skill remains the orchestration and quality layer.

### 5. Implement for the Domain

For product, SaaS, dashboard, and internal-tool work:

- optimize scanning, comparison, repeated action, and keyboard use
- use compact headings and predictable navigation
- include filters, state feedback, empty/loading/error states, and recovery paths where natural
- use icons for familiar tools and add tooltips for unfamiliar icon-only actions

For brand, landing, editorial, campaign, and portfolio work:

- make the brand, offer, subject, or work visible in the first viewport
- use a real, repository-provided, freely licensed, or user-approved generated visual when imagery carries the subject
- let the hero reveal a hint of the next section on desktop and mobile
- use expressive type, composition, and motion selectively; keep content legible and actionable

For every page:

- make desktop and mobile composition intentional rather than merely stacked; write the one-line mobile order before coding
- keep text inside its container and prevent overlap at all supported sizes
- cover the full state matrix and accessibility baselines in [states-and-a11y.md](references/states-and-a11y.md)
- use motion from [motion-interaction.md](references/motion-interaction.md) sparingly, and respect `prefers-reduced-motion`
- for Chinese-language products read [chinese-product-ui.md](references/chinese-product-ui.md) (font stacks, density, H5/小程序, formats)
- avoid visible instructional copy that explains the interface instead of letting controls communicate their purpose

### 6. Run the Anti-Template Audit

Pause after the first implementation pass. Redesign if three or more of these are true:

- the page could belong to any unrelated product after swapping the logo
- most content is presented as similarly rounded cards
- the hero is centered text followed by a generic dashboard mockup
- color is dominated by purple-blue, slate, beige, or one hue family without meaningful contrast
- typography contributes no hierarchy or character
- motion is scattered decoration rather than one coherent interaction idea
- icons substitute for meaningful content
- spacing is uniformly generous even where users need density
- mobile is only the desktop layout stacked vertically
- the design has no signature moment tied to the subject

### 7. Verify and Revise in a Real Browser

Read and apply [quality-gate.md](references/quality-gate.md) for every implementation or review. Start with the automated pass:

```bash
python3 <skill-dir>/scripts/verify_frontend.py path/to/index.html --out ./verify-output
# options: --viewports 1440x900,390x844  --format json  --static  --strict
```

Honest scope: with python `playwright` + Chromium it screenshots both viewports and reports console errors, horizontal overflow, missing alt, and unnamed controls. Without playwright (as on machines without it) it runs a static HTML audit only (title, lang, viewport, alt, empty links/buttons, heading order, `!important`, external CDN/font URLs, reduced-motion, focus styles) and prints a note saying no rendering was checked. A static pass is not browser verification. Then use Playwright or the available browser tooling to inspect at desktop and mobile sizes, exercise critical interactions, and make at least one evidence-based refinement pass.

Do not claim browser verification if it was not run. Report the exact verification completed and any remaining risk.

## Review-Only Requests

When asked to critique an existing page, prefer `frontend-design-review` for a scored, prioritized report. If staying in this skill, lead with concrete findings ordered by user impact. Separate visual authorship problems from UX, accessibility, responsiveness, and implementation defects. Cite files and lines when code is available. Recommend the smallest redesign that establishes a coherent direction instead of proposing a wholesale rewrite by default.

## Completion Format

Keep the handoff concise and include:

- the visual direction and the signature decision
- the important implementation locations
- the free components or resources used, if any
- browser sizes and interactions verified
- unresolved limitations only when they are real

## References

- [ui-vocabulary.md](references/ui-vocabulary.md): precise pattern names with prompt phrases
- [motion-interaction.md](references/motion-interaction.md): motion principles and dependency-free snippets
- [states-and-a11y.md](references/states-and-a11y.md): state matrix, forms, keyboard, contrast, CJK/RTL
- [chinese-product-ui.md](references/chinese-product-ui.md): Chinese-language product guidance
- [design-directions.md](references/design-directions.md), [quality-gate.md](references/quality-gate.md), [free-toolkit.md](references/free-toolkit.md), [component-sources.md](references/component-sources.md)

## 变更记录 / Changelog

- `2026.11.12`: added ui-vocabulary, motion-interaction, states-and-a11y, chinese-product-ui references; added `scripts/verify_frontend.py` (playwright when available, static fallback) and wired it into the verify step; encoded A/B-test composition lessons in quality-gate and operating-context routing in design-directions; added when-to-use and related-skill sections; clarified the system-font rule for CJK.
- `2026.07.24`: initial version (design contract, free-first routing, anti-template audit, browser quality gate).
