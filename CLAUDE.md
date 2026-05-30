# Kingdom Platform

Local-first control plane for AI-assisted software development.
Root path: `~/kingdom`. Runs on Linux (ChromeOS Crostini / Penguin, user `techcorp2024`).

This file is the root memory for Claude Code. Rules here apply everywhere under
`~/kingdom`. Each tracked project under `projects/` may carry its own `CLAUDE.md`
for project-specific rules, loaded hierarchically when working in that subtree.

## Purpose

Kingdom is the control plane for managing projects, repos, tasks, runs, memories,
and artifacts across AI-assisted development work (first tracked project:
CivicMAPS). It is deliberately separate from the business data of the projects it
tracks — do not mix project business data with Kingdom control-plane data.

## Stack (authoritative)

- Package / project manager: **uv** (pyproject.toml + uv.lock; never pip/requirements)
- Language: **Python 3.12** (typed; mypy strict)
- API: **FastAPI** + **uvicorn** (async, stateless, OpenAPI docs at `/docs`)
- Database: **PostgreSQL 17**
- ORM: **SQLAlchemy 2.0** (async, `asyncpg` driver) with typed `Mapped[...]` models
- Migrations: **Alembic** (async env)
- Validation / settings: **Pydantic v2** + **pydantic-settings**
- MCP server: official **`mcp` SDK FastMCP**, stdio transport
- Lint / format: **ruff**   ·   Types: **mypy (strict)**   ·   Tests: **pytest + pytest-asyncio + httpx**
- Optional queue: **Redis** (only if the worker needs it)

This platform uses PostgreSQL by design. It does NOT use Flask or MongoDB/MongoEngine
— those belong to other projects (Le Répertoire is Flask/Mongo; CivicMAPS is
Node/Express + Postgres). Keep stacks separate.

## Project structure (src layout)

```
pyproject.toml          uv project: deps, entry points, ruff/mypy/pytest config
uv.lock                 locked dependency graph (committed)
alembic.ini             migration config (URL injected from settings at runtime)
docker-compose.yml      local Postgres (localhost-bound)
src/kingdom/
  config.py             pydantic-settings Settings (reads .env)
  db.py                 lazy async engine + session factory + session_scope()
  services.py           business logic shared by API and MCP (single source of truth)
  models/               SQLAlchemy models: base.py (Base + mixins), entities.py
  api/app.py            FastAPI app factory + routes; `kingdom-api` entry point
  mcp/server.py         FastMCP server + 5 tools; `kingdom-mcp` entry point
  worker/               background execution (added when needed)
  migrations/           Alembic env.py + versions/
tests/                  pytest suite (in-memory aiosqlite; no Postgres needed)
data/  artifacts/  projects/  knowledge/  docs/  scripts/
```

Console entry points (defined in pyproject.toml): `kingdom-api`, `kingdom-mcp`.

## MCP server contract

The root `.mcp.json` launches the server via the installed console script:
`/home/techcorp2024/kingdom/.venv/bin/kingdom-mcp` (created by `uv sync`).
Tools share `services.py` with the API, so both surfaces behave identically.
Current tools: `list_projects`, `get_project`, `search_memories`, `create_task`,
`list_artifacts`. Bind everything to localhost; never expose MCP, API, or Postgres
publicly.

## Current state — vertical slice complete

A working slice ships: `Project`, `Task`, `Memory` models → initial Alembic
migration (`0001_initial`) → API routes (`/health`, `/projects`) → all five MCP
tools, with passing tests, clean ruff, and strict mypy. The remaining documented
entities (repositories, agents, skills, tools, runs, run_events, artifacts) are
added by following the exact same pattern: model in `entities.py` → service
functions in `services.py` → expose via API route and/or MCP tool → autogenerate a
migration.

## Conventions

- Production-ready code only. No placeholders, no half-built scaffolds, no TODO stubs.
- Preserve existing functionality. No breaking changes without explicit approval.
- Business logic lives in `services.py`, not in route handlers or tool functions —
  keep API and MCP surfaces thin so they never diverge.
- Typed throughout; `uv run mypy` must stay green (strict mode).
- Configuration via environment variables only (`.env`, gitignored). No secrets in code.
- All DB access is async via `session_scope()` (commit/rollback/close handled).
- Migrations are reviewed before apply; constraint names follow the naming convention
  in `models/base.py` so autogenerate stays deterministic.

## Git / merge hygiene

- PRs are squash-merged. A squash commit on `main` is NOT an ancestor of its source
  branch, so `git merge/pull --ff-only` will refuse afterward — treat that refusal as
  the signal the branch diverged, never as something to force past.
- Never force-push a post-squash feature branch onto `main` (it erases the PR merge).
  To land commits made after a squash, cherry-pick (or `rebase --onto origin/main`)
  only the genuinely-new commits, then fast-forward + push.
- "Committed locally" ≠ "on main". Before building on prior work, confirm it shipped:
  `git diff --stat origin/main HEAD` and check key files exist on `origin/main`.
- Delete the source branch in the same step as the squash-merge, and branch fresh from
  updated `main`. Never keep committing on a branch whose earlier state was squashed —
  that is exactly how work gets stranded off `main`.

## Build order

1. Workspace skeleton ✓
2. Local Postgres via Docker Compose; `uv run alembic upgrade head`
3. Remaining schema entities + migrations
4. API routers for each entity
5. Expand MCP tool surface to match
6. Repo / project registration + ingestion
7. Knowledge indexing
8. Artifact generation
9. Backup + restore scripts
10. Security hardening

## Everyday commands

```bash
uv sync                                              # install from lockfile
uv run kingdom-api                                   # serve API (http://127.0.0.1:8000)
uv run kingdom-mcp                                    # run MCP server (stdio)
uv run pytest                                         # tests
uv run ruff check . && uv run ruff format .           # lint + format
uv run mypy                                            # type-check
uv run alembic upgrade head                            # apply migrations
uv run alembic revision --autogenerate -m "msg"       # new migration
```

## Active Session Baseline
Current source of truth: docs/kingdom-continuation-2026-05-31T11-30-00.md
