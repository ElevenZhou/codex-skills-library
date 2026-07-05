#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if command -v rg >/dev/null 2>&1; then
  if rg -n --hidden \
    --glob '!/.git/**' \
    --glob '!*.png' \
    --glob '!*.jpg' \
    --glob '!*.jpeg' \
    --glob '!*.webp' \
    --glob '!*.pdf' \
    'sk-[A-Za-z0-9_-]{20,}|OPENAI_API_KEY\s*=|ANTHROPIC_API_KEY\s*=|GITHUB_TOKEN\s*=|password\s*=' \
    "$REPO_ROOT"; then
    echo "Potential secret found. Review before committing." >&2
    exit 1
  fi
else
  echo "rg not found; skipping fast secret scan." >&2
fi

echo "No obvious secrets found."

