---
name: review-open-pr
description: Review an open pull request and classify findings into four buckets. Use when the user asks to review a PR, evaluate merge readiness, or provide code-review feedback with prioritized categories.
---

# Review Open PR

## Purpose
Review the target pull request and return results in exactly these categories:
1. ctirical
2. csn-address-later
3. clean-code-improvements-can-be-done
4. all-good-lgtm

Keep feedback concise and actionable.

## Review Workflow
1. Identify the PR to review (URL, PR number, or current branch PR).
2. Read PR metadata, changed files, and relevant discussion.
3. Focus on correctness first, then risk, then maintainability.
4. Classify every finding into one of the four required categories.
5. If no issues are found, use `all-good-lgtm`.

## Classification Rules
- `ctirical`: Must-fix issues before merge. Examples: broken logic, security risks, data loss, crashes, failing behavior, major regression risk.
- `csn-address-later`: Real issue, but not merge-blocking. Examples: minor robustness gaps, limited edge-case handling, non-critical test gaps.
- `clean-code-improvements-can-be-done`: Refactors/readability improvements that are optional and low risk.
- `all-good-lgtm`: Use only when there are no findings in the first three categories.

## Output Format
Always return only this structure:

```markdown
ctirical
- <item or "none">

csn-address-later
- <item or "none">

clean-code-improvements-can-be-done
- <item or "none">

all-good-lgtm
- <"yes" only if all three sections above are none; otherwise "no">
```

## Quality Bar
- Prefer high-signal findings over long lists.
- Tie each finding to specific file/symbol context when available.
- Do not invent issues; mark sections as `none` when empty.
