---
name: approve-pr
description: Approve a pull request after quick merge-readiness checks. Use when the user asks to approve a PR, mark review as approved, or run a final go/no-go before approval.
---

# Approve PR

## Purpose
Approve the target PR when it is ready, or clearly explain why approval is blocked.

## Workflow
1. Identify the PR (URL, PR number, or current branch PR).
2. Check for blockers:
   - unresolved critical review findings
   - failing required checks
   - unresolved merge conflicts
   - obvious regression/security risk in the diff
3. If blockers exist, do not auto-approve. Ask the user whether to override approval for this PR.
4. If the user explicitly says to override, approve and mention it was an explicit user override.
5. If the user does not override, return a concise blocker list and keep approval blocked.
6. If no blockers exist, approve the PR.
7. Report final status in a short, explicit format.

## Decision Policy
- Approve only when merge risk is low and no critical concerns remain.
- If uncertainty exists, request one targeted follow-up check instead of approving blindly.
- Explicit user override can bypass blockers when the user directly confirms override.

## Output Format
Use exactly:

```markdown
approval-status: <approved | blocked>
reason:
- <short bullet(s)>
next-step:
- <what to do next, or "none">
```

## Notes
- Keep output brief and actionable.
- Do not invent checks; rely on available PR signals.
