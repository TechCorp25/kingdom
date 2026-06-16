---
title: "studio-suite — Continuation Baseline (Source of Truth)"
project: "studio-suite (Kingdom workspace)"
version: "2026-06-16T11-46-00"
owner: "TechCorp (solo developer, Melbourne AU)"
supersedes: "n/a — first studio-suite baseline"
status: "MID-TASK handoff — 01.0.1 (faithful landing) is the single open thread to resume first"
baseline_location: "~/kingdom/docs/studio-suite/"
note: "Secrets are never in this document — values live only in gitignored .env / Railway Variables."
---

# studio-suite — Continuation Baseline

Authoritative state as of 2026-06-16T11-46-00 (Melbourne). Where this conflicts with an older note,
this wins. This is a **mid-task** boundary: the orchestrator side is clean (every thread resolved or
parked), but build task **01.0.1 is in flight** — resume it first (see §6).

---

## 1. Identity & environment (inherited from kingdom)
- Owner: TechCorp, Melbourne AU. Machine: ChromeOS Crostini (Penguin), user `techcorp2024`.
- Workspace: `~/kingdom` (native btrfs); never `/mnt/chromeos/*` (FUSE).
- GitHub: account `TechCorp25`, org `techcorp-DevApps`. SSH key `~/.ssh/id_ed25519` (passphrase) →
  `Hi TechCorp25!`. SSH remotes only (HTTPS push is dead). git identity `techcorp2024` /
  `techcorp2024@gmail.com`.
- `kstart` loads postgres + ssh-add + status.

## 2. Project facts (LOCKED — §1 of the orchestrator prompt is filled)
| Field | Value |
|---|---|
| Repo | `git@github.com:techcorp-DevApps/studio-suite.git` · branch `main` |
| Slug / dir | `studio-suite` · `~/kingdom/projects/studio-suite/` |
| Product | Studio management system + client-portal companion. Public no-auth marketing front-end = entry point → auth-gated studio admin portal + individual auth-gated client portals. Burst-access high-res media in scope. |
| Topology | Monorepo: `backend/` · `web/` · `mobile/` (+ `shared/` if it emerges) |
| Stack (inherited from IMG — **NOT** the CLAUDE.md Flask/MongoEngine default) | Backend FastAPI + async Mongo (Motor); web Vite + React 19 + Tailwind + shadcn/ui (publish `build/`); mobile Expo + RN (EAS), **iOS + Android**; MongoDB Atlas (metadata only); Cloudflare R2 private buckets + Worker/CDN |
| Hosting | Railway (backend + web; derivative worker later). Mobile via EAS, not Railway. |
| "OTA" scope | Railway CD (prod from `main`) + PR previews + `.github/workflows/ci.yml` gate; EAS Workflows + EAS Update OTA for mobile |
| CC model | Opus 4.8 (re-select if Fable 5 is default & unavailable) |
| Mobile location | `~/kingdom/projects/studio-suite/mobile/` (ratified over `~/app-work/`) |
| Baseline location | `~/kingdom/docs/studio-suite/studio-suite-continuation-<ISO8601>.md` |

## 3. Git state
- **`main` tip = `42b1a0b`** "Update railway.toml" (owner, GitHub web — the EBUSY fix). Local = origin, clean.
- Lineage: `42b1a0b` → `e914bb4` (Foundation/backend web #1, squash of 01.0.0) → `bbfbb4a` (design-system + branding genesis) → `8f5c6d2` (pre-genesis remote tree).
- **Tree contents:** `design-system/` (canonical brand system: `components/`, `styles/`, `scripts/tokens.ts`, `data/illuminate-design-spec.json`, `assets/`, `branding/`), `backend/`, `web/`, `mobile/README.md`, infra (`backend/railway.toml`, `web/railway.toml`, `.github/workflows/ci.yml`).
- `.orchestrator/` (instructional prompts) and any local `.gitignore` edits — `.orchestrator/` is gitignored; nothing else uncommitted.

## 4. ★ TWO-SIDED REPO as of `e914bb4`
Codex can push to this remote. A deferred Codex branch exists:
`origin/codex/set-up-automated-git-workflows-with-codex` (commit `979e1da` — PR-review + preflight
workflows; **deferred by owner decision**, do NOT merge yet; revisit after Railway/landing stable).
**Discipline now mandatory every session:** `git fetch` + `git branch -a` at start; `git pull --ff-only`
only; never force-push; pin review bases to a SHA (origin/main can move from the owner's web edits or
Codex). Demonstrated this session: owner's `42b1a0b` appeared via fetch and was inspected before ff.

## 5. What is DONE (01.0.0 — on `main`)
- Monorepo foundation: backend (FastAPI + Motor, `/api/health` + `/api/health/db`, CORS with
  `CORS_ORIGINS` + `CORS_ORIGIN_REGEX`, R2 settings reserved by name), web (Vite/React 19/Tailwind/
  shadcn skeleton), `railway.toml` ×2, `.github/workflows/ci.yml` (backend ruff+pytest · web build).
- CI green on clean runners; squash-merged PR #1.
- **Railway hookup (partial):** web service `a3b1e95d-d9ea-41b9-92c8-15c7f71c2837` deploys from `main`;
  web URL `studio-suite-preview.up.railway.app` renders. EBUSY build failure **resolved** by `42b1a0b`
  (removed the redundant second `npm ci`; build is bare `npm run build`).

## 6. ★ OPEN THREAD — resume FIRST: task 01.0.1 (faithful public landing)
**Why:** 01.0.0 shipped a generic shadcn landing placeholder (orchestrator scoping error, owner-flagged).
The `design-system/` is the STRICT, pixel-faithful source of truth for every surface.
- **Prompt:** `.orchestrator/InstructionalPrompt_01.0.1.md` (ready). Branch off **current `main`
  (`42b1a0b`)**, NOT the stale `e914bb4` written in the prompt.
- **Scope:** port the design-system foundation into `web/` (self-host Cinzel/Cormorant/Inter/JetBrains
  Mono; port token CSS-vars + `.display`/`.serif-italic`/`.eyebrow`/`.gold-text`/`.hairline`/`--shadow-*`
  from `styles/styles.css`, additive to shadcn) → rebuild the **public landing only**, pixel-faithful to
  `design-system/components/landing.jsx` + `tokens.ts` + spec rules. Branch `feature/landing-from-design-system` → PR → CI → review → squash.
- **Ratified:** fonts SELF-HOSTED (no CDN); default theme LIGHT (toggle to dark); both themes must work.
- **DECISIVE GATE IS VISUAL:** green build proves nothing. Serve it; confirm it matches the design-system
  screenshots — Cormorant/Cinzel editorial hero (not Helvetica), gold-only accent, `#050505` not pure
  black, floating collage + SINCE MMXIV badge, 280+/12YR/40 stat row, Selected Frames — in light AND dark.
- **Deferred to their own later tasks:** booking calendar, pricing/packages, Client Portal, Studio Admin,
  live portfolio/R2 media pipeline. Sequencing agreed: each page/feature is its own scoped reviewable task.

## 7. Pending owner-side / infra items (not blocking 01.0.1)
- **Railway env/secrets** not yet fully set: `MONGODB_URI`, `MONGODB_DB_NAME`, CORS vars on the backend
  service; R2 creds deferred (no media pipeline yet). `CORS_ORIGIN_REGEX` recommended value:
  `^https://[a-z0-9-]+\.up\.railway\.app$` ; `CORS_ORIGINS` empty for now.
- **Backend service** `/api/health` close-out still owed (deploy + verify) whenever convenient.
- **PR preview + CORS preflight proof** (throwaway PR → preview frontend reaches preview backend, no
  failing `OPTIONS`) not yet done — can fold into the 01.0.1 PR.
- **EAS / mobile (01.1.0)** not started AND **its instructional prompt is NOT yet written** — to be
  authored when the web track is stable. (Earlier notes calling it "ready" were inaccurate; do not assume
  a `_01.1.0.md` exists on disk — verify before relying on it.)
- **Kingdom registration:** confirm studio-suite is registered as a kingdom tracked project; add it to
  the kingdom continuation baseline's tracked-projects table at next kingdom close.

## 8. Known fragilities (watch list)
- **Web build relies on Railpack auto-installing devDeps.** Bare `npm run build` works only while
  Railpack's `npm ci` includes devDeps (Vite is a devDependency). If a future web deploy dies with
  `vite: not found`, the cause is skipped devDeps — fix with `NPM_CONFIG_INCLUDE=dev` (or
  `RAILPACK_NO_CACHE=1`), NOT by re-adding a second `npm ci` (that caused the EBUSY on `.vite`).
- **`web/railway.toml` `preDeployCommand = "rm -rf node_modules/.vite"`** is still present and harmless,
  but redundant now — flag if it ever causes a deploy-phase error.
- **`from __future__ import annotations`** banned in any backend route/`Depends` module (HTTP 422).
- **Tailwind `shadow-[var(--x)]`** parses as a shadow COLOR → renders nothing; use a named `.shadow-*`.

## 9. Verify-live commands (run before acting on anything time-sensitive)
```bash
kstart
cd ~/kingdom/projects/studio-suite
git fetch origin
git branch -a                      # expect main + origin/main + the deferred codex/... branch
git log --oneline -3               # expect tip 42b1a0b
git status --short                 # expect clean (ignore .orchestrator/)
# web is live: studio-suite-preview.up.railway.app
```

## 10. Standing rules (do-not-lapse)
Git diff is truth, not CC checkboxes (`git diff --stat origin/main HEAD`). Green build ≠ renders ≠ OTA.
Files not copy-paste (mobile corrupts unicode). Stage by explicit path, never `git add -A`. `/clear` not
`/compact`. Security-critical work not past ~70–80% context. Design-system is STRICT law — pixel-faithful,
no interpretation. Additive-only to design tokens. Every irreversible step owner-gated (remote, push,
env/secrets, prod deploy, EAS publish, squash). Two-sided discipline (§4) in force.
**Every CC build prompt MUST open with `/automate-dev` as line one** — it activates the
build→review→simplify→test→fix loop; without it the loop collapses to a single pass. One task per prompt;
explicit per-sub-task completion gates; file approval option 1 (file-by-file). No prompt ships to CC
without `/automate-dev` at the top.

---
*First studio-suite baseline. Filename: studio-suite-continuation-2026-06-16T11-46-00.md*
*Commit in isolation to `~/kingdom/docs/studio-suite/` (stage ONLY this file; `git status` to verify).*
*Paired handoff: 2026-06-16T11-46-00-studio-suite-orchestrator-handoff.md*
