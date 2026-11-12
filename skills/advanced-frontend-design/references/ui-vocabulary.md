# UI Vocabulary: Name the Pattern, Then Specify It

Vague specs ("a nice dashboard section") make models fall back to the average layout. Naming the pattern precisely removes guesswork. This list is written from scratch for this skill; for the external idea it comes from, see NameThatUI in `frontend-web-tools-comparison-20260718.md`.

Use: pick the pattern, copy its **prompt phrase**, and fill the brackets. Pair every layout pattern with the states it needs (see [states-and-a11y.md](states-and-a11y.md)).

## Layout and Structure

| Pattern | Use when | Do not use when | Prompt phrase |
| --- | --- | --- | --- |
| Bento grid | A few heterogeneous highlights of unequal importance on a brand or overview page | Records that must be compared row by row | "Bento grid, 12-col, one 2x2 hero tile, tiles differ in content type (chart, image, quote), 8px radius, 16px gap" |
| Master-detail | List of records plus inspection of one at a time (mail, tickets, alerts) | Fewer than ~5 records or no per-record depth | "Master-detail: left list 360px with selected state, right detail pane, mobile = list then pushed detail with back button" |
| Sticky rail | Persistent local navigation or summary that must stay visible while content scrolls | Pages shorter than 2 viewports | "Sticky left rail 240px, `position: sticky; top: 0; height: 100dvh`, collapses to top bar under 768px" |
| Split pane | Direct comparison or edit/preview, resizable | Narrow mobile contexts | "Resizable split pane, drag handle with keyboard support (arrow keys), min 280px per pane" |
| Holy-grail app shell | Tools: header, sidebar, main, optional inspector | Content or marketing pages | "App shell: 56px top bar, 232px sidebar, scrolling main, 320px optional inspector drawer" |
| Ledger / data table | Dense comparable records with sort/filter | Fewer than 3 columns of data | "Ledger table, sticky header, tabular numerals right-aligned, row hover, zebra off, density toggle" |
| Kanban board | Items move through discrete stages | Stages with no real movement | "Kanban columns with WIP counts, drag handle plus keyboard move menu" |
| Timeline / activity feed | Chronological history, audits | Non-temporal data | "Vertical timeline, time on left rail, grouped by day, collapsible system events" |
| Stepper / wizard | Multi-step, order matters, partial progress must persist | Short forms (<6 fields) | "Stepper with numbered steps, current/complete/error states, save draft, back keeps values" |
| Accordion / disclosure | Secondary detail, FAQ, long settings | Primary content users need at once | "Accordion, one open at a time, chevron rotates, button headers with `aria-expanded`" |
| Tabs vs segmented control | Tabs switch sections of content; segmented control switches a view of the same data | Navigation between pages (use links) | "Segmented control: Day / Week / Month, same chart, selected pill with 2px ink underline" |

## Navigation and Command

| Pattern | Use when | Prompt phrase |
| --- | --- | --- |
| Command palette | Many actions, power users, keyboard-first tools | "Command palette on Cmd/Ctrl+K, fuzzy search, grouped results (Pages, Actions, Recent), arrow keys + Enter, Esc closes, focus trapped" |
| Breadcrumbs | Hierarchy deeper than 2 levels | "Breadcrumb trail, last item is current page and not a link, truncates middle items on mobile" |
| Bottom tab bar | Mobile apps/H5 with 3-5 top-level destinations | "Bottom tab bar 56px + safe-area inset, 4 items, icon + label, active item filled" |
| Mega menu | Large catalogues in commerce | "Mega menu opens on click and focus, 4 columns, featured image slot, Esc closes" |
| Skip link | Every page with repeated header/nav | "Skip to main content link, visible on focus only" |
| Pagination vs infinite scroll vs load more | Pagination for findable/bookmarkable records; load more for feeds; infinite scroll rarely | "Numbered pagination with page size selector and total count" |

## Feedback and State

| Pattern | Use when | Prompt phrase |
| --- | --- | --- |
| Empty state | A list/table/dashboard has no data yet | "Empty state: one-line explanation of why it is empty, one primary action, no illustration unless it carries meaning" |
| Skeleton | Loading structured content with predictable shape (>300ms) | "Skeleton matching final layout dimensions, shimmer disabled under reduced motion, no layout shift on swap" |
| Spinner / progress bar | Short unknown wait (spinner); known progress (bar) | "Determinate progress bar with percentage and cancel" |
| Toast | Low-stakes confirmation of an action that already happened | "Toast bottom-center, 4s, `role=status`, undo action, stack max 3; never for errors that need action" |
| Inline validation | Form field errors | "Error text under the field, linked via `aria-describedby`, shown on blur then on change, icon not color only" |
| Banner / callout | Page-level persistent status (offline, maintenance) | "Full-width banner below header, `role=alert` only if urgent, dismissible only if safe" |
| Confirmation dialog | Destructive or irreversible action | "Modal confirm: names the object being deleted, destructive button labeled with the verb, default focus on Cancel" |
| Optimistic UI + undo | Fast reversible actions (archive, like) | "Apply immediately, show Undo toast, roll back on failure with error message" |
| Focus ring | All keyboard-focusable controls | "`:focus-visible` 3px outline, offset 2px, 3:1 contrast against both adjacent colors" |
| Tooltip vs popover | Tooltip: short label for icon-only control; popover: interactive content | "Tooltip on hover AND focus, 500ms delay, `aria-describedby`; popover has its own focus handling" |

## Content and Data

| Pattern | Use when | Prompt phrase |
| --- | --- | --- |
| KPI strip | Few headline metrics in a ruled row, not four boxed cards | "Ruled status strip: label, value in tabular numerals, delta with sign and arrow, one sparkline max" |
| Sparkline | Trend at a glance beside a number | "Inline sparkline 80x24, no axes, last point marked, accessible text summary" |
| Data-ink chart | Real comparison needs | "Direct-labeled lines instead of legend, 1 accent + neutrals, gridlines at 8% opacity" |
| Pull quote / testimonial | Editorial trust building | "Pull quote with real name, role, company, and portrait; no five-star row" |
| Logo wall | Social proof with real customers only | "Monochrome logo row, 6 max, grayscale to color on hover" |
| Comparison table | Pricing/plans with 2-4 options | "Plan table, recommended column offset, feature rows grouped, sticky header on mobile via horizontal scroll container" |
| Avatar stack | Collaborators/participants | "Overlapping avatars, +N overflow chip, tooltip with names" |
| Badge vs tag vs chip | Badge: status/count; tag: classification; chip: user-applied filter (removable) | "Status badge: dot + text, never color alone" |

## Hero and Brand Moments (landing/editorial only)

| Pattern | Prompt phrase |
| --- | --- |
| Asymmetric split hero | "Left 7 cols headline + one CTA, right 5 cols real product/photo, crop bleeds off edge" |
| Editorial manifesto hero | "Poster-scale headline, no image, one supporting line, hint of next section visible" |
| Before/after slider | "Draggable divider, keyboard arrows, labeled both ends" |
| Scroll-pinned story | "Section pins for 3 steps, left text changes, right visual morphs; reduced motion = stacked" |
| Marquee | "Slow ticker for secondary content only, pauses on hover/focus, static under reduced motion" |

## Writing a Precise Component Spec

Fill in: pattern name, content (real, with lengths), states (default/hover/focus/active/disabled/loading/error/empty), responsive behavior (what moves, what hides, what changes form), keyboard behavior, motion (one phrase from [motion-interaction.md](motion-interaction.md)). If you cannot fill all eight, the pattern is not yet decided.
