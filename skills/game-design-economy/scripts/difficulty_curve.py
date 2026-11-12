#!/usr/bin/env python3
"""difficulty_curve.py - generate a level difficulty curve and print a table.

Stdlib only, Python 3.9 compatible, deterministic with --seed.

Difficulty is a score in [0, 10]. Shapes:
    ramp       linear rise from --start to --end
    sawtooth   ramp with a relief dip after every hard level (every --period levels)
    stairs     plateaus that step up every --period levels
    wave       smooth sine wave on top of a slow ramp

Extras:
    --tutorial N     first N levels are forced easy (score <= 1.5)
    --boss-every K   every K-th level is a spike (+--boss-bump) flagged BOSS
    --jitter J       random +/- J added to every level (seeded)
    --param NAME=BASE,SCALE   derived level parameter: BASE * (1 + SCALE*score)
                              (repeatable), e.g. --param moves=30,-0.04
Target win rate is mapped linearly: score 0 -> --wr-easy, score 10 -> --wr-hard.
These mappings are reference values; calibrate with telemetry per genre.

Examples:
    python3 difficulty_curve.py --levels 30 --shape sawtooth --period 5
    python3 difficulty_curve.py --levels 20 --shape ramp --param moves=30,-0.04 --csv
"""
import argparse
import csv
import json
import math
import random
import sys


def die(msg):
    sys.stderr.write("error: %s\n" % msg)
    sys.exit(2)


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def base_score(shape, i, n, a):
    """i is 0-based level index."""
    t = i / float(max(1, n - 1))
    lin = a.start + (a.end - a.start) * t
    if shape == "ramp":
        return lin
    if shape == "sawtooth":
        pos = i % a.period            # 0 .. period-1
        # within a cycle rise to the cycle peak, then next cycle starts lower
        cycle_t = pos / float(max(1, a.period - 1))
        peak = lin + a.amplitude * 0.5
        trough = lin - a.amplitude * 0.5 * (1.0 + a.relief)
        return max(0.5 * a.start, trough + (peak - trough) * cycle_t)
    if shape == "stairs":
        step = i // a.period
        steps = max(1, (n - 1) // a.period)
        return a.start + (a.end - a.start) * (step / float(steps))
    if shape == "wave":
        return lin + a.amplitude * 0.5 * math.sin(2 * math.pi * i / float(a.period))
    die("unknown shape %s" % shape)


def tag_for(score, is_boss, in_tutorial, prev, score_next_dip):
    if in_tutorial:
        return "TUTORIAL"
    if is_boss:
        return "BOSS"
    if prev is not None and score < prev - 0.8:
        return "RELIEF"
    if score < 2.5:
        return "easy"
    if score < 5.0:
        return "normal"
    if score < 7.5:
        return "hard"
    return "brutal"


def parse_params(items):
    out = []
    for it in items or []:
        try:
            name, rest = it.split("=", 1)
            base, scale = rest.split(",", 1)
            out.append((name.strip(), float(base), float(scale)))
        except ValueError:
            die("--param must look like NAME=BASE,SCALE (got %r)" % it)
    return out


def generate(a):
    rng = random.Random(a.seed)
    params = parse_params(a.param)
    rows = []
    prev = None
    for i in range(a.levels):
        s = base_score(a.shape, i, a.levels, a)
        if a.jitter:
            s += rng.uniform(-a.jitter, a.jitter)
        is_boss = bool(a.boss_every) and (i + 1) % a.boss_every == 0 and i + 1 > a.tutorial
        if is_boss:
            s += a.boss_bump
        in_tut = i < a.tutorial
        if in_tut:
            s = min(s, 1.5)
        s = clamp(s, 0.0, 10.0)
        wr = a.wr_easy - (a.wr_easy - a.wr_hard) * (s / 10.0)
        row = {
            "level": i + 1,
            "score": round(s, 2),
            "tag": tag_for(s, is_boss, in_tut, prev, None),
            "target_win_rate": round(wr, 3),
            "expected_attempts": round(1.0 / wr, 2) if wr > 0 else None,
        }
        for name, base, scale in params:
            row[name] = round(base * (1.0 + scale * s), 2)
        rows.append(row)
        prev = s
    return rows, [p[0] for p in params]


def print_table(rows, pnames):
    head = "%-6s %-6s %-9s %-8s %-9s" % ("level", "score", "tag", "win%", "attempts")
    for p in pnames:
        head += " %-9s" % p
    head += " curve"
    print(head)
    for r in rows:
        bar = "#" * int(round(r["score"] * 2))
        line = "%-6d %-6.2f %-9s %-8.1f %-9.2f" % (
            r["level"], r["score"], r["tag"], 100 * r["target_win_rate"], r["expected_attempts"])
        for p in pnames:
            line += " %-9s" % r[p]
        print(line + " " + bar)
    scores = [r["score"] for r in rows]
    peaks = [r["level"] for r in rows if r["tag"] in ("BOSS",)]
    print("")
    print("levels=%d  min=%.2f  max=%.2f  mean=%.2f  boss_levels=%s" % (
        len(rows), min(scores), max(scores), sum(scores) / len(scores), peaks or "none"))
    jumps = [abs(rows[i]["score"] - rows[i - 1]["score"]) for i in range(1, len(rows))]
    if jumps:
        print("largest level-to-level jump=%.2f (flag if > 2.5 outside bosses)" % max(jumps))


def build_parser():
    ap = argparse.ArgumentParser(
        description="Generate a level difficulty curve (sawtooth/ramp/stairs/wave) and print a table "
                    "with target win rate and expected attempts per level.")
    ap.add_argument("--levels", type=int, default=30, help="number of levels (default 30)")
    ap.add_argument("--shape", choices=["ramp", "sawtooth", "stairs", "wave"], default="sawtooth")
    ap.add_argument("--start", type=float, default=1.0, help="start difficulty score 0-10 (default 1)")
    ap.add_argument("--end", type=float, default=8.0, help="end difficulty score 0-10 (default 8)")
    ap.add_argument("--period", type=int, default=5, help="cycle length for sawtooth/stairs/wave (default 5)")
    ap.add_argument("--amplitude", type=float, default=2.5, help="swing size for sawtooth/wave (default 2.5)")
    ap.add_argument("--relief", type=float, default=0.6,
                    help="sawtooth: extra depth of the trough after a peak, 0..1+ (default 0.6)")
    ap.add_argument("--tutorial", type=int, default=3, help="number of forced-easy tutorial levels (default 3)")
    ap.add_argument("--boss-every", type=int, default=10, help="every K-th level is a boss spike (0 = off)")
    ap.add_argument("--boss-bump", type=float, default=1.5, help="score added on boss levels (default 1.5)")
    ap.add_argument("--jitter", type=float, default=0.3, help="random +/- noise per level (default 0.3)")
    ap.add_argument("--wr-easy", type=float, default=0.92, help="target win rate at score 0 (default 0.92)")
    ap.add_argument("--wr-hard", type=float, default=0.25, help="target win rate at score 10 (default 0.25)")
    ap.add_argument("--param", action="append", metavar="NAME=BASE,SCALE",
                    help="derived parameter BASE*(1+SCALE*score); repeatable")
    ap.add_argument("--seed", type=int, default=42, help="RNG seed for jitter (default 42)")
    out = ap.add_mutually_exclusive_group()
    out.add_argument("--csv", action="store_true", help="print CSV")
    out.add_argument("--json", action="store_true", help="print JSON")
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)
    if a.levels < 1:
        die("--levels must be >= 1")
    if a.period < 1:
        die("--period must be >= 1")
    if not (0 < a.wr_hard < a.wr_easy <= 1):
        die("need 0 < --wr-hard < --wr-easy <= 1")
    rows, pnames = generate(a)
    if a.json:
        print(json.dumps(rows, indent=2))
    elif a.csv:
        cols = ["level", "score", "tag", "target_win_rate", "expected_attempts"] + pnames
        w = csv.writer(sys.stdout, lineterminator="\n")
        w.writerow(cols)
        for r in rows:
            w.writerow([r[c] for c in cols])
    else:
        print_table(rows, pnames)
    return 0


if __name__ == "__main__":
    sys.exit(main())
