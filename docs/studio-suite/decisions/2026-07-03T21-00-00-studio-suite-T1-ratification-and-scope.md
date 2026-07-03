---
title: "studio-suite — T1: Ratification & Scope Record"
project: "studio-suite (new app dev) · Kingdom workspace"
type: "task-record + ratification"
version: "2026-07-03T21-00-00"
owner: "TechCorp (solo developer, Melbourne AU)"
status: "RATIFIED (owner-delegated calls recorded in §4). Closes T1 authoring; T1 completes when this file + the knowledge brief land in kingdom-docs."
relates_to: "studio-suite-continuation-2026-06-22T19-30-00.md (reset ledger §5); DR-001; DR-001 Addendum A"
supersedes: "nothing — first T-task record of the reset"
---

# T1 — Ratification & Scope

T1 is the gate task of the design-system reset: lock the architecture, resolve placement,
write the responsive acceptance gate concretely, and scope what T2–T6 inherit. This record is
the resolved-decision truth for those items. The continuation baseline remains live-state truth.

---

## 1. Live state at ratification (verified this session, raw output)

- **studio-suite `main` = `07d5d3e`** — advanced from `2014e2b` by four owner web-upload commits
  (Jun 27), **docs-only**: the content policy + the `docs/luma-response-audit-fix/` bundle (00–11).
  No code, no `tokens.ts`, no `web/` touched. **Every artifact pinning `2014e2b` is SHA-stale but
  substance-current**; the T5 rebase target (`feature/landing-fidelity` → brass-corrected main)
  is unchanged in effect. Next baseline re-pins to `07d5d3e`.
- **`feature/landing-fidelity` @ `0e834d5`** retained (T5 seed). Codex `979e1da` deferred.
  Stale `fix/tokens-light-gold-brass` lingers (optional verified-safe cleanup, parked).
- **kingdom-docs @ `5cddda8`**; DR-001 + Addendum A committed under
  `docs/studio-suite/decisions/` — **`decisions/` is the standing convention** for DR-class
  artifacts, this file included.
- Untracked-vs-uploaded collision (13 files) resolved: all byte-identical, backed aside,
  fast-forwarded, re-verified identical post-pull. Preview 200.
- Local-only untracked remaining: `design-system/assets/logo-banner-multi.svg` (→ §6.3),
  `docs/studio-suite-content-policy.docx` (→ §4.2).

## 2. Ratified architecture (carried from baseline §5, locked here)

1. **Gradients-in-tokens** — adopted, scoped to brand/semantic gold; plain-CSS consumption only,
   never Tailwind arbitrary-value vars.
2. **Two-ramp gold** (`goldBrass`/`goldChampagne`) — adopted; resolved base identical to main.
3. **Scale-var CSS system** — adopted; it is the authoring contract for landing + portal surfaces.
4. **Fluid responsive web** — hard completion gate, wording in §3 below.
5. **Architecture B** — shared `@is/tokens` scale to native; responsive layout logic per-platform.
   T2/T3 must confirm the responsive design is scale-driven (token-backed).

## 3. Responsive acceptance gate — §11, final wording

**Two-part gate (DR-001 §2/§4.1):**
- **Spec (design lane):** the extended `qa/responsive-harness.html` defines the viewport ×
  orientation × surface matrix — per Addendum A: **17 surface states × 16 viewports**, including
  the mandatory **375px portrait small-end**, landscape phone, tablet portrait + landscape,
  desktop, wide, and **constrained-height**. Spec inputs also include: the per-surface verdict
  ledger, the **1152px landing nav fit floor** with `LandingNavSheet` collapse behaviour,
  **44×44 tap-target hardening** on touch, and container-query work (**B-3**) deferred to the
  production re-implementation.
- **Gate (dev lane, binding):** a **Playwright suite in studio-suite's Vite CI, run against the
  shipped build**, across the full harness matrix. Pass = zero horizontal-overflow dead-zones on
  every surface at every matrix point, both orientations. Authored dev-side as each surface lands
  (T5 first; small dedicated CI-setup slice permitted just ahead of T5).

**Frozen-desktop reconciliation clause (binding):** the gate is satisfied by **passing the
matrix**, not by mandating intrinsic layout. A frozen surface that passes is compliant; intrinsic
is authorized per-surface only where frozen **provably fails** the matrix, each desktop-affecting
change individually owner-gated with the design lead's stated reason for the constraint
(DR-001 §3). Frozen-desktop / "no auto-fit" is a **controlled exception surface**, neither
inviolable nor freely overridable.

**Caveat held (Addendum A §A3):** bundle PASS ≠ production sign-off. The buildless prototype's
17/17 result is spec + intent-proof; production **re-implements (seed-not-dropin) and
re-certifies** against the real Vite build — including independently getting the sign-in
hooks-order fix right in the production lane.

## 4. Placement & canonical-form ratifications (owner-delegated, decided 2026-07-03)

1. **Product-governance / Luma-ops material lives in the APP repo under `docs/`, outside
   `design-system/`.** Grounds: A4 work-type distinction — product/content lane ≠ design lane.
   The Jun-27 landing of the content policy and audit-fix bundle at `docs/` is hereby ratified as
   deliberate. At T2 ingest, the bundle's `contracts/` and `policy/` directories land as
   `docs/contracts/` and `docs/policy/` (renamed per §5), never inside `design-system/`.
2. **Content policy canonical form:** the tracked
   `docs/illuminate-studios-image-representation-content-policy.md` is **canonical** (frontmatter
   carries `source_file:` provenance). The `.docx` is **not committed**; owner preserves it
   off-repo. `03_COPYWRITER_IMAGE_REPRESENTATION_POLICY.md` is tagged the bundle-embedded copy of
   the same policy; the standalone wins on any conflict. The canonical file is **renamed** in the
   §5 pass (legacy brand in filename + body).

## 5. Legacy-brand rename scope (T2 global pass — now concrete)

"Illuminate Studios" / "IlluminateMyGallery" / "Illuminate" branding is confirmed pervasive in the
Jun-27 material: filenames (`illuminate-studios-…content-policy.md`), body text of all 13 docs, the
machine-readable JSON (`"brand": "Illuminate Studios"`), and the content policy's frontmatter
(`organisation:`). The T2 rename is **global**: bundle + committed docs + filenames + frontmatter +
JSON values. Product-name strings inside the Luma policy corpus rename to the studio-suite brand;
`assistant: "Luma"` is retained (Luma is the product's own concierge name, not legacy brand).

## 6. The Jun-27 material — characterization, lane tags (A4), and dispositions

**What it is:** a complete Luma/content governance package with two hard rules —
(1) **no image-editing/retouching/appearance-alteration language anywhere** (appearance is
natural, straight-out-of-camera); (2) **booking-state language control** — a tentative request,
availability hold, or pending request is never described as confirmed.

### 6.1 Lane-tag ledger

| File | Lane | Disposition |
|---|---|---|
| `00_README` | index | Reference; bundle manifest + the two non-negotiable rules |
| `01_FORMATTED_BOOKING_TRANSCRIPT` | source/example | **Synthetic test data — NOT real client PII** (owner-confirmed 2026-07-03). Retained as a **known-non-compliant example** for correction reference (`09` fixes it); never reuse as approved copy or training data |
| `02_LUMA_RESPONSE_POLICY` | policy (product) | Binding on Luma output → T6-luma spec input |
| `03_COPYWRITER_IMAGE_REPRESENTATION_POLICY` | policy (content) | Bundle-embedded copy of the canonical content policy (§4.2) |
| `04_CODEX_IMPLEMENTATION_HANDOFF` | engineering (dev) | IMG-era Codex handoff. **Input only — re-implement in-lane** (seed-not-dropin). Its internal file table uses stale pre-bundle numbering; recorded, harmless |
| `05_LUMA_PROMPT_PATCH` | engineering/spec | Prompt text → re-authored for studio-suite's Luma at T6 |
| `06_RESPONSE_VALIDATION_RULES` | engineering spec | Post-generation validator requirement → T6-luma |
| `07_BOOKING_STATE_LANGUAGE_RULES` | policy/spec | State-driven language matrix (8 states incl. `needs_human`) → T6-luma + booking |
| `08_REGRESSION_TEST_CASES` | test (dev) | Re-implement as real tests in T6's suite |
| `09_TRANSCRIPT_CORRECTIONS` | spec/source | Mandatory corrections to `01` |
| `10_MACHINE_READABLE_POLICY` | policy (machine-readable) | JSON config — directly consumable by the production validator |
| `11_RESPONSE_VALIDATOR_REFERENCE` | engineering (dev) | Reference Python — **re-implement against studio-suite's actual backend, never drop in**. Note: reference code uses `from __future__ import annotations` — the known FastAPI `Depends()` 422 trap; the production implementation must respect the standing convention |

### 6.2 Cross-cutting compliance gate (recorded, not new scope)

The content policy governs **all client-facing and automated copy** — not just Luma. Therefore:
- **T5 (landing)** inherits a named authoring constraint: landing copy must comply with the
  canonical content policy (no editing/retouching language). Checked at T5's review gate.
- **T6 (every portal surface)** inherits the same constraint; **T6-luma** additionally inherits
  the engineering spec set (`02`,`05`,`06`,`07`,`10`,`11` as inputs; validator + booking-state
  language + regression tests re-implemented in-lane).
No new T-task is created; T5/T6 completion gates each gain one named check.

### 6.3 Deliberate landings queued

- `design-system/assets/logo-banner-multi.svg` — new design-lane asset, untracked. Lands
  deliberately at T2 (explicit-path stage, design-system placement), pending owner confirmation
  it is final.
- `knowledge/projects/studio-suite.md` — the remaining T1 close item; authored against the
  kingdom `_template`, committed in isolation to kingdom-docs.

## 7. T2 pre-gate (hard): the post-remediation bundle

The scratch bundle at `~/ds-incoming-review/illuminate-design-system/` **predates Addendum A's
remediation** — `qa/evidence/` and `docs/responsive-remediation-plan-2026-06-26.md` are absent,
meaning its `portal/landing.jsx` lacks `LandingNavSheet` and its harness lacks the full matrix.
**T2 must not ingest this scratch.** Owner-relay to the design lead: deliver the
post-remediation bundle zip (must contain `qa/evidence/`, the remediation plan, the modified
`portal/landing.jsx` + `foundation/styles.css`, and the extended harness). T2 authoring is
blocked until it is on disk and characterized.

## 8. Ledger effects (what T2–T6 inherit from this record)

- **T2:** ingest the **post-remediation** bundle (§7) · global rename (§5) · place
  `contracts/`→`docs/contracts/`, `policy/`→`docs/policy/` (§4.1) · land `logo-banner-multi.svg`
  (§6.3) · triage out anything this record marks input-only.
- **T3:** two-ramp gold + scale-vars + brand/semantic gradients emitted from tokens; confirm
  two-copy `tokens.ts` lockstep vs consolidation (still open, owner call at T3).
- **T4:** consume via plain CSS; never Tailwind arbitrary-value vars for composite vars.
- **T5:** landing re-implemented from the retained seed against the new `landing.jsx`; §3 gate
  binds; §6.2 content-policy check binds; Playwright CI stands up here (or one slice ahead).
- **T6:** per-surface; §6.2 binds everywhere; T6-luma consumes the §6.1 engineering inputs
  in-lane; booking-state language matrix (`07`) binds the booking surface too.
- **Parked, unchanged:** Dependabot (both repos), Codex branch, live theme toggle, `ds-shots/`,
  stale-branch cleanup.

---
*T1 record. Commit to kingdom-docs `docs/studio-suite/decisions/` in isolation. T1 closes when
this file and `knowledge/projects/studio-suite.md` are both committed and pushed.*
