# Panda Skills for LLMs

**Lazy like pandas. Efficient like pros.** Reusable skills that turn prompt effort into reliable LLM workflows.

This is a **public, community-maintained collection** that anyone can use, fork, and improve.

## What this repo is

- A curated set of practical agent skills you can copy into your own environment
- A starting point for teams who want shared, reusable skill workflows
- A place for community contributions and iterative improvements

## Repository layout

- `skills/`: reusable skill definitions for agent workflows
- `rules/`: reusable policy/rule files to guide agent behavior (includes optional Cursor `.mdc` and Claude Code reminders under `rules/claude-code/`)
- `templates/spec-driven/`: PRD/UI/TECH/RFC/ADR/traceability/release templates
- `templates/tdd/`: test planning and regression checklist templates
- `dashboard/`: Streamlit analytics app for skill usage
- `scripts/`: utility scripts (for example, event logging)

## Design principles

- LLM-agnostic: content should work regardless of the underlying model
- Runtime-flexible: adapt to Cursor, Claude-style agents, or similar tooling
- Reusable by default: prefer templates and composable workflows over one-off prompts
- Contributor-friendly: keep docs clear, practical, and easy to extend

## How to use

- Copy or adapt the `skills/`, `rules/`, and `templates/` content into your agent setup
- Adjust prompts/instructions for your tooling and team conventions
- Submit improvements back via pull requests

## Skill usage tracking (transcripts → JSONL → dashboard)

This answers: **“Which skills did my agents actually use, and when?”** It does **not** read your whole chat—only lines that reference a skill path or a known skill name from `skills/`.

| Piece | What it does |
| --- | --- |
| **Watcher** | `scripts/auto_track_skill_usage.py` tails transcript files, appends one JSON line per detected skill hit. |
| **Logs** | JSONL files you can back up, merge, or feed to other tools. |
| **Dashboard** | `streamlit run dashboard/app.py` charts and filters those events. |

Set a stable label for your work (replace `YOUR_REPO` with a short name, or use your git remote name):

```bash
export PANDA_SKILLS_ROOT="/absolute/path/to/this/repo"   # optional but handy
export REPO_LABEL="YOUR_REPO"   # used as --repo in examples below; e.g. my-app
```

### Where files go (Cursor vs Claude Code)

| Runtime | Watcher flag | Transcripts (default) | Events JSONL | Offset state (no double-count) |
| --- | --- | --- | --- | --- |
| **Cursor** | `--layout cursor` (default) | `~/.cursor/projects/**/agent-transcripts/**/*.jsonl` | `~/.cursor/ai-tracking/skill-usage.jsonl` | `~/.cursor/ai-tracking/skill-tracker-state.json` |
| **Claude Code** | `--layout claude-code` | `~/.claude/projects/**/*.jsonl` (excludes `memory/`, `tool-results/`) | `~/.claude/ai-tracking/skill-usage.jsonl` | `~/.claude/ai-tracking/skill-tracker-state.json` |

If you set **`CLAUDE_CONFIG_DIR`**, Claude’s paths are under that directory instead of `~/.claude`. Cursor and Claude use **separate** logs so you can run two watchers at once.

### Event format (one JSON object per line)

```json
{"timestamp":"2026-04-30T18:52:00Z","skill_name":"spec-driven-development","session_id":"abc123","repo":"YOUR_REPO","model":"cursor"}
```

### Quick start

1. **Install dashboard dependencies**

   ```bash
   pip install -r dashboard/requirements.txt
   ```

2. **Ingest history once, then keep watching (Cursor example)**

   From the repo root (or use `$PANDA_SKILLS_ROOT`):

   ```bash
   python scripts/auto_track_skill_usage.py --once --repo "$REPO_LABEL" --model cursor
   python scripts/auto_track_skill_usage.py --repo "$REPO_LABEL" --model cursor --interval-seconds 5
   ```

3. **Open the dashboard**

   ```bash
   streamlit run dashboard/app.py
   ```

   By default the primary file is `~/.cursor/ai-tracking/skill-usage.jsonl`.

4. **Claude Code (second process, does not touch Cursor files)**

   ```bash
   python scripts/auto_track_skill_usage.py \
     --layout claude-code \
     --repo "$REPO_LABEL" \
     --model claude-code \
     --interval-seconds 5
   ```

   Omit `--log-path` / `--state-path` to keep defaults under `~/.claude/ai-tracking/`.

5. **See both tools in one dashboard**

   Sidebar: primary = Cursor JSONL, **Additional log paths** = `~/.claude/ai-tracking/skill-usage.jsonl`.

Transcript layout reference: [Claude Code application data](https://code.claude.com/docs/en/claude-directory.md#application-data).

### Dashboard metrics

- **Total invocations**: events matching current filters.
- **Invocations today**: events on the latest calendar day in the filtered data (UTC by ingestion timestamps).
- **Unique skills / sessions / repos**: distinct values in the filtered set.

### Screenshot

![Panda Skills Analytics Full View](assets/skills-analytics-fullpage.png)

### Manual log line (testing)

```bash
python scripts/log_skill_event.py \
  --skill-name spec-driven-development \
  --session-id demo-001 \
  --repo "$REPO_LABEL" \
  --model gpt-5.3-codex
```

### Optional: have the agent offer to start tracking every new session

Copy the versioned templates from this repo into your **global** config (not per-project), then new chats will be nudged to start the watcher if you want it.

| Product | Copy this file | To |
| --- | --- | --- |
| **Cursor** | `rules/skill-tracking-session-offer.mdc` | `~/.cursor/rules/` (same filename; `alwaysApply: true` is already set) |
| **Claude Code** | `rules/claude-code/skill-tracking-session-offer.md` | `~/.claude/rules/` |

Set `PANDA_SKILLS_ROOT` in your shell profile so the agent can run `"$PANDA_SKILLS_ROOT/scripts/auto_track_skill_usage.py"` without guessing. The rules only **prompt** the assistant; they do not start processes by themselves.

### Auto-start on macOS (Cursor watcher only)

```bash
python scripts/install_launch_agent.py --repo "$REPO_LABEL" --model cursor
```

Uninstall: `python scripts/uninstall_launch_agent.py`

### Troubleshooting

- **Empty dashboard**: run `--once`, confirm the JSONL path in the sidebar exists and has lines.
- **No new events**: confirm the watcher is running; for non-default transcript locations use `--transcripts-root`.
- **Reset and re-scan**: delete the JSONL **and** the matching `skill-tracker-state.json` for that runtime, then run `--once` again (you will re-emit events for all matching lines in existing transcripts).
- **Two Cursor watchers**: avoid running `launchd` and a manual Cursor watcher with the same log without intending duplicates.

## Contributing

Contributions are welcome.

- Add new high-quality skills with clear scope and usage guidance
- Improve existing skill prompts, safety checks, and examples
- Keep skills focused, testable, and easy to understand

When opening a PR, include:

- What changed and why
- How you validated the skill behavior
- Any compatibility notes (Cursor/Claude/tooling assumptions)

## License

License terms are **pending internal review**. Until published otherwise, treat this repository as **not open source**—no permission is granted to use, copy, or distribute the contents.

Contact your Metropolis engineering or legal contact for questions.
