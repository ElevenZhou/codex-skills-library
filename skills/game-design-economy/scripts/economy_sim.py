#!/usr/bin/env python3
"""economy_sim.py - simulate a game economy for N players over D days.

Stdlib only, Python 3.9 compatible, deterministic with --seed.

Usage:
    python3 economy_sim.py --config ../assets/economy_example.json
    python3 economy_sim.py --config cfg.json --players 5000 --days 60 --seed 7
    python3 economy_sim.py --config cfg.json --json > out.json

What it models (deliberately simple; calibrate against real data later):
  * Player types (weighted). Each has a retention anchor table (day -> share
    still playing), sessions per day, rewarded ads per day.
  * Sources: per-session income (optionally scaled by upgrade level),
    daily income (daily login), ad income (per rewarded ad watched).
  * Sinks: per-session consumable cost, and one upgrade ladder
    (cost = base * growth ** level) bought greedily at end of each session.
  * Stall churn: a player who cannot afford the next upgrade for
    `stall_patience_days` days leaves with `stall_churn_per_day` per day.
  * Milestones: ladder level thresholds -> time to reach.

Currency model: one soft currency ("currency" key in config) for the ladder.
All numbers in the example config are placeholders, not benchmarks.
"""
import argparse
import json
import math
import random
import sys


def die(msg):
    sys.stderr.write("error: %s\n" % msg)
    sys.exit(2)


def percentile(sorted_vals, q):
    """q in [0,1]; linear interpolation. Empty -> 0."""
    if not sorted_vals:
        return 0.0
    if len(sorted_vals) == 1:
        return float(sorted_vals[0])
    pos = q * (len(sorted_vals) - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    frac = pos - lo
    return sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac


def build_survival(anchors, days):
    """anchors: {"1":0.4,"7":0.15,...} share still active at END of that day.
    Returns list S[0..days] with S[0]=1, log-linear interpolation between
    anchors, flat-slope extrapolation after the last anchor."""
    pts = [(0, 1.0)]
    for k, v in sorted(((int(k), float(v)) for k, v in anchors.items())):
        if k <= 0 or not (0 < v <= 1):
            die("retention anchors need day>0 and 0<share<=1, got %s:%s" % (k, v))
        pts.append((k, v))
    surv = [1.0] * (days + 1)
    for d in range(1, days + 1):
        left = pts[0]
        right = None
        for p in pts:
            if p[0] <= d:
                left = p
            if p[0] >= d:
                right = p
                break
        if right is None:
            # beyond last anchor: continue the last segment's log slope
            if len(pts) >= 2:
                (d0, v0), (d1, v1) = pts[-2], pts[-1]
                slope = (math.log(v1) - math.log(v0)) / float(d1 - d0)
            else:
                slope = 0.0
            val = math.exp(math.log(pts[-1][1]) + slope * (d - pts[-1][0]))
        elif right[0] == left[0]:
            val = left[1]
        else:
            t = (d - left[0]) / float(right[0] - left[0])
            val = math.exp(math.log(left[1]) * (1 - t) + math.log(right[1]) * t)
        surv[d] = min(val, surv[d - 1])
    return surv


def sample_churn_day(rng, surv):
    """First day d where S[d] < u; returns days+1 if never (survives)."""
    u = rng.random()
    for d in range(1, len(surv)):
        if surv[d] < u:
            return d
    return len(surv)


def poisson_like(rng, mean):
    """floor(mean) plus a Bernoulli on the fraction. Cheap and stable."""
    base = int(math.floor(mean))
    return base + (1 if rng.random() < (mean - base) else 0)


def noisy(rng, mean, cv):
    if cv <= 0:
        return mean
    v = rng.gauss(mean, mean * cv)
    return max(0.0, v)


def validate(cfg):
    for key in ("player_types", "ladder"):
        if key not in cfg:
            die("config missing '%s'" % key)
    if not cfg["player_types"]:
        die("player_types is empty")
    lad = cfg["ladder"]
    for k in ("base_cost", "growth"):
        if k not in lad:
            die("ladder missing '%s'" % k)
    if lad["growth"] < 1.0:
        die("ladder.growth must be >= 1.0")
    for pt in cfg["player_types"]:
        for k in ("name", "weight", "sessions_per_day", "retention"):
            if k not in pt:
                die("player type missing '%s': %s" % (k, pt))


def simulate(cfg, players, days, seed):
    validate(cfg)
    rng = random.Random(seed)
    lad = cfg["ladder"]
    base_cost = float(lad["base_cost"])
    growth = float(lad["growth"])
    max_level = int(lad.get("max_level", 10 ** 6))
    start_bal = float(cfg.get("start_balance", 0))
    stall_patience = int(cfg.get("stall_patience_days", 3))
    stall_churn = float(cfg.get("stall_churn_per_day", 0.25))
    per_session = cfg.get("per_session_sources", [])
    daily_sources = cfg.get("daily_sources", [])
    ad_amount = float(cfg.get("ad_reward_amount", 0))
    session_sink = float(cfg.get("per_session_sink", 0))
    milestones = cfg.get("milestones", [])

    types = cfg["player_types"]
    total_w = sum(float(t["weight"]) for t in types)
    surv_by_type = [build_survival(t["retention"], days) for t in types]

    # per-player state
    pop = []
    for _ in range(players):
        r = rng.random() * total_w
        acc = 0.0
        ti = len(types) - 1
        for i, t in enumerate(types):
            acc += float(t["weight"])
            if r <= acc:
                ti = i
                break
        churn_day = sample_churn_day(rng, surv_by_type[ti])
        pop.append({
            "t": ti, "bal": start_bal, "lvl": 0, "churn": churn_day,
            "stall_days": 0, "alive": True, "stall_left": False,
            "ms": {}, "earned": 0.0, "spent": 0.0,
        })

    earned_by = {}
    spent_ladder = 0.0
    spent_sessions = 0.0
    checkpoints = sorted(set(d for d in (1, 3, 7, 14, 30, 60, 90, days) if d <= days))
    rows = []

    for day in range(1, days + 1):
        for p in pop:
            if not p["alive"]:
                continue
            if day >= p["churn"]:
                p["alive"] = False
                continue
            t = types[p["t"]]
            lvl_at_start = p["lvl"]
            # daily sources
            for s in daily_sources:
                if rng.random() < float(s.get("probability", 1.0)):
                    amt = float(s["amount"])
                    p["bal"] += amt
                    p["earned"] += amt
                    earned_by[s["id"]] = earned_by.get(s["id"], 0.0) + amt
            # ads
            n_ads = poisson_like(rng, float(t.get("ads_per_day", 0)))
            if n_ads and ad_amount:
                amt = n_ads * ad_amount
                p["bal"] += amt
                p["earned"] += amt
                earned_by["rewarded_ad"] = earned_by.get("rewarded_ad", 0.0) + amt
            # sessions
            n_sess = poisson_like(rng, float(t["sessions_per_day"]))
            for _s in range(n_sess):
                for s in per_session:
                    mean = float(s["amount"]) * (1.0 + float(s.get("scale_with_level", 0.0)) * p["lvl"])
                    amt = noisy(rng, mean, float(s.get("cv", 0.2)))
                    p["bal"] += amt
                    p["earned"] += amt
                    earned_by[s["id"]] = earned_by.get(s["id"], 0.0) + amt
                if session_sink:
                    pay = min(p["bal"], session_sink)
                    p["bal"] -= pay
                    p["spent"] += pay
                    spent_sessions += pay
                # greedy ladder purchases
                while p["lvl"] < max_level:
                    cost = base_cost * (growth ** p["lvl"])
                    if p["bal"] >= cost:
                        p["bal"] -= cost
                        p["spent"] += cost
                        spent_ladder += cost
                        p["lvl"] += 1
                        for m in milestones:
                            if p["lvl"] >= int(m["ladder_level"]) and m["id"] not in p["ms"]:
                                p["ms"][m["id"]] = day
                    else:
                        break
            # stall logic: no level gained today (and ladder not maxed)
            if p["lvl"] == lvl_at_start and p["lvl"] < max_level:
                p["stall_days"] += 1
            else:
                p["stall_days"] = 0
            if p["stall_days"] >= stall_patience and rng.random() < stall_churn:
                p["alive"] = False
                p["stall_left"] = True

        if day in checkpoints:
            alive = [p for p in pop if p["alive"]]
            lv = sorted(p["lvl"] for p in alive)
            bal = sorted(p["bal"] for p in alive)
            stalled = sum(1 for p in alive if p["stall_days"] >= stall_patience)
            rows.append({
                "day": day,
                "active": len(alive),
                "active_pct": 100.0 * len(alive) / players,
                "bal_median": percentile(bal, 0.5),
                "bal_p90": percentile(bal, 0.9),
                "lvl_p10": percentile(lv, 0.1),
                "lvl_median": percentile(lv, 0.5),
                "lvl_p90": percentile(lv, 0.9),
                "stalled_pct": (100.0 * stalled / len(alive)) if alive else 0.0,
            })

    ms_out = []
    for m in milestones:
        days_hit = sorted(p["ms"][m["id"]] for p in pop if m["id"] in p["ms"])
        ms_out.append({
            "id": m["id"],
            "ladder_level": int(m["ladder_level"]),
            "reached_pct": 100.0 * len(days_hit) / players,
            "median_day": percentile(days_hit, 0.5) if days_hit else None,
            "p90_day": percentile(days_hit, 0.9) if days_hit else None,
        })

    total_earned = sum(earned_by.values())
    src_out = sorted(
        ({"source": k, "total": v, "share_pct": 100.0 * v / total_earned if total_earned else 0.0}
         for k, v in earned_by.items()),
        key=lambda x: -x["total"])
    stall_left_pct = 100.0 * sum(1 for p in pop if p["stall_left"]) / players
    return {
        "players": players, "days": days, "seed": seed,
        "checkpoints": rows, "milestones": ms_out, "sources": src_out,
        "sinks": {"ladder": spent_ladder, "per_session": spent_sessions},
        "stall_churned_pct": stall_left_pct,
        "final_hoard_per_alive": (
            sum(p["bal"] for p in pop if p["alive"]) / max(1, sum(1 for p in pop if p["alive"]))),
    }


def print_report(res, name):
    print("Economy simulation: %s" % name)
    print("players=%d days=%d seed=%d" % (res["players"], res["days"], res["seed"]))
    print("")
    print("%-5s %8s %7s %10s %10s %6s %6s %6s %9s" % (
        "day", "active", "act%", "bal_med", "bal_p90", "L_p10", "L_med", "L_p90", "stalled%"))
    for r in res["checkpoints"]:
        print("%-5d %8d %6.1f%% %10.0f %10.0f %6.1f %6.1f %6.1f %8.1f%%" % (
            r["day"], r["active"], r["active_pct"], r["bal_median"], r["bal_p90"],
            r["lvl_p10"], r["lvl_median"], r["lvl_p90"], r["stalled_pct"]))
    print("")
    print("Time to milestone (ladder level):")
    if not res["milestones"]:
        print("  (none configured)")
    for m in res["milestones"]:
        if m["median_day"] is None:
            print("  %-12s L%-4d reached by %5.1f%% of players  median day: never" % (
                m["id"], m["ladder_level"], m["reached_pct"]))
        else:
            print("  %-12s L%-4d reached by %5.1f%% of players  median day %.1f  p90 day %.1f" % (
                m["id"], m["ladder_level"], m["reached_pct"], m["median_day"], m["p90_day"]))
    print("")
    print("Income by source:")
    for s in res["sources"]:
        print("  %-14s %12.0f  %5.1f%%" % (s["source"], s["total"], s["share_pct"]))
    print("Spend: ladder=%.0f per_session=%.0f" % (res["sinks"]["ladder"], res["sinks"]["per_session"]))
    print("Players who left because stalled: %.1f%% of all simulated players" % res["stall_churned_pct"])


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Simulate N players over D days against a JSON economy config "
                    "(sources, sinks, sessions, retention). Prints currency curve, "
                    "time-to-milestone and percent of players stalled.")
    ap.add_argument("--config", required=True, help="path to JSON config (see assets/economy_example.json)")
    ap.add_argument("--players", type=int, help="override config 'players' (default 2000)")
    ap.add_argument("--days", type=int, help="override config 'days' (default 30)")
    ap.add_argument("--seed", type=int, default=42, help="RNG seed for deterministic output (default 42)")
    ap.add_argument("--json", action="store_true", help="print machine-readable JSON instead of a table")
    args = ap.parse_args(argv)

    try:
        with open(args.config, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except (OSError, ValueError) as e:
        die("cannot read config: %s" % e)
    players = args.players or int(cfg.get("players", 2000))
    days = args.days or int(cfg.get("days", 30))
    if players < 1 or days < 1:
        die("players and days must be >= 1")
    res = simulate(cfg, players, days, args.seed)
    if args.json:
        print(json.dumps(res, indent=2, sort_keys=True))
    else:
        print_report(res, cfg.get("name", "unnamed"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
