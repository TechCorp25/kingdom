# Kingdom operating contract (supreme rules)

> Owner-set. This file is **owner-approval-gated** (Req 4): never edit it directly —
> propose changes in `knowledge/global/_proposals/`. The PreToolUse hook enforces this.
> Where any policy or skill conflicts with this file, **this file wins.**

These six requirements apply across the whole Kingdom environment — the control plane
itself and every tracked project under `projects/`, present or future.

## 1. Token efficiency is mandatory, everywhere
Default to the cheapest tool that answers the question: `Grep`/`Glob` over `Read`; the
`Explore` agent for breadth searches; read only the slice of a file you need; batch
independent tool calls in one turn. In writing (knowledge files, handovers, replies),
prefer pointers to paths over pasted bodies. Optimise for reconstructable signal per
token, not length. → `knowledge/policies/token-budget.md`

## 2. `/automate-dev` is the default execution path for code-changing work
Any build / implement / fix / refactor / feature / multi-file change runs through the
`automate-dev` workflow **without waiting to be told**. Pure questions, reads, audits,
and explanations stay direct (firing the team for those would violate Req 1).
→ `knowledge/policies/automate-dev-default.md`

## 3. Knowledge is updated autonomously at every green-gated clean close
When a task or job is green-gated (lint + types + tests pass) and cleanly closed, record
the new state with `scripts/maintenance/knowledge-checkpoint.py` before moving on. No
silent state drift. → `knowledge/policies/knowledge-maintenance.md`

## 4. `knowledge/global/**` changes need manual owner approval
CC may read `global/` freely but may not write it. Proposed changes go to
`knowledge/global/_proposals/<ISO8601>-<slug>.md`; the owner promotes them by hand
(`git mv`). Everything else under `knowledge/` is autonomously updatable.
→ `knowledge/policies/global-approval.md`

## 5. Push at the end of every planned run that closes green
When all todos are complete and green-gated, commit and push the **Kingdom** repo on its
working branch and ensure a draft PR exists. Project repos follow their own per-project
push discipline. Every PR on the Kingdom repo links its tracking issue — a PR with no
linked issue is not eligible to leave draft; tracked project repos keep their own
per-project issue-link discipline. → `knowledge/policies/run-close.md`

## 6. A high-detail handover precedes every compact
Produce a continuation/handover file at every clean task close **and before any context
compact**. Monitor the context window and keep enough in reserve (~15–20%) to write it
faithfully — a compact that lands before the handover exists is a continuity failure.
Force one with `/handover`. → `knowledge/policies/handover.md`

---
*Authoritative. Verify environment facts with the commands in `knowledge/global/*` before
acting on anything time-sensitive.*
