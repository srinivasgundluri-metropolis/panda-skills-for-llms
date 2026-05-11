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
    bash_path: str,
    wrapper_script: str,
    repo_root: str,
    python_bin: str,
    port: int,
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
    <string>{bash_path}</string>
    <string>{wrapper_script}</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PANDA_SKILLS_ROOT</key>
    <string>{repo_root}</string>
    <key>SKILL_DASHBOARD_PYTHON</key>
    <string>{python_bin}</string>
    <key>SKILL_DASHBOARD_PORT</key>
    <string>{port}</string>
  </dict>
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


def pick_default_python_bin() -> str:
    conda = Path("/opt/anaconda3/bin/python3")
    if conda.is_file():
        return str(conda)
    return sys.executable


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install launchd LaunchAgent to start the Streamlit skill dashboard at login "
        "and open http://localhost:<port> when the server is ready."
    )
    parser.add_argument(
        "--label",
        default="com.panda.skills.dashboard",
        help="launchd label (default: com.panda.skills.dashboard).",
    )
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parent.parent),
        help="Clone root (default: parent of scripts/).",
    )
    parser.add_argument("--python-bin", default=pick_default_python_bin())
    parser.add_argument("--port", type=int, default=8501)
    parser.add_argument(
        "--bash-bin",
        default="/bin/bash",
        help="bash used to run the wrapper (default: /bin/bash).",
    )
    args = parser.parse_args()

    repo_root = str(Path(args.repo_root).resolve())
    wrapper = str((Path(__file__).resolve().parent / "start_skill_dashboard_launchagent.sh").resolve())
    launch_agents = Path.home() / "Library" / "LaunchAgents"
    launch_agents.mkdir(parents=True, exist_ok=True)

    logs_dir = Path.home() / ".cursor" / "ai-tracking"
    logs_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = str(logs_dir / "streamlit-dashboard-launchd-wrapper.out.log")
    stderr_path = str(logs_dir / "streamlit-dashboard-launchd-wrapper.err.log")

    plist_path = launch_agents / f"{args.label}.plist"
    plist_path.write_text(
        plist_content(
            label=args.label,
            bash_path=args.bash_bin,
            wrapper_script=wrapper,
            repo_root=repo_root,
            python_bin=args.python_bin,
            port=max(1, args.port),
            stdout_path=stdout_path,
            stderr_path=stderr_path,
        )
    )

    subprocess.run(["launchctl", "unload", str(plist_path)], check=False)
    run(["launchctl", "load", str(plist_path)])

    print(f"Installed and loaded: {plist_path}")
    print(f"PANDA_SKILLS_ROOT={repo_root}")
    print(f"Python={args.python_bin} port={args.port}")
    print("Logs: Streamlit → ~/.cursor/ai-tracking/streamlit-dashboard-launchd.log")
    print("      Wrapper stdout/stderr → streamlit-dashboard-launchd-wrapper.{out,err}.log")
    print("Remove: python scripts/uninstall_launch_agent.py --label com.panda.skills.dashboard")


if __name__ == "__main__":
    main()
