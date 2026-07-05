#!/usr/bin/env python3
"""Check domain availability with public RDAP endpoints.

This is a lightweight helper, not a registrar guarantee. A 404 RDAP response
usually means the registry has no domain object, but registrar premium/reserved
rules can still block registration.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

RDAP_ENDPOINTS = {
    "com": "https://rdap.verisign.com/com/v1/domain/{domain}",
    "net": "https://rdap.verisign.com/net/v1/domain/{domain}",
    "ai": "https://rdap.identitydigital.services/rdap/domain/{domain}",
    "io": "https://rdap.nic.io/domain/{domain}",
    "org": "https://rdap.publicinterestregistry.org/rdap/domain/{domain}",
    "app": "https://rdap.nic.google/domain/{domain}",
    "dev": "https://rdap.nic.google/domain/{domain}",
}

@dataclass
class Result:
    domain: str
    tld: str
    status: str
    http_status: int | None
    source: str | None
    note: str


def normalize(domain: str) -> str:
    domain = domain.strip().lower().removeprefix("http://").removeprefix("https://")
    return domain.split("/")[0].strip(".")


def check(domain: str, timeout: int = 8) -> Result:
    domain = normalize(domain)
    if "." not in domain:
        return Result(domain, "", "unknown", None, None, "domain has no TLD")
    tld = domain.rsplit(".", 1)[1]
    template = RDAP_ENDPOINTS.get(tld)
    if not template:
        return Result(domain, tld, "unknown", None, None, f"unsupported TLD: {tld}")
    url = template.format(domain=domain)
    req = Request(url, headers={"User-Agent": "domain-brand-finder/1.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            code = resp.getcode()
            if code == 200:
                return Result(domain, tld, "registered", code, url, "RDAP object found")
            return Result(domain, tld, "unknown", code, url, f"unexpected RDAP HTTP {code}")
    except HTTPError as exc:
        if exc.code == 404:
            return Result(domain, tld, "available", 404, url, "RDAP object not found")
        return Result(domain, tld, "unknown", exc.code, url, f"RDAP HTTP error {exc.code}")
    except (URLError, TimeoutError) as exc:
        return Result(domain, tld, "unknown", None, url, f"network error: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check domain availability through public RDAP endpoints.")
    parser.add_argument("domains", nargs="+", help="Domains to check, e.g. flaios.com example.ai")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a table")
    parser.add_argument("--timeout", type=int, default=8, help="Per-domain timeout in seconds")
    parser.add_argument("--sleep", type=float, default=0.15, help="Delay between checks")
    args = parser.parse_args()

    results = []
    for domain in args.domains:
        results.append(check(domain, timeout=args.timeout))
        if args.sleep:
            time.sleep(args.sleep)

    if args.json:
        print(json.dumps([asdict(r) for r in results], ensure_ascii=False, indent=2))
    else:
        print(f"{'DOMAIN':<32} {'STATUS':<10} {'HTTP':<6} NOTE")
        for r in results:
            http = "" if r.http_status is None else str(r.http_status)
            print(f"{r.domain:<32} {r.status:<10} {http:<6} {r.note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
