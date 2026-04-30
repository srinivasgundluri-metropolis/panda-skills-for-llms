---
name: test-driven-development
description: Enforces test-first and verification loops for feature work, including unit and regression coverage. Use when implementing features, fixing bugs, or validating refactors that can introduce regressions.
---

# Test Driven Development

## Core rule
Write or update tests around behavior changes before finalizing implementation.

## Templates to use
- `templates/spec-driven/ACCEPTANCE-TEST-MAP.md`
- `templates/tdd/TEST-PLAN.md`
- `templates/tdd/REGRESSION-CHECKLIST.md`

## Required workflow
1. Identify behavior changes and affected surfaces.
2. Add or update unit tests for new and modified logic.
3. Add or update regression tests for impacted user flows.
4. Map each requirement ID to at least one validating test in `docs/specs/ACCEPTANCE-TEST-MAP.md`.
5. Run tests.
6. Fix failures and rerun until all relevant tests pass.

## Test scope policy
- **Unit tests:** mandatory for changed business logic and reusable UI behavior.
- **Regression tests:** mandatory for key user paths touched by the change.
- **Smoke checks:** run build/type/lint where available.

## Execution guidance
- Prefer targeted test runs first for speed.
- After targeted tests pass, run broader regression suite when risk is medium/high.
- When flaky tests appear, document flake evidence and rerun to confirm.

## Reporting format
- Report:
  - requirement IDs covered (`REQ-###`/`NFR-###`),
  - tests added/updated,
  - command(s) executed,
  - pass/fail results,
  - residual risk or known gaps.

## Completion criteria
- Relevant unit tests pass.
- Relevant regression tests pass.
- No unresolved critical failures remain.

## Token-saving default
- Update `docs/specs/ACCEPTANCE-TEST-MAP.md` with compact rows instead of long prose.
