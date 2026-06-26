---
title: "studio-suite — DR-001 Addendum A: §3 Downstream Resolved (Additive), Responsive-Spec Inputs Captured, and the Work-Type-Distinction Principle"
project: "studio-suite (new app dev) · Kingdom workspace"
type: "decision-record-addendum"
version: "2026-06-26T11-00-00"
owner: "TechCorp (solo developer, Melbourne AU)"
amends: "2026-06-22T20-00-00-studio-suite-DR-001-responsive-and-collaboration.md"
status: "RATIFIED. Flips DR-001 §3 status PENDING → RESOLVED (additive; zero owner-gated breaks). Adds the work-type-distinction principle (§A4)."
relates_to: "studio-suite-continuation-2026-06-22T19-30-00.md — outputs below are T5 / production §11-gate inputs."
---

# DR-001 — Addendum A

Amends DR-001. The design team's per-surface responsive remediation (the checkpoint DR-001 §3 left PENDING)
has come back. This addendum records the outcome, captures its reusable outputs, holds the one caveat that
keeps it from being over-read, and — prompted by a controlled lane-crossing in the same pass — establishes a
standing **work-type-distinction** principle.

## A1. DR-001 §3 downstream — RESOLVED additively, zero owner-gated breaks
The evidence-triggered hybrid resolved entirely to **additive**. The design team's executor ran the real §11
matrix as a headless probe — **17 surface states × 16 viewports** (portrait small incl. the mandatory **375px**
gate, landscape phone, tablet portrait + landscape, desktop, wide, **constrained-height**) — and derived
pass/fail from **measured horizontal overflow per surface**:
- **16 of 17 surfaces passed (0px overflow) → kept FROZEN, zero regression** (sign-in ×2, all client + admin
  views, both detail drawers, Luma).
- **1 surface failed** — the public landing header nav (links + theme toggle + Client Portal + Reserve-a-Date
  CTA clipped off-screen with no scroll below ~1024px) → fixed **additively**:
  - `portal/landing.jsx` — Topnav collapses links + actions into a new `LandingNavSheet` (hamburger → sheet)
    **below a measured 1152px fit floor**; desktop renders the original inline bar unchanged.
  - `foundation/styles.css` — `@media (max-width:1151px)` compact-nav rules; theme toggle hardened to
    `--tap-min` 44×44 on touch.
  - `qa/responsive-harness.html` — extended to the full §11 matrix (buildless intent proof).
  - Container-query work (DR-bundle "B-3") **deferred to the production Vite re-implementation** per the
    role-split — no §11 trigger on the passing surfaces, so deferring avoids regression risk.

**Desktop byte-identical, proven not eyeballed:** post-fix probe shows all 17 surfaces PASS, 0px overflow
everywhere; a same-run **layout-geometry parity** comparison (original vs modified) shows every element's
bounding box identical at **≥1152px** on all 17 surfaces (residual pixel diffs are only time-of-day greetings /
live dates / animated grain). **No frozen-desktop surface was touched → there were zero owner-gated breaking
changes to approve.** This is the best-case resolution of DR-001 §3: the constraint collision never forced a
break.

Evidence artifacts (in the bundle): `docs/responsive-remediation-plan-2026-06-26.md` (work plan + per-surface
verdict ledger + requirement-by-requirement adherence table), `qa/evidence/` (probe script, before/after
evidence JSON, geometry-parity JSON, before/after landing screenshots), `.automate-dev/iteration_plan.md`.

## A2. Captured as T5 / production §11-gate inputs (responsive SPEC)
These are now the responsive spec the **dev-side** gate enforces, and they de-risk T5 by handing over a
ready-made test plan:
- **The per-surface verdict ledger** (which surfaces frozen, which moved, with measured evidence).
- **The 1152px landing fit floor** and the `LandingNavSheet` collapse behaviour.
- **The extended harness** (full surface × viewport matrix) as the buildless spec.
- **Tap-target 44×44 hardening** on touch.
- **Deferred container queries (B-3)** — to be implemented in the production re-implementation, not the prototype.

## A3. Caveat held on the record — bundle PASS ≠ production §11 sign-off
Per DR-001 §2 the **binding** §11 gate runs **dev-side, in studio-suite's Vite CI, against the shipped build**.
What A1 delivered is **spec + prototype evidence**, not the production gate discharged: the buildless prototype's
rendering is not the Vite-built output (font loading, CSS processing, hydration can differ). Production
**re-implements (seed-not-dropin) and re-certifies** against the real build. "All 17 PASS" is excellent input —
it is **not** production sign-off.

Includes the **pre-existing sign-in hooks crash** ("Rendered fewer hooks than expected" on landing → sign-in,
reproduces in the *unmodified* original at 1440 and 375 — pre-existing, unrelated to responsive layout). Owner
authorized fixing it as seed hygiene. Fix must be **root-caused** (hook called conditionally / after an early
return — fix the hook-order violation, not a wrapper band-aid; production-code-quality rule), reproduce-then-
resolve verified, and logged as a **known pattern the production re-implementation must independently get right** —
fixing the prototype does not discharge production.

## A4. Work-type-distinction principle (new standing rule)
**Observation (recorded, not a reprimand):** the hooks-crash fix in A3 is **engineering-domain** work performed
by the **design team's** executor as seed hygiene — a cross-lane action. It was carried out under **explicit
owner + engineering-lead supervision** (heavily monitored — controlled, not drift).

**Principle:** keep a **clean distinction of work types**, each with its own lane and owner:
- **Design intent / visual law / responsive spec** → design team (domain owner).
- **Engineering implementation** (component logic, hooks, build, data) → dev side.
- **Certification of the shipped artifact** against intent → dev/orchestrator (the §11 gate).
- **Authority to break a ratified rule / documented constraint** → owner, gated individually.

**Rule:** cross-lane work is **permitted only when explicit, supervised, and recorded** — as A3's fix was. It
must **never be silently absorbed** across lanes, and the artifact's lane must be **tagged** so the receiving
side knows what it inherited. Reinforced by seed-not-dropin: a supervised cross-lane fix on the *prototype* does
**not** discharge the *production* lane — production re-does and re-certifies engineering work in its own lane.

**Why it matters:** the role-split in DR-001 §2/§5 only protects quality if work types stay distinguishable.
Blur without record means a later session can't tell design intent from engineering implementation from
certification — and can't tell what production still owes. A3 is the model: lane crossed, but explicit,
supervised, recorded. (Promotable to a standalone standing rule / DR-002 if cross-lane situations recur often
enough to warrant their own record.)

---
*Addendum A to DR-001. Prepared 2026-06-26T11-00-00. Commit alongside DR-001 in `docs/studio-suite/`
(or `…/decisions/`). Updates DR-001 §3 status: PENDING → RESOLVED (additive, zero owner-gated breaks).*
