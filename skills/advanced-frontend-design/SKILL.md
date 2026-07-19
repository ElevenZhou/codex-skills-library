---
name: advanced-frontend-design
description: Design, build, critique, and refine distinctive production-grade frontend pages and applications with a free-first workflow. Use for landing pages, SaaS products, dashboards, internal tools, portfolios, component redesigns, or any request to avoid generic AI/Codex aesthetics, choose a stronger visual direction, use only free/open-source resources, improve UX states, or verify a frontend in a real browser.
---

# Advanced Frontend Design

Create frontend work with a clear point of view, complete product behavior, and browser-verified polish. Act as a design director, UX reviewer, and senior frontend engineer in one workflow.

## Non-Negotiable Defaults

- Use free and open-source resources by default. Do not depend on paid tiers, premium templates, or credit-based builders unless the user explicitly opts in.
- Preserve the repository's framework, design system, architecture, and conventions when they already exist.
- Build the requested experience as the first screen. Do not replace an app or tool request with a marketing landing page.
- Make one deliberate visual direction fit the audience and content. Do not blend several fashionable styles without a reason.
- Avoid generic AI patterns: purple-blue gradients, interchangeable rounded card grids, excessive pills, glass everywhere, giant empty heroes, decorative blobs, and identical icon-text feature blocks.
- Avoid default typography such as Inter, Roboto, Arial, or a system stack unless the project already requires it.
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

For a new visual direction, read [design-directions.md](references/design-directions.md). Choose one direction and adapt it to the domain; do not copy it as a fixed theme.

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

- make desktop and mobile composition intentional rather than merely stacked
- keep text inside its container and prevent overlap at all supported sizes
- respect `prefers-reduced-motion`
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

Read and apply [quality-gate.md](references/quality-gate.md) for every implementation or review. Use Playwright or the available browser tooling, inspect at desktop and mobile sizes, capture screenshots, exercise critical interactions, and make at least one evidence-based refinement pass.

Do not claim browser verification if it was not run. Report the exact verification completed and any remaining risk.

## Review-Only Requests

When asked to critique an existing page, lead with concrete findings ordered by user impact. Separate visual authorship problems from UX, accessibility, responsiveness, and implementation defects. Cite files and lines when code is available. Recommend the smallest redesign that establishes a coherent direction instead of proposing a wholesale rewrite by default.

## Completion Format

Keep the handoff concise and include:

- the visual direction and the signature decision
- the important implementation locations
- the free components or resources used, if any
- browser sizes and interactions verified
- unresolved limitations only when they are real
