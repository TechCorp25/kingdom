---
title: Kingdom control-plane — continuation (PR-issue-link rule close-out)
version: 2026-06-28T11-23-06
supersedes: >
  docs/illuminate-my-gallery/kingdom-continuation-2026-06-13T13-00-00.md as the latest
  Kingdom CC continuation. NOTE: CLAUDE.md "Active Session Baseline" is intentionally
  left pointing at the 2026-06-13 file — advancing the baseline pointer is left to the
  owner / claude.ai-orchestrator layer (see Governance note §0). Where this conflicts
  with an older control-plane note, this wins.
repo: ~/kingdom  (git@github.com:TechCorp25/kingdom.git)
branch: chore/closeout-pr-issue-link-rule  (close-out → draft PR #11 for squash-merge)
state: PR #10 merged (PR-issue-link rule STAGED, not live); awaiting owner `git mv -f` promotion.
---

# Kingdom control-plane continuation (2026-06-28)

Close-out for the "every PR links an issue" governance rule. It is on `main` as a
**proposal** (Option B) but **not live** — promotion is the one owner-gated step left.

## 0. Governance note (why this file is HERE and not in docs/orchestrator/)
`docs/orchestrator/` is reserved for **claude.ai-orchestrator-scaffolded + owner-committed**
baselines (`docs/orchestrator/README.md`), and the CLAUDE.md baseline repoint to that series
was deliberately deferred to the orchestrator layer. So this CC Req-6 handover lives in the
established Kingdom CC series (`docs/illuminate-my-gallery/`) and does **not** repoint
CLAUDE.md. A first attempt that placed it under `docs/orchestrator/` + did the repoint was
backed out as a layer overreach (governance precedent wins). → `knowledge/policies/global-approval.md`,
memory `kingdom-orchestrator-and-audit-prs`.

## 1. Git state (verify before trusting — SHAs are last-observed)
- Branch this run: `chore/closeout-pr-issue-link-rule` (Req-3 checkpoint + this continuation;
  pushed as draft PR #11 for squash-merge).
- `origin/main` tip: **`4e7930a`** — `docs(knowledge): propose PR-issue-link clause … (#10)`.
- Squash-merged this session: **PR #10 = `4e7930a`** (proposal artifact landed on main).
- Already cleaned up: `main` ff `c6e1038 → 4e7930a`; stale local branch
  `chore/pr-issue-link-rule` (was `f68d17c`) force-deleted (squash commit not its ancestor).
- Re-verify:
  ```bash
  cd ~/kingdom && git fetch origin --prune
  git rev-parse --short origin/main          # 4e7930a (later if promotion already merged)
  git log --oneline -5 origin/main
  ```

## 2. What CLOSED this run
- **PR #10 (squash-merged @ `4e7930a`)** staged a full proposed copy of the operating contract
  at `knowledge/global/_proposals/2026-06-27T10-30-00-operating-contract-pr-issue-link.md`.
  Change = one **additive** sentence under **Req 5**: *every PR on the Kingdom repo links its
  tracking issue; a PR with no linked issue is not eligible to leave draft* — **scope (i)
  Kingdom control-plane repo only**. The live `operating-contract.md` was NOT touched (Req 4).
- **Placement decision = Option B** (global proposal) over Option A (policy `run-close.md`):
  policies/** is autonomously CC-updatable, global/** is owner-locked — B makes the rule immune
  to silent erosion by a future autonomous session. Cost accepted: the proposal is **inert until
  the owner promotes it**. DR: `2026-06-27T10-30-00` (pr-issue-link-rule).
- **This close-out branch** added: Req-3 checkpoint (`knowledge/projects/kingdom.state.md`) and
  this Req-6 continuation. No CLAUDE.md change (see §0).

## 3. OPEN workstreams (carried forward)
**A. Promote the rule — make it live. [OWNER-GATED, the one blocker]**
- Status: proposal on `main`, NOT live (live contract has no `issue` clause).
- Decision pending: none — placement (B) + scope (i) settled.
- Next step (owner, own terminal — CC is hook-blocked from self-promoting, Req 4):
  ```bash
  cd ~/kingdom && git checkout -b chore/promote-pr-issue-link
  git mv -f knowledge/global/_proposals/2026-06-27T10-30-00-operating-contract-pr-issue-link.md \
            knowledge/global/operating-contract.md
  git commit -m "chore(knowledge): promote PR-issue-link clause into operating contract (Req 5)"
  ```
  **`-f` required** (destination exists; bare `git mv` aborts). See §6.

**B. Re-checkpoint once live [optional, after A].** Run `knowledge-checkpoint.py --slug kingdom
  --assume-green --summary "PR-issue-link rule promoted/live …"`.

**C. CLAUDE.md baseline pointer [owner/orchestrator decision, deferred].** Still points at the
  2026-06-13 continuation. Advancing it — and whether the authoritative baseline should become a
  claude.ai-orchestrator-scaffolded `docs/orchestrator/` file — is the orchestrator layer's call,
  not CC's. → `docs/orchestrator/README.md`.

**D. This close-out PR #11 [in flight].** Push branch, draft PR exists; owner squash-merges.

## 4. Known untracked / in-flight files (expected, on this branch pre-commit)
- `M knowledge/projects/kingdom.state.md` — Req-3 checkpoint entry (2026-06-28).
- `?? docs/illuminate-my-gallery/kingdom-continuation-2026-06-28T11-23-06.md` — this file.
Committed per-concern; CLAUDE.md is deliberately untouched.

## 5. Verification commands (run at next session start)
```bash
cd ~/kingdom && git fetch origin --prune
git rev-parse --short origin/main                                   # 4e7930a (or later)
git show origin/main:knowledge/global/operating-contract.md | grep -n issue
#   EMPTY = rule NOT yet promoted/live (expected until owner runs git mv -f)
#   match = rule is LIVE (then Workstream B)
git ls-tree origin/main -- knowledge/global/_proposals/            # proposal listed until promoted
uv run ruff check . && uv run mypy && uv run pytest -q             # green: ruff pass · mypy 16 · 11 passed
```

## 6. Standing rules & gotchas (that bit this run)
- **Global is owner-gated (Req 4):** never write `knowledge/global/**` directly; stage in
  `_proposals/`, owner promotes by hand. Promoting an **existing** global file needs **`git mv -f`**
  (bare aborts). Memory: `kingdom-global-proposal-promotion-git-mv-f`. → `knowledge/policies/global-approval.md`
- **`block-global-bash.sh` is heuristic:** a redirect (`>`, `2>/dev/null`) on a command line that
  also names a non-`_proposals/` global path trips the gate even on a pure read. Pipe to `grep`
  instead. → `knowledge/policies/global-approval.md`
- **Squash-merge hygiene:** a squash commit is not an ancestor of its source branch — ff `main`
  forward, force-delete (`-D`) the stale local branch, branch fresh; never force-push a post-squash
  branch onto `main`. (Force-pushing an *unmerged draft* feature branch to amend its own PR is fine.)
  → `knowledge/policies/merge-hygiene.md`
- **Layer discipline:** CC (this layer) does not author `docs/orchestrator/` baselines or repoint the
  CLAUDE.md baseline to that series — those are claude.ai-orchestrator + owner actions. → §0.
- **Doc-only change:** the gate proves the tree still builds/types/tests clean, NOT that the rule
  "works" — nothing runtime to verify.

## 7. Next action
**Owner:** promote the rule (Workstream A — single `git mv -f` step) to make it live; then
squash-merge close-out PR #11. Baseline-pointer advancement (C) is a separate orchestrator-layer call.
