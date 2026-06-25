# Policy — token budget (Req 1)

Token efficiency is mandatory across Kingdom and every tracked project. Optimise for
**reconstructable signal per token**, not for length or thoroughness theatre.

## Search & read
- Prefer `Grep`/`Glob` over `Read` to locate things. Read only the slice you need
  (`offset`/`limit`), not whole files "to be safe."
- For breadth ("where is X / which files touch Y"), delegate to the **Explore** agent
  instead of opening many files in the main thread.
- Don't re-read a file you just wrote/edited — the harness already tracks its state.
- Batch independent tool calls into one turn (parallel) rather than serial round-trips.

## Writing (knowledge, handovers, replies)
- Point to paths and policy docs; don't paste large bodies that already live in the repo.
- Knowledge files are re-loaded every session — keep them dense and pointer-based. A
  bloated knowledge base taxes every future run.
- In replies, lead with the answer. Don't narrate options you won't take or re-derive
  facts already established in the conversation.

## Agents & skills
- Spawning a subagent or firing a multi-agent team has real token cost. Use it when the
  work genuinely needs it (see `automate-dev-default.md`), not for questions/reads.
- Reuse a running agent (continue it) rather than cold-spawning a fresh one when the
  context still applies.

## Context window
- Treat the window as a budget with a reserve. Before it gets heavy, checkpoint
  (`knowledge-maintenance.md`) and write the handover (`handover.md`) — never spend the
  last of the window and then try to hand off.

## The one tension to hold
Req 2 (default to `/automate-dev`) must not override this. Code-changing work → the team;
questions, reads, audits, single-file lookups → stay direct. Firing the team for a
read-only question is a Req 1 violation.
