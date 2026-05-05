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

**Resolve the skill log path** (for the empty check and for telling the user where data goes):

- If **`CLAUDE_CONFIG_DIR`** is set: **`$CLAUDE_CONFIG_DIR/ai-tracking/skill-usage.jsonl`**
- Else: **`~/.claude/ai-tracking/skill-usage.jsonl`**

Check whether the log already has content, e.g.:

```bash
CC_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
test -s "$CC_HOME/ai-tracking/skill-usage.jsonl" && echo has_events || echo empty_or_missing
```

If the result is **`empty_or_missing`**, include in the same ask (or a clear follow-up before starting):

- Whether to start the **interval** watcher, and
- Whether to **backfill** existing transcripts once with **`--once`**. The interval watcher **tails new bytes only** by default (it does not scan transcript history for files it has never seen). **`--once`** is what ingests **existing** transcript files—only ask this if they want past sessions in the dashboard.

If the log **already has content**, only ask whether to start the watcher (no need to push backfill unless they ask).

## 3. If they say yes — you must run Bash and confirm it started

Do **not** only “plan” to start the watcher—**execute** a shell command, then **verify** with `pgrep` again.

**Resolve the script path** (first match wins):

1. `$PANDA_SKILLS_ROOT/scripts/auto_track_skill_usage.py` if `PANDA_SKILLS_ROOT` is set and that file exists.
2. Otherwise **`$(git rev-parse --show-toplevel 2>/dev/null)/scripts/auto_track_skill_usage.py`** if you are inside a git clone and that file exists.
3. Otherwise tell the user you need the **absolute path** to their Panda Skills repo (or they must `export PANDA_SKILLS_ROOT=...`) and **stop**—do not pretend the watcher started.

**Optional `--agent`:** if the user names a label (e.g. `plan`, `opus-session`), pass **`--agent <label>`**; otherwise omit it (watcher default is **`claude-code`**).

**Backfill (only if they agreed to it in step 2):** run **`--once`** in the foreground first, same resolved script path and optional **`--agent`**. If they already ran the interval watcher and state points at EOF but they still want a full history pass for one run, use **`--once --backfill`** instead (can duplicate JSONL rows if those lines were already logged).

```bash
CC_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
mkdir -p "$CC_HOME/ai-tracking"
python3 "<ABSOLUTE_PATH_TO>/scripts/auto_track_skill_usage.py" --once
```

(Add **`--agent <label>`** after the script path when needed. Append **`--backfill`** only when they need the forced full re-read described above.)

**Start** the interval watcher (runs detached; logs stderr/stdout to **`watcher-nohup.log`** next to the JSONL):

```bash
CC_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
mkdir -p "$CC_HOME/ai-tracking"
nohup python3 "<ABSOLUTE_PATH_TO>/scripts/auto_track_skill_usage.py" \
  --interval-seconds 5 \
  >> "$CC_HOME/ai-tracking/watcher-nohup.log" 2>&1 &
sleep 1
pgrep -f auto_track_skill_usage.py
```

(Add **`--agent <label>`** before `--interval-seconds` when the user asked for a specific agent label.) If they **declined** backfill, **omit** the **`--once`** block and only run the **nohup** lines.

- If `pgrep` now shows a PID, tell the user **success** (mention **`$CC_HOME/ai-tracking/watcher-nohup.log`** if something looks wrong later).
- If **still no PID**, show **`tail -20 "$CC_HOME/ai-tracking/watcher-nohup.log"`** and say start failed.

## 4. Optional: macOS login autostart

`python scripts/install_launch_agent.py` installs **`com.panda.skills.claude-code`**. After that, step 1 usually finds a PID and you skip asking.

## 5. If they decline

Do not ask again in this thread unless they ask.

Skip steps 1–2 if their first message already specifies tracking on or off.
