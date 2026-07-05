#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

printf "%-28s %-34s %s\n" "SKILL" "DISPLAY NAME" "DESCRIPTION"
printf "%-28s %-34s %s\n" "-----" "------------" "-----------"

for skill_dir in "$REPO_ROOT"/skills/*; do
  [[ -d "$skill_dir" ]] || continue
  skill="$(basename "$skill_dir")"
  display="$skill"
  if [[ -f "$skill_dir/agents/openai.yaml" ]]; then
    parsed="$(awk -F': ' '/display_name:/ {gsub(/"/, "", $2); print $2; exit}' "$skill_dir/agents/openai.yaml")"
    [[ -n "$parsed" ]] && display="$parsed"
  fi
  desc=""
  if [[ -f "$skill_dir/SKILL.md" ]]; then
    desc="$(awk -F'description: ' '/^description:/ {gsub(/^"|"$/, "", $2); print $2; exit}' "$skill_dir/SKILL.md")"
  fi
  printf "%-28s %-34s %s\n" "$skill" "$display" "$desc"
done
