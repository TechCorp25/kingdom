---
title: "Kingdom — Continuation Baseline (Source of Truth)"
version: "2026-05-31T12-00-00"
---

# Kingdom — Continuation Baseline (Source of Truth)

> **Authoritative baseline as of 2026-05-31T12-00-00 — session fully closed. Priority 3 next.**
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

- **Repo:** `git@github.com:TechCorp25/kingdom.git`, branch `main`. Pushed (includes
  continuation baseline commit `8d7a3f4` + CLAUDE.md + DECISION-RECORD §9 update).
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

- **Repo:** `git@github.com:techcorp-DevApps/IlluminateMyGallery.git`, `main`.
- **Local:** `~/kingdom/projects/illuminate-my-gallery`.
- **Stack:** FastAPI backend + Vite / React 19 + Tailwind + shadcn/ui.
  **Railway** (backend root `/backend`, frontend root `/frontend`, publish `build/`).
  **MongoDB Atlas + Cloudflare R2** for storage. Cloudflare Worker for CDN delivery.
- **TWO-SIDED REPO:** Claude Code + Codex. `git pull --ff-only` every session. Never
  force-push. If pull refuses fast-forward: STOP and diagnose (see §7 merge hygiene).
- **Current branch:** `main` at `c847870`. All task branches deleted.
  Only remote branches remaining: `origin/main`, `origin/conflict_230526_1727`.

---

### 6.1 Done ✓

- CRA → Vite migration, merged.
- Backend hardening: lazy DB, lifespan, CORS, Luma vendor-neutralisation.
- **Task 1 Phase 1 + Phase 2 — design-system alignment: COMPLETE.**
- **Task 2 Priority 1 — Structural safety audit: COMPLETE.**
- **Task 2 Priority 2 — Auth foundation: COMPLETE. ✅ main @ c847870.**

  Session close actions completed:
  - `origin/storage/task-2-atlas-r2` deleted; local branch force-deleted (`-D`
    required because cherry-pick gives different SHAs — content was byte-verified
    identical on main first).
  - Kingdom repo: continuation baseline committed (`8d7a3f4`), `~/kingdom/CLAUDE.md`
    git-hygiene block added, `.automate-dev/DECISION-RECORD.md §9` added, Kingdom
    baseline pointer updated to `05-31`. All pushed.
  - Kingdom DB: task created recording P2 complete @ c847870, P3 next.

---

### 6.2 Next: Priority 3 — Storage foundation

**Session start checklist:**
```bash
kstart
cd ~/kingdom/projects/illuminate-my-gallery
git pull --ff-only origin main
git log --oneline -3                      # expect: c847870 at tip
git branch                                # expect: main only
git status                                # expect: clean
# Confirm P2 work is on origin/main (not just local):
git diff --stat origin/main HEAD          # expect: empty
cd backend && ./.venv/bin/python -m pytest tests/test_priority2_auth.py -q
# expect: 45 passed
```

**Priority 3 build items (in order):**

1. **R2 adapter** — `backend/storage.py` has lazy boto3 import. Verify/extend:
   - `generate_presigned_put_url(bucket, key, expires=3600)` — admin uploads
   - `generate_presigned_get_url(bucket, key, expires=60)` — download redirect
   - `object_exists(bucket, key)` — post-upload verification

2. **`gallery_assets` collection + indexes** — ensure at startup (lifespan or
   bootstrap script):
   ```js
   db.gallery_assets.createIndex({ gallery_id: 1, sort_order: 1 })
   db.gallery_assets.createIndex({ gallery_id: 1, visibility: 1, sort_order: 1 })
   db.gallery_assets.createIndex({ gallery_id: 1, created_at: -1 })
   db.gallery_assets.createIndex({ asset_id: 1 }, { unique: true })
   db.gallery_assets.createIndex({ r2_original_key: 1 }, { unique: true })
   ```

3. **Upload intent endpoint** — `POST /api/galleries/{id}/assets/upload-intent`
   (require_staff): create `gallery_asset` (status: `created`), return presigned
   PUT URL for `R2_BUCKET_ORIGINALS` + `{asset_id, upload_url, key}`.

4. **Upload confirm endpoint** — `POST /api/galleries/{id}/assets/{asset_id}/confirm`
   (require_staff): `object_exists` check → status `uploaded` → enqueue derivatives
   (status → `processing`).

5. **Async derivative generation** — background task or Railway worker:
   - Download original from `R2_BUCKET_ORIGINALS`
   - Pillow → `thumb-v1.webp` (100–250 KB) + `preview-v1.webp` (2–5 MB)
   - Upload both to `R2_BUCKET_DERIVATIVES`
   - Update asset: status → `ready`, record keys + dimensions
   - On failure: status → `failed`
   - **Never synchronous in the request cycle** — 40 MB files will time out Railway

6. **Processing status in admin UI** — per-asset state visible in gallery management.

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

**Test approach:** mock boto3 at the adapter boundary. `mongomock_motor` + `conftest.py`
pattern from Priority 2 continues to apply.

---

### 6.3 Remaining build sequence

- **Priority 4** — Gallery delivery (cursor-paginated asset API, Worker cookie
  integration, selections, download authorization + 60s presigned URL + 302 redirect,
  client-side protection layer, virtualized frontend grid).
  **Prerequisite:** confirm Cloudflare Worker deployed at
  `media.illuminatestudios.com.au` — flag to owner if not.
- **Priority 5+** — Booking, contracts, invoices (out of scope for Task 2).

---

### 6.4 Application and scale

High-resolution burst-access gallery platform. Defining load: 300 parents open a
1,000-image childcare gallery within 30 min — ~75 GB optimised media transfer.
This load cannot touch the Railway backend.

**Non-negotiable architecture rule:**
```
MongoDB   → metadata only
R2        → image objects only
Cloudflare Worker + CDN → serves gallery media
Backend   → authorizes, signs, paginates, audits
Backend   → does NOT stream image bytes. Ever.
```

| Dimension | Value |
|---|---|
| Full-res image size | 25–40 MB (Canon EOS R2) |
| Images/gallery | 300–1,000 typical; 2,000 school/event |
| Burst concurrency | 500 target; 1,000 hardening |
| Monthly R2 growth | 100–850 GB |
| 12-month R2 | 1.2–10 TB |

---

### 6.5 Image pipeline

| Variant | File | Size | Bucket | Delivery |
|---|---|---|---|---|
| Thumbnail | `thumb-v{n}.webp` | 100–250 KB | `illuminate-prod-derivatives` | Cloudflare Worker + CDN |
| Preview | `preview-v{n}.webp` | 2–5 MB | `illuminate-prod-derivatives` | Cloudflare Worker + CDN |
| Original | `original.jpg` | 25–40 MB | `illuminate-prod-originals` | 60s presigned URL only |

Originals never in any `<img src>`. `R2_BUCKET_PUBLIC` retired. Both buckets private.

---

### 6.6 CDN delivery — Cloudflare Worker-gated

Worker on `media.illuminatestudios.com.au` via R2 binding. Client gets 4-hour
gallery media JWT as HttpOnly `gallery_token` cookie on gallery page load. Worker
validates → fetches derivatives → `Cache-Control: public, max-age=31536000, immutable`.
Cloudflare edge caches; subsequent requests never hit Worker or R2.

---

### 6.7 Auth and permissions

| Role | Created by | Access |
|---|---|---|
| `owner` | System bootstrap | Everything |
| `admin` | Owner invite | Everything except settings, billing, inviting staff |
| `editor` | Owner invite | Galleries and bookings only |
| `client` | System on gallery token claim | Gallery view, selections, downloads |

Legacy `"user"` role → `client` via `normalize_role()` — never treated as staff.
All tokens hashed at rest; raw values never stored.

---

### 6.8 Authoritative docs in repo

| Path | What |
|---|---|
| `test_reports/full_scale_infra_assessment_2026-05-27.md` | Storage/DB plan of record |
| `test_reports/2026-05-31T00-00-00-priority-2-completion-report.md` | P2 work report |
| `.automate-dev/DECISION-RECORD.md` | Living ADR (§9 = squash-merge hygiene) |
| `task2-handoff-brief-FINAL.md` | Complete Task 2 build spec |
| `FIRST-SESSION.md` | Cold-start brief |

---

## 7. Operating conventions

- **Production-ready, complete code.** No placeholders, no stubs, no truncation.
- **Preserve existing functionality.** No breaking changes without approval.
- **Files not copy-paste.** Mobile Claude corrupts unicode on paste. Files only.
- **Prompt framing:** task-context, not persona/role.
- **Work reports:** ISO 8601 datetime-prefixed Markdown (`YYYY-MM-DDTHH-MM-SS-name.md`).
- **Multi-step builds:** `automate-dev`, one task at a time.
- **Verify by running.** Build green ≠ works.
- **Test harness** — `mongomock_motor` backs `db._db`; `litellm` stubbed via
  `sys.modules`; rate limiter reset in `fresh_state` autouse fixture (`conftest.py`).
- **`from __future__ import annotations` must NOT be used in `security/rate_limit.py`**
  or any module used as a FastAPI class-instance `Depends()`.

### Git / merge hygiene (added 2026-05-31)

PRs are squash-merged. A squash commit on `main` is NOT an ancestor of its source
branch — `--ff-only` will refuse after a squash merge. That refusal means the branch
diverged; never force past it.

- Never force-push a post-squash feature branch onto `main` (erases the PR commit).
- To land commits made after a squash: cherry-pick the genuinely-new commits onto
  `origin/main`, verify tree + tests, then fast-forward push.
- "Committed locally" ≠ "on main". Before building on prior work, confirm it shipped:
  `git diff --stat origin/main HEAD` (expect empty).
- Delete the source branch in the same step as the squash-merge. Never keep committing
  on a branch whose earlier state was squashed — that is how work gets stranded.
- Session start checklist includes `git diff --stat origin/main HEAD` for this reason.

## 8. Verify-live commands

```bash
# Kingdom platform
cd ~/kingdom
git log --oneline -3 && git status --short
uv run pytest -q                          # expect: 11 passed
uv run alembic current                    # expect: 0001_initial (head)

# Active project — start of every session
cd ~/kingdom/projects/illuminate-my-gallery
git pull --ff-only origin main
git log --oneline -3                      # expect: c847870 at tip
git diff --stat origin/main HEAD          # expect: empty (P2 verified on remote)
git branch                                # expect: main only
git status                                # expect: clean
npm run build --prefix frontend           # expect: green, 2958 modules

# Regression check
cd backend
JWT_SECRET=x CLIENT_SESSION_SECRET=y CLOUDFLARE_WORKER_SHARED_SECRET=z \
  ./.venv/bin/python -m pytest tests/test_priority2_auth.py -q
# expect: 45 passed
```

## 9. Things NOT to do

- Don't pin a second Context7 MCP server.
- Don't commit secrets or `.env` files.
- Don't silently change `railway.toml` or Railway service config — flag it.
- Don't stream image bytes through the backend. Ever.
- Don't use on-the-fly watermarking.
- Don't generate derivatives synchronously in the upload request cycle — async only.
- Don't create or reference `R2_BUCKET_PUBLIC` — retired.
- Don't run stateful shell commands as one-off Claude Code Bash calls — ephemeral.
- Don't force-push. `git pull --ff-only` only; if it refuses, diagnose first.
- Don't extract zips via ChromeOS Files GUI — drops dotfiles. Use terminal `unzip`.
- Don't assume green build = working.
- Don't add `from __future__ import annotations` to `security/rate_limit.py`.
- Don't keep committing on a branch after its earlier state was squash-merged to main.
- Don't assume "committed locally" = "on main" — verify with `git diff --stat origin/main HEAD`.

## 10. Roadmap

**Immediate (IlluminateMyGallery):**
1. ✅ Task 1 design-system alignment — on `main`
2. → **Task 2: MongoDB Atlas + R2 + Auth — IN PROGRESS**
   - ✅ Priority 1 structural safety audit — on `main`
   - ✅ Priority 2 auth foundation — on `main` at `c847870`
   - → **Priority 3 storage foundation — NEXT** (see §6.2)
   - ⬜ Priority 4 gallery delivery (confirm Cloudflare Worker first)
3. Resolve "builds-but-not-viewable" (CORS / Vite `allowedHosts`)
4. Task 1 Phase 3 page migration — after Task 2 stable
5. Confirm Cloudflare Worker at `media.illuminatestudios.com.au` before Priority 4

**Kingdom platform Phase 3+:** remaining entities via vertical-slice pattern.

## 11. Key file index

| Path | What |
|---|---|
| `~/kingdom/CLAUDE.md` | Kingdom conventions (git hygiene block added 2026-05-31) |
| `~/kingdom/docs/kingdom-continuation-2026-05-31T11-30-00.md` | This baseline in repo |
| `~/kingdom/docs/runbooks/2026-05-24T08-00-00-kingdom-runbook.md` | Ops runbook |
| `~/kingdom/scripts/bootstrap/kingdom-start.sh` | `kstart` launcher |
| `~/kingdom/projects/illuminate-my-gallery/FIRST-SESSION.md` | IMG cold-start |
| `~/.ssh/id_ed25519` | Account SSH key (passphrase) |
| `~/kingdom/.env` | Kingdom secrets (gitignored) |

---
*End of baseline. Filename: kingdom-continuation-2026-05-31T12-00-00.md*
*Session fully closed 2026-05-31. Both repos clean and pushed. Priority 3 is next.*
*Next update on session close: kingdom-continuation-YYYY-MM-DDTHH-MM-SS.md*
