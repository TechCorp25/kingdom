# knowledge/global/_proposals/ — owner approval queue (Req 4)

`knowledge/global/**` is owner-approval-gated. CC cannot edit it directly — the
PreToolUse hook (`.claude/hooks/block-global-knowledge.sh`) blocks `Edit`/`Write`/
`MultiEdit` anywhere under `knowledge/global/` **except this `_proposals/` folder**.

## Flow
1. CC writes a proposed global file here as `<ISO8601>-<target-name>.md`
   (e.g. `2026-06-25T17-52-00-environment.md`).
2. The **owner** reviews it.
3. The owner promotes it by hand — this is the approval signal:
   ```bash
   git mv knowledge/global/_proposals/<ISO8601>-<target>.md knowledge/global/<target>.md
   ```
4. Reject by simply deleting the proposal.

Nothing here is "live" knowledge — only files that have been promoted into
`knowledge/global/` are part of the operating contract. Bypassing this queue (e.g.
writing to `global/` via a raw shell heredoc) is a contract violation, not a shortcut.
