# CC task — <short title>

`/automate-dev`

<!--
LINE ONE IS `/automate-dev` — it activates build→review→simplify→test→fix with quality gates.
Without it the loop collapses to a single pass. One task per prompt. Owner pastes this file's path
as the first message in the CC session.
-->

## Operating context
- Repo: `~/kingdom` (workspace root; launch CC from here — `cd` does not persist across CC bash subprocesses).
- Branch: cut fresh from updated `main` → `chore/<topic>`. Never commit to `main`. Draft PR is the path.
- Base pinned to SHA: `<SHA>` (do not assume `main` is current).
- Gate: `ruff` + `mypy --strict` + `pytest`, **re-run by the script**, not asserted.

## The single task
`<Exactly one task. What, where, the acceptance criterion drawn from the canonical reference (policy /
operating-contract / doc) — not a diff impression.>`

## Constraints
- Additive-only to shared knowledge/policies/config. Global knowledge → `_proposals/` + owner-gated `git mv`
  only. Do not fight the `.claude/` hooks; a block is the protection working.
- Infra/automation files (`.claude/**`, `settings.json`, `pyproject.toml`, `docker-compose.yml`, hooks) are
  **surfaced as a decision**, never silently edited.
- Stage by explicit path; commit per concern; never `git add -A`. No secrets / `.env`.
- File approval = option 1 (file-by-file).

## Per-sub-task completion gates
- [ ] `<sub-task>` — done when `<objective check>`; gate green (re-run); on-disk verified (`git status` + `grep`).
- [ ] `<sub-task>` — …

## Pre-output verification checklist (CC must report before finishing)
- [ ] Raw `git status` + `git diff --stat` pasted (not prose).
- [ ] Gate result is from a **re-run**, not a recollection.
- [ ] Any fix verified only by `grep` is flagged as **NOT runtime-verified**.
- [ ] Nothing committed to `main`; PR is draft; branch name + base SHA stated.
