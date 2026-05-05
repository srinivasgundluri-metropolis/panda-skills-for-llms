#!/usr/bin/env bash
# Copy Panda skill-tracking "session offer" rules from this repo into global
# Claude Code (~/.claude/rules/) and Cursor (~/.cursor/rules/) installs.
# Run after pulling the repo so pgrep/layout logic stays in sync.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_DST="${HOME}/.claude/rules/skill-tracking-session-offer.md"
CURSOR_DST="${HOME}/.cursor/rules/skill-tracking-session-offer.mdc"
mkdir -p "${HOME}/.claude/rules" "${HOME}/.cursor/rules"
install -m 0644 "${REPO_ROOT}/rules/claude-code/skill-tracking-session-offer.md" "${CLAUDE_DST}"
install -m 0644 "${REPO_ROOT}/rules/skill-tracking-session-offer.mdc" "${CURSOR_DST}"
echo "Synced:"
echo "  -> ${CLAUDE_DST}"
echo "  -> ${CURSOR_DST}"
