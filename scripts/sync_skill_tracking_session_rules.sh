#!/usr/bin/env bash
# Copy Panda agent rules from this repo into global installs (always applies).
# Delegates to sync_repo_skills_to_global.sh --apply --rules-only.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec bash "${REPO_ROOT}/scripts/sync_repo_skills_to_global.sh" --apply --rules-only
