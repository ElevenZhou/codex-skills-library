#!/usr/bin/env python3
"""apk_budget_check.py - check an APK/AAB/zip size against a budget and list
the largest entries.

Stdlib only, Python 3.9 compatible. Read-only: the archive is never extracted.

Exit codes:  0 within budget   1 over budget (or --max-entry-mb exceeded)
             2 usage / unreadable archive

Examples:
    python3 apk_budget_check.py build/game.apk --budget-mb 80
    python3 apk_budget_check.py game.aab --budget-mb 150 --top 20 --json
    python3 apk_budget_check.py game.apk --budget-mb 60 --max-entry-mb 15

Budget guidance (reference values, calibrate per genre; see
references/perf-budgets.md): hyper-casual < 30 MB, casual < 80 MB,
mid-core < 200 MB. Google Play base APK/AAB limits change over time;
check the current Play Console documentation.
"""
import argparse
import json
import os
import sys
import zipfile

MB = 1024.0 * 1024.0


def die(msg, code=2):
    sys.stderr.write("error: %s\n" % msg)
    sys.exit(code)


def categorize(name):
    n = name.lower()
    if n.startswith("lib/") or "/lib/" in n and n.endswith(".so"):
        return "native libs (.so)"
    if n.endswith(".dex"):
        return "dex (code)"
    if n.endswith(".pck") or n.endswith(".obb"):
        return "engine pack (.pck/.obb)"
    if n.endswith((".png", ".jpg", ".jpeg", ".webp", ".ktx", ".astc", ".etc2", ".ctex")):
        return "images/textures"
    if n.endswith((".ogg", ".mp3", ".wav", ".m4a", ".opus", ".oggvorbisstr")):
        return "audio"
    if n.endswith((".ttf", ".otf", ".fontdata")):
        return "fonts"
    if n.startswith("res/") or "/res/" in n:
        return "android res"
    if n.startswith("assets/") or "/assets/" in n:
        return "assets (other)"
    return "other"


def analyze(path, top):
    try:
        zf = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as e:
        die("cannot open %s as zip: %s" % (path, e))
    infos = [i for i in zf.infolist() if not i.is_dir()]
    zf.close()
    entries = sorted(infos, key=lambda i: -i.compress_size)
    cats = {}
    for i in infos:
        c = cats.setdefault(categorize(i.filename), {"files": 0, "compressed": 0, "uncompressed": 0})
        c["files"] += 1
        c["compressed"] += i.compress_size
        c["uncompressed"] += i.file_size
    return {
        "file": os.path.abspath(path),
        "file_bytes": os.path.getsize(path),
        "entries": len(infos),
        "uncompressed_bytes": sum(i.file_size for i in infos),
        "top": [{"name": i.filename, "compressed": i.compress_size, "uncompressed": i.file_size}
                for i in entries[:top]],
        "categories": cats,
        "_all": [{"name": i.filename, "compressed": i.compress_size} for i in entries],
    }


def build_parser():
    ap = argparse.ArgumentParser(
        description="Check APK/AAB (zip) size vs a budget and list the top-N largest entries.")
    ap.add_argument("archive", help="path to .apk / .aab / .zip")
    ap.add_argument("--budget-mb", type=float, required=True, help="maximum allowed file size in MB (1 MB = 1048576 bytes)")
    ap.add_argument("--warn-ratio", type=float, default=0.9,
                    help="print WARN when size >= ratio*budget (default 0.9)")
    ap.add_argument("--top", type=int, default=10, help="list the N largest entries (default 10)")
    ap.add_argument("--max-entry-mb", type=float, default=0.0,
                    help="optional: fail if any single entry (compressed) exceeds this size")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)
    if not os.path.isfile(a.archive):
        die("file not found: %s" % a.archive)
    if a.budget_mb <= 0 or a.top < 0:
        die("--budget-mb must be > 0 and --top >= 0")
    r = analyze(a.archive, a.top)
    size_mb = r["file_bytes"] / MB
    ratio = size_mb / a.budget_mb
    all_entries = r.pop("_all")
    over_entry = [e for e in all_entries if a.max_entry_mb and e["compressed"] / MB > a.max_entry_mb]
    if ratio > 1.0 or over_entry:
        status = "FAIL"
    elif ratio >= a.warn_ratio:
        status = "WARN"
    else:
        status = "PASS"
    r.update({"budget_mb": a.budget_mb, "size_mb": round(size_mb, 3),
              "ratio": round(ratio, 3), "status": status,
              "entries_over_max": [e["name"] for e in over_entry]})
    if a.json:
        print(json.dumps(r, indent=2, sort_keys=True))
    else:
        print("%s  %s" % (status, os.path.basename(a.archive)))
        print("size=%.2f MB  budget=%.2f MB  used=%.0f%%  entries=%d  uncompressed=%.2f MB" % (
            size_mb, a.budget_mb, 100 * ratio, r["entries"], r["uncompressed_bytes"] / MB))
        print("")
        print("By category (compressed):")
        for k, v in sorted(r["categories"].items(), key=lambda kv: -kv[1]["compressed"]):
            print("  %-26s %5d files  %9.2f MB  (uncompressed %.2f MB)" % (
                k, v["files"], v["compressed"] / MB, v["uncompressed"] / MB))
        print("")
        print("Top %d entries (compressed):" % len(r["top"]))
        for e in r["top"]:
            print("  %9.3f MB  %9.3f MB raw  %s" % (e["compressed"] / MB, e["uncompressed"] / MB, e["name"]))
        if over_entry:
            print("")
            print("Entries over --max-entry-mb: %s" % ", ".join(e["name"] for e in over_entry))
    return 1 if status == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
