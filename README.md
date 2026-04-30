# Panda Skills for LLMs

**Lazy like pandas. Efficient like pros.** Reusable skills that turn prompt effort into reliable LLM workflows.

This is a **public, community-maintained collection** that anyone can use, fork, and improve.
The repo intentionally includes only your personal/global skill set as the starting point.

## What this repo is

- A curated set of practical agent skills you can copy into your own environment
- A starting point for teams who want shared, reusable skill workflows
- A place for community contributions and iterative improvements

## Included

- `skills/` (your personal/global skill set from `~/.cursor/skills`)
- `rules/` (your personal/global rule set from `~/.cursor/rules`)
- `templates/spec-driven/` (PRD/UI/TECH/RFC/ADR/traceability/release templates)
- `templates/tdd/` (test plan and regression checklist templates)

## Excluded

- `skills-cursor/` (not treated as your personal skill set)
- Claude-synced/default skills that are not part of your personal set
- Third-party/plugin-cache skills (including Superpowers cache content)
- Machine-local generated artifacts not useful for contributors

## How to use

- Copy the skill folders you want into your own agent skill directory
- Copy the rule files you want into your own global/project rules directory
- Adapt prompts/instructions to your workflow and stack
- Submit improvements back via pull requests

## Skill Usage Dashboard

A simple Streamlit dashboard is included at `dashboard/app.py`.

- Install deps: `pip install -r dashboard/requirements.txt`
- Run: `streamlit run dashboard/app.py`
- Default log path: `~/.cursor/ai-tracking/skill-usage.jsonl`

Expected JSONL shape per line:

```json
{"timestamp":"2026-04-30T18:52:00Z","skill_name":"spec-driven-development","session_id":"abc123","repo":"panda-skills-for-llms","model":"gpt-5.3-codex"}
```

### Log helper

Use `scripts/log_skill_event.py` to append valid events quickly:

```bash
python scripts/log_skill_event.py \
  --skill-name spec-driven-development \
  --session-id demo-001 \
  --repo panda-skills-for-llms \
  --model gpt-5.3-codex
```

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
