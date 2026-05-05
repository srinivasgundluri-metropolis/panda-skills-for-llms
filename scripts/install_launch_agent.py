#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def default_claude_ai_tracking_dir() -> Path:
    """Log directory for launchd stdout/stderr (matches Claude Code skill logs)."""
    override = os.environ.get("CLAUDE_CONFIG_DIR", "").strip()
    root = Path(override).expanduser() if override else Path.home() / ".claude"
    return root / "ai-tracking"


def ai_tracking_dir_for_layout(layout: str) -> Path:
    """launchd stdout/stderr: same tree as skill JSONL for that layout."""
    if layout == "cursor":
        return Path.home() / ".cursor" / "ai-tracking"
    return default_claude_ai_tracking_dir()


def plist_content(
    label: str,
    python_bin: str,
    tracker_script: str,
    layout: str,
    agent: str,
    interval_seconds: int,
    stdout_path: str,
    stderr_path: str,
) -> str:
    layout_args = f"""
    <string>--layout</string>
    <string>{layout}</string>"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>{label}</string>
  <key>ProgramArguments</key>
  <array>
    <string>{python_bin}</string>
    <string>{tracker_script}</string>{layout_args}
    <string>--agent</string>
    <string>{agent}</string>
    <string>--interval-seconds</string>
    <string>{interval_seconds}</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>{stdout_path}</string>
  <key>StandardErrorPath</key>
  <string>{stderr_path}</string>
</dict>
</plist>
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install launchd service for skill usage tracking (auto_track_skill_usage.py). "
        "Run once for Claude Code (default) and once with --layout cursor for Cursor."
    )
    parser.add_argument(
        "--layout",
        choices=("claude-code", "cursor"),
        default="claude-code",
        help="Transcript layout (default: claude-code). Use cursor for Cursor agent-transcripts.",
    )
    parser.add_argument(
        "--label",
        default=None,
        help="launchd label (default: com.panda.skills.claude-code or com.panda.skills.cursor by layout).",
    )
    parser.add_argument(
        "--agent",
        default=None,
        help="Agent label in JSONL (default: claude-code or cursor by layout).",
    )
    parser.add_argument("--interval-seconds", type=int, default=5)
    parser.add_argument(
        "--tracker-script",
        default=str((Path(__file__).resolve().parent / "auto_track_skill_usage.py")),
    )
    parser.add_argument("--python-bin", default=sys.executable)
    args = parser.parse_args()
    layout = args.layout
    label = args.label or (
        "com.panda.skills.cursor" if layout == "cursor" else "com.panda.skills.claude-code"
    )
    agent = args.agent or ("cursor" if layout == "cursor" else "claude-code")

    launch_agents = Path.home() / "Library" / "LaunchAgents"
    launch_agents.mkdir(parents=True, exist_ok=True)
    logs_dir = ai_tracking_dir_for_layout(layout)
    logs_dir.mkdir(parents=True, exist_ok=True)

    plist_path = launch_agents / f"{label}.plist"
    stdout_path = logs_dir / "skill-tracker-launchd.out.log"
    stderr_path = logs_dir / "skill-tracker-launchd.err.log"

    plist_path.write_text(
        plist_content(
            label=label,
            python_bin=args.python_bin,
            tracker_script=args.tracker_script,
            layout=layout,
            agent=agent,
            interval_seconds=max(1, args.interval_seconds),
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
        )
    )

    # Best effort unload first, then load.
    subprocess.run(["launchctl", "unload", str(plist_path)], check=False)
    run(["launchctl", "load", str(plist_path)])

    print(f"Installed and loaded: {plist_path}")
    print(f"Layout={layout} agent={agent} interval={args.interval_seconds}s")
    if layout == "cursor":
        print("Writes Cursor skill usage under ~/.cursor/ai-tracking/ by default.")
    else:
        print("Writes Claude Code skill usage under ~/.claude/ai-tracking/ by default (honors CLAUDE_CONFIG_DIR).")


if __name__ == "__main__":
    main()
