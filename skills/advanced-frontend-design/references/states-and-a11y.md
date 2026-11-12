# States, Accessibility, and Typography Baselines

Use as the checklist behind the "real states" requirement. Targets reference WCAG 2.2 AA unless stated.

## 1. State Matrix

Every data-bearing surface (list, table, card set, chart, form, detail pane) needs each row below, or an explicit note that it cannot occur.

| State | What the user must see | Common failure |
| --- | --- | --- |
| Loading (first) | Skeleton matching final layout; after ~10s, a message plus retry | Spinner on a blank page; layout jump on load |
| Loading (refresh) | Old data stays, subtle in-place indicator, timestamp "updated 12:04" | Content flashes to skeleton on every refetch |
| Empty (first use) | Why it is empty + the primary action to fill it | Blank area or "No data" |
| Empty (no results) | Echo the query/filters, one-click "clear filters" | Same screen as first-use empty |
| Error (recoverable) | What failed in plain words, what is preserved, Retry | Raw error codes; losing user input |
| Error (fatal/404/500) | Where they are, a way out (home, back, contact) | Dead end |
| Partial | Section-level error, rest of page works, "3 of 5 sources loaded" | One failed widget blanks the page |
| Offline / slow | Banner with queued-actions status; read cached data | Silent failure of writes |
| Permission denied | Say what is missing and who can grant it; do not hide the feature silently when discoverability matters | Generic "Something went wrong" |
| Success | Confirmation near the action; undo where reversible | Toast that disappears before it is read |
| Stale / conflict | "Changed by someone else", offer reload or merge | Overwriting silently |
| Disabled | Explain why (tooltip/helper text) when not obvious; keep focusable-by-description via `aria-disabled` if the reason matters | Gray control with no reason |

Also verify: long text (2x expected length, and a single unbroken token), missing image, zero/one/many items, very large numbers, and negative/zero/null values.

## 2. Forms

- Visible `<label>` for every field; placeholder is an example, not a label.
- Mark optional vs required consistently (prefer "optional" text over asterisks only).
- Correct `type`, `inputmode`, `autocomplete` (e.g. `autocomplete="email"`, `inputmode="numeric"`; Chinese mobile: `type="tel"` for phone, avoid `type="number"` for IDs and codes).
- Validate on blur, then live after first error. Error text adjacent to the field, tied with `aria-describedby`, plus `aria-invalid="true"`. On submit failure, focus the first invalid field and show a summary if more than 3 errors.
- Never clear user input on error. Preserve drafts for long forms.
- Submit button states: idle, submitting (disabled + label change, no double submit), success, failure.
- One primary action per view; destructive actions are visually and spatially separated.

## 3. Keyboard and Focus

- Everything operable by mouse is operable by keyboard; DOM order equals visual order. Do not use positive `tabindex`.
- Visible focus on every interactive element: `:focus-visible` outline at least 2px, 3:1 contrast against adjacent colors. Never `outline: none` without a replacement.
- Dialogs: focus moves in, is trapped, Esc closes, focus returns to the trigger. Native `<dialog>.showModal()` does this.
- Menus/tabs/listboxes: arrow keys move within, Tab leaves (roving tabindex). Command palette: Cmd/Ctrl+K opens.
- Skip link first in the DOM. Single `<main>`. Landmarks: header, nav, main, footer.
- Custom widgets: prefer native elements (`button`, `details`, `dialog`, `select`) over `div role=...`. Icon-only controls need `aria-label`.
- Live updates: `role="status"` (polite) for confirmations; `role="alert"` only for urgent errors.

## 4. Contrast, Color, Target Size

- Text contrast: 4.5:1 normal, 3:1 large (>=24px, or >=18.66px bold). UI components and focus indicators: 3:1.
- State is never color alone: add icon, text, or shape. Check status badges in grayscale.
- Touch targets: at least 24x24 CSS px (WCAG 2.2 AA floor), aim for 44x44 (Apple HIG) / 48dp (Material) on touch UIs, with 8px spacing between adjacent targets.
- Zoom: layout works at 200% zoom and 320px width without horizontal scroll (except data tables, maps, code in their own scroll container).
- Dark mode: re-check contrast; do not just invert; avoid pure white on pure black for body text.
- Images and media: meaningful `alt` (what it conveys, not "image of"); decorative `alt=""`; video with captions; no autoplay audio.

## 5. Typography Baselines

- Body 16px minimum on mobile (iOS zooms inputs below 16px). Line length 45-75 Latin characters, 25-40 CJK characters.
- Line-height: Latin body 1.5-1.65; headings 1.1-1.3. CJK body 1.7-1.9; CJK headings 1.3-1.5 (CJK glyphs fill the em box, so Latin-tight leading looks cramped).
- `font-variant-numeric: tabular-nums` for tables, prices, timers, KPI.
- Hierarchy through size + weight + color; limit to 2 families and 3-4 weights.

## 6. i18n and CJK

- Set `lang` on `<html>` (`zh-CN`, `zh-TW`, `ja`, `ko`) and on mixed-language fragments; it selects the correct Han glyph variants.
- **No `letter-spacing` on CJK text** (breaks rhythm). Zero it on elements that mix Latin small caps with CJK. Tracking is for short uppercase Latin labels only.
- No italic or synthetic bold for CJK; use a real bold weight or a heavier font.
- Line breaking: `line-break: strict` for body, `word-break: normal`, `overflow-wrap: anywhere` for URLs and tokens. Avoid `word-break: break-all` on mixed text.
- Punctuation squeeze: use `text-spacing-trim: space-first` where supported (progressive enhancement); `hanging-punctuation` is Safari-only. Use full-width Chinese punctuation, half-width only inside Latin/number runs.
- Latin-CJK spacing: a thin gap between Chinese and Latin/digits is conventional; use `text-autospace: normal` where supported instead of typing spaces.
- Allow text expansion: German/Russian +30%, Chinese often 30-50% shorter than English. Do not fix widths on buttons and labels.
- Use `Intl.DateTimeFormat`, `Intl.NumberFormat`, `Intl.RelativeTimeFormat`, `Intl.PluralRules` rather than hand-built strings. Avoid concatenating translated fragments.
- Do not embed text in images.

## 7. RTL Notes

- Use logical properties: `margin-inline-start`, `padding-inline`, `inset-inline-end`, `text-align: start`, `border-start-start-radius`.
- Set `dir="rtl"` on `<html>` (or per fragment, `dir="auto"` for user content). Flip directional icons (arrows, back, progress), not logos, media controls, or numerals.
- Test a mixed-direction string (Arabic with a Latin brand name or number) for bidi order; wrap with `<bdi>` when inserting user content.
- Flexbox/grid already follow direction; hard-coded `left/right`, `translateX`, and `background-position: left` do not.

## 8. Automated Check vs Human Check

`scripts/verify_frontend.py` catches missing alt, unnamed controls, missing `lang`/viewport/title, heading skips, and (browser mode) overflow and console errors. It does not measure contrast, focus order, screen-reader output, or content quality. Do those by hand: Tab through the page, zoom to 200%, switch the OS to reduced motion, and read the page with a screen reader (VoiceOver on macOS) for the critical path.
