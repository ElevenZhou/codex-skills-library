#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
SOURCE="$CODEX_HOME_DIR/skills"

mkdir -p "$REPO_ROOT/skills"

# Usage: pull-from-local-codex.sh [skill ...]
# With no arguments, pulls every local skill that already exists in the repo.
# Skills present only in the repo are never deleted; new local skills must be
# named explicitly so private/local-only skills are not committed by accident.
if [[ "$#" -eq 0 ]]; then
  for skill_dir in "$REPO_ROOT"/skills/*/; do
    skill="$(basename "$skill_dir")"
    if [[ -d "$SOURCE/$skill" ]]; then
      set -- "$@" "$skill"
    fi
  done
fi

for skill in "$@"; do
  if [[ ! -d "$SOURCE/$skill" ]]; then
    echo "Local skill not found: $SOURCE/$skill" >&2
    exit 1
  fi
  rsync -a --delete \
    --exclude '.DS_Store' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '*.tmp' \
    --exclude '*.new.md' \
    "$SOURCE/$skill/" "$REPO_ROOT/skills/$skill/"
  echo "Pulled skill: $skill"
done

echo "Source: $SOURCE"

