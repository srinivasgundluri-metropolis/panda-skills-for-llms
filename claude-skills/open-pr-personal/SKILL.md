---
name: open-pr-personal
description: Drafts a pull request title/body using a personal-project template (no Jira prefix). Use for personal repos when the user asks to open/draft a PR. For work repos with Jira tickets, use the /open-pr slash command instead.
---

# Open PR

## Purpose
Prepare a high-signal PR draft from the current branch by reviewing all changes since divergence from `main`.

## Required inputs
- Base branch: default `main` unless user specifies otherwise.
- Scope: all commits and file diffs in `main...HEAD`.

## Workflow
1. Confirm current branch and working tree status.
2. Fetch latest refs when possible (`git fetch origin`) before diffing.
3. Review complete change scope:
   - `git log --oneline main..HEAD`
   - `git diff --stat main...HEAD`
   - `git diff main...HEAD`
4. Extract:
   - user-visible behavior changes,
   - technical changes (refactors, infra, docs, config),
   - risks and migration notes,
   - testing performed or still needed.
5. Draft PR content in this personal-project format:

```markdown
# Overview
<1-2 short paragraphs on what changed and why>

## What changed
- <key implementation change>
- <key implementation change>

## Why this approach
- <design/implementation rationale>

## Risks / Notes
- <risk or "None identified">

## Testing
- [ ] <test step>
- [ ] <test step>

## Next steps (optional)
- <follow-up item or "None">
```

## Title guidance
- Use imperative style and outcome-focused wording.
- Keep under ~72 chars when possible.
- Prefer prefixes only when repo already uses them (`feat:`, `fix:`, etc.).
- Do not use Jira/ticket prefixes unless the user explicitly requests them.

## Output requirements
- Provide:
  - proposed PR title,
  - PR body draft,
  - short list of open questions (if any).
- If change scope is unclear, ask targeted questions before finalizing draft.

## Optional execution
If user asks to actually open the PR:
1. Ensure branch is pushed (`git push -u origin HEAD` if needed).
2. Create draft PR:
   - `gh pr create --draft --title "<title>" --body "<body>"`
3. Return PR URL.
