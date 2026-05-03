# Panda skill tracking — session start

When this is a **new Claude Code session** (your first reply after the session begins), **before** substantive work:

## 1. Check if tracking is already running (do this first)

```bash
pgrep -f auto_track_skill_usage.py
```

- **Any PIDs printed** → watcher is already running (terminal or Launch Agent **`com.panda.skills.claude-code`**). **Do not ask.** **Do not start another.** Continue with the user’s task.
- **No output** → go to step 2.

If `pgrep` does not exist, skip to step 2.

## 2. Only if no watcher — ask once

Ask whether to start **Panda Skills** usage tracking for Claude Code.

## 3. If they say yes — you must run Bash and confirm it started

Do **not** only “plan” to start the watcher—**execute** a shell command, then **verify** with `pgrep` again.

**Resolve the script path** (first match wins):

1. `$PANDA_SKILLS_ROOT/scripts/auto_track_skill_usage.py` if `PANDA_SKILLS_ROOT` is set and that file exists.
2. Otherwise **`$(git rev-parse --show-toplevel 2>/dev/null)/scripts/auto_track_skill_usage.py`** if you are inside a git clone and that file exists.
3. Otherwise tell the user you need the **absolute path** to their Panda Skills repo (or they must `export PANDA_SKILLS_ROOT=...`) and **stop**—do not pretend the watcher started.

**Resolve `--repo`:** from `git remote get-url origin` basename inside that repo, else `basename` of the repo root.

**Start** (runs detached from the tool; logs errors to a file you can read):

```bash
mkdir -p ~/.claude/ai-tracking
nohup python3 "<ABSOLUTE_PATH_TO>/scripts/auto_track_skill_usage.py" \
  --repo "<REPO_LABEL>" \
  --model claude-code \
  --interval-seconds 5 \
  >> ~/.claude/ai-tracking/watcher-nohup.log 2>&1 &
sleep 1
pgrep -f auto_track_skill_usage.py
```

- If `pgrep` now shows a PID, tell the user **success** (mention the log file `~/.claude/ai-tracking/watcher-nohup.log` if something looks wrong later).
- If **still no PID**, show the user **`tail -20 ~/.claude/ai-tracking/watcher-nohup.log`** output and say start failed.

## 4. Optional: macOS login autostart

`python scripts/install_launch_agent.py --repo … --model claude-code` installs **`com.panda.skills.claude-code`**. After that, step 1 usually finds a PID and you skip asking.

## 5. If they decline

Do not ask again in this thread unless they ask.

Skip steps 1–2 if their first message already specifies tracking on or off.
