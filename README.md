# Panda Skills for LLMs

Reusable **skills** (prompt workflows) for coding agents—copy them into your setup or contribute new ones.

## What’s in this repo

| Folder | Purpose |
| --- | --- |
| `skills/` | Skill definitions (`SKILL.md` per skill) |
| `rules/` | Optional agent rules (e.g. Claude Code in `rules/claude-code/`) |
| `templates/` | Spec and TDD templates |
| `dashboard/` | Streamlit app: usage over time, **per-agent comparison** when multiple `agent` values exist |
| `scripts/` | Transcript watcher → JSONL logs; optional macOS LaunchAgents |

## Using the skills

Open a folder under `skills/`, read `SKILL.md`, and copy or adapt it for Cursor, Claude Code, or similar tools.

## Skill usage tracking

The watcher (`scripts/auto_track_skill_usage.py`) scans **session transcripts** on disk. When a line matches a skill from this repo’s `skills/` list (path or name), it appends one JSON line to a **JSONL** log. A small **state** file stores read offsets so lines are not double-counted.

| Topic | Meaning |
| --- | --- |
| **`--layout`** | Where transcripts are read and default log paths: **`claude-code`** (default) or **`cursor`**. |
| **`--agent`** | Label stored on each event for filtering and dashboards—not the in-session LLM model name. Same layout can use different labels (e.g. two machines). |

If **`CLAUDE_CONFIG_DIR`** is set, Claude-side paths use that tree instead of `~/.claude`.

### Claude Code (default)

Transcripts: `projects/` under your Claude config (default `~/.claude/projects/`).  
Log + state (default): `~/.claude/ai-tracking/skill-usage.jsonl` and `skill-tracker-state.json`.

```bash
pip install -r dashboard/requirements.txt

python scripts/auto_track_skill_usage.py --once
python scripts/auto_track_skill_usage.py --interval-seconds 5
```

Optional **`--agent LABEL`** on both commands (default label: **`claude-code`**). Leave the interval process running; stop with **Ctrl+C**.

### Cursor (second process)

Uses **`--layout cursor`**, reads under `~/.cursor/projects/**/agent-transcripts/`, and writes defaults under **`~/.cursor/ai-tracking/`**. Use a **distinct** **`--agent`** (e.g. **`cursor`**) so merged dashboard data stays separable.

```bash
python scripts/auto_track_skill_usage.py --layout cursor --agent cursor --once
python scripts/auto_track_skill_usage.py --layout cursor --agent cursor --interval-seconds 5
```

Only **one** process should append to a given JSONL path.

### Dashboard

```bash
streamlit run dashboard/app.py
```

- **Primary log path** defaults to the Claude JSONL; add **`~/.cursor/ai-tracking/skill-usage.jsonl`** under **Additional log paths** to combine streams.
- **Compare agents**: summary per `agent` label and a grouped chart when at least two agents appear in the filtered data.

### macOS LaunchAgents (optional)

Install **once per layout** (separate jobs, separate logs):

```bash
python scripts/install_launch_agent.py
python scripts/install_launch_agent.py --layout cursor
```

Defaults: labels **`com.panda.skills.claude-code`** and **`com.panda.skills.cursor`**; agents **`claude-code`** and **`cursor`**. Uninstall:

```bash
python scripts/uninstall_launch_agent.py
python scripts/uninstall_launch_agent.py --label com.panda.skills.cursor
```

Legacy label: **`com.panda.skills.tracker`**.  
The plist uses the **same Python** as the one that ran the installer (`sys.executable`); reinstall with your preferred interpreter if needed.

### Session rules (“start tracking?”)

Copy **`rules/claude-code/skill-tracking-session-offer.md`** → **`~/.claude/rules/`**, and optionally **`rules/skill-tracking-session-offer.mdc`** → **`~/.cursor/rules/`**.

Behavior (high level): **`pgrep -f auto_track_skill_usage.py`** — if a watcher is already running, **do not** ask or start another. If not running, offer to start the interval watcher. If the skill JSONL is **missing or empty**, the rule also offers a one-time **`--once`** backfill before starting the long-running process.

Set **`PANDA_SKILLS_ROOT`** to the **absolute path** of this repo when the agent should resolve `scripts/` without your working directory being the clone.

If LaunchAgents are installed, **`pgrep`** is usually satisfied at login and the nudge does not appear.

### Other scripts

- Smoke event: `python scripts/log_skill_event.py --skill-name brainstorming`  
  For the Cursor log explicitly: add **`--log-path`** (expanded path to that layout’s JSONL) and **`--agent`** matching your watcher.

### Troubleshooting

| Issue | What to try |
| --- | --- |
| Empty dashboard | Run **`--once`**; confirm the JSONL path in the sidebar exists and transcripts contain skill references. |
| No new lines | Keep the interval watcher running; confirm transcript roots (`--transcripts-root` if non-default). |
| Rebuild counts from scratch | Delete **`skill-usage.jsonl`** and **`skill-tracker-state.json`** for that layout, then **`--once`**. |
| “Yes” but no watcher | Use **`PANDA_SKILLS_ROOT`** or run from the repo root; inspect **`watcher-nohup.log`** under the same **`ai-tracking/`** directory if the rule started **`nohup`**. |
| launchd job errors | Check **`skill-tracker-launchd.out.log`** / **`.err.log`** next to that layout’s JSONL. |

Claude transcript layout: [Claude Code application data](https://code.claude.com/docs/en/claude-directory.md#application-data).

### Screenshot

![Panda Skills Analytics](assets/skills-analytics-fullpage.png)

## Contributing

Open a PR with a short **what / why**, how you tested, and any tooling assumptions.

## License

MIT — see `LICENSE`.
