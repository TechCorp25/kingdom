---
title: "studio-suite — continuation baseline"
version: "2026-06-17T04-38-29"
supersedes: "studio-suite-continuation-2026-06-16T14-32-00.md"
project: "studio-suite (new app dev) · Kingdom workspace"
owner: "TechCorp (solo developer, Melbourne AU)"
status: "AUTHORITATIVE STATE — newest baseline wins on facts"
boundary: "CLEAN — 01.0.1a closed, squash-merged to main, deployed live, render-confirmed"
---

# studio-suite — continuation baseline (2026-06-17T04-38-29)

This file supersedes the T14-32 baseline and is the source of truth for state. The orchestrator
system prompt still governs **how to operate**; this file governs **facts**. Re-derive live at
session start (§9) before trusting any SHA — recorded SHAs are the state at close, not a substitute
for `git fetch`.

---

## 0. ★ Status at close — CLEAN boundary

**01.0.1a is COMPLETE, merged, deployed, and render-confirmed on production.** Not mid-task. The
next session starts a new task (01.0.1b) cleanly from the pinned `main` SHA below.

What landed: the shared design-token package `@is/tokens` exists and builds to its three dist
outputs; the repo is a pnpm workspace; the web app consumes the **compiled** package; `ThemeProvider`
mounts at the web root; and the placeholder landing renders **visually unchanged** (proven: 0/1,024,000
px diff light + dark, and a clean live render on `main`). The pnpm + Railway infra migration is
**proven live**, not theoretical — see §5, which is the most important section for the next session.

---

## 1. Pinned git state (re-derive live before trusting)

| Repo | Tip SHA | Meaning |
|---|---|---|
| studio-suite `main` | **`0ded334`** | "Feature/tokens package (#3)" — the 01.0.1a squash. **Pin 01.0.1b off this.** |
| studio-suite (prev) | `42b1a0b` | "Update railway.toml" — the 01.0.1a base, now parent of `0ded334`. |
| studio-suite Codex | `979e1da` | `origin/codex/set-up-automated-git-workflows-with-codex` — **DEFERRED, do NOT merge.** |
| kingdom docs | `7180708` | pre-this-baseline tip; committing THIS baseline + handoff advances it. |

- `git rev-parse HEAD origin/main` at close → both `0ded3346747441ea8eee66fc796f97a93e094519`; tree clean.
- `feature/tokens-package` is **fully deleted** — local (`-D`, was `6929e1a`), remote (GitHub), and the
  stale remote-tracking ref pruned. It is a squash-severed non-ancestor of `main`; **never recreate or
  reuse that name.**
- Branches present: `main`, `origin/main`, `origin/codex/...` only.

---

## 2. Topology (unchanged from T14-32 + the workspace move)

Monorepo at repo root: `backend/` (FastAPI, Python — NOT a pnpm member) · `web/` (Vite + React 19 +
Tailwind + shadcn/ui, **JavaScript**, publishes `web/build/`) · `packages/tokens/` (`@is/tokens`,
TypeScript, the new shared package) · `design-system/` (strict pixel-faithful **law**: `scripts/tokens.ts`
is canonical token source, `components/ds-*.jsx` are the fidelity reference). `mobile/` not yet created
(arrives 01.1.0).

pnpm workspace members (`pnpm-workspace.yaml`): `packages/*` and `web`. Backend is Python; not a member.

---

## 3. Locked architecture decisions (do NOT re-litigate)

- **Architecture B**: native Expo/RN consuming `@is/tokens` (the `use-dom` web-in-webview path is
  superseded). Tokens adopted before web ships fidelity.
- **JS/TS option 1**: tokens authored in TS, compiled to `dist/index.js` + `dist/index.native.js` +
  `dist/css/index.css` + `.d.ts`. **Web stays JavaScript and consumes the compiled package** — no
  web→TS conversion.
- **Default theme LIGHT**; both light + dark must work.
- Self-hosted fonts (Cinzel, Cormorant Garamond, Cormorant Italic, Inter, JetBrains Mono) — **deferred
  to 01.0.1b**, NOT done in 01.0.1a.
- design-system is strict law; tokens are **additive-only**.

---

## 4. `@is/tokens` — as built (reference for consumers)

- Source `packages/tokens/src/`: `tokens.ts` (byte-identical copy of `design-system/scripts/tokens.ts`
  — keep in sync; design-system is law), `ThemeProvider.tsx` (web: sets `data-theme` on `body`, writes
  `themeToCSSVars` onto `documentElement`), `ThemeProvider.native.tsx` (context only), `index.ts`,
  `index.native.ts`. Build: `tsup && node scripts/build-css.mjs` (tsup first, then CSS generated from
  the built `themes`/`themeToCSSVars`).
- `package.json` exports: `"."` → conditional `react-native`→`dist/index.native.js` / default→`dist/index.js`;
  `"./css"` and `"./dist/css/index.css"` both → `dist/css/index.css`. `peerDependencies.react >=18`.
- Vars are namespaced (`--surface-*`, `--ink-*`, `--brand-*`, `--border-*`, `--scrim`) and set on
  `data-theme` — distinct from shadcn's own tokens, which is **why** the placeholder landing is
  unaffected. The vars are present-but-unused until a page consumes them (01.0.1b does).
- Web consumption (`web/src/main.jsx`): wraps `<App/>` in `<ThemeProvider defaultTheme="light">` and
  imports `@is/tokens/dist/css/index.css`.

---

## 5. ★★ pnpm + Railway infra reality — PROVEN LIVE (the hard-won lesson; do not relearn)

This session's main cost was making Railway build the workspace. The resolution, now confirmed by a
green build + live render:

- **`railway.toml` drives — dashboard overrides must stay CLEARED.** The web service had a stale
  dashboard **Custom Build Command** (`npm run build`) and **Custom Start Command** (`-s build`) that
  silently overrode the file and forced an `npm install` → which died on `workspace:*`
  (`EUNSUPPORTEDPROTOCOL`). Fix = clear both custom commands in the dashboard so `web/railway.toml`
  supplies them. **If a future deploy reverts to npm or stale commands, check for dashboard overrides FIRST.**
- **Web service Root Directory = repo ROOT** (not `web/`), config-as-code path = `web/railway.toml`.
  Root is required so Railpack sees the root `pnpm-lock.yaml` + `packageManager` and so the workspace
  installs. Because CWD is root, the start path is **`serve -s web/build`** (not `-s build`) — this is
  the `6929e1a` correction, now proven live.
- With root correct, **Railpack auto-detects pnpm** (`↳ Using pnpm package manager`, `Found workspace
  with 2 packages`, `Installing pnpm@10.34.3 with Corepack`). The earlier `No package manager inferred`
  only happened when rooted at `web/`.
- `web/railway.toml` effective config: builder RAILPACK; build
  `pnpm install --frozen-lockfile && pnpm -F @is/tokens build && pnpm -F studio-suite-web build`;
  start `npx --yes serve@14.2.6 -s web/build -l tcp://0.0.0.0:$PORT`; `preDeployCommand
  rm -rf node_modules/.vite` (stale npm-era artifact, harmless — strip if ever touching the file).
- **CI** (`.github/workflows/ci.yml`): web job is pnpm-aware (pnpm setup → root install → build
  `@is/tokens` → build + lint web). Backend job (ruff + pytest) untouched. PR #3 checks: all green
  (web build 30s, backend 15s).
- **pnpm pinned 10.34.3** (root `packageManager`). pnpm 11 needs Node ≥22.13; this env/CI/Railway runs
  Node ≤20, so **do not bump pnpm to 11** without first moving Node ≥22.

---

## 6. Carried fragilities / watch-items (none fix-now)

- **esbuild build scripts ignored under pnpm 10 default-deny** (`Ignored build scripts: esbuild@…`).
  Benign now (Vite/tsup ship their own binaries). IF a deploy ever fails on a missing esbuild binary →
  `pnpm approve-builds` or add `pnpm.onlyBuiltDependencies: ["esbuild"]` to root `package.json`.
- **Node resolved to 18.20.8** on Railway (from `engines.node >=18`). If 01.0.1b pulls a dep needing
  Node ≥20, raise the engines floor deliberately and re-confirm Railway/CI agree.
- **corepack `EBADENGINE` on Node 18** — cosmetic warning only; pnpm activates fine. Ignore.
- **Dependabot**: 3 alerts on `main` (1 high / 1 moderate / 1 low). **Parked for a deliberate own pass**,
  never folded into a feature merge. Queue after 01.0.1b, before/around mobile work.
- **Codex branch `979e1da`** deferred; gets its own pass, never auto-merged.

---

## 7. Open thread carried forward (non-blocking)

The **direct devtools var check** (`document.body[data-theme="light"]`, `:root` carrying `--surface-*`
/ `--brand-gold` on the deployed bundle) was **not** confirmed by eye this session. Mounting is proven
**indirectly** (0-px diff + clean live render + `ThemeProvider` in `main.jsx`). 01.0.1b exercises the
vars directly, which closes this loop for real. If you want the explicit check, glance at live `main`'s
`:root` for `--brand-gold` — otherwise it carries.

---

## 8. NEXT TASK — 01.0.1b (the pixel-faithful landing rebuild)

Pin off **`0ded334`**. Branch `feature/landing-fidelity` (fresh name — never reuse `feature/tokens-package`).
Scope (ONE concern, gated): rebuild `web/src/pages/Landing.jsx` to be **pixel-faithful to the
design-system** — self-host the five fonts, consume the `@is/tokens` vars (Cormorant/Cinzel type, gold
palette, `#050505`, collage, "SINCE MMXIV", 280+/12YR/40 stats, "Selected Frames"), both themes working,
light default. This is where the landing **visibly changes** — the opposite of 01.0.1a's invariance gate.
Acceptance = fidelity to `design-system/components/ds-*.jsx`, not a diff impression. Author the prompt
cold + verify the design-system source against the repo first (the dual-repo verify rule).

---

## 9. Verify-live block (run at session start before authoring 01.0.1b)

```bash
kstart
cd ~/kingdom/projects/studio-suite
git fetch origin
git status --short                 # expect clean
git log --oneline -3               # expect tip 0ded334 "Feature/tokens package (#3)"
git rev-parse HEAD origin/main     # expect both = 0ded334
git branch -a                      # expect main, origin/main, origin/codex/... ONLY (no feature/*)
git log --oneline -1 origin/codex/set-up-automated-git-workflows-with-codex   # expect 979e1da (deferred)
git -C ~/kingdom log --oneline -1  # kingdom-docs tip (advanced by this baseline's commit)
# web live (main): the Railway web-service URL — expect GET / → 200, assets resolve
```

If `origin/main` ≠ `0ded334`, STOP — Codex or owner direct-to-main moved it; diagnose before branching.

---

## 10. Standing rules (unchanged — orchestrator prompt governs in full)

git diff is truth over CC prose; pin bases to a SHA; one cold-authored prompt per task; `/automate-dev`
line one; file approval option 1; stage by explicit path, commit per concern, never `git add -A`; infra
surfaced as owner decision; green build ≠ renders (verify live); security-critical work not pushed past
~70–80% context; `/clear` not `/compact`; continuation baseline committed in isolation at every clean
boundary. **The owner is the only relay to the machine; every irreversible step is owner-gated.**
