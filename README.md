# Panda Skills for LLMs

**Lazy like pandas. Efficient like pros.** Reusable skills that turn prompt effort into reliable LLM workflows.

This is a **public, community-maintained collection** that anyone can use, fork, and improve.

## What this repo is

- A curated set of practical agent skills you can copy into your own environment
- A starting point for teams who want shared, reusable skill workflows
- A place for community contributions and iterative improvements

## Repository layout

- `skills/`: reusable skill definitions for agent workflows
- `rules/`: reusable policy/rule files (includes optional Claude Code session prompts under `rules/claude-code/`)
- `templates/spec-driven/`: PRD/UI/TECH/RFC/ADR/traceability/release templates
- `templates/tdd/`: test planning and regression checklist templates
- `dashboard/`: Streamlit analytics app for **Claude Code** skill usage JSONL
- `scripts/`: skill usage watcher, log helper, macOS launchd installer

## Design principles

- LLM-agnostic: content should work regardless of the underlying model
- Runtime-flexible: adapt to Cursor, Claude-style agents, or similar tooling
- Reusable by default: prefer templates and composable workflows over one-off prompts
- Contributor-friendly: keep docs clear, practical, and easy to extend

## How to use

- Copy or adapt the `skills/`, `rules/`, and `templates/` content into your agent setup
- Adjust prompts/instructions for your tooling and team conventions
- Submit improvements back via pull requests

## Skill usage tracking (Claude Code → JSONL → dashboard)

This answers: **“Which skills did Claude Code actually use, and when?”** It does **not** read your whole transcript—only lines that reference a skill path or a known skill name from `skills/`.

| Piece | What it does |
| --- | --- |
| **Watcher** | `scripts/auto_track_skill_usage.py` tails **Claude Code** session JSONL under `~/.claude/projects`, appends one JSON line per detected skill hit. |
| **Logs** | `~/.claude/ai-tracking/skill-usage.jsonl` (and `skill-tracker-state.json` for offsets). Honors **`CLAUDE_CONFIG_DIR`**. |
| **Dashboard** | `streamlit run dashboard/app.py` reads that JSONL (and optional extra paths you paste in). |

Set a stable label for your work (replace `YOUR_REPO` with a short name, or use your git remote name):

```bash
export PANDA_SKILLS_ROOT="/absolute/path/to/this/repo"   # optional but handy
export REPO_LABEL="YOUR_REPO"   # used as --repo in examples below; e.g. my-app
```

### Paths (Claude Code)

| | Location |
| --- | --- |
| **Transcripts (read)** | `~/.claude/projects/**/*.jsonl` (excludes `memory/`, `tool-results/`) |
| **Events JSONL (write)** | `~/.claude/ai-tracking/skill-usage.jsonl` |
| **Offset state** | `~/.claude/ai-tracking/skill-tracker-state.json` |

The watcher defaults to **Claude Code**; you do **not** need `--layout` unless you use the optional **`--layout cursor`** path for non-Claude agents (advanced).

### Event format (one JSON object per line)

```json
{"timestamp":"2026-04-30T18:52:00Z","skill_name":"spec-driven-development","session_id":"abc123","repo":"YOUR_REPO","model":"claude-code"}
```

### Quick start

1. **Install dashboard dependencies**

   ```bash
   pip install -r dashboard/requirements.txt
   ```

2. **Ingest history once, then keep watching**

   From the repo root (or use `$PANDA_SKILLS_ROOT`):

   ```bash
   python scripts/auto_track_skill_usage.py --once --repo "$REPO_LABEL" --model claude-code
   python scripts/auto_track_skill_usage.py --repo "$REPO_LABEL" --model claude-code --interval-seconds 5
   ```

3. **Open the dashboard**

   ```bash
   streamlit run dashboard/app.py
   ```

   Default log path in the sidebar: **`~/.claude/ai-tracking/skill-usage.jsonl`**. Use **Additional log paths** only if you want to merge another JSONL file (e.g. a second machine’s export).

Transcript reference: [Claude Code application data](https://code.claude.com/docs/en/claude-directory.md#application-data).

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
  --model claude-code
```

### Optional: have the agent offer to start tracking every new session

| Product | Copy this file | To |
| --- | --- | --- |
| **Cursor (IDE)** | `rules/skill-tracking-session-offer.mdc` | `~/.cursor/rules/` |
| **Claude Code** | `rules/claude-code/skill-tracking-session-offer.md` | `~/.claude/rules/` |

Set `PANDA_SKILLS_ROOT` in your shell profile so the agent can run `"$PANDA_SKILLS_ROOT/scripts/auto_track_skill_usage.py"` without guessing.

### Auto-start on macOS (Claude Code watcher)

Installs **`com.panda.skills.claude-code`**: runs `auto_track_skill_usage.py` with **default Claude Code layout** (no `--layout` in plist). Stdout/stderr go under **`~/.claude/ai-tracking/`** next to your skill JSONL.

```bash
python scripts/install_launch_agent.py --repo "$REPO_LABEL" --model claude-code
```

Uninstall:

```bash
python scripts/uninstall_launch_agent.py
```

If you previously installed **`com.panda.skills.tracker`** (legacy Cursor job), remove it explicitly:

```bash
python scripts/uninstall_launch_agent.py --label com.panda.skills.tracker
```

### Troubleshooting

- **Empty dashboard**: run `--once`, confirm `~/.claude/ai-tracking/skill-usage.jsonl` exists and the sidebar path matches.
- **No new events**: confirm the watcher is running; use `--transcripts-root` only if transcripts are not under `~/.claude/projects`.
- **Reset and re-scan**: delete `skill-usage.jsonl` **and** `skill-tracker-state.json`, then run `--once` again (re-emits from existing transcripts).
- **Duplicate launchd jobs**: unload the old label before installing the new one (see uninstall command above).

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
