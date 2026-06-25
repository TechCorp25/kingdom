# Skill recipe — frontend / design work (IlluminateMyGallery)

Use with the `frontend-design` / `code-quality` skills. Project brief:
`knowledge/projects/illuminate-my-gallery.md`.

## Canonical design-system reference (repo root of the app)
- `design-system/components/landing.jsx` — the canonical component.
- `design-system/styles/tokens.ts` — type scale, shadow spec, breakpoints.
- `design-system/styles/styles.css` — `.display`/`.eyebrow`, `--shadow-*`, gold-glow,
  bloom alphas.
- App page it pairs with: `frontend/src/pages/Landing.jsx`.
- ⚠️ The OTHER `design-system/` on disk belongs to CivicMAPS
  (`projects/civic-maps-preview/...`) — different project, ignore it.

## Acceptance criteria come from the canonical component, not a styling diff
- Verify **mobile and desktop**, **light and dark**. Render-at-1280 ≠ responsive.
- Prefer **computed font-size measurement** over eyeballing (hero overshoot bug came
  from trusting the eye). Canonical hero ≈ 76.8px @1280, not 88px.

## Tailwind shadow gotcha (standing)
`shadow-[var(--x)]` is parsed by Tailwind as a shadow **COLOR** → renders
`box-shadow: none`. Use a **named `.shadow-*` utility** instead (e.g. `.shadow-collage`).

## Token rule for a faithful canonical rebuild
"No new tokens" is too strict — **allow ADDITIVE DS primitives** ported from canonical /
spec values (e.g. `.hero-atmosphere`, `.panel-gold`). **Never modify or remove an
existing token** — admin/shared consumers read `index.css` / `tailwind.config.js`.

## Delivery
File-based only (mobile corrupts unicode on paste). Owner-gated merges; squash + delete
branch; branch fresh from verified `main`.
