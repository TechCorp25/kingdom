# Kingdom — Continuation Baseline (Source of Truth)

> **Authoritative baseline as of 2026-06-10T13-00-00.**
> Supersedes all prior continuation baselines (most recently 2026-06-07T17-00-00).
> Where this conflicts with any older note, Claude Code compacted summaries, or memory,
> this document wins on facts.
> Run §8 verify commands before acting on anything time-sensitive.
> Secrets are never in this document — values live in gitignored `.env` files only.
>
> **Session-close state:** IMG `main @ 3f05ea9` (clean, in sync with origin). Four PRs
> landed this multi-session run: Luma #14, Mongo #15, CORS #16, plus a direct package.json
> + railway.toml hotfix pair. **DB connection prod-VERIFIED.** **One open thread: the
> frontend redeploy after `3f05ea9` is UNVERIFIED — see §6.2 + the mid-task handoff.**
> Kingdom `main @ 2dd2f34` untouched this session.

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
  **Note:** direct GitHub-web / other-surface commits also land under
  `TechCorp <techcorp2024@gmail.com>` — see §6.11 (the package.json/railway.toml hotfixes
  were authored this way, not by Codex).

## 3. Kingdom platform

Local-first control plane for AI-assisted development. PostgreSQL + FastAPI +
SQLAlchemy 2.0 async + Alembic + Pydantic v2 + FastMCP. **Not Flask/MongoDB.**

- **Repo:** `git@github.com:TechCorp25/kingdom.git`, branch `main @ 2dd2f34`.
  Clean, pushed.
- **Implemented:** `Project`, `Task`, `Memory` — full vertical slice, tested, clean.
- **Not yet built:** repositories, agents, skills, tools, runs, run_events, artifacts.
- **MCP tools (5):** `list_projects`, `get_project`, `search_memories`, `create_task`,
  `list_artifacts`.
- **Context7:** account connector. Do NOT add a second project-pinned one.
- **`automate-dev` skill:** primary mechanism for multi-step builds. One task at a time.
  Launch `claude` from the **project dir** (`~/kingdom/projects/illuminate-my-gallery`),
  not from `~/kingdom`, so git/npm target the IMG repo automatically.
  Skill suite vendored + reproducible at `.claude/skills/` (commit `3f6a387`).

## 4. Session startup

```bash
kstart                                        # postgres + ssh key + status (source it)
cd ~/kingdom/projects/illuminate-my-gallery   # LAUNCH FROM PROJECT DIR, not ~/kingdom
git pull --ff-only origin main                # mandatory — two-sided repo
git log --oneline -3                          # confirm tip = 3f05ea9
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

- **Repo:** `git@github.com:techcorp-DevApps/IlluminateMyGallery.git`.
- **Local:** `~/kingdom/projects/illuminate-my-gallery`.
- **Active branch:** `main @ 3f05ea9`. Clean, in sync with origin. All task branches deleted.
- **Stack:** FastAPI backend (`/backend`) + Vite / React 19 + Tailwind + shadcn/ui
  (`/frontend`, publish `build/`). **Railway** hosting (backend + frontend + derivative
  worker services). **MongoDB Atlas + Cloudflare R2** storage. Cloudflare Worker for CDN.
- **TWO-SIDED REPO:** Claude Code + Codex (+ owner direct-to-main edits via GitHub web).
  `git pull --ff-only` every session. If it refuses: STOP and diagnose (rebase if it's a
  clean divergence with no file overlap; never force).
- **Merge discipline (§7 ADR):** PRs are **squash-merged** to main; delete source branch
  at squash. Squash severs ancestry — `--ff-only` refusing afterward = diverged, diagnose,
  never force. Never reuse a branch whose earlier state was squash-merged. Never
  local-merge a non-ancestor branch.

---

### 6.1 Done ✓

- CRA → Vite migration, merged. Backend hardening.
- **Task 1 Phase 1 + Phase 2 — design-system alignment.**
- **Priority 1 — structural safety audit.**
- **Priority 2 — auth foundation.**
- **Priority 3 — storage foundation** — squash-merged as `d86d4b4` (#11).
- **Codex UI A/B merges** (design-system refresh + mobile sign-in + grain fix).
- **Luma booking fallback fix** — PR #14, squash `339d945`. Reviewed GO (forked-base trap
  caught; net 7 files; preserves session on LLM failure → `needs_human`/`handoff_to_human`).
- **MongoDB Railway/Atlas connection config** — PR #15, squash `695d699`. Reviewed GO
  (8 files, +311/−43; resolver prefers `MONGODB_URI`/`MONGODB_DB_NAME`, legacy
  `MONGO_URL`/`DB_NAME` aliases; `/api/health/db` probe; worker shares resolver).
  **PROD-VERIFIED** — startup log: `MongoDB connection verified
  (database=illuminate_studios, maxPoolSize=20, serverSelectionTimeoutMS=10000)`.
- **CORS + production frontend deploy fix** — PR #16, squash `573d089`. **Landed WITHOUT a
  formal pre-merge review session** (process deviation — §6.11). Post-merge greps
  substituted: `/api/health/db` survived the `server.py` merge; CORS uses
  `allow_credentials=_cors_origins != ["*"]` (safe — no credentials-with-wildcard footgun)
  + `allow_origin_regex` for preview hosts; `railway.toml` switched frontend to a real
  production Vite build served via `npx serve -s build`.
- **packageManager hotfix** — `9310dc3 Update package.json` (direct to main, owner via
  GitHub web): removed the stale `"packageManager": "yarn@1.22.22..."` field that was
  forcing Railpack to install with Yarn and colliding with the `npm ci` build command
  (EBUSY on `node_modules/.vite`). Pre-existing since the Vite migration (`f28d0af`);
  masked until #16 switched to a real `npm` build. An identical local terminal fix
  (`d55516d`) was **deduplicated by git on rebase** (`skipped previously applied commit`).
- **railway.toml build-command simplification** — `3f05ea9 Update railway.toml` (direct to
  main, owner): `buildCommand` changed from
  `npm ci --include=dev && NODE_ENV=production npm run build` → bare `npm run build`,
  relying on Railpack's auto-install. **⚠️ See §6.2 — this is UNVERIFIED and carries a
  dev-dependency risk.**

### 6.2 ★ OPEN THREAD — frontend redeploy after `3f05ea9` is UNVERIFIED (DO FIRST)

**"Builds but not viewable" is NOT yet confirmed closed.** The DB layer is fixed and
prod-verified; the frontend-serving layer is not.

The current `frontend/railway.toml` build command is bare `npm run build` (`3f05ea9`).
**Risk:** Vite lives in `devDependencies` (`"vite": "^6.0.7"`). If Railpack's auto-install
omits devDependencies (e.g. `NODE_ENV=production` set in the build env causing npm to skip
devDeps), `npm run build` → `vite build` fails with `vite: not found`. The prior explicit
command carried `--include=dev` specifically to prevent this.

**First action next session:** redeploy the frontend service from `3f05ea9` and watch the
BUILD log:
- **If build passes** (Railpack installed devDeps, Vite ran, `build/` produced, `serve`
  started) → proceed to the render + preflight verification below.
- **If build fails with `vite: not found`** → restore the explicit install: set
  `frontend/railway.toml` `buildCommand = "npm ci --include=dev && npm run build"`
  (keep `--include=dev`; the `NODE_ENV=production` prefix is optional — `vite build` is
  production by default). Commit directly to main (it's an infra hotfix, surface it),
  redeploy.

**Then the actual close of "builds but not viewable" (only the deploy can answer):**
1. Load the deployed frontend URL — does the site RENDER (real UI, not blank / dev
   artifact)? This proves out the production-build-and-serve change.
2. Watch backend logs for `OPTIONS /api/luma/chat` → must return **200/204, not 400**.
   That 400 preflight failure was the symptom of the CORS problem; its disappearance is
   the direct signal #16's CORS fix works and unblocks Luma end-to-end.
3. Test Luma in the browser — should now get a response (preflight passing unblocks the POST).

Only when the site renders AND the preflight passes is the "builds but not viewable"
problem (open since the 2026-05-27 baseline) closeable.

### 6.3 Application and scale

High-resolution **burst-access gallery platform**. Defining load case: school/childcare
gallery release — hundreds of parents opening one gallery in 30–60 min; ~75 GB optimised
media transfer in 30 min; cannot touch the Railway backend.

**Non-negotiable architecture rule:**
```
MongoDB   → metadata only
R2        → image objects only
Cloudflare Worker + CDN → serves gallery media
Backend   → authorizes, signs, paginates, audits. Never streams image bytes.
```

| Dimension | Value |
|---|---|
| Full-res image size | 25–40 MB (Canon EOS R2) |
| Images/gallery | 300–1,000 typical; 2,000 school/event |
| Burst concurrency | 500 target; 1,000 hardening |
| Monthly R2 growth | 100–850 GB; 12-month 1.2–10 TB |

### 6.4 Image pipeline (unchanged)

Three variants per original, **no watermarking**: `thumb-v{n}.webp` (100–250 KB) and
`preview-v{n}.webp` (2–5 MB) in `illuminate-prod-derivatives` (Worker+CDN);
`original.jpg` (25–40 MB) in `illuminate-prod-originals` (backend 60s presigned URL,
paid download only). Versioned keys `prod/galleries/{gallery_id}/assets/{asset_id}/…`.
Both buckets private; no public R2, no `r2.dev`. `R2_BUCKET_PUBLIC` is retired.
Upload direct-to-R2 via presigned PUT; derivatives async (Pillow + separate worker),
never in the request cycle.

### 6.5 CDN delivery — Cloudflare Worker-gated (unchanged)

Both buckets private. Thumbs/previews served via Cloudflare Worker on
`media.illuminatestudios.com.au` using Worker R2 binding. Backend issues a 4-hour
gallery media JWT (HMAC-SHA256, `CLOUDFLARE_WORKER_SHARED_SECRET`) as HttpOnly cookie;
Worker validates signature + expiry + gallery_id-in-path, returns
`Cache-Control: public, max-age=31536000, immutable`; edge caches thereafter.
Worker is a separate Cloudflare deployment; **flag to owner if not yet deployed — Priority
4 gallery delivery can't be verified without it** (still the long-pole dependency).

### 6.6 Auth and permissions (unchanged)

Roles: `owner` / `admin` / `editor` / `client`. No self-registration; role immutable by
holder; only owner assigns roles. Admin: email+password, JWT 8h, refresh 7d bcrypt rotated.
Client: password (30-day rolling) or magic link (15-min single-use SHA-256). All tokens
hashed at rest. Backend enforces every route server-side; Luma does not decide auth.
Legacy `"user"` role → `client` via `normalize_role()`.

### 6.7 Priority 3 staging checklist — infra-team items (CARRY FORWARD)

P3 code is on main. Infra-provisioning confirmations still required before the staging
exit gate (NOT code work):

1. **Railway worker module path** — service `illuminate-derivative-worker`
   (ID `95c0e2a5-3536-45a1-b629-5cf5fdd8969d`). Deploy contract:
   `docs/2026-05-31T13-00-00-derivative-worker-railway-service-spec.md`. Confirm entry
   point matches. (Mongo review confirmed the worker shares `get_database()`, so it
   inherits `MONGODB_DB_NAME` resolution — the code side of the old `MONGO_URL` mapping
   item is resolved; remaining is the provisioned env-var-name confirmation.)
2. **`MONGODB_URI → MONGO_URL` mapping** — now mostly moot: the #15 resolver reads both.
   Confirm the worker service's actual env var names.
3. **Worker memory ≥ 2 GB** — concurrent Canon decodes at concurrency 4.
4. **R2 CORS on originals bucket** — browser-direct presigned PUT (P3 staging exit gate).

### 6.8 Next: Priority 4 — Gallery delivery

Prerequisite: **confirm Cloudflare Worker deployment** at `media.illuminatestudios.com.au`.
Build items: cursor-paginated asset API; gallery media JWT on page load; gallery access
token validation (14-day claim); selections endpoint; admin approval endpoint; download
endpoint (302 → 60s presigned URL, no bytes through backend); client-side image protection
layer; virtualized grid + lazy thumbnails.

### 6.9 Railway env state (production backend)

Confirmed set (names only): `MONGODB_URI`, `MONGODB_DB_NAME=illuminate_studios`,
`MONGODB_APP_NAME`, `MONGODB_MAX_POOL_SIZE=20`, `MONGODB_SERVER_SELECTION_TIMEOUT_MS=10000`,
`MONGODB_CONNECT_TIMEOUT_MS`, `MONGODB_SOCKET_TIMEOUT_MS`. The URI has no DB in its path
(`/?retryWrites=...`) — DB name comes from `MONGODB_DB_NAME`.

- **Manual `DB_NAME=illuminate_studios` stopgap** was added mid-session to un-break the
  pre-#15 deploy (old code did `_require("DB_NAME")`). Post-#15, the resolver reads
  `MONGODB_DB_NAME` natively (prod-verified), so **`DB_NAME` is now REMOVABLE** — but only
  as a SEPARATE deliberate post-verification action. Leaving it is harmless (resolver
  prefers `MONGODB_DB_NAME`). Don't remove it until the frontend redeploy thread (§6.2) is
  closed and you want to do a clean env pass.
- The `MONGODB_URI` value is clean in Railway (an earlier `\""` was a copy-paste artifact,
  not in the stored value).

### 6.10 Authoritative docs in repo

| Path | What |
|---|---|
| `test_reports/full_scale_infra_assessment_2026-05-27.md` | Storage/DB plan of record |
| `test_reports/2026-06-01T07-06-07-priority-3-storage-foundation-report.md` | P3 report |
| `docs/2026-05-31T13-00-00-derivative-worker-railway-service-spec.md` | Worker contract |
| `.automate-dev/DECISION-RECORD.md` | Living ADR (§9 = squash-merge hygiene) |
| `.automate-dev/reports/` | UI A/B + Luma + Mongo merge-readiness reports |
| `FIRST-SESSION.md` | Cold-start brief |

### 6.11 ★ This session — landed changes, deviations, lineage

**PRs/commits landed on IMG `main` (in order):**

| SHA | What | Reviewed? |
|---|---|---|
| `339d945` | Luma booking fallback fix (PR #14) | Formal GO (report committed `0f04438`) |
| `695d699` | MongoDB Railway/Atlas config (PR #15) | Formal GO (report uncommitted — §6.12) |
| `573d089` | CORS + prod frontend deploy (PR #16) | **NO formal review** (deviation) — post-merge greps only |
| `9310dc3` | Remove stale yarn `packageManager` field | Direct-to-main hotfix (owner) |
| `3f05ea9` | Simplify `railway.toml` buildCommand → `npm run build` | Direct-to-main (owner) — **UNVERIFIED, §6.2** |

**Process deviations to record (carry into ADR / next baseline):**
1. **CORS #16 landed without a formal pre-merge review session.** Post-merge verification
   (greps) substituted and passed, but the merge-readiness playbook was not run. The
   `server.py` collision with #15 resolved clean, but this broke the
   review-before-merge discipline used for #14/#15.
2. **`railway.toml` changed directly on main (`3f05ea9`)** — the "never silent infra
   change" file, edited outside review, simplifying the build command. Surfaced here, but
   it's unverified (§6.2) and may need reverting if the build fails on missing devDeps.
3. **Two direct-to-main hotfixes** (`9310dc3`, `3f05ea9`) bypassed the PR-squash norm —
   defensible as live-deploy unblocks, recorded as deviation.

**Lineage notes:**
- The `packageManager` fix CONVERGED: owner fixed it on GitHub (`9310dc3`) and identically
  in the terminal (`d55516d`); git deduplicated the terminal copy on `pull --rebase`
  (`warning: skipped previously applied commit`). Benign — both agreed. Local ended clean
  at `3f05ea9`, the terminal commit absent because its content was already upstream.
- All this session's Codex branches forked from pre-current bases (Luma forked pre-#11,
  Mongo forked pre-#14) — the **forked-base trap** appeared on both reviews and was caught
  each time by byte-comparing the merge-tree net-effect against the branch's own
  merge-base diff. This is now a standing review step (§12).

### 6.12 Uncommitted in the IMG working tree (carry / resolve)

`git status --short` shows three untracked files (NOT committed this session):
- `.automate-dev/reports/2026-06-08T05-25-36Z-mongo-merge-readiness.md` — the **Mongo #15
  review report**. SHOULD be committed (audit trail for the #15 merge, matching the Luma
  report pattern). Commit in isolation.
- `docs/2026-06-07T16-00-00-luma-merge-readiness-prompt.md` — Luma review prompt doc.
  Commit or clean up (owner's call).
- `docs/2026-06-07T16-45-00-luma-report-addendum-and-commands.md` — orchestrator-produced
  addendum/commands file. Commit or clean up.

Don't `git add -A` — stage by path, commit per concern.

---

## 7. Operating conventions

- Production-ready, complete code. No placeholders, stubs, or truncation.
- Preserve existing functionality. No breaking changes without approval.
- Files not copy-paste (mobile Claude corrupts unicode).
- Work reports: ISO 8601 datetime-prefixed Markdown.
- Multi-step builds: `automate-dev`, one task at a time. `/automate-dev` leads line one;
  explicit per-sub-task completion gates; file approval option 1 (file-by-file).
- **Git diff is truth, not Claude Code's task checkboxes.** "Committed locally" ≠ "on main".
  Always verify `git diff --stat origin/main HEAD`.
- Verify by running. **Green build ≠ renders** (the entire §6.2 thread is this lesson).
- `from __future__ import annotations` must NOT appear in `security/rate_limit.py` or any
  module used as a FastAPI class-instance `Depends()` — silent HTTP 422. (Pre-existing in
  `db.py` is harmless — `db.py` is not a Depends() callable.)
- Test harness: `mongomock_motor` + litellm stub + `get_limiter().reset()`. A `git worktree`
  lacks the untracked `backend/.venv` — run worktree tests with the MAIN checkout's venv
  interpreter (`~/kingdom/projects/illuminate-my-gallery/backend/.venv/bin/python`).

### Key git/merge lessons (codified)

- **Squash-merge discipline (§7 ADR):** squash severs ancestry; `--ff-only` refusing after
  = diverged, diagnose never force; delete source branch at squash; never reuse a
  squash-merged branch; never local-merge a non-ancestor.
- **Forked-base trap (seen on BOTH Luma and Mongo):** a two-dot `base..branch` diff
  overstates a branch that forked before earlier work landed (shows phantom "reversions").
  Derive the TRUE net effect via `git merge-tree --write-tree` and byte-compare suspected
  duplicate files (`git show A:path | sha256sum` vs `B:path`). Report real net-new only.
- **Rebase, don't merge, to land a local commit on a moved origin** — and a redundant local
  commit is auto-deduplicated by `pull --rebase` (`skipped previously applied commit`),
  which is benign, not an error.
- **Pin review base to a SHA, never a branch name** — origin/main moved twice mid-session
  under our feet; the SHA pin caught it both times.
- **Never `git checkout --theirs .`** on a 3-way merge.
- **JSON hand-edits corrupt easily** — removing a last-property field leaves a trailing
  comma / unbalanced braces. Use a JSON parser to rewrite (`json.load` → `pop` →
  `json.dump`), then `python3 -c "import json; json.load(...)"` to validate and `git diff`
  to confirm a surgical change before committing. (This session: a hand-edit silently
  corrupted `package.json` in a buffer; the file on disk was never saved — confirmed by
  empty `git diff` + `grep` still finding the field. Always verify on-disk state, not the
  buffer.)
- **PR "Squash and merge" is two clicks** — button → message editor → Confirm button.
- **Don't paste a shell prompt line** (`techcorp2024@penguin:...$`) into the terminal as a
  command — it splits the command sequence (caused a confusing half-run this run).

## 8. Verify-live commands

```bash
# Kingdom platform
cd ~/kingdom && git log --oneline -3 && git status --short
# expect tip: 2dd2f34 ; working tree clean
uv run pytest -q                          # expect: 11 passed

# Active project — every session start
cd ~/kingdom/projects/illuminate-my-gallery
git pull --ff-only origin main
git log --oneline -5                      # expect tip: 3f05ea9
git status --short                        # expect: 3 untracked docs (§6.12), else clean
grep -c packageManager frontend/package.json   # expect: 0
cat frontend/railway.toml                  # confirm buildCommand (currently bare `npm run build`)
npm run build --prefix frontend           # local build sanity (expect green)
cd backend && JWT_SECRET=x CLIENT_SESSION_SECRET=y CLOUDFLARE_WORKER_SHARED_SECRET=z \
  ./.venv/bin/python -m pytest -q
# expect: 89 passed (84 baseline + 5 Mongo test_db_config)
```

## 9. Things NOT to do

- Don't pin a second Context7 MCP server.
- Don't commit secrets or `.env` files.
- Don't silently change `railway.toml` — flag it; infra team owns provisioning. (Two direct
  edits happened this session — recorded as deviations, §6.11.)
- Don't stream image bytes through the backend. Ever. No sync derivatives. No
  `R2_BUCKET_PUBLIC`.
- Don't force-push. If `--ff-only` refuses: STOP and diagnose (rebase clean divergences).
- Don't reuse a branch after its earlier state was squash-merged; don't local-merge a
  non-ancestor.
- Don't assume "committed locally" = "on main"; don't assume a two-dot diff answers "does
  it merge" (`merge-tree`); don't assume green build = renders.
- Don't `git add -A` — stage by path, commit per concern.
- Don't hand-edit JSON brace-by-brace — use a parser + validate.
- Don't run stateful shell commands as one-off CC Bash calls (effects evaporate).
- Don't launch `claude` from `~/kingdom` for IMG work — launch from the project dir.
- Don't `/compact` a high-context session — commit + `/clear` + reload.
- Don't add `from __future__ import annotations` to `security/rate_limit.py`.
- Don't remove the manual Railway `DB_NAME` until §6.2 is closed (harmless meanwhile).

## 10. Roadmap

1. ✅ Task 1 design-system alignment — on `main`
2. **Task 2 — IN PROGRESS**
   - ✅ Priority 1 — structural safety audit
   - ✅ Priority 2 — auth foundation
   - ✅ Priority 3 — storage foundation — on `main`
   - → **Priority 4 — gallery delivery (confirm Cloudflare Worker first)**
3. **★ FIRST NEXT SESSION: verify the frontend redeploy (§6.2)** — build green?, site
   renders?, `OPTIONS /api/luma/chat` preflight 200/204? Close "builds but not viewable"
   or revert the `railway.toml` build command.
4. Commit the Mongo #15 review report + resolve the 2 other untracked docs (§6.12).
5. Remove the manual Railway `DB_NAME` stopgap (after #3 is clean).
6. Dependabot (2 critical, 5 high) — own deliberate pass.
7. Task 1 Phase 3 page migration — after Task 2 stable.
8. Kingdom platform Phase 3+: remaining entities via vertical-slice.

## 11. Key file index

| Path | What |
|---|---|
| `~/kingdom/CLAUDE.md` | Kingdom conventions incl. git hygiene |
| `~/kingdom/scripts/bootstrap/kingdom-start.sh` | `kstart` launcher |
| `~/kingdom/.claude/skills/` | Vendored skill suite + automate-dev overlay (`3f6a387`) |
| `~/kingdom/projects/illuminate-my-gallery/FIRST-SESSION.md` | IMG cold-start |
| `frontend/railway.toml` | Frontend deploy config (build/start commands) — §6.2 |
| `frontend/package.json` | packageManager field removed (`9310dc3`) |
| `~/.ssh/id_ed25519` | SSH key (passphrase) |
| `~/kingdom/.env` | Kingdom secrets (gitignored) |

## 12. Merge-readiness playbook — key non-obvious rules (carried)

Reusable for any incoming Codex branch. Phase 1 Analyse + Phase 3 Review only; halt at
go/no-go gate; merge only on explicit approval. **#16 skipped this — don't skip it again.**

- **Base = the merge target pinned to its SHA**, not `main` by name (origin moved twice
  this session). Re-pin if the base moved + record the re-pin reasoning (merge-base
  unchanged = safe).
- **Confirm the commit set** — `git log --oneline base..head`.
- **Merge dry-run** — `git merge-tree --write-tree base head`. Two-dot tip diff does NOT
  answer "does it merge."
- **Byte-compare suspected duplicates** (forked-base trap) before judging branch scope.
- **Disambiguate** multiple matching Codex branches — list, don't guess.
- **Build the integrated tree** (worktree + main's venv interpreter), not the head alone.
- **Guided 3-way resolution** — never `git checkout --theirs .`.
- **`automate-dev` Python scripts non-authoritative on JS** — trust manual review +
  integrated build + tests.
- **Cross-branch collision:** when ≥2 unmerged branches touch the same file, a clean
  verdict goes STALE the moment one lands — re-review the other against the new tip.

---

*Filename: kingdom-continuation-2026-06-10T13-00-00.md*
*Supersedes: kingdom-continuation-2026-06-07T17-00-00.md*
*IMG `main @ 3f05ea9` (clean, synced). Kingdom `main @ 2dd2f34` (clean).*
*Four PRs landed (#14/#15/#16 + 2 direct hotfixes). DB prod-VERIFIED.*
*★ OPEN: frontend redeploy after 3f05ea9 UNVERIFIED — §6.2 is the first next action.*
*Next update on session close: kingdom-continuation-YYYY-MM-DDTHH-MM-SS.md*
