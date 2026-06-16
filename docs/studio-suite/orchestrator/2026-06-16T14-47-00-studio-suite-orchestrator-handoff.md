---
title: "studio-suite — Orchestrator Handoff (next session)"
project: "studio-suite (Kingdom workspace)"
prepared: "2026-06-16T14-47-00"
pairs_with: "studio-suite-continuation-2026-06-16T14-32-00.md (state-of-truth)"
type: "MID-TASK handoff — session-01 close; next session resumes with a settled plan"
---

# Orchestrator Handoff — studio-suite

You are the **orchestrator / relay**: the architectural decision + review layer (claude.ai) above Claude
Code. You do NOT run commands. The owner runs terminal / Railway / EAS and pastes raw output; you reason
over it, gate every irreversible step, draft CC prompts as downloadable files. Task + context +
verification framing — never persona.

## §0 — ★ READ THIS FIRST: how to operate (this session taught these the hard way)
1. **★ NON-NEGOTIABLE — verify against BOTH repos before asserting anything.** Before you state or write
   into any artifact ANY claim about git state, file existence, prompt contents, or task status, use
   project/repo search to confirm it against **both** the connected `studio-suite` and `kingdom` repos.
   Never from memory, sandbox copy, or an inherited summary. (This session produced false claims —
   "01.1.0 doesn't exist", "mobile not started" — contradicted by files sitting in the repos. Do not repeat it.)
2. **★ Small, individually-gated tasks — owner's explicit directive.** The owner would rather run 10
   small, heavily-gated sessions than one sprawling one. Decompose to the smallest single-concern unit.
   **One CC build prompt per session, authored cold in that session, verified per §0.1.** Do NOT bulk-write
   prompts ahead — that is exactly how this session's errors happened (writing on momentum, tired, unverified).
3. The baseline `studio-suite-continuation-2026-06-16T14-32-00.md` is state-of-truth. Read it fully.
   It supersedes T11-46-00 and records the two corrections (01.1.0 exists; Architecture B ratified).

## §1 — Settled decisions (do NOT re-litigate; this session churned enough)
- **Mobile = Architecture B:** native Expo/RN consuming a shared **`@is/tokens`** package (the design-
  system's prescribed path). The `use-dom` webview plan is SUPERSEDED.
- **`@is/tokens` adoption happens before web ships** (cheapest moment; no shipped web app to migrate).
- **★ JS/TS decision LOCKED — option 1:** `@is/tokens` is authored in TypeScript but **compiles to
  `dist/index.js` + `dist/index.native.js` + `dist/css/index.css` + `.d.ts`**. The web app **stays
  JavaScript** (it is `.jsx`, npm, `jsconfig.json`, `components.json` `"tsx": false`) and consumes the
  **compiled** package. NO web→TypeScript conversion. (`package.json "main": "./dist/index.js"` was
  designed for JS consumers.) A web TS conversion, if ever wanted, is its own separate future task.
- **Repo moves to a pnpm workspace** to host `packages/tokens/`. This changes the web lockfile
  (`package-lock.json` → `pnpm-lock.yaml`) and the Railway web build command — **owner-gated infra.**
- Self-hosted fonts (no CDN); default theme LIGHT (toggle dark); both themes must work. Design-system =
  STRICT pixel-faithful law.

## §2 — ★ The gated task ledger (next sessions execute these in order, one per session)
See the paired `2026-06-16T14-47-00-studio-suite-task-ledger.md` for the full per-task gate detail. Order:

- **01.0.1a — Tokenization foundation (infra).** Stand up `packages/tokens/` (`@is/tokens`) from the
  design-system's `scripts/tokens.ts` + `ds-handoff.jsx`; pnpm workspace; build emits the 3 dist outputs;
  web converted to **consume the compiled package** (stays JS); Railway web build made pnpm-aware.
  **Gate:** `pnpm -F @is/tokens build` emits all 3 outputs; web still builds + deploys; theme swap works;
  **placeholder landing visually UNCHANGED** (proves foundation in isolation). Owner-gated Railway change.
- **01.0.1b — Faithful public landing (visual).** On the `@is/tokens` foundation, build the landing
  pixel-faithful to `design-system/components/landing.jsx`. **Gate: VISUAL** vs the design-system,
  light + dark (Cormorant/Cinzel hero, gold-only, `#050505`, collage + SINCE MMXIV, 280+/12YR/40, Selected Frames).
- **01.1.0 — Mobile foundation (native).** Expo/RN under `mobile/` consuming the SAME `@is/tokens`
  (ThemeProvider.native, expo-font ×5, useColorScheme, react-native-svg, expo-secure-store) + EAS/OTA
  pipeline (eas.json, Update channels, `.eas/workflows/*`, CI mobile job). **Gate:** DS 12-point checklist
  green (both apps themed, no flash, all fonts); owner runs `eas init`→`eas update` OTA proof.
- **01.1.1 — First faithful native screen (visual).** **Gate:** visual on device/sim, light + dark.
- **Then** (each its own task): backend `/api/health` close-out + Railway env/secrets; web surfaces
  (Studio Admin, Client portals + sign-in, Investment/pricing, Experience, Journal); R2/Worker media pipeline.

## §3 — The gate loop (every CC task)
At each CC gate, owner pastes CC's report PLUS the raw facts:
```
git diff --stat origin/main HEAD
git diff --name-only origin/main HEAD
git status --short
# task-specific greps (e.g. for 01.0.1b: grep -rn "googleapis" web/ ; grep -rn "shadow-\[var(" web/)
```
Re-derive from the raw diff, never CC's prose. Confirm the branch forked from the CURRENT `main` SHA
(pin it; don't trust a stale SHA in any prompt). Infra gates (pnpm/Railway, eas.json) are owner-gated.
Visual gates need a served build + screenshot compared to the design-system — green build proves nothing.

## §4 — Watch items (verified, carry forward)
- **Two-sided repo:** fetch + `git branch -a` every session; `--ff-only` only; never force; pin to SHA.
  Owner sometimes edits infra on GitHub web — inspect any unexpected `origin/main` move with `git show --stat` before ff.
- **Deferred Codex branch** `codex/set-up-automated-git-workflows-with-codex` (`979e1da`) — do NOT merge yet.
- **Web build fragility** changes under pnpm (§1) — re-verify the Railway build command when `@is/tokens` lands;
  pre-pnpm rule was: bare `npm run build` depends on Railpack devDeps, fix `vite: not found` via
  `NPM_CONFIG_INCLUDE=dev`, never a second `npm ci` (caused EBUSY).
- **Backend traps:** no `from __future__ import annotations` in route/`Depends` modules (HTTP 422);
  Tailwind never `shadow-[var(--x)]` (named `.shadow-*`).
- **Stale docs:** `.orchestrator/InstructionalPrompt_01.1.0.md` (Jun-15) and `SESSION_01.md §0.3` still
  describe the OLD `use-dom` plan. The baseline supersedes them on authority; the 01.1.0 rewrite (when
  authored) replaces the prompt. `SESSION_01.md` is a historical doc — leave it; baseline overrides.

## §5 — Git state (verified 2026-06-16T14-32)
- `studio-suite` `main` tip = **`42b1a0b`**, clean, = origin. Web live: `studio-suite-preview.up.railway.app`.
  Web service id `a3b1e95d-d9ea-41b9-92c8-15c7f71c2837`.
- `kingdom` docs repo tip = **`5670c8b`** (T14-32-00 baseline committed in isolation + pushed). Per-project
  subfoldered: `docs/illuminate-my-gallery/`, `docs/studio-suite/`.

## §6 — Operating reminders
Owner is the only machine relay. Files not copy-paste (mobile corrupts unicode; prefer raw git/grep over
CC prose). `/automate-dev` line one of every build prompt. File approval option 1. `/clear` not `/compact`.
Every irreversible step owner-gated. Keep steady judgment; gate hard; re-derive from verified facts; and
when unsure of state — **search both repos before you speak.**

---
*Session-01 close (mid-task). Next session: resume at 01.0.1a, one prompt, authored cold + verified.*
*Prepared 2026-06-16T14-47-00. Pairs with baseline T14-32-00 and the task ledger T14-47-00.*
