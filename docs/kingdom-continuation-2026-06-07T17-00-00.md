# Kingdom — Continuation Baseline (Source of Truth)

> **Authoritative baseline as of 2026-06-07T17-00-00.**
> Supersedes all prior continuation baselines (most recently 2026-06-07T16-00-00).
> Where this conflicts with any older note, Claude Code compacted summaries, or memory,
> this document wins on facts.
> Run §8 verify commands before acting on anything time-sensitive.
> Secrets are never in this document — values live in gitignored `.env` files only.
>
> **Session-close state:** Luma Codex branch reviewed **GO** (review-only, nothing merged).
> Merge-readiness report committed + pushed to IMG `main @ 0f04438` (rebased onto origin's
> docs commit `07ea282`, clean fast-forward push). **Luma branch landing DEFERRED** — not
> merged this session. Kingdom `main @ 043a7e0` untouched this session.

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
  Skill suite vendored + reproducible — see §3.1.

### 3.1 Skill suite — vendored (stable since 2026-06-07T16-00-00)

The full Claude Code skill suite is tracked in the kingdom repo at `.claude/skills/`
(commit `3f6a387`); orphan continuation docs recovered (`043a7e0`). `Archive.zip` lives
gitignored in `~/kingdom/artifacts/`. Discovery scope: `.claude/skills/` here is a
**parent** of the IMG launch dir, so the suite is NOT auto-discovered during IMG
sessions (CC discovers from `~/.claude/skills/`, launch-dir `.claude/skills/`, and cwd
subdirs — never parent dirs). It IS discovered in kingdom-platform sessions launched
from `~/kingdom`. (Full detail in the 06-07T16-00-00 baseline §3.1 if needed.)

## 4. Session startup

```bash
kstart                                        # postgres + ssh key + status (source it)
cd ~/kingdom/projects/illuminate-my-gallery   # LAUNCH FROM PROJECT DIR, not ~/kingdom
git pull --ff-only origin main                # mandatory — two-sided repo
git log --oneline -3                          # confirm tip = 0f04438
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
- **Active branch:** `main @ 0f04438`. Clean, in sync with origin.
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
- **Luma merge-readiness review — this session:** reviewed **GO** (see §6.11). Report
  committed + pushed to `main @ 0f04438`. Branch **not yet merged** (deferred).

  **What is on main @ `d86d4b4` / now `0f04438` (key files; report doc added this session):**
  - `backend/r2_storage.py` — dual-bucket R2 adapter (SigV4, presign PUT/GET,
    `object_exists`, worker byte methods)
  - `backend/gallery_assets.py` — asset domain, key builders, doc factory, `ensure_indexes`
  - `backend/derivative_jobs.py` — `derivative_jobs` queue
  - `backend/app/worker/derivative_worker.py` — separate Railway worker process
    (atomic claim, reaper for stalled claims, per-asset independence, Pillow pipeline)
  - `backend/routes/galleries_routes.py` — upload-intent, confirm, list `/assets` endpoints
  - `backend/luma/agent.py`, `tools.py`, `system.py`, `routes/luma_routes.py` — Luma
    booking agent (on main; the waiting Codex branch carries a small fallback fix — §6.11)
  - `backend/tests/test_r2_storage.py` (10) + `test_priority3_storage.py` (29) — 84
    total backend tests passing, zero regression
  - `docs/2026-05-31T13-00-00-derivative-worker-railway-service-spec.md` — worker contract
  - `test_reports/2026-06-01T07-06-07-priority-3-storage-foundation-report.md` — P3 report
  - `.automate-dev/reports/` — UI merge-readiness (A + B) + **Luma merge-readiness**
    (`2026-06-07T10-54-07Z-luma-merge-readiness.md`, committed `0f04438` this session)
  - `frontend/src/context/ThemeContext.jsx`, `Layout.jsx`, `index.css`, `App.jsx` — Codex UI

### 6.2 Known open problem

**"Builds but not viewable"** — CORS / Vite `allowedHosts` / R2 asset serving. The
`frontend/vite.config.js` on main has 3-host `allowedHosts` (`preview-d482`, `pr-11`,
`pr-12`). The waiting Luma branch adds `pr-14` (the lone merge conflict — §6.11).
Re-verify whether deployed frontend renders before assuming a new code bug. Build is
verified green (2960 modules) but green build ≠ renders.

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
| `codex/run-assessment-for-luma-booking-agent-failure` | **Reviewed GO this session (§6.11). NOT yet merged — landing deferred.** Tip `190a842`. Land via PR squash-merge to main (resolve the one `vite.config.js` conflict), delete at squash. |
| `codex/update-ui-to-match-design-system` | Already merged (branch A). Prune when convenient. |
| `codex/update-ui-to-match-design-system-frt6hq` | Already merged (branch B). Prune when convenient. |

### 6.10 Authoritative docs in repo

| Path | What |
|---|---|
| `test_reports/full_scale_infra_assessment_2026-05-27.md` | Storage/DB plan of record |
| `test_reports/2026-06-01T07-06-07-priority-3-storage-foundation-report.md` | P3 completion report |
| `docs/2026-05-31T13-00-00-derivative-worker-railway-service-spec.md` | Worker deploy contract |
| `.automate-dev/DECISION-RECORD.md` | Living ADR (§9 = squash-merge hygiene) |
| `.automate-dev/reports/2026-06-07T10-54-07Z-luma-merge-readiness.md` | **Luma review (GO) — this session** |
| `.automate-dev/reports/` | UI merge-readiness review reports (A + B) |
| `FIRST-SESSION.md` | Cold-start brief |

---

### 6.11 ★ Luma Codex branch — merge-readiness review (THIS SESSION, GO, NOT merged)

Review-scoped `automate-dev` pass (Phase 1 Analyse + Phase 3 Review only). Nothing
merged, pushed (except the report doc), or modified in the branch. Verdict **GO**;
landing **deferred** to a later session.

**Base re-pin (deliberate, recorded):** the prompt pinned base `d86d4b4`, but the
pre-flight gate correctly caught `origin/main` had advanced `d86d4b4 → 07ea282`
(docs-only: worker-spec doc + the luma prompt itself). Re-pinned to **`07ea282`** because
the **merge-base is `e09b3a2` either way** (the Luma branch forked before `d86d4b4`
landed), so the three-way merge result is identical; `07ea282` is the real current target.

**Branch facts (raw):**
- Branch `origin/codex/run-assessment-for-luma-booking-agent-failure`, tip `190a842`.
  Disambiguation: exactly one luma branch (expected name).
- Two-dot `$BASE..$BR` diff is misleading — looks like a P3-storage implementation, but
  **all P3 files are byte-identical to main** (this is #11's work, which the branch
  forked before; main squash-landed it independently). Verified identical, all 11 files.
- **Real net effect of the merge = 7 files / +81 −11**, a focused Luma fallback fix:
  - `backend/luma/agent.py` (+17) — wraps the LLM call in `chat_step` in try/except; on
    failure sets `state.status = "needs_human"`, emits `handoff_to_human`, breaks inside
    `chat_step` so session state is **persisted** (previously caught only at route level,
    which returned `state: None` and lost session context).
  - `backend/luma/system.py` (+4) — corrects the `create_booking` prompt to match the tool
    schema (the tool already declares args; main's prompt said "takes no arguments").
  - `backend/routes/luma_routes.py` (+8) — DRYs route-level fallback to reuse
    `LLM_FAILURE_REPLY` (backstop retained).
  - `backend/tests/test_priority2_auth.py` (+21) — new test
    `test_llm_failure_keeps_session_context`.
  - `frontend/src/components/LumaChat.jsx` (+4) — drops a genuinely-dead `MessageCircle`
    import + unused catch binding (lint).
  - `...luma-booking-agent-assessment.md` (+33) — doc only.
- **Merge dry-run:** CONFLICT in **one file only — `frontend/vite.config.js`** (Railway
  preview-host allowlist `pr-12` on main vs `pr-14` on branch + an added
  `import process from "node:process";`). **Trivial — union the hosts, keep the import.
  Do NOT `git checkout --theirs .`.**

**Convention findings (all PASS):**
- `from __future__ import annotations` — PASS. `security/rate_limit.py` correctly avoids
  it (carries a defensive comment documenting the 422 trap). The future-import appears in
  other modules but none are in this branch's net diff and none are class-instance
  `Depends()` callables.
- Secrets / `.env` / `railway.toml` — PASS, none touched.
- `R2_BUCKET_PUBLIC` / sync derivatives / image streaming — PASS (only hit is the prompt
  doc's own text; all storage code byte-identical to main).
- **Luma does NOT decide authorization — PASS.** `tool_create_booking` writes
  `status: "pending"` (hardcoded) + returns `pending_admin_approval`; price is
  server-side `pkg["base_price"]`; package identity from looked-up `pkg`; `user_id` from
  server-side email find-or-create. The model cannot create an approved booking — staff
  approval is the gate. Booking-logic block is byte-identical to main (unchanged by the
  branch).

**Data-source finding (reviewed, contained, recorded — NOT a blocker):**
`tool_create_booking` (agent.py:122) builds the record as `args.get(field) or
state.<field> or ""` — model args take precedence over session state for the **soft**
fields (client_name, phone, preferred_date/time, location, suburb, notes). **No
cross-check** against confirmed session values, so the `system.py` prompt change (which
now actively has the model supply args) could persist details that drift from what the
client confirmed. **Contained:** the authorization- and money-critical fields are
server-controlled regardless of args (`estimated_price = pkg["base_price"]`, package
identity from `pkg`, `status` hardcoded `pending`, `user_id` server-side). Staff approval
surfaces the details before confirmation. Logged as a data-quality hardening item
(cross-check args against session state, or drop args for fields already validated in
session) — adjacent to follow-up #1 below.

**Build + test (isolated worktree at branch tip `190a842`, main venv interpreter):**
**85 backend tests passed** (84 baseline + the 1 new fallback test), representative of
the merged backend (merged backend == branch backend; P3 identical). Frontend not built
(net frontend change is only `LumaChat.jsx` + the trivial `vite.config.js`; main's DS
work untouched by the branch); verified `MessageCircle` is a dead import.

**Three pre-existing non-blocking follow-ups (on main via #11, NOT introduced by this branch):**
1. `tool_create_booking` `insert_one` is **not idempotent** — a double tool-call →
   duplicate booking. (More exposed after the fallback change, though not caused by it.)
2. Admin notification email sent **directly in the agent path**, not via the outbox pattern.
3. `check_availability` returns a `hold_id` that is **never persisted** — non-functional hold.

**Landing path (owner's call, NOT done):** resolve the one `vite.config.js` conflict in
the PR (union hosts + keep import) → **squash-merge to main** → delete source branch at
squash. Never local-merge — the branch is a **non-ancestor** of main (§7 ADR).

**Note:** the CC session autonomously corrected its own `project_state.md` (P3 "not
started" → on main). The orchestrator-side baselines already had P3 correct on
`main @ d86d4b4` — no orchestrator-side drift; logged for lineage accuracy.

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
  `backend/tests/conftest.py`. A `git worktree` won't carry the untracked
  `backend/.venv`; run worktree tests with the main checkout's venv interpreter.

### Key git/merge lessons (codified)

- **Squash-merge discipline (§7 ADR):** PRs squash-merge. Squash severs ancestry.
  `--ff-only` refusing afterward = branch diverged from main — diagnose, never force.
  Delete source branch at squash; never reuse. Two-dot tip diff does NOT answer
  "does it merge" — run `git merge-tree` to find real conflicts before calling clean.
- **Two-dot diff hides forked-base reality** — this session, `$BASE..$BR` made the Luma
  branch look like a full P3 implementation; it's actually a content-duplicate of #11
  (byte-identical files) + a small real delta. Always verify net content (byte-compare
  suspected-duplicate files) before judging branch size.
- **Trust git, not task trackers** — committed diff is the source of truth.
- **Merge-base matters** — content-superset in a two-dot diff ≠ clean merge.
- **Never `git checkout --theirs .`** on a 3-way merge.
- **Rebase, don't merge, to land a local commit on a moved origin** — this session the
  report commit `bb35015` (on `d86d4b4`) diverged 1-and-1 from `origin/main @ 07ea282`
  (docs-only, no file overlap). `git pull --rebase origin main` replayed it cleanly to
  `0f04438` → fast-forward push. A plain `git pull` would have made a merge commit.
- **Pre-flight base-pin gate works** — pinning the review base to a SHA caught that
  `origin/main` had moved (`d86d4b4 → 07ea282`) since the prompt was authored; re-pin was
  a low-risk deliberate decision because the merge-base was unchanged.
- **PR "Squash and merge" is two clicks** — button → message editor → Confirm button.

## 8. Verify-live commands

```bash
# Kingdom platform
cd ~/kingdom && git log --oneline -3 && git status --short
# expect tip: 043a7e0 ; working tree clean ; up to date with origin/main
uv run pytest -q                          # expect: 11 passed

# Active project — every session start
cd ~/kingdom/projects/illuminate-my-gallery
git pull --ff-only origin main
git log --oneline -3                      # expect: 0f04438 at tip
git diff --stat origin/main HEAD          # expect: empty
git branch && git status                  # expect: main, clean (1 untracked prompt doc OK)
npm run build --prefix frontend           # expect: green, 2960 modules
cd backend && JWT_SECRET=x CLIENT_SESSION_SECRET=y CLOUDFLARE_WORKER_SHARED_SECRET=z \
  ./.venv/bin/python -m pytest -q
# expect: 84 passed on main (85 if the Luma branch has been landed)
```

## 9. Things NOT to do

- Don't pin a second Context7 MCP server.
- Don't commit secrets or `.env` files.
- Don't silently change `railway.toml` — flag it; infra team owns provisioning.
- Don't stream image bytes through the backend. Ever.
- Don't generate derivatives synchronously — async worker only.
- Don't reference `R2_BUCKET_PUBLIC` — retired.
- Don't force-push. If `--ff-only` refuses: STOP and diagnose (rebase if it's a clean
  divergence with no file overlap; never force).
- Don't reuse a branch after its earlier state was squash-merged.
- Don't local-merge the Luma branch — it's a non-ancestor; squash-merge via PR only.
- Don't assume "committed locally" = "on main".
- Don't assume a two-dot tip diff answers "does it merge" — run `merge-tree`.
- Don't run stateful shell commands as one-off Claude Code Bash calls (effects evaporate).
- Don't launch `claude` from `~/kingdom` for IMG work — launch from the project dir.
- Don't `/compact` a high-context session — commit + `/clear` + reload instead.
- Don't add `from __future__ import annotations` to `security/rate_limit.py`.
- Don't `git add -A` a dirty tree — stage by path, verify, commit per concern.
- Don't paste a shell prompt line (`techcorp2024@penguin:...$`) into the terminal as a
  command — it breaks the command sequence (happened this session; caused a confusing
  half-run before the rebase).

## 10. Roadmap

1. ✅ Task 1 design-system alignment — on `main`
2. **Task 2 — IN PROGRESS**
   - ✅ Priority 1 — structural safety audit
   - ✅ Priority 2 — auth foundation
   - ✅ Priority 3 — storage foundation — `main @ d86d4b4` (now `0f04438` with report doc)
   - → **Priority 4 — gallery delivery (confirm Cloudflare Worker first)**
3. **Land the Luma branch** — reviewed GO this session (§6.11); resolve the one
   `vite.config.js` conflict, PR squash-merge to main, delete at squash. THEN it's 85 tests.
4. Dependabot (2 critical, 5 high on default branch — re-confirmed in this session's push
   output) — own deliberate pass.
5. Resolve "builds-but-not-viewable" — re-verify after UI/vite changes on main.
6. Luma data-quality hardening (§6.11): cross-check `create_booking` args vs session
   state; + the three pre-existing follow-ups (idempotent `insert_one`, outbox email,
   persisted `hold_id`).
7. Task 1 Phase 3 page migration — after Task 2 stable.
8. Kingdom platform Phase 3+: remaining entities via vertical-slice; expand MCP surface.

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

## 12. Merge-readiness playbook — key non-obvious rules (carried)

Reusable for any incoming Codex branch. Run Phase 1 Analyse + Phase 3 Review only;
halt at go/no-go gate; merge only on explicit approval.

- **Base = the merge target pinned to its SHA**, not `main` by name (a later push can move
  the name — happened this session, `d86d4b4 → 07ea282`). Re-pin is fine when the
  merge-base is unchanged; record the re-pin in the report.
- **Confirm the commit set** — `git log --oneline base..head`.
- **Run a merge dry-run** — `git merge-tree --write-tree base head`. Two-dot tip diff
  does NOT answer "does it merge."
- **Byte-compare suspected-duplicate files** before judging branch size — a forked-base
  branch can look huge while being a content-duplicate of squash-landed work + a small delta.
- **Disambiguate before reviewing** — multiple matching Codex branches → list, don't guess.
- **Build the integrated tree**, not the head alone, when branches share files. A worktree
  lacks the untracked venv — run with the main checkout's interpreter.
- **Guided 3-way resolution** — never `git checkout --theirs .`.
- **`automate-dev` Python scripts are non-authoritative on JS branches** — trust manual
  review + the integrated build. (Luma was backend Python + a tiny JS lint — weight
  manual review + the 85-test run.)
- **PR "Squash and merge" is two clicks** — button → message editor → Confirm button.

---

*Filename: kingdom-continuation-2026-06-07T17-00-00.md*
*Supersedes: kingdom-continuation-2026-06-07T16-00-00.md*
*IMG `main @ 0f04438` (clean, pushed — Luma review report landed). Kingdom `main @ 043a7e0` (clean).*
*Luma Codex branch reviewed GO (§6.11); landing DEFERRED — not merged this session.*
*Next: land Luma branch (PR squash) → Dependabot pass → Priority 4 (confirm Worker first).*
*Next update on session close: kingdom-continuation-YYYY-MM-DDTHH-MM-SS.md*
