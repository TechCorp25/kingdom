---
title: "Kingdom-environment orchestrator — continuation baseline"
version: "2026-06-28T13-20-00"
supersedes: "none — FIRST baseline in the docs/orchestrator/ series"
corresponds_to: "docs/illuminate-my-gallery/kingdom-continuation-2026-06-28T11-23-06.md (CC build-layer continuation for the same task — separate lane, cross-referenced not superseded)"
status: "AUTHORITATIVE STATE. Newest file wins on live facts. Committed in isolation."
series: "docs/orchestrator/ — orchestrator (claude.ai) lane; distinct from project continuations under docs/<slug>/ and from knowledge/projects/kingdom.state.md"
machine_checkpoint_ref: "knowledge/projects/kingdom.state.md @ verify at next startup"
owner: "TechCorp"
pairs_with: "2026-06-28T13-20-00-kingdom-orchestrator-handoff.md"
---

# Kingdom-environment orchestrator — continuation baseline (2026-06-28T13-20-00)

> Source of truth on **live facts** for the orchestrator layer. The live `knowledge/policies/` win on
> **rules**; the skill wins on **how to operate**. This is the FIRST file in the `docs/orchestrator/`
> series — it does NOT supersede the CC continuation series under `docs/illuminate-my-gallery/` (separate
> lane). Commit this file ALONE, by explicit path. Re-derive every SHA below against raw `git` at startup.

## 0. State at close — CLEAN boundary
- Kingdom `main` tip: **`34c082b`** — "chore(knowledge): promote PR-issue-link clause into operating
  contract (Req 5) (#12)". `main` == `origin/main`, fast-forwarded, tree clean.
- In-flight branch(es): none. `chore/promote-pr-issue-link` squash-merged (PR #12), then deleted
  (local `-D` + remote + pruned tracking ref — all confirmed from raw output).
- Open PRs: the baseline/handoff PR opened at this close (see §6 staging) — draft.
- Machine checkpoint (`kingdom.state.md`): last advanced by PR #11 (`edc8d6e`). **NOT re-derived from raw
  output this session — verify at next startup** (`git log -1 -- knowledge/projects/kingdom.state.md`).

## 1. Remaining work items
- [ ] None carried from this task. Next session starts cleanly from `34c082b`.
- [ ] **Owner action (per docs/orchestrator/README.md):** point `CLAUDE.md → Active Session Baseline` at
      this file (first orchestrator-series baseline). Left to owner — not done silently by this layer.

## 2. Known issues + verification status
- Promoted change is a **doc/governance edit** — nothing to runtime-verify; "live" = present in
  `operating-contract.md` on `main` (confirmed via raw `git show HEAD:` + the squash diff). No grep-only
  caveats outstanding.

## 3. Pending owner decisions
- None blocking. The A-vs-B placement decision was made this session (Option B — see §5).
- The baseline-pointer advancement in §1 is the one optional owner action queued.

## 4. Knowledge base / registry state
- `knowledge/global/_proposals/`: **empty** of task files (only `README.md`). The
  `2026-06-27T10-30-00-operating-contract-pr-issue-link.md` proposal was promoted (deleted on `git mv -f`).
- `knowledge/global/operating-contract.md`: **changed** — Req 5 now carries the PR-issue-link clause
  (Kingdom-repo scope; project repos keep their own per-project issue-link discipline). 49 lines, six
  requirements intact.
- Policies changed: none (`run-close.md` untouched — placement went to the contract, see §5).
- `.claude/` automation touched: none.
- Project registry: no change.
- Decision record: `DR-2026-06-27-pr-issue-link` (placement + scope rationale), referenced by PR #12.

## 5. Standing rules / decisions carried forward
- **PR-issue-link rule is contract-level (Option B, Req 5), not policy-level.** Rationale recorded so a
  future session does not "tidy" it into `run-close.md`: `policies/**` is autonomously CC-updatable, so a
  clause there could be weakened/dropped with no owner in the loop; `global/**` is owner-gated both ways.
  For a rule gating whether a PR may leave draft, that erosion-immunity is decisive. Cost accepted: live
  only on owner `git mv -f` + PR #12 merge.
- **Scope = Kingdom repo only (i)**, mirroring `run-close.md`'s existing "Scope (owner decision: Kingdom
  only)" carve-out. Widening to project repos (ii) is a SEPARATE deliberate decision — must not ride in on
  placement.
- **Two continuation lanes are intentionally separate** (README): orchestrator series in
  `docs/orchestrator/`; CC build-layer series in `docs/illuminate-my-gallery/`. Never supersede across
  lanes even though the `kingdom-continuation-*` names rhyme.
- The owner's standing CLAUDE.md Flask/Mongo stack governs **projects**, not the Kingdom control plane
  (uv + FastAPI + PostgreSQL + SQLAlchemy async). Do not conflate.

## 6. Re-entry pointer
Next session: read the skill → read live `knowledge/policies/` + `operating-contract.md` in full
(**Req 5 now includes the issue-link clause**) → re-derive facts → run §5 startup; confirm `main` tip ==
**`34c082b`**. If it differs, another committer landed work — reconcile first. Verify machine-checkpoint
freshness (§0). Paired handoff: `2026-06-28T13-20-00-kingdom-orchestrator-handoff.md`.

## 7. Gotchas that bit this run (carry forward)
- **Resolve the live baseline filename + series directory from `ls`/`git log` BEFORE writing a
  continuation — never from prior-context/project-knowledge memory.** This session twice staged toward a
  stale "newest baseline" SHA (`043a7e0`) and the wrong series dir (`docs/illuminate-my-gallery/`); the
  live `ls` caught both. Derive from the tree, not from memory.
- **`git mv -f` of a full-copy proposal shows the proposal's whole length as DELETIONS** in the commit
  summary (here `50 deletions`) — that is the source file being removed, NOT the contract being gutted.
  Read the per-file diff (`git diff HEAD~1 HEAD -- <contract>`), not the summary line, before alarming.
- **Promoting an EXISTING global file needs `git mv -f`** — bare `git mv` aborts (target exists).
- **`block-global-bash.sh` is heuristic:** a redirect (`>`, `2>/dev/null`) on a line that also names a
  non-`_proposals/` global path trips the gate even on a pure read — pipe to `grep` instead.
- **Squash-merged branch is a non-ancestor** — `-D` the stale local branch, prune the remote ref, never
  reuse the name.

---
*Filename: kingdom-continuation-2026-06-28T13-20-00.md (docs/orchestrator/ — FIRST in series).*
*Supersedes: none. Corresponds to CC continuation docs/illuminate-my-gallery/...2026-06-28T11-23-06.md.*
*Kingdom `main @ 34c082b` (clean, pushed). Lineage 4e7930a(#10) → edc8d6e(#11) → 34c082b(#12), intact.*
*PR #12 squash-merged + branch deleted. PR-issue-link rule live at contract Req 5, Kingdom-only.*
*Next update on session close: kingdom-continuation-YYYY-MM-DDTHH-MM-SS.md*
