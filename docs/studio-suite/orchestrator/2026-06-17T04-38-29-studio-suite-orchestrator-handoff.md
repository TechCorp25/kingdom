---
title: "studio-suite — orchestrator handoff (next chat)"
version: "2026-06-17T04-38-29"
pairs_with: "studio-suite-continuation-2026-06-17T04-38-29.md"
project: "studio-suite (new app dev) · Kingdom workspace"
owner: "TechCorp (solo developer, Melbourne AU)"
boundary: "CLEAN — 01.0.1a closed; next session opens 01.0.1b"
---

# studio-suite — orchestrator handoff (2026-06-17T04-38-29)

## 0. How to use this pair

Two files were produced at this clean boundary:
- **`studio-suite-continuation-2026-06-17T04-38-29.md`** — the **state-of-truth**. Facts, SHAs, infra
  reality, fragilities, next task. Read it first.
- **This handoff** — how to operate + what to do first.

The orchestrator system prompt (project custom instructions) governs **how to operate** in full. The
continuation baseline governs **facts**. This is a **CLEAN** boundary — 01.0.1a is done; you are
starting a fresh task, not resuming an open thread.

## 1. You are the relay/review layer

No terminal, no Railway, no git. The **owner** runs everything and pastes raw output; you re-derive
from git/log output (never CC prose), recommend with reasoning, flag inconsistencies, and **gate every
irreversible step**. Anything CC-bound is delivered as a **downloadable `.md`** (never copy-paste —
unicode corrupts on mobile). CC prompts are pointed-to by file, not pasted.

## 2. First actions, in order

1. **Read the continuation baseline in full.** §5 (pnpm/Railway infra) and §6 (fragilities) are the
   load-bearing parts — the prior session spent most of its cost there; do not relearn it.
2. **Run the §9 verify-live block.** Confirm `main` = `0ded334`, tree clean, only `main`/`origin/main`/
   `origin/codex/...` branches, Codex still `979e1da`. If `origin/main` moved, STOP and diagnose.
3. **Then author 01.0.1b** — ONE cold prompt, verified against the repo first.

## 3. The task — 01.0.1b (pixel-faithful landing rebuild)

Pin off `0ded334`. Branch `feature/landing-fidelity` (**never** reuse `feature/tokens-package` — it is
a squash-severed non-ancestor, fully deleted). Rebuild `web/src/pages/Landing.jsx` to be pixel-faithful
to the design-system: self-host the five fonts, consume the `@is/tokens` namespaced vars, both themes,
light default. This is the task where the landing **visibly changes** (the inverse of 01.0.1a's
invariance gate). Acceptance = fidelity to `design-system/components/ds-*.jsx`, not a diff impression.

**Before authoring:** verify the design-system source (`ds-*.jsx`, fonts, the exact type/colour/spacing
tokens) against the connected repo via project/repo search — the dual-repo verify rule. The web is
JavaScript and consumes the **compiled** `@is/tokens`; do not introduce TS into web.

## 4. Infra you do NOT need to touch for 01.0.1b (already proven)

The pnpm workspace + Railway pipeline is live and green. 01.0.1b is app-code + fonts + CSS only — no
`railway.toml`, `ci.yml`, or workspace changes expected. If 01.0.1b somehow needs an infra change
(e.g. a font-loading build step), surface it as an owner-gated decision; do not let CC silently edit
infra. Watch the §6 fragilities only if a build behaves oddly (esbuild scripts; Node 18 floor).

## 5. Session-close protocol (when 01.0.1b reaches a clean boundary)

Commit at the boundary → produce `studio-suite-continuation-<ISO8601>.md` superseding THIS baseline
(record the new `main` SHA, update kingdom-docs SHA, carry forward unresolved fragilities) → commit it
in isolation → produce the paired handoff → `/clear`. Filename timestamp = real close time.

## 6. Standing reminders

git diff is truth; pin bases to a SHA; `/automate-dev` line one; file approval option 1; stage by
explicit path; never `git add -A`; green build ≠ renders (verify live on both themes); `/clear` not
`/compact`; Dependabot (3 on `main`) gets its own deliberate pass, never folded into a feature merge;
Codex branch stays deferred. Every push and merge is owner-gated.
