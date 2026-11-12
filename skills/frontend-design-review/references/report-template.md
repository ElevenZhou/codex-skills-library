# Review Report Template

Fill every section. Delete a section only if it is truly empty, and say so ("No P0 findings"). Evidence must be a selector, `file:line`, a screenshot region, or a script output line. A finding without evidence is a guess; move it to "Not verified".

## Full form

```markdown
# Design Review: <page or product name>

**Target**: <file / URL / screenshot set>   **Page class**: product | brand | commerce | editorial
**Reviewed**: <date>   **Viewports checked**: <e.g. 1440x900, 390x844>   **Method**: static script | browser | screenshot only

## Verdict
<Ship / Ship after P0+P1 / Rework. One or two sentences on why, naming the single biggest problem.>

## Scorecard (0-5, see references/review-rubric.md)
| Axis | Score | One concrete observation |
| --- | ---: | --- |
| Generic / AI-template tells | | |
| Hierarchy | | |
| Typography | | |
| Color and contrast | | |
| Spacing and rhythm | | |
| Responsive recomposition | | |
| Interaction states | | |
| Accessibility | | |
| Performance | | |
| Content realism | | |
| **Weighted total** | | weights used: <list, from the page-class table> |

## Findings

### P0 - blocking (broken, inaccessible, or fails the page's job)
**F1. <short title>**
- Evidence: <selector | file:line | screenshot region | script line>
- Problem: <what is wrong and who it hurts>
- Fix: <specific change, with values where possible>
- Effort: S | M | L

### P1 - should fix before release
(same fields)

### P2 - polish
(same fields)

## Keep
<2-4 things that work and must survive the rework. Reviews that only list faults cause regressions.>

## Not verified
<What you could not check and why: no browser, no real data, no keyboard pass, third-party font licences, etc.>

## Next step
<One recommended action. Say whether code changes need the user's go-ahead; this skill does not rewrite code unless asked.>
```

## Severity rules
- **P0**: content unreadable or unreachable, horizontal overflow on mobile, keyboard trap, missing focus path, console errors that break function, contrast failure on primary text or actions, the main task not completable.
- **P1**: weak hierarchy on the primary view, missing empty/loading/error states, unnamed controls, template structure that hides the product, inconsistent type or spacing scale.
- **P2**: motion polish, icon consistency, copy tone, minor alignment, optional enhancements.

Effort: **S** under 1 hour, **M** half a day, **L** a day or more. Merge duplicates: one root cause is one finding.

## Short chat form (for quick reviews)

```markdown
**Verdict**: <Ship / Ship after fixes / Rework> - <one sentence>
**Scores**: Generic <n> | Hierarchy <n> | Type <n> | Color <n> | Rhythm <n> | Responsive <n> | States <n> | A11y <n> | Perf <n> | Content <n>
**P0**: <F1 title (evidence) - fix> ...
**P1**: <titles with evidence, one line each>
**P2**: <comma-separated titles>
**Keep**: <what works>
**Not verified**: <gaps>
```
