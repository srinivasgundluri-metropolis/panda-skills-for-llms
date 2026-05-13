#!/usr/bin/env bash
# Copy *your* global Cursor / Claude rules and skills into this repo when they are
# missing here. Does not remove or overwrite repo files unless you pass --force.
#
# Defaults to --dry-run (print only). Use --apply to write.
#
# Edit scripts/sync-from-home-exclude.txt to skip third-party or GSD names (globs).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXCLUDE_FILE="${REPO_ROOT}/scripts/sync-from-home-exclude.txt"

DRY_RUN=1
FORCE=0
RULES=1
SKILLS=1
while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply) DRY_RUN=0 ;;
    --dry-run) DRY_RUN=1 ;;
    --force) FORCE=1 ;;
    --rules-only) SKILLS=0 ;;
    --skills-only) RULES=0 ;;
    -h|--help)
      echo "Usage: $0 [--dry-run] | [--apply] [--force] [--rules-only | --skills-only]"
      echo "  Copies missing rules/skills from ~/.cursor and ~/.claude into repo rules/, rules/claude-code/, skills/."
      echo "  Excludes patterns in scripts/sync-from-home-exclude.txt"
      echo "  --rules-only   do not copy skills (useful before you tune excludes)."
      echo "  --skills-only  do not copy rules."
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

excluded() {
  local name="$1"
  [[ ! -f "${EXCLUDE_FILE}" ]] && return 1
  local line pat
  while IFS= read -r line || [[ -n "${line}" ]]; do
    [[ -z "${line// }" || "${line}" =~ ^# ]] && continue
    pat="${line//[[:space:]]/}"
    [[ -z "${pat}" ]] && continue
    if [[ "${name}" == ${pat} ]]; then
      return 0
    fi
  done < "${EXCLUDE_FILE}"
  return 1
}

install_rule() {
  local src=$1 dst=$2
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "[dry-run] install ${src} -> ${dst}"
  else
    mkdir -p "$(dirname "${dst}")"
    install -m 0644 "${src}" "${dst}"
    echo "added: ${dst}"
  fi
}

# --- Cursor rules -> repo rules/*.mdc
if [[ "${RULES}" -ne 1 ]]; then
  echo "(skip rules: --skills-only)"
else
shopt -s nullglob
for src in "${HOME}/.cursor/rules"/*.mdc; do
  base="$(basename "${src}")"
  if excluded "${base}"; then
    echo "skip (exclude): cursor rule ${base}"
    continue
  fi
  dst="${REPO_ROOT}/rules/${base}"
  if [[ -f "${dst}" ]]; then
    if cmp -s "${src}" "${dst}"; then
      echo "ok (same): rules/${base}"
    elif [[ "${FORCE}" -eq 1 ]]; then
      echo "overwrite (--force): rules/${base}"
      install_rule "${src}" "${dst}"
    else
      echo "skip (differs): rules/${base} — use --force to overwrite from ~/.cursor/rules"
    fi
  else
    install_rule "${src}" "${dst}"
  fi
done

# --- Claude rules -> repo rules/claude-code/*.md
for src in "${HOME}/.claude/rules"/*.md; do
  base="$(basename "${src}")"
  if excluded "${base}"; then
    echo "skip (exclude): claude rule ${base}"
    continue
  fi
  dst="${REPO_ROOT}/rules/claude-code/${base}"
  if [[ -f "${dst}" ]]; then
    if cmp -s "${src}" "${dst}"; then
      echo "ok (same): rules/claude-code/${base}"
    elif [[ "${FORCE}" -eq 1 ]]; then
      echo "overwrite (--force): rules/claude-code/${base}"
      install_rule "${src}" "${dst}"
    else
      echo "skip (differs): rules/claude-code/${base} — use --force to overwrite from ~/.claude/rules"
    fi
  else
    install_rule "${src}" "${dst}"
  fi
done
fi

# --- Skills: union of folder names under ~/.cursor/skills and ~/.claude/skills
if [[ "${SKILLS}" -ne 1 ]]; then
  echo "(skip skills: --rules-only)"
else
# (pipe form for macOS /bin/bash 3.2 — no process substitution)
{
  shopt -s nullglob
  for d in "${HOME}/.cursor/skills"/*/; do
    [[ -d "${d}" ]] && basename "${d}"
  done
  for d in "${HOME}/.claude/skills"/*/; do
    [[ -d "${d}" ]] && basename "${d}"
  done
} | sort -u | while IFS= read -r name; do
  [[ -z "${name}" ]] && continue
  if excluded "${name}"; then
    echo "skip (exclude): skill ${name}"
    continue
  fi
  if [[ -d "${REPO_ROOT}/skills/${name}" ]]; then
    echo "ok (exists): skills/${name}/"
    continue
  fi
  src_claude="${HOME}/.claude/skills/${name}/SKILL.md"
  src_cursor="${HOME}/.cursor/skills/${name}/SKILL.md"
  src=""
  if [[ -f "${src_claude}" && -f "${src_cursor}" ]]; then
    if cmp -s "${src_claude}" "${src_cursor}"; then
      src="${src_claude}"
    else
      if [[ "${src_claude}" -nt "${src_cursor}" ]]; then
        src="${src_claude}"
        echo "note: skills/${name} differs between ~/.claude and ~/.cursor; using newer (~/.claude)"
      else
        src="${src_cursor}"
        echo "note: skills/${name} differs between ~/.claude and ~/.cursor; using newer (~/.cursor)"
      fi
    fi
  elif [[ -f "${src_claude}" ]]; then
    src="${src_claude}"
  elif [[ -f "${src_cursor}" ]]; then
    src="${src_cursor}"
  else
    echo "skip (no SKILL.md): ${name}"
    continue
  fi

  dst_dir="${REPO_ROOT}/skills/${name}"
  dst="${dst_dir}/SKILL.md"
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "[dry-run] mkdir -p ${dst_dir} && install ${src} ${dst}"
  else
    mkdir -p "${dst_dir}"
    install -m 0644 "${src}" "${dst}"
    echo "added: skills/${name}/SKILL.md"
  fi
done
fi

if [[ "${DRY_RUN}" -eq 1 ]]; then
  echo ""
  echo "Dry run only. Re-run with: $0 --apply"
fi
