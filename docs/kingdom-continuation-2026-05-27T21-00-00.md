# Kingdom — Continuation Baseline (Source of Truth)

> **Authoritative baseline as of 2026-05-27T21-00-00 — all Task 2 decisions closed.**
> Supersedes all prior continuation baselines. Where this conflicts with any older note, this wins.
> Run §13 verify commands before acting on anything time-sensitive.
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

---

### 6.1 Done ✓

- CRA → Vite migration, merged. Build green (2958 modules).
- Backend hardening: lazy DB, lifespan, CORS, Luma vendor-neutralisation,
  requirements split prod/dev.
- **Task 1 Phase 1 + Phase 2 — design-system alignment: COMPLETE, merged to `main`.**
  Tokens (letterSpacing caps/caps-wide/caps-cta, maxWidth.shell) + component
  primitives (Button editorial variants, SectionShell, SectionLabel, StatusPill,
  PageHeadingBlock). Build verified green.

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

### 6.9 Task 2 in-flight

**All decisions closed. Ready to build.**

Pre-build steps (do in this order):
1. `git pull --ff-only origin main`
2. Read `test_reports/full_scale_infra_assessment_2026-05-27.md`
3. Update `.automate-dev/DECISION-RECORD.md §5` from the handoff brief
4. Create branch `storage/task-2-atlas-r2`
5. `/automate-dev` — Priority 1 first

**Build sequence:**
- Priority 1 — Structural safety audit (existing auth assumptions, backend-only guards)
- Priority 2 — Auth foundation (JWT, sessions, invites, client provisioning, magic link,
  gallery media JWT for Worker)
- Priority 3 — Storage foundation (R2 adapter, gallery_assets, upload pipeline, async
  derivatives via Pillow)
- Priority 4 — Gallery delivery (paginated API, Worker cookie integration, selections,
  download authorization, client protection layer, virtualized frontend grid)
- Priority 5+ — Booking, contracts, invoices (out of scope for Task 2)

**Handoff brief:** `2026-05-27T21-00-00-task2-handoff-brief-FINAL.md`
(complete build instructions, code patterns, all env vars).

---

### 6.10 Authoritative docs in repo

| Path | What |
|---|---|
| `test_reports/full_scale_infra_assessment_2026-05-27.md` | Storage/DB plan of record |
| `.automate-dev/DECISION-RECORD.md` | Living ADR (update §5 before building) |
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
git log --oneline HEAD..origin/main       # what's new from Codex
git branch                                # expect: main only
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

## 10. Roadmap

**Immediate (IlluminateMyGallery):**
1. ✅ Task 1 design-system alignment — DONE
2. → **Task 2: MongoDB Atlas + R2 + Auth.** All decisions closed. See §6.9.
3. Resolve "builds-but-not-viewable" (CORS / Vite `allowedHosts`)
4. Task 1 Phase 3 page migration — after Task 2 stable
5. Confirm Cloudflare Worker deployment with owner before Priority 4

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
*End of baseline. Filename: kingdom-continuation-2026-05-27T21-00-00.md*
*Updated 2026-05-27 — all Task 2 decisions closed.*
*Next update on session close: kingdom-continuation-YYYY-MM-DDTHH-MM-SS.md*
