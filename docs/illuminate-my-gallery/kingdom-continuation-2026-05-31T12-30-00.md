---
title: "Kingdom — Continuation Baseline (Source of Truth)"
version: "2026-05-31T12-30-00"
---

# Kingdom — Continuation Baseline (Source of Truth)

> **Authoritative baseline as of 2026-05-31T12-30-00 — both repos clean, pushed, session closed.**
> Supersedes all prior continuation baselines. Where this conflicts with any older note, this wins.
> Run §8 verify commands before acting on anything time-sensitive.
> Secrets are never in this document — values live in gitignored `.env` files only.

---

## 1. Identity & environment

- **Owner:** TechCorp (solo developer), Melbourne, Australia.
- **Machine:** ChromeOS, Crostini (Penguin) Linux container. User `techcorp2024`.
- **Workspace root:** `~/kingdom` (= `/home/techcorp2024/kingdom`).
- **Disk:** single btrfs volume, ~17 GB. All working files on native filesystem.
  Never put venvs/git/working copies on `/mnt/chromeos/*` (FUSE — no reliable inodes).
- **GitHub:** account `TechCorp25` (personal). Org `techcorp-DevApps`. Same SSH key.

## 2. SSH & git

- **Key:** `~/.ssh/id_ed25519`, passphrase. `ssh -T git@github.com` → `Hi TechCorp25!`
- No SSH host aliases. Plain `git@github.com:...` remotes. HTTPS push is dead.
- Load key: `eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519` — `kstart` does this.
- git identity: `user.name = techcorp2024`, `user.email = techcorp2024@gmail.com`.

## 3. Kingdom platform

Local-first control plane for AI-assisted development. PostgreSQL + FastAPI +
SQLAlchemy 2.0 async + Alembic + Pydantic v2 + FastMCP. **Not Flask/MongoDB.**

- **Repo:** `git@github.com:TechCorp25/kingdom.git`, `main` @ `cc0f37d`. Clean, pushed.
  Fast-forward `3ab592f..cc0f37d` — continuation baseline + CLAUDE.md git-hygiene block.
  Active Session Baseline pointer → `docs/kingdom-continuation-2026-05-31T11-30-00.md`.
  Note: unrelated automate-dev changes (skills, token_budget_monitor.py, 05-29 continuation
  doc) remain uncommitted — intentionally left untouched this session.
- **Implemented:** `Project`, `Task`, `Memory` — full vertical slice, tested, clean.
- **Not yet built:** repositories, agents, skills, tools, runs, run_events, artifacts.
- **MCP tools (5):** `list_projects`, `get_project`, `search_memories`, `create_task`,
  `list_artifacts`.
- **Context7:** account connector. Do NOT add a second project-pinned one.
- **`automate-dev` skill:** committed at `.claude/skills/automate-dev/`.

## 4. Session startup

```bash
kstart                                        # postgres + ssh key + status (source it)
cd ~/kingdom/projects/illuminate-my-gallery
git pull --ff-only origin main                # mandatory every session
claude
```

## 5. Tracked projects

| Slug | Name | On disk |
|---|---|---|
| `illuminate-my-gallery` | IlluminateMyGallery | full git clone (active) |
| `civic-maps-preview` | CivicMaps-preview | snapshot |
| `lensflow` | lensflow | snapshot |

---

## 6. ACTIVE PROJECT — IlluminateMyGallery (Illuminate Studios)

- **Repo:** `git@github.com:techcorp-DevApps/IlluminateMyGallery.git`, `main` @ `e09b3a2`.
- **Local:** `~/kingdom/projects/illuminate-my-gallery`.
- **Stack:** FastAPI backend + Vite / React 19 + Tailwind + shadcn/ui.
  **Railway** (backend root `/backend`, frontend root `/frontend`, publish `build/`).
  **MongoDB Atlas + Cloudflare R2** for storage. Cloudflare Worker for CDN delivery.
- **TWO-SIDED REPO:** Claude Code + Codex. `git pull --ff-only` every session. If it
  refuses fast-forward: STOP — diagnose before acting (see §7 git hygiene).
- **Branch:** `main` only. All task branches deleted. Remote branches:
  `origin/main`, `origin/conflict_230526_1727` (ignore).

---

### 6.1 Done ✓

- CRA → Vite migration, merged.
- Backend hardening: lazy DB, lifespan, CORS, Luma vendor-neutralisation.
- **Task 1 Phase 1 + Phase 2 — design-system alignment: COMPLETE.**
- **Task 2 Priority 1 — Structural safety audit: COMPLETE.**
- **Task 2 Priority 2 — Auth foundation: COMPLETE. ✅**

  **illuminate-my-gallery main @ e09b3a2** (pushed `c847870..e09b3a2`):
  - `e09b3a2` — `docs(DECISION-RECORD): add §9 git & branch lifecycle ADR`
  - `c847870` — `Task 2 Priority 2: finish auth foundation` (galleries_routes,
    luma H2/M2, rate_limit fix, server.py staff_router, tests, work report)
  - `201df05` — `Task 2 Priority 2: auth foundation` (roles, token_store,
    gallery_media, security/, auth_routes, staff_routes, seed)

  **What is on main (key files):**
  - `backend/roles.py`, `backend/token_store.py`, `backend/gallery_media.py`
  - `backend/security/` — role assertions + rate_limit (no `__future__` annotations)
  - `backend/routes/auth_routes.py`, `staff_routes.py` — fully wired + registered
  - `backend/routes/galleries_routes.py` — `require_staff`, `is_staff()` ownership,
    Task 8 access-token endpoint, Task 9 media-token endpoint
  - `backend/routes/luma_routes.py` — H2/M2 rate limiting
  - `backend/server.py` — staff_router registered (64 routes, 11 routers)
  - `backend/tests/conftest.py` + `test_priority2_auth.py` — 45/45 passing
  - `test_reports/2026-05-31T00-00-00-priority-2-completion-report.md`
  - `.automate-dev/DECISION-RECORD.md` — §9 squash-merge ADR

---

### 6.2 Next: Priority 3 — Storage foundation

**Session start checklist:**
```bash
kstart
cd ~/kingdom/projects/illuminate-my-gallery
git pull --ff-only origin main
git log --oneline -3                      # expect: e09b3a2 at tip
git diff --stat origin/main HEAD          # expect: empty
git branch                                # expect: main only
git status                                # expect: clean
cd backend && ./.venv/bin/python -m pytest tests/test_priority2_auth.py -q
# expect: 45 passed
```

**Priority 3 build items (in order):**

1. **R2 adapter** — `backend/storage.py` has lazy boto3 import. Verify/extend:
   - `generate_presigned_put_url(bucket, key, expires=3600)` — admin uploads
   - `generate_presigned_get_url(bucket, key, expires=60)` — download redirect
   - `object_exists(bucket, key)` — post-upload verification

2. **`gallery_assets` collection + indexes** — ensure at startup:
   ```js
   db.gallery_assets.createIndex({ gallery_id: 1, sort_order: 1 })
   db.gallery_assets.createIndex({ gallery_id: 1, visibility: 1, sort_order: 1 })
   db.gallery_assets.createIndex({ gallery_id: 1, created_at: -1 })
   db.gallery_assets.createIndex({ asset_id: 1 }, { unique: true })
   db.gallery_assets.createIndex({ r2_original_key: 1 }, { unique: true })
   ```

3. **Upload intent endpoint** — `POST /api/galleries/{id}/assets/upload-intent`
   (require_staff): create `gallery_asset` (status: `created`), return presigned PUT
   URL for `R2_BUCKET_ORIGINALS` + `{asset_id, upload_url, key}`.

4. **Upload confirm endpoint** — `POST /api/galleries/{id}/assets/{asset_id}/confirm`
   (require_staff): `object_exists` → status `uploaded` → enqueue derivatives
   (status → `processing`).

5. **Async derivative generation** — background task or Railway worker:
   - Pillow → `thumb-v1.webp` (100–250 KB) + `preview-v1.webp` (2–5 MB)
   - Upload to `R2_BUCKET_DERIVATIVES`, update asset status → `ready`
   - On failure → `failed`. **Never in the HTTP request cycle.**

6. **Processing status in admin UI** — per-asset state visible.

**Processing state machine:**
```
created → uploading → uploaded → processing → ready → failed → archived → deleted
```

**R2 env vars:**
```
R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY
R2_ENDPOINT_URL=https://{account_id}.r2.cloudflarestorage.com
R2_BUCKET_DERIVATIVES=illuminate-prod-derivatives
R2_BUCKET_ORIGINALS=illuminate-prod-originals
R2_CUSTOM_DOMAIN=https://media.illuminatestudios.com.au
```

**Object key pattern:**
```
prod/galleries/{gallery_id}/assets/{asset_id}/original.jpg
prod/galleries/{gallery_id}/assets/{asset_id}/thumb-v1.webp
prod/galleries/{gallery_id}/assets/{asset_id}/preview-v1.webp
```

**Test approach:** mock boto3 at adapter boundary. `mongomock_motor` + `conftest.py`
pattern continues. No `from __future__ import annotations` on FastAPI class dependencies.

---

### 6.3 Remaining build sequence

- **Priority 4** — Gallery delivery (cursor-paginated asset API, Worker cookie,
  selections, download authorization + 302 redirect, client protection, virtual grid).
  Prerequisite: confirm Cloudflare Worker at `media.illuminatestudios.com.au`.
- **Priority 5+** — Booking, contracts, invoices (out of scope for Task 2).

---

### 6.4 Application and scale

Non-negotiable architecture rule:
```
MongoDB   → metadata only
R2        → image objects only
Cloudflare Worker + CDN → serves gallery media
Backend   → authorizes, signs, paginates, audits. Never streams image bytes.
```

| Full-res image | 25–40 MB (Canon EOS R2) | Burst concurrency | 500 target / 1,000 hardening |
|---|---|---|---|
| Images/gallery | 300–1,000 / 2,000 school | Monthly R2 growth | 100–850 GB |

---

### 6.5 Two buckets — both private

| Env var | Bucket | Contents | Access |
|---|---|---|---|
| `R2_BUCKET_DERIVATIVES` | `illuminate-prod-derivatives` | Thumbs, previews | Cloudflare Worker R2 binding |
| `R2_BUCKET_ORIGINALS` | `illuminate-prod-originals` | Originals | Backend presigned URLs only |

`R2_BUCKET_PUBLIC` retired. Staging mirrors: `illuminate-staging-*`.

---

### 6.6 Auth summary

Roles: `owner` / `admin` / `editor` / `client`. Legacy `"user"` → `client` via
`normalize_role()`. All tokens hashed at rest. JWT 8h + bcrypt refresh 7d for staff.
Client: 30-day session or magic link. Gallery media JWT: 4h HMAC HttpOnly cookie.

---

### 6.7 Authoritative docs in repo

| Path | What |
|---|---|
| `test_reports/full_scale_infra_assessment_2026-05-27.md` | Storage/DB plan of record |
| `test_reports/2026-05-31T00-00-00-priority-2-completion-report.md` | P2 work report |
| `.automate-dev/DECISION-RECORD.md` | Living ADR (§9 = squash-merge hygiene) |
| `task2-handoff-brief-FINAL.md` | Complete Task 2 build spec |

---

## 7. Operating conventions

- Production-ready, complete code. No placeholders, stubs, or truncation.
- Preserve existing functionality. No breaking changes without approval.
- Files not copy-paste (mobile Claude corrupts unicode). Files only.
- Work reports: ISO 8601 datetime-prefixed Markdown.
- Multi-step builds: `automate-dev`, one task at a time.
- Verify by running. Build green ≠ works.
- Test harness: `mongomock_motor` + litellm stub + `get_limiter().reset()` — see
  `backend/tests/conftest.py`.
- `from __future__ import annotations` must NOT be in `security/rate_limit.py` or
  any module used as a FastAPI class-instance `Depends()`.

### Git / merge hygiene (codified 2026-05-31)

PRs are squash-merged. A squash severs branch ancestry — `--ff-only` will refuse
afterward. That refusal = branch diverged; diagnose before acting, never force past.

- Never force-push a post-squash feature branch onto main.
- To land post-squash commits: cherry-pick onto `origin/main`, verify tree + tests,
  fast-forward push.
- "Committed locally" ≠ "on main". Always verify: `git diff --stat origin/main HEAD`
  (expect empty) at session start.
- Delete source branch at the same time as the squash-merge. Never keep committing
  on a branch whose earlier state was squashed.

Full ADR: `.automate-dev/DECISION-RECORD.md §9`.

## 8. Verify-live commands

```bash
# Kingdom platform
cd ~/kingdom && git log --oneline -3 && git status --short
uv run pytest -q                          # expect: 11 passed

# Active project — every session start
cd ~/kingdom/projects/illuminate-my-gallery
git pull --ff-only origin main
git log --oneline -3                      # expect: e09b3a2 at tip
git diff --stat origin/main HEAD          # expect: empty
git branch && git status                  # expect: main, clean
npm run build --prefix frontend           # expect: green, 2958 modules
cd backend && JWT_SECRET=x CLIENT_SESSION_SECRET=y CLOUDFLARE_WORKER_SHARED_SECRET=z \
  ./.venv/bin/python -m pytest tests/test_priority2_auth.py -q
# expect: 45 passed
```

## 9. Things NOT to do

- Don't pin a second Context7 MCP server.
- Don't commit secrets or `.env` files.
- Don't silently change `railway.toml` — flag it.
- Don't stream image bytes through the backend. Ever.
- Don't generate derivatives synchronously — async only.
- Don't reference `R2_BUCKET_PUBLIC` — retired.
- Don't force-push. If `--ff-only` refuses, diagnose.
- Don't extract zips via ChromeOS Files GUI — drops dotfiles.
- Don't assume green build = working.
- Don't add `from __future__ import annotations` to `security/rate_limit.py`.
- Don't keep committing on a branch after its earlier state was squash-merged.
- Don't assume "committed locally" = "on main".

## 10. Roadmap

1. ✅ Task 1 design-system alignment — on `main`
2. **Task 2 — IN PROGRESS**
   - ✅ Priority 1 structural safety audit
   - ✅ Priority 2 auth foundation — `main` @ `e09b3a2`
   - → **Priority 3 storage foundation — NEXT**
   - ⬜ Priority 4 gallery delivery (confirm Worker first)
3. Resolve "builds-but-not-viewable" (CORS / Vite `allowedHosts`)
4. Task 1 Phase 3 page migration — after Task 2 stable

## 11. Key file index

| Path | What |
|---|---|
| `~/kingdom/CLAUDE.md` | Kingdom conventions incl. git hygiene (updated 2026-05-31) |
| `~/kingdom/docs/kingdom-continuation-2026-05-31T11-30-00.md` | Baseline in Kingdom repo |
| `~/kingdom/scripts/bootstrap/kingdom-start.sh` | `kstart` launcher |
| `~/kingdom/projects/illuminate-my-gallery/FIRST-SESSION.md` | IMG cold-start |
| `~/.ssh/id_ed25519` | SSH key (passphrase) |
| `~/kingdom/.env` | Kingdom secrets (gitignored) |

---
*Filename: kingdom-continuation-2026-05-31T12-30-00.md*
*Session fully closed. illuminate @ e09b3a2, Kingdom @ cc0f37d. Both pushed.*
*Priority 3 storage foundation is next.*
