---
title: "Decision record — <short title>"
id: "DR-<ISO8601>"
status: "<proposed | accepted | superseded>"
domain: "<knowledge-base | policy | .claude-automation | hygiene | cross-project | dependency | other>"
owner_gated: "<yes — awaiting owner | approved by owner on ISO8601>"
supersedes: "<DR id or 'none'>"
---

# DR-<ISO8601> — <short title>

## Context
`<What surfaced, where, and why a decision is needed now. Cite the raw evidence — git/gate/grep output, a
policy clause, a hook block — not an impression.>`

## Options considered
1. **<option A>** — `<trade-offs>`
2. **<option B>** — `<trade-offs>`

## Decision
`<The chosen option, stated as an intentional change. If it changes a documented constraint (stack version, a
policy, a hook), say so explicitly — this is a deliberate change, gated individually, not a hygiene fix.>`

## How it lands (intentional-change path)
- Additive to global knowledge? → staged in `_proposals/`, promoted via owner-gated `git mv`.
- Infra/automation file touched? → surfaced here as a decision; not silently edited.
- Verification: `<runtime-verified | grep-only (note it) | gate re-run by script>`.

## Cross-boundary relay (if any)
`<Framed question + reasoned recommendation for the owner to relay to: who.>`

## Consequences
`<What changes for future sessions / project orchestrators / the baseline. What the next session must honour.>`
