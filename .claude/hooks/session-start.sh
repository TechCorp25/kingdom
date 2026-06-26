#!/usr/bin/env bash
# SessionStart — inject the Kingdom operating contract into every session.
# Deliberately terse: detail lives in knowledge/ (pointers, not pasted dumps) so
# this injection itself honours the token budget (Req 1).
cat <<'EOF'
KINGDOM OPERATING CONTRACT — authoritative copy: knowledge/global/operating-contract.md
1. TOKEN-EFFICIENT by default — Grep/Glob over Read, the Explore agent for breadth,
   batch independent tool calls, prefer pointers over pasted file dumps.
   → knowledge/policies/token-budget.md
2. /automate-dev is the DEFAULT path for code-changing work (build / implement / fix /
   refactor / feature / multi-file edit) — invoke it without being asked. Pure
   questions, reads, and audits stay direct. → knowledge/policies/automate-dev-default.md
3. At every GREEN-GATED clean task close, update knowledge autonomously:
   uv run python scripts/maintenance/knowledge-checkpoint.py --slug <slug> --summary "..."
   → knowledge/policies/knowledge-maintenance.md
4. knowledge/global/** is OWNER-APPROVAL-GATED — never edit directly (hook-enforced);
   drop proposals in knowledge/global/_proposals/. → knowledge/policies/global-approval.md
5. On planned-run close with all todos green: commit + push the KINGDOM repo on its
   branch + ensure a draft PR exists. → knowledge/policies/run-close.md
6. Produce a high-detail handover/continuation file at every clean task close AND before
   any compact — monitor context and reserve room to write it. Force one with /handover.
   → knowledge/policies/handover.md
EOF
