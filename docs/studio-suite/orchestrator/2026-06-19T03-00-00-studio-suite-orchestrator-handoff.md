---
title: "studio-suite — orchestrator handoff (next chat)"
version: "2026-06-19T03-00-00"
pairs_with: "studio-suite-continuation-2026-06-19T03-00-00.md"
project: "studio-suite (new app dev) · Kingdom workspace"
owner: "TechCorp (solo developer, Melbourne AU)"
boundary: "MID-FLIGHT — gold-fix closed on main (2014e2b); resume at the 01.0.1b landing close-out"
---

# studio-suite — orchestrator handoff (2026-06-19T03-00-00)

## 0. How to use this pair

Two files produced at this boundary:
- **`studio-suite-continuation-2026-06-19T03-00-00.md`** — state-of-truth (facts, SHAs, the brass
  correction, the open ledger, fragilities, verify-live). **Read it first.**
- **This handoff** — how to operate + what to do first.

**This is a MID-FLIGHT boundary.** The gold-fix task is closed and squashed to `main` (`2014e2b`), so
there is nothing uncommitted — but the broader 01.0.1b landing work is **parked** (PR #4). The single open
thread to resume first is the **01.0.1b close-out** (continuation §4). Do not start anything in §5 until
01.0.1b is squashed.

## 1. You are the relay/review layer

No terminal, no Railway, no git. The owner runs everything and pastes raw output; you re-derive from git/log
output (never CC prose), recommend with reasoning, flag inconsistencies, and gate every irreversible step.
Anything CC-bound is a downloadable `.md` (point CC at the file, never paste — unicode corrupts on mobile).
Diagnostics for the owner are downloadable `.sh`. The orchestrator system prompt governs how to operate in full.

## 2. First actions, in order

1. **Read the continuation baseline in full.** §2 (brass correction) and §3/§4 (landing state + the resume
   sequence) are load-bearing.
2. **Run the §8 verify-live block.** Confirm `main` = `2014e2b`, tree clean, `feature/landing-fidelity`
   (`0e834d5`) still present, Codex `979e1da`. If `origin/main` moved or PR #4's branch is gone, STOP.
3. **Resume the 01.0.1b close-out** (baseline §4): rebase the landing branch onto `2014e2b` first — do not
   author anything new until that rebase + a fresh visual check is in hand.

## 3. The immediate task — 01.0.1b close-out (baseline §4)

Owner rebases `feature/landing-fidelity` onto `main` `2014e2b` (clean — disjoint files), rebuilds, and
visual-checks light. The brass token change should auto-correct deltas #1 ('quietly extraordinary' gold) and
#3 (gold-fill buttons) **if** `landing.css` consumes `var(--brand-gold)`; any residual champagne = a
hardcoded literal to rewire. Then **one cold polish prompt** off the rebased tip: button sizes (#2), the
footer (inert), the 826 KB logo (SVG hunt / compress). Re-gate visually vs the design-system in **brass**,
light AND dark. Then squash 01.0.1b → `main`.

**Before authoring the polish prompt:** verify the rebased `landing.css` / `Landing.jsx` and the design-system
`.btn` values against the connected repos (the dual-repo verify rule). Expected diff stays `web/**` only.

## 4. What you do NOT touch for 01.0.1b polish

`packages/tokens/**` (brass is correct and landed — do not reopen it), `railway.toml`, `ci.yml`,
`pnpm-workspace.yaml`, `backend/**`, `main.jsx`, `index.css`, `tailwind.config.js`. If the logo or anything
else seems to need a package/infra change, surface it owner-gated; do not let CC edit infra silently.

## 5. Then (queued — baseline §5)

01.0.2 responsive landing (NEW design layer — needs mobile breakpoints specced by owner/dev team first; the
landing is desktop-fixed and clips on mobile, the primary client viewport) · live theme toggle (additive
`@is/tokens` setter; owner-gated package change) · Dependabot pass (4 alerts, 1 high) · `ds-shots/` committed
reference renders (would have caught the gold off-by-one at authoring).

## 6. Session-close protocol (when 01.0.1b reaches its clean boundary)

Commit at the boundary → produce `studio-suite-continuation-<ISO>.md` superseding THIS baseline (record the
new `main` SHA, update kingdom-docs SHA, carry forward §5/§6/§7) → commit it in isolation → produce the paired
handoff → `/clear`. Filename timestamp = real close time.

## 7. Standing reminders

git diff is truth; pin bases to a SHA; verify claims against both repos before asserting; `/automate-dev` line
one; file approval option 1; stage by explicit path, never `git add -A`; green build ≠ renders (verify live,
both themes, **and mobile** now that it's a known gap); tokens are the single colour source — never hardcode
gold in web; `/clear` not `/compact`; Dependabot and Codex stay parked; every push and merge is owner-gated.
