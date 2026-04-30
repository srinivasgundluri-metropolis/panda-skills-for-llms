# Panda Cursor + Claude Skills

Public backup of first-party global skills from local Cursor and Claude installations.

## Scope and Exclusions

- Included: `~/.cursor/skills`, `~/.cursor/skills-cursor`, and `~/.claude/skills`
- Excluded: plugin caches and third-party skills (including Superpowers cache paths)

## Cursor Skills (skills/)

- `approve-pr`: Approve a pull request after quick merge-readiness checks. Use when the user asks to approve a PR, mark review as approved, or run a final go/no-go before approval.
- `fix-terminal-error-and-re-run`: Diagnose terminal command failures, identify root cause from recent terminal output, apply targeted fixes, and safely rerun commands.
- `grill-me`: Ask structured, high-signal discovery questions to fully clarify product specs, UX behavior, technical architecture, constraints, and user preferences before implementation.
- `merge-pr`: Merge an open GitHub pull request by PR number using `gh` CLI with safety checks.
- `merge-pr-merge`: Merge an open GitHub pull request by PR number using `gh` CLI with merge-commit as default.
- `open-pr`: Compare current branch against main and draft a pull request title/body with summary and test plan.
- `review-open-pr`: Review an open pull request and classify findings into four buckets.
- `spec-driven-development`: Enforce split-spec workflow using PRD, UI-SPEC, and TECH-SPEC with hybrid execution gates.
- `test-driven-development`: Enforce test-first and verification loops for feature work, including unit and regression coverage.
- `workflow-agent-pipeline`: Workflow pipeline helper skill.

## Cursor Skills (skills-cursor/)

- `babysit`: Keep a PR merge-ready by triaging comments, resolving clear conflicts, and fixing CI in a loop.
- `canvas`: Build rich Cursor Canvas artifacts for analytical and data-heavy outputs.
- `create-hook`: Create Cursor hooks, `hooks.json`, and supporting scripts.
- `create-rule`: Create Cursor rules and persistent AI guidance in project/global rule files.
- `create-skill`: Create Cursor Agent Skills and guidance around `SKILL.md` structure.
- `create-subagent`: Create and configure reusable subagents.
- `migrate-to-skills`: Migrate older command/rule logic into skill format.
- `shell`: Run shell-focused workflows safely and effectively.
- `split-to-prs`: Split current work into small reviewable pull requests.
- `statusline`: Configure Cursor CLI status line and prompt footer context.
- `update-cli-config`: Modify Cursor CLI config values and defaults.
- `update-cursor-settings`: Modify Cursor/VSCode user settings in `settings.json`.

## Claude Skills (claude-skills/)

- `approve-pr`: Approve a pull request after quick merge-readiness checks.
- `babysit`: Keep a PR merge-ready by triaging comments, resolving clear conflicts, and fixing CI.
- `brainstorming`: Required before creative work; explores intent and requirements before implementation.
- `canvas`: Build live React canvas artifacts for analytical deliverables.
- `create-hook`: Create Cursor hooks and hook automation.
- `create-rule`: Create Cursor rules for persistent AI guidance.
- `create-skill`: Guide creation of effective Agent Skills.
- `create-subagent`: Create reusable subagents.
- `dispatching-parallel-agents`: Coordinate 2+ independent tasks across parallel agents.
- `executing-plans`: Execute written implementation plans with checkpoints.
- `finishing-a-development-branch`: Choose merge/PR/cleanup path after implementation.
- `fix-terminal-error-and-re-run`: Diagnose and recover failed terminal commands.
- `grill-me`: Run structured discovery for specs, architecture, and constraints.
- `merge-pr`: Merge open PRs with safety checks.
- `merge-pr-merge`: Merge open PRs with merge-commit default.
- `migrate-to-skills`: Migrate workflows into skill-based structure.
- `open-pr-personal`: Draft personal-project PR title/body using a non-Jira template.
- `receiving-code-review`: Triage and validate code review feedback rigorously before changes.
- `requesting-code-review`: Request review after major changes or before merge.
- `review-open-pr`: Review open PRs and classify findings.
- `shell`: Shell-focused execution helper.
- `spec-driven-development`: Drive implementation from explicit PRD/UI/TECH specs.
- `split-to-prs`: Split larger work into multiple reviewable PRs.
- `statusline`: Configure CLI status line and footer behavior.
- `subagent-driven-development`: Execute plans with independent tasks in the same session.
- `systematic-debugging`: Follow rigorous debugging process for bugs and failures.
- `test-driven-development`: Use TDD for features and bug fixes.
- `update-cli-config`: Modify CLI config behavior.
- `update-cursor-settings`: Modify editor settings in `settings.json`.
- `using-git-worktrees`: Use isolated git worktrees for safer feature work.
- `using-superpowers`: Establish skill discovery and invocation workflow at session start.
- `verification-before-completion`: Verify with commands before claiming completion.
- `workflow-agent-pipeline`: Pipeline orchestration helper.
- `writing-plans`: Write implementation plans before touching code.
- `writing-skills`: Create/edit/verify skills before deployment.
