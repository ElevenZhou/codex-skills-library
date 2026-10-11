#!/usr/bin/env python3
"""视频算力双站对账（离线、只读）。

输入：老站/新站导出（日聚合或逐笔，TSV/CSV），渠道账单（日汇总或逐笔）。
输出：summary.json、daily.csv、by_model.csv、discrepancies.csv、report.md。
金额一律 Decimal，单位元；站内金额为官方原价（list_yuan）与客户实扣（cust_yuan）。
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

UTC8 = timezone(timedelta(hours=8))
ZERO = Decimal(0)
NOISE = ("██", "请使用", "Please use", "Please", "https://up.", "\tup.yd", "*****", "SET", "Output format", "Field separator", "START", "COMMIT")

ALIASES = {
    "bill_day": ["bill_day", "d", "day", "date", "日期", "完成日期cst"],
    "completed_at": ["completed_at", "finish_time", "finished_at", "完成时间"],
    "model": ["model", "model_name", "模型"],
    "status": ["status", "状态"],
    "n": ["n", "count", "任务数"],
    "tokens": ["tokens", "tok", "total_tokens"],
    "list_yuan": ["list_yuan", "官方原价元"],
    "cust_yuan": ["cust_yuan", "客户实扣元"],
    "upstream_task_id": ["upstream_task_id", "adapter_task_id", "上游任务id"],
    "our_task_id": ["our_task_id", "public_task_id"],
    "amount": ["amount", "consumption", "vendor_amount", "消耗额", "消耗额度"],
    "opening": ["opening", "期初", "折划算力额度余额"],
    "closing": ["closing", "期末", "当日额度余额"],
}
SUCCESS = {"success", "succeeded", "成功"}
FAILED = {"failure", "failed", "error", "cancelled", "canceled", "失败"}


def read_table(path: Path) -> list[dict]:
    lines = [x for x in path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
             if x.strip() and not x.lstrip().startswith(NOISE)]
    if not lines:
        return []
    delim = max(",\t|;", key=lambda c: lines[0].count(c))
    rows = list(csv.reader(lines, delimiter=delim))
    head = [h.strip().lower() for h in rows[0]]
    return [dict(zip(head, r)) for r in rows[1:] if len(r) == len(head)]


def pick(row: dict, key: str) -> str:
    return next(((row.get(a) or "").strip() for a in ALIASES[key] if a in row), "")


def dec(v: str) -> Decimal | None:
    try:
        return Decimal(v.replace(",", "")) if v else None
    except InvalidOperation:
        return None


def to_day(v: str) -> str:
    if not v:
        return ""
    try:
        dt = datetime.fromtimestamp(int(v), UTC8) if v.isdigit() else datetime.fromisoformat(v.replace("Z", "+00:00"))
    except ValueError:
        return ""
    return (dt if dt.tzinfo else dt.replace(tzinfo=UTC8)).astimezone(UTC8).date().isoformat()


def norm_status(s: str) -> str:
    s = s.lower()
    return "success" if s in SUCCESS else "failed" if s in FAILED else (s or "unknown")


def load_site(path: Path, site: str) -> list[dict]:
    out = []
    for r in read_table(path):
        day = pick(r, "bill_day")
        day = day if len(day) == 10 and day[4] == "-" else to_day(pick(r, "completed_at") or day)
        out.append({
            "site": site, "bill_day": day, "model": pick(r, "model"),
            "status": norm_status(pick(r, "status")),
            "n": int(dec(pick(r, "n")) or 1), "tokens": int(dec(pick(r, "tokens")) or 0),
            "list": dec(pick(r, "list_yuan")) or ZERO, "cust": dec(pick(r, "cust_yuan")) or ZERO,
            "upstream_task_id": pick(r, "upstream_task_id"), "our_task_id": pick(r, "our_task_id"),
        })
    return out


def load_vendor(path: Path) -> list[dict]:
    out = []
    for r in read_table(path):
        day = pick(r, "bill_day")
        day = day if len(day) == 10 and day[4] == "-" else to_day(pick(r, "completed_at") or day)
        out.append({"bill_day": day, "amount": dec(pick(r, "amount")) or ZERO,
                    "opening": dec(pick(r, "opening")), "closing": dec(pick(r, "closing")),
                    "upstream_task_id": pick(r, "upstream_task_id")})
    return out


def q2(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"))


def reconcile(sites: list[dict], vendor: list[dict], start: str, end: str, exclude: set[str],
              discount: Decimal, threshold: Decimal) -> dict:
    inwin = lambda d: d and start <= d < end and d not in exclude
    sites = [r for r in sites if inwin(r["bill_day"])]
    vendor = [r for r in vendor if inwin(r["bill_day"])]
    disc: list[dict] = []

    # 四组汇总
    tot = defaultdict(lambda: {"list": ZERO, "cust": ZERO, "success": 0, "failed": 0, "other": 0})
    for r in sites:
        t = tot[r["site"]]
        t["list"] += r["list"]; t["cust"] += r["cust"]
        t[r["status"] if r["status"] in ("success", "failed") else "other"] += r["n"]
        if r["status"] == "failed" and r["cust"] > 0:
            disc.append({"type": "failed_with_charge", "site": r["site"], "bill_day": r["bill_day"],
                         "key": r["upstream_task_id"] or r["model"], "detail": f"失败但客户实扣 {r['cust']}"})
    vtotal = sum((r["amount"] for r in vendor), ZERO)
    ours = sum((t["list"] for t in tot.values()), ZERO)
    diff = vtotal - ours
    rate = diff / vtotal if vtotal else Decimal(0)
    groups = {}
    for s, t in sorted(tot.items()):
        margin = t["cust"] - t["list"] * discount
        groups[s] = {"list_yuan": str(q2(t["list"])), "cost_yuan": str(q2(t["list"] * discount)),
                     "cust_yuan": str(q2(t["cust"])), "margin_yuan": str(q2(margin)),
                     "margin_rate": f"{margin / t['cust'] * 100:.1f}%" if t["cust"] else "",
                     "success": t["success"], "failed": t["failed"], "other": t["other"]}
    cust_all = sum((t["cust"] for t in tot.values()), ZERO)
    groups["combined"] = {"list_yuan": str(q2(ours)), "cost_yuan": str(q2(ours * discount)), "cust_yuan": str(q2(cust_all))}
    groups["vendor"] = {"list_yuan": str(q2(vtotal)), "cost_yuan": str(q2(vtotal * discount)),
                        "margin_vs_bill_yuan": str(q2(cust_all - vtotal * discount))}

    # 逐日
    by_day = defaultdict(lambda: defaultdict(lambda: ZERO))
    for r in sites:
        by_day[r["bill_day"]][r["site"]] += r["list"]
    vday = defaultdict(lambda: ZERO)
    for r in vendor:
        vday[r["bill_day"]] += r["amount"]
    site_names = sorted(tot)
    daily = []
    for d in sorted(set(by_day) | set(vday)):
        o = sum(by_day[d].values(), ZERO); dd = vday[d] - o
        dr = dd / vday[d] if vday[d] else None
        daily.append({"bill_day": d, "vendor": q2(vday[d]), **{s: q2(by_day[d][s]) for s in site_names},
                      "ours": q2(o), "diff": q2(dd), "rate": f"{dr * 100:+.2f}%" if dr is not None else ""})
        if d not in vday:
            disc.append({"type": "missing_vendor_day", "site": "vendor", "bill_day": d, "key": "", "detail": f"我方 {q2(o)}，账单无此日"})
        elif not by_day[d]:
            disc.append({"type": "missing_ours_day", "site": "ours", "bill_day": d, "key": "", "detail": f"账单 {q2(vday[d])}，我方无此日"})
        elif dr is not None and abs(dr) >= Decimal("0.05") and abs(dd) >= 100:
            disc.append({"type": "daily_diff_large", "site": "", "bill_day": d, "key": "", "detail": f"差 {q2(dd)}（{dr * 100:+.2f}%）"})

    # 余额滚动：期初 ≠ 前日期末
    rolled = [r for r in sorted(vendor, key=lambda r: r["bill_day"]) if r["opening"] is not None and r["closing"] is not None]
    for prev, cur in zip(rolled, rolled[1:]):
        if cur["opening"] != prev["closing"]:
            disc.append({"type": "balance_adjustment", "site": "vendor", "bill_day": cur["bill_day"], "key": "",
                         "detail": f"期初 {cur['opening']} − 前日期末 {prev['closing']} = {cur['opening'] - prev['closing']}"})

    # 分模型
    bm = defaultdict(lambda: [0, 0, ZERO, ZERO])
    for r in sites:
        x = bm[(r["site"], r["model"], r["status"])]
        x[0] += r["n"]; x[1] += r["tokens"]; x[2] += r["list"]; x[3] += r["cust"]
    by_model = [{"site": k[0], "model": k[1], "status": k[2], "n": v[0], "tokens": v[1],
                 "list_yuan": q2(v[2]), "cust_yuan": q2(v[3])} for k, v in sorted(bm.items())]

    # 逐笔匹配（双方都有上游任务 ID 时）
    per_task = any(r["upstream_task_id"] for r in vendor) and any(r["upstream_task_id"] for r in sites)
    if per_task:
        mine, theirs = defaultdict(list), defaultdict(list)
        for r in sites:
            if r["upstream_task_id"]:
                mine[r["upstream_task_id"]].append(r)
        for r in vendor:
            if r["upstream_task_id"]:
                theirs[r["upstream_task_id"]].append(r)
        for k in sorted(set(mine) | set(theirs)):
            m, t = mine.get(k, []), theirs.get(k, [])
            if len(m) > 1 or len(t) > 1:
                disc.append({"type": "duplicate", "site": ",".join(sorted({x["site"] for x in m})) or "vendor", "bill_day": (m or t)[0]["bill_day"], "key": k, "detail": f"我方 {len(m)} 条 / 账单 {len(t)} 条"})
            if m and not t:
                if any(x["list"] > 0 for x in m):
                    disc.append({"type": "missing_vendor", "site": m[0]["site"], "bill_day": m[0]["bill_day"], "key": k, "detail": f"我方原价 {sum((x['list'] for x in m), ZERO)}，账单无"})
            elif t and not m:
                disc.append({"type": "missing_ours", "site": "vendor", "bill_day": t[0]["bill_day"], "key": k, "detail": f"账单 {sum((x['amount'] for x in t), ZERO)}，我方无（创建超时/孤儿任务？）"})
            elif m and t:
                a, b = sum((x["list"] for x in m), ZERO), sum((x["amount"] for x in t), ZERO)
                if any(x["status"] == "failed" for x in m) and b > 0:
                    disc.append({"type": "failed_but_vendor_charged", "site": m[0]["site"], "bill_day": m[0]["bill_day"], "key": k, "detail": f"我方失败，账单 {b}"})
                elif abs(a - b) > Decimal("0.01"):
                    disc.append({"type": "amount_diff", "site": m[0]["site"], "bill_day": m[0]["bill_day"], "key": k, "detail": f"我方 {a} / 账单 {b}"})
                if m[0]["bill_day"] != t[0]["bill_day"]:
                    disc.append({"type": "time_boundary_diff", "site": m[0]["site"], "bill_day": m[0]["bill_day"], "key": k, "detail": f"账单日 {t[0]['bill_day']}"})

    verdict = "pass" if vtotal and abs(rate) < threshold else ("no_vendor" if not vtotal else "needs_per_task")
    return {
        "window": {"start": start, "end": end, "excluded_days": sorted(exclude), "timezone": "Asia/Shanghai", "boundary": "[00:00, 24:00)"},
        "discount": str(discount), "threshold": str(threshold), "per_task_matched": per_task,
        "vendor_total": str(q2(vtotal)), "ours_total": str(q2(ours)), "diff": str(q2(diff)), "diff_rate": f"{rate * 100:+.2f}%",
        "verdict": verdict, "groups": groups, "daily": daily, "by_model": by_model, "discrepancies": disc,
        "discrepancy_counts": dict(Counter(x["type"] for x in disc)),
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        if not rows:
            f.write(""); return
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def render_report(res: dict, title: str) -> str:
    g, sites = res["groups"], [k for k in res["groups"] if k not in ("combined", "vendor")]
    verdict = {"pass": f"**通过**：差异率 {res['diff_rate']} 低于阈值，不做逐笔核对",
               "needs_per_task": f"**需逐笔核对**：差异率 {res['diff_rate']} 超过阈值",
               "no_vendor": "**未提供渠道账单**，只做站内汇总"}[res["verdict"]]
    L = [f"# {title}", "", f"窗口：{res['window']['start']} ～ {res['window']['end']}（不含），北京时间完成日切分"
         + (f"；排除 {', '.join(res['window']['excluded_days'])}" if res["window"]["excluded_days"] else ""), "",
         f"结论：{verdict}。账单 {res['vendor_total']}，我方合计 {res['ours_total']}，差 {res['diff']}。", "",
         f"## 四组汇总（元，成本 = 原价 × {res['discount']}）", "",
         "| 项目 | 渠道账单 | " + " | ".join(sites) + " | 合计 |", "|---|" + "---:|" * (len(sites) + 2)]
    for label, key in (("官方原价", "list_yuan"), ("成本", "cost_yuan"), ("客户实扣", "cust_yuan")):
        v = g["vendor"].get(key, "—") if key != "cust_yuan" else "—"
        L.append(f"| {label} | {v} | " + " | ".join(g[s][key] for s in sites) + f" | {g['combined'][key]} |")
    L.append("| 毛利 | — | " + " | ".join(f"{g[s]['margin_yuan']}（{g[s]['margin_rate']}）" for s in sites)
             + f" | {g['vendor']['margin_vs_bill_yuan']}（扣账单全额成本） |")
    L.append("| 成功/失败 | — | " + " | ".join(f"{g[s]['success']}/{g[s]['failed']}" for s in sites) + " | |")
    L += ["", "## 逐日对照（官方原价，元）", "", "| 日期 | 账单 | " + " | ".join(sites) + " | 合计 | 差额 | 差异率 |",
          "|---|" + "---:|" * (len(sites) + 4)]
    for d in res["daily"]:
        L.append(f"| {d['bill_day']} | {d['vendor']} | " + " | ".join(str(d[s]) for s in sites) + f" | {d['ours']} | {d['diff']} | {d['rate']} |")
    L += ["", "## 差异", ""]
    L += [f"- {k}: {v}" for k, v in res["discrepancy_counts"].items()] or ["- 无"]
    L += ["", "明细见 discrepancies.csv、by_model.csv、daily.csv。"]
    return "\n".join(L) + "\n"


def run(a) -> dict:
    sites = []
    for path, name in ((a.old, a.old_label), (a.new, a.new_label)):
        if path:
            sites += load_site(path, name)
    vendor = load_vendor(a.vendor) if a.vendor else []
    res = reconcile(sites, vendor, a.start, a.end, set(a.exclude_day or []), Decimal(a.discount), Decimal(a.threshold))
    if a.output:
        a.output.mkdir(parents=True, exist_ok=True)
        write_csv(a.output / "daily.csv", res["daily"])
        write_csv(a.output / "by_model.csv", res["by_model"])
        write_csv(a.output / "discrepancies.csv", res["discrepancies"] or [{"type": "", "site": "", "bill_day": "", "key": "", "detail": ""}][:0])
        (a.output / "summary.json").write_text(json.dumps({k: v for k, v in res.items() if k not in ("daily", "by_model", "discrepancies")},
                                                          ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        (a.output / "report.md").write_text(render_report(res, a.title), encoding="utf-8")
    return res


def selftest() -> None:
    fx = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "zsg-20260929-20261009"
    exp = json.loads((fx / "expected.json").read_text(encoding="utf-8"))
    ns = argparse.Namespace(old=fx / "old_daily.tsv", new=fx / "new_daily.tsv", vendor=fx / "vendor_daily.csv",
                            old_label="old", new_label="new", start="2026-09-29", end="2026-10-11",
                            exclude_day=["2026-10-10"], discount="0.77", threshold="0.01", output=None, title="")
    res = run(ns)
    got = {"vendor_total": res["vendor_total"], "ours_total": res["ours_total"], "diff": res["diff"],
           "verdict": res["verdict"], "new_list": res["groups"]["new"]["list_yuan"],
           "old_list": res["groups"]["old"]["list_yuan"], "old_cust": res["groups"]["old"]["cust_yuan"],
           "balance_adjustments": res["discrepancy_counts"].get("balance_adjustment", 0)}
    bad = {k: (got[k], v) for k, v in exp.items() if str(got.get(k)) != str(v)}
    print(json.dumps(got, ensure_ascii=False))
    if bad:
        sys.exit(f"SELFTEST FAIL: {bad}")
    print("SELFTEST OK")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--old", type=Path, help="老站导出（old_daily.sql / old_tasks.sql 输出）")
    ap.add_argument("--new", type=Path, help="新站导出（new_daily.sql / new_tasks.sql 输出）")
    ap.add_argument("--vendor", type=Path, help="渠道账单：日汇总（bill_day, amount[, opening, closing]）或逐笔（含 upstream_task_id）")
    ap.add_argument("--old-label", default="old"); ap.add_argument("--new-label", default="new")
    ap.add_argument("--start"); ap.add_argument("--end", help="不含")
    ap.add_argument("--exclude-day", action="append", help="排除的日期（如截止时刻存疑的不完整日），可重复")
    ap.add_argument("--discount", default="1", help="合同折扣：成本 = 原价 × discount")
    ap.add_argument("--threshold", default="0.01", help="合计差异率低于该值判定通过")
    ap.add_argument("--output", type=Path); ap.add_argument("--title", default="视频算力渠道对账报告")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.start and a.end and a.output):
        ap.error("需要 --start、--end、--output")
    res = run(a)
    print(json.dumps({k: res[k] for k in ("vendor_total", "ours_total", "diff", "diff_rate", "verdict", "discrepancy_counts")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
