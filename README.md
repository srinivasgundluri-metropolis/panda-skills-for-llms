# Panda Skills for LLMs

**Lazy like pandas. Efficient like pros.** Reusable skills that turn prompt effort into reliable LLM workflows.

This is a **public, community-maintained collection** that anyone can use, fork, and improve.

## What this repo is

- A curated set of practical agent skills you can copy into your own environment
- A starting point for teams who want shared, reusable skill workflows
- A place for community contributions and iterative improvements

## Repository layout

- `skills/`: reusable skill definitions for agent workflows
- `rules/`: reusable policy/rule files to guide agent behavior
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

## Skill Usage Tracking (Dashboard + Events)

The tracking system has two parts:

1. **Event producer**: writes skill-usage events to JSONL
2. **Streamlit dashboard**: reads that JSONL and visualizes usage

### Event format

Expected JSONL shape per line:

```json
{"timestamp":"2026-04-30T18:52:00Z","skill_name":"spec-driven-development","session_id":"abc123","repo":"panda-skills-for-llms","model":"gpt-5.3-codex"}
```

### Quick start (recommended)

1) Install dashboard dependencies:

```bash
pip install -r dashboard/requirements.txt
```

2) Backfill existing transcripts once:

```bash
python scripts/auto_track_skill_usage.py \
  --once \
  --repo panda-skills-for-llms \
  --model cursor
```

3) Start continuous tracking:

```bash
python scripts/auto_track_skill_usage.py \
  --repo panda-skills-for-llms \
  --model cursor \
  --interval-seconds 5
```

4) Run dashboard:

```bash
streamlit run dashboard/app.py
```

By default the dashboard reads: `~/.cursor/ai-tracking/skill-usage.jsonl`

### Dashboard metric definitions

- **Total invocations**: total number of events in the currently selected filters (date range, repo, model).
- **Invocations today**: number of events on the most recent day present in the filtered dataset.
- **Unique skills / sessions / repos**: distinct counts within the currently filtered dataset.

### Dashboard screenshots

![Panda Skills Analytics Full View](assets/skills-analytics-fullpage.png)

### Log helper

Use `scripts/log_skill_event.py` to append valid events quickly:

```bash
python scripts/log_skill_event.py \
  --skill-name spec-driven-development \
  --session-id demo-001 \
  --repo panda-skills-for-llms \
  --model gpt-5.3-codex
```

### Automated tracking (recommended)

Use `scripts/auto_track_skill_usage.py` to automatically watch agent transcripts and append skill events.

One-time ingest of current transcript history:

```bash
python scripts/auto_track_skill_usage.py \
  --once \
  --repo panda-skills-for-llms \
  --model gpt-5.3-codex
```

Continuous watch mode:

```bash
python scripts/auto_track_skill_usage.py \
  --repo panda-skills-for-llms \
  --model gpt-5.3-codex \
  --interval-seconds 5
```

Notes:
- The watcher reads transcript JSONL files and detects:
  - explicit `skills/<name>/SKILL.md` references, and
  - explicit skill-name mentions (using known skill folders from `skills/`).
- It stores per-file offsets in `~/.cursor/ai-tracking/skill-tracker-state.json` to avoid double counting.
- It writes events to `~/.cursor/ai-tracking/skill-usage.jsonl`, which the dashboard already reads.
- Use `--transcripts-root` if your agent stores transcripts in a non-default location.

#### Claude Code alongside Cursor

Claude Code reads transcripts from **`~/.claude/projects`** (session `*.jsonl` files). Skill usage events belong under **`~/.claude/ai-tracking/`**, separate from Cursor’s **`~/.cursor/ai-tracking/`**.

Keep the Cursor watcher unchanged. Run a **second** process for Claude Code; with `--layout claude-code`, **omit** `--log-path` / `--state-path` to use the Claude defaults:

```bash
python scripts/auto_track_skill_usage.py \
  --layout claude-code \
  --repo panda-skills-for-llms \
  --model claude-code \
  --interval-seconds 5
```

That writes `~/.claude/ai-tracking/skill-usage.jsonl` and `~/.claude/ai-tracking/skill-tracker-state.json`. If you use `CLAUDE_CONFIG_DIR`, both transcript scanning and these paths resolve under that directory (same as Claude’s own config layout).

The Streamlit sidebar can **merge** logs: primary = `~/.cursor/ai-tracking/skill-usage.jsonl`, “Additional log paths” = `~/.claude/ai-tracking/skill-usage.jsonl` (or clear the extra box to view one source).

See Claude’s [application data](https://code.claude.com/docs/en/claude-directory.md#application-data) for where transcripts live.

### Auto-start on macOS (launchd)

Install and start tracker at login:

```bash
python scripts/install_launch_agent.py \
  --repo panda-skills-for-llms \
  --model gpt-5.3-codex
```

Uninstall:

```bash
python scripts/uninstall_launch_agent.py
```

### Troubleshooting

- **Dashboard is empty**: run `--once` ingest first and confirm events exist in `~/.cursor/ai-tracking/skill-usage.jsonl`.
- **No new events**: verify transcript path is correct (`--transcripts-root`) and tracker is running.
- **Duplicate events concern**: offsets are persisted in `skill-tracker-state.json`; do not delete it unless you want reprocessing.
- **Wrong model label**: reinstall launch agent with a new `--model` value.

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

MIT — see `LICENSE`.
