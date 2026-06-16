---
title: "studio-suite — Continuation Baseline (Source of Truth)"
project: "studio-suite (Kingdom workspace)"
version: "2026-06-16T14-32-00"
owner: "TechCorp (solo developer, Melbourne AU)"
supersedes: "studio-suite-continuation-2026-06-16T11-46-00.md"
status: "MID-TASK — resume 01.0.1 first; mobile architecture changed to native @is/tokens (Architecture B)"
baseline_location: "~/kingdom/docs/studio-suite/"
note: "Secrets never appear here — values live only in gitignored .env / Railway Variables / EAS."
---

# studio-suite — Continuation Baseline (supersedes 2026-06-16T11-46-00)

Authoritative state as of 2026-06-16T14-32-00 (Melbourne). This **supersedes** the T11-46-00 baseline,
which contained two errors now corrected here (see §0). Where anything conflicts, **this wins**.

---

## 0. ★ CORRECTIONS to the superseded T11-46-00 baseline (read first)
1. **01.1.0 prompt EXISTS.** The prior baseline §7 stated "01.1.0 not started AND its prompt is not yet
   written." That was FALSE — `InstructionalPrompt_01.1.0.md` was authored 2026-06-15 and is referenced
   across `SESSION_01.md`, `SESSION_01_ToDo.md` (§E), `SESSION_01_CC-Command-Sequence.md` (Phase 2), and
   `mobile/README.md`. The error came from asserting state without searching the connected repos. It is
   corrected here and the rule in §10 now makes that verification mandatory.
2. **Mobile architecture CHANGED — Architecture B ratified.** `SESSION_01.md §0.3` assumed mobile would
   replicate web via the **`use-dom` webview** strategy (Architecture A). That is now **SUPERSEDED.**
   Mobile is **native Expo/RN consuming a shared `@is/tokens` package** (Architecture B) — the path the
   design-system itself prescribes (`design-system/components/ds-handoff.jsx` ships `.native.tsx`
   ThemeProvider, `shadowToRN()`, `trackingToRN()`, `expo-font`, `expo-secure-store`). The existing
   01.1.0 prompt (shell + EAS OTA, defer replication) is therefore being **rewritten** to the native
   `@is/tokens` foundation (see §6).

## 1. Identity & environment (inherited from kingdom — verified)
- Owner: TechCorp, Melbourne AU. Machine: ChromeOS Crostini (Penguin), user `techcorp2024`.
- Workspace: `~/kingdom` (native btrfs); never `/mnt/chromeos/*` (FUSE).
- GitHub: account `TechCorp25`, org `techcorp-DevApps`. SSH key `~/.ssh/id_ed25519` (passphrase). SSH
  remotes only. git identity `techcorp2024` / `techcorp2024@gmail.com`. `kstart` = postgres + ssh-add + status.

## 2. Project facts (LOCKED)
| Field | Value |
|---|---|
| Repo | `git@github.com:techcorp-DevApps/studio-suite.git` · branch `main` |
| Slug / dir | `studio-suite` · `~/kingdom/projects/studio-suite/` |
| Product | Studio management system + client-portal companion. Public no-auth marketing front-end → auth-gated studio admin portal + individual auth-gated client portals. Burst-access high-res media in scope. |
| Topology | Monorepo: `backend/` · `web/` · `mobile/` · **`packages/tokens/` (`@is/tokens`, new — Architecture B)** |
| Stack (inherited from IMG — NOT the CLAUDE.md Flask default) | Backend FastAPI + Motor; web Vite + React 19 + Tailwind + shadcn; mobile **native Expo + RN (EAS), iOS + Android**; MongoDB Atlas (metadata); Cloudflare R2 private + Worker/CDN |
| Hosting | Railway (backend + web). Mobile via EAS, not Railway. |
| CC model | Opus 4.8 (re-select if Fable 5 is default & unavailable) |
| Mobile location | `~/kingdom/projects/studio-suite/mobile/` |
| Baseline location | `~/kingdom/docs/studio-suite/` |

## 3. Git state (verified via repo search 2026-06-16T14-32)
- **`main` tip = `42b1a0b`** "Update railway.toml" (owner GitHub-web edit — the EBUSY fix). Local = origin, clean.
- Lineage: `42b1a0b` → `e914bb4` (PR #1 squash, 01.0.0) → `bbfbb4a` (design-system + branding genesis) → `8f5c6d2`.
- Tree: `design-system/` (canonical), `backend/`, `web/`, `mobile/README.md` (reserved), infra (`backend/railway.toml`, `web/railway.toml`, `.github/workflows/ci.yml`). `.orchestrator/` gitignored.
- **Kingdom docs repo** (`git@github.com:TechCorp25/kingdom.git`): tip `a0a5894` — IMG baselines relocated to `docs/illuminate-my-gallery/`, studio-suite baseline + session-01 docs under `docs/studio-suite/`. Per-project subfoldering now in effect (resolves the old §7 collision question).

## 4. ★ TWO-SIDED REPO (studio-suite, as of `e914bb4`)
Codex can push. Deferred branch `origin/codex/set-up-automated-git-workflows-with-codex` (`979e1da` —
PR-review + preflight workflows; **do NOT merge yet**). Every session: `git fetch` + `git branch -a`;
`--ff-only` only; never force-push; pin bases to a SHA. Demonstrated this session: owner's `42b1a0b`
appeared via fetch and was inspected (`git show --stat`) before fast-forwarding.

## 5. What is DONE (01.0.0 — on `main`)
- Backend (FastAPI + Motor: `/api/health` + `/api/health/db`, CORS `CORS_ORIGINS` + `CORS_ORIGIN_REGEX`,
  R2 settings reserved by name), web (Vite/React 19/Tailwind/shadcn skeleton + a GENERIC placeholder
  landing — to be replaced by 01.0.1), `railway.toml` ×2, `.github/workflows/ci.yml`. CI green; PR #1 squashed.
- **Railway (partial):** web service `a3b1e95d-d9ea-41b9-92c8-15c7f71c2837` deploys from `main`; renders
  at `studio-suite-preview.up.railway.app`. EBUSY resolved by `42b1a0b` (build is bare `npm run build`).

## 6. ★ OPEN THREADS — order of work
**6a. RESUME FIRST — 01.0.1 (faithful public landing, REWRITTEN for Architecture B).**
- 01.0.0 shipped a generic placeholder (orchestrator scoping error, owner-flagged). `design-system/` is
  STRICT pixel-faithful law.
- **REWRITTEN scope:** stand up **`packages/tokens/` (`@is/tokens`)** per `ds-handoff.jsx` (exports:
  palette, themes, space, radius, type, shadow, motion, z, breakpoint, shadowToCSS, shadowToRN,
  themeToCSSVars, trackingToRN, useTheme, ThemeProvider [+ `.native`]) → **web consumes `@is/tokens`**
  (ThemeProvider, `@is/tokens/dist/css/index.css`) → build the **public landing only**, pixel-faithful to
  `design-system/components/landing.jsx`. Self-host fonts; default theme LIGHT; both themes work.
- **Adopting `@is/tokens` now (not inlining) eliminates web/mobile token divergence at the root** — chosen
  because doing it before web ships costs least; there is no shipped web app to migrate.
- **pnpm + Railway implication (OWNER-GATED INFRA):** `@is/tokens` is a workspace package; the repo moves
  to a pnpm workspace. Railway web build (`npm run build`) and the lockfile (`package-lock.json` →
  `pnpm-lock.yaml`) change. The rewritten prompt spells this out; the owner provisions the Railway build-command change.
- Branch `feature/landing-from-design-system` off **current `main` (`42b1a0b`)** → PR → CI → **VISUAL gate** → squash.
- **DECISIVE GATE = VISUAL:** serve it; confirm it matches the design-system (Cormorant/Cinzel hero, gold-only,
  `#050505` not black, collage + SINCE MMXIV, 280+/12YR/40, Selected Frames) in light AND dark. Green build proves nothing.

**6b. 01.1.0 (mobile foundation, REWRITTEN for Architecture B).** Native Expo/RN under `mobile/` consuming
the SAME `@is/tokens` (ThemeProvider.native, `expo-font` five families, `useColorScheme`, `react-native-svg`,
`expo-secure-store`) + the EAS/OTA pipeline scoping the prior draft did well (`eas.json` profiles, Update
channels, `.eas/workflows/{development,preview,production,hotfix}.yml`, CI mobile job, owner-run `eas init`→
`eas update` OTA proof). Ends at the DS 12-point checklist green (both apps themed, no flash, all fonts). No screens.

**6c. 01.1.1 (later).** First faithful NATIVE mobile screen, pixel-faithful, decisive visual gate on device/sim (light+dark).

**6d. Subsequent web surfaces**, each its own scoped reviewable task: Studio Admin portal, Client portal(s) + sign-in,
Investment/pricing, Experience, Journal, R2/Worker media pipeline.

## 7. Pending owner-side / infra (not blocking 01.0.1 build, but 01.0.1 PR needs the Railway change)
- **Railway web build command** must become pnpm-aware when `@is/tokens` lands (see §6a). Owner-gated.
- **Backend Railway env/secrets** not fully set: `MONGODB_URI`, `MONGODB_DB_NAME`, CORS vars; R2 deferred.
  Recommended `CORS_ORIGIN_REGEX` = `^https://[a-z0-9-]+\.up\.railway\.app$`; `CORS_ORIGINS` empty for now.
- **Backend `/api/health` close-out** (deploy + verify) owed.
- **PR-preview CORS-preflight proof** — can fold into the 01.0.1 PR.
- **EAS hookup (Phase 0c)** runs after 01.1.0 lands.
- **Kingdom tracked-project registration** for studio-suite — confirm + add to the kingdom baseline's table at next kingdom close.

## 8. Known fragilities (watch list)
- **Web build relies on Railpack auto-installing devDeps.** Bare `npm run build` works only while Railpack's
  install includes devDeps (Vite is a devDependency). If a web deploy dies `vite: not found`, the cause is
  skipped devDeps — fix with `NPM_CONFIG_INCLUDE=dev` / `RAILPACK_NO_CACHE=1`, NOT a second `npm ci` (that caused EBUSY).
  **NOTE:** moving to pnpm (§6a) changes this surface — re-verify the build command when `@is/tokens` lands.
- **`web/railway.toml` `preDeployCommand = "rm -rf node_modules/.vite"`** present, redundant, harmless — flag if it errors.
- **`from __future__ import annotations`** banned in any backend route/`Depends` module (HTTP 422).
- **Tailwind `shadow-[var(--x)]`** parses as a shadow COLOR → renders nothing; named `.shadow-*` only.

## 9. Verify-live commands (run before acting; ALSO see §10 search rule)
```bash
kstart
cd ~/kingdom/projects/studio-suite
git fetch origin
git branch -a                      # expect main + origin/main + deferred codex/... branch
git log --oneline -3               # expect tip 42b1a0b
git status --short                 # expect clean (ignore .orchestrator/)
# web live: studio-suite-preview.up.railway.app
```

## 10. ★ Standing rules (do-not-lapse)
- **★ NON-NEGOTIABLE — VERIFY AGAINST BOTH REPOS BEFORE ASSERTING STATE.** The orchestrator MUST use
  repo/project search to confirm any claim about git state, file existence, prompt contents, or task
  status against **both** the connected `studio-suite` and `kingdom` repos **before** stating it or
  writing it into any artifact. Never assert from memory, from a sandbox copy, or from an inherited
  summary. This rule exists because this session produced false claims (01.1.0 "doesn't exist"; mobile
  "not started") that were contradicted by files sitting in the connected repos. Search first, every time.
- Git diff is truth, not CC checkboxes (`git diff --stat origin/main HEAD`). Green build ≠ renders ≠ OTA.
- **Every CC build prompt opens with `/automate-dev` as line one** — no prompt ships without it; without it
  the build→review→simplify→test→fix loop collapses to a single pass. One task per prompt; explicit
  per-sub-task gates; file approval option 1 (file-by-file).
- Files not copy-paste (mobile corrupts unicode). Stage by explicit path, never `git add -A` (the one
  exception this session — a fully-enumerated rename move — was verified file-by-file before staging).
- `/clear` not `/compact`. Security-critical work not past ~70–80% context.
- Design-system = STRICT pixel-faithful law; additive-only to tokens; no interpretation.
- Every irreversible step owner-gated (remote, push, env/secrets, prod deploy, EAS publish, squash). Two-sided discipline (§4) in force.

---
*Supersedes 2026-06-16T11-46-00. Filename: studio-suite-continuation-2026-06-16T14-32-00.md*
*Commit in isolation to `~/kingdom/docs/studio-suite/` (stage ONLY this file; `git status` to verify).*
*Paired handoff: 2026-06-16T14-32-00-studio-suite-orchestrator-handoff.md*
