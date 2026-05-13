#!/usr/bin/env bash
# Copy Panda agent rules from this repo into global installs:
#   rules/*.mdc (regular files only; skip symlinks) -> ~/.cursor/rules/
#   rules/claude-code/*.md (regular files only)     -> ~/.claude/rules/
# Run after pulling the repo so Cursor and Claude Code stay in sync.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "${HOME}/.claude/rules" "${HOME}/.cursor/rules"

shopt -s nullglob
for src in "${REPO_ROOT}/rules"/*.mdc; do
  if [[ -L "${src}" ]]; then
    continue
  fi
  base="$(basename "${src}")"
  install -m 0644 "${src}" "${HOME}/.cursor/rules/${base}"
  echo "  -> ${HOME}/.cursor/rules/${base}"
done

for src in "${REPO_ROOT}/rules/claude-code"/*.md; do
  if [[ -L "${src}" ]]; then
    continue
  fi
  base="$(basename "${src}")"
  install -m 0644 "${src}" "${HOME}/.claude/rules/${base}"
  echo "  -> ${HOME}/.claude/rules/${base}"
done

echo "Synced repo rules/ -> ~/.cursor/rules and rules/claude-code/ -> ~/.claude/rules"
