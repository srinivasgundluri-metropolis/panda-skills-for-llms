# Panda skill tracking — session start

When this is a **new Claude Code session** (your first reply after the session begins), **before** substantive work:

## 1. Check if tracking is already running (do this first)

Run a quick process check (macOS / Linux):

```bash
pgrep -f auto_track_skill_usage.py
```

- If this prints **one or more PIDs**, a watcher is already running (manual terminal **or** Launch Agent **`com.panda.skills.claude-code`**). **Do not ask** the user about starting tracking. **Do not** start another copy. Continue with their task.
- If it prints **nothing** (exit code 1 is normal), treat the watcher as **not** running and go to step 2.

If `pgrep` is not available, skip the check and go to step 2.

## 2. Only if no watcher is running — ask once

Ask whether to start **Panda Skills** usage tracking for Claude Code (background process).

## 3. If they say yes

Resolve `PANDA_SKILLS_ROOT` from the environment or ask once, then run in the **background**:

```bash
python3 "$PANDA_SKILLS_ROOT/scripts/auto_track_skill_usage.py" \
  --repo "$(git remote get-url origin 2>/dev/null | sed 's/.*\///;s/\.git//' || basename "$(git rev-parse --show-toplevel 2>/dev/null)" || echo unknown)" \
  --model claude-code \
  --interval-seconds 5
```

(`--layout claude-code` is optional; it is the script default.)

## 4. Optional: macOS login autostart

From the repo: `python scripts/install_launch_agent.py --repo … --model claude-code` installs **`com.panda.skills.claude-code`**. After that, step 1 should usually find a PID and you will **not** prompt.

## 5. If they decline

**Do not** ask again in the same thread unless they request it.

Skip steps 1–2 if their first message already specifies tracking on or off.
