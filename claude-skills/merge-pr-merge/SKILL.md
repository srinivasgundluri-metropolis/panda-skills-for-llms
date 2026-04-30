---
name: merge-pr-merge
description: Merge an open GitHub pull request by PR number using gh CLI with merge-commit as default. Use when the user asks to merge a PR and provides a PR number.
---

# Merge PR (Merge Commit Default)

## Purpose
Merge an open pull request when the user provides a PR number argument, using a merge commit by default.

## Required input
- `pr_number` (integer), e.g. `1280`

## Workflow
1. Validate input:
   - Ensure PR number is present and numeric.
   - If missing, ask for the PR number.
2. Inspect PR before merge:
   - `gh pr view <pr_number> --json number,title,state,isDraft,mergeStateStatus,headRefName,baseRefName,url`
3. Guardrails:
   - Stop if PR is not `OPEN`.
   - Stop if PR is draft (`isDraft=true`) unless the user explicitly asks to merge draft.
   - Stop if `mergeStateStatus` is clearly blocking (for example: `DIRTY`, `BLOCKED`, `UNKNOWN`), and report reason.
4. Merge:
   - Default method: merge commit with branch deletion.
   - Command:
     - `gh pr merge <pr_number> --merge --delete-branch`
   - If user requests a different method, use `--squash` or `--rebase` instead.
5. Verify:
   - `gh pr view <pr_number> --json state,mergedAt,url`
   - Confirm state is `MERGED`.
6. Report:
   - Return PR URL and merge result.
   - If merge failed, return concise error and next action.

## Notes
- Do not create commits while executing this skill.
- Do not push unrelated local changes.
- If GitHub requires checks/reviews first, report that and stop.

## Example invocation intent
- "merge pr 1280"
- "merge PR #1280"
- "please merge 1280"
