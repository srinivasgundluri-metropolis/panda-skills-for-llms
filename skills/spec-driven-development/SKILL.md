---
name: spec-driven-development
description: Enforces split-spec workflow using PRD, UI-SPEC, and TECH-SPEC with hybrid execution gates. Use when starting a new project, planning features, redesigning UI, or implementing medium/large changes that require explicit requirements, design decisions, and acceptance criteria.
---

# Spec Driven Development

## Default behavior
- Treat specs as source of truth before major implementation.
- Reference pack: `templates/spec-driven/PLAYBOOK.md`
- Templates: `templates/spec-driven/`
- Use split specs at:
  - `docs/specs/PRD.md`
  - `docs/specs/UI-SPEC.md`
  - `docs/specs/TECH-SPEC.md`
- For major product/architecture decisions, also require:
  - `docs/specs/RFC.md`
  - `docs/specs/ADR.md`
- Maintain:
  - `docs/specs/TRACEABILITY.md`
  - `docs/specs/ACCEPTANCE-TEST-MAP.md`
  - `docs/specs/RELEASE-RISK-CHECKLIST.md`
- If files do not exist, create them before major code changes.
- Prefer copying templates from this repo into project `docs/specs/` instead of drafting from scratch.

## Hybrid gating policy
- **Hard gate** for major changes:
  - New product flows
  - Landing/dashboard redesigns
  - Cross-cutting architecture changes
  - Multi-file refactors with behavior changes
- **Soft gate** for minor changes:
  - Small visual polish
  - Copy tweaks
  - Isolated low-risk fixes

## Required workflow
1. Confirm scope and success criteria.
2. For planning-heavy work, prefer a stronger planning model:
   - `claude-opus-4-7-thinking-xhigh` or `gpt-5.3-codex`
3. Author or update `PRD.md`:
   - Problem statement
   - User outcomes
   - In-scope / out-of-scope
   - Acceptance criteria with requirement IDs (`REQ-###`, `NFR-###`)
4. Author or update `UI-SPEC.md` (for UX/UI work):
   - Information architecture
   - Visual direction and interaction rules
   - Responsive behavior
   - Accessibility requirements
5. Author or update `TECH-SPEC.md`:
   - Files to change
   - Data/control flow
   - Rollout and validation plan
6. For major decisions, update `RFC.md` and record approved choices in `ADR.md`.
7. Update `TRACEABILITY.md` to map requirement IDs to implementation tasks and tests.
8. Implement only what is approved in specs (faster implementation models are acceptable).
9. Validate implementation against spec acceptance criteria with tests and update `ACCEPTANCE-TEST-MAP.md`.
10. Complete release risk checks in `RELEASE-RISK-CHECKLIST.md`.

## Non-negotiables
- Do not skip specs for major work.
- Do not implement requirements not captured in spec docs without updating specs first.
- Keep terminology consistent between PRD, UI-SPEC, TECH-SPEC, and code.
- Keep specs concise and testable; avoid vague goals.
- Every major requirement must have a requirement ID and test mapping.
- Every major architecture/product decision must be traceable in ADR entries.
- Use table/checklist format whenever possible to minimize tokens.

## Output format for proposals
- When proposing work, present:
  - Scope summary
  - Spec deltas (`PRD.md`, `UI-SPEC.md`, `TECH-SPEC.md`)
  - Implementation steps
  - Validation checklist mapped to acceptance criteria

## Quick checklist
- [ ] `docs/specs/PRD.md` updated
- [ ] `docs/specs/UI-SPEC.md` updated (if UI/UX touched)
- [ ] `docs/specs/TECH-SPEC.md` updated
- [ ] `docs/specs/RFC.md` updated (major changes only)
- [ ] `docs/specs/ADR.md` updated (major changes only)
- [ ] `docs/specs/TRACEABILITY.md` updated
- [ ] `docs/specs/ACCEPTANCE-TEST-MAP.md` updated
- [ ] `docs/specs/RELEASE-RISK-CHECKLIST.md` completed
- [ ] Gate type decided (hard vs soft)
- [ ] Implementation aligned to specs
- [ ] Acceptance criteria verified
