---
title: "Kingdom facts — the environment definition"
source: "§1 of the Kingdom orchestrator manual"
caution: "Re-derive anything here against raw owner output at session start. Never trust verbatim — state moves between sessions and via other committers. Replace any `<…>` at first session."
---

# Kingdom facts — the environment definition

> **Re-derive, don't trust.** This table is the *shape* of the environment, not its live state. At session
> start, confirm the moving parts (repo tip, branch list, venv interpreter, gate result) against raw output the
> owner pastes. A mismatch between this table and live output is a finding, not a typo to overwrite.

| Field | Value |
|---|---|
| Kingdom repo | `git@github.com:TechCorp25/kingdom.git` · default branch `main` (verify tip each session) |
| Workspace root | `~/kingdom` (native filesystem; never `/mnt/chromeos/*` — FUSE/symlink limits) |
| Machine | ChromeOS Crostini (Penguin), user `techcorp2024`. `kstart` = postgres + ssh-add + status (NOT visible to non-interactive `bash` subprocesses — enter the SSH passphrase manually when running scripts, or `kstart` in the shell first). SSH remotes only; key `~/.ssh/id_ed25519` (passphrase). |
| Infra toolchain | Python **3.12** (uv-managed `.venv`, pinned via `.python-version`); gate = `ruff` + `mypy --strict` + `pytest`. Postgres via `docker-compose.yml`; `asyncpg` driver (`DATABASE_URL`). Console scripts via `pyproject.toml`. `.venv` is gitignored. |
| Knowledge base | `knowledge/` — `global/` (commands, environment, operating-contract, ssh-and-git, `_proposals/`), `policies/` (automate-dev-default, confidential-areas, global-approval, handover, knowledge-maintenance, merge-hygiene, python-gotchas, run-close, secrets, stack-boundaries, token-budget), `projects/` (`_template`, per-project state files, `kingdom.state.md`), `skills/` (playbooks/recipes). |
| Automation layer | `.claude/` — `hooks/` (block-global-bash, block-global-knowledge, run-close-reminder, session-start), `settings.json`, `skills/` (automate-dev, handover, kingdom-orchestrator). These enforce protections; do not fight them. |
| Maintenance scripts | `scripts/maintenance/knowledge-checkpoint.py` (re-runs gates, writes `kingdom.state.md`), `register-projects.py`. |
| Docs | `docs/` (`README.md` documents the `docs/<slug>/` layout + retention rule) and per-project doc trees (e.g. `docs/<project>/`, `…/orchestrator/`, `…/decisions/`). |
| Other committers | CC sessions, Codex (PR-review automation), `claude/*` working branches, AND the owner via **direct GitHub upload** (lands on `main` via PR). Treat as a **multi-sided repo**. |
| CC model | Opus 4.8 (re-select if a higher tier is set as default and unavailable). |

**First action at session one:** read the SKILL.md, then read the live `knowledge/policies/` and
`knowledge/global/operating-contract.md` **in full** — they are the binding rules this orchestrator curates and
must layer with; the manual references them by intent, but they are the source of truth. Then run the §5
startup (`references/session-protocol.md`).
