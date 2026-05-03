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

If you use **`CLAUDE_CONFIG_DIR`**, those paths live under that directory instead of `~/.claude`.

### Run it (three steps)

From your clone of this repo, with **`YOUR_PROJECT`** replaced by a short name (e.g. your git repo name):

```bash
pip install -r dashboard/requirements.txt

python scripts/auto_track_skill_usage.py --once --repo YOUR_PROJECT --model claude-code
python scripts/auto_track_skill_usage.py --repo YOUR_PROJECT --model claude-code --interval-seconds 5
```

Leave the second command running while you work. Stop it with **Ctrl+C**.

Then open the charts:

```bash
streamlit run dashboard/app.py
```

The app expects the log at **`~/.claude/ai-tracking/skill-usage.jsonl`** unless you change the path in the sidebar.

### Optional extras

- **Test one event:**  
  `python scripts/log_skill_event.py --skill-name brainstorming --repo YOUR_PROJECT --model claude-code`
- **macOS login autostart:**  
  `python scripts/install_launch_agent.py --repo YOUR_PROJECT --model claude-code`  
  Uninstall: `python scripts/uninstall_launch_agent.py`  
  If you ever used the old **`com.panda.skills.tracker`** job:  
  `python scripts/uninstall_launch_agent.py --label com.panda.skills.tracker`
- **Nudge your agent when tracking is off:** copy `rules/claude-code/skill-tracking-session-offer.md` → `~/.claude/rules/` (and optionally `rules/skill-tracking-session-offer.mdc` → `~/.cursor/rules/` for Cursor). Those rules tell the assistant to run **`pgrep -f auto_track_skill_usage.py`** first; it **only asks** to start tracking if no watcher process is found (so Launch Agent alone usually means no prompt).

### `PANDA_SKILLS_ROOT` and the “start tracking?” question

**`PANDA_SKILLS_ROOT`** is an optional environment variable: the **absolute path to this repo** (the folder that contains `scripts/`). Set it in your shell profile if you want agents to run `python3 "$PANDA_SKILLS_ROOT/scripts/auto_track_skill_usage.py"` without you pasting the path each time. You don’t need it when you run the commands yourself from inside the clone.

**Launch Agent vs that question:** **`install_launch_agent.py`** starts the watcher at login. The **session rules** above first check **`pgrep -f auto_track_skill_usage.py`**; if a process exists (including one started by Launch Agent), the agent **should not** ask to start tracking.

### If something looks wrong

- **Dashboard empty:** run the `--once` line above, then confirm the JSONL file exists.
- **No new lines:** make sure the watcher is still running; transcripts must be under **`~/.claude/projects`** unless you passed **`--transcripts-root`**.
- **Start counts over:** delete **`skill-usage.jsonl`** and **`skill-tracker-state.json`**, then run **`--once`** again (old transcripts get scanned again).

Where Claude stores transcripts: [Claude Code application data](https://code.claude.com/docs/en/claude-directory.md#application-data).

### Screenshot

![Panda Skills Analytics](assets/skills-analytics-fullpage.png)

## Contributing

Open a PR with a short **what / why**, how you tested, and any tooling assumptions.

## License

MIT — see `LICENSE`.
