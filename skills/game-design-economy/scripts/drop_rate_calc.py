#!/usr/bin/env python3
"""drop_rate_calc.py - gacha / drop-rate math: expected pulls, pity, 50/50.

Stdlib only, Python 3.9 compatible. Monte Carlo parts are deterministic via --seed.

Model of the per-pull success probability (the "top rarity" item):
    p(k) = rate                                   for k < soft_start
    p(k) = min(1, rate + soft_step*(k-soft_start+1))   for soft_start <= k < hard_pity
    p(k) = 1                                      for k == hard_pity
where k is the pull number since the last success (1-based). With no
--hard-pity and no --soft-start the rate is constant (geometric).

Subcommands:
    expected   expected pulls to first success, median/p90/p99
    prob       P(at least one success within N pulls) for one or several N
    fifty      pulls to get the FEATURED item with a 50/50 + guarantee mechanic
    copies     pulls to get K copies of the featured item (or of any success)
    simulate   Monte Carlo cross-check of the analytic mean

Examples:
    python3 drop_rate_calc.py expected --rate 0.006 --hard-pity 90 --soft-start 74 --soft-step 0.06
    python3 drop_rate_calc.py prob --rate 0.02 --pulls 10 50 100
    python3 drop_rate_calc.py fifty --rate 0.006 --hard-pity 90 --featured 0.5
    python3 drop_rate_calc.py copies --rate 0.006 --hard-pity 90 --featured 0.5 --count 3
"""
import argparse
import math
import random
import sys

MAX_LEN = 4000  # cap on pmf length when there is no hard pity (tail truncated)


def die(msg):
    sys.stderr.write("error: %s\n" % msg)
    sys.exit(2)


def per_pull_prob(k, rate, hard_pity, soft_start, soft_step):
    if hard_pity and k >= hard_pity:
        return 1.0
    p = rate
    if soft_start and k >= soft_start:
        p = rate + soft_step * (k - soft_start + 1)
    return min(1.0, max(0.0, p))


def first_success_pmf(rate, hard_pity, soft_start, soft_step, start_pity=0):
    """pmf[n] = P(first success happens exactly on pull n), n=1..len-1.
    start_pity: pulls already done since last success (applies to first run)."""
    pmf = [0.0]
    surv = 1.0
    n = 0
    while True:
        n += 1
        p = per_pull_prob(n + start_pity, rate, hard_pity, soft_start, soft_step)
        pmf.append(surv * p)
        surv *= (1.0 - p)
        if surv <= 1e-12 or p >= 1.0:
            break
        if n >= MAX_LEN:
            break
    return pmf


def convolve(a, b, cap=None):
    n = len(a) + len(b) - 1
    if cap is not None:
        n = min(n, cap)
    out = [0.0] * n
    for i, x in enumerate(a):
        if x == 0.0:
            continue
        for j, y in enumerate(b):
            if i + j >= n:
                break
            out[i + j] += x * y
    return out


def mix(a, b, wa, wb):
    n = max(len(a), len(b))
    out = [0.0] * n
    for i, x in enumerate(a):
        out[i] += wa * x
    for i, x in enumerate(b):
        out[i] += wb * x
    return out


def featured_pmf(base, featured_rate, guarantee_after_loss=True, start_guaranteed=False):
    """pmf of pulls until the featured item, from base = first-success pmf.
    featured_rate: P(a success is the featured item) when not guaranteed."""
    if start_guaranteed or featured_rate >= 1.0:
        return list(base)
    if not guarantee_after_loss:
        # every success independently featured with prob f -> geometric mixture
        # pmf_f = sum_k P(k-th success is first featured) -> compute by iteration
        total = [0.0] * len(base)
        cur = list(base)       # distribution of the time of the k-th success
        weight = featured_rate
        for _ in range(60):
            total = mix(total, cur, 1.0, weight)
            weight *= (1.0 - featured_rate)
            if weight < 1e-12:
                break
            cur = convolve(cur, base, cap=MAX_LEN * 2)
        return total
    two = convolve(base, base, cap=MAX_LEN * 2)
    return mix(base, two, featured_rate, 1.0 - featured_rate)


def mean_of(pmf):
    return sum(i * p for i, p in enumerate(pmf))


def quantile(pmf, q):
    acc = 0.0
    for i, p in enumerate(pmf):
        acc += p
        if acc >= q:
            return i
    return len(pmf) - 1


def prob_within(pmf, n):
    return min(1.0, sum(pmf[: n + 1]))


def add_model_args(sp):
    sp.add_argument("--rate", type=float, required=True, help="base per-pull probability, e.g. 0.006")
    sp.add_argument("--hard-pity", type=int, default=0, help="guaranteed success at this pull (0 = none)")
    sp.add_argument("--soft-start", type=int, default=0, help="pull number where soft pity begins (0 = none)")
    sp.add_argument("--soft-step", type=float, default=0.0, help="probability added per pull after soft-start")
    sp.add_argument("--start-pity", type=int, default=0, help="pulls already made since last success")


def check_model(a):
    if not (0 < a.rate <= 1):
        die("--rate must be in (0, 1]")
    if a.hard_pity and a.soft_start and a.soft_start > a.hard_pity:
        die("--soft-start must be <= --hard-pity")
    if a.soft_start and a.soft_step <= 0:
        die("--soft-start needs --soft-step > 0")
    if a.hard_pity < 0 or a.soft_start < 0 or a.start_pity < 0:
        die("pity values must be >= 0")


def base_pmf(a):
    return first_success_pmf(a.rate, a.hard_pity, a.soft_start, a.soft_step, a.start_pity)


def summarize(label, pmf):
    print("%-34s mean=%7.2f  median=%4d  p90=%4d  p99=%4d" % (
        label, mean_of(pmf), quantile(pmf, 0.5), quantile(pmf, 0.9), quantile(pmf, 0.99)))


def cmd_expected(a):
    check_model(a)
    pmf = base_pmf(a)
    print("rate=%.5f hard_pity=%s soft_start=%s soft_step=%.4f" % (
        a.rate, a.hard_pity or "none", a.soft_start or "none", a.soft_step))
    summarize("pulls to first success", pmf)
    print("no-pity expectation 1/rate = %.2f" % (1.0 / a.rate))
    if len(pmf) >= MAX_LEN:
        print("note: tail truncated at %d pulls" % MAX_LEN)
    return 0


def cmd_prob(a):
    check_model(a)
    pmf = base_pmf(a)
    print("%8s  %s" % ("pulls", "P(at least one)"))
    for n in a.pulls:
        print("%8d  %6.2f%%" % (n, 100.0 * prob_within(pmf, n)))
    return 0


def cmd_fifty(a):
    check_model(a)
    if not (0 < a.featured <= 1):
        die("--featured must be in (0, 1]")
    base = base_pmf(a)
    fp = featured_pmf(base, a.featured, not a.no_guarantee, a.guaranteed)
    summarize("any success", base)
    summarize("featured (50/50 mechanic)" if not a.no_guarantee else "featured (no guarantee)", fp)
    print("")
    print("P(featured within N pulls):")
    for n in (a.pulls or [30, 60, 90, 120, 160, 180, 240, 300]):
        print("  N=%-5d %6.2f%%" % (n, 100.0 * prob_within(fp, n)))
    if a.hard_pity:
        print("worst case with guarantee: %d pulls" % (2 * a.hard_pity if not a.guaranteed else a.hard_pity))
    return 0


def cmd_copies(a):
    check_model(a)
    if a.count < 1:
        die("--count must be >= 1")
    base = base_pmf(a)
    one = featured_pmf(base, a.featured, not a.no_guarantee, a.guaranteed)
    # after the first copy the run restarts: pity reset, not guaranteed
    base_fresh = first_success_pmf(a.rate, a.hard_pity, a.soft_start, a.soft_step, 0)
    one_fresh = featured_pmf(base_fresh, a.featured, not a.no_guarantee, False)
    total = one
    for _ in range(a.count - 1):
        total = convolve(total, one_fresh, cap=MAX_LEN * 4)
    summarize("pulls for %d featured copies" % a.count, total)
    for n in (a.pulls or []):
        print("  P(>=%d copies within %d pulls) = %.2f%%" % (a.count, n, 100.0 * prob_within(total, n)))
    return 0


def cmd_simulate(a):
    check_model(a)
    rng = random.Random(a.seed)
    totals = []
    for _ in range(a.trials):
        got = 0
        pulls = 0
        pity = a.start_pity
        guaranteed = a.guaranteed
        while got < a.count:
            pulls += 1
            pity += 1
            if rng.random() < per_pull_prob(pity, a.rate, a.hard_pity, a.soft_start, a.soft_step):
                pity = 0
                if guaranteed or rng.random() < a.featured:
                    got += 1
                    guaranteed = False
                else:
                    guaranteed = not a.no_guarantee
        totals.append(pulls)
    totals.sort()
    mean = sum(totals) / float(len(totals))
    print("Monte Carlo trials=%d seed=%d count=%d" % (a.trials, a.seed, a.count))
    print("mean=%.2f median=%d p90=%d p99=%d" % (
        mean, totals[len(totals) // 2], totals[int(len(totals) * 0.9)], totals[int(len(totals) * 0.99)]))
    return 0


def build_parser():
    ap = argparse.ArgumentParser(
        description="Gacha / drop-rate calculator: expected pulls, pity, 50/50 mechanics, "
                    "probability of getting an item in N pulls.",
        epilog="Run '<subcommand> --help' for details. Numbers are math, not a guarantee "
               "of what a shipped game's real rates are; disclose rates per local regulation.")
    sub = ap.add_subparsers(dest="cmd")
    sub.required = True

    p = sub.add_parser("expected", help="expected pulls to the first success")
    add_model_args(p)
    p.set_defaults(fn=cmd_expected)

    p = sub.add_parser("prob", help="P(at least one success) within N pulls")
    add_model_args(p)
    p.add_argument("--pulls", type=int, nargs="+", required=True, help="one or more N values")
    p.set_defaults(fn=cmd_prob)

    def add_fifty(sp):
        sp.add_argument("--featured", type=float, default=0.5,
                        help="P(a success is the featured item) when not guaranteed (default 0.5)")
        sp.add_argument("--no-guarantee", action="store_true",
                        help="disable the 'lose 50/50 -> next is guaranteed' rule")
        sp.add_argument("--guaranteed", action="store_true",
                        help="start in the guaranteed state (lost the last 50/50)")

    p = sub.add_parser("fifty", help="pulls to the featured item with a 50/50 + guarantee mechanic")
    add_model_args(p)
    add_fifty(p)
    p.add_argument("--pulls", type=int, nargs="*", help="N values to report P(featured within N)")
    p.set_defaults(fn=cmd_fifty)

    p = sub.add_parser("copies", help="pulls to get K copies of the featured item")
    add_model_args(p)
    add_fifty(p)
    p.add_argument("--count", type=int, default=2, help="number of featured copies wanted")
    p.add_argument("--pulls", type=int, nargs="*", help="N values to report P(>=K copies within N)")
    p.set_defaults(fn=cmd_copies)

    p = sub.add_parser("simulate", help="Monte Carlo cross-check")
    add_model_args(p)
    add_fifty(p)
    p.add_argument("--count", type=int, default=1, help="number of featured copies wanted")
    p.add_argument("--trials", type=int, default=20000)
    p.add_argument("--seed", type=int, default=42, help="RNG seed (deterministic)")
    p.set_defaults(fn=cmd_simulate)
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
