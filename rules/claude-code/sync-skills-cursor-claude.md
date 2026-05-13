# Sync skills between Cursor and Claude (global only)

**Repo copies:** `rules/claude-code/sync-skills-cursor-claude.md` (this file) and `rules/sync-skills-cursor-claude.mdc`. Install to **`~/.claude/rules/`** and **`~/.cursor/rules/`** with **`./scripts/sync_skill_tracking_session_rules.sh`**.

Two cases only. **Ask once per new skill**, then do not ask again until a different skill is created.

## 1. Skill created in **Claude Code**

If the user **creates or substantially authors** a new skill under **`~/.claude/skills/<skill-name>/`**, **before finishing**:

- **Ask once** whether to replicate the **same** skill to **global Cursor**: **`~/.cursor/skills/<skill-name>/SKILL.md`** (create the directory if needed). `<skill-name>` matches the skill folder / YAML `name` (kebab-case).
- If **yes**: copy there and **tailor for Cursor** (paths and discovery for Cursor—not a blind paste).
- If **no**: stop; do not ask again for that skill session.

## 2. Skill created in **Cursor**

If the user **creates or substantially authors** a new skill under **`~/.cursor/skills/<skill-name>/`** or in **this repo’s** **`skills/<skill-name>/`** tree, **before finishing**:

- **Ask once** whether to replicate the **same** skill to **global Claude**: **`~/.claude/skills/<skill-name>/SKILL.md`** (create the directory if needed).
- If **yes**: copy there and **tailor for Claude Code** (Skill tool, `~/.claude/skills/`—not a blind paste).
- If **no**: stop; do not ask again for that skill session.

## Safety

Never copy or overwrite global skills without the user’s explicit yes to that question.
