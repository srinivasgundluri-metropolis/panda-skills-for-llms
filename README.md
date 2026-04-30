# Panda Skills for LLMs

**Lazy like pandas. Efficient like pros.** Reusable skills that turn prompt effort into reliable LLM workflows.

This is a **public, community-maintained collection** that anyone can use, fork, and improve.
One shared `skills/` directory is designed to work across Cursor/Claude-style agents regardless of underlying LLM.

## What this repo is

- A curated set of practical agent skills you can copy into your own environment
- A starting point for teams who want shared, reusable skill workflows
- A place for community contributions and iterative improvements

## Included

- `skills/` (unified, cross-compatible skill set for Cursor/Claude-style workflows)

## Excluded

- `skills-cursor/` (not treated as your personal skill set)
- Separate runtime-specific duplication folders (for example old `claude-skills/`)
- Third-party/plugin-cache skills (including Superpowers cache content)
- Machine-local generated artifacts not useful for contributors

## How to use

- Copy the skill folders you want into your own agent skill directory
- Adapt prompts/instructions to your workflow and stack
- Submit improvements back via pull requests

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
