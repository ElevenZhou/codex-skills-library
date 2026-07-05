#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
TARGET="$CODEX_HOME_DIR/skills"

mkdir -p "$TARGET"

rsync -a --delete \
  --exclude '.system' \
  --exclude '.DS_Store' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  "$REPO_ROOT/skills/" "$TARGET/"

echo "Installed skills to $TARGET"

