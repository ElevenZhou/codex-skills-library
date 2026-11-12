---
name: frontend-design-lab
description: Create controlled frontend design experiments that hold one product contract constant while producing, implementing, and browser-testing multiple mutually exclusive visual directions. Use when the user asks for several frontend styles, 多个风格方案, 风格对比, A/B or multi-variant design comparison, 设计实验室/界面棱镜, aesthetic exploration before choosing a direction, comparison of minimalist/industrial/cartographic/editorial strategies, or evidence-based selection that avoids generic AI/Codex templates. After a direction is chosen, hand off to advanced-frontend-design.
---

# Interface Prism (frontend-design-lab)

Skill version: `2026.11.12`

Treat one product as a controlled design experiment. Keep its users, content, data, behavior, stack, and acceptance criteria fixed; vary only the design strategy, composition, material language, typography, and motion grammar.

## 何时用 / 何时不用

Use when the decision is "which direction", the cost of a wrong direction is high, or the user explicitly wants several variants side by side.

Do not use when the direction is already known (use `advanced-frontend-design`), when the task is a quick page or component, or when the user only wants a critique of one page (use `frontend-design-review`). Do not run a lab to avoid making a design decision: three variants cost roughly three builds.

## 相关 skill

- `advanced-frontend-design`: product contract, anti-template audit, quality gate, `scripts/verify_frontend.py`; receives the winner (see [handoff-to-production.md](references/handoff-to-production.md)).
- `frontend-design-review`: score or sanity-check each variant (or the production result) with the 0-5 rubric.
- `design-taste-frontend`: aesthetic dials and AI-tell ban list for landing, portfolio, redesign variants.
- `playwright` / `playwright-interactive`: screenshots and interaction checks for the comparison.
- `local-image-generator`: the only still-image generator; use for a direction that truly needs a bitmap.

## Core Rule

Do not produce several recolored versions of one layout. Create genuinely different interface silhouettes that solve the same product task.

Do not merge the visual signatures back into one page. Select a direction after comparison, then refine that direction for production.

## Orchestration

When available, combine:

- `advanced-frontend-design` for the product contract, anti-template audit, implementation, and browser quality gate
- `frontend-design` for visual authorship and memorable composition
- `ui-ux-pro-max` for states, accessibility, information architecture, and UX critique
- `local-image-generator` (the library's single still-image skill) only when a bitmap asset materially improves one direction
- `playwright` or available browser tooling for the controlled comparison, and `advanced-frontend-design/scripts/verify_frontend.py` for the per-variant technical pass

Remain free-first. Do not depend on paid builders, premium templates, or paid component tiers. Do not trigger a quota-consuming image API unless the user requested generated imagery or has authorized that local tool workflow.

## Workflow

### 1. Inspect Before Experimenting

Read the repository, current page, routes, components, assets, design tokens, and existing screenshots. For an existing project, produce a compact audit:

```text
Preserve: architecture, behavior, brand, and components that already work.
Fix now: high-impact hierarchy, typography, layout, state, and responsiveness defects.
Defer: worthwhile changes outside the current experiment.
Do not touch: protected business logic, routes, APIs, or framework choices.
```

Do not migrate frameworks or rewrite product logic merely to run a visual experiment.

### 2. Lock the Shared Product Contract

Read [experiment-protocol.md](references/experiment-protocol.md) and write the contract before designing:

- primary user and job to be done
- first-screen outcome and critical path
- fixed content, data, and content length
- fixed interactions and required states
- fixed framework, component library, and asset constraints
- fixed desktop and mobile viewports
- shared technical and accessibility acceptance criteria

If these variables differ across variants, the comparison is invalid.

### 3. Select Mutually Exclusive Directions

Read [direction-packs.md](references/direction-packs.md). Choose three directions by default; use two for a narrow A/B decision or four to five only when the decision space genuinely needs it.

Include the existing design as a baseline when redesigning a real project. Do not intentionally weaken the baseline.

For every direction, define:

```text
Visual thesis: one sentence.
Page silhouette: rail, ledger, canvas, console, spread, timeline, or another domain-specific form.
Type voice: where the personality lives.
Color behavior: dominant neutrals, accent role, and functional states.
Material language: ink, paper, pixels, metal, photography, map, or no metaphor.
Motion grammar: spring, glide, snap, reveal, continuity, or stillness.
Signature moment: one product-specific visual or interaction idea.
Main risk: what could make this direction less usable.
```

The six design dimensions are: page silhouette, type voice, color behavior, material language, motion grammar, and signature moment. Any two variants must differ in at least four. Avoid presenting near-duplicates as separate directions.

### 4. Implement Controlled Variants

Keep shared product behavior in reusable code where practical. Isolate each design in a separate route, directory, entry point, or theme module so variants do not leak visual rules into one another.

Keep constant:

- information and data values
- primary actions and state transitions
- empty, loading, error, success, selected, disabled, and focus behavior
- content length and language
- target viewport sizes
- technical stack and dependency policy

Allow each direction to recompose the interface for mobile. Equal behavior does not require identical layout.

### 5. Route Visual Assets Carefully

Read [visual-assets.md](references/visual-assets.md) when any direction needs photography, generated cartography, textures, illustration, or another bitmap.

Keep interface text, controls, state, and data in HTML or native components. Generated images may provide subject matter, atmosphere, material, or spatial context; they must not become screenshots of fake UI.

### 6. Build the Comparison Surface

Create a useful comparison harness when implementation is requested:

- left and right variant selectors
- independent open links for full-size inspection
- one-sentence thesis and risk for each selected direction
- the same viewport dimensions for both previews
- a compact usage-boundary matrix
- links to screenshots and generated-asset provenance

Do not force four tiny previews into one viewport. Prefer selectable two-up comparison plus independent full-size pages.

### 7. Verify Before Scoring

Read [comparison-scorecard.md](references/comparison-scorecard.md). Verify each variant at desktop and mobile sizes before assigning scores.

For every variant:

- capture desktop around 1440 x 900 and mobile around 390 x 844
- check console errors, failed resources, and horizontal overflow (run `verify_frontend.py` per variant; if python `playwright` is missing it only does a static audit, so use the `playwright` skill for the rendered checks)
- exercise the same critical interactions
- verify focus, keyboard, dialog, filter, selection, acknowledgement, and recovery states where relevant
- confirm generated assets are nonblank, correctly cropped, optimized, and readable behind overlays
- make at least one evidence-based refinement pass

Do not select a winner from a single desktop screenshot.

### 8. Recommend by Context

Name the strongest direction for the product's actual operating context, not the most visually dramatic screenshot. It is valid for different directions to win different categories such as long-session use, emergency response, spatial reasoning, brand memorability, or delivery speed.

Read [nightline-case-study.md](references/nightline-case-study.md) when a concrete worked example would help.

### 9. Hand Off the Winner

Once the user picks a direction, read [handoff-to-production.md](references/handoff-to-production.md): deliver tokens, type scale, component inventory, layout recipes, asset manifest, and rejected-direction notes to `advanced-frontend-design`. The lab does not build the production page and does not ship the comparison harness.

## Guardrails

- Do not confuse style names with product strategy.
- Do not average several visual directions into a fashionable hybrid.
- Do not change copy or data to make one version look better.
- Do not use paid or freemium resources by default.
- Do not generate imagery when CSS, existing assets, or real product media is more appropriate.
- Do not put all variants in one component with a few color variables if their silhouettes should differ.
- Do not ship the comparison harness as the production product.

## Completion Format

Report:

- the shared product contract
- direction names, theses, signatures, and risks
- implementation and comparison entry points
- generated asset paths, prompts, and optimized versions when used
- browser sizes and interactions verified
- recommendation by operating context, including why other directions lost

## 变更记录 / Changelog

- `2026.11.12`: added when-to-use and related-skill sections, Chinese trigger phrases, the explicit list of six design dimensions, a handoff step and `references/handoff-to-production.md`; replaced the stale `imagegen` reference with `local-image-generator`; replaced Windows `Y:\` paths in the case study with this machine's paths; pointed per-variant technical checks at `verify_frontend.py`.
- `2026.07.24`: initial version.
