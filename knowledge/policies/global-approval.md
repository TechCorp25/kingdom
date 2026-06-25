# Policy — global knowledge requires owner approval (Req 4)

`knowledge/global/**` holds the supreme operating contract and the environment/identity
facts true in every session. It changes only with **manual owner approval**.

## Enforcement (hard, not honour-system)
`.claude/hooks/block-global-knowledge.sh` is a `PreToolUse` hook (matcher
`Edit|Write|MultiEdit`, wired in `.claude/settings.json`). It blocks any edit whose
`file_path` is under `knowledge/global/` — **except** `knowledge/global/_proposals/` —
and returns exit 2 so CC sees the rejection reason.

## The approved flow
1. CC writes the proposed file to
   `knowledge/global/_proposals/<ISO8601>-<target-name>.md`.
2. Owner reviews.
3. **Owner promotes it by hand — this `git mv` IS the approval signal:**
   ```bash
   git mv knowledge/global/_proposals/<ISO8601>-<target>.md knowledge/global/<target>.md
   ```
4. Reject = delete the proposal.

## Rules
- Never circumvent the gate (e.g. writing to `global/` via a raw shell heredoc, or
  `git mv`-ing your own proposal). The gate guards the *contract* — bypassing it is a
  contract violation, not a clever shortcut.
- Reading `global/` is always free and encouraged.
- Only files actually present in `knowledge/global/` (promoted) are "live." Anything in
  `_proposals/` is a draft with no authority.

## Initial baseline note
The first population of `global/` was delivered as proposals for exactly this reason —
the owner promotes the foundational files before they take effect.
