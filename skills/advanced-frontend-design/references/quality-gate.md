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

## Evidence-Based Revision

After the first screenshot pass:

1. List the three highest-impact visual or UX defects.
2. Fix them in code.
3. Recapture the affected viewport or interaction.
4. Stop only when no blocking overlap, broken state, or incoherent hierarchy remains.

Report what was actually tested. If browser automation could not run, state that clearly and provide the most relevant manual verification command or route.
