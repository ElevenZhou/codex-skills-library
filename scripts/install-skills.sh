#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
TARGET="$CODEX_HOME_DIR/skills"

mkdir -p "$TARGET"

if [[ "$#" -eq 0 || "${1:-}" == "--all" ]]; then
  rsync -a --delete \
    --exclude '.system' \
    --exclude '.DS_Store' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    "$REPO_ROOT/skills/" "$TARGET/"
  echo "Installed all skills to $TARGET"
  exit 0
fi

for skill in "$@"; do
  if [[ ! -d "$REPO_ROOT/skills/$skill" ]]; then
    echo "Skill not found: $skill" >&2
    echo "Available skills:" >&2
    find "$REPO_ROOT/skills" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort >&2
    exit 1
  fi
  rsync -a --delete \
    --exclude '.DS_Store' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    "$REPO_ROOT/skills/$skill/" "$TARGET/$skill/"
  echo "Installed skill: $skill"
done

echo "Target: $TARGET"
