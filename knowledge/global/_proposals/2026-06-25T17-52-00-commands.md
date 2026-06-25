# Command inventory (Kingdom control plane)

Toolchain: **uv** (never pip/requirements). Everything runs via `uv run …`.

## Session start
```bash
source ~/kingdom/scripts/bootstrap/kingdom-start.sh   # = `kstart`: postgres + ssh key + status
cd ~/kingdom
```

## Everyday
```bash
uv sync                                  # install/restore from lockfile (.venv + console scripts)
uv run kingdom-api                       # FastAPI at http://127.0.0.1:8000 (docs /docs) — FOREGROUND
uv run kingdom-mcp                        # MCP server over stdio (Claude Code launches this) — FOREGROUND
uv run pytest -q                          # test suite (in-memory aiosqlite; no Postgres needed)
uv run ruff check . && uv run ruff format .   # lint + format
uv run mypy                               # strict type-check
```
The API and MCP servers are **foreground** — they hold the terminal until Ctrl+C. Use a
second tab, or stop the server, before running other commands.

## Database / migrations
```bash
sudo service postgresql start                          # after every reboot
uv run alembic upgrade head                             # apply migrations
uv run alembic revision --autogenerate -m "add <x>"    # new migration (review before apply)
uv run alembic current                                  # show applied revision
```

## Maintenance
```bash
uv run python scripts/maintenance/register-projects.py --dry-run --prune <folder> ...
uv run python scripts/maintenance/knowledge-checkpoint.py --slug <slug> --summary "..." \
    --gate "uv run ruff check ." --gate "uv run mypy" --gate "uv run pytest -q"
./scripts/backup/snapshot-repos.sh                      # bundles + worktree archives
```

## Console entry points (pyproject.toml): `kingdom-api`, `kingdom-mcp`
Defined in `[project.scripts]`; created in `.venv` by `uv sync`; `.mcp.json` targets
`kingdom-mcp`.
