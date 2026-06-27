---
title: "GitHub workflow — multi-sided repo discipline"
source: "§4 of the Kingdom orchestrator manual"
note: "`merge-hygiene` is a written policy in `knowledge/policies/` — read it live and follow it; this file is the operating summary."
---

# GitHub workflow — multi-sided repo discipline

## Branch → PR → review → squash-merge → delete → re-branch

1. **Never commit directly to `main`.** Branch fresh from updated `main` for each task (e.g. `chore/<topic>`).
   A **draft PR** is the standard path (it satisfies the operating contract's PR requirement); the owner gates
   the merge.
2. **Squash-merge to `main`** (owner-gated). On GitHub this is **two clicks**: the green button opens the
   commit-message editor; a separate **Confirm** fires the merge. Stopping after the first leaves the PR open.
3. **Delete the source branch at squash.** Re-branch from the now-updated `main` for the next task.
4. **Never reuse a branch whose earlier state was squash-merged** (squash severs ancestry).

## Multi-sided discipline (CC + Codex + `claude/*` branches + owner direct-upload)

- `git fetch` + `git branch -a` **every session**. Pull with **`--ff-only`** (or a clean rebase). If `--ff-only`
  **refuses → STOP and diagnose** (you're likely on the wrong branch, or it diverged): clean divergence →
  rebase; file-overlap → guided 3-way. **Never force-push.**
- **Pin review bases to a SHA**; never assume `main` is current — it can move twice in a session, and other
  committers (Codex, `claude/*`, direct uploads) land independently.
- **The direct-GitHub-upload path is real.** A doc can already be committed on `main` (via an upload that merged
  in a PR) even though your working tree shows it "untracked." **Always `git log -- <path>` before assuming a
  file isn't committed**, and re-derive — do not double-add.
- **Carry untracked work across a branch switch with `git stash -u`**, not a commit-on-wrong-branch. If `stash
  pop` collides with an already-committed copy, the pop aborts atomically and **keeps the stash** — verify the
  committed copy matches, then `git add` the rest by explicit path and `git stash drop` only after the push is
  clean.

## Traps (codified)

- Squash severs ancestry; a branch forked before an earlier squash landed can only land via a squash-merge PR,
  never a local merge.
- A two-dot `base..branch` diff overstates a branch that forked before earlier work landed.
- Never `git checkout --theirs .` wholesale in a guided merge.
- **Infra/automation files** (`.claude/**`, `settings.json`, `pyproject.toml`, `docker-compose.yml`, hooks) are
  surfaced as **decisions**, never silently modified.
