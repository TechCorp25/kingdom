# Policy — global knowledge requires owner approval (Req 4)

`knowledge/global/**` holds the supreme operating contract and the environment/identity
facts true in every session. It changes only with **manual owner approval**.

## Enforcement (two PreToolUse hooks + honour-system backstop)
Both hooks are wired in `.claude/settings.json` and return exit 2 (with a reason) to
block:
- **File tools** — `block-global-knowledge.sh` (matcher `Edit|Write|MultiEdit`) blocks any
  call whose `file_path` is under `knowledge/global/`, **except** `_proposals/`. This is
  exact: the file path is known, so coverage is complete.
- **Shell** — `block-global-bash.sh` (matcher `Bash`) blocks a command that references a
  non-`_proposals/` global path together with a mutation form: redirect (`>`/`>>`), `tee`,
  `sed -i`, `mv`/`cp`/`rm`/`ln`/`dd`/`truncate`/`install`/`rsync`, `git mv|rm|restore|checkout`
  of a file, or `python open(...,'w')`. Reads (`cat`/`grep`/`ls`/`git log`/`git diff`) pass.

The Bash gate is **heuristic** — shell can be obfuscated (base64, eval, an interpreter
reading from stdin), so it cannot be airtight. It catches every realistic write/promotion
form (all tested); the rule below is the backstop for the rest. Note the owner's promotion
`git mv` runs in their **own terminal**, not through CC's Bash tool, so it is unaffected —
and CC attempting that same `git mv` is correctly blocked (CC must not self-promote).

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
