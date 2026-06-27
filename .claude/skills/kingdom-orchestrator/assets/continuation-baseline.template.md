---
title: "Kingdom continuation baseline"
version: "<ISO8601 datetime — the real close time>"
supersedes: "<filename of the prior kingdom-continuation-*.md>"
status: "AUTHORITATIVE STATE. Newest file wins on live facts. Committed in isolation."
machine_checkpoint_ref: "knowledge/projects/kingdom.state.md @ <SHA or note>"
owner: "TechCorp"
---

# Kingdom continuation baseline — <ISO8601>

> Source of truth on **live facts**. The live `knowledge/policies/` win on **rules**; the skill wins on
> **how to operate**. Commit this file ALONE, by explicit path.

## 0. State at close
- Kingdom `main` tip: `<SHA>` (`git log --oneline -1` output)
- In-flight branch(es): `<branch> @ <SHA>` — or "none, tree clean"
- Open PRs: `<#num — title — draft/ready>` — or "none"
- Machine checkpoint (`kingdom.state.md`): last gate `<pass/fail>`, written `<ISO8601>` — **verified by raw output? yes/no**

## 1. Remaining work items
- [ ] `<item — what, where, why>`
- [ ] `<item>`

## 2. Known issues + verification status
- `<issue>` — **<runtime-verified | grep-only / NOT runtime-verified | unverified>**. `<detail / what would close it>`

## 3. Pending owner decisions
- `<decision needed>` — framed question + the orchestrator's reasoned recommendation: `<…>` (relay to: `<who>`)

## 4. Knowledge base / registry state
- `knowledge/global/_proposals/`: `<staged proposals awaiting owner-gated git mv>` — or "empty"
- Policies changed this session: `<which, and what they now say>` — or "none"
- `.claude/` automation touched: `<hooks/settings/skills + decision-record ref>` — or "none"
- Project registry: `<projects registered/changed>` — or "no change"

## 5. Standing rules carried forward
- `<any session-specific standing rule or caveat the next session must honour>`

## 6. Re-entry pointer
Next session: read the skill → read live `knowledge/policies/` + `operating-contract.md` in full → re-derive
facts → run §5 startup; confirm `main` tip == `<SHA>` above. If it differs, another committer landed work —
reconcile before starting. Paired handoff: `<ISO8601>-kingdom-orchestrator-handoff.md`.
