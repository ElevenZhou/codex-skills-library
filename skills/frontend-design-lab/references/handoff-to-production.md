# Handoff to Production

The lab ends with a chosen direction. Production work then belongs to `advanced-frontend-design`, which owns the design contract, states, motion, accessibility, and the browser quality gate. The comparison harness is not shipped (see Guardrails in `SKILL.md`).

## When to Hand Off

Hand off only after: verified desktop and mobile screenshots for every variant, a scorecard with evidence, and a recommendation by operating context. If the user has not chosen, present the recommendation and ask before building.

## Artifacts to Hand Over

Create a `handoff/` folder (or section of the report) with these items. Keep each short.

| Artifact | Contents | Source in the lab |
| --- | --- | --- |
| Direction brief | Name, one-sentence visual thesis, page silhouette, signature moment, main risk and its mitigation | Variant matrix in `experiment-protocol.md` |
| Shared product contract | Audience, job, first-screen goal, fixed data, actions, states, viewports, acceptance criteria | Contract written in step 2 |
| Design tokens | Semantic color roles (neutrals, one accent, status colors) with hex values, contrast results, spacing scale, radius, border, shadow, motion durations/easings | The winning variant's CSS custom properties, cleaned up |
| Type scale | Families (and where to get them, free license noted), sizes, weights, line-heights, numeral style; CJK stack if relevant | Winning variant |
| Component inventory | Each component actually used, with variants and states shown in the lab (button, filter, row, dialog, badge, etc.), and which are native vs custom | Winning variant markup |
| Layout recipes | Desktop grid and the explicit mobile recomposition order (what moves, collapses, becomes a sheet) | Screenshots plus notes |
| Asset manifest | Original, optimized file, prompt, sizes, licenses, crop and overlay rules | Generated-asset provenance from `visual-assets.md` |
| Rejected-direction notes | For each losing direction: why it lost, what it did better, and which single idea (never the whole signature) might be borrowed | Scorecard and category winners |
| Known gaps | States not yet built, content placeholders, risks measured in the lab | Verification log |
| Evidence | Screenshot paths, console/overflow results, interaction results | Browser verification |

## Rules for the Transfer

1. Hand over the winner's design logic, not the harness. Remove variant selectors, comparison pages, and losing-direction CSS.
2. Do not merge rejected directions back in. A borrowed idea must be justified against the winner's thesis and stated in one sentence.
3. Convert lab CSS into the project's real token system. If the repository already has tokens, map the direction onto them instead of adding a second system.
4. Replace stubbed data and simulated interactions with the real data layer; keep the lab states as the acceptance list.
5. Re-run the full state matrix (`advanced-frontend-design/references/states-and-a11y.md`). Lab variants often cover only the critical path.
6. For Chinese-language products, apply `advanced-frontend-design/references/chinese-product-ui.md` (font delivery, density, formats) before locking the type scale.
7. Re-verify with `advanced-frontend-design/scripts/verify_frontend.py` plus real browser checks; the lab's earlier screenshots do not count for production code.

## Suggested Handoff Prompt

```text
Use $advanced-frontend-design to implement the chosen direction "[name]" in [project path].
Inputs: handoff/ folder (direction brief, tokens, type scale, component inventory, layout recipes, asset manifest, rejected-direction notes).
Preserve: [stack, routes, business logic]. Free/open-source only.
Acceptance: full state matrix, 1440x900 and 390x844, verify_frontend.py clean of errors, one refinement pass from screenshots.
```

## After Implementation

Run `frontend-design-review` on the production page for a second-pass critique; compare against the lab recommendation to confirm the direction survived real content.
