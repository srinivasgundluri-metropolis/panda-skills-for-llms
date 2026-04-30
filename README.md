# Panda Cursor + Claude Skills

Public backup of first-party global skills from local Cursor and Claude installations.

## Scope and Exclusions

- Included: `~/.cursor/skills`, `~/.cursor/skills-cursor`, and first-party synced entries from `~/.claude/skills`
- Excluded: Superpowers/third-party/plugin-cache skills

## Cursor Skills (skills/)

- `approve-pr`: Approve a pull request after quick merge-readiness checks. Use when the user asks to approve a PR, mark review as approved, or run a final go/no-go before approval.
- `fix-terminal-error-and-re-run`: Diagnose terminal command failures, identify root cause from recent terminal output, apply targeted fixes, and safely rerun commands. Use when the user asks to check terminal errors, fix failed commands, clear occupied ports, restart dev servers, or recover from Docker/Next/npm startup issues.
- `grill-me`: Ask structured, high-signal discovery questions to fully clarify product specs, UX behavior, technical architecture, constraints, and user preferences before implementation. Use when requirements are ambiguous, work is medium/large, or as a pre-step in spec-driven-development workflows.
- `merge-pr`: Merge an open GitHub pull request by PR number using gh CLI with safety checks. Use when the user asks to merge a PR and provides a PR number.
- `merge-pr-merge`: Merge an open GitHub pull request by PR number using gh CLI with merge-commit as default. Use when the user asks to merge a PR and provides a PR number.
- `open-pr`: Compares the current branch against main and drafts a pull request title/body with summary and test plan. Use when the user asks to open a PR, draft a PR, prepare PR notes, or review branch changes before creating a PR.
- `review-open-pr`: Review an open pull request and classify findings into four buckets. Use when the user asks to review a PR, evaluate merge readiness, or provide code-review feedback with prioritized categories.
- `spec-driven-development`: Enforces split-spec workflow using PRD, UI-SPEC, and TECH-SPEC with hybrid execution gates. Use when starting a new project, planning features, redesigning UI, or implementing medium/large changes that require explicit requirements, design decisions, and acceptance criteria.
- `test-driven-development`: Enforces test-first and verification loops for feature work, including unit and regression coverage. Use when implementing features, fixing bugs, or validating refactors that can introduce regressions.
- `workflow-agent-pipeline`: Orchestrates a 3-stage delivery workflow: spec-driven planning, implementation, and test-driven verification. Use when starting medium/large features, redesigns, refactors, or any task that needs stronger planning quality and reliable test gates.

## Cursor Skills (skills-cursor/)

- `babysit`: Keep a PR merge-ready by triaging comments, resolving clear conflicts, and fixing CI in a loop.
- `canvas`: A Cursor Canvas is a live React app that the user can open beside the chat. You MUST use a canvas when the agent produces a standalone analytical artifact — quantitative analyses, billing investigations, security audits, architecture reviews, data-heavy content, timelines, charts, tables, interactive explorations, repeatable tools, or any response that benefits from visual layout. Especially prefer a canvas when presenting results from MCP tools (Datadog, Databricks, Linear, Sentry, Slack, etc.) where the data is the deliverable — render it in a rich canvas rather than dumping it into a markdown table or code block. If you catch yourself about to write a markdown table, stop and use a canvas instead. You MUST also read this skill whenever you create, edit, or debug any .canvas.tsx file.
- `create-hook`: Create Cursor hooks. Use when you want to create a hook, write hooks.json, add hook scripts, or automate behavior around agent events.
- `create-rule`: Create Cursor rules for persistent AI guidance. Use when you want to create a rule, add coding standards, set up project conventions, configure file-specific patterns, create RULE.md files, or asks about .cursor/rules/ or AGENTS.md.
- `create-skill`: Create Cursor Agent Skills. Use when authoring a new skill or asking about SKILL.md structure.
- `create-subagent`: Create custom subagents for specialized AI tasks. Use when you want to create a new type of subagent, set up task-specific agents, configure code reviewers, debuggers, or domain-specific assistants with custom prompts.
- `migrate-to-skills`: Convert 'Applied intelligently' Cursor rules (.cursor/rules/*.mdc) and slash commands (.cursor/commands/*.md) to Agent Skills format (.cursor/skills/). Use when you want to migrate rules or commands to skills, convert .mdc rules to SKILL.md format, or consolidate commands into the skills directory.
- `shell`: Runs the rest of a /shell request as a literal shell command. Use only when the user explicitly invokes /shell and wants the following text executed directly in the terminal.
- `split-to-prs`: Split current work into small reviewable PRs. Use when the user asks to split a chat, set of changes, branch, or PR.
- `statusline`: Configure a custom status line in the CLI. Use when the user mentions status line, statusline, statusLine, CLI status bar, prompt footer customization, or wants to add session context above the prompt.
- `update-cli-config`: View and modify Cursor CLI configuration settings in ~/.cursor/cli-config.json. Use when the user wants to change CLI settings, configure permissions, switch approval mode, enable vim mode, toggle display options, configure sandbox, or manage any CLI preferences.
- `update-cursor-settings`: Modify Cursor/VSCode user settings in settings.json. Use when you want to change editor settings, preferences, configuration, themes, font size, tab size, format on save, auto save, keybindings, or any settings.json values.

## Claude Skills (claude-skills/)

- `babysit`: Keep a PR merge-ready by triaging comments, resolving clear conflicts, and fixing CI in a loop.
- `canvas`: A Cursor Canvas is a live React app that the user can open beside the chat. You MUST use a canvas when the agent produces a standalone analytical artifact — quantitative analyses, billing investigations, security audits, architecture reviews, data-heavy content, timelines, charts, tables, interactive explorations, repeatable tools, or any response that benefits from visual layout. Especially prefer a canvas when presenting results from MCP tools (Datadog, Databricks, Linear, Sentry, Slack, etc.) where the data is the deliverable — render it in a rich canvas rather than dumping it into a markdown table or code block. If you catch yourself about to write a markdown table, stop and use a canvas instead. You MUST also read this skill whenever you create, edit, or debug any .canvas.tsx file.
- `create-hook`: Create Cursor hooks. Use when you want to create a hook, write hooks.json, add hook scripts, or automate behavior around agent events.
- `create-rule`: Create Cursor rules for persistent AI guidance. Use when you want to create a rule, add coding standards, set up project conventions, configure file-specific patterns, create RULE.md files, or asks about .cursor/rules/ or AGENTS.md.
- `create-skill`: Guides users through creating effective Agent Skills for Cursor. Use when you want to create, write, or author a new skill, or asks about skill structure, best practices, or SKILL.md format.
- `create-subagent`: Create custom subagents for specialized AI tasks. Use when you want to create a new type of subagent, set up task-specific agents, configure code reviewers, debuggers, or domain-specific assistants with custom prompts.
- `migrate-to-skills`: Convert 'Applied intelligently' Cursor rules (.cursor/rules/*.mdc) and slash commands (.cursor/commands/*.md) to Agent Skills format (.cursor/skills/). Use when you want to migrate rules or commands to skills, convert .mdc rules to SKILL.md format, or consolidate commands into the skills directory.
- `shell`: Runs the rest of a /shell request as a literal shell command. Use only when the user explicitly invokes /shell and wants the following text executed directly in the terminal.
- `split-to-prs`: Split current work into small reviewable PRs. Use when the user asks to split a chat, set of changes, branch, or PR.
- `statusline`: Configure a custom status line in the CLI. Use when the user mentions status line, statusline, statusLine, CLI status bar, prompt footer customization, or wants to add session context above the prompt.
- `update-cli-config`: View and modify Cursor CLI configuration settings in ~/.cursor/cli-config.json. Use when the user wants to change CLI settings, configure permissions, switch approval mode, enable vim mode, toggle display options, configure sandbox, or manage any CLI preferences.
- `update-cursor-settings`: Modify Cursor/VSCode user settings in settings.json. Use when you want to change editor settings, preferences, configuration, themes, font size, tab size, format on save, auto save, keybindings, or any settings.json values.

