#!/usr/bin/env python3
"""Create an Auto Loop autopilot workspace with ledgers for long tasks."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", help="Workspace directory to create")
    parser.add_argument("--slug", default="autopilot", help="Task slug")
    args = parser.parse_args()

    root = Path(args.workspace).expanduser().resolve()
    for rel in [
        "notes",
        "agents",
        "qa",
        "artifacts",
        "scratch",
        "sources",
    ]:
        (root / rel).mkdir(parents=True, exist_ok=True)

    (root / "notes" / f"{args.slug}-contract.txt").write_text(
        "\n".join(
            [
                f"Auto Loop Contract: {args.slug}",
                f"Created: {datetime.now().isoformat(timespec='seconds')}",
                "",
                "Objective:",
                "Audience/user:",
                "Inputs:",
                "Deliverables:",
                "Constraints:",
                "Assumptions:",
                "Acceptance checks:",
                "Fallbacks:",
                "Stop condition:",
            ]
        ),
        encoding="utf-8",
    )

    (root / "notes" / f"{args.slug}-input-checklist.txt").write_text(
        "\n".join(
            [
                f"Auto Loop Input Checklist: {args.slug}",
                "",
                "Completeness:",
                "- [ ] goal",
                "- [ ] artifact type",
                "- [ ] audience/user",
                "- [ ] inputs/source paths",
                "- [ ] output format/path",
                "- [ ] constraints",
                "- [ ] quality bar",
                "- [ ] autonomy level",
                "- [ ] risks/sensitive boundaries",
                "",
                "Missing items:",
                "",
                "Autofill assumptions:",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    (root / "qa" / f"{args.slug}-qa-ledger.txt").write_text(
        "\n".join(
            [
                f"Auto Loop QA Ledger: {args.slug}",
                "",
                "Universal checks:",
                "- [ ] deliverable exists",
                "- [ ] explicit requirements covered",
                "- [ ] relevant specialist skills/tools used",
                "- [ ] artifact-specific QA run",
                "- [ ] role review or multi-agent review completed",
                "- [ ] improvement pass completed",
                "- [ ] final handoff includes paths and validation",
                "",
                "Findings:",
            ]
        ),
        encoding="utf-8",
    )

    (root / "agents" / f"{args.slug}-roles.txt").write_text(
        "\n".join(
            [
                "Roles / lanes:",
                "- Planner:",
                "- Researcher:",
                "- Architect:",
                "- Builder:",
                "- Verifier:",
                "- Critic:",
                "- Integrator:",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(root)


if __name__ == "__main__":
    main()
