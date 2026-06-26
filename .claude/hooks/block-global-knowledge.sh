#!/usr/bin/env bash
# PreToolUse gate — protect knowledge/global/** from autonomous edits (Req 4).
#
# Blocks Edit/Write/MultiEdit whose target is under knowledge/global/, EXCEPT
# knowledge/global/_proposals/ (where CC drops change proposals for owner review).
# The owner promotes a proposal by hand:
#   git mv knowledge/global/_proposals/<file> knowledge/global/<name>
#
# Exit 2 = block the tool call and feed stderr back to Claude as the reason.
set -euo pipefail

input="$(cat)"
path="$(printf '%s' "$input" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' \
  2>/dev/null || true)"

# No path (or parser failure) → nothing to gate.
[ -z "$path" ] && exit 0

case "$path" in
  *knowledge/global/_proposals/*)
    exit 0 ;;                       # proposals are always writable
  *knowledge/global/*)
    {
      echo "BLOCKED: knowledge/global/ is owner-approval-gated (Req 4) — no direct edits."
      echo "Write the change as a proposal instead:"
      echo "  knowledge/global/_proposals/<ISO8601>-<slug>.md"
      echo "The owner promotes it manually with:"
      echo "  git mv knowledge/global/_proposals/<file> knowledge/global/<name>"
    } >&2
    exit 2 ;;
esac

exit 0
