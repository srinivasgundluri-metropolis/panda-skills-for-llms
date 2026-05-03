# Panda skill tracking — session start

When this is a **new Claude Code session** (your first reply after the session begins), **before** substantive work:

1. **Ask once** whether to start **Panda Skills** usage tracking for Claude Code.
2. **If yes**, run in the **background** (continuous polling). Resolve `PANDA_SKILLS_ROOT` from the user’s clone (environment variable or ask once), then:

   ```bash
   python3 "$PANDA_SKILLS_ROOT/scripts/auto_track_skill_usage.py" \
     --repo "$(git remote get-url origin 2>/dev/null | sed 's/.*\///;s/\.git//' || basename "$(git rev-parse --show-toplevel 2>/dev/null)" || echo unknown)" \
     --model claude-code \
     --interval-seconds 5
   ```

   (`--layout claude-code` is optional; it is the script default.)

3. **Before starting**, check that another `auto_track_skill_usage.py` is not already running for the same log (`pgrep -af auto_track_skill_usage`); avoid duplicates.
4. If they decline or tracking is already active, **do not** ask again unless they request it.

Skip if their first message already specifies tracking on or off.
