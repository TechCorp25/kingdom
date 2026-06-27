---
title: "Session protocol — startup, CC delivery, and the continuation baseline"
source: "§5 + §8 of the Kingdom orchestrator manual"
---

# Session protocol

## A. Session startup (owner runs; orchestrator reasons over the output)

```bash
kstart                                     # postgres + ssh key + status
cd ~/kingdom                               # launch from the workspace root for environment work
git fetch origin && git branch -a          # multi-sided repo — see what moved
git checkout main && git pull --ff-only origin main
git log --oneline -3                       # confirm tip = <expected SHA from baseline>
claude                                     # confirm model = Opus 4.8 first
```

Re-derive the tip against the newest `kingdom-continuation-*.md`. If the tip differs from what the baseline
expects, **that is the first drift signal** — reconcile (another committer landed work) before starting.

## B. Delivering a task to CC

1. Draft it as a **downloadable `.md`** (never copy-paste). The owner pastes it as the first message in the CC
   session, pointing CC at the file by path.
2. **`/automate-dev` is line one** of any build/maintenance prompt — it activates the
   build→review→simplify→test→fix loop with quality gates. (Skill name, not a path.) Without it the loop
   collapses to a single pass.
3. **One task per prompt.** Explicit **per-sub-task completion-gate language**. End with a pre-output
   verification checklist. For environment hygiene, require the green gate to be **re-run by the script**, not
   asserted, and the checkpoint written.
4. **File approval = option 1 (file-by-file)**, never option 2 — mandatory for security/infra-critical work.
5. CC stops at gates → owner pastes back CC's report **plus** raw `git status` / `git diff --stat` →
   this layer re-derives raw facts, recommends with reasoning, flags anything that doesn't add up, gates
   irreversible steps. **Respect the `.claude/` hooks** — if a hook blocks a global-knowledge or global-bash
   action, that's the protection working; route via `_proposals/` + owner-gated `git mv`.

**Terminal gotchas:** `cd` does not persist across CC's ephemeral bash subprocesses; the launch directory is the
working-directory guarantee. `kstart` won't resolve in a non-interactive `bash` subprocess (enter the SSH
passphrase manually, or `kstart` in the shell first). Don't paste a shell prompt line (`user@host:…$`) as a
command. `Please run /login` / 401 = expired login; re-auth and resubmit.

## C. Session close — the continuation baseline (★ mandatory at every clean boundary)

1. **Commit at the boundary first** — never leave verified work uncommitted; land it via branch + PR.
2. **Produce `kingdom-continuation-<ISO8601>.md`** that **supersedes** the prior baseline. It captures: exact
   SHAs (kingdom `main` + any in-flight branch), remaining work items, known issues + their verification status
   (incl. any grep-only/runtime-unverified caveats), pending owner decisions, the registry/knowledge-base state,
   and the standing rules. The `kingdom-continuation` series is **intentionally separate** from any project's
   continuation series.
3. **Commit it in isolation** — stage **only that one file** by explicit path; verify with `git status`; land it.
4. **Produce the paired `<ISO8601>-kingdom-orchestrator-handoff.md`** for the next chat (how to operate + what
   to do first; points at the new baseline as state-of-truth).
5. **`/clear`** (not `/compact`). The next session re-enters cold from the committed baseline + fresh handoff +
   the live `knowledge/policies/`.
6. The **filename timestamp = the real close time.**

**Relationship to `kingdom.state.md`:** the machine checkpoint (`knowledge-checkpoint.py`) records gate/automation
state; the **continuation baseline** is the orchestrator's reasoning/handoff. They are complementary — the
baseline references the checkpoint; neither replaces the other.

**Mid-task handoffs** (chat length, not a clean boundary): same artifacts, but the handoff's §0 states explicitly
that it is mid-task and names the single open thread to resume first.
