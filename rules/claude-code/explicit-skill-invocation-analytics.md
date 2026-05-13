# Explicit Skill Invocation

- When a relevant skill is available, invoke it explicitly before doing the work.
- Do not rely on "following the pattern" without invocation if the goal includes skill analytics visibility.
- In responses about skill usage, name only skills that were explicitly invoked in this session.

## Workflow Routing

Before starting any task, determine if it requires the `workflow-agent-pipeline` skill:

**Route through `workflow-agent-pipeline` when the task is:**
- A new medium or large feature
- A redesign or significant refactor
- Any change that needs spec artifacts, planning gates, or acceptance-test traceability

**Skip `workflow-agent-pipeline` for:**
- Bug fixes
- Small, well-scoped changes (single function, single file)
- Hotfixes or DAG/config-only changes
- Answering questions or explanations

If in doubt, ask the user before proceeding.
