# Kingdom — Continuation Baseline (Source of Truth)

> **Authoritative baseline as of 2026-05-29T22-30-00 — Task 2 Priority 2 mostly built and committed.**
> Supersedes all prior continuation baselines. Where this conflicts with any older note, this wins.
> Run §8 verify commands before acting on anything time-sensitive.
> Secrets are never in this document — values live in gitignored `.env` files only.
> **Trust git, not task trackers.** Claude Code's in-session task checkboxes lag behind
> actual file writes; the committed diff is the source of truth for what is done.

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

- **Repo:** `git@github.com:TechCorp25/kingdom.git`, branch `main`. Clean, pushed.
- **Implemented:** `Project`, `Task`, `Memory` — full vertical slice, tested, clean.
- **Not yet built:** repositories, agents, skills, tools, runs, run_events, artifacts.
  Add each via the same vertical-slice pattern (model → service → API/MCP → migration).
- **MCP tools (5):** `list_projects`, `get_project`, `search_memories`, `create_task`,
  `list_artifacts`.
- **Context7:** account connector. Do NOT add a second project-pinned one.
- **`automate-dev` skill:** committed at `.claude/skills/automate-dev/`. Primary
  mechanism for multi-step builds. `/automate-dev`, one task at a time.

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
  force-push. If pull refuses fast-forward: STOP and reconcile.
- **Active branch:** `storage/task-2-atlas-r2` (NOT yet merged to main; do not pull main over it).

---

### 6.1 Done ✓

- CRA → Vite migration, merged. Build green (2958 modules, verified 2026-05-29).
- Backend hardening: lazy DB, lifespan, CORS, Luma vendor-neutralisation,
  requirements split prod/dev.
- **Task 1 Phase 1 + Phase 2 — design-system alignment: COMPLETE, merged to `main`.**
  Tokens (letterSpacing caps/caps-wide/caps-cta, maxWidth.shell) + component
  primitives (Button editorial variants, SectionShell, SectionLabel, StatusPill,
  PageHeadingBlock). Build verified green.
- **Task 2 Priority 1 — Structural safety audit: COMPLETE & committed.**
  Report at `test_reports/2026-05-29T00-00-00-priority-1-safety-audit.md`.
  Findings: H1 (hardcoded seed client creds), H2 (Luma chat unprotected),
  H3 (plaintext/stateless refresh), plus M1–M5 medium findings.
- **Task 2 Priority 2 — Auth foundation: MOSTLY BUILT, committed at `1e61164`.**
  Branch `storage/task-2-atlas-r2`. 13 files, +1285/−46. Done & committed:
  - **H1 fixed:** `seed.py` test client (`client@example.com`) gated behind
    `ENVIRONMENT != production`; owner bootstrap added (`seed_owner`); legacy
    `"user"` role normalised to `client`.
  - **H3 fixed:** stateless refresh JWT replaced with server-side hashed, rotating,
    revocable refresh-token store (`token_store.py`, bcrypt, rotate-on-use).
  - **Role model:** `roles.py` (owner/admin/editor/client + legacy alias);
    `auth.py` deps `require_roles`, `require_owner`, `require_staff`,
    `get_current_admin` (now owner+admin). Role always re-read from DB, never token.
  - **Client auth:** 30-day rolling client sessions, magic-link request/consume,
    set-password flow, gallery-claim auto-provision — all in `routes/auth_routes.py`.
  - **Staff invite flow:** `routes/staff_routes.py` (owner-only invite → accept).
  - **Gallery media token:** `gallery_media.py` (HMAC-SHA256, 4h, HttpOnly cookie).
  - **Security primitives:** `security/tokens.py` (peppered SHA-256 + bcrypt),
    `security/rate_limit.py` (sliding window); rate limits on all auth endpoints (H2/M2).
  - **`.env.example`:** added `ENVIRONMENT`, `CLIENT_SESSION_SECRET`,
    `CLOUDFLARE_WORKER_SHARED_SECRET`, optional `OWNER_EMAIL/PASSWORD`; flagged the
    P3 env-var rename (MONGO_URL→MONGODB_URI, S3_*→R2_*) — NOT done in P2.

---

### 6.2 Current problem

**App builds and deploys but is NOT currently viewable.** Fault likely intersects
CORS, Vite `allowedHosts`, or R2 asset serving. Verify before assuming new code bug.

---

### 6.3 Application and scale

**Illuminate Studios** — professional photography studio.

This is a **high-resolution burst-access gallery platform**.
Defining load case: school/childcare gallery release — hundreds of parents opening
the same gallery within 30–60 minutes of publish. ~75 GB optimised media transfer
in 30 minutes. This load cannot touch the Railway backend.

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

### 6.4 Image pipeline

**Three variants per original. No watermarking.**

| Variant | File | Size | Bucket | Delivery |
|---|---|---|---|---|
| Thumbnail | `thumb-v{n}.webp` | 100–250 KB | `illuminate-prod-derivatives` | Cloudflare Worker + CDN |
| Preview | `preview-v{n}.webp` | 2–5 MB | `illuminate-prod-derivatives` | Cloudflare Worker + CDN |
| Original | `original.jpg` | 25–40 MB | `illuminate-prod-originals` | 60s presigned URL (paid download only) |

Originals never appear in any `<img src>` attribute. Only path to an original:
validated download authorization → backend-issued 60s presigned URL → R2 redirect.

**Object keys (versioned):**
```
prod/galleries/{gallery_id}/assets/{asset_id}/thumb-v1.webp
prod/galleries/{gallery_id}/assets/{asset_id}/preview-v1.webp
prod/galleries/{gallery_id}/assets/{asset_id}/original.jpg
```

**Two buckets — both private at R2 level. No public R2 access. No `r2.dev` subdomain.**

| Env var | Bucket | Contents | Access |
|---|---|---|---|
| `R2_BUCKET_DERIVATIVES` | `illuminate-prod-derivatives` | Thumbs, previews | Cloudflare Worker R2 binding |
| `R2_BUCKET_ORIGINALS` | `illuminate-prod-originals` | Originals | Backend presigned URLs only |

`R2_BUCKET_PUBLIC` is retired from the architecture — no public R2 bucket exists.

Staging mirrors: `illuminate-staging-derivatives`, `illuminate-staging-originals`.

**Upload:** direct-to-R2 via presigned PUT URL. Backend never receives image bytes.
**Derivatives:** async generation (Pillow). Never in request cycle — 40 MB files
will time out a Railway dyno if processed synchronously.

---

### 6.5 CDN delivery — Cloudflare Worker-gated

Both buckets are private. Thumbnails and previews are served via a **Cloudflare
Worker** on `media.illuminatestudios.com.au` using the Worker's R2 binding.

**Flow:**
1. Client loads gallery → backend issues a 4-hour gallery media JWT (HMAC-SHA256,
   signed with `CLOUDFLARE_WORKER_SHARED_SECRET`) set as HttpOnly cookie.
2. Image requests hit `media.illuminatestudios.com.au` with the cookie.
3. Worker validates signature + expiry + gallery_id matches URL path.
4. Worker fetches from R2 derivatives bucket, returns with
   `Cache-Control: public, max-age=31536000, immutable`.
5. Cloudflare edge caches response — subsequent requests served from cache, no Worker
   invocation, no R2 read.

**Revocation:** revoking main session stops new media JWTs being issued. Existing
JWTs expire within 4 hours. Cloudflare Cache Purge API available for immediate
CDN invalidation (admin action, e.g. gallery takedown).

Worker is a separate Cloudflare deployment (not Railway). Flag to owner if not yet
deployed — gallery delivery cannot be verified without it.

---

### 6.6 Image protection — client-side (no watermarking)

Applied to all non-admin users. Admin fully exempt.

1. **Download blocker** — `draggable="false"`, `pointer-events: none`, transparent
   overlay intercepts all pointer events on gallery images.
2. **Context menu disable** — `contextmenu` preventDefault for non-admin.
3. **Long-press disable (iOS + Android)** — CSS `-webkit-touch-callout: none` +
   `touch-action: pan-x pan-y`. Kills iOS save-image sheet at OS layer, no JS needed.
4. **Screenshot overlay (desktop keyboard only)** — Mac Cmd+Shift+3/4/5 + Windows
   PrtSc detected; images set to opacity 0 for 200ms. iOS hardware screenshot is
   undetectable by any web API — documented known gap, not a blocker.

---

### 6.7 Auth and permissions

**Role model:**

| Role | Created by | Access |
|---|---|---|
| `owner` | System bootstrap | Everything |
| `admin` | Owner invite | Everything except settings, billing, inviting staff |
| `editor` | Owner invite | Galleries and bookings only |
| `client` | System on gallery token claim | Gallery view, selections, authorized downloads |

No self-registration. Clients auto-provisioned from booking data on token claim.
Role immutable by holder. Only `owner` can assign/change roles.

**Admin auth:** email + password. JWT 8h. Refresh token 7 days (bcrypt hashed,
rotated on use).

**Client auth (both paths always available):**
- Email + password → 30-day rolling session
- Magic link → 15-min single-use SHA-256 hashed token → 30-day session on click

Client account lifecycle: token link (14-day TTL) → auto-provision → set password
on first access → gallery attached to account → accessible via login until archived.

**Staff invites:** owner assigns role (admin or editor) on invite → staff sets
password on acceptance.

**Token storage — all hashed, raw values never stored:**

| Token | Hash | TTL |
|---|---|---|
| Gallery access token (link) | SHA-256 | 14 days |
| Gallery media JWT (Worker) | HMAC-SHA256 | 4 hours |
| Magic link | SHA-256 | 15 minutes |
| JWT refresh | bcrypt | 7 days |
| Staff invite | SHA-256 | 7 days |

**Backend enforcement:** all admin routes: JWT + role check server-side. All client
routes: session token server-side. Luma AI does not decide authorization.

---

### 6.8 Selections and download authorization

Client selects images from preview gallery → `gallery_selections` (status: pending)
→ admin approves in cockpit → `download_authorizations` created (limit: 3 downloads)
→ client downloads: backend validates → increments count → 60s presigned URL for
original → 302 redirect. No bytes through backend.

**New collections (Task 2):** `gallery_assets`, `gallery_selections`,
`download_authorizations`, `gallery_tokens`, `magic_link_tokens`, `staff_invites`,
`refresh_tokens`.

---

### 6.9 Task 2 Priority 2 — REMAINING work (resume here)

Priority 2 auth foundation is committed at `1e61164` (see §6.1). The session was
cleared at ~90% context after committing. **Remaining Priority 2 items** (the only
work left before Priority 3):

1. **`galleries_routes.py`** — was NOT committed (edit declined at clear). Switch
   `get_current_admin` → `require_staff`; fix owner/editor ownership checks; add
   gallery access-token endpoint + gallery media-token endpoint (Tasks 8 & 9).
2. **`app.py`** — register `staff_routes` router (and any new routers); confirm
   `auth_routes` still registered.
3. **`email_service.py`** — confirm the magic-link, staff-invite, and gallery-access
   senders are present and wired (senders were committed in `1e61164`; verify
   names match the imports in the routes).
4. **H2 Luma guard** — rate-limit + session gate on `POST /api/luma/chat` per audit
   H2/M2. (Confirm whether this landed before clear — verify in `luma_routes.py`.)
5. **Tests + work report** — write tests, save report to `test_reports/`.

**Fresh-session re-entry prompt:**
```
On branch storage/task-2-atlas-r2. Priority 2 auth foundation built & committed (1e61164).
First run: git log --oneline -8 and git status.
Read backend/auth.py, token_store.py, security/, routes/auth_routes.py,
routes/staff_routes.py, seed.py to load what's done.
Finish ONLY the remaining Priority 2 items:
  1. galleries_routes.py: get_current_admin → require_staff, owner/editor checks,
     gallery access-token + media-token endpoints (Tasks 8 & 9)
  2. Register staff_routes (+ new routers) in app.py
  3. Confirm email_service.py senders match route imports
  4. H2: rate-limit + session gate on POST /api/luma/chat per audit H2/M2
  5. Tests + work report to test_reports/
Do not begin Priority 3. Verify all imports resolve before declaring done.
```

**Build sequence (overall Task 2):**
- Priority 1 — Structural safety audit ✅ DONE & committed
- Priority 2 — Auth foundation 🔄 mostly done (see remaining items above)
- Priority 3 — Storage foundation (R2 adapter, gallery_assets, upload pipeline, async
  derivatives via Pillow). Includes the env-var rename: MONGO_URL→MONGODB_URI, S3_*→R2_*.
- Priority 4 — Gallery delivery (paginated API, Worker cookie integration, selections,
  download authorization, client protection layer, virtualized frontend grid)
- Priority 5+ — Booking, contracts, invoices (out of scope for Task 2)

**Handoff brief:** `task2-handoff-brief-2026-05-27T21-00-00.md` (note: brief ends at
§13 — any reference to "§22" is phantom; rate-limit work follows audit H2/M2).

---

### 6.10 Authoritative docs in repo

| Path | What |
|---|---|
| `test_reports/full_scale_infra_assessment_2026-05-27.md` | Storage/DB plan of record |
| `test_reports/2026-05-29T00-00-00-priority-1-safety-audit.md` | Priority 1 audit findings (H1–H3, M1–M5) |
| `.automate-dev/DECISION-RECORD.md` | Living ADR (§5 updated from handoff brief) |
| `frontend/docs/design-system-audit-workplan.md` | Design-system plan |
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

## 8. Verify-live commands

```bash
# Kingdom platform
cd ~/kingdom
git log --oneline -3 && git status --short
uv run pytest -q                          # expect: 11 passed
uv run alembic current                    # expect: 0001_initial (head)
uv run kingdom-api                        # /health → {"database":"ok"}

# Active project
cd ~/kingdom/projects/illuminate-my-gallery
git fetch origin
git log --oneline -8                      # confirm 1e61164 auth foundation present
git branch                                # expect: storage/task-2-atlas-r2 (active)
git status                                # expect: clean
npm run build --prefix frontend           # expect: green, 2958 modules
```

## 9. Things NOT to do

- Don't pin a second Context7 MCP server — account connector already provides it.
- Don't commit secrets or `.env` files.
- Don't silently change `railway.toml` or Railway service config — flag it.
- Don't stream image bytes through the backend. Ever.
- Don't use on-the-fly watermarking — removed from architecture entirely.
- Don't generate derivatives synchronously in the upload request cycle — async only.
- Don't create or reference `R2_BUCKET_PUBLIC` — the concept is retired. Both buckets
  are private; use `R2_BUCKET_DERIVATIVES` and `R2_BUCKET_ORIGINALS`.
- Don't run stateful shell commands as one-off Claude Code Bash calls — ephemeral
  subprocesses; effects evaporate.
- Don't force-push. `git pull --ff-only` only on the two-sided repo.
- Don't extract zips via ChromeOS Files GUI — drops dotfiles. Use terminal `unzip`.
- Don't assume green build = working — confirm the app renders and backend responds.
- Don't reference "§22" of the handoff brief — it does not exist (brief ends at §13).
  Rate-limit work follows the Priority 1 audit's H2/M2 recommendations.
- Don't trust Claude Code's in-session task checkboxes — they lag behind file writes.
  The committed git diff is the truth for what is done.
- Don't `/compact` a high-context Claude Code session as the handoff — commit, then
  `/clear` and re-enter from this baseline + committed files. Files are source of truth.
- Don't let a session push past ~70–80% context on security-critical work — commit at
  a clean boundary and clear, so the sensitive auth code gets full attention.

## 10. Roadmap

**Immediate (IlluminateMyGallery):**
1. ✅ Task 1 design-system alignment — DONE
2. ✅ Task 2 Priority 1 — Structural safety audit — DONE & committed
3. 🔄 **Task 2 Priority 2 — Auth foundation** — mostly built & committed (`1e61164`).
   Finish remaining items in §6.9 (galleries routes, app.py registration, Luma H2
   guard, tests + report).
4. Task 2 Priority 3 — Storage foundation (incl. env-var rename to MONGODB_URI/R2_*)
5. Task 2 Priority 4 — Gallery delivery (confirm Cloudflare Worker deployed first)
6. Resolve "builds-but-not-viewable" (CORS / Vite `allowedHosts`)
7. Task 1 Phase 3 page migration — after Task 2 stable

**Kingdom platform Phase 3+:** remaining entities (repositories, agents, skills,
tools, runs, run_events, artifacts) via vertical-slice pattern; expand MCP surface.

**Deployment later:** swap `DATABASE_URL` to Railway Postgres, `alembic upgrade head`.

## 11. Key file index

| Path | What |
|---|---|
| `~/kingdom/CLAUDE.md` | Kingdom conventions (committed) |
| `~/kingdom/docs/runbooks/2026-05-24T08-00-00-kingdom-runbook.md` | Ops runbook |
| `~/kingdom/docs/architecture/0001-stack-decisions.md` | Stack ADR |
| `~/kingdom/scripts/bootstrap/kingdom-start.sh` | `kstart` launcher |
| `~/kingdom/projects/illuminate-my-gallery/FIRST-SESSION.md` | IMG cold-start |
| `~/.ssh/id_ed25519` | Account SSH key (passphrase) |
| `~/kingdom/.env` | Kingdom secrets (gitignored) |

---
*End of baseline. Filename: kingdom-continuation-2026-05-29T22-30-00.md*
*Updated 2026-05-29 — Task 2 Priority 2 auth foundation committed at `1e61164`; session*
*cleared at ~90% context. Remaining P2 items in §6.9.*
*Next update on session close: kingdom-continuation-YYYY-MM-DDTHH-MM-SS.md*
