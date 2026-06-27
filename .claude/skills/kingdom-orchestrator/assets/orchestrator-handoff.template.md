---
title: "Kingdom-orchestrator handoff"
for_session_after: "<ISO8601 — close time of the baseline this pairs with>"
pairs_with_baseline: "kingdom-continuation-<ISO8601>.md"
handoff_type: "<clean-boundary | MID-TASK>"
---

# Kingdom-orchestrator handoff — <ISO8601>

## 0. Type & first thread
- **Type:** `<clean-boundary | MID-TASK>`
- If **MID-TASK**: the single open thread to resume FIRST is: `<exact thread + where it stopped + why>`.
- If **clean-boundary**: no open thread; start from the work queue in the baseline §1.

## 1. How to operate (unchanged unless noted)
- You are the Kingdom-**environment** orchestrator: governance + decision + review, **no terminal**. The owner
  relays every machine action; every irreversible step is owner-gated. Peer to project orchestrators — never
  reach into project product code.
- Frame as task + operating context + explicit verification. Never persona.
- Files, not copy-paste, for everything handed to the owner.

## 2. Do first
1. Read this handoff, then the newest `kingdom-continuation-*.md` (state of truth).
2. Read live `knowledge/policies/` + `knowledge/global/operating-contract.md` in full.
3. Re-derive `references/kingdom-facts.md` against raw owner output; run the §5 startup; confirm `main` tip ==
   the baseline's expected SHA.

## 3. Watch-outs carried in
- `<any grep-only/runtime-unverified caveat, dirty-tree note, or in-flight branch that needs care>`

## 4. State-of-truth pointer
The newest `kingdom-continuation-*.md` is authoritative on facts; the live `knowledge/policies/` on rules; the
skill on how to operate. This handoff only tells you how to re-enter.
