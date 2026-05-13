#!/usr/bin/env bash
# Copy Panda skills and/or rules from this repo into global Cursor and Claude dirs.
#
# Defaults to --dry-run. Use --apply to write. Use --force to overwrite when a file differs.
#
# Skills:  each skills/<name>/  -> ~/.cursor/skills/<name>/ and ~/.claude/skills/<name>/ (rsync)
# Rules:   rules/*.mdc         -> ~/.cursor/rules/   (regular files; skip symlinks)
#           rules/claude-code/*.md -> ~/.claude/rules/
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_SRC="${REPO_ROOT}/skills"
RULES_CURSOR_SRC="${REPO_ROOT}/rules"
RULES_CLAUDE_SRC="${REPO_ROOT}/rules/claude-code"

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
      echo "  Skills: rsync each repo skills/<name>/ to ~/.cursor/skills/ and ~/.claude/skills/."
      echo "  Rules:  install rules/*.mdc -> ~/.cursor/rules/; rules/claude-code/*.md -> ~/.claude/rules/."
      echo "  Without --force, skips when a destination file exists and differs (use --force to overwrite)."
      echo "  Default: sync both rules and skills. --rules-only / --skills-only restrict scope."
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

install_one_rule() {
  local src=$1
  local dst=$2
  local label=$3

  if [[ -L "${src}" ]]; then
    echo "skip (symlink): ${label}"
    return
  fi
  if [[ ! -f "${src}" ]]; then
    return
  fi

  if [[ -f "${dst}" ]] && ! cmp -s "${src}" "${dst}" && [[ "${FORCE}" -ne 1 ]]; then
    echo "skip (differs, use --force): ${label}"
    return
  fi

  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "[dry-run] install ${src} -> ${dst}"
    return
  fi

  mkdir -p "$(dirname "${dst}")"
  install -m 0644 "${src}" "${dst}"
  echo "synced: ${label}"
}

sync_rules() {
  if [[ "${RULES}" -ne 1 ]]; then
    echo "(skip rules: --skills-only)"
    return
  fi

  echo "== Rules: repo -> global =="
  shopt -s nullglob
  for src in "${RULES_CURSOR_SRC}"/*.mdc; do
    base="$(basename "${src}")"
    install_one_rule "${src}" "${HOME}/.cursor/rules/${base}" "cursor rules/${base}"
  done

  for src in "${RULES_CLAUDE_SRC}"/*.md; do
    base="$(basename "${src}")"
    install_one_rule "${src}" "${HOME}/.claude/rules/${base}" "claude rules/${base}"
  done
}

sync_one_skill_dest() {
  local dest_root=$1
  local name=$2
  local src_dir="${SKILLS_SRC}/${name}"
  local dst_dir="${dest_root}/${name}"
  local src_md="${src_dir}/SKILL.md"
  local dst_md="${dst_dir}/SKILL.md"

  if [[ ! -f "${src_md}" ]]; then
    echo "skip (no repo SKILL.md): ${name}"
    return
  fi

  if [[ -f "${dst_md}" ]] && ! cmp -s "${src_md}" "${dst_md}" && [[ "${FORCE}" -ne 1 ]]; then
    echo "skip (differs, use --force): ${dest_root##*/} skills/${name}/SKILL.md"
    return
  fi

  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "[dry-run] rsync ${src_dir}/ -> ${dst_dir}/"
    return
  fi

  mkdir -p "${dst_dir}"
  rsync -a "${src_dir}/" "${dst_dir}/"
  echo "synced: ${name} -> ${dst_dir}"
}

sync_skills() {
  if [[ "${SKILLS}" -ne 1 ]]; then
    echo "(skip skills: --rules-only)"
    return
  fi

  echo "== Skills: repo -> global =="
  shopt -s nullglob
  for src_dir in "${SKILLS_SRC}"/*/; do
    [[ -d "${src_dir}" ]] || continue
    name="$(basename "${src_dir}")"
    sync_one_skill_dest "${HOME}/.cursor/skills" "${name}"
    sync_one_skill_dest "${HOME}/.claude/skills" "${name}"
  done
}

sync_rules
sync_skills

if [[ "${DRY_RUN}" -eq 1 ]]; then
  echo ""
  echo "Dry run only. Re-run with: $0 --apply"
fi
