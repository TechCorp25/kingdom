# IlluminateMyGallery — brief (active project)

> Distilled stable brief. **Live state** (current `main` SHA, open items) is in the dated
> `docs/illuminate-my-gallery/kingdom-continuation-<ISO8601>.md` series — read the latest
> before acting; SHAs there are "last observed," verify with the commands below.

- **Slug:** `illuminate-my-gallery` (Illuminate Studios — professional photography studio)
- **Repo:** `git@github.com:techcorp-DevApps/IlluminateMyGallery.git` (branch `main`)
- **On disk:** `projects/illuminate-my-gallery/` (full clone, active). **ONE checkout** —
  there is no `illuminate-my-studio` dir; "studio" naming was an artifact. Gallery is
  canonical.

## Stack
FastAPI backend + Vite/React 19 + Tailwind + shadcn/ui. **MongoDB Atlas** (metadata only)
+ **Cloudflare R2** (image objects) + **Cloudflare Worker** CDN. Hosted on **Railway**
(backend root `/backend`, frontend `/frontend`, publish `build/`).

## Branch & merge discipline
**TWO-SIDED repo: Claude Code + Codex both commit.** `git pull --ff-only origin main`
every session; if it refuses, STOP and reconcile (`policies/merge-hygiene.md`). Never
force-push. Owner-gated merges; squash-merge + delete source branch same step; branch
fresh from verified `main`.

## Non-negotiable architecture rule
```
MongoDB → metadata only.   R2 → image objects only.
Cloudflare Worker + CDN → serves gallery media.
Backend → authorizes, signs, paginates, audits.  Backend does NOT stream image bytes. Ever.
```
- Defining load: 300 parents open a 1,000-image gallery in 30 min ≈ 75 GB transfer — must
  not touch the Railway backend.
- **Originals never in any `<img src>`** — download authorization → 60s presigned URL →
  R2 redirect. No on-the-fly watermarking. Derivatives generated **async**, never in the
  upload request cycle.
- Two private buckets: `R2_BUCKET_ORIGINALS`, `R2_BUCKET_DERIVATIVES`.
  `R2_BUCKET_PUBLIC` is **retired** — never reference it.

## Image pipeline (3 variants/original, no watermark)
thumb-v{n}.webp (100–250 KB) + preview-v{n}.webp (2–5 MB) → derivatives bucket, Worker+CDN;
original.jpg (25–40 MB) → originals bucket, 60s presigned only.
State machine: `created → uploading → uploaded → processing → ready → failed → archived → deleted`.

## Auth (roles immutable by holder; only owner changes roles)
`owner` > `admin` > `editor` > `client`. No self-registration. Legacy `"user"` →
`client` via `normalize_role()` — NOT staff. Tokens stored hashed (SHA-256 / HMAC /
bcrypt); raw values never stored.

## Open workstreams (see latest continuation for current status)
Portfolio image pipeline (owner-decision-gated) · R2 env vars set in Railway · pricing
source-of-truth (5 categories, ~22 packages — not 3 collections) · contracts/consent
(`policies/confidential-areas.md`) · Cloudflare Worker confirmation → Priority 4 gallery
delivery · Dependabot (2 criticals queued).

## Verify at session start
```bash
cd ~/kingdom/projects/illuminate-my-gallery
git fetch origin && git log --oneline -3 origin/main   # compare to latest continuation
git status -sb                                          # expect clean + known untracked
npm run build --prefix frontend                         # expect green
cd backend && JWT_SECRET=x CLIENT_SESSION_SECRET=y CLOUDFLARE_WORKER_SHARED_SECRET=z \
  ./.venv/bin/python -m pytest tests/test_priority2_auth.py -q   # expect 45 passed
```

## Gotchas
`from __future__ import annotations` in FastAPI route/Depends files → HTTP 422
(`policies/python-gotchas.md`). Tailwind `shadow-[var(--x)]` renders nothing
(`skills/frontend-design-recipe.md`). File-based delivery only. `cd` doesn't persist
across CC bash calls.
