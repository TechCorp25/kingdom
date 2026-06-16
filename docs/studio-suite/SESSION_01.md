---
title: "SESSION_01 — studio-suite · Foundation + dual deployment pipeline"
project: "studio-suite (Kingdom workspace)"
owner: "TechCorp (solo developer, Melbourne AU)"
orchestrator_layer: "claude.ai — architectural decision + review (above Claude Code)"
prepared: "2026-06-15T12-30-00"
status: "READY — §1 locked this session; Phase 0 is owner-gated and runs first"
supersedes: "n/a (first session)"
next_baseline: "~/kingdom/docs/studio-suite/studio-suite-continuation-<ISO8601>.md (produced at session close)"
---

# SESSION_01 — studio-suite

First build session. Goal: **stand up the monorepo skeleton and prove BOTH deployment
pipelines green (Railway CD for web/backend · EAS Update OTA for mobile) before any feature
work.** No product features land this session — feature build (replicating the design-system)
begins Session 02, after the web app exists for the mobile app to replicate.

Operate as the relay: this layer drafts files, reasons over pasted raw output, and gates every
irreversible step. The owner runs the terminal / Railway / EAS. Files, never paste.

---

## §0 — Decisions ratified + the three still to ratify at the Phase-0 gate

### Locked this session (do not re-litigate)

| Field | Value |
|---|---|
| Product | Studio management system + client-portal companion. **Public no-auth marketing front-end** = entry point → **auth-gated studio admin portal** + **individual auth-gated client portals**. Burst-access high-res media in scope. |
| Repo | `git@github.com:techcorp-DevApps/studio-suite.git` · default branch `main` |
| Kingdom slug / dir | `studio-suite` · `~/kingdom/projects/studio-suite/` |
| Topology | **Monorepo:** `backend/` · `web/` · `mobile/` (+ `shared/` if a shared API client/types emerge) |
| Stack (inherited from IMG — **NOT** the CLAUDE.md Flask/MongoEngine default) | Backend **FastAPI + async Mongo (Motor)**; web **Vite + React 19 + Tailwind + shadcn/ui** (publish `build/`); mobile **Expo + React Native** (EAS); **MongoDB Atlas** (metadata only) · **Cloudflare R2** private buckets + **Worker/CDN** for media |
| Hosting | **Railway** — backend + web (+ derivative worker) services. Mobile ships via **EAS**, not Railway. |
| "OTA" scope | Railway native CD (prod from `main`) + PR/branch preview deploys + a `.github/workflows/ci.yml` gate **AND** EAS Workflows (`.eas/workflows/`) + EAS **Update** OTA channels for mobile |
| Baseline location | `~/kingdom/docs/studio-suite/` · file `studio-suite-continuation-<ISO8601>.md` |
| Committers | **Claude Code only** to start (single-sided; add Codex + two-sided `--ff-only` discipline only when a second committer joins) |
| CC model | **Opus 4.8** (re-select if Fable 5 is the default and unavailable) |

> **Stack-divergence note, on purpose:** studio-suite inherits IMG's FastAPI/Motor/React/Railway
> stack because it is a port of the IMG orchestrator model — it does **not** use the
> `CLAUDE.md` greenfield default (Flask + MongoEngine + Tailwind + Waitress). That default is the
> Le Répertoire ecosystem's; it does not apply here. Flagged so the FastAPI choice is not a surprise.

### To ratify at the Phase-0 gate (orchestrator recommendation in **bold**; owner confirms before any command runs)

1. **Mobile target platforms** — **iOS + Android** (recommended: the client portal is consumer-facing;
   clients are on iPhones). Your eMAPS pattern is Android-only — confirm you do *not* want that here.
2. **Mobile location on disk** — **`~/kingdom/projects/studio-suite/mobile/`** inside the monorepo
   (native btrfs; symlinks/inodes are fine here — the FUSE problem is only `/mnt/chromeos/*`; EAS Build
   runs cloud-side, so heavy local `node_modules` is the only footprint). Confirm this over your
   standalone `~/app-work/` Node convention, which exists for non-kingdom projects.
3. **Web↔native code-sharing strategy** — defer the final call to Session 02, but the likely mechanism
   is the installed **`use-dom`** skill (run web React in a webview on native, migrate incrementally) so
   the RN app can "replicate the web app exactly" without a parallel rewrite. Noted now as the working
   assumption; not committed this session.

---

## §1 — Session shape (two CC build tasks, each its own prompt)

| Task | Prompt file | Scope | Pipeline proven |
|---|---|---|---|
| 01.0.0 | `InstructionalPrompt_01.0.0.md` | Monorepo hygiene + **backend** (FastAPI health/config/CORS/Mongo-resolver) + **web** (Vite/React/Tailwind/shadcn shell) + `railway.toml` ×2 + `.github/workflows/ci.yml` | **Railway CD + PR previews + CI gate** |
| 01.1.0 | `InstructionalPrompt_01.1.0.md` | **mobile** (Expo shell that renders one screen) + `eas.json` + `.eas/workflows/{development,preview,production,hotfix}.yml` + EAS **Update** channels | **EAS Update OTA** |

One task per prompt. `/automate-dev` is line one of each. Each prompt carries explicit per-sub-task
completion gates and ends with a pre-output verification checklist. File approval = **option 1
(file-by-file)**, always.

---

## §2 — Phase plan (interleaves owner-infra with CC builds; full commands in the CC-Command-Sequence file)

**Phase 0a — repo genesis (owner, no CC).** `kstart` → make project dir → `git init -b main` →
create the empty remote → empty initial commit → push. Register studio-suite as a kingdom tracked
project. *Gate: confirm repo org/name + the three §0 ratification items before the remote is created —
remote creation + first push is the irreversible step.*

**Phase 1 — CC task 01.0.0 (backend + web + Railway CD + CI).** Paste `InstructionalPrompt_01.0.0.md`
as message one of a fresh CC session (launched from the project dir). CC branches off `main`, scaffolds,
self-reviews via automate-dev, pushes. Owner pastes back CC's report **plus** `git diff --stat
origin/main HEAD` and `git diff --name-only`. This layer re-derives from the raw diff against the
completion gate, recommends, and gates the squash-merge.

**Phase 0b — Railway hookup (owner, after 01.0.0 on `main`).** Create the Railway project, link the
repo, create **backend** (root `/backend`) and **web** (root `/web`, publish `build/`) services, set
service roots + the build commands from the merged `railway.toml`s, set env vars (Mongo, R2, CORS
regex — secrets, owner-only). Verify: prod deploys from `main`; open a throwaway PR and confirm a
**preview deployment** appears and the preview frontend can reach the preview backend (CORS
`allow_origin_regex`). *Gate: env-var/secret entry and the first production deploy are owner-confirmed.*

**Phase 2 — CC task 01.1.0 (mobile + EAS OTA).** Paste `InstructionalPrompt_01.1.0.md` into a fresh CC
session. CC reads the `expo-*` skills, scaffolds the Expo app + EAS config, pushes; same review/gate loop.

**Phase 0c — EAS hookup + OTA proof (owner, after 01.1.0 on `main`).** `eas init`, link the project,
configure Update channels, run a **development build**, then publish an **EAS Update** and confirm the
running build pulls it OTA. *Gate: project linking + first publish are owner-confirmed.*

**Phase 3 — session close (§7 protocol).** Commit at the clean boundary → produce
`studio-suite-continuation-<ISO8601>.md` in `~/kingdom/docs/studio-suite/` (supersedes nothing yet —
first baseline) → commit it **in isolation** (stage only that file; `git status` to verify) → push →
produce the paired `<ISO8601>-studio-suite-orchestrator-handoff.md` → `/clear`.

---

## §3 — Definition of done for Session 01

- `main` exists with the monorepo skeleton; `backend/`, `web/`, `mobile/` all build clean.
- Railway: production deploys from `main`; a PR produces a working preview (frontend→backend CORS OK).
- EAS: a development build runs and successfully pulls a published **EAS Update** OTA.
- `.github/workflows/ci.yml` runs lint + test + build on PRs and is **required** before merge.
- No secrets in git; `.env.example` files present for every service; `.gitignore` covers
  `.env`, `.venv/`, `node_modules/`, `build/`, Expo/EAS local artifacts.
- First continuation baseline committed in isolation to `~/kingdom/docs/studio-suite/`.

If context runs past ~70–80% before this is reached, **stop at the nearest clean boundary, commit,
and hand off mid-task** (the handoff's §0 names the single open thread to resume).

---

## §4 — Standing stack traps in force this session (from §6 of the orchestrator prompt)

- **No `from __future__ import annotations`** in any FastAPI route file or any module used as a
  class-instance `Depends()` → silent HTTP 422 on affected endpoints.
- **Tailwind `shadow-[var(--x)]`** parses the var as a shadow *colour* → renders nothing. Named
  `.shadow-*` utility only.
- **Backend never streams image/media bytes** — Worker-gated CDN from private R2. No sync derivatives;
  no public bucket, no `r2.dev`. Both buckets private (`R2_BUCKET_ORIGINALS`, `R2_BUCKET_DERIVATIVES`).
- **Web Railway build keeps dev deps** — Vite lives in `devDependencies`; build command must
  `npm ci --include=dev && npm run build`, serve `npx serve -s build`. A bare `npm run build` under
  `NODE_ENV=production` fails `vite: not found`.
- **DB env names canonical** — `MONGODB_URI` + `MONGODB_DB_NAME`; no legacy aliases left set.
- **Dependabot** gets its own deliberate pass, never folded into a feature/foundation merge.
- **Additive-only** to shared design tokens / CSS.
- **`railway.toml` / `eas.json` / deploy config are infra decisions** — surfaced to the owner, never
  silently modified by CC.

---

## §5 — Hard operating rules (do-not-lapse)

- Git diff is truth, not CC's task checkboxes. Re-derive from `git diff --stat origin/main HEAD`.
- Green build ≠ renders / ≠ OTA works. Prove by running the deployed result and the OTA pull.
- Stage by explicit path; commit per concern. Never `git add -A`.
- `/clear`, not `/compact`, at high context. Commit at a clean boundary first.
- Files, not copy-paste, for everything handed to the owner.
- Every irreversible step (remote creation, first push, env/secrets, prod deploy, EAS publish,
  squash-merge) is owner-gated.

---

*Anchor doc for Session 01. Paired files: `SESSION_01_ToDo.md`,
`SESSION_01_CC-Command-Sequence.md`, `InstructionalPrompt_01.0.0.md`,
`InstructionalPrompt_01.1.0.md`. Prepared 2026-06-15T12-30-00.*
