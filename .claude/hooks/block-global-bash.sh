#!/usr/bin/env bash
# PreToolUse gate (Bash) — extend the knowledge/global/ owner-approval gate (Req 4) to
# shell commands, which the Edit|Write|MultiEdit matcher cannot see.
#
# Blocks a Bash command when it BOTH references a knowledge/global/ path outside
# _proposals/ AND looks like a mutation (redirect, tee/sed -i/mv/cp/rm/dd/ln/...,
# git mv|rm|restore|checkout of a file, or python open(...,'w')). Reads (cat/grep/ls/
# head/tail/find/git log/git diff) are allowed — reading global is always fine.
#
# This is necessarily heuristic (shell can be obfuscated). It catches the realistic
# write/promotion forms; the honour-system policy in knowledge/policies/global-approval.md
# covers the rest. Exit 2 = block and surface the reason to Claude.
set -euo pipefail

input="$(cat)"

GUARD_INPUT="$input" python3 - <<'PY'
import json, os, re, sys

try:
    cmd = json.loads(os.environ.get("GUARD_INPUT", "")).get("tool_input", {}).get("command", "")
except Exception:
    sys.exit(0)  # unparseable input → don't break unrelated bash (fail-open on parse only)

if not cmd:
    sys.exit(0)

GLOBAL = "knowledge/global/"
PROP = "knowledge/global/_proposals/"

# No global reference at all → nothing to gate.
if GLOBAL not in cmd:
    sys.exit(0)

# Drop allowed _proposals/ references; if every global reference was under _proposals,
# the command does not touch gated global → allow.
if GLOBAL not in cmd.replace(PROP, ""):
    sys.exit(0)

# A non-proposals global path is referenced. Block if the command looks mutating.
redirect = re.search(r">>?\s*['\"]?\S*knowledge/global/(?!_proposals/)", cmd)
mutators = re.search(r"(?:^|[\s|;&(])(tee|mv|cp|rm|truncate|dd|ln|install|rsync)(?:\s|$)", cmd)
sed_inplace = re.search(r"sed\s+[^|;&]*-i", cmd)
git_mut = re.search(r"git\s+(mv|rm|restore|checkout)\b", cmd)
py_write = re.search(r"open\([^)]*['\"][wax]", cmd)

if redirect or mutators or sed_inplace or git_mut or py_write:
    sys.stderr.write(
        "BLOCKED: shell write/move/delete targeting knowledge/global/ "
        "(owner-approval-gated, Req 4).\n"
        "Reading global/ is fine; mutating it is not. Put the change in "
        "knowledge/global/_proposals/ and let the OWNER promote it (the owner's git mv "
        "runs in their own terminal, not through this tool).\n"
    )
    sys.exit(2)

# Global path referenced but no mutation indicator → treat as a read; allow.
sys.exit(0)
PY
