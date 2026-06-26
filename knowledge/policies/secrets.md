# Policy — secrets & configuration

- **Configuration via environment variables only** (`.env`, gitignored). No secrets in
  code, ever.
- `.env.example` is the committed contract (placeholder values). Real values live only in
  `.env`. After a stack change: `cp .env.example .env`, then set real values (and keep
  `DATABASE_URL` on the `+asyncpg` driver).
- **Never commit** `.env`, credentials, tokens, keys, or Postgres data dirs / backups /
  indexes (all gitignored under `data/`).
- **Never put a secret in** a commit message, PR title/body, code comment, knowledge
  file, handover, or any pushed artifact. Handover docs explicitly state "secrets are
  never in this document — values live in gitignored `.env` only."
- Before any push (`run-close.md`), confirm nothing sensitive is staged:
  `git diff --cached --name-only` and check for `.env` / key material.
- Generate strong values, e.g. `python3 -c "import secrets; print(secrets.token_hex(32))"`.
- Bind API, MCP, and Postgres to **localhost only** — never expose them publicly.
- Tokens are stored hashed (SHA-256 / HMAC / bcrypt per use); raw values are never
  persisted (IlluminateMyGallery auth model).
