# Kingdom

Local-first control plane for AI-assisted software development.
See `CLAUDE.md` for the full stack, conventions, and build order, and
`docs/architecture/0001-stack-decisions.md` for the rationale.

## Quick start

```bash
uv sync                       # create .venv and install everything from the lockfile
cp .env.example .env          # then edit POSTGRES password + secrets
docker compose up -d          # start local Postgres
uv run alembic upgrade head   # apply migrations
uv run kingdom-api            # serve the API at http://127.0.0.1:8000 (docs at /docs)
```

## Common commands

```bash
uv run kingdom-mcp            # run the MCP server over stdio (used by Claude Code)
uv run pytest                # run the test suite (uses in-memory SQLite)
uv run ruff check .          # lint
uv run ruff format .         # format
uv run mypy                  # type-check
uv run alembic revision --autogenerate -m "message"   # new migration
```
