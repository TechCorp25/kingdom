# <Project name> — brief (template)

> Copy this to `knowledge/projects/<slug>.md` for a new tracked project. Keep it dense
> and pointer-based (Req 1). Live, changing state goes in the auto-generated
> `<slug>.state.md` (written by `scripts/maintenance/knowledge-checkpoint.py`), not here.

- **Slug:** `<slug>`
- **Repo:** `git@github.com:<owner>/<repo>.git` (branch `<branch>`)
- **On disk:** `projects/<slug>/` (full clone | snapshot)
- **Status:** active | snapshot | archived

## Stack
<language / framework / db / hosting — one or two lines>

## Branch & merge discipline
<two-sided repo? ff-only? owner-gated merges? squash + delete? force-push ban?>
See `knowledge/policies/merge-hygiene.md`.

## Architecture rules (non-negotiable)
<the things that must never be violated for this project>

## Active workstreams (carried forward)
<what's open, the pending decision, the next concrete step, any owner-gated blocker —
or point to the latest continuation doc that holds this>

## Verify commands (run at session start)
```bash
<git state + gates + build, with expected output>
```

## Known gotchas
<project-specific traps; cross-reference knowledge/policies/ rather than re-deriving>
