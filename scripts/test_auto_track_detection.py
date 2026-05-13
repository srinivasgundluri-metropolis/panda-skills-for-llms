#!/usr/bin/env python3
"""Unit tests for structured-only skill detection. Run: python3 scripts/test_auto_track_detection.py"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parent / "auto_track_skill_usage.py"
_spec = importlib.util.spec_from_file_location("auto_track_skill_usage", _SCRIPT)
assert _spec and _spec.loader
atu = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(atu)


def _process_one_line(line: str, *, layout: str = atu.LAYOUT_CURSOR) -> list[dict]:
    with tempfile.TemporaryDirectory() as td:
        tdir = Path(td)
        session = tdir / "fake-session-uuid"
        session.mkdir()
        transcript = session / "0.jsonl"
        transcript.write_text(line + "\n", encoding="utf-8")
        log_path = tdir / "out.jsonl"
        new_off, n = atu.process_new_lines(
            transcript_file=transcript,
            old_offset=0,
            log_path=log_path,
            agent_label="cursor",
            layout=layout,
        )
        assert new_off > 0
        if not log_path.exists():
            return []
        return [json.loads(x) for x in log_path.read_text(encoding="utf-8").strip().splitlines() if x.strip()]


class DetectionTests(unittest.TestCase):
    def test_ignores_path_only_line(self) -> None:
        line = '{"x": "home/.cursor/skills/clean-up-repo/SKILL.md"}'
        events = _process_one_line(line)
        self.assertEqual(events, [])

    def test_logs_skill_tool(self) -> None:
        payload = {"type": "tool_use", "name": "Skill", "input": {"skill": "open-pr"}}
        line = json.dumps(payload)
        events = _process_one_line(line)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["skill_name"], "open-pr")
        self.assertEqual(events[0]["detection"], "tool_use")


if __name__ == "__main__":
    unittest.main()
