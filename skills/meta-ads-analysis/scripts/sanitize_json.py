#!/usr/bin/env python3
"""Remove tokens and token-bearing paging URLs from Meta Graph JSON."""

import json
import re
import sys
from pathlib import Path


TOKEN_KEYS = {"access_token", "token", "appsecret_proof"}


def sanitize(value):
    if isinstance(value, dict):
        clean = {}
        for key, item in value.items():
            if key.lower() in TOKEN_KEYS:
                clean[key] = "<redacted>"
            elif key == "paging":
                clean[key] = sanitize({k: v for k, v in item.items() if k not in {"next", "previous"}})
            else:
                clean[key] = sanitize(item)
        return clean
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    if isinstance(value, str):
        return re.sub(r"([?&]access_token=)[^&]+", r"\1<redacted>", value)
    return value


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: sanitize_json.py INPUT OUTPUT")
    source, target = map(Path, sys.argv[1:])
    target.write_text(json.dumps(sanitize(json.loads(source.read_text())), ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
