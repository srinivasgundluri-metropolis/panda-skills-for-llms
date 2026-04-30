---
name: workflow-agent-pipeline
description: Orchestrates a 3-stage delivery workflow: spec-driven planning, implementation, and test-driven verification. Use when starting medium/large features, redesigns, refactors, or any task that needs stronger planning quality and reliable test gates.
---

# Workflow Agent Pipeline

## Purpose
Run work in three strict stages:
1. Spec-driven planning
2. Implementation
3. Test-driven verification

Global workflow reference: `~/.cursor/spec-driven/PLAYBOOK.md`

## Stage 1: Spec-driven planning
- Start with the `spec-driven-development` skill.
- Require spec artifacts before major implementation:
  - `docs/specs/PRD.md`
  - `docs/specs/UI-SPEC.md` (if UI/UX is touched)
  - `docs/specs/TECH-SPEC.md`
  - `docs/specs/RFC.md` (for major product/architecture changes)
  - `docs/specs/ADR.md` (for decisions and rationale)
  - `docs/specs/TRACEABILITY.md` (requirement -> task -> PR -> test mapping)
- Planning model preference:
  - First choice: `claude-opus-4-7-thinking-xhigh`
  - Alternate: `gpt-5.3-codex`
- Output from this stage:
  - Approved scope
  - Acceptance criteria
  - File-level implementation map
  - Requirement IDs (for traceability), e.g. `REQ-001`, `NFR-001`
- Token-saving default: fill only required sections in copied templates.

## Stage 2: Implementation
- Implement only approved spec scope.
- Implementation model preference:
  - First choice: `gpt-5.5-medium`
  - Faster alternate: `composer-2-fast`
- Keep changes incremental and traceable to spec acceptance criteria.

## Stage 3: Test-driven verification
- Use the `test-driven-development` skill.
- Required verification:
  - Unit tests for changed logic/components
  - Regression tests for impacted flows
  - Build/type/lint checks when applicable
- Maintain acceptance-test mapping in `docs/specs/ACCEPTANCE-TEST-MAP.md`.
- If tests fail, return to implementation stage and repeat until green.

## Gating rules
- Hard gate for major changes: do not skip Stage 1.
- Soft gate for minor changes: allow direct implementation, but still run Stage 3.
- Before merge/deploy, complete `docs/specs/RELEASE-RISK-CHECKLIST.md`.

## Completion criteria
- Specs are aligned with delivered behavior.
- Code changes are implemented and test-verified.
- Acceptance criteria are explicitly marked pass/fail.
- Traceability matrix is updated and auditable.
