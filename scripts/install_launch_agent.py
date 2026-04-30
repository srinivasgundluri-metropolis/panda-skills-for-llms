#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def plist_content(
    label: str,
    python_bin: str,
    tracker_script: str,
    repo: str,
    model: str,
    interval_seconds: int,
    stdout_path: str,
    stderr_path: str,
) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>{label}</string>
  <key>ProgramArguments</key>
  <array>
    <string>{python_bin}</string>
    <string>{tracker_script}</string>
    <string>--repo</string>
    <string>{repo}</string>
    <string>--model</string>
    <string>{model}</string>
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
    parser = argparse.ArgumentParser(description="Install launchd service for auto skill tracking.")
    parser.add_argument("--label", default="com.panda.skills.tracker")
    parser.add_argument("--repo", default="panda-skills-for-llms")
    parser.add_argument("--model", default="unknown")
    parser.add_argument("--interval-seconds", type=int, default=5)
    parser.add_argument(
        "--tracker-script",
        default=str((Path(__file__).resolve().parent / "auto_track_skill_usage.py")),
    )
    parser.add_argument("--python-bin", default=sys.executable)
    args = parser.parse_args()

    launch_agents = Path.home() / "Library" / "LaunchAgents"
    launch_agents.mkdir(parents=True, exist_ok=True)
    logs_dir = Path.home() / ".cursor" / "ai-tracking"
    logs_dir.mkdir(parents=True, exist_ok=True)

    plist_path = launch_agents / f"{args.label}.plist"
    stdout_path = logs_dir / "skill-tracker-launchd.out.log"
    stderr_path = logs_dir / "skill-tracker-launchd.err.log"

    plist_path.write_text(
        plist_content(
            label=args.label,
            python_bin=args.python_bin,
            tracker_script=args.tracker_script,
            repo=args.repo,
            model=args.model,
            interval_seconds=max(1, args.interval_seconds),
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
        )
    )

    # Best effort unload first, then load.
    subprocess.run(["launchctl", "unload", str(plist_path)], check=False)
    run(["launchctl", "load", str(plist_path)])

    print(f"Installed and loaded: {plist_path}")
    print("Service will auto-start on login.")


if __name__ == "__main__":
    main()
