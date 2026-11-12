# Browser Quality Gate

Apply this gate to every frontend implementation or review. Use Playwright or available browser tooling and revise the code after inspection.

## Required Viewports

Test at minimum:

- desktop around 1440 x 900
- mobile around 390 x 844

Add an intermediate tablet or narrow-desktop viewport when the layout has sidebars, dense tables, split panes, or complex navigation.

## Visual Inspection

- Capture a full-page screenshot at desktop and mobile sizes.
- Confirm the first viewport communicates the product, subject, or primary task.
- Check that the next section or continuation is discoverable where appropriate.
- Check type hierarchy, line length, wrapping, contrast, image crops, and visual balance.
- Confirm text and controls do not overlap, clip, or escape their containers.
- Confirm repeated UI has stable dimensions and does not shift on hover, loading, or label changes.
- Confirm mobile is recomposed for priority and reachability, not merely stacked.
- Scan the palette for purple-blue, slate, beige, brown-orange, or single-hue dominance and justify or revise it.
- Count rounded panels. If most sections look like cards, remove containers and restore page-level composition.

## Interaction Inspection

Exercise the critical path and all visible controls that affect it:

- navigation and back/close behavior
- forms, validation, submit, success, and recovery
- menus, dialogs, tabs, accordions, filters, and pagination
- hover, focus-visible, active, selected, disabled, and loading states
- keyboard navigation and escape behavior
- empty, error, offline, permission, and no-results states when relevant
- reduced-motion behavior

## Technical Inspection

- Check the browser console for errors and failed asset requests.
- Check horizontal overflow at every tested viewport.
- Confirm images have stable dimensions and meaningful alt behavior.
- Confirm controls have accessible names and visible focus.
- Confirm color contrast is reasonable for normal text and state indicators.
- Confirm motion does not block interaction or cause layout shifts.
- Confirm the page loads with the project's normal command and route.

For canvas, WebGL, or 3D work, also inspect actual canvas pixels at desktop and mobile sizes, confirm the scene is nonblank and correctly framed, and verify interaction or animation over time.

## Automated First Pass

Run `python3 scripts/verify_frontend.py <file-or-url>` (path relative to this skill) before manual inspection. With python `playwright` installed it captures 1440x900 and 390x844 screenshots and reports console errors, horizontal overflow, images without alt, and unnamed controls. Without it, it falls back to a static HTML audit and says so; that fallback proves nothing about layout, overflow, or console health, so still use the browser tooling (`playwright` or `playwright-interactive` skills) for the visual and interaction checks below.

## Composition Lessons from the A/B Tests

Evidence: `frontend-design-ab-test/comparison-report.md` (same Nightline task, advanced vs standard skill). The standard output was polished and fully functional, yet scored lowest on anti-template quality (3.5 vs 5.0) because of its structure, not its styling.

- **Default-structure anti-pattern:** top nav + hero + row of four equal stat cards + map card + list card. Check the page skeleton, not the palette. If you can describe the page with that sentence, recompose it.
- **Work-surface first:** for operational and tool pages, the first viewport is the work surface (map, queue, status, primary action), not a hero. Delete the hero unless the page is brand-led. Test: in ten seconds, can an operator say what is at risk and what to do next?
- **Metrics as a status strip or a side column, not four boxed cards.** Ruled rows, one shared baseline, tabular numerals. Cards are for objects users open.
- **Status and action live in the same row** as the item they affect (severity, time, location, action). Do not make users hop between a summary and a detail card.
- **Mobile is recomposed, not stacked.** Concrete moves seen in the winning version: the persistent side rail became a compact top rail, the map stayed first, four metrics became a 2x2 block, and alerts followed with their actions intact. For each page, write the one-line mobile order (what comes first, what collapses, what becomes a sheet) before coding.
- **Score the structure separately from the finish.** A clean, coherent, familiar dashboard is a legitimate baseline; keep it in comparisons and do not sabotage it. It loses on structure and domain specificity, not on craft.
- **State changes must be visible:** acknowledging, filtering, and dialog flows need an obvious before/after (status label, count, position change), verified in the browser rather than assumed from code.

## Evidence-Based Revision

After the first screenshot pass:

1. List the three highest-impact visual or UX defects.
2. Fix them in code.
3. Recapture the affected viewport or interaction.
4. Stop only when no blocking overlap, broken state, or incoherent hierarchy remains.

Report what was actually tested. If browser automation could not run, state that clearly and provide the most relevant manual verification command or route.
