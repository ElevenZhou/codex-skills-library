# Motion and Interaction

Motion earns its place by doing one of four jobs (see `component-sources.md`): continuity, feedback, entry hierarchy, or one signature moment. Everything below is dependency-free. Spring-physics library references (Kinetics): see `frontend-web-tools-comparison-20260718.md`.

## Principles

- **One grammar per product.** Pick spring, glide, snap, or still (see `design-directions.md`) and keep it.
- **Durations.** Press/hover feedback 80-150ms. Small state change (toggle, tab, tooltip) 150-220ms. Panel/dialog/page-region entry 220-350ms. Large choreographed entry up to 600ms, once. Exits are ~30% faster than entries. Operations tools: stay at the low end.
- **Easing.** Entering elements: ease-out (decelerate). Leaving: ease-in. Moving between positions: ease-in-out. Springs (overshoot) only for playful or direct-manipulation moments; never on data, tables, or error messages.
- **Stagger.** 30-60ms per item, cap total at ~400ms (limit to first 8-10 items; the rest appear together).
- **Animate only `transform` and `opacity`** (compositor-friendly). Avoid animating `width/height/top/left/box-shadow/filter: blur` on large areas. For height reveals use the grid-rows trick below. Use `will-change` only briefly, on elements about to animate.
- **No layout shift.** Reserve space; animate with transforms from the final layout position.
- **Reduced motion.** Honor `prefers-reduced-motion: reduce` by removing movement and parallax, keeping instant state changes and (optionally) short opacity fades. Never hide content behind an animation that will not run.
- **Never block input.** Interactions stay usable during animations; no animation gates a click.

## 1. Tokens and Reduced-Motion Reset

```css
:root {
  --dur-fast: 120ms; --dur-base: 200ms; --dur-slow: 320ms;
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-in: cubic-bezier(0.64, 0, 0.78, 0);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);   /* fallback overshoot */
}
@supports (transition-timing-function: linear(0, 1)) {
  :root { --ease-spring: linear(0, 0.25, 0.63, 0.92, 1.05, 1.08, 1.04, 0.99, 1, 1); }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important; animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important; scroll-behavior: auto !important;
  }
}
```

(The `!important` here is the one accepted use: it is a global user-preference override.)

## 2. Press and Hover Feedback

```css
.btn { transition: transform var(--dur-fast) var(--ease-out), background-color var(--dur-fast); }
@media (hover: hover) { .btn:hover { transform: translateY(-1px); } }
.btn:active { transform: translateY(0) scale(0.97); transition-duration: 60ms; }
```

Gate hover with `(hover: hover)` so touch devices do not get stuck hover states.

## 3. Spring-like Entry (linear() with fallback)

```css
.pop { animation: pop var(--dur-slow) var(--ease-spring) both; }
@keyframes pop { from { opacity: 0; transform: translateY(8px) scale(0.96); } }
```

`from` with only changed properties animates from those values to the element's natural state.

## 4. Scroll Reveal with Stagger (IntersectionObserver)

```html
<ul class="reveal-group"><li style="--i:0">A</li><li style="--i:1">B</li></ul>
```
```css
.js .reveal { opacity: 0; transform: translateY(12px); }
.js .reveal.in { opacity: 1; transform: none;
  transition: opacity 400ms var(--ease-out), transform 400ms var(--ease-out);
  transition-delay: calc(min(var(--i, 0), 8) * 45ms); }
```
```js
document.documentElement.classList.add('js');           // content stays visible without JS
const els = document.querySelectorAll('.reveal');
if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) {
  els.forEach(e => e.classList.add('in'));
} else {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });
  els.forEach(e => io.observe(e));
}
```

## 5. Number Count-Up

```js
function countUp(el, duration = 900) {
  const end = parseFloat(el.dataset.value), dec = (el.dataset.value.split('.')[1] || '').length;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;   // DOM already holds the final text
  const t0 = performance.now();
  const tick = (t) => {
    const p = Math.min((t - t0) / duration, 1), eased = 1 - Math.pow(1 - p, 3);
    el.textContent = (end * eased).toLocaleString(undefined, { minimumFractionDigits: dec, maximumFractionDigits: dec });
    if (p < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}
// <span class="num" data-value="96.4">96.4</span>   .num { font-variant-numeric: tabular-nums; }
```

Start it from the IntersectionObserver callback so it runs when visible. Keep the final number in the markup for no-JS and screenshots.

## 6. View Transitions

Same-document (state changes, list-to-detail):

```js
function go(update) {
  if (!document.startViewTransition || matchMedia('(prefers-reduced-motion: reduce)').matches) return update();
  document.startViewTransition(update);
}
```
```css
.card-thumb { view-transition-name: hero; }   /* names must be unique at transition time */
::view-transition-old(root), ::view-transition-new(root) { animation-duration: 200ms; }
```

Multi-page (same origin): `@view-transition { navigation: auto; }`. Browser support is uneven; both are progressive enhancements, never required for function.

## 7. Scroll-Driven Progress (CSS only)

```css
@supports (animation-timeline: scroll()) {
  .progress { transform-origin: 0 50%; animation: grow linear both; animation-timeline: scroll(root); }
  @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
}
```

## 8. Height Reveal Without Animating Height

```css
.panel { display: grid; grid-template-rows: 0fr; transition: grid-template-rows var(--dur-base) var(--ease-out); }
.panel[data-open="true"] { grid-template-rows: 1fr; }
.panel > .inner { overflow: hidden; min-height: 0; }
```

Toggle `data-open` and `aria-expanded` together; hide closed content from tab order with `inert` on `.inner`.

## 9. Dialog Entry with `@starting-style`

```css
dialog[open] { opacity: 1; transform: none; transition: opacity var(--dur-base), transform var(--dur-base) var(--ease-out); }
dialog { opacity: 0; transform: translateY(8px); }
@starting-style { dialog[open] { opacity: 0; transform: translateY(8px); } }
dialog::backdrop { background: rgb(0 0 0 / 0.4); }
```

Use native `<dialog>` + `showModal()` for focus trapping and Escape. Exit animation needs `transition-behavior: allow-discrete` on `display`/`overlay`; skip it if support matters more than polish.

## 10. Skeleton Shimmer

```css
.skeleton { background: linear-gradient(90deg, #0000000d 25%, #0000001a 50%, #0000000d 75%) 0 0 / 200% 100%;
  animation: shimmer 1.4s linear infinite; border-radius: 4px; }
@keyframes shimmer { to { background-position: -200% 0; } }
```

Give skeletons the final element's dimensions. Under reduced motion the global reset freezes it into a flat block, which is the right result.

## Checklist Before Shipping Motion

- Can each animation be described in one sentence with its job?
- Does it run at 60fps on a mid-range phone, and animate only transform/opacity?
- Does everything still work and read correctly with motion off?
- Is there more than one "signature" effect? Remove all but one.
