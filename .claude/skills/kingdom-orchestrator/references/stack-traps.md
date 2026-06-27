---
title: "Hard rules + Kingdom-stack traps"
source: "§6 + §7 of the Kingdom orchestrator manual"
---

# Universal hard rules & gotchas (§6, full)

- **Git diff is truth, not CC's task checkboxes.** "Committed locally" ≠ "on main." Always verify with raw
  `git status` / `git diff --stat` / `git log -- <path>`.
- **Green gate ≠ correct, and grep-confirmed ≠ runtime-confirmed.** A passing `ruff`/`mypy`/`pytest` gate proves
  the static checks; a config/compose/env fix verified only by `grep` is **not** runtime-verified — say so
  explicitly and carry the caveat forward.
- **Verify on-disk state**, not the editor buffer — confirm with `git status` + `grep`.
- **Stage by explicit path; commit per concern.** Never `git add -A`, especially on a dirty or multi-committer
  tree. Confirm exactly the intended files are staged before committing.
- **`/clear`, not `/compact`** for high-context sessions. Commit at a clean boundary → `/clear` → re-enter from
  the committed files + continuation baseline.
- **Security/infra-critical work is not pushed past ~70–80% context.** Stop, commit, hand off.
- **JSON/TOML hand-edits are brittle** — edit via a parser, validate, confirm with `git diff` + `grep`.
- **Don't commit secrets or `.env` files.** Prefer fail-fast env idioms (`${VAR:?message}`) over silent
  placeholder defaults.
- **Acceptance criteria come from the canonical reference** (the live policy/operating-contract/doc), not a
  styling or diff impression.
- **Additive-only to shared knowledge/policies/config** — never modify or remove existing global knowledge
  without the owner-gated `_proposals/` + `git mv` flow.
- Files, not copy-paste, for **everything** handed to the owner.

# Kingdom-stack-specific traps (§7, full)

- **Version-triple alignment.** Keep `.venv` interpreter = `ruff`/`mypy` targets = the documented stack version
  = `.python-version` in lockstep. A drifted `.venv` (e.g. an undocumented newer interpreter) is a hygiene
  finding: align to the **documented** version via `uv venv --clear --python <X> && uv sync` and pin
  `.python-version`; treat adopting a new version as a **deliberate CLAUDE.md stack change**, not a hygiene fix.
  The rebuild swaps the gitignored `.venv` (won't show in the diff) and regenerates console scripts.
- **`uv sync` is the rebuild path.** An intermediate `uv venv` error can be harmless if `sync` then rebuilds on
  the pinned version — confirm `python --version` + a full green gate on the rebuilt venv before trusting it.
- **docker-compose env.** Use fail-fast `${VAR:?set VAR in .env}` (no silent `change_me`); keep `.env.example`
  honest and matched to the config defaults (e.g. driver `asyncpg` vs `psycopg` must match `config.py`). A
  compose runtime check may be skipped when docker isn't present — that's **grep-verified, not runtime-verified**.
- **The maintenance scripts are behaviour, not docs.** `knowledge-checkpoint.py` re-runs the gate and writes
  `kingdom.state.md`; `register-projects.py` registers projects. A diff to either is a logic change — review it,
  don't wave it through under a "hygiene" label.
- **The `.claude/` hooks enforce protections.** `block-global-knowledge` / `block-global-bash` exist to stop
  unguarded global writes; route around them via `_proposals/` + owner-gated `git mv`, never by disabling them.
- **Dependabot** gets a deliberate own pass, queued after active work — not folded into feature/hygiene merges.
