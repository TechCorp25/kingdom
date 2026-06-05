# Kingdom — Continuation Baseline (Source of Truth)

> **Authoritative baseline as of 2026-06-05T07-00-00.**
> Supersedes all prior continuation baselines (most recently 2026-05-27T21-00-00).
> Where this conflicts with any older note or with Claude Code's compacted summaries, this wins.
> Run §8 verify commands before acting on anything time-sensitive — the IlluminateMyGallery
> repo is two-sided (Claude Code + Codex) and advances independently.
> Secrets are never in this document — values live in gitignored `.env` files only.
>
> **Session-close state:** branch B merged + pushed (`0083c5b`); both review reports
> committed + pushed (`0f61a90`). Current branch tip `storage/task-2-atlas-r2 @ 0f61a90`.
> Remaining close-out: commit this continuation doc.

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
- Load key: `eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519` — `kstart` does this
  (one passphrase prompt per shell; re-prompts after reboot or in a fresh terminal).
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
- **`automate-dev` skill:** primary mechanism for multi-step builds. `/automate-dev`,
  one task at a time. Committed in the kingdom repo at `.claude/skills/automate-dev/`
  AND resolves as a personal/user skill from the IlluminateMyGallery launch dir (it is
  discoverable regardless of which of the two repos you launch `claude` in — confirmed
  working this session). Claude Code discovers skills from `~/.claude/skills/`, the
  launch/project `.claude/skills/`, and subdirs of cwd — NOT from parent dirs.

## 4. Session startup

```bash
kstart                                        # postgres + ssh key + status (source it)
cd ~/kingdom/projects/illuminate-my-gallery   # LAUNCH FROM THE PROJECT DIR, not ~/kingdom
git pull --ff-only origin main                # (kingdom platform) — or fetch for IMG (§8)
claude                                        # then paste the task prompt
```

- **Launch `claude` from the project dir** (`~/kingdom/projects/illuminate-my-gallery`),
  not from `~/kingdom`. Each Claude Code Bash call starts in the launch dir, so git/npm
  target the IMG repo automatically. Launching from `~/kingdom` would target the kingdom
  platform repo (wrong repo) and force `git -C …` everywhere.
- **Stateful setup goes in the real terminal, never in the prompt** — `kstart`, `cd`,
  `ssh-add`, `export` run as one-off Claude Code Bash calls evaporate (ephemeral
  subprocess; a `cd` in one call does not persist to the next). The git **object store**
  IS shared between terminal and Claude Code, so a fetch/commit in either is visible to
  both; only in-process state doesn't cross.
- **`Please run /login` / 401 Invalid credentials** on launch = Claude Code login
  expired (common post-reboot/fresh terminal). Run `/login`, re-auth, re-submit the
  prompt. No need to re-run `kstart` or relaunch.

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
- **Active branch:** `storage/task-2-atlas-r2` (MongoDB Atlas + R2 + Auth + now the
  Codex design-system UI refresh — see §6.11). Pushed to origin and advancing.
- **Stack:** FastAPI backend (root `/backend`) + Vite / React 19 + Tailwind + shadcn/ui
  (root `/frontend`, publish `build/`). **Railway** hosting. **MongoDB Atlas + Cloudflare
  R2** storage. Cloudflare Worker for CDN delivery.
- **TWO-SIDED REPO:** Claude Code + Codex. Codex pushes `codex/...` branches. Fetch every
  session; `git pull --ff-only` / `git merge --ff-only` only; never force-push. A pruned
  `origin/conflict_230526_1727` branch was observed this session — residue of an earlier
  Codex divergence reconciliation; expect occasional sibling/auto-suffixed Codex branches.

---

### 6.1 Done ✓

- CRA → Vite migration, merged. Backend hardening (lazy DB, lifespan, CORS, Luma
  vendor-neutralisation, requirements split prod/dev).
- **Task 1 Phase 1 + Phase 2 — design-system alignment:** tokens + component primitives.
- **Priority 1 (structural safety) + Priority 2 (auth foundation):** complete per prior
  memory (commits referenced as `c43e152` P1; `201df05`, `c847870` P2). Verify these
  against the current branch history on resume — the branch has advanced via Codex UI
  merges since those were recorded (see §6.11), so do not assume the tip lineage.
- **Codex design-system UI refresh merged into `storage/task-2-atlas-r2` this session
  (§6.11):** branch A fast-forwarded; branch B landed via guided 3-way merge.

### 6.2 Known open problem

**"Builds but not currently viewable"** (carried forward; CORS / Vite `allowedHosts` /
R2 asset serving). The UI merges this session touched `vite.config.js` (added a PR-12
host to dev-server `allowedHosts`) and the app-wide base CSS / ThemeContext — re-verify
whether the deployed frontend now renders before assuming a fresh bug. Build is green
(2960 modules) but green build ≠ renders.

### 6.3 Application and scale

High-resolution **burst-access gallery platform**. Defining load case: school/childcare
gallery release — hundreds of parents opening one gallery in 30–60 min; ~75 GB optimised
media transfer in 30 min; cannot touch the Railway backend.

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
| Monthly R2 growth | 100–850 GB; 12-month 1.2–10 TB |

### 6.4 Image pipeline (unchanged)

Three variants per original, **no watermarking**: `thumb-v{n}.webp` (100–250 KB) and
`preview-v{n}.webp` (2–5 MB) in `illuminate-prod-derivatives` (Worker+CDN);
`original.jpg` (25–40 MB) in `illuminate-prod-originals` (backend 60s presigned URL,
paid download only). Versioned keys `prod/galleries/{gallery_id}/assets/{asset_id}/…`.
Both buckets private; no public R2, no `r2.dev`. `R2_BUCKET_PUBLIC` is retired. Upload
direct-to-R2 via presigned PUT; derivatives async (Pillow), never in the request cycle.

### 6.5 CDN delivery — Cloudflare Worker-gated (unchanged)

Both buckets private. Thumbs/previews served via a Cloudflare Worker on
`media.illuminatestudios.com.au` using the Worker R2 binding. Backend issues a 4-hour
gallery media JWT (HMAC-SHA256, `CLOUDFLARE_WORKER_SHARED_SECRET`) as an HttpOnly cookie;
Worker validates signature + expiry + gallery_id-in-path, returns
`Cache-Control: public, max-age=31536000, immutable`; edge caches thereafter. Revocation:
stop issuing JWTs (≤4h expiry) + Cloudflare Cache Purge API for immediate takedown.
Worker is a separate Cloudflare deployment (not Railway); flag to owner if not yet
deployed — Priority 4 gallery delivery can't be verified without it.

### 6.6 Image protection — client-side, no watermarking (unchanged)

Non-admin only; admin exempt. Download blocker (draggable=false, pointer-events overlay),
context-menu disable, long-press/touch-callout disable (CSS, iOS+Android), desktop
screenshot opacity flash. iOS hardware screenshot is an undetectable, documented gap.

### 6.7 Auth and permissions (unchanged)

Roles: `owner` (bootstrap) / `admin` (owner invite) / `editor` (owner invite) / `client`
(system on gallery token claim). No self-registration; role immutable by holder; only
owner assigns roles. Admin: email+password, JWT 8h, refresh 7d bcrypt rotated. Client:
password (30-day rolling) or magic link (15-min single-use SHA-256). All tokens hashed at
rest. Backend enforces every admin/client route server-side; Luma does not decide auth.

### 6.8 Selections and download authorization (unchanged)

Client selects → `gallery_selections` (pending) → admin approves →
`download_authorizations` (limit 3) → download validates + atomic increment → 60s
presigned URL for original → 302 redirect. No bytes through backend.
New Task-2 collections: `gallery_assets`, `gallery_selections`, `download_authorizations`,
`gallery_tokens`, `magic_link_tokens`, `staff_invites`, `refresh_tokens`.

### 6.9 Task 2 / Priority 3 — in-flight (carried from memory; VERIFY on resume)

The branch state has moved since these were recorded (it has been pushed and advanced via
Codex UI merges), so treat the following as open items to confirm against the current
branch, not as settled:

- **Priority 3 — storage foundation** (R2 adapter, `gallery_assets`, direct-to-R2 upload
  pipeline, async derivatives via Pillow): sub-tasks 4 and 5 reported incomplete.
- **Railway derivative worker:** service `illuminate-derivative-worker`
  (ID `95c0e2a5-3536-45a1-b629-5cf5fdd8969d`) provisioned against the staging branch by
  the Railway infra team. Separate worker process (not in-process `BackgroundTasks`),
  bounded internal concurrency, atomic MongoDB job-claim pattern.
- **Open infra dependencies to confirm with the Railway infra team:**
  1. **Module path mismatch** — staged service uses `python -m app.worker.derivative_worker`
     but built code landed at `python -m derivative_worker`. Reconcile.
  2. **`MONGODB_URI → MONGO_URL` mapping** — verify.
  3. **Worker memory ≥ 2 GB** — required for concurrent Canon original decodes at
     concurrency 4. Confirm provisioned limit.
  4. **R2 CORS on the originals bucket** — required for browser-direct upload and the
     Priority 3 end-to-end staging exit gate.
- Architectural decisions standing: unified asset route prefix `/api/galleries/{id}/…`
  with `require_staff`; separate Railway worker over in-process tasks; Sub-task 6 = Option 1
  (full pipeline integration, not display-only status panel).

### 6.10 Authoritative docs in repo

| Path | What |
|---|---|
| `test_reports/full_scale_infra_assessment_2026-05-27.md` | Storage/DB plan of record |
| `.automate-dev/DECISION-RECORD.md` | Living ADR |
| `.automate-dev/reports/2026-06-02T06-10-00-ui-merge-readiness.md` | **Pass 1 — branch A review** |
| `.automate-dev/reports/2026-06-05T06-34-11Z-ui-merge-readiness-passB.md` | **Pass 2 — branch B review** |
| `frontend/docs/design-system-audit-workplan.md` | Design-system plan |
| `FIRST-SESSION.md` | Cold-start brief |

> Both review reports are committed to `storage/task-2-atlas-r2` (commit `0f61a90`,
> "docs(automate-dev): add UI merge-readiness reports for branch A and B"). They are the
> audit trail for the A and B merges.

### 6.11 ★ Codex UI/design-system branch merges — this session (VERIFIED)

Two sibling Codex branches, both forked from the same base `13821ae`
(`origin/storage/task-2-atlas-r2` at the start of pass 1). **B is NOT stacked on A.**

| Branch | Ref | Commits | Tip |
|---|---|---|---|
| **A** | `codex/update-ui-to-match-design-system` | 2 — `2c6c20a` (remove binary assets), `4137cd7` (update vite.config.js) | `4137cd7` |
| **B** | `codex/update-ui-to-match-design-system-frt6hq` | 1 — `348f12a` (fix mobile sign-in + lights-out grain) | `348f12a` |

**What landed (A):** design-system refresh — light/dark `ThemeContext` + toggle, expanded
gold/sage/ink/bone token system, restyled header/footer/buttons, Cinzel/Inter fonts,
reworked grain overlay. UI-only; no backend/R2/Worker/env/JWT touched. The `vite.config.js`
edit added a PR-12 host to dev-server `allowedHosts` + an ESLint globals block.

**A merge (done):** pure fast-forward. Local was stale at `63ee7db` (behind origin
`13821ae`); `git merge --ff-only` advanced `63ee7db → 4137cd7`; outbound set confirmed ==
the 2 reviewed commits (`git log 13821ae..4137cd7` and
`origin/storage..storage` both showed exactly `2c6c20a`,`4137cd7`); `git push` advanced
**origin `13821ae → 4137cd7`**, no force. Scores: compatibility 100 / preservation 100 /
quality 88. `POST_A_BASE = 4137cd7`.

**B review (done, pass 2 against `POST_A_BASE = 4137cd7`):** mergeable via a deterministic
guided 3-way merge — **not** auto-clean, **not** blocked.
- 5 of B's 7 files byte-identical to post-A (B contains all of A's work).
- **2 conflicts: `Layout.jsx` + `index.css`** — mechanical, not semantic. In both spots
  B = A's content + the fix. **Resolve toward B.**
- **`vite.config.js`: no conflict** — a normal 3-way merge keeps A's version (PR-12 host
  retained). ⚠️ Do **NOT** `git checkout --theirs .` wholesale — that would drop A's
  PR-12 host. Take B only on the two conflicted files.
- B's net over A: +11/−5, 2 files — responsive mobile sign-in ("Sign in"/"Client portal",
  "Join"/"Become a client") + `body.lights-out-active .grain{display:none}`. This is the
  fix for pass-1 findings #1 (mobile login/toggle hidden) and #3 (always-mounted grain).
- Integrated A+B build (resolved tree, isolated worktree): **GREEN** — 2960 modules, 0
  lint errors (15 pre-existing warnings in untouched files). Scores: 100 / 100 / quality 92.

**B merge — guided 3-way recipe (when executed):**
```
git merge <B>           # normal 3-way; keeps A's vite.config.js automatically
# resolve the 2 conflicts by taking B's side on Layout.jsx and index.css only
# (NOT checkout --theirs . — that drops vite.config.js / PR-12 host)
npm run build --prefix frontend   # expect green, 2960 modules
git push origin storage/task-2-atlas-r2   # confirm exact steps at the gate first
```
**B MERGED TIP:** `0083c5b` — merge commit, parents `4137cd7` (A) + `348f12a` (B);
committed tree built green (2960 modules, 0 lint errors); pushed origin `4137cd7 → 0083c5b`,
no force. Both UI branches now integrated into `storage/task-2-atlas-r2`.

**Open non-blocking polish (carried, not addressed by A or B):** copy drift "Reserve a
date" vs "Book a session"; `#fdf8ee` hardcoded literals; `ThemeContext` not unified with
`next-themes`/sonner toasts; arbitrary Tailwind `px-[18px]` on login/register links.
Track separately.

---

## 7. Operating conventions

- Production-ready, complete code. No placeholders/stubs/truncation.
- Preserve existing functionality. No breaking changes without approval.
- Files, not copy-paste (mobile Claude corrupts unicode on paste).
- Task-context prompt framing, not persona/role.
- Work reports / continuation docs: ISO 8601 datetime-prefixed Markdown.
- Multi-step builds: `automate-dev`, one task at a time; `/automate-dev` leads line one;
  explicit per-sub-task completion gates; file approval option 1 (file-by-file).
- **Git diff is truth, not Claude Code's task checkboxes** — checkboxes lag file writes.
- Verify by running. Green build ≠ renders.
- **High-context boundary discipline:** commit at a clean boundary → `/clear` → re-enter
  from committed files + this continuation doc. **`/compact` is wrong for high-context
  work** (lossy summary is what file-based handoff replaces); `/compact` only before heavy
  mid-session read ops. Security-critical / branch-merge work should not push past
  ~70–80% context window.

## 8. Verify-live commands

```bash
# Kingdom platform
cd ~/kingdom
git log --oneline -3 && git status --short
uv run pytest -q                          # expect: 11 passed
uv run alembic current                    # expect: 0001_initial (head)

# Active project — IlluminateMyGallery
cd ~/kingdom/projects/illuminate-my-gallery
git fetch origin --prune
git rev-parse origin/storage/task-2-atlas-r2     # A → 4137cd7; B merge → 0083c5b; +reports → 0f61a90 (current tip)
git log --oneline -5 storage/task-2-atlas-r2
git status                                       # expect clean (only untracked report dir until committed)
git rev-parse origin/codex/update-ui-to-match-design-system-frt6hq   # 348f12a if B unmerged/unchanged
npm run build --prefix frontend                  # expect green, ~2960 modules
```

## 9. Things NOT to do

- Don't pin a second Context7 MCP server.
- Don't commit secrets or `.env`.
- Don't silently change `railway.toml` / Railway service config — flag it.
- Don't stream image bytes through the backend, ever. No synchronous derivative
  generation. No on-the-fly watermarking. No `R2_BUCKET_PUBLIC`.
- Don't force-push; `--ff-only` / guided 3-way only on the two-sided repo. If a pull
  refuses fast-forward: STOP and reconcile.
- Don't run stateful shell commands as one-off Claude Code Bash calls (effects evaporate).
- Don't launch `claude` from `~/kingdom` for IMG work — launch from the project dir.
- Don't `/compact` a high-context session — commit + `/clear` + reload instead.
- **Don't trust `automate-dev`'s Python scripts on JS branches.** `code_reviewer.py` /
  `fix_validator.py` are Python-oriented; their `breaking=False` / `preserved=True` are
  **non-authoritative for JS**, and the uniform `bare_except` flag + score-90 on every
  file is a script false-positive. The language-agnostic band-aid scan is the only
  meaningful signal. Rely on **manual review + the integrated build** for JS verdicts.
- **Don't judge a non-`main` merge against `main`, and don't judge sibling branches in
  isolation.** Pin the base to the actual **post-merge tip SHA** (not a branch name) when
  it's local-only; build the **integrated tree**, not the head alone, when branches are
  siblings touching shared files. (This session: A vs main would have been the wrong
  check; B vs pre-A base would have shown a false "clean".)
- **Don't resolve a B-type merge with `git checkout --theirs .`** — a normal 3-way `git
  merge` keeps A's `vite.config.js` (PR-12 host); wholesale-theirs drops it.

## 10. Roadmap

**Immediate (IlluminateMyGallery):**
1. ✅ Branch A merged + pushed (`4137cd7`); ✅ branch B merged + pushed (`0083c5b`).
2. ✅ Both review reports committed + pushed (`0f61a90`). B merged tip recorded (§6.11).
3. Resolve Priority 3 / infra open items (§6.9): module path mismatch, MONGO_URL mapping,
   worker memory ≥2 GB, R2 CORS on originals.
4. Complete Priority 3 sub-tasks 4 & 5; verify P1/P2 landing against current branch.
5. Resolve "builds-but-not-viewable" (re-check after the UI/vite changes).
6. Confirm Cloudflare Worker deployment before Priority 4 gallery delivery.
7. Non-blocking UI polish (§6.11 carried items).
8. **Triage GitHub Dependabot alert — 9 vulnerabilities (2 critical, 5 high, 1 moderate,
   1 low)** on the default branch. Pre-existing, unrelated to the UI merges, but "2
   critical" on a repo about to carry auth + R2 storage warrants its own deliberate pass.
9. **New Codex branch `codex/run-assessment-for-luma-booking-agent-failure`** appeared this
   session — Luma booking-agent work (Priority 4). Likely next-session target; apply the
   same merge-readiness pattern used for A/B (pin base to the live tip, build integrated,
   gate before merge).

**Kingdom platform Phase 3+:** remaining entities via vertical-slice; expand MCP surface.

## 11. Key file index

| Path | What |
|---|---|
| `~/kingdom/CLAUDE.md` | Kingdom conventions (committed) |
| `~/kingdom/docs/runbooks/2026-05-24T08-00-00-kingdom-runbook.md` | Ops runbook |
| `~/kingdom/scripts/bootstrap/kingdom-start.sh` | `kstart` launcher |
| `~/kingdom/projects/illuminate-my-gallery/FIRST-SESSION.md` | IMG cold-start |
| `.automate-dev/reports/2026-06-02T06-10-00-ui-merge-readiness.md` | Pass 1 (A) report |
| `.automate-dev/reports/2026-06-05T06-34-11Z-ui-merge-readiness-passB.md` | Pass 2 (B) report |
| `~/.ssh/id_ed25519` | Account SSH key (passphrase) |
| `~/kingdom/.env` | Kingdom secrets (gitignored) |

---
## 12. ★ Kingdom-repo hygiene — UNRESOLVED, triage FIRST next session

Surfaced at this session's close via `git status` in `~/kingdom` (NOT committed — the
continuation doc was committed in isolation as `549ce31`, deliberately leaving the
following untouched). This is the "parallel processes cause divergence" hazard showing
up in the **kingdom platform repo's** own working tree. Do NOT blanket `git add -A` —
triage each:

1. **`automate-dev` skill modified + a large untracked skill suite landed.**
   - Modified (uncommitted): `automate-dev/SKILL.md` + `references/{agents,quality-gates,
     token-budgeting,workflow-phases}.md` + `scripts/token_budget_monitor.py`.
   - Untracked inside automate-dev: `.claude-plugin/`, `agent-teams/`, nested `skills/`,
     `commands/team-*.md` (×7), `references/agent-teams-integration.md`, and an
     **`Archive.zip`** (a zip inside the skill dir — a smell; do NOT commit it).
   - ~45 NEW top-level skills under `.claude/skills/` (e.g. `backend-development`,
     `codebase-review`, `frontend-design`, `use-railway`, `use-zello`, `skill-creator`,
     `git-pr-workflows`, …). Contradicts the prior note that only `codebase-review` was
     selectively adopted from `claude-caliper` — a full suite is now present.
   - Implication: A and B were reviewed against a **modified** `automate-dev`, so its
     phase numbers / script names may differ from the last committed version. It worked,
     but the skill state is now untracked and unreproducible. Decide what to keep, delete
     `Archive.zip`, then commit deliberately.
   - Triage cmds: `git -C ~/kingdom diff --stat .claude/skills/automate-dev/`;
     `ls ~/kingdom/.claude/skills/`; `unzip -l …/automate-dev/Archive.zip` (list, don't extract).

2. **Three orphan continuation docs — uncommitted, NEWER than the 2026-05-27 base this
   doc was built on:** `docs/kingdom-continuation-2026-05-29T22-30-00.md`,
   `…2026-05-31T12-00-00.md`, `…2026-05-31T12-30-00.md`.
   - These likely hold the authoritative Priority-3 / Railway-worker state that §6.9 here
     only **reconstructed from memory**. Read the newest (`05-31T12-30-00`) and reconcile:
     if richer, it supersedes §6.9 and this doc should defer to it.
   - Decide: commit them (real state) or delete (abandoned drafts). Don't leave them
     orphaned a third session.

---

*End of baseline. Filename: kingdom-continuation-2026-06-05T16-40-00.md*
*Supersedes 2026-05-27T21-00-00 (and reconcile vs the three orphan docs in §12.2).*
*B merged tip `0083c5b`; branch tip `0f61a90`; this doc committed `549ce31`.*
*Next update on session close: kingdom-continuation-YYYY-MM-DDTHH-MM-SS.md*