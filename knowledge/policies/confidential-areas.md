# Policy — confidential & fragile areas

## `docs/contracts ` (IlluminateMyGallery) — confidential, fragile name
- Holds a 7-piece contract pack incl. consent / marketing release. **Business-confidential**
  and carries a solicitor-review caveat on the legal set.
- **The directory name has a trailing space** (`docs/contracts ` ← note the space). This
  is brittle: it breaks globs, tab-completion, and scripts. Rename to `docs/contracts/`
  only at a deliberate, safe point — do not touch casually.
- Decide where the confidential source docs live **before** any commit; do not commit
  confidential material into a public/shared repo without owner direction.

## General
- Don't commit confidential business material, contracts, client data, or legal drafts
  without explicit owner approval and a decision on the destination repo.
- Don't silently change deployment config (`railway.toml`, Railway service settings) —
  flag it to the owner.
- Treat anything under a project's `docs/` that looks legal/financial/client-identifying
  as confidential until told otherwise.
