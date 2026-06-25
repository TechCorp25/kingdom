# Policy — /automate-dev is the default for code-changing work (Req 2)

The `automate-dev` skill (`.claude/skills/automate-dev/`) is the **standard deployment
path** for development work in Kingdom. It runs the full build → review → test → fix
loop with quality gates, rejects band-aid fixes, and enforces zero breaking changes.
Invoke it **without being asked** — it should not require a manual trigger from the owner.

## Fires automatically on (code-changing intent)
build · implement · develop · create feature · fix bug · refactor · migrate · wire up ·
"make it work" · any multi-file edit · anything that should end green-gated.

## Stays direct (do NOT fire the team — Req 1)
questions · explanations · code reading / search / audits · "where is X" · single-file
trivial edits · doc/config/knowledge edits · planning discussions · this kind of
scaffolding work.

The triage rule: **does this change application code and need to end green?** → team.
Otherwise → direct.

## How to run
- One task at a time — scope `/automate-dev` to a single task, let it close green, then
  the next. Don't hand it a multi-task batch.
- It is the executor; architectural decisions and owner-gated steps stay above it (see
  the operating model in the latest continuation doc).
- Its Python review scripts are heuristic and **non-authoritative for JSX/JS** — trust
  the gates (lint/types/tests) and human/Codex review over the script's score.

## Boundary with the rest of the contract
- On green close, the team's work still goes through `knowledge-maintenance.md` (Req 3)
  and, at run end, `run-close.md` (Req 5).
- Security-critical work is not pushed past ~70–80% context; approve CC file changes
  file-by-file (option 1), never bulk-approve, for security-sensitive edits.
