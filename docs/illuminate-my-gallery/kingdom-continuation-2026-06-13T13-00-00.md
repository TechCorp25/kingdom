---
title: "Kingdom — Continuation Baseline (landing workstream CLOSED; portfolio/pricing/contracts/R2 carried forward)"
project: IlluminateMyGallery (active)
owner: TechCorp (solo developer, Melbourne AU)
version: 2026-06-13T13-00-00
supersedes: kingdom-continuation-2026-06-13T10-00-00.md
state: CLEAN boundary — landing canonical rebuild + gating + polish all squash-merged to main
repo_app: techcorp-DevApps/IlluminateMyGallery  (project dir: ~/kingdom/projects/illuminate-my-gallery)
repo_control_plane: TechCorp25/kingdom  (this file lives in ~/kingdom/docs/)
---

# Kingdom — Continuation Baseline

This supersedes `kingdom-continuation-2026-06-13T10-00-00.md`. Where they differ, THIS wins on facts.
SHAs below are "last observed" — verify with the commands in §6 before any branch work.

## 1. Git state (verify before trusting)
- **main tip: `ed9957a`** — squash-merge of `design-system/landing-canonical-body` (landing canonical
  body rebuild + Investment gating + type-scale/depth polish). Replaces the prior tip `cfc86ea`
  (landing conformance #17).
- Branch lineage that produced it (now squashed away): `46ffe62` canonical BODY rebuild → `33ba1d4`
  Investment gating → `7e9f6ae` type-scale + depth polish.
- `design-system/landing-canonical-body` is to be DELETED (local `-D`, remote via PR). After cleanup,
  `git branch -a | grep landing` must return nothing.
- Local `main` was behind at `3f05ea9` (railway.toml) and has been fast-forwarded to `ed9957a`.

## 2. What CLOSED this session (landing workstream — done, merged)
- **Investment section gated** to an honest "pricing on enquiry" panel. Removed the invented
  COLLECTIONS array (Essentials/Signature/Atelier, prices 3200/5800/9200) and the orphaned
  CollectionCard so nothing fictional ships in the bundle. Headline "Three collections." →
  "Bespoke by nature." CTA reuses existing `/book` route. In-code `// WIP:` comment points to the real
  5-category schedule (Workstream 1); does not render.
- **Type-scale corrected** to the canonical's own `clamp()` ramps (hero `clamp(48px,6vw,88px)`, h2s
  `clamp(36px,5vw,56px)` / `clamp(30px,4vw,40px)`, pricing `clamp(28px,4.5vw,36px)`, testimonial
  `clamp(24px,4vw,32px)`). Fixed the desktop overshoot (hero was 88px, canonical is 76.8px @1280).
  Verified by COMPUTED font-size measurement at 375x812 and 1280x1600, light + dark.
- **Depth restored** as ADDITIVE DS primitives in `frontend/src/index.css` (theme-aware, values ported
  from `design-system/components/landing.jsx` + `design-system/styles`): `.hero-atmosphere` (gold
  blooms), `.shadow-collage`, `.panel-gold` (gradient + gold border + `--shadow-gold`). index.css diff
  is 100% additive — no existing token modified/removed; `tailwind.config.js` untouched.
- **Latent bug fixed:** `shadow-[var(--shadow-lg)]` was parsed by Tailwind as a shadow COLOR and
  rendered `box-shadow: none` — the conformance pass's collage shadow never displayed. Replaced with
  the named `.shadow-collage` utility. (Standing gotcha — see §7.)

## 3. Path reconciliation (RETIRED — formerly "studio vs gallery")
- There is ONE checkout: `~/kingdom/projects/illuminate-my-gallery`. **No `illuminate-my-studio`
  directory exists.** The memory's "studio" naming was an artifact. Gallery is canonical.
- Canonical design-system reference (for any future faithful rebuild) lives at the repo root:
  `design-system/components/landing.jsx` (the component), `design-system/styles/tokens.ts` (type scale,
  shadow spec, breakpoints), `design-system/styles/styles.css` (`.display`/`.eyebrow` classes,
  `--shadow-*`, gold-glow, bloom alphas). The app page it pairs with is `frontend/src/pages/Landing.jsx`.
- The other `design-system/` on disk is CivicMAPS (`projects/civic-maps-preview/...`) — different
  project, ignore.

## 4. OPEN workstreams (carried forward)

### 4.1 Portfolio image pipeline  (owner-DECISION-gated — highest-value open item)
- Root cause of the grey "Selected Frames": no public portfolio image pipeline exists; `/api/portfolio`
  returns `[]`; the reel renders fixed 6 tiles when empty. No public R2/Worker route for studio photos.
- **NEW (Codex secondary review, P2):** `SelectedFrames({ items })` in `Landing.jsx` does
  `Array.from({ length: 6 }, (_, i) => items[i])` → always 6 clickable tiles; slots beyond
  `items.length` render blank. Pre-existing (from `46ffe62`); the merged branch did NOT regress it.
- **DISCREPANCY to reconcile:** Codex says default seed creates 3 portfolio entries; our 2026-06-12
  diagnosis observed `/api/portfolio` → `[]` (0). Conflict ⇒ likely the seed exists in code but isn't
  running on the deployed instance (seeding/deploy gap). VERIFY before choosing the interim fix.
- **Decision pending:** 5 pipeline options (orchestrator lean: public R2 bucket OR public Worker prefix
  — keeps Cloudflare posture; AVOID authless backend proxy, which reintroduces backend image-serving the
  architecture avoids).
- **Interim SelectedFrames fix (tie to pipeline choice):** limit rendered tiles to `items.length`
  (no blank clickable boxes) vs backfill canonical fallbacks (= generic stock on a real photographer's
  site → off-brand → owner call). A minimal standalone `items.length` guard can land off updated `main`
  independently if desired.

### 4.2 R2 env vars  (owner-executed in Railway — infra, not a code bug)
- 7 R2 vars NOT set on backend Railway service `098b3c91…` → upload returns 500. Includes
  `R2_BUCKET_ORIGINALS`, `R2_BUCKET_DERIVATIVES` + 4 related credentials (names enumerated in the
  prior baseline §4). Set in Railway, redeploy, re-test upload.

### 4.3 Pricing source-of-truth  (Workstream 1)
- Real schedule = FIVE categories (Family / Anniversaries / Kids Birthdays / Events / Weddings,
  ~22 packages), NOT 3 wedding collections. The landing Investment WIP comment points here.
- Decision pending: docs stay canonical (re-import) vs admin becomes canonical after first seed.

### 4.4 Contracts / consent  (Workstream 2 — business-confidential)
- 7-piece contract pack incl. consent / marketing release. Solicitor-review caveat on the legal set.
- Currently UNTRACKED at `docs/contracts ` — **NOTE the trailing space in the directory name** (brittle:
  breaks globs/tab-completion/scripts). Rename to `docs/contracts/` at a safe point; holds confidential
  material so do not touch casually. Decide where the confidential source docs live before any commit.

### 4.5 Cloudflare Worker confirmation → Priority 4 (gallery delivery)
- Worker at `media.illuminatestudios.com.au` (HMAC-SHA256 token validation) — long-pole dependency.
  Owner confirmation required before P4 staging validation. P4 branches fresh from updated main
  (`ed9957a`) after Worker confirmation.

### 4.6 Dependabot  (queued)
- 2 critical vulnerabilities flagged (GitHub default-branch notice seen on the polish push). Queue after
  active branch work. No dependencies were touched this session.

### 4.7 Luma quality + safety hardening  (separate, review-gated)
- Functioning; this is durable hardening, not a fix. Booking-safety guardrails are security-adjacent
  backend logic → require the merge-readiness playbook + go/no-go gate. Parked prompt/addendum:
  `docs/2026-06-07T16-00-00-luma-merge-readiness-prompt.md`,
  `docs/2026-06-07T16-45-00-luma-report-addendum-and-commands.md` (both untracked).

### 4.8 Mongo merge-readiness  (parked)
- Report at `.automate-dev/reports/2026-06-08T05-25-36Z-mongo-merge-readiness.md` (untracked).

## 5. Known untracked files (expected on the tree — none are app code)
`.automate-dev/reports/2026-06-08T05-25-36Z-mongo-merge-readiness.md`,
`.automate-dev/reports/2026-06-12T11-48-19Z-portfolio-pipeline-diagnosis.md`,
`docs/2026-06-07T16-00-00-luma-merge-readiness-prompt.md`,
`docs/2026-06-07T16-45-00-luma-report-addendum-and-commands.md`,
`docs/contracts ` (confidential; trailing-space name).

## 6. Verification commands (run at next session start)
```
cd ~/kingdom/projects/illuminate-my-gallery
git fetch origin
git log --oneline -3 origin/main          # expect tip ed9957a
git branch -a | grep landing              # expect EMPTY (branch deleted)
git status -sb                            # expect clean except the §5 untracked files
```
For the portfolio discriminator: `/api/portfolio` response (DevTools/Network) and whether the deployed
backend ran its seed — settle the §4.1 "3 vs 0 entries" discrepancy.

## 7. Standing rules & gotchas (authoritative)
- **File-based delivery only** — mobile corrupts unicode on paste; all code/prompts as downloadable .md.
- **`/automate-dev` is line 1** of every CC prompt — it's a SKILL invocation, not a path (symlinked
  `~/kingdom/.claude/skills` → `~/.claude/skills`); its Python review scripts are non-authoritative for
  JSX/JS.
- **Owner-gated merges**; squash-merge + delete source branch same step; branch fresh from verified
  main; `git pull --ff-only`; never force-push (two-sided repo, CC + Codex both commit).
- **Squash non-ancestry trap:** a branch forked before a prior squash may not have `origin/main` as an
  ancestor → land ONLY via squash-merge PR, never a local merge. (This branch was exactly that case.)
- **git diff is truth.** Green build ≠ renders correctly. Render-at-1280 ≠ responsive — verify MOBILE
  and desktop, both themes; prefer COMPUTED font-size measurement over eyeballing.
- **Acceptance criteria from the right reference** (the canonical component), not a styling diff.
- **"No new tokens" is too strict for a faithful canonical rebuild** — allow ADDITIVE DS primitives
  ported from canonical/spec values; NEVER modify/remove existing tokens (protects admin/shared
  consumers that read `index.css` / `tailwind.config.js`).
- **Tailwind shadow gotcha:** `shadow-[var(--x)]` is parsed as a shadow COLOR and renders nothing
  without a base shadow utility — use named `.shadow-*` utilities instead.
- **Stage by explicit path** — never `git add -A` on a dirty tree.
- **`cd` does not persist** across CC's ephemeral bash subprocesses — launch from the project dir.
- **`/clear`, not `/compact`**; security-critical work not pushed past 70–80% context; CC file approval
  always option 1 (file-by-file), never option 2 for security-critical.
- **`from __future__ import annotations`** in FastAPI route files → HTTP 422 on affected endpoints.
- **Model note:** Claude Fable 5 is currently unavailable; CC sessions run on Opus 4.8. If Fable 5 is
  set as the model default, re-select Opus 4.8 at session start.

## 8. Operating model (unchanged)
Orchestrator/relay: the controller (claude.ai) is the architectural decision + review layer above
Claude Code (the build executor). Owner runs the terminal/Railway, pastes raw logs back; the controller
reasons from logs, gates irreversible steps, and drafts automate-dev prompts as downloadable files.
No machine access. Frame as task + operating context + explicit verification, never persona.

## 9. Session-close protocol (for the NEXT close)
At a clean boundary: produce the next `kingdom-continuation-<ISO8601>.md` superseding THIS file, commit
it in isolation to `~/kingdom/docs/` (stage ONLY that file; verify with `git status`), push, then
`/clear`. Also produce the paired `<ISO8601>-kingdom-orchestrator-handoff.md` for the new chat.
