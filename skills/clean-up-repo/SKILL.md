---
name: clean-up-repo
description: >-
  Classifies local and origin branches vs main using diffs, PR state (open/draft),
  ahead/behind counts, and recent commit age; groups branches into Active PRs,
  Active PR + behind main, needs review before deleting, and safe to delete; then
  prompts for category-based deletion (1–4 or all). Agent-agnostic: requires git and
  gh in the environment only. Use when cleaning up branches, pruning stale work,
  or auditing repo branch hygiene before deletes.
---

# Clean up repo (branch audit vs `main`)

## When to use

Invoke when the user wants to **audit branches against `main`**, see **diff/log context**, account for **open or draft PRs**, bucket branches into the four categories below, and optionally **delete remote branches by category** after they pick `1`, `2`, `3`, `4`, or `all`.

## Defaults and assumptions

- **Base branch:** `main` on `origin` (`origin/main`). If the repo uses a different default branch, substitute it everywhere below.
- **“Owner” branches:** Remote heads `origin/<name>` where **either**:
  - `<name>` starts with `GitHub_login/` and `GitHub_login` is from `gh api user -q .login`, **or**
  - the user explicitly asks to include **all** non-`main` remote branches (then skip the prefix filter and label the report “all remote branches”).
- If `gh` is unavailable, stop and say authentication/API is required for PR classification; still list branches with git-only stats if the user agrees.
- **“Commits ahead of `main`”:** `git rev-list --count origin/main..origin/<branch>` (unique commits on the branch not reachable from `origin/main`).
- **“Behind `main`” (for the Active PR + behind main bucket):** `git rev-list --count origin/<branch>..origin/main` > 0 (commits on `main` not in the branch).
- **“Commits in the last 3 days”:** any commit on `origin/<branch>` **not** in `origin/main` has committer date within the last 3 days **or** the branch tip `git log -1 --format=%ct origin/<branch>` is within the last 3 days. If there are **no** commits ahead of `main`, use **only** the tip timestamp for “last activity.”
- **PR check:** For each candidate branch short name `<branch>` (no `origin/` prefix), run  
  `gh pr list --repo "$(gh repo view --json nameWithOwner -q .nameWithOwner)" --head "<branch>" --state all --json number,state,isDraft,url`  
  Treat **open** PRs (`state` is `OPEN`) as present—including **drafts** (`isDraft` true).

## Classification rules (apply in order)

Consider only branches that pass the **owner** filter (unless user waived it).

1. **Active PR + behind main**  
   Branch has at least one **OPEN** PR (draft or not) **and** `git rev-list --count origin/<branch>..origin/main` > 0.

2. **Active PRs**  
   Branch has at least one **OPEN** PR and is **not** placed in bucket 1 (i.e. not behind `main` by the definition above).

3. If **no** OPEN PR for the branch, evaluate git state:
   - **Needs review before deleting:**  
     `commits_ahead == 0` **and** **no** commit activity in the last **3** days per the definition above (stale, looks fully merged or idle—human should confirm before deleting).
   - **Safe to delete:**  
     Any other no-PR case: `commits_ahead > 0` **or** there **is** commit activity within the last 3 days (per the definition above).

## Workflow

1. `git fetch origin --prune` (and ensure `origin/main` exists or resolve default branch).
2. Build the candidate branch list (owner rule or user override).
3. For each branch, record:
   - `git diff --stat origin/main...origin/<branch>` (and optionally `git log --oneline origin/main..origin/<branch>` truncated),
   - `commits_ahead`, `commits_behind` (the behind count above),
   - PR summary from `gh`,
   - tip SHA, tip date, assigned **bucket**.
4. Present a **summary table** grouped by the four buckets (list 1 first if you want PR+behind highlighted at top, else follow numeric order below for the menu).
5. **Deletion prompt (exactly this style):**  
   Ask which categories to delete remote branches for: **`1`** = Active PR + behind main, **`2`** = Active PRs (open/draft, not behind), **`3`** = Needs review before deleting, **`4`** = Safe to delete, **`all`** = union of all four.  
   Require explicit choice; do not delete without a clear answer mapping to those keys.
6. On confirmation:
   - For each branch in selected categories, `git push origin --delete <branch>` (or the user’s remote name if not `origin`).
   - **Warn before deleting bucket 1 or 2:** open PRs may be affected; GitHub may block or leave dangling PR state—confirm override if they still choose it.
   - After deletes, show `git fetch origin --prune` and a short recap.

## Output format

Use clear headings:

- **Active PR + behind main**
- **Active PRs**
- **Needs review before deleting**
- **Safe to delete**

Under each, bullet lines: branch name, ahead/behind counts, PR link or `none`, one-line diff stat or “no diff”, last activity date.

## Edge cases

- **Merged but branch not deleted:** Usually `commits_ahead == 0`; with no PR open, lands in **needs review before deleting** when also stale—intended.
- **Local-only branches:** Include in a separate subsection if the user cares; remote-delete steps do not apply until pushed.
- **Protected branches / delete failures:** Report stderr from `git push` and stop that branch; continue others if the user wants.

## Safety

Never force-delete without the numbered/`all` confirmation. Never delete `main` or the repo’s default release branches.
