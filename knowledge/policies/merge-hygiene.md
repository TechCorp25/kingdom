# Policy — git & merge hygiene

The trap that has stranded work here more than once: **a squash-merge on `main` is NOT
an ancestor of its source branch.** Internalise the consequences.

## Squash-merge reality
- PRs are squash-merged. After a squash, `git merge/pull --ff-only` from the old branch
  will **refuse** — treat that refusal as the signal the branch diverged, never as
  something to force past.
- A branch forked *before* a prior squash may not have `origin/main` as an ancestor →
  land it ONLY via a fresh squash-merge PR, never a local merge.

## Hard rules
- **Never force-push** a post-squash feature branch onto `main` — it erases the PR merge.
  To land commits made after a squash, cherry-pick (or `rebase --onto origin/main`) only
  the genuinely-new commits, then fast-forward + push.
- **`git pull --ff-only` only.** If it refuses, STOP and reconcile — diagnose before
  acting. Two-sided repos (CC + Codex both commit) make blind merges dangerous.
- **"Committed locally" ≠ "on main".** Before building on prior work, confirm it shipped:
  `git diff --stat origin/main HEAD` and check key files exist on `origin/main`.
- **Delete the source branch in the same step as the squash-merge,** and branch fresh
  from updated `main`. Never keep committing on a branch whose earlier state was squashed
  — that is exactly how work gets stranded off `main`.
- **Stage by explicit path** — never `git add -A` on a dirty tree.
- **Push before you duplicate** — unpushed commits were the root cause of stale repo
  copies.

## At run close
See `run-close.md` (Req 5) for the Kingdom push/PR sequence. Network-error pushes retry
with backoff; a non-fast-forward rejection means diverge → reconcile, do not retry.
