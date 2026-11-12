# Review Rubric

Score each axis 0-5. The scale extends `frontend-design-lab/references/comparison-scorecard.md` (1-5) by adding 0 for "absent or broken". Verify before scoring; support every score with one concrete observation. Do not total blindly: weight by page class (see bottom).

## Scale

- **0**: absent or broken; the axis cannot be assessed because the thing does not work
- **1**: fails the product task or contains blocking defects
- **2**: usable only with significant redesign
- **3**: competent but generic, incomplete, or weakly matched to the domain
- **4**: strong, coherent, production-credible with minor limitations
- **5**: exceptional fit, clear authorship, verified polish

## Axes: what to look for

### 1. Generic / AI-template tells
Evidence of a default structure rather than a decision.
- Structure: centered hero + three/four equal feature or stat cards + CTA band; hero followed by generic dashboard mockup; everything a rounded card; cards inside cards.
- Surface: purple-blue gradient, glassmorphism everywhere, glow, decorative blobs, pill badges, emoji or identical icon-in-circle feature blocks, version/BETA eyebrows.
- Swap test: replace the logo with an unrelated one; does anything change? If not, score 2 or lower.
- Cross-check the ban list in `taste-skill` section 9 (AI Tells).
- Score 4-5 needs a recognizable domain decision (silhouette, material, type voice) and a signature moment tied to the subject.

### 2. Hierarchy
- Squint test: first/second/third noticed elements match the page's job.
- One primary action per view; primary vs secondary visually distinct.
- Operational pages: status, risk and next action in the first viewport; no hero consuming it.
- Group proximity: related items closer than unrelated ones.

### 3. Typography
- Distinct display/body roles or deliberate single-family choice; weights used for hierarchy, not decoration.
- Line length 45-75 Latin / 25-40 CJK; body size at least 16px mobile; line-height per `states-and-a11y.md` section 5.
- Numerals tabular in data. No letter-spacing on CJK. Correct `lang`.
- Heading scale is consistent and not oversized for its container; no all-caps paragraphs.
- Font delivery: remote CDN or heavy CJK web font flagged by the script.

### 4. Color and contrast
- Defined roles: neutrals, one accent, functional status colors. Dominant single-hue or purple-blue/slate/beige sameness without contrast is a defect.
- Text 4.5:1 (3:1 large); UI and focus indicators 3:1; status never by color alone.
- Both themes if offered. Accent used for action and signal, not decoration everywhere.
- Do not guess contrast from a screenshot when the exact values are readable in code; compute them.

### 5. Spacing and rhythm
- A visible spacing scale (4/8-based); consistent gutters; alignment to a grid; no orphan gaps or accidental collisions.
- Rhythm varies deliberately (dense data zone vs breathing hero) instead of uniform generous padding everywhere.
- Density fits the page class: tools dense and calm; editorial spacious.

### 6. Responsive
- Checked at 1440x900 and 390x844 at minimum; intermediate width when sidebars or tables exist.
- Mobile recomposed (reordered, collapsed, re-formed), not just stacked. Primary action reachable.
- No horizontal overflow outside intentional scroll containers; no clipped text; images keep ratio.
- Touch targets at least 24px (aim 44); safe-area handling on mobile web.

### 7. Interaction states
- Hover, focus-visible, active, disabled, selected, loading, empty, error, success, offline, permission.
- Forms: labels, validation timing, preserved input, submit states.
- Feedback for every action; destructive actions confirmed; undo where cheap.
- Motion has a job; respects `prefers-reduced-motion`; no layout shift on hover or load.

### 8. Accessibility
- Landmarks and heading order; `lang`, title, viewport; alt text; names for icon buttons and links.
- Full keyboard path; visible focus; dialogs trap and restore focus; no keyboard traps.
- Zoom to 200% without loss; screen-reader sanity on the critical path (say if not tested).

### 9. Performance
- Weight: images oversized or unoptimized (prefer WebP/AVIF, explicit dimensions), CJK web fonts unsubsetted, large blocking scripts, remote CDN dependencies.
- Layout stability (no shift), animation on transform/opacity only, heavy effects (large blur, backdrop-filter stacks) on low-end devices.
- Say "not measured" unless the browser path or Lighthouse-like data was actually available.

### 10. Content realism
- Real, specific, locale-appropriate content: believable names, messy numbers (47.2% not 99.9%), concrete verbs, no "Lorem ipsum", no startup-slop names, no fake logos or testimonials.
- Text length variety tested: long names, empty values, wrapped labels.
- Images show the actual subject; no div-built fake screenshots; generated images contain no fake UI text.
- Copy explains the product, not the interface (no visible instructional filler).

## Weighting by Page Class

| Page class | Weight up | Weight down |
| --- | --- | --- |
| Product / operations | Hierarchy, interaction states, accessibility, responsive | Generic tells beyond structure, motion |
| Brand / landing / portfolio | Generic tells, typography, content realism, performance | Dense-state coverage |
| Commerce | Interaction states, performance, accessibility, content realism | Experimental layout |
| Editorial | Typography, rhythm, performance | Interaction states |

## Verdict Bands (average of weighted axes)

- below 2.0: do not ship; redesign direction
- 2.0-3.0: rework structure, then re-review
- 3.0-4.0: ship after P0/P1 fixes
- 4.0 and above: ship; P2 as backlog

Any P0 overrides the band.
