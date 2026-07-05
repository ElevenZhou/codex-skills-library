#!/usr/bin/env python3
"""Create a standard workspace for Deck Studio Loop deliverables."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", help="Workspace directory to create")
    parser.add_argument("--slug", default="deck", help="Deck/task slug")
    args = parser.parse_args()

    root = Path(args.workspace).expanduser().resolve()
    paths = [
        root / "tmp" / "assets",
        root / "tmp" / "qa",
        root / "tmp" / "notes",
        root / "tmp" / "build",
        root / "outputs",
    ]
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)

    ledger = root / "tmp" / "qa" / f"{args.slug}-qa-ledger.txt"
    if not ledger.exists():
        ledger.write_text(
            "\n".join(
                [
                    f"Deck Studio Loop QA Ledger: {args.slug}",
                    f"Created: {datetime.now().isoformat(timespec='seconds')}",
                    "",
                    "Acceptance checks:",
                    "- [ ] PPTX exported",
                    "- [ ] slide PNGs rendered",
                    "- [ ] contact sheet inspected",
                    "- [ ] overflow/layout check passed",
                    "- [ ] brand/product names consistent",
                    "- [ ] required charts/tables/graphics present",
                    "- [ ] role review completed",
                    "- [ ] revision pass completed",
                    "",
                    "Findings:",
                ]
            ),
            encoding="utf-8",
        )

    print(root)


if __name__ == "__main__":
    main()
