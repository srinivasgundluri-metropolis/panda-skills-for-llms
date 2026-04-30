#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_LOG_PATH = Path.home() / ".cursor" / "ai-tracking" / "skill-usage.jsonl"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Append one skill-usage JSONL event."
    )
    parser.add_argument("--skill-name", required=True, help="Skill name, e.g. spec-driven-development")
    parser.add_argument("--session-id", default="manual", help="Session identifier")
    parser.add_argument("--repo", default="unknown", help="Repository/project name")
    parser.add_argument("--model", default="unknown", help="Model identifier")
    parser.add_argument("--timestamp", default="", help="ISO timestamp (defaults to current UTC)")
    parser.add_argument(
        "--log-path",
        default=str(DEFAULT_LOG_PATH),
        help="Path to JSONL file (default: ~/.cursor/ai-tracking/skill-usage.jsonl)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    event = {
        "timestamp": args.timestamp or utc_now_iso(),
        "skill_name": args.skill_name,
        "session_id": args.session_id,
        "repo": args.repo,
        "model": args.model,
    }

    log_path = Path(args.log_path).expanduser()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, separators=(",", ":")) + "\n")

    print(f"Appended event to {log_path}")


if __name__ == "__main__":
    main()
