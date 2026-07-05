#!/usr/bin/env python3
"""Compute Seoul FRP node names, aliases, and ports."""

import re
import sys

REGIONS = {
    "n": 16000,
    "tw": 16100,
    "sg": 16200,
    "my": 16300,
    "jp": 16400,
    "kr": 16500,
    "ts": 16600,
    "uk": 16700,
}


def parse_node(raw: str):
    node = raw.strip().lower()
    match = re.fullmatch(r"([a-z]+)(\d{1,2})", node)
    if not match:
        raise SystemExit(f"invalid node name: {raw}")
    prefix, number_text = match.groups()
    if prefix not in REGIONS:
        raise SystemExit(f"unknown node prefix: {prefix}")
    number = int(number_text)
    if not 1 <= number <= 99:
        raise SystemExit(f"node number out of range 01-99: {raw}")
    canonical = f"{prefix}{number:02d}"
    port = REGIONS[prefix] + number
    aliases = [canonical]
    if canonical == "n06":
        aliases.insert(0, "n6")
    if canonical == "n07":
        aliases.insert(0, "n7")
    return canonical, port, aliases


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: node_rules.py <node>")
    canonical, port, aliases = parse_node(argv[1])
    print(f"canonical={canonical}")
    print(f"port={port}")
    print(f"aliases={','.join(aliases)}")
    print(f"public_urls={','.join(f'https://{a}.api.flaios.com' for a in aliases)}")
    print(f"newapi_base_url=http://172.17.0.1:{port}")


if __name__ == "__main__":
    main(sys.argv)
