---
title: "studio-suite — orchestrator handoff (next chat)"
version: "2026-06-22T19-30-00"
pairs_with: "studio-suite-continuation-2026-06-22T19-30-00.md"
project: "studio-suite (new app dev) · Kingdom workspace"
owner: "TechCorp (solo developer, Melbourne AU)"
boundary: "CLEAN PIVOT — 01.0.1b abandoned (superseded). Next-gen design-system reset begins at T1."
---

# studio-suite — orchestrator handoff (2026-06-22T19-30-00)

## 0. How to use this pair
- **`studio-suite-continuation-2026-06-22T19-30-00.md`** — state-of-truth (the pivot, ratified architecture,
  git SHAs, the reset ledger, the responsive gate, parked items). **Read it first, in full.**
- **This handoff** — how to operate + what to do first.

This is a **CLEAN PIVOT** boundary, not a resume. The prior 01.0.1b landing close-out is deliberately
**abandoned** — do not pick it up. The new line is the next-gen design-system reset; the first task is **T1**.

## 1. You are the relay/review layer
No terminal, no Railway, no git. The owner runs everything and pastes raw output; you re-derive from
git/log/diff output (never CC prose), recommend with reasoning, flag inconsistencies, gate every irreversible
step. CC-bound work = downloadable `.md` (point CC at the file; never paste — mobile corrupts unicode).
Owner diagnostics = downloadable `.sh`. The orchestrator system prompt governs how to operate in full.

## 2. First actions, in order
1. **Read the continuation baseline in full.** §4 (the pivot + PR #4 seed guard) and §5 (the ratified
   architecture + reset ledger) are load-bearing.
2. **Run the §8 verify-live block.** Confirm `main` = `2014e2b`, tree clean, **`feature/landing-fidelity`
   (`0e834d5`) still present** (it is the landing seed — its absence is a STOP), kingdom-docs at this
   baseline's commit, preview 200, bundle scratch present (re-unzip from `~/studio-suite/update-design-system.zip`
   if gone). If `origin/main` moved, STOP and inspect with `git show --stat`.
3. **Begin T1** (ratify & scope). Do NOT author any T2+ build prompt until T1 resolves the `contracts/`/`policy/`
   placement and the responsive acceptance gate is written down concretely.

## 3. Boundary actions still outstanding for the owner (this pivot)
- **Close PR #4 UNMERGED** (GitHub, owner-gated) with a note that it's superseded by the design-system reset.
  **Do NOT delete `feature/landing-fidelity`** — it holds the only copy of `web/src/pages/Landing.jsx`, the T5 seed.
- **Commit this baseline + handoff** to kingdom-docs (baseline in `docs/studio-suite/`, this file in
  `docs/studio-suite/orchestrator/`), staged by explicit path, then push. That advances kingdom-docs off `ddf05c5`.
- Optional, non-blocking: the stale `fix/tokens-light-gold-brass` verified-safe cleanup.

## 4. The bundle (context for T1/T2)
Lives read-only at `~/ds-incoming-review/illuminate-design-system/` (scratch; source zip
`~/studio-suite/update-design-system.zip`). It is **NOT in the repo** and must not be unzipped into the working
tree as adoption — T2 brings it in deliberately, placed + globally renamed (Illuminate → studio-suite) + triaged.
Resolved brand-gold base already matches `main` (brass light / champagne dark) — no colour migration.

## 5. Ratified architecture (locked this session — see baseline §5)
Gradients-in-tokens (scoped to brand/semantic; plain-CSS consumption, never Tailwind arbitrary-value vars) ·
two-ramp gold (zero visual delta) · scale-var CSS system · **fluid viewport-and-orientation responsive on web as
a HARD gate** (continuous range + both orientations; iPhone 13 mini as small-end gate; validated on
`qa/responsive-harness.html`; no dead-zones) · shared-token contract → native (Architecture B; confirm responsive
is scale-driven at T2/T3).

## 6. Standing reminders
git diff is truth; re-derive from raw output; verify against both repos before asserting; `/automate-dev` line
one; file approval option 1; stage by explicit path (never `git add -A`); files-not-paste; green build ≠ renders
— and "renders" now means fluid across the range + both orientations on the harness; tokens are the single colour
source (brand gradients now in tokens, plain-CSS consumed); `/clear` not `/compact`; Dependabot + Codex stay
parked; every push, merge, and PR close is owner-gated.

---
*Pairs with studio-suite-continuation-2026-06-22T19-30-00.md. Pivot boundary — begin at T1.*
