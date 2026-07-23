# Meta Ads analysis reference

## Metric hierarchy

1. Revenue, purchases, subscriptions, or qualified leads.
2. A validated deep-funnel event such as registration complete or core experience entry.
3. A qualified-visit event based on an intentional interaction.
4. Landing page views.
5. Link clicks, CTR, and CPM as diagnostic metrics.

Never promote a diagnostic metric above an available business outcome.

## Core calculations

- CTR = clicks / impressions.
- Link CTR = link clicks / impressions.
- CPC = spend / clicks.
- Cost per link click = spend / link clicks.
- CPM = spend / impressions * 1000.
- LPV rate = landing page views / link clicks.
- Cost per LPV = spend / landing page views.
- Qualified rate = qualified events / landing page views.
- Cost per qualified event = spend / qualified events.
- Error rate = page error events / landing page loads.

## Confidence guidance

Use these as reporting guardrails, not universal statistical laws:

- Under 1,000 impressions or under 50 LPVs: directional only.
- Under 20 deep events: insufficient for a stable winner.
- Large delivery imbalance can reflect auction preference rather than proven business value.
- If one ad consumes over 80% of a treatment campaign's spend, label the treatment result confounded by creative allocation.
- A statistically different observed rate is not a causal treatment result when targeting, placements, creative mix, or delivery differ.
- Compare the same dates and attribution settings.
- For rate comparisons, report raw numerator and denominator with the percentage.
- Require downstream quality before scaling a cheap-traffic winner.

## Pixel event classification

- Diagnostic: page view, landing load, A/B assignment.
- Engagement: compare, video start after user action, zone click.
- Intent: selection, interaction-page load, core-story entry, outbound business action.
- Conversion: registration, lead, checkout, purchase, subscription.
- Negative: page error, failed load, immediate exit.

Confirm trigger semantics before classifying custom event names. Prefer a single deduplicated `QualifiedVisit` event when several interactions express the same funnel stage.

Pixel API event totals are event counts, not unique users. Use deduplicated sessions or event IDs before calculating user conversion rates. Inspect hourly concentration: a negative event concentrated in one hour is more consistent with a deployment or environment incident than persistent traffic quality.

## Breakdown priorities

When an AI/Advantage treatment has low CPM but weak CTR, request these breakdowns before blaming the treatment globally:

1. `publisher_platform` and `platform_position`.
2. age and gender.
3. country or region.
4. device platform.

Then compare the same creative across treatment groups.


## Recommendation language

- `Scale candidate`: efficient on a validated outcome with adequate sample.
- `Keep collecting`: promising but under-sampled.
- `Investigate`: tracking, delivery, landing-page, or audience anomaly.
- `Stop candidate`: materially inefficient on the primary outcome with adequate sample. This is not authorization to pause it.
