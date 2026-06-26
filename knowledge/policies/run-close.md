# Policy — run close: push & PR (Req 5)

At the end of every **planned run** where all todos are complete and green-gated, the
**Kingdom** repo is committed and pushed, and a draft PR exists.

## Scope (owner decision: Kingdom only)
This applies to the Kingdom control-plane repo (`~/kingdom`) on its working branch.
**Tracked project repos are NOT auto-pushed by this policy** — they follow their own
per-project discipline (two-sided CC+Codex repos, `--ff-only`, owner-gated merges; see
`knowledge/projects/<slug>.md`). Pushing a project repo is the project session's job.

## Sequence
```bash
# 1. Green-gate (must pass before anything goes out)
uv run ruff check . && uv run mypy && uv run pytest -q

# 2. Checkpoint knowledge (Req 3)
uv run python scripts/maintenance/knowledge-checkpoint.py --slug kingdom \
    --summary "<run summary>" --assume-green

# 3. Handover if the run is closing / context heavy (Req 6) — commit it in isolation

# 4. Stage explicitly (never `git add -A` on a dirty tree), commit, push
git add <paths>
git commit -m "<message>"
git push -u origin <branch>          # retry w/ backoff on network error only

# 5. Ensure a DRAFT PR exists for the branch (create if missing)
```

## Rules
- Push the working branch named for the run (here: `claude/dreamy-volta-8gzg9z`).
  Never push to `main` directly, never force-push.
- If `git push` fails on a **network** error, retry up to 4× with backoff (2/4/8/16s).
  A non-network rejection (e.g. non-fast-forward) means **diverge — stop and reconcile**,
  see `merge-hygiene.md`.
- After pushing, if no PR exists for the branch, open one as a **draft**.
- Secrets never go out: confirm no `.env` / credentials are staged (`secrets.md`).
