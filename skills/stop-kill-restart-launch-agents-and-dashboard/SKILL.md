---
name: stop-kill-restart-launch-agents-and-dashboard
description: >-
  Stops Panda skill-tracking LaunchAgents (Claude Code and Cursor watchers) and the
  Streamlit dashboard agent, frees TCP port 8501, then reinstalls and loads all three
  from this repo’s install scripts. Use on macOS when the user wants to restart watchers
  and dashboard, kill duplicate tracker PIDs, or recover after script or plist changes.
disable-model-invocation: true
---

# Stop, Kill, Restart Launch Agents and Dashboard

## Purpose

Cleanly **stop** the three Panda LaunchAgents (`com.panda.skills.claude-code`, `com.panda.skills.cursor`, `com.panda.skills.dashboard`), **free port 8501** (Streamlit), then **reinstall and load** trackers and dashboard so launchd runs the current repo scripts with default ports (**dashboard on 8501**).

## Preconditions

- **macOS** with `launchctl` and user LaunchAgents under `~/Library/LaunchAgents/`.
- Repo clone with `scripts/install_launch_agent.py` and `scripts/install_dashboard_launch_agent.py` (this project).
- Resolve the clone directory as **`REPO`** (e.g. `git rev-parse --show-toplevel` when cwd is inside the clone, or **`PANDA_SKILLS_ROOT`** if set).

## Workflow (agent must run commands)

### 1) Boot out (or unload) the three LaunchAgents

Plist paths (default labels):

| Label | Plist |
|-------|--------|
| `com.panda.skills.cursor` | `~/Library/LaunchAgents/com.panda.skills.cursor.plist` |
| `com.panda.skills.claude-code` | `~/Library/LaunchAgents/com.panda.skills.claude-code.plist` |
| `com.panda.skills.dashboard` | `~/Library/LaunchAgents/com.panda.skills.dashboard.plist` |

For each plist that exists, stop the job (prefer modern `bootout`, fall back to `unload`):

```bash
LA="$HOME/Library/LaunchAgents"
UID_NUM="$(id -u)"
for label in com.panda.skills.cursor com.panda.skills.claude-code com.panda.skills.dashboard; do
  plist="$LA/${label}.plist"
  if [ -f "$plist" ]; then
    launchctl bootout "gui/${UID_NUM}" "$plist" 2>/dev/null || launchctl unload "$plist" 2>/dev/null || true
  fi
done
```

### 2) Kill listeners on port 8501 (dashboard)

Repeat until nothing listens, then force-kill if needed:

```bash
for i in 1 2; do
  pids=$(lsof -nP -iTCP:8501 -sTCP:LISTEN -t 2>/dev/null || true)
  if [ -n "$pids" ]; then kill $pids 2>/dev/null || true; sleep 1; fi
done
pids=$(lsof -nP -iTCP:8501 -sTCP:LISTEN -t 2>/dev/null || true)
if [ -n "$pids" ]; then kill -9 $pids 2>/dev/null || true; fi
```

Confirm: `lsof -nP -iTCP:8501 -sTCP:LISTEN` prints nothing.

### 3) Optional — remove duplicate orphan tracker processes

If **`pgrep -fl auto_track_skill_usage.py`** shows **more than two** lines (Claude + Cursor), older **`nohup`** or manual runs may still be writing JSONL. Keep only the launchd-managed pair after step 5; if duplicates remain **before** reinstall, kill extra PIDs that are **not** the ones launchd will respawn (after step 1, ideally none remain). After step 5, if duplicates still exist, kill orphans whose parent is `init` (PPID 1) that duplicate the same `--layout` / `--agent` argv.

### 4) Reinstall and load from **`REPO`**

Use the same Python you want launchd to pin (the installer records `sys.executable` in the plist).

```bash
cd "$REPO"
python3 scripts/install_launch_agent.py
python3 scripts/install_launch_agent.py --layout cursor
python3 scripts/install_dashboard_launch_agent.py
```

`install_dashboard_launch_agent.py` defaults to **port 8501**; do not pass `--port` unless the user asked for a different port.

Ignore **“Unload failed: 5”** from the installer if **`Installed and loaded`** still prints — common after `bootout` already removed the job.

### 5) Verify

```bash
launchctl list | grep com.panda.skills
pgrep -fl 'auto_track_skill_usage\.py' || true
lsof -nP -iTCP:8501 -sTCP:LISTEN
```

Expect: three `com.panda.skills.*` entries, **two** `auto_track_skill_usage.py` processes (one `--layout claude-code`, one `--layout cursor`), Streamlit listening on **8501**.

## Notes

- **Uninstall** (remove plist files) is different from this skill; use `scripts/uninstall_launch_agent.py` only if the user wants agents removed entirely.
- Dashboard logs: `~/.cursor/ai-tracking/streamlit-dashboard-launchd*.log` and wrapper logs as documented in `README.md`.
- Tracker logs: `skill-tracker-launchd.{out,err}.log` under each layout’s `ai-tracking` directory.

## Uninstall reference (do not run unless asked)

```bash
python3 scripts/uninstall_launch_agent.py
python3 scripts/uninstall_launch_agent.py --label com.panda.skills.cursor
python3 scripts/uninstall_launch_agent.py --label com.panda.skills.dashboard
```
