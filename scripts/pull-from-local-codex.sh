#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
SOURCE="$CODEX_HOME_DIR/skills"

mkdir -p "$REPO_ROOT/skills"

rsync -a --delete \
  --exclude '.system' \
  --exclude '.DS_Store' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  "$SOURCE/" "$REPO_ROOT/skills/"

echo "Pulled skills from $SOURCE"

