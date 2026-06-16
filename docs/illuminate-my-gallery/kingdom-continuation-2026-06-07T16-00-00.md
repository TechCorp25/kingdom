# Kingdom — Continuation Baseline (Source of Truth)

> **Authoritative baseline as of 2026-06-07T16-00-00.**
> Supersedes all prior continuation baselines (most recently 2026-06-07T14-30-00).
> Where this conflicts with any older note, Claude Code compacted summaries, or memory,
> this document wins on facts.
> Run §8 verify commands before acting on anything time-sensitive.
> Secrets are never in this document — values live in gitignored `.env` files only.
>
> **Session-close state:** Kingdom-repo hygiene (§12) FULLY RESOLVED and pushed —
> kingdom `main @ 043a7e0` (origin up to date, working tree clean). IMG `main @ d86d4b4`
> untouched this session. Next: Luma Codex branch merge-readiness (prompt drafted — §13).

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

- **Repo:** `git@github.com:TechCorp25/kingdom.git`, branch `main @ 043a7e0`.
  Clean, pushed, working tree clean.
- **Implemented:** `Project`, `Task`, `Memory` — full vertical slice, tested, clean.
- **Not yet built:** repositories, agents, skills, tools, runs, run_events, artifacts.
- **MCP tools (5):** `list_projects`, `get_project`, `search_memories`, `create_task`,
  `list_artifacts`.
- **Context7:** account connector. Do NOT add a second project-pinned one.
- **`automate-dev` skill:** primary mechanism for multi-step builds. One task at a time.
  Launch `claude` from the **project dir** (`~/kingdom/projects/illuminate-my-gallery`),
  not from `~/kingdom`, so git/npm target the IMG repo automatically.
  **NOW VENDORED + REPRODUCIBLE** — see §3.1.

### 3.1 ★ Skill suite — vendored this session (was §12 hygiene)

The full Claude Code skill suite is now **tracked** in the kingdom repo at
`.claude/skills/` (commit `3f6a387`). This is a **deliberate reversal** of the prior
baseline's "gitignore the bulk suite, don't vendor it" verdict (06-05 §12 / 06-07 §12
item 2).

**Rationale for the reversal (owner decision this session):** the suite is official
first-party skills (`use-expo`, `use-railway`, `frontend-design`, `codebase-review`,
`database-*`, `git-pr-workflows`, `ui-design`, `llm-application-dev`, etc.) plus the
full `automate-dev` agent-teams overlay. The overlay is the **primary in-use agent/skill
set**; the individual skills are first-party, area-specific (Expo, Railway, …) and
beneficial to retain for targeted use. Vendoring pins them as reproducible control-plane
state rather than leaving them untracked and unreproducible.

- **What was committed (`3f6a387`):** 447 files, +137,728 / −44. The 44 deletions are
  edits across the 6 pre-modified `automate-dev` files (SKILL.md + 4 references +
  `token_budget_monitor.py`); everything else is new (the overlay: `.claude-plugin/`,
  `agent-teams/`, 7 `commands/team-*.md`, `references/agent-teams-integration.md`,
  nested `skills/`; plus ~40 first-party top-level skills). 5.5M, text-only.
- **`Archive.zip` (95K install blob):** moved to `~/kingdom/artifacts/Archive.zip`
  (preserved, NOT deleted) and gitignored. The `.gitignore` now excludes both
  `artifacts/Archive.zip` and `.claude/skills/automate-dev/Archive.zip`.
- **Discovery note:** `use-expo` and `use-zello` are nested-skill bundles (orchestrator
  + sub-skills). There is name overlap between flat skills (`frontend-design`,
  `skill-creator`, `code-quality`) and bundle internals. If Claude Code ever reports a
  duplicate skill name, this overlap is the cause — not a corruption.
- **Discovery scope reminder:** `.claude/skills/` here is a **parent** of the IMG launch
  dir, so this suite is NOT auto-discovered during IMG sessions (CC discovers from
  `~/.claude/skills/`, launch-dir `.claude/skills/`, and cwd subdirs — never parent
  dirs). It IS discovered in kingdom-platform sessions launched from `~/kingdom`.

## 4. Session startup

```bash
kstart                                        # postgres + ssh key + status (source it)
cd ~/kingdom/projects/illuminate-my-gallery   # LAUNCH FROM PROJECT DIR, not ~/kingdom
git pull --ff-only origin main                # mandatory — two-sided repo
git log --oneline -3                          # confirm tip = d86d4b4
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
- **Active branch:** `main @ d86d4b4`. All task branches deleted. Untouched this session.
- **Stack:** FastAPI backend (`/backend`) + Vite / React 19 + Tailwind + shadcn/ui
  (`/frontend`, publish `build/`). **Railway** hosting. **MongoDB Atlas + Cloudflare R2**
  storage. Cloudflare Worker for CDN delivery.
- **TWO-SIDED REPO:** Claude Code + Codex. Codex pushes `codex/...` branches.
  `git pull --ff-only` every session. If it refuses: STOP and diagnose. Never force-push.
- **Merge discipline (§7 ADR):** PRs are **squash-merged** to main. A squash severs branch
  ancestry — `--ff-only` will refuse afterward. Land post-squash commits via cherry-pick
  onto `origin/main`, not by reusing the old branch. Delete source branch at squash time.
  **Never keep committing on a branch whose earlier state was squash-merged.**

---

### 6.1 Done ✓

- CRA → Vite migration, merged. Backend hardening.
- **Task 1 Phase 1 + Phase 2 — design-system alignment:** tokens + primitives.
- **Priority 1 — structural safety audit:** complete.
- **Priority 2 — auth foundation:** complete. Commits `201df05`, `c847870`, `e09b3a2`
  (squash-merged to main before the task-2 branch; on main's first-parent history).
- **Priority 3 — storage foundation:** complete. Squash-merged to main as
  `d86d4b4 Storage/task 2 atlas r2 (#11)` via PR #11.
- **Codex UI A/B merges** (design-system refresh + mobile sign-in + lights-out grain
  fix): complete, carried in the same squash.

  **What is on main @ `d86d4b4` (key new files):**
  - `backend/r2_storage.py` — dual-bucket R2 adapter (SigV4, presign PUT/GET,
    `object_exists`, worker byte methods)
  - `backend/gallery_assets.py` — asset domain, key builders, doc factory, `ensure_indexes`
  - `backend/derivative_jobs.py` — `derivative_jobs` queue
  - `backend/app/worker/derivative_worker.py` — separate Railway worker process
    (atomic claim, reaper for stalled claims, per-asset independence, Pillow pipeline)
  - `backend/routes/galleries_routes.py` — upload-intent, confirm, list `/assets` endpoints
  - `backend/tests/test_r2_storage.py` (10) + `test_priority3_storage.py` (29) — 84
    total backend tests passing, zero regression
  - `docs/2026-05-31T13-00-00-derivative-worker-railway-service-spec.md` — worker contract
  - `test_reports/2026-06-01T07-06-07-priority-3-storage-foundation-report.md` — P3 report
  - `.automate-dev/reports/` — both UI merge-readiness reports (pass A + pass B)
  - `frontend/src/context/ThemeContext.jsx`, updated `Layout.jsx`, `index.css`,
    `App.jsx` — Codex UI refresh

### 6.2 Known open problem

**"Builds but not viewable"** — CORS / Vite `allowedHosts` / R2 asset serving. The
`frontend/vite.config.js` now has 3-host `allowedHosts` (`preview-d482`, `pr-11`,
`pr-12`). Re-verify whether deployed frontend renders before assuming a new code bug.
Build is verified green (2960 modules) but green build ≠ renders.

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
Revocation: stop issuing JWTs (≤4h expiry) + Cloudflare Cache Purge API for immediate
takedown. Worker is a separate Cloudflare deployment; flag to owner if not yet
deployed — Priority 4 gallery delivery can't be verified without it.

### 6.6 Auth and permissions (unchanged)

Roles: `owner` (bootstrap) / `admin` (owner invite) / `editor` (owner invite) / `client`
(system on gallery token claim). No self-registration; role immutable by holder; only
owner assigns roles. Admin: email+password, JWT 8h, refresh 7d bcrypt rotated. Client:
password (30-day rolling) or magic link (15-min single-use SHA-256). All tokens hashed
at rest. Backend enforces every admin/client route server-side; Luma does not decide auth.
Legacy `"user"` role → `client` via `normalize_role()`.

### 6.7 Priority 3 staging checklist — infra-team items (CARRY FORWARD)

P3 **code is complete and on main**. The following are infra-provisioning confirmations
required before the staging exit gate — not code work:

1. **Railway worker module path** — service `illuminate-derivative-worker`
   (ID `95c0e2a5-3536-45a1-b629-5cf5fdd8969d`) entry point. The deploy contract
   (`docs/2026-05-31T13-00-00-derivative-worker-railway-service-spec.md`) is the
   source of truth — confirm the provisioned entry point matches.
2. **`MONGODB_URI → MONGO_URL` mapping** — confirm Railway env var name used by the
   worker service.
3. **Worker memory ≥ 2 GB** — required for concurrent Canon original decodes at
   concurrency 4.
4. **R2 CORS on originals bucket** — required for browser-direct presigned PUT upload
   (Priority 3 end-to-end staging exit gate).

These are the only items blocking a full end-to-end staging verification of P3.

### 6.8 Next: Priority 4 — Gallery delivery

Prerequisite: **confirm Cloudflare Worker deployment** at `media.illuminatestudios.com.au`
before starting Priority 4. Cannot verify gallery delivery without it.

Priority 4 build items:
- Cursor-paginated gallery asset API
  (`GET /api/galleries/{id}/assets?limit=80&cursor=…`)
- Gallery media JWT issued on gallery page load (sets `gallery_token` HttpOnly cookie)
- Gallery access token validation (14-day claim flow)
- Client selections endpoint (`gallery_selections`)
- Admin approval endpoint (`download_authorizations`)
- Download endpoint (302 redirect to 60s presigned URL — no bytes through backend)
- Client-side image protection layer (download blocker, context menu, long-press, screenshot)
- Virtualized gallery grid + lazy-loaded thumbnails (frontend)

### 6.9 Waiting Codex branches

| Branch | Status |
|---|---|
| `codex/run-assessment-for-luma-booking-agent-failure` | Luma booking-agent work (P4-adjacent). **NEXT TASK.** Merge-readiness prompt drafted this session (§13). Apply against `main @ d86d4b4` as base before merging. |
| `codex/update-ui-to-match-design-system` | Already merged (branch A). Prune when convenient. |
| `codex/update-ui-to-match-design-system-frt6hq` | Already merged (branch B). Prune when convenient. |

### 6.10 Authoritative docs in repo

| Path | What |
|---|---|
| `test_reports/full_scale_infra_assessment_2026-05-27.md` | Storage/DB plan of record |
| `test_reports/2026-06-01T07-06-07-priority-3-storage-foundation-report.md` | P3 completion report |
| `docs/2026-05-31T13-00-00-derivative-worker-railway-service-spec.md` | Worker deploy contract |
| `.automate-dev/DECISION-RECORD.md` | Living ADR (§9 = squash-merge hygiene) |
| `.automate-dev/reports/` | UI merge-readiness review reports (A + B) |
| `FIRST-SESSION.md` | Cold-start brief |

---

## 7. Operating conventions

- Production-ready, complete code. No placeholders, stubs, or truncation.
- Preserve existing functionality. No breaking changes without approval.
- Files not copy-paste (mobile Claude corrupts unicode).
- Work reports: ISO 8601 datetime-prefixed Markdown.
- Multi-step builds: `automate-dev`, one task at a time. `/automate-dev` leads line one;
  explicit per-sub-task completion gates; file approval option 1 (file-by-file).
- **Git diff is truth, not Claude Code's task checkboxes** — checkboxes lag file writes.
  "Committed locally" ≠ "on main". Always verify: `git diff --stat origin/main HEAD`.
- Verify by running. Green build ≠ renders.
- `from __future__ import annotations` must NOT appear in `security/rate_limit.py` or
  any module used as a FastAPI class-instance `Depends()` — causes HTTP 422 silently.
- Test harness: `mongomock_motor` + litellm stub + `get_limiter().reset()` — see
  `backend/tests/conftest.py`.

### Key git/merge lessons (codified)

- **Squash-merge discipline (§7 ADR):** PRs squash-merge. Squash severs ancestry.
  `--ff-only` refusing afterward = branch diverged from main — diagnose, never force.
  Cherry-pick onto `origin/main` is the landing method for post-squash commits.
  Delete source branch at squash; never reuse. Two-dot tip diff does NOT answer
  "does it merge" — run `git merge-tree` to find real conflicts before calling clean.
- **Trust git, not task trackers** — committed diff is the source of truth for what is done.
- **Merge-base matters** — a branch being a content-superset of main in a two-dot diff
  does not mean it merges cleanly. The three-way merge conflict depends on what *both
  sides changed since their common ancestor*, not just the tip states.
- **Never `git checkout --theirs .`** on a 3-way merge — a normal `git merge` keeps the
  base's version of non-conflicted files. Wholesale-theirs drops them.
- **PR "Squash and merge" is two clicks** — the button opens the message editor; a
  separate "Confirm squash and merge" button below it fires the actual merge.
- **Deliberate-commit discipline on a dirty tree** — never `git add -A` a working tree
  carrying mixed concerns. Stage by path, verify the staged set (`git diff --cached
  --stat`, grep for any blob), commit each concern in isolation. (This session: skills
  suite, orphan docs, and `.gitignore` handled as separate deliberate stages; an
  Archive.zip-staged guard ran before the suite commit.)

## 8. Verify-live commands

```bash
# Kingdom platform
cd ~/kingdom && git log --oneline -3 && git status --short
# expect tip: 043a7e0 ; working tree clean ; up to date with origin/main
uv run pytest -q                          # expect: 11 passed

# Active project — every session start
cd ~/kingdom/projects/illuminate-my-gallery
git pull --ff-only origin main
git log --oneline -3                      # expect: d86d4b4 at tip
git diff --stat origin/main HEAD          # expect: empty
git branch && git status                  # expect: main, clean
npm run build --prefix frontend           # expect: green, 2960 modules
cd backend && JWT_SECRET=x CLIENT_SESSION_SECRET=y CLOUDFLARE_WORKER_SHARED_SECRET=z \
  ./.venv/bin/python -m pytest -q
# expect: 84 passed (45 P2 + 10 r2_storage + 29 P3)
```

## 9. Things NOT to do

- Don't pin a second Context7 MCP server.
- Don't commit secrets or `.env` files.
- Don't silently change `railway.toml` — flag it; infra team owns provisioning.
- Don't stream image bytes through the backend. Ever.
- Don't generate derivatives synchronously — async worker only.
- Don't reference `R2_BUCKET_PUBLIC` — retired.
- Don't force-push. If `--ff-only` refuses: STOP and diagnose.
- Don't reuse a branch after its earlier state was squash-merged.
- Don't assume "committed locally" = "on main".
- Don't assume a two-dot tip diff answers "does it merge" — run `merge-tree`.
- Don't run stateful shell commands as one-off Claude Code Bash calls (effects evaporate).
- Don't launch `claude` from `~/kingdom` for IMG work — launch from the project dir.
- Don't `/compact` a high-context session — commit + `/clear` + reload instead.
- Don't add `from __future__ import annotations` to `security/rate_limit.py`.
- Don't `git add -A` a dirty kingdom tree — stage by path, verify, commit per concern.
- Don't re-commit `Archive.zip` into the tracked tree — it lives in `artifacts/`, gitignored.

## 10. Roadmap

1. ✅ Task 1 design-system alignment — on `main`
2. **Task 2 — IN PROGRESS**
   - ✅ Priority 1 — structural safety audit
   - ✅ Priority 2 — auth foundation
   - ✅ Priority 3 — storage foundation — `main @ d86d4b4`
   - → **Priority 4 — gallery delivery (confirm Cloudflare Worker first)**
3. ✅ Kingdom-repo hygiene — RESOLVED this session (`043a7e0`, pushed). Suite vendored.
4. **Luma Codex branch** (`codex/run-assessment-for-luma-booking-agent-failure`) — NEXT.
   Merge-readiness playbook against `main @ d86d4b4`. Prompt drafted (§13).
5. Dependabot (2 critical, 5 high on default branch) — own deliberate pass after Luma.
6. Resolve "builds-but-not-viewable" — re-verify after UI/vite changes on main.
7. Task 1 Phase 3 page migration — after Task 2 stable.

## 11. Key file index

| Path | What |
|---|---|
| `~/kingdom/CLAUDE.md` | Kingdom conventions incl. git hygiene |
| `~/kingdom/scripts/bootstrap/kingdom-start.sh` | `kstart` launcher |
| `~/kingdom/.claude/skills/` | Vendored skill suite + automate-dev overlay (`3f6a387`) |
| `~/kingdom/artifacts/Archive.zip` | Skill install blob (gitignored, preserved) |
| `~/kingdom/projects/illuminate-my-gallery/FIRST-SESSION.md` | IMG cold-start |
| `~/.ssh/id_ed25519` | SSH key (passphrase) |
| `~/kingdom/.env` | Kingdom secrets (gitignored) |

---

## 12. Kingdom-repo hygiene — ✅ RESOLVED this session

Prior baselines (06-05 §12, 06-07 §12) carried this as open. **Closed now.**

**Commits landed and pushed (kingdom `main`, `ce695be..043a7e0`):**

| SHA | What |
|---|---|
| `3f6a387` | Vendor full skill suite + automate-dev overlay (447 files, +137,728/−44, 5.5M text-only). Archive.zip moved to `artifacts/` + gitignored via the same commit's `.gitignore` change. |
| `043a7e0` | Commit three orphan continuation docs (05-29, 05-31×2) — recovers the lineage chain the 06-05 baseline forked past. |

**Resolution differs from the prior plan — recorded as a deliberate reversal (see §3.1):**
the prior verdict was "gitignore the bulk suite, don't vendor ~43 third-party skills."
The owner's standing intent is the opposite — the suite is first-party, area-specific,
and the automate-dev overlay is the primary in-use set — so it was vendored as
reproducible state. Only `Archive.zip` (binary blob) stays out of git.

**Correction to the 06-07 handoff assumption:** the handoff said the 06-07 baseline was
"carried untracked, commit at session close." In fact it was already committed and pushed
at `ce695be` (`docs: kingdom continuation baseline 2026-06-07T14-30-00`) before this
session. No action was needed; noted so the lineage is accurate.

**Nothing hygiene-related remains open in the kingdom repo.** Working tree clean.

---

## 13. ★ Luma Codex branch — merge-readiness (NEXT TASK; prompt drafted)

`codex/run-assessment-for-luma-booking-agent-failure` is waiting on origin. A
review-scoped `automate-dev` prompt has been drafted this session
(`2026-06-07T16-00-00-luma-merge-readiness-prompt.md`) to run in a fresh Claude Code
session launched from the IMG project dir.

**The prompt enforces the playbook (carried from the 06-05/06-07 handoffs):**
- Base = the merge target **pinned to its SHA** — `main @ d86d4b4`, not `main` by name.
- Disambiguate first — if more than one `codex/...*luma*` branch exists, list and STOP;
  don't guess.
- Confirm the commit set — `git log --oneline d86d4b4..<branch>`.
- Merge dry-run — `git merge-tree --write-tree d86d4b4 <branch>`. A two-dot tip diff does
  NOT answer "does it merge."
- Build the integrated tree (not the head alone) if it touches shared files.
- Phase 1 Analyse + Phase 3 Review only — halt at a go/no-go gate; **no merge without
  explicit approval**.
- `automate-dev`'s Python scripts are non-authoritative on JS branches — trust manual
  review + the integrated build. (Luma is likely Python/backend — note whether the diff
  is backend, frontend, or both, and weight script output accordingly.)
- This is a backend booking-agent branch; pay special attention to the §7 conventions:
  no `from __future__ import annotations` in FastAPI `Depends()` modules; Luma does not
  decide authorization (backend gates every write); idempotent booking creation; outbox
  email pattern.

**At merge time (only after go-gate approval):** PR squash-merge to `main`, delete source
branch at squash. Never local-`git merge` a non-ancestor branch.

---

## 14. ★ Merge-readiness playbook — key non-obvious rules (carried)

Reusable for any incoming Codex branch. Run Phase 1 Analyse + Phase 3 Review only;
halt at go/no-go gate; merge only on explicit approval.

- **Base = the merge target pinned to its SHA** (currently `main @ d86d4b4`).
- **Confirm the commit set** — `git log --oneline base..head`.
- **Run a merge dry-run** — `git merge-tree --write-tree base head`. Two-dot tip diff
  does NOT answer "does it merge."
- **Disambiguate before reviewing** — multiple matching Codex branches → list, don't guess.
- **Build the integrated tree**, not the head alone, when branches share files.
- **Guided 3-way resolution** — never `git checkout --theirs .`.
- **`automate-dev` Python scripts are non-authoritative on JS branches** — trust manual
  review + the integrated build.
- **PR "Squash and merge" is two clicks** — button → message editor → Confirm button.
  Watch for the purple "Merged" badge before any post-merge reconcile.

---

*Filename: kingdom-continuation-2026-06-07T16-00-00.md*
*Supersedes: kingdom-continuation-2026-06-07T14-30-00.md*
*Kingdom `main @ 043a7e0` (clean, pushed). IMG `main @ d86d4b4` (clean, untouched).*
*§12 hygiene RESOLVED — skill suite vendored, orphan docs recovered, all pushed.*
*Next: Luma Codex branch merge-readiness (§13). Then Dependabot, then Priority 4.*
*Next update on session close: kingdom-continuation-YYYY-MM-DDTHH-MM-SS.md*
