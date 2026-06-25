# Policy — autonomous knowledge maintenance (Req 3)

Knowledge is updated **autonomously**, at minimum every time a task or job is
green-gated and cleanly closed. No silent state drift between sessions.

## What "green-gated clean close" means
Lint + types + tests for the relevant repo all pass, the work is committed (or ready to
commit), and the task is actually done — not paused or partial.

## Do this at every such close
```bash
uv run python scripts/maintenance/knowledge-checkpoint.py \
    --slug <project-slug> \
    --summary "<what closed; what is next>" \
    --gate "uv run ruff check ." --gate "uv run mypy" --gate "uv run pytest -q"
```
- The script runs the gates and **refuses to write unless they pass** — so the
  checkpoint is proof-of-green, not a claim.
- If you already ran the gates this turn, use `--assume-green` instead of re-running.
- It prepends a newest-first entry to `knowledge/projects/<slug>.state.md` with the
  timestamp, branch@SHA, gate results, and your summary.
- For a tracked project, point `--repo` at the project checkout so the recorded SHA is
  the project's, not Kingdom's: `--repo projects/<slug>`.

## What to checkpoint vs what to hand over
- **Checkpoint** (this policy) = a short, durable state delta after each task. Cheap,
  frequent, machine-written.
- **Handover** (`handover.md`, Req 6) = the full continuation narrative at run close /
  before compact. Richer, human-readable, supersedes the prior one.
Do both at a run close; the checkpoint feeds the handover.

## The global exception (Req 4)
This autonomy covers `knowledge/projects/`, `knowledge/skills/`, `knowledge/policies/`.
It does **not** cover `knowledge/global/` — those changes are owner-gated; see
`global-approval.md`. The checkpoint script will refuse to write under `global/`.
