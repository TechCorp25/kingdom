# kingdom — live state (autonomous checkpoint log)

> Maintained by `scripts/maintenance/knowledge-checkpoint.py` at each green-gated clean task close (Req 3).
> Newest checkpoint first. Control-plane knowledge — not project business data.

<!-- CHECKPOINTS -->
## 2026-06-27T19:28:41Z — chore/orchestrator-housekeeping @ 75d5646 (dirty)
- gates: uv run ruff check . OK, uv run mypy OK, uv run pytest -q OK
- Post-merge housekeeping (orchestrator): PR #7 (hygiene audit, 8 findings) + PR #8 (kingdom-orchestrator skill bundle) squash-merged to main @ 75d5646. This pass: docs/orchestrator/ output-home convention (README); kingdom-facts.md self-listing (skills row now includes kingdom-orchestrator); ruff-cleaned scaffold_artifacts.py (UP017 datetime.UTC + E501 wraps), smoke-test still emits 4 artifacts. Gates green: ruff (.claude excluded) / mypy strict (16) / 11 pytest. Deferred: repoint CLAUDE.md Active Session Baseline to the orchestrator's first kingdom-continuation baseline once one exists (premature now).

## 2026-06-27T06:25:29Z — main @ 04e7bac (dirty)
- gates: uv run ruff check . OK, uv run mypy OK, uv run pytest -q OK
- Hygiene-audit deferred-items batch (2026-06-27, /automate-dev solo pass 2): F-1 collapsed the Python version triple — added .python-version=3.12 and rebuilt .venv on cpython-3.12.13 (was drifted 3.14.5) so venv matches the declared stack + ruff/mypy py312 targets; N-2 docker-compose POSTGRES_PASSWORD now fail-fast (${VAR:?...}) instead of a silent change_me default, and .env.example nudges a generated strong value; N-3 added docs/README.md documenting docs/<slug>/ layout + source-of-truth/retention convention (agents do not delete handovers); N-4 .env.example DATABASE_URL psycopg->asyncpg + comment, now matching src/kingdom/config.py default. Gates green on 3.12: ruff clean / mypy strict clean (16) / 11 pytest passed. All 8 audit findings now resolved (I-1,F-1,F-2,F-3,N-1,N-2,N-3,N-4). Working tree NOT committed/pushed (awaiting owner go-ahead).

## 2026-06-27T01:09:57Z — main @ 04e7bac (dirty)
- gates: uv run ruff check . OK, uv run mypy OK, uv run pytest -q OK
- Hygiene-audit remediation batch (2026-06-27, via /automate-dev solo pass): I-1 fixed CLAUDE.md Active Session Baseline pointer (broken+stale path -> docs/illuminate-my-gallery/kingdom-continuation-2026-06-13T13-00-00.md); F-2 removed out-of-stack FLASK_SECRET_KEY + relabelled API section FastAPI/uvicorn in .env.example; F-3 ruff-formatted scripts/maintenance/{knowledge-checkpoint,register-projects}.py; N-1 added [tool.ruff] extend-exclude=['.claude'] so 'ruff check .' reflects Kingdom code only. Gates green: ruff clean / mypy strict clean (16) / 11 pytest passed. Working tree NOT committed/pushed (awaiting owner go-ahead). Deferred pending owner decision: F-1 Python 3.11/3.12/3.14 version triple; N-2 docker-compose change_me default; N-3 docs/ handover retention convention; N-4 NEW .env.example DATABASE_URL advertises psycopg but config.py defaults to asyncpg.

## 2026-06-26T05:59:39Z — claude/dreamy-volta-8gzg9z @ 4bc0427
- gates: uv run pytest -q OK
- Addressed Codex P2 review on PR #6: added block-global-bash.sh (Bash PreToolUse gate) closing the shell-write bypass of the knowledge/global gate (20-case matrix passes); .gitignore now excludes .claude/settings.local.json; global-approval.md documents both hooks + heuristic limitation honestly. Both review threads replied + resolved. Pushed 4bc0427.

## 2026-06-25T22:39:26Z — claude/dreamy-volta-8gzg9z @ 2c571b2 (dirty)
- gates: asserted green by caller (--assume-green)
- Knowledge base activated: SessionStart contract injection + PreToolUse global gate + Stop run-close nudge; /handover skill; knowledge-checkpoint.py; policies/skills/projects seeded; global baseline queued in _proposals for owner promotion. Gates: ruff clean (my code), 11 pytest passed, mypy strict clean on script. Next: owner promotes global/_proposals; consider Phase-7 list_knowledge/read_knowledge MCP tools.

