#!/usr/bin/env bash
# Copy skills from this repo's skills/ tree into global Cursor and Claude skill dirs.
#
# Defaults to --dry-run. Use --apply to write. Use --force to overwrite when SKILL.md differs.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_SRC="${REPO_ROOT}/skills"

DRY_RUN=1
FORCE=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply) DRY_RUN=0 ;;
    --dry-run) DRY_RUN=1 ;;
    --force) FORCE=1 ;;
    -h|--help)
      echo "Usage: $0 [--dry-run] | [--apply] [--force]"
      echo "  Copies each skills/<name>/ into ~/.cursor/skills/<name>/ and ~/.claude/skills/<name>/."
      echo "  Without --force, skips when destination SKILL.md exists and differs from repo (use --force to overwrite)."
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

sync_one_dest() {
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

shopt -s nullglob
for src_dir in "${SKILLS_SRC}"/*/; do
  [[ -d "${src_dir}" ]] || continue
  name="$(basename "${src_dir}")"
  sync_one_dest "${HOME}/.cursor/skills" "${name}"
  sync_one_dest "${HOME}/.claude/skills" "${name}"
done

if [[ "${DRY_RUN}" -eq 1 ]]; then
  echo ""
  echo "Dry run only. Re-run with: $0 --apply"
fi
