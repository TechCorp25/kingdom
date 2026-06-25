#!/usr/bin/env bash
# Stop — gentle run-close nudge. NON-blocking (exit 0), and only when the working
# tree is dirty, so it stays quiet on read-only turns and never loops the agent.
set -euo pipefail

root="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$root" 2>/dev/null || exit 0

if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  echo "↳ Run-close checklist (knowledge/policies/run-close.md): green-gate → knowledge-checkpoint → handover if context heavy → commit + push (Kingdom) + ensure draft PR."
fi
exit 0
