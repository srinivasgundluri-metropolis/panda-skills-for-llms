---
name: grill-me
description: Ask structured, high-signal discovery questions to fully clarify product specs, UX behavior, technical architecture, constraints, and user preferences before implementation. Use when requirements are ambiguous, work is medium/large, or as a pre-step in spec-driven-development workflows.
---

# Grill Me

## Purpose
Run a focused question loop to remove ambiguity before planning or coding.

This skill is the discovery front-door for `spec-driven-development`:
- Use this first to gather complete context.
- Then convert answers into spec updates (`PRD.md`, `UI-SPEC.md`, `TECH-SPEC.md`).

## When to invoke
Invoke when any of the following is true:
- The user asks for a new feature, redesign, integration, or refactor.
- Requirements are underspecified or contain hidden tradeoffs.
- Architecture, data model, API shape, security, or rollout is unclear.
- Success criteria, acceptance tests, or UX details are not explicit.

## Operating mode
- Ask concise, specific questions in batches.
- Prefer multiple-choice or constrained options where possible.
- Avoid broad questions when a targeted question can close a decision.
- Continue until uncertainty is low enough to implement safely.

## Required discovery checklist
Do not exit discovery until these areas are resolved (or explicitly deferred):

1. Problem and outcomes
- What user problem is being solved?
- What outcomes define success?
- What is out of scope?

2. Users and UX behavior
- Who are primary users/personas?
- Key flows, edge states, and error states?
- Accessibility and responsive expectations?

3. Product rules and preferences
- Business rules, validations, permissions, and policy constraints?
- Copy/tone, visual style, and interaction preferences?
- Non-negotiables vs nice-to-haves?

4. Technical architecture
- Existing systems touched, boundaries, and integration points?
- Data contracts, schema changes, API changes, migration needs?
- Performance, reliability, observability, and security constraints?

5. Delivery and validation
- Milestones, rollout strategy, and backward compatibility?
- Acceptance criteria and test plan?
- Risks, open questions, and decision owners?

## Question loop protocol
Use this loop repeatedly:
1. Ask the minimum next set of high-value questions.
2. Summarize confirmed decisions and remaining unknowns.
3. Ask follow-up questions only on unresolved or risky areas.
4. Stop only when implementation can proceed with low risk.

## Completion criteria
Discovery is complete only when:
- Core requirements are testable and unambiguous.
- Major architectural decisions are explicit.
- User preferences and UX constraints are captured.
- Acceptance criteria are concrete.
- Remaining unknowns are documented with owner + next action.

## Handoff into spec-driven-development
After discovery:
1. Produce a concise decision summary.
2. Map decisions into spec deltas for:
   - `docs/specs/PRD.md`
   - `docs/specs/UI-SPEC.md` (if UI is involved)
   - `docs/specs/TECH-SPEC.md`
3. Label gate type (hard/soft) and explain why.
4. Proceed to implementation only after specs reflect decisions.

## Output format
When reporting progress, use:
- Confirmed decisions
- Open questions
- Risks/assumptions
- Proposed spec deltas
- Ready-to-implement verdict (`yes`/`no`)

## Guardrails
- Do not jump to implementation while critical unknowns remain.
- Do not ask redundant questions already answered by the user.
- Keep terminology consistent across discovery, specs, and code.
- Prefer fast convergence: fewer, better questions.
