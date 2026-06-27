# `docs/` — Kingdom continuation & reference docs

Control-plane documentation for the Kingdom platform and the projects it tracks.
This is **control-plane knowledge, not project business data** (keep stacks separate —
see `CLAUDE.md` → "Purpose").

## Layout

| Path | Holds |
|---|---|
| `docs/<project-slug>/` | Per-project session **continuation** + **handover/handoff** docs (the running history of work on that project). |
| `docs/architecture/` | Kingdom architecture notes. |
| `docs/runbooks/` | Operational runbooks. |
| `docs/schemas/` | Schema references. |

Per-project handovers **nest under `docs/<slug>/`** — never at the `docs/` root.

## Naming

- Continuation baselines: `kingdom-continuation-<ISO8601>.md` or `<slug>-continuation-<ISO8601>.md`
- Orchestrator handoffs: `<ISO8601>-<slug>-...-handoff.md`

Use a sortable timestamp (`YYYY-MM-DDTHH-MM-SS`) so the newest file sorts last.

## Source of truth & retention

- The **newest** continuation file for the active project is the current source of truth.
  `CLAUDE.md` → "Active Session Baseline" points at it explicitly; update that pointer
  whenever a newer baseline supersedes it.
- `knowledge/projects/<slug>.state.md` is the **live auto-checkpoint** (written by
  `scripts/maintenance/knowledge-checkpoint.py`) — the quick machine-readable state.
- **Retention:** keep the most recent baselines per project active; move older ones to
  `docs/<slug>/archive/` to keep the working set legible. Handover docs are history —
  **the owner prunes/archives them; automated agents do not delete them.**
