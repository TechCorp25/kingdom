# Skill recipe — review & verify

## /code-review (working diff) vs /review (a GitHub PR)
- `/code-review` — your current working diff. Effort levels: low/medium = fewer,
  high-confidence findings; high/max = broader, may include uncertain ones. Flags:
  `--comment` posts inline PR comments; `--fix` applies findings to the working tree.
- `/simplify` — quality-only pass (reuse/simplification/efficiency); does NOT hunt bugs.
  Use `/code-review` for correctness.
- `/security-review` — security pass over pending changes; required for security-adjacent
  work (auth, rate limiting, tokens, booking-safety) before merge.

## verify / run — prove it works, don't trust the build
- Green build ≠ works. After a change, actually run it:
  - **Kingdom**: `uv run pytest -q`, then exercise the API (`uv run kingdom-api`, hit
    `/docs`) or the MCP tool path.
  - **IlluminateMyGallery**: `npm run build --prefix frontend` (expect green), plus the
    backend regression suite (`pytest tests/test_priority2_auth.py -q`, expect 45
    passed). Render mobile + desktop, both themes.
- The `verify` skill drives the app to observe real behaviour — prefer it over asserting
  success from logs.

## Gating order at a green close
lint → types → tests → (security-review if sensitive) → checkpoint (Req 3) → run-close
push + draft PR (Req 5) → handover if closing (Req 6).
