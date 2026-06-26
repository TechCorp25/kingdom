# Skill recipe — automate-dev (how to wield it here)

The skill bundle lives in `.claude/skills/automate-dev/`. This file is the *meta*
guidance for using it in the Kingdom environment. Policy: `policies/automate-dev-default.md`.

## When
Default path for code-changing work (build/fix/refactor/feature/multi-file). It is the
primary mechanism for multi-step builds. Stays OFF for questions/reads/audits (Req 1).

## How to run well
- **One task at a time.** Scope to a single task, let it close green, then the next.
  Don't hand it a multi-task batch — it loops build→review→test→fix per task.
- **Frame as task + operating context + explicit verification**, never as a persona.
- **Trust the gates over the script's score.** Its Python review scripts
  (`scripts/code_reviewer.py`, `references/quality-gates.md`) are heuristic and
  **non-authoritative for JSX/JS** — lint/types/tests + human/Codex review decide.
- **Verify by running**, not by green build alone. A green build ≠ it works / renders.
- It is the executor; architectural decisions and irreversible/owner-gated steps stay
  above it. Don't let it self-approve a merge or a deploy.

## Close-out (every green task)
1. Knowledge checkpoint — `policies/knowledge-maintenance.md` (Req 3).
2. At run end — `policies/run-close.md` (Req 5, Kingdom push + draft PR).
3. Handover if closing/context-heavy — `policies/handover.md` (Req 6).

## Guardrails
- Security-critical work: approve file changes one-by-one (option 1), never bulk; don't
  push past ~70–80% context.
- Zero breaking changes without explicit owner approval; preserve existing functionality.
