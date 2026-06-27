# `docs/orchestrator/` — Kingdom-environment orchestrator artifacts

Home for the artifacts the **`kingdom-orchestrator`** skill (the claude.ai governance layer) produces.
These are **control-plane** reasoning/handoff artifacts — distinct from any project's continuation series and
from the machine-written `knowledge/projects/kingdom.state.md` checkpoint.

The orchestrator's `scripts/scaffold_artifacts.py` emits ISO-8601-stamped skeletons to a downloads dir
(`--out`); the **owner commits the filled-in file here**, by explicit path.

## What lives here

| File pattern | Produced by | Role |
|---|---|---|
| `kingdom-continuation-<ISO8601>.md` | `scaffold_artifacts.py baseline` | Authoritative **state-of-truth baseline**; newest supersedes the prior, committed in isolation. |
| `<ISO8601>-kingdom-orchestrator-handoff.md` | `scaffold_artifacts.py handoff` | Paired **re-entry handoff** for the next session. |
| `DR-<ISO8601>.md` | `scaffold_artifacts.py dr` | **Decision record** for an environment/governance decision. |

## Conventions

- These are the **orchestrator's own** `kingdom-continuation-*` series — **intentionally separate** from the
  project continuations under `docs/<slug>/` (e.g. `docs/illuminate-my-gallery/`), even where names rhyme.
- **Newest baseline wins** on live facts; `CLAUDE.md → Active Session Baseline` should point at the newest
  `docs/orchestrator/kingdom-continuation-*.md` once one exists.
- Retention follows `docs/README.md`: keep recent baselines active; archive older ones under
  `docs/orchestrator/archive/`. Handover docs are history — the **owner** prunes/archives them.
