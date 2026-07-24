---
name: meta-ads-analysis
description: Analyze Meta Ads accounts with the installed meta-ads CLI and Marketing API, including campaign/ad set/ad comparisons, creative winners, budget delivery, traffic quality, Pixel funnels, experiment uncertainty, anomalies, and evidence-backed recommendations. Use when Codex is asked for Meta/Facebook Ads performance analysis, account audits, AI-vs-control comparisons, Pixel event diagnosis, daily/weekly reporting, optimization recommendations, or expert advertising conclusions. This skill is read-only unless the user separately and explicitly authorizes an exact delivery status change.
---

# Meta Ads Analysis

Skill version: `2026.07.25`

Use `meta-ads` for authenticated reads and `scripts/analyze_report.py` for deterministic aggregation. Never print or persist access tokens.

## Workflow

1. Load credentials from a Git-ignored local environment file without echoing it.
2. Run `meta-ads --json doctor` and `meta-ads --json accounts list`; stop on account mismatch.
3. Discover active and paused campaigns, ad sets, and ads before interpreting IDs.
4. Export ad-level data because it preserves campaign, ad set, and ad dimensions:

```bash
mkdir -p reports
meta-ads --json reports export --level ad --date-preset last_7d --out reports/meta-ads-ad-last7d.json
python3 "$CODEX_HOME/skills/meta-ads-analysis/scripts/analyze_report.py" \
  reports/meta-ads-ad-last7d.json \
  --account-id act_ACCOUNT_ID --currency USD --timezone Asia/Shanghai \
  --window last_7d --markdown reports/meta-ads-analysis.md
```

Use `last_30d` for mature accounts. For newly launched tests, use `last_7d` and state the actual launch dates.

The current CLI may misparse `insights get --level ad` and silently fall back to campaign level. Prefer `reports export --level ad`. If direct insights are necessary, verify that returned rows contain `ad_id` and `ad_name`; never trust the requested level alone.

5. Query Pixel ownership and recency when traffic quality or conversion tracking matters:

```bash
meta-ads --json request get /BUSINESS_ID/owned_pixels \
  --fields id,name,last_fired_time,is_unavailable |
  jq '{ok, data: {data: .data.data}}'
```

Raw Graph paging URLs can contain the token. Always pipe raw requests through a projection that removes `paging` before displaying or saving output.

For JSON that has already been captured, sanitize it before inspection:

```bash
python3 "$CODEX_HOME/skills/meta-ads-analysis/scripts/sanitize_json.py" raw.json sanitized.json
```

6. Read [references/metrics.md](references/metrics.md) when comparing tests, interpreting Pixel events, or recommending budget changes.
7. Deliver findings in this order: executive conclusion, comparison table, funnel/Pixel quality, risks and uncertainty, next actions, data limitations.

## Analysis rules

- Compare campaigns with the same objective and optimization goal. Report other objectives separately.
- Audit experiment comparability before attributing causality: age, gender, country, placements, devices, audience expansion, optimization, attribution window, schedule, budget, and creative matrix must match.
- Calculate spend concentration by ad. A campaign whose top ad consumes nearly all spend is not a clean campaign-level treatment test.
- Pair the same creative across campaigns when possible. Distinguish an overall treatment effect from a creative-by-audience or creative-by-placement interaction.
- Treat `landing_page_view` as stronger than link clicks and clicks. Calculate LPV/link-click rate.
- Do not call a winner from CTR alone. Prefer cost per business outcome, then cost per qualified event, then cost per LPV.
- Use spend, impressions, conversions, launch time, and delivery imbalance to qualify confidence.
- Separate cheap reach from qualified traffic: a low CPM with poor CTR or high cost per LPV is not a win.
- Report frequency and flag fatigue only with supporting trend or repeated exposure.
- Treat Pixel `page_error` events as a quality guardrail, not a conversion.
- Never represent arbitrary engagement scores as revenue. Use `value` and `currency` only for real or defensible economic values.
- Identify missing attribution, conversion mappings, revenue, and downstream events explicitly.
- Check balance/payment risk and current-day delivery when the account appears to underspend, but separate unsettled intraday data from completed-day performance.
- Recommendations are advisory. Do not pause, activate, change budgets, targeting, bids, or creatives without exact user authorization.

## Required output

Include:

- Account ID, currency, timezone, analysis window, and data freshness.
- Spend, impressions, reach, frequency, CTR, CPC, CPM, link clicks, LPV, LPV rate, and cost per LPV.
- Campaign-level comparison and ad-level winners/losers with minimum-sample caveats.
- Experiment-integrity checks, top-ad spend concentration, and same-creative cross-campaign comparisons.
- Pixel last-fired status, event funnel, error events, and tracking gaps when available.
- A concise decision: keep collecting, investigate, scale candidate, or stop candidate. Mark it as a recommendation only.
