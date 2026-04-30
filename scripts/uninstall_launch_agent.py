#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Uninstall launchd service for auto skill tracking.")
    parser.add_argument("--label", default="com.panda.skills.tracker")
    args = parser.parse_args()

    plist_path = Path.home() / "Library" / "LaunchAgents" / f"{args.label}.plist"
    if plist_path.exists():
        subprocess.run(["launchctl", "unload", str(plist_path)], check=False)
        plist_path.unlink()
        print(f"Uninstalled: {plist_path}")
    else:
        print(f"No plist found at: {plist_path}")


if __name__ == "__main__":
    main()
