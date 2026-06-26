# kingdom — live state (autonomous checkpoint log)

> Maintained by `scripts/maintenance/knowledge-checkpoint.py` at each green-gated clean task close (Req 3).
> Newest checkpoint first. Control-plane knowledge — not project business data.

<!-- CHECKPOINTS -->
## 2026-06-26T05:59:39Z — claude/dreamy-volta-8gzg9z @ 4bc0427
- gates: uv run pytest -q OK
- Addressed Codex P2 review on PR #6: added block-global-bash.sh (Bash PreToolUse gate) closing the shell-write bypass of the knowledge/global gate (20-case matrix passes); .gitignore now excludes .claude/settings.local.json; global-approval.md documents both hooks + heuristic limitation honestly. Both review threads replied + resolved. Pushed 4bc0427.

## 2026-06-25T22:39:26Z — claude/dreamy-volta-8gzg9z @ 2c571b2 (dirty)
- gates: asserted green by caller (--assume-green)
- Knowledge base activated: SessionStart contract injection + PreToolUse global gate + Stop run-close nudge; /handover skill; knowledge-checkpoint.py; policies/skills/projects seeded; global baseline queued in _proposals for owner promotion. Gates: ruff clean (my code), 11 pytest passed, mypy strict clean on script. Next: owner promotes global/_proposals; consider Phase-7 list_knowledge/read_knowledge MCP tools.

