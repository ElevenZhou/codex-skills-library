#!/usr/bin/env python3
"""Utilities for maintaining an Obsidian memory vault."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

DEFAULT_DIRS = [
    "00 Inbox",
    "10 Memory",
    "20 Projects",
    "30 Decisions",
    "40 Knowledge/Patterns",
    "40 Knowledge/Lessons",
    "50 Reviews/Weekly",
    "50 Reviews/Monthly",
    "90 Index",
    "99 System",
]

SEED_NOTES = {
    "00 Inbox/Memory Inbox.md": "# Memory Inbox\n\nCapture raw items here before they are processed.\n",
    "10 Memory/User Profile.md": "# User Profile\n\n## Confirmed\n\n## Inferred\n\n## Needs Confirmation\n",
    "10 Memory/Preferences.md": "# Preferences\n\n## Communication\n\n## Tools\n\n## Workflow\n",
    "10 Memory/Working Style.md": "# Working Style\n\n## Operating Principles\n\n## Collaboration Notes\n",
    "90 Index/MOC - Memory.md": "# MOC - Memory\n\n- [[User Profile]]\n- [[Preferences]]\n- [[Working Style]]\n",
    "90 Index/MOC - Projects.md": "# MOC - Projects\n\n## Active\n\n## Archived\n",
    "90 Index/MOC - Decisions.md": "# MOC - Decisions\n\n",
    "99 System/Memory Runs.md": "# Memory Runs\n\n",
}


def slug_title(value: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|]", "-", value).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned or "Untitled"


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value).replace('"', '\\"')
    return f'"{text}"'


def render_frontmatter(props: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in props.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {yaml_scalar(item)}")
        else:
            lines.append(f"{key}: {yaml_scalar(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def ensure_vault(vault: Path) -> None:
    vault.mkdir(parents=True, exist_ok=True)
    for rel in DEFAULT_DIRS:
        (vault / rel).mkdir(parents=True, exist_ok=True)
    for rel, body in SEED_NOTES.items():
        path = vault / rel
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")


def normalize_note_path(entry: dict[str, Any]) -> Path:
    raw = entry.get("path") or entry.get("title") or "Untitled"
    raw = str(raw)
    if not raw.endswith(".md"):
        raw = f"{raw}.md"
    parts = [slug_title(part) for part in Path(raw).parts]
    return Path(*parts)


def render_note(entry: dict[str, Any]) -> str:
    title = entry.get("title") or Path(str(entry.get("path", "Untitled"))).stem
    today = date.today().isoformat()
    props = {
        "title": title,
        "type": entry.get("type", "memory"),
        "status": entry.get("status", "confirmed"),
        "updated": entry.get("updated", today),
        "confidence": entry.get("confidence", "confirmed"),
        "sources": entry.get("sources", []),
        "tags": entry.get("tags", ["memory"]),
    }
    props.update(entry.get("properties", {}))
    body = str(entry.get("content", "")).strip()
    if not body.startswith("#"):
        body = f"# {title}\n\n{body}".rstrip()
    return render_frontmatter(props) + body + "\n"


def append_once(path: Path, content: str) -> bool:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    marker = content.strip()
    if marker and marker in old:
        return False
    with path.open("a", encoding="utf-8") as handle:
        if old and not old.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + content.strip() + "\n")
    return True


def write_json(vault: Path, input_path: Path) -> list[str]:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    entries = data.get("entries", data if isinstance(data, list) else [])
    changed: list[str] = []
    for entry in entries:
        rel = normalize_note_path(entry)
        target = vault / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        mode = entry.get("mode", "replace")
        if mode == "append":
            if append_once(target, str(entry.get("content", ""))):
                changed.append(str(rel))
        else:
            rendered = render_note(entry)
            old = target.read_text(encoding="utf-8") if target.exists() else None
            if old != rendered:
                target.write_text(rendered, encoding="utf-8")
                changed.append(str(rel))
    run_log = vault / "99 System/Memory Runs.md"
    run_log.parent.mkdir(parents=True, exist_ok=True)
    summary = ", ".join(changed) if changed else "no note changes"
    append_once(run_log, f"- {datetime.now().isoformat(timespec='seconds')}: write-json from `{input_path}`; {summary}.")
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description="Maintain an Obsidian memory vault.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    init_parser = sub.add_parser("init", help="Create the default memory vault folders and seed notes.")
    init_parser.add_argument("--vault", required=True)

    write_parser = sub.add_parser("write-json", help="Write notes from a memory packet JSON file.")
    write_parser.add_argument("--vault", required=True)
    write_parser.add_argument("--input", required=True)

    args = parser.parse_args()
    vault = Path(args.vault).expanduser().resolve()
    if args.cmd == "init":
        ensure_vault(vault)
        print(f"Initialized memory vault structure at {vault}")
    elif args.cmd == "write-json":
        ensure_vault(vault)
        changed = write_json(vault, Path(args.input).expanduser().resolve())
        print(json.dumps({"changed": changed}, indent=2))


if __name__ == "__main__":
    main()
