# Kingdom — Continuation Baseline (Source of Truth)

> **Purpose.** This document is the authoritative baseline for continuing work on the
> Kingdom platform and its tracked projects. It captures environment, architecture,
> current state, conventions, and direction as of **2026-05-27**. Treat it as the
> single source of truth; where it conflicts with older notes, this wins. Verify live
> state with the commands in §13 before acting on anything time-sensitive (the
> IlluminateMyGallery repo is worked from two sides and advances independently).

> **Secrets are NOT in this document by design.** Database password, R2 keys, and the
> MongoDB Atlas URI live only in gitignored `.env` files on the machine. This doc names
> where they are and how to set them, never their values.

---

## 1. Identity & environment

- **Owner:** TechCorp (solo developer), Melbourne, Australia.
- **Machine:** ChromeOS, Crostini (Penguin) Linux container. User `techcorp2024`.
- **Disk:** single btrfs volume (`/dev/vdc`), ~17 GB. Keep all working files on the
  native filesystem (`~/...`); never put venvs/git/working copies on `/mnt/chromeos/*`
  (9p/FUSE bridge — no reliable symlinks/inodes). Reading a file from `/mnt/chromeos`
  to copy it in is fine; *working* there is not.
- **Workspace root:** `~/kingdom` (= `/home/techcorp2024/kingdom`).
- **GitHub identity:** account `TechCorp25` (personal). Some repos live under the
  `techcorp-DevApps` org; the `TechCorp25` account key has access to both.

## 2. SSH & git authentication (clean single-key setup)

- **One account key:** `~/.ssh/id_ed25519`, titled `claude-kingdom` on GitHub, registered
  as an **authentication** SSH key on the `TechCorp25` account. It has a **passphrase**.
- `ssh -T git@github.com` greets **`Hi TechCorp25!`** (a username = account key; if it ever
  greets a `repo/name`, that's a deploy key and is wrong for general push).
- **No SSH host aliases.** Earlier `github-techcorp` alias and the `id_ed25519_techcorp`
  deploy key were deleted. Use plain `git@github.com:...` remotes.
- After a reboot the agent is empty; load once per shell: `eval "$(ssh-agent -s)" &&
  ssh-add ~/.ssh/id_ed25519` (the `kstart` launcher in §9 does this).
- **Always use SSH remotes** (`git@github.com:...`). HTTPS push fails — GitHub password
  auth is dead.
- git identity: `user.name = techcorp2024`, `user.email = techcorp2024@gmail.com`.

## 3. The Kingdom platform — what it is

Local-first **control plane** for AI-assisted software development: manages projects,
tasks, runs, memories, and artifacts, consumed primarily by Claude Code via an MCP
server. Deliberately separate from the business data of the projects it tracks. Uses
**PostgreSQL by design** — NOT Flask/MongoDB (that stack belongs to other projects).

### Stack (authoritative)
| Layer | Choice |
|---|---|
| Package/proj mgr | **uv** (pyproject.toml + uv.lock; never pip/requirements) |
| Language | Python 3.12+ (system has 3.14; uv re-syncs `.venv` to it — normal) |
| API | **FastAPI** + **uvicorn** (async, OpenAPI at `/docs`) |
| DB | **PostgreSQL** (local for dev) |
| ORM | **SQLAlchemy 2.0** async, `asyncpg` driver, typed `Mapped[...]` |
| Migrations | **Alembic** (async `env.py`) |
| Settings/validation | **Pydantic v2** + **pydantic-settings** |
| MCP server | official **`mcp` SDK FastMCP**, stdio transport |
| Lint/format/types/tests | ruff · mypy (strict) · pytest + pytest-asyncio + httpx |
| Optional queue | Redis (only if the worker needs it) |

### Repo
- **Remote:** `git@github.com:TechCorp25/kingdom.git`, branch `main`.
- **Status:** clean, pushed, correct authorship.

## 4. Kingdom layout (src layout)

```
pyproject.toml          uv project: deps, entry points, ruff/mypy/pytest config
uv.lock                 committed lockfile
alembic.ini             migration config (URL injected from settings at runtime)
docker-compose.yml      local Postgres option (unused — running native instead)
.mcp.json               MCP server config (kingdom server)
CLAUDE.md               root memory/conventions for Claude Code
src/kingdom/
  config.py             pydantic-settings Settings (reads ~/kingdom/.env)
  db.py                 lazy async engine + session factory + session_scope()
  services.py           business logic shared by API and MCP (single source of truth)
  models/base.py        Base + UUID/Timestamp mixins + naming convention
  models/entities.py    Project, Task, Memory
  api/app.py            FastAPI app factory + routes; entry point `kingdom-api`
  mcp/server.py         FastMCP server + 5 tools; entry point `kingdom-mcp`
  worker/               background execution (not yet built)
  migrations/           Alembic env.py + versions/0001_initial.py
tests/                  pytest suite (in-memory aiosqlite; no Postgres needed)
data/ artifacts/ projects/ knowledge/ docs/ scripts/
.claude/skills/automate-dev/   committed skill (see §8)
.claude/settings.local.json    personal state — GITIGNORED
```

Console entry points (pyproject `[project.scripts]`): `kingdom-api`, `kingdom-mcp`.

### Repo boundary
- **Committed:** platform code, tests, migration, `uv.lock`, docs, scripts, folder
  structure (`.gitkeep`), the `automate-dev` skill.
- **Gitignored:** `.env` (secrets), `.venv/` (regenerable via `uv sync`), `projects/*/`
  (vendored project source — tracked elsewhere), `artifacts/*/` contents (snapshots/
  binaries/outputs), `.claude/settings.local.json`.

## 5. Database (local PostgreSQL)

- Role `kingdom`, database `kingdom`, owner `kingdom`. Password is in `~/kingdom/.env`
  (NOT in this doc).
- `DATABASE_URL` form (async driver mandatory): `postgresql+asyncpg://kingdom:<PW>@localhost:5432/kingdom`.
- Created once with: `sudo -u postgres psql -c "CREATE ROLE kingdom LOGIN PASSWORD '<PW>';" -c "CREATE DATABASE kingdom OWNER kingdom;"`
- Service is **not** auto-started on Crostini: `sudo service postgresql start` (use
  `service`, never `systemctl`).
- Schema applied via `uv run alembic upgrade head` (migration `0001_initial`:
  projects, tasks, memories).

## 6. Data model & current build state

- **Models implemented (vertical slice):** `Project`, `Task`, `Memory` — fully wired
  model → migration → service → API route → MCP tool, tested, ruff-clean, mypy-strict-clean.
- **Remaining documented entities (not yet built):** repositories, agents, skills, tools,
  runs, run_events, artifacts. Add each by the SAME pattern: model in `entities.py` →
  service fn in `services.py` → expose via API route and/or MCP tool →
  `uv run alembic revision --autogenerate -m "..."` → `upgrade head`.
- **Business logic lives in `services.py`**, shared by API and MCP so the two surfaces
  never diverge. Keep route handlers and tool functions thin.

## 7. MCP server & connectors

- **kingdom server:** `.mcp.json` → `/home/techcorp2024/kingdom/.venv/bin/kingdom-mcp`
  (the installed console script; created by `uv sync`). Connected in Claude Code,
  verified read + write against live Postgres.
- **Tools (5):** `list_projects`, `get_project`, `search_memories`, `create_task`,
  `list_artifacts`. `list_artifacts` is filesystem-backed (reads `artifacts/`); the
  rest hit Postgres.
- **Context7:** connected via the **claude.ai account connector** (not a project pin),
  2 tools (`query-docs`, `resolve-library-id`). Available in every session automatically.
  Do NOT add a second/project-pinned Context7 — it would duplicate the tools.
- Other account connectors present: Supabase (29 tools), Google Drive / Jam / Slack
  (need auth; ignore unless needed).

## 8. Skills & tooling

- **`automate-dev`** — committed to the repo at `.claude/skills/automate-dev/`
  (SKILL.md + agents/ + commands/ + references/ + scripts/). Autonomous
  build→review→test→fix workflow with quality gates. Invoke `/automate-dev`, scope to
  ONE task at a time. This is the primary mechanism for multi-step build work.
- Other built-in Claude Code skills available: code-review, verify, run, security-review,
  init, etc.

## 9. Session startup (automated)

- **Launcher:** `~/kingdom/scripts/bootstrap/kingdom-start.sh`, aliased as **`kstart`**
  (alias in `~/.profile`). It starts Postgres (idempotent), loads the SSH key (one
  passphrase prompt — unavoidable), and prints status. **Must be sourced** to persist
  the key into the shell (the alias does this).
- **Every new session:**
  ```bash
  kstart                                          # postgres + ssh key + status
  cd ~/kingdom/projects/<project>
  git pull --ff-only origin main                  # stay current (see §11)
  claude                                          # Claude Code session
  ```
- Post-reboot extras if needed: Claude Code may require `/login` again until its session
  persists.

## 10. Tracked projects

Registry lives in the Kingdom database (`projects` table); source lives under
`~/kingdom/projects/<slug>/` (gitignored from the control-plane repo). Reconcile the set
with `scripts/maintenance/register-projects.py` (`--dry-run`/`--prune` supported).

| Slug | Name | On disk |
|---|---|---|
| `illuminate-my-gallery` | IlluminateMyGallery | full git clone (active work — see §11) |
| `civic-maps-preview` | CivicMaps-preview | snapshot |
| `lensflow` | lensflow | snapshot |

## 11. ACTIVE PROJECT — IlluminateMyGallery (Illuminate Studios)

**This is the live work.** It is the priority focus of current sessions.

- **Repo:** `git@github.com:techcorp-DevApps/IlluminateMyGallery.git`, branch `main`
  (the org repo; `TechCorp25` key has access).
- **Local:** `~/kingdom/projects/illuminate-my-gallery` (a real git checkout, not a
  snapshot).
- **Stack:** FastAPI backend + **Vite** / React 19 + Tailwind + shadcn/ui frontend.
  Deployed on **Railway** (backend service root `/backend`, frontend service root
  `/frontend`, publish `build/`). Storage/DB target: **MongoDB Atlas + Cloudflare R2**.
- **TWO-SIDED REPO:** worked both from here (Claude Code in Kingdom) AND by an external
  **Codex** workflow (PRs on `codex/...` branches). **ALWAYS `git pull --ff-only origin
  main` at the start of every session.** If a pull refuses to fast-forward, STOP and
  reconcile; never force.

### Done
- **CRA → Vite migration:** complete, merged to `main`, production build green
  (`npm run build` → `build/`, ~2958 modules). Verified on-machine.
- Backend hardening (lazy DB, lifespan/non-fatal seed, storage/CORS hardening, Luma
  vendor-neutralisation), requirements split prod/dev.

### Current problem (the reason work continues)
**The app builds and deploys successfully but is NOT currently viewable.** A green build
is necessary but NOT sufficient — success = the deployed frontend actually renders and
reaches the backend. The fault likely intersects CORS, Vite `allowedHosts`, or asset/
image serving via R2 (recent commits already touched CORS and `allowedHosts` — verify
before assuming a fresh code bug).

### Urgent tasks (priority order) — both flagged URGENT for first operational use
1. **Design-system alignment** — plan of record: `frontend/docs/design-system-audit-workplan.md`.
   Existing design groundwork already in repo under `design-system/` (Codex-built:
   tokens.ts, foundations, components, patterns, brand assets). Reconcile against the
   work plan; **non-breaking alignment only** — no changes to existing rendered UI
   without explicit approval. Read the work plan AND the `design-system/` tree before
   creating anything (avoid duplication).
2. **Storage / DB integration — MongoDB Atlas + Cloudflare R2** — plan of record:
   `test_reports/full_scale_infra_assessment_2026-05-27.md`. Resolve the open
   image-security decision (Pattern A vs B, watermarking, download gating) recorded in
   `.automate-dev/DECISION-RECORD.md` BEFORE building image storage/serving — it
   determines the R2 access model.

### In-flight work (mid-session at time of this baseline)
A Claude Code session began **task 1** on branch **`ds/phase-1-tokens-and-primitives`**,
making **additive** Tailwind token edits (`letterSpacing`: caps/caps-wide/caps-cta;
`maxWidth.shell: 1400px`) inside `tailwind.config.js` `extend`. This was NOT yet
committed/merged when this baseline was written. **On continuation: check git state
first** — `git -C ~/kingdom/projects/illuminate-my-gallery branch` and `git status` —
to see whether that branch exists, what it contains, and whether to resume, commit, or
discard it before proceeding.

### Authoritative docs to READ before acting (in the repo)
1. `frontend/docs/design-system-audit-workplan.md` (design-system plan of record)
2. `test_reports/full_scale_infra_assessment_2026-05-27.md` (storage/DB plan of record)
3. `.automate-dev/DECISION-RECORD.md` (living ADR; open image-security decisions)
4. `design-system/` tree (existing groundwork)
5. `FIRST-SESSION.md` (the cold-start brief already committed to the repo)

### Run locally
```bash
cd backend && pip install -r requirements.txt        # dev: requirements-dev.txt; env per backend/.env.example
cd frontend && npm install
VITE_BACKEND_URL=http://localhost:8000 npm run dev    # or `npm run build` → build/
```

## 12. Operating conventions (apply to all work)

- **Production-ready, complete code only.** No placeholders, no `# ... unchanged`, no
  half-built scaffolds, no TODO stubs in delivered code.
- **Preserve existing functionality.** No breaking changes without explicit approval.
- **Consistent naming/imports**; resolve root causes, not band-aids.
- **Deliver code/config as downloadable files**, never copy-paste blocks — the mobile
  Claude app corrupts smart quotes/unicode on paste. File download is the canonical
  transfer method.
- **Prompt framing:** task-context, not persona/role ("You are an expert…" is rejected —
  it reduces self-checking). Frame by task, constraints, operating context, with explicit
  pre-output verification checklists.
- **Work reports:** ISO 8601 datetime-prefixed Markdown filenames
  (`YYYY-MM-DDTHH-MM-SS-descriptor.md`). YAML frontmatter where the consuming system
  expects it.
- **Explanations:** clear and concise — no bloat, no reasoning-validation padding.
- **Multi-step builds:** use `automate-dev` (build → review → simplify → test → fix loop
  with quality gates), one task at a time.
- **Verify by running**, not by asserting (build green ≠ works; see the IlluminateMyGallery
  "not viewable" lesson).

## 13. Verify-live commands (run on continuation)

```bash
# Kingdom platform health
cd ~/kingdom
git log --oneline -3 && git status --short
uv run pytest -q                      # expect: 11 passed
uv run alembic current                # expect: 0001_initial (head)
uv run kingdom-api                     # http://127.0.0.1:8000/health → "database":"ok"

# MCP server (Postgres must be up)
ls -la .venv/bin/kingdom-mcp || uv sync

# Active project state
cd ~/kingdom/projects/illuminate-my-gallery
git fetch origin && git log --oneline HEAD..origin/main   # what's new from Codex side
git branch                            # is ds/phase-1-tokens-and-primitives present?
git status
```

## 14. Things NOT to do (hard-won)

- Don't pin a second/project Context7 MCP server — it's already provided by the account
  connector; pinning duplicates tools.
- Don't commit secrets or `.env` files; don't write secret values into shared docs.
- Don't silently change `railway.toml` or Railway service/deploy config — that's infra
  configuration; flag it, don't edit it.
- Don't run stateful shell commands (`ssh-agent`, `cd` you expect to persist, `export`,
  anything interactive/passphrase) as one-off Claude Code Bash tool calls — each runs in
  an ephemeral subprocess and the effect evaporates. Do those in the real terminal.
- Don't force-push; don't `git pull` without `--ff-only` on the two-sided repo.
- Don't extract zips via the ChromeOS Files GUI — it drops dotfiles; use terminal `unzip`.
- Don't assume a green build means success for IlluminateMyGallery — confirm it renders.

## 15. Direction / roadmap

- **Immediate (IlluminateMyGallery):** finish design-system alignment (task 1), then
  storage/DB integration (task 2), and resolve "builds-but-not-viewable". Keep pulling
  the Codex side.
- **Kingdom platform (Phase 3+):** build out the remaining entities (repositories, agents,
  skills, tools, runs, run_events, artifacts) following the established vertical-slice
  pattern; expand MCP tool surface to match; then repo/project ingestion, knowledge
  indexing, artifact generation, backup/restore, security hardening.
- **Deployment (later):** Kingdom can move to Railway by swapping `DATABASE_URL` to a
  Railway Postgres (asyncpg + SSL) and running `alembic upgrade head` once against it.

## 16. Key file index

| Path | What |
|---|---|
| `~/kingdom/CLAUDE.md` | Kingdom conventions/memory (committed) |
| `~/kingdom/docs/runbooks/2026-05-24T08-00-00-kingdom-runbook.md` | operations runbook |
| `~/kingdom/docs/architecture/0001-stack-decisions.md` | stack ADR |
| `~/kingdom/scripts/bootstrap/kingdom-start.sh` | `kstart` session launcher |
| `~/kingdom/scripts/backup/snapshot-repos.sh` | recoverable repo snapshots |
| `~/kingdom/scripts/backup/verify-and-delete.sh` | verify-then-delete sources |
| `~/kingdom/scripts/maintenance/register-projects.py` | project registry reconcile |
| `~/kingdom/projects/illuminate-my-gallery/FIRST-SESSION.md` | IMG cold-start brief |
| `~/.ssh/id_ed25519` | the one account SSH key (passphrase) |
| `~/kingdom/.env` | Kingdom secrets (gitignored) |

---
*End of baseline. Update this document on every material change of state or direction.*
