---
title: "studio-suite — Gated Task Ledger"
project: "studio-suite (Kingdom workspace)"
prepared: "2026-06-16T14-47-00"
pairs_with: "studio-suite-continuation-2026-06-16T14-32-00.md · 2026-06-16T14-47-00-studio-suite-orchestrator-handoff.md"
principle: "Smallest single-concern unit per task. One CC prompt per session, authored cold + verified per the dual-repo rule. Heavily gated."
---

# studio-suite — Gated Task Ledger

The remaining work, decomposed to the smallest reviewable units, in execution order. **One task = one
session = one prompt.** Each prompt is authored cold in its own session (not bulk-written ahead), opens
with `/automate-dev`, and is verified against both repos before it ships. Every task has ONE primary
concern and ONE decisive gate. Infra changes are owner-gated. Do not combine tasks to "save time" — the
combining is what went wrong.

> Status legend: ☐ not started · ◐ prompt authored, not run · ● done (on `main`)

---

## PHASE A — Tokenization (unblocks everything; Architecture B)

### ☐ 01.0.1a — Stand up `@is/tokens` + pnpm workspace (INFRA)
- **One concern:** the shared token package exists, builds, and web consumes it — with NO visual change.
- Build `packages/tokens/` from `design-system/scripts/tokens.ts` + `ds-handoff.jsx`: `tokens.ts`,
  `index.ts`, `ThemeProvider.tsx`, `ThemeProvider.native.tsx`, `package.json` (`name:"@is/tokens"`,
  conditional exports `react-native`→`dist/index.native.js`, default→`dist/index.js`, `./css`→`dist/css/index.css`),
  a build step (e.g. tsup) emitting all three dist outputs + `.d.ts`.
- Convert repo to **pnpm workspace** (`pnpm-workspace.yaml`); web keeps JS, imports the **compiled** package
  + `@is/tokens/dist/css/index.css`; mount `ThemeProvider defaultTheme="light"` at web root. Placeholder
  landing otherwise untouched.
- **Owner-gated infra:** Railway web build command → pnpm-aware; lockfile → `pnpm-lock.yaml`. Surface as
  an infra decision; owner provisions the Railway change and confirms the deploy.
- **GATE:** `pnpm -F @is/tokens build` emits index.js + index.native.js + css/index.css; `pnpm -F web build`
  green; web still deploys on Railway; theme swap (light↔dark) works at root; **placeholder landing renders
  visually identical to before** (proves the foundation in isolation, no fidelity work yet).
- Branch `feature/tokens-package` off current `main` → PR → CI → owner Railway-deploy confirm → squash.

---

## PHASE B — Web public landing

### ☐ 01.0.1b — Faithful public landing (VISUAL)
- **One concern:** the public landing matches the design-system, pixel-faithful.
- On the `@is/tokens` foundation, replace `web/src/pages/Landing.jsx` faithful to
  `design-system/components/landing.jsx`: self-host Cinzel/Cormorant/Inter/JetBrains Mono; nav
  (Portfolio·Experience·Investment·Journal · Client Portal · Reserve a Date · theme toggle); hero
  (◆ Est. Melbourne·2014; Cinzel lines + Cormorant-italic gold "quietly extraordinary."; lede; BEGIN +
  VIEW PORTFOLIO; floating collage + SINCE MMXIV badge); stat row 280+/12YR/40; RECENT WORK → SELECTED
  FRAMES + ALL PORTFOLIO. Nav buttons may route to placeholders (those surfaces are later tasks). Use
  design-system assets; do NOT wire `/api/portfolio`. Never `shadow-[var(--x)]`.
- **GATE: VISUAL.** Serve build; compare to the design-system in **light AND dark** — Cormorant/Cinzel
  hero (not Helvetica), gold-only accent, `#050505` not black, collage + badge, stat row, Selected Frames.
  Screenshot for review. Green build is NOT the gate.
- Branch `feature/landing-from-design-system` off current `main` → PR → CI + VISUAL GO → squash.

---

## PHASE C — Mobile foundation

### ☐ 01.1.0 — Native mobile foundation on `@is/tokens` (NATIVE + EAS/OTA)
- **One concern:** the Expo app exists, is themed from the shared package, and the OTA pipeline is provable.
  No app screens.
- Scaffold Expo/RN under `mobile/` (SDK per owner's ratified baseline — verify current, do not assume
  55/0.83.2); consume the SAME `@is/tokens` via `ThemeProvider.native`; `expo-font` preloads all five
  families; `useColorScheme` drives theme; `react-native-svg` icons; `expo-secure-store` for sessions.
  NativeWind/react-native-css for local Tailwind (no CDN). Read the `expo-*` skills first.
- EAS/OTA (fold in the good scoping from the Jun-15 draft): `eas.json` (development/preview/production +
  Update channels), app config wired for EAS Update, `.eas/workflows/{development,preview,production,hotfix}.yml`,
  CI mobile job (tsc/lint, builds stay cloud-side). `eas.json`/workflows are infra — surface for owner review.
- **GATE:** DS 12-point checklist green (ThemeProvider at root, theme swap no-flash, all five fonts, etc.);
  typecheck/lint clean; owner runs `eas init`→ dev build → `eas update` → confirms OTA pull.
- Branch `foundation/mobile-eas` off current `main` → PR → CI + owner OTA proof → squash.

### ☐ 01.1.1 — First faithful native screen (VISUAL)
- **One concern:** one screen, pixel-faithful, native.
- **GATE:** visual on device/simulator, light + dark, vs the design-system.

---

## PHASE D — Backend + infra close-outs (each its own small task)
- ☐ **D1** — Backend Railway env/secrets (`MONGODB_URI`, `MONGODB_DB_NAME`, CORS vars; `CORS_ORIGIN_REGEX`
  = `^https://[a-z0-9-]+\.up\.railway\.app$`) + deploy + `/api/health` + `/api/health/db` verified live. Owner-gated.
- ☐ **D2** — PR-preview CORS preflight proof (throwaway PR → preview frontend reaches preview backend, no failing OPTIONS).
- ☐ **D3** — Kingdom tracked-project registration for studio-suite (add to kingdom baseline's table at next kingdom close).

---

## PHASE E — Product surfaces (each its OWN scoped, visual-gated task; do NOT batch)
- ☐ Studio Admin portal  ·  ☐ Client portal(s) + sign-in flows  ·  ☐ Investment / pricing  ·
  ☐ Experience  ·  ☐ Journal  ·  ☐ R2 + Worker media pipeline (private buckets, Worker-gated CDN, no backend byte-streaming).
- Each consumes `@is/tokens`, is pixel-faithful to the design-system, and has a visual gate. One per session.

---

## Deferred / parked (not scheduled)
- Codex workflows branch `979e1da` — merge decision parked.
- `@is/ui` component package (the design-system also prescribes it) — adopt if/when shared primitives are
  needed beyond tokens; not required for the landing or mobile foundation.
- Web→TypeScript conversion — only if ever desired; its own task, not bundled into tokenization.

---
*Execute top-to-bottom, one task per session. Re-verify the current `main` SHA at the start of each
(it moves — owner web edits, Codex). Author each prompt cold, verified against both repos. Heavily gated.*
