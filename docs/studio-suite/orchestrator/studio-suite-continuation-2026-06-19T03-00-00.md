---
title: "studio-suite — continuation baseline (state-of-truth)"
version: "2026-06-19T03-00-00"
supersedes: "studio-suite-continuation-2026-06-17T04-38-29.md"
pairs_with: "2026-06-19T03-00-00-studio-suite-orchestrator-handoff.md"
project: "studio-suite (new app dev) · Kingdom workspace"
owner: "TechCorp (solo developer, Melbourne AU)"
boundary: "gold-fix CLOSED on main; 01.0.1b landing MID-FLIGHT (PR #4 parked for rebase→polish→squash)"
---

# studio-suite — continuation baseline (2026-06-19T03-00-00)

This file is authoritative state. Where it and the orchestrator system prompt overlap, **this wins on
facts; the prompt wins on how to operate.** Read it first, then the paired handoff. Every SHA/branch
fact below was re-derived from the owner's raw git output this session — but it is NOT a live checkout;
re-run §8 at session start before acting.

---

## 0. What just happened / boundary type

- **Gold-fix task CLOSED clean.** Squash-merged to `main` (PR #5). `main` = `2014e2b`. This corrected a
  latent `tokens.ts` bug — light brand-gold was champagne, should always have been brass (§2).
- **01.0.1b landing is MID-FLIGHT, not closed.** `feature/landing-fidelity` (PR #4) is built, reviewed,
  and **parked open** — it does NOT merge until rebased onto the new `main`, polished, and re-gated (§3, §4).
- So: clean on gold (nothing uncommitted), but the **single open thread to resume first is the 01.0.1b
  close-out (§4).** Everything in §5 is queued behind it.

---

## 1. Pinned git state (re-derive via §8 before trusting)

- **studio-suite `main` = `origin/main` = `2014e2b`** — "fix(tokens): correct light brand.gold to brass
  #a8884f (#5)". Fast-forwarded from `0ded334`.
- **Open branch `feature/landing-fidelity` = `0e834d5`**, forked off `0ded334`, pushed, **PR #4 OPEN/parked**.
  Its file set (`web/**`) is **disjoint** from the gold change (`packages/tokens/**` + design-system docs),
  so it **rebases cleanly** onto `2014e2b`.
- **Codex** `origin/codex/set-up-automated-git-workflows-with-codex` = `979e1da` — deferred, do NOT merge.
- **kingdom-docs**: prior tip `3f61216`; **advances when these two artifacts are committed.**
- **Dependabot**: 4 alerts on `main` (1 high / 1 mod / 2 low) — parked for its own pass (§5).

**Infra ids (verified from Railway deploy logs):** project `543da574-8060-43be-a666-a7e107e34c51`;
web service `a3b1e95d-d9ea-41b9-92c8-15c7f71c2837` (serves from `main`, host
`studio-suite-preview.up.railway.app`); backend service `ad5561ce-2407-488d-b14a-88c4cc6a4e7f`
(Mongo db `illuminate_studios`, `/api/health` 200).

---

## 2. The brass correction (now canonical) — tokens are single colour source

`design-system/scripts/tokens.ts` is canonical. Its light `brand.gold` referenced the wrong palette index
(`gold[300]` champagne `#c9a96e`) while its own comment said "brass" and BOTH `illuminate-design-spec.json`
and `styles.css` specified brass `#a8884f`. Corrected (light only):

- `brand.gold`: `gold[300]` → **`gold[400]` (`#a8884f` brass)**
- `brand.goldHover`: `gold[200]` → **`gold[300]` (`#c9a96e` champagne — in-ramp; doubles as the named
  alternate for a fast client champagne-reship: flip this one index back)**
- `brand.goldMuted`: unchanged (already brass-based rgba)
- `border.gold`: unchanged (`gold[400]` `#a8884f` — spec has brand==border gold in light)
- **Dark theme UNCHANGED** — dark `brand.gold` stays `gold[300]` `#c9a96e` (champagne reads better on near-black).

Both byte-identical `tokens.ts` copies (`design-system/scripts/` + `packages/tokens/src/`) and the
`ds-foundations.jsx` doc table (both `brand.gold` and `brand.goldHover` Light cells) were corrected.
`packages/tokens/dist` is **gitignored** (CI rebuilds). `@is/tokens` emits colour-only namespaced vars
(`--surface-*`, `--border-*`, `--ink-*`, `--brand-gold[-hover/-muted]`, `--scrim`) — no type vars, no
utility classes, no gradients; those live web-local in `landing.css` (the Option A bridge).

---

## 3. The landing (01.0.1b) — built state on PR #4 (champagne build)

Faithful **desktop** rebuild, **scope-1**: Topnav (ThemeToggle omitted — no setter yet) → HeroSection →
PortfolioStrip, page ends at Selected Frames. Light default. Fonts self-hosted via 4 fontsource packages
(`cinzel`, `cormorant-garamond` incl. 400-italic, `inter`, `jetbrains-mono`). Logo via theme-swapped
banner PNGs (**826 KB total — flagged for compression/SVG**). `landing.css` = additive Option A layer
(fonts + type vars + ported utility classes + gold gradients; colours via `@is/tokens` vars). Diff = 6 files.
CI green; served preview verified from Railway logs (GET / 200, all assets 200, no 404s).

**Owner visual review (on the champagne build):** light / fonts / colour / shadows faithful; page ends
cleanly after the 6-grid (no clip — the scope-1 boundary). Three deltas:
- **#1 'quietly extraordinary' gold** + **#3 gold-fill buttons lighter** = the champagne-vs-brass fork.
  Should **auto-resolve on rebase onto brass `main`** IF `landing.css` consumes `var(--brand-gold)`; if
  either is still champagne after rebuild, it is a hardcoded literal in `landing.css` → rewire to the var.
- **#2 button sizes** larger than the design-system `.btn-lg`/`.btn-sm` → a genuine web delta, fixed in polish.
- **Footer** absent (scope-1 excluded it). Agreed to **add it, inert**, in the polish pass.

---

## 4. RESUME FIRST — 01.0.1b close-out (the only mid-flight thread)

In order, all owner-gated:
1. **Rebase `feature/landing-fidelity` onto `main` `2014e2b`** (clean — disjoint files). Rebuild → web gold
   auto-corrects to brass.
2. **Visual re-check** light: confirm #1 and #3 now render brass. Any residual champagne = hardcoded literal
   in `landing.css` → rewire to `var(--brand-gold)` (additive, app-code only).
3. **Polish pass** on the rebased branch:
   - button sizes (#2) to match the design-system `.btn` values exactly;
   - **footer** — render faithfully but **inert** (placeholder links, NO newsletter/admin/backend wiring,
     same rule as the nav);
   - **logo 826 KB** — check `design-system/assets` for an SVG/vector lockup; if none, resize+compress the
     PNGs to display size before they enter `main` history permanently.
4. **Visual gate** vs design-system (now **brass**), light AND dark (dark via temporary `defaultTheme="dark"`
   rebuild, reverted before commit — the proven method; `main.jsx` unchanged in the final diff). Owner-reviewed.
5. **Squash 01.0.1b → `main`**, delete branch, production redeploys.

> Authoring rule for the polish prompt: one cold CC prompt, off the rebased branch tip, verified against the
> repo first. Expected diff stays `web/**` only (Landing.jsx, landing.css, maybe assets) — no `packages/tokens`,
> no infra. If the logo SVG hunt or anything else implies a package/infra touch, surface it owner-gated.

---

## 5. Queued (after 01.0.1b squashes)

- **01.0.2 — responsive landing.** A **new design layer, not a bug fix.** `design-system/components/landing.jsx`
  is a fixed-desktop composition with no breakpoints, so on mobile the header is partially cut off and body
  content squashes (mobile is the primary client viewport). Responsiveness is net-new design the source does
  not specify — **mobile behaviour must be decided/specced by owner+dev team before authoring** (target
  breakpoints; how the hero two-column stacks, the collage, the stat row, the nav). Do NOT let CC improvise it.
- **Live theme toggle** (was "01.0.1c"). `@is/tokens` `useTheme()` exposes no setter (the context holds
  `setTheme` but it is not exported). A live toggle needs a small **additive** package export (e.g.
  `useThemeControls`; leave `useTheme` unchanged). Owner-gated package change. Pull forward only if live
  dark-switching is needed to ship; otherwise bundle with mobile theme needs.
- **Dependabot pass** — 4 alerts (1 high). Own deliberate pass, never folded into a feature merge; bump the
  high up the queue.
- **`ds-shots/`** — committed per-surface reference renders beside the `ds-*.jsx`, so visual gates compare
  against a committed image, not memory. Would have caught the gold off-by-one at authoring. Small docs task.

---

## 6. Carried fragilities (do not relearn)

- **pnpm workspace is the build reality.** Railway web service: Root Dir = repo root, config = `web/railway.toml`,
  **no dashboard command overrides** (overrides were the original deploy-failure cause). Railpack detects pnpm
  from root `packageManager` + `pnpm-lock.yaml`. CI web job is pnpm-aware.
- **esbuild build-scripts ignored** under pnpm 10's default-deny — benign; if a deploy ever dies on the esbuild
  binary, fix = `pnpm approve-builds` / `onlyBuiltDependencies`.
- **Node resolves to 18.20.8** on Railway (`engines: >=18`). Flag if anything pulls a 20+ requirement.
- **Vite is in devDependencies** — the build command must include dev deps or it fails `vite: not found`
  (proven OK on the landing build).
- Stack traps from the orchestrator prompt §6 still apply (`from __future__ import annotations` → 422;
  `shadow-[var(--x)]` renders nothing; backend never streams media; etc.).

---

## 7. Standing rules (non-negotiable)

- **Verify before asserting.** Any claim about git state, file existence, prompt contents, or task status is
  checked against both connected repos (search) AND the owner's raw output before being stated or written into
  an artifact. (Established after a prior fabrication was committed to a baseline.)
- **Git diff is truth, not CC prose.** Re-derive every gate from raw output.
- **Many small, individually-gated tasks.** One CC prompt per session, authored cold, verified first.
- **Files not paste** for CC prompts and diagnostics (mobile corrupts unicode). Point CC at the file;
  `/automate-dev` is line one; file approval = option 1 (file-by-file).
- **Stage by explicit path; never `git add -A`.** Commit per concern.
- **Pin review bases to a SHA.** Squash severs ancestry — never reuse a squash-merged branch.
- **Additive-only to `@is/tokens` / shared CSS.** Tokens are the single colour source; never hardcode or
  re-declare colour ramps in `web/`.
- **Green build ≠ renders.** Verify live, both themes, mobile + desktop.
- Every push/merge is owner-gated. `/clear`, not `/compact`.

---

## 8. Verify-live block (run at next session start)

```bash
source kstart
cd ~/kingdom/projects/studio-suite
git fetch origin
git checkout main
git pull --ff-only origin main
git log --oneline -3                 # EXPECT tip: 2014e2b  fix(tokens): correct light brand.gold to brass #a8884f (#5)
git rev-parse HEAD origin/main       # EXPECT both = 2014e2b...
git branch -a                        # EXPECT: main, origin/main, origin/feature/landing-fidelity, origin/codex/...
git log --oneline -1 origin/feature/landing-fidelity   # EXPECT 0e834d5 (PR #4, parked)
git log --oneline -1 origin/codex/set-up-automated-git-workflows-with-codex   # EXPECT 979e1da (deferred)
git -C ~/kingdom log --oneline -1    # kingdom-docs tip (advanced by THIS baseline's commit)
curl -s -o /dev/null -w "%{http_code}\n" https://studio-suite-preview.up.railway.app   # EXPECT 200
```

If `origin/main` ≠ `2014e2b` or PR #4's branch is gone, STOP and diagnose before acting.
