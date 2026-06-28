---
title: "Kingdom-environment orchestrator — handoff"
version: "2026-06-28T13-20-00"
pairs_with: "kingdom-continuation-2026-06-28T13-20-00.md"
series: "docs/orchestrator/ — orchestrator lane (distinct from docs/<slug>/ project lanes)"
boundary: "CLEAN — PR-issue-link rule promoted to operating contract, merged (#12), main re-pinned"
owner: "TechCorp"
---

# Kingdom-environment orchestrator — handoff (2026-06-28T13-20-00)

State-of-truth is the paired baseline (`kingdom-continuation-2026-06-28T13-20-00.md`, in
`docs/orchestrator/`). This file is **how to operate + what to do first**; the baseline holds the facts.

## 0. Boundary type
**CLEAN.** Not mid-task. The PR-issue-link task is fully closed: owner `git mv -f` promotion →
squash-merge (PR #12) → `main` re-pinned to `34c082b` → branch deleted. No open thread to resume; the
next session starts fresh.

## 1. How this layer operates (the essentials)
- Environment governance layer on claude.ai. **No terminal**; the owner is the sole relay — runs every
  command, pastes raw output; this layer reasons over it and gates irreversible steps.
- **Peer** to project orchestrators; never touches a project's application code (separate repos, carved
  out of Kingdom auto-push).
- Re-derive from raw `git`/gate output; never trust prose or prior-context memory. "Committed locally" ≠
  on `main`; green gate ≠ runtime-correct; grep-confirmed ≠ runtime-confirmed.
- Everything handed to the owner is a **downloadable file**, never copy-paste.
- Global knowledge is owner-gated: `_proposals/` + hand `git mv -f`. A hook block is the protection
  working — route around via the queue, never by disabling it.

## 2. First actions next session (self-bootstrap — before any task)
1. Read the skill, then the live `knowledge/policies/` + `knowledge/global/operating-contract.md` in
   full. **Heads-up:** Req 5 now carries the PR-issue-link clause added this session — it is live.
2. Re-derive environment facts against raw owner output.
3. Run the §5 startup (owner pastes `git fetch` / `branch -a` / `log --oneline -3`). Confirm `main` tip
   == **`34c082b`**. A different tip = another committer landed work → reconcile first.
4. **Resolve live filenames from the tree, not memory:** before writing any continuation, run
   `ls -1t docs/orchestrator/kingdom-continuation-*.md` to get the real newest baseline + its series dir.
   (This session lost time staging toward a stale SHA and the wrong directory — the live `ls` is truth.)
5. Verify machine-checkpoint freshness (`git log -1 -- knowledge/projects/kingdom.state.md`).

## 3. What landed this session
- New rule: every PR on the **Kingdom** repo links its tracking issue (not eligible to leave draft);
  project repos keep their own discipline. Placed at **operating contract Req 5** (Option B), Kingdom-only.
- Why contract-level not policy-level: erosion-immunity (owner-locked both ways). Full rationale in
  baseline §5 and `DR-2026-06-27-pr-issue-link`. Do NOT relocate it into `run-close.md`.
- Files: `knowledge/global/operating-contract.md` (+clause); proposal removed from `_proposals/`.
  PR chain: #10 propose → #11 prior CC close-out → #12 promote.

## 4. Gotchas that bit this session (also in baseline §7)
- A `git mv -f` of a full-copy proposal shows the proposal's whole length as *deletions* in the commit
  summary — the source file being removed, NOT the contract gutted. Read the per-file diff before alarming.
- Promoting an existing global file needs `git mv -f` (bare aborts).
- `block-global-bash.sh` trips on a redirect (`2>/dev/null`) next to a global path even on a pure read —
  pipe to `grep`.
- Two continuation lanes are separate by design (orchestrator vs CC) even though names rhyme — never
  cross-supersede.

## 5. Pending owner action (optional, not blocking)
Per `docs/orchestrator/README.md`, point `CLAUDE.md → Active Session Baseline` at this baseline (first in
the orchestrator series). Left to the owner — this layer does not repoint it silently.

## 6. Next action
Nothing pending. Await the owner's next task; begin with §2 self-bootstrap regardless of opener phrasing.
