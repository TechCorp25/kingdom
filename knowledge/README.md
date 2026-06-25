# knowledge/ — Kingdom's filesystem knowledge base

Durable, CC-facing knowledge for the Kingdom control plane and the projects it tracks.
This is the *filesystem* counterpart to the structured `Memory` rows in Postgres: prose
that should survive across sessions and load cheaply at the start of work.

## Layout
```
knowledge/
  global/        Owner-approval-gated (Req 4). Supreme contract + environment/identity facts.
    _proposals/  CC writes proposed global changes here; owner promotes via `git mv`.
  policies/      Autonomously updatable rules: the 6 requirements' mechanics + gotchas.
  skills/        Meta-recipes for wielding skills in THIS environment (not skill copies).
  projects/      Per-project briefs (<slug>.md) + auto-generated live state (<slug>.state.md).
```

## How CC reaches this (routes)
1. **SessionStart hook** (`.claude/hooks/session-start.sh`) injects the 6-point operating
   contract with pointers into here — active on every session.
2. **`CLAUDE.md`** names the high-value files so CC reads them on demand (auto-loaded).
3. **Explicit Read** of any path above when a task touches that area.
4. (Future, Phase 7) MCP `list_knowledge` / `read_knowledge` tools mirroring
   `list_artifacts`, so the API and every client can enumerate the tree.

## The operating contract (authoritative: `global/operating-contract.md`)
1. Token-efficient by default — `policies/token-budget.md`
2. `/automate-dev` is the default for code-changing work — `policies/automate-dev-default.md`
3. Autonomous knowledge checkpoint at every green close — `policies/knowledge-maintenance.md`
4. `global/**` changes need owner approval — `policies/global-approval.md`
5. Push Kingdom + draft PR at green run close — `policies/run-close.md`
6. Handover before any compact — `policies/handover.md`

## Editing rules
- `global/**`: never edit directly (hook-enforced). Propose in `global/_proposals/`.
- Everything else: update freely; prefer the checkpoint script for `projects/*.state.md`.
- Keep entries dense and pointer-based — this tree is re-read every session (Req 1).
