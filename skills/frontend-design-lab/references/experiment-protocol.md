# Controlled Experiment Protocol

Use this protocol to keep frontend design comparisons fair and useful.

## Shared Contract

Freeze these before implementation:

| Variable | Required decision |
| --- | --- |
| Audience | Who operates or consumes the interface |
| Job | What they must understand or complete |
| First screen | What must be visible within ten seconds |
| Data | Exact values, labels, ordering, and content length |
| Actions | Primary, secondary, destructive, and recovery actions |
| States | Loading, empty, error, success, selected, disabled, focus |
| Stack | Framework, CSS strategy, component library, icon system |
| Assets | Existing, generated, licensed, and prohibited sources |
| Viewports | Desktop, mobile, and any domain-specific intermediate size |
| Acceptance | Accessibility, performance, console, and interaction checks |

## Existing Project Audit

Before redesigning, list:

1. **Preserve**: working behavior, architecture, brand equity, accessible components.
2. **Fix now**: problems that materially affect hierarchy, task speed, trust, responsiveness, or consistency.
3. **Defer**: improvements that do not affect the current design decision.
4. **Do not touch**: protected APIs, routes, business logic, and framework boundaries.

Prefer local upgrades over migrations. Reuse the current design system when it is coherent; replace only the rules causing the problem.

## Variant Matrix

Create a table before coding:

| Direction | Silhouette | Type voice | Color behavior | Material | Motion | Signature | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |

Require at least four meaningful differences between any two variants. A palette swap is not a separate direction.

## Implementation Isolation

Choose one structure that fits the repo:

- separate static directories for a small HTML experiment
- separate routes in an application
- separate theme modules plus different layout components
- feature-flagged variants when user testing requires shared deployment

Share data and behavior. Isolate visual composition, tokens, and direction-specific assets.

## Baseline Fairness

Include an existing or conventional version when useful, but do not sabotage it. Give every variant:

- the same functionality
- the same content completeness
- the same browser verification
- the same opportunity for one refinement pass

The purpose is to expose tradeoffs, not manufacture a predetermined winner.

## Comparison Harness

Prefer a selectable two-up surface with:

- labeled selectors
- full-size open links
- visible direction thesis and main risk
- stable equal preview sizes
- independent scrolling when necessary
- a usage-boundary matrix below the previews

On mobile, stack previews and retain independent open links. Contain wide comparison tables in a horizontal scroll region instead of overflowing the document.
