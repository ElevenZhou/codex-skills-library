#!/usr/bin/env python3
"""Aggregate a meta-ads ad-level JSON export without handling credentials."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def number(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def action_map(row):
    return {item.get("action_type"): number(item.get("value")) for item in row.get("actions", [])}


def aggregate(rows, key_fields):
    groups = defaultdict(lambda: {
        "spend": 0.0, "impressions": 0.0, "reach": 0.0, "clicks": 0.0,
        "link_clicks": 0.0, "landing_page_views": 0.0, "rows": 0,
    })
    for row in rows:
        key = tuple(row.get(field, "") for field in key_fields)
        item = groups[key]
        actions = action_map(row)
        item["spend"] += number(row.get("spend"))
        item["impressions"] += number(row.get("impressions"))
        item["reach"] += number(row.get("reach"))
        item["clicks"] += number(row.get("clicks"))
        item["link_clicks"] += actions.get("link_click", number(row.get("inline_link_clicks")))
        item["landing_page_views"] += actions.get("landing_page_view", 0)
        item["rows"] += 1

    result = []
    for key, item in groups.items():
        impressions = item["impressions"]
        spend = item["spend"]
        clicks = item["clicks"]
        links = item["link_clicks"]
        lpv = item["landing_page_views"]
        reach = item["reach"]
        record = {field: value for field, value in zip(key_fields, key)}
        record.update(item)
        record.update({
            "frequency": impressions / reach if reach else None,
            "ctr_pct": clicks / impressions * 100 if impressions else None,
            "link_ctr_pct": links / impressions * 100 if impressions else None,
            "cpc": spend / clicks if clicks else None,
            "cost_per_link_click": spend / links if links else None,
            "cpm": spend / impressions * 1000 if impressions else None,
            "lpv_rate_pct": lpv / links * 100 if links else None,
            "cost_per_lpv": spend / lpv if lpv else None,
            "traffic_sample": "directional" if impressions < 1000 or lpv < 50 else "sufficient",
        })
        result.append(record)
    ordered = sorted(result, key=lambda x: x["spend"], reverse=True)
    return ordered


def fmt(value, digits=2):
    return "-" if value is None else f"{value:.{digits}f}"


def markdown(report):
    lines = ["# Meta Ads analysis", ""]
    lines.extend([
        f"- Account: `{report.get('account_id') or 'not supplied'}`",
        f"- Currency / timezone: {report.get('currency') or 'not supplied'} / {report.get('timezone') or 'not supplied'}",
        f"- Window: {report.get('window') or 'not supplied'}",
        f"- Export generated at: {report.get('generated_at') or 'not supplied'}",
        "",
        "## Campaign comparison",
        "",
    ])
    lines.append("| Campaign | Spend | Impressions | Freq. | CPM | Link CTR | Cost/link | LPV | LPV/link | Cost/LPV | Top-ad share | Traffic sample | Decision |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |")
    for row in report["campaigns"]:
        if row.get("allocation_warning"):
            decision = "Keep collecting; allocation-confounded"
        elif row["traffic_sample"] == "directional":
            decision = "Keep collecting"
        else:
            decision = "Compare validated outcomes"
        lines.append(
            f"| {row.get('campaign_name','')} | {fmt(row['spend'])} | {int(row['impressions'])} | "
            f"{fmt(row['frequency'])} | {fmt(row['cpm'])} | {fmt(row['link_ctr_pct'])}% | "
            f"{fmt(row['cost_per_link_click'],3)} | {int(row['landing_page_views'])} | "
            f"{fmt(row['lpv_rate_pct'])}% | {fmt(row['cost_per_lpv'],3)} | "
            f"{fmt(row.get('top_ad_spend_share_pct'))}% | {row['traffic_sample']} | {decision} |"
        )
    lines.extend(["", "## Allocation warnings", ""])
    warnings = [row for row in report["campaigns"] if row.get("allocation_warning")]
    if warnings:
        for row in warnings:
            lines.append(f"- `{row['campaign_name']}`: top ad consumed {fmt(row['top_ad_spend_share_pct'])}% of spend; do not infer a clean campaign-level treatment effect.")
    else:
        lines.append("- No campaign exceeded the 80% top-ad spend concentration threshold.")

    lines.extend(["", "## Same-creative cross-campaign comparison", ""])
    lines.append("| Creative/ad name | Campaign | Spend | LPV | Cost/LPV |")
    lines.append("| --- | --- | ---: | ---: | ---: |")
    for group in report.get("same_creative", []):
        for row in group["rows"]:
            lines.append(f"| {group['ad_name']} | {row['campaign_name']} | {fmt(row['spend'])} | {int(row['landing_page_views'])} | {fmt(row['cost_per_lpv'],3)} |")

    lines.extend(["", "## Ad detail", ""])
    lines.append("| Ad | Campaign | Spend | Impressions | Link CTR | LPV | Cost/LPV | Traffic sample |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |")
    for row in report["ads"]:
        lines.append(
            f"| {row.get('ad_name','')} | {row.get('campaign_name','')} | {fmt(row['spend'])} | "
            f"{int(row['impressions'])} | {fmt(row['link_ctr_pct'])}% | {int(row['landing_page_views'])} | "
            f"{fmt(row['cost_per_lpv'],3)} | {row['traffic_sample']} |"
        )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--json", dest="json_output", type=Path)
    parser.add_argument("--markdown", type=Path)
    parser.add_argument("--account-id")
    parser.add_argument("--currency")
    parser.add_argument("--timezone")
    parser.add_argument("--window")
    args = parser.parse_args()

    payload = json.loads(args.input.read_text())
    rows = payload.get("data", payload if isinstance(payload, list) else [])
    report = {
        "source": str(args.input),
        "generated_at": payload.get("generatedAt") if isinstance(payload, dict) else None,
        "account_id": args.account_id,
        "currency": args.currency,
        "timezone": args.timezone,
        "window": args.window,
        "campaigns": aggregate(rows, ["campaign_id", "campaign_name"]),
        "ads": aggregate(rows, ["campaign_id", "campaign_name", "ad_id", "ad_name"]),
    }

    ads_by_campaign = defaultdict(list)
    for ad in report["ads"]:
        ads_by_campaign[ad["campaign_id"]].append(ad)
    for campaign in report["campaigns"]:
        ads = ads_by_campaign[campaign["campaign_id"]]
        spend = campaign["spend"]
        campaign["top_ad_spend_share_pct"] = (
            max((ad["spend"] for ad in ads), default=0) / spend * 100 if spend else None
        )
        campaign["allocation_warning"] = bool(
            campaign["top_ad_spend_share_pct"] is not None
            and campaign["top_ad_spend_share_pct"] >= 80
        )

    by_name = defaultdict(list)
    for ad in report["ads"]:
        if ad.get("ad_name"):
            by_name[ad["ad_name"]].append(ad)
    report["same_creative"] = [
        {"ad_name": name, "rows": sorted(items, key=lambda x: x["campaign_name"])}
        for name, items in sorted(by_name.items()) if len({item["campaign_id"] for item in items}) > 1
    ]

    if args.json_output:
        args.json_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    rendered = markdown(report)
    if args.markdown:
        args.markdown.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
