#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Kingdom — workspace bootstrap (uv-based)
#
# Ensures the directory tree and .gitkeep placeholders exist, installs the
# project with uv (creating .venv from the lockfile), seeds .env from
# .env.example, and initialises git.
#
# Idempotent: safe to run repeatedly. Existing files are never overwritten.
#
# Usage:
#   ./scripts/bootstrap/bootstrap.sh            # tree + uv sync + .env + git
#   ./scripts/bootstrap/bootstrap.sh --no-sync  # skip dependency install
#   ./scripts/bootstrap/bootstrap.sh --help
#
# Workspace root defaults to the script's project root. Override with:
#   KINGDOM_ROOT=/path/to/kingdom ./bootstrap.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# Resolve project root: scripts/bootstrap/ -> two levels up.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KINGDOM_ROOT="${KINGDOM_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
RUN_SYNC=1

for arg in "$@"; do
  case "$arg" in
    --no-sync) RUN_SYNC=0 ;;
    --help|-h) sed -n '3,21p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown argument: $arg (use --help)" >&2; exit 2 ;;
  esac
done

log()  { printf '  \033[0;32m✓\033[0m %s\n' "$1"; }
skip() { printf '  \033[0;90m·\033[0m %s\n' "$1"; }
info() { printf '\033[1m%s\033[0m\n' "$1"; }

info "Kingdom bootstrap → $KINGDOM_ROOT"
cd "$KINGDOM_ROOT"

# ─── 1. Directory tree + .gitkeep ────────────────────────────────────────────
info "1. Directory tree"
DIRS=(
  data/postgres data/backups data/indexes
  artifacts/reports artifacts/exports artifacts/prompts artifacts/snapshots
  projects/civicmaps
  knowledge/global knowledge/projects knowledge/skills knowledge/policies
  docs/architecture docs/runbooks docs/schemas
  scripts/bootstrap scripts/backup scripts/maintenance
  src/kingdom/api src/kingdom/mcp src/kingdom/worker
  src/kingdom/models src/kingdom/migrations/versions
  tests
)
for d in "${DIRS[@]}"; do
  mkdir -p "$d"
  if [ -z "$(ls -A "$d" 2>/dev/null)" ]; then
    touch "$d/.gitkeep"
  fi
done
log "${#DIRS[@]} directories ensured"

# ─── 2. Tooling check: uv ────────────────────────────────────────────────────
info "2. Tooling"
if ! command -v uv >/dev/null 2>&1; then
  echo "  uv not found on PATH. Install it with:" >&2
  echo "    curl -fsSL https://astral.sh/uv/install.sh | sh" >&2
  echo "  then re-open the terminal and re-run this script." >&2
  exit 1
fi
log "uv $(uv --version | awk '{print $2}') found"

# ─── 3. Environment file ─────────────────────────────────────────────────────
info "3. Environment"
if [ -f .env ]; then
  skip ".env exists — left untouched"
elif [ -f .env.example ]; then
  cp .env.example .env
  log ".env seeded from .env.example — set real POSTGRES password + secrets"
else
  skip ".env.example missing — skipped (restore it from the repo)"
fi

# ─── 4. Dependencies (uv sync) ───────────────────────────────────────────────
info "4. Dependencies"
if [ "$RUN_SYNC" -eq 1 ]; then
  uv sync
  log "uv sync complete (.venv ready, console scripts installed)"
else
  skip "skipped uv sync (--no-sync)"
fi

# ─── 5. Git ──────────────────────────────────────────────────────────────────
info "5. Git"
if [ ! -d .git ]; then
  git init --quiet
  log "git repository initialised"
else
  skip ".git exists — left untouched"
fi

# ─── Summary ─────────────────────────────────────────────────────────────────
echo
info "Workspace ready at $KINGDOM_ROOT"
cat <<EOF

Next steps:
  1. Edit .env — set the Postgres password (and keep DATABASE_URL in sync).
  2. docker compose up -d            # start local Postgres
  3. uv run alembic upgrade head     # create the schema
  4. uv run pytest                   # confirm everything is green
  5. uv run kingdom-api              # API at http://127.0.0.1:8000/docs
  6. cd $KINGDOM_ROOT && claude      # start a Claude Code session
EOF
