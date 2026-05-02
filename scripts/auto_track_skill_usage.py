#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_LOG_PATH = Path.home() / ".cursor" / "ai-tracking" / "skill-usage.jsonl"
DEFAULT_STATE_PATH = Path.home() / ".cursor" / "ai-tracking" / "skill-tracker-state.json"
DEFAULT_TRANSCRIPTS_GLOB_CURSOR = "**/agent-transcripts/**/*.jsonl"
# Paths under ~/.claude/projects/ to ignore when layout=claude-code (not session transcripts).
CLAUDE_TRANSCRIPT_EXCLUDE_DIR_NAMES = frozenset({"memory", "tool-results"})
DEFAULT_SKILLS_DIR = (Path(__file__).resolve().parent.parent / "skills")

LAYOUT_CURSOR = "cursor"
LAYOUT_CLAUDE_CODE = "claude-code"

SKILL_PATTERNS = [
    re.compile(r"/skills/([^/]+)/SKILL\.md"),
    re.compile(r"\\.claude/skills/([^/]+)/SKILL\.md"),
]

EXCLUDE_SNIPPETS = [
    "/plugins/cache/",
    "/.cursor/plugins/cache/",
    "/.claude/plugins/cache/",
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def default_claude_config_home() -> Path:
    override = os.environ.get("CLAUDE_CONFIG_DIR", "").strip()
    if override:
        return Path(override).expanduser()
    return Path.home() / ".claude"


def default_claude_projects_root() -> Path:
    return default_claude_config_home() / "projects"


def default_claude_skill_log_and_state() -> tuple[Path, Path]:
    """Skill usage JSONL + offset state under ~/.claude/ai-tracking (or CLAUDE_CONFIG_DIR)."""
    base = default_claude_config_home() / "ai-tracking"
    return base / "skill-usage.jsonl", base / "skill-tracker-state.json"


def load_state(path: Path) -> dict[str, dict[str, int]]:
    if not path.exists():
        return {"offsets": {}}
    try:
        data = json.loads(path.read_text())
        if isinstance(data, dict) and isinstance(data.get("offsets"), dict):
            return data
    except Exception:
        pass
    return {"offsets": {}}


def save_state(path: Path, state: dict[str, dict[str, int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2))


def _path_contains_excluded_dir(path: Path, excluded: frozenset[str]) -> bool:
    return bool(excluded.intersection({p.lower() for p in path.parts}))


def discover_transcripts(root: Path, layout: str) -> list[Path]:
    if layout == LAYOUT_CLAUDE_CODE:
        found: list[Path] = []
        for p in sorted(root.glob("**/*.jsonl")):
            if not p.is_file():
                continue
            if _path_contains_excluded_dir(p, CLAUDE_TRANSCRIPT_EXCLUDE_DIR_NAMES):
                continue
            found.append(p)
        return found
    return sorted(root.glob(DEFAULT_TRANSCRIPTS_GLOB_CURSOR))


def load_known_skills(skills_dir: Path) -> set[str]:
    if not skills_dir.exists():
        return set()
    return {p.name for p in skills_dir.iterdir() if p.is_dir()}


def is_valid_skill_name(skill: str) -> bool:
    if not skill:
        return False
    if "<" in skill or ">" in skill:
        return False
    return bool(re.fullmatch(r"[a-zA-Z0-9._-]+", skill))


def extract_path_skills(raw_line: str) -> set[str]:
    skills: set[str] = set()
    if any(x in raw_line for x in EXCLUDE_SNIPPETS):
        return skills
    for pattern in SKILL_PATTERNS:
        for match in pattern.findall(raw_line):
            if match and is_valid_skill_name(match):
                skills.add(match)
    return skills


def extract_named_skills(raw_line: str, known_skills: set[str]) -> set[str]:
    # Only attempt mention parsing when line likely discusses skills.
    lowered = raw_line.lower()
    if "skill" not in lowered and "invoke" not in lowered and "use " not in lowered:
        return set()

    found: set[str] = set()
    for skill in known_skills:
        if not is_valid_skill_name(skill):
            continue
        pattern = re.compile(rf"(?<![A-Za-z0-9._-]){re.escape(skill)}(?![A-Za-z0-9._-])")
        if pattern.search(raw_line):
            found.add(skill)
    return found


def infer_session_id(file_path: Path, layout: str) -> str:
    if layout == LAYOUT_CLAUDE_CODE:
        # Session transcript files are named <session-id>.jsonl under each project folder.
        return file_path.stem
    # Cursor: parent folder is the transcript UUID.
    if file_path.parent.name:
        return file_path.parent.name
    return file_path.stem


def process_new_lines(
    transcript_file: Path,
    old_offset: int,
    log_path: Path,
    repo_name: str,
    model_name: str,
    known_skills: set[str],
    layout: str,
) -> tuple[int, int]:
    file_size = transcript_file.stat().st_size
    offset = min(old_offset, file_size)
    events_written = 0

    with transcript_file.open("r", encoding="utf-8", errors="ignore") as src:
        src.seek(offset)
        new_data = src.read()
        new_offset = src.tell()

    if not new_data:
        return new_offset, events_written

    session_id = infer_session_id(transcript_file, layout)
    lines = new_data.splitlines()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as out:
        for line in lines:
            path_skills = extract_path_skills(line)
            named_skills = extract_named_skills(line, known_skills)
            all_skills = sorted(path_skills | named_skills)
            if not all_skills:
                continue
            for skill in all_skills:
                detection = "path" if skill in path_skills else "mention"
                event = {
                    "timestamp": utc_now_iso(),
                    "skill_name": skill,
                    "session_id": session_id,
                    "repo": repo_name,
                    "model": model_name,
                    "source": "transcript-watcher",
                    "detection": detection,
                    "transcript_file": str(transcript_file),
                }
                out.write(json.dumps(event, separators=(",", ":")) + "\n")
                events_written += 1

    return new_offset, events_written


def run_once(
    transcripts_root: Path,
    log_path: Path,
    state_path: Path,
    repo_name: str,
    model_name: str,
    known_skills: set[str],
    layout: str,
) -> int:
    state = load_state(state_path)
    offsets: dict[str, int] = state.get("offsets", {})
    total_events = 0

    for transcript_file in discover_transcripts(transcripts_root, layout):
        key = str(transcript_file)
        old_offset = int(offsets.get(key, 0))
        new_offset, events = process_new_lines(
            transcript_file=transcript_file,
            old_offset=old_offset,
            log_path=log_path,
            repo_name=repo_name,
            model_name=model_name,
            known_skills=known_skills,
            layout=layout,
        )
        offsets[key] = new_offset
        total_events += events

    state["offsets"] = offsets
    save_state(state_path, state)
    return total_events


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Auto-track skill usage from agent transcript files (Cursor, Claude Code, similar)."
    )
    parser.add_argument(
        "--layout",
        choices=(LAYOUT_CURSOR, LAYOUT_CLAUDE_CODE),
        default=LAYOUT_CURSOR,
        help=(
            "Transcript layout: "
            f"'{LAYOUT_CURSOR}' expects **/agent-transcripts/**/*.jsonl under --transcripts-root; "
            f"'{LAYOUT_CLAUDE_CODE}' expects session *.jsonl under ~/.claude/projects (see docs)."
        ),
    )
    parser.add_argument(
        "--transcripts-root",
        default=None,
        help=(
            "Root to scan for transcripts. Default: ~/.cursor/projects when layout=cursor, "
            "or ~/.claude/projects when layout=claude-code."
        ),
    )
    parser.add_argument(
        "--log-path",
        default=None,
        help=(
            "JSONL output path. Default: ~/.cursor/ai-tracking/skill-usage.jsonl for layout=cursor; "
            "~/.claude/ai-tracking/skill-usage.jsonl for layout=claude-code (honors CLAUDE_CONFIG_DIR)."
        ),
    )
    parser.add_argument(
        "--state-path",
        default=None,
        help=(
            "Offset state path. Default: ~/.cursor/ai-tracking/skill-tracker-state.json for cursor; "
            "~/.claude/ai-tracking/skill-tracker-state.json for claude-code."
        ),
    )
    parser.add_argument("--repo", default="unknown", help="Repo/project label for events.")
    parser.add_argument("--model", default="unknown", help="Model label for events.")
    parser.add_argument(
        "--skills-dir",
        default=str(DEFAULT_SKILLS_DIR),
        help="Skills directory used for mention-based detection.",
    )
    parser.add_argument(
        "--interval-seconds",
        type=int,
        default=5,
        help="Polling interval when running in watch mode.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Process currently available transcript updates once and exit.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    layout: str = args.layout
    if args.transcripts_root:
        transcripts_root = Path(args.transcripts_root).expanduser()
    elif layout == LAYOUT_CLAUDE_CODE:
        transcripts_root = default_claude_projects_root()
    else:
        transcripts_root = Path.home() / ".cursor" / "projects"

    if args.log_path is not None:
        log_path = Path(args.log_path).expanduser()
    elif layout == LAYOUT_CLAUDE_CODE:
        log_path, _ = default_claude_skill_log_and_state()
    else:
        log_path = DEFAULT_LOG_PATH

    if args.state_path is not None:
        state_path = Path(args.state_path).expanduser()
    elif layout == LAYOUT_CLAUDE_CODE:
        _, state_path = default_claude_skill_log_and_state()
    else:
        state_path = DEFAULT_STATE_PATH
    skills_dir = Path(args.skills_dir).expanduser()
    known_skills = load_known_skills(skills_dir)

    if args.once:
        events = run_once(
            transcripts_root,
            log_path,
            state_path,
            args.repo,
            args.model,
            known_skills,
            layout,
        )
        print(f"Processed once. New events written: {events}")
        return

    print(f"Layout: {layout}")
    print(f"Watching transcripts under: {transcripts_root}")
    print(f"Using skills directory: {skills_dir}")
    print(f"Writing events to: {log_path}")
    print(f"State file: {state_path}")
    while True:
        events = run_once(
            transcripts_root,
            log_path,
            state_path,
            args.repo,
            args.model,
            known_skills,
            layout,
        )
        if events:
            print(f"[{utc_now_iso()}] wrote {events} new event(s)")
        time.sleep(max(1, args.interval_seconds))


if __name__ == "__main__":
    main()
