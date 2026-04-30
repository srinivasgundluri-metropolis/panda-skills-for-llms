---
name: fix-terminal-error-and-re-run
description: Diagnose terminal command failures, identify root cause from recent terminal output, apply targeted fixes, and safely rerun commands. Use when the user asks to check terminal errors, fix failed commands, clear occupied ports, restart dev servers, or recover from Docker/Next/npm startup issues.
---

# Fix Terminal Error and Re-Run

## Purpose

Use this skill to recover quickly from failed terminal workflows without guessing.

## Workflow

Copy this checklist and update it while working:

```text
Recovery Checklist
- [ ] Read latest terminal output and identify the true failing command
- [ ] Classify error type (env/tooling/process/network/config/path/permissions)
- [ ] Apply the minimum safe fix
- [ ] Re-run only the necessary command(s)
- [ ] Verify healthy state and report exact next step
```

## 1) Read the failure first

- Inspect active terminal output before running new commands.
- Capture:
  - failing command
  - first actionable error line
  - whether process is still running
- Do not rely on secondary warnings if there is a clear primary error.

## 2) Classify error quickly

- **Service not running**: Docker daemon, DB service, Redis, etc.
- **Port conflict**: app says port in use or auto-increments.
- **Path/config error**: missing file, wrong working directory, bad env.
- **Dependency/tooling**: module missing, stale cache, invalid lockfile.
- **Permissions**: operation not permitted, EACCES, socket access.

## 3) Apply targeted fix patterns

### Docker daemon unavailable

- Symptom: `Cannot connect to the Docker daemon ... docker.sock`
- Fix:
  1. Start Docker Desktop / daemon.
  2. Wait until engine is healthy.
  3. Re-run `docker compose up -d --build`.

### Ports in use (3000/3001/3002 style)

- Symptom: server keeps hopping ports, or user wants clean restart.
- Fix:
  1. Kill listeners on target ports.
  2. Verify no listeners remain.
  3. Re-run dev command.

### Next.js stale cache issues

- Symptom: strange webpack cache warnings, stale build behavior.
- Fix:
  1. Remove `.next`.
  2. Re-run `npm run dev` (or build).

### Wrong directory / missing package config

- Symptom: `ENOENT ... package.json` or command cannot find project files.
- Fix:
  1. `cd` into exact app directory.
  2. Re-run command.

### Comment lines pasted into shell

- Symptom: `zsh: command not found: #`
- Fix:
  - Ignore that line and run only real commands (no inline comments).

## 4) Re-run and verify

- Re-run the smallest command set required.
- Confirm expected success signal:
  - dev server: startup banner + local URL
  - docker compose: services healthy in `docker compose ps`
  - backend API: docs endpoint accessible
- If still failing, collect new error and repeat from classification.

## 5) Response format to user

- Keep output concise and action-oriented:
  1. **Root cause** (single sentence)
  2. **Fix applied** (exactly what was done)
  3. **Current state** (running/not running + URL/port)
  4. **Next command** user should run (if any)

## Guardrails

- Do not use destructive repo commands (`git reset --hard`, etc.).
- Prefer killing only the specific conflicting processes/ports.
- Do not claim success until verification step passes.
