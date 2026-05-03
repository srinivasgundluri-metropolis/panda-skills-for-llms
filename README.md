# Panda Skills for LLMs

Reusable **skills** (prompt workflows) for coding agents—copy them into your setup or contribute new ones.

## What’s in this repo

| Folder | Purpose |
| --- | --- |
| `skills/` | Skill definitions (`SKILL.md` per skill) |
| `rules/` | Optional agent rules (e.g. Claude Code prompts in `rules/claude-code/`) |
| `templates/` | Spec and TDD templates |
| `dashboard/` | Small **Streamlit** app to chart skill usage |
| `scripts/` | Watcher that reads Claude Code transcripts and writes usage logs |

## Using the skills

Open a folder under `skills/`, read `SKILL.md`, and copy or adapt it for Cursor, Claude Code, or similar tools.

## Skill usage (Claude Code)

**What it does:** watches Claude Code session logs under `~/.claude/projects`, and each time it sees a skill path or skill name from this repo’s `skills/` list, it appends one line to **`~/.claude/ai-tracking/skill-usage.jsonl`**. A companion file **`skill-tracker-state.json`** remembers how far it read so it does not double-count.

Each event stores an **`agent`** string (default **`claude-code`**) so you can run **several watchers** with different `--agent` values (e.g. `plan`, `opus`) if you split work that way—not the same as the LLM model name inside a session.

If you use **`CLAUDE_CONFIG_DIR`**, those paths live under that directory instead of `~/.claude`.

### Run it (three steps)

From your clone of this repo:

```bash
pip install -r dashboard/requirements.txt

python scripts/auto_track_skill_usage.py --once
python scripts/auto_track_skill_usage.py --interval-seconds 5
```

Optional: **`--agent YOUR_LABEL`** on both lines (default is `claude-code`). Leave the second command running while you work; stop with **Ctrl+C**.

Then open the charts:

```bash
streamlit run dashboard/app.py
```

The app expects the log at **`~/.claude/ai-tracking/skill-usage.jsonl`** unless you change the path in the sidebar.

### Optional extras

- **Test one event:**  
  `python scripts/log_skill_event.py --skill-name brainstorming`
- **macOS login autostart:**  
  `python scripts/install_launch_agent.py`  
  (optional: `--agent claude-code` — same default as the watcher.)  
  Uninstall: `python scripts/uninstall_launch_agent.py`  
  Legacy plist: `python scripts/uninstall_launch_agent.py --label com.panda.skills.tracker`
- **Nudge your agent when tracking is off:** copy `rules/claude-code/skill-tracking-session-offer.md` → `~/.claude/rules/` (and optionally `rules/skill-tracking-session-offer.mdc` → `~/.cursor/rules/` for Cursor). Those rules run **`pgrep -f auto_track_skill_usage.py`** first and only ask to start tracking if nothing is running. Set **`PANDA_SKILLS_ROOT`** to this repo if the agent should run scripts by path.

### `PANDA_SKILLS_ROOT` and the “start tracking?” question

**`PANDA_SKILLS_ROOT`** is optional: the **absolute path to this repo** (the folder that contains `scripts/`). You don’t need it when you run commands from inside the clone.

**Launch Agent vs that question:** launchd starts the watcher at login. The **session rules** check **`pgrep`** first; if a process exists, the agent should **not** ask to start tracking.

### If something looks wrong

- **Dashboard empty:** run **`--once`**, then confirm the JSONL file exists.
- **No new lines:** keep the watcher running; transcripts must be under **`~/.claude/projects`** unless you passed **`--transcripts-root`**.
- **Start counts over:** delete **`skill-usage.jsonl`** and **`skill-tracker-state.json`**, then run **`--once`** again.
- **Agent said yes but no watcher:** set **`PANDA_SKILLS_ROOT`** or run from inside the clone. Check **`~/.claude/ai-tracking/watcher-nohup.log`** if the session rule used **`nohup`**.

Where Claude stores transcripts: [Claude Code application data](https://code.claude.com/docs/en/claude-directory.md#application-data).

### Screenshot

![Panda Skills Analytics](assets/skills-analytics-fullpage.png)

## Contributing

Open a PR with a short **what / why**, how you tested, and any tooling assumptions.

## License

MIT — see `LICENSE`.
