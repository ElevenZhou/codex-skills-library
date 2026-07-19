# Component Source Routing

Use this reference before adding dependencies or borrowing component patterns.

## General Rule

Start with the repository. Reuse its components, tokens, icons, animation package, and accessibility conventions. Add a dependency only when it removes meaningful implementation risk or supplies a well-tested primitive the project lacks.

## Route by Page Type

| Page type | Preferred base | Optional expression layer | Avoid |
| --- | --- | --- | --- |
| SaaS product or dashboard | Existing system, Mantine, or Radix/shadcn primitives | Small CSS or current motion library | Marketing-style feature cards and ornamental hero sections |
| Internal operations tool | Existing enterprise library, Ant Design, Mantine | Functional transitions only | Decorative animation, hidden controls, low-density layouts |
| Landing or campaign page | Semantic local components | Magic UI, Animata, Animate UI, CSS Text Effects, Kinetics | Combining several animation libraries or copying a full template |
| Portfolio or creative page | Local semantic layout and media components | React Bits free set, Animata, Kinetics | Effects that obscure the actual work |
| Content or editorial site | Native layout, existing CMS components | CSS text/image transitions | Dashboard cards used as article structure |

## React Decisions

- Use Radix Primitives when accessibility and custom visual authorship matter.
- Use shadcn/ui as source-owned primitives, then replace default radius, color, spacing, typography, and composition.
- Use Mantine when the app needs a broad, reliable suite of forms, overlays, notifications, and hooks.
- Keep Ant Design or MUI when the repository already depends on them; theme and compose them instead of fighting the library.
- Use the project's installed motion library before adding another one.

## Vanilla, Vue, Svelte, and Other Stacks

- Prefer native semantic HTML and CSS for simple components.
- Use the framework's established accessible component library when present.
- Translate a visual idea rather than porting React-specific source line for line.
- Keep state, focus management, and keyboard behavior native to the target framework.

## Animation Decisions

Add motion only when it serves one of four purposes:

1. explain spatial or state continuity
2. provide immediate interaction feedback
3. establish hierarchy during entry
4. create the single signature moment

For simple transitions, use CSS. For component lifecycle or gesture work, use the existing framework motion package. Use Kinetics as a motion-behavior reference. Borrow CSS Text Effects only for critical display text, never body copy.

## Copy-Paste Intake Checklist

Before accepting an external component:

- confirm its license and free status
- remove unused dependencies and decorative wrappers
- replace hard-coded colors, spacing, and radii with project tokens
- verify keyboard navigation and focus behavior
- add loading, empty, disabled, and error states where applicable
- test long text, missing media, and narrow containers
- confirm it still fits the chosen visual thesis after restyling
