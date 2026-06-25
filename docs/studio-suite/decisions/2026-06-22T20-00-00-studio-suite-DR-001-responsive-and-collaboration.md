---
title: "studio-suite — Decision Record DR-001: Responsive Validation Ownership + Frozen-Desktop/§11 Reconciliation, and the Interdepartmental-Collaboration Precedent"
project: "studio-suite (new app dev) · Kingdom workspace"
type: "decision-record + collaboration-precedent"
version: "2026-06-22T20-00-00"
owner: "TechCorp (solo developer, Melbourne AU)"
status: "RATIFIED by owner; communicated to design lead. Downstream per-surface outcomes PENDING the lead's plan + individual sign-off."
relates_to: "studio-suite-continuation-2026-06-22T19-30-00.md (the next-gen design-system pivot baseline); feeds T1 of the reset plan."
authority: "Authoritative for the specific decisions in §2–§3 and the collaboration pattern in §5. The continuation baseline wins on live state; this wins on these resolved decisions until explicitly superseded."
---

# DR-001 — Responsive validation ownership, frozen-desktop/§11 reconciliation, and the interdepartmental-collaboration precedent

## 0. Purpose & how to use this
Two architectural questions arose at the **design ↔ engineering boundary** while preparing the next-gen
design-system adoption (see the pivot baseline). Both were resolved by the owner in collaboration with the
**design team lead**. This record exists so future orchestrator sessions **inherit** these decisions rather
than re-litigate them, and so the **precedent** that the orchestrator may direct cross-domain collaboration is
preserved (§5). Read this alongside the continuation baseline; the baseline is live-state truth, this is the
resolved-decision truth.

## 1. Context
- studio-suite has **pivoted** to adopt the design team's next-generation design-system (baseline §4). The
  design team is the **upstream domain owner** of the design system, its responsive intent, and its visual law.
- The next-gen bundle ships as a **buildless CDN/Babel prototype** (no Vite build, no test runner) — it is the
  **design source of truth + intent proof**, NOT the shipped artifact.
- The shipped artifact is the **studio-suite React/Vite production app**, where requirement **§11** (fluid,
  viewport-and-orientation responsive across the continuous range; iPhone 13 mini as small-end; no dead-zones)
  binds as a **hard completion gate** (baseline §5, ratified architecture #4).
- Two questions surfaced that the build layer could not and should not resolve unilaterally. Both were put to
  the design lead **through the owner relay** (the orchestrator has no direct channel to any department — see §5).

## 2. Decision 1 — Responsive validation: role + ownership split
**Question (design lead):** The §11 requirement targets a React/Vite app with a mandatory automated responsive
harness, but the bundle is a buildless CDN prototype with no Vite build or test runner. Where should updates
land, and how should they be validated? (Options offered: retrofit bundle in-place · target the real React/Vite
repo · stand up Vite+Vitest+Playwright around the bundle · other.)

**Resolution (ratified):** §11 is a property of the **production studio-suite React/Vite app**, not of the
buildless reference bundle. Split by role:

- **Design side (lead's deliverable):** Extend `qa/responsive-harness.html`; **keep it buildless**. The four
  added cases — landscape, tablet-landscape, wide-desktop, **constrained-height** — are accepted (constrained-
  height is the split-screen / landscape-phone case most work misses). Its role is the **responsive SPEC**: it
  defines the viewport + orientation **matrix** and the design intent. It is **not** the acceptance gate.
- **Production side (dev/orchestrator):** The automated §11 gate is a **Playwright suite in studio-suite's
  Vite app, in CI**, run against the **shipped build** across the harness matrix (fluid, both orientations,
  mini small-end, no dead-zones). Authored on the dev side as each surface lands (T5/T6).
- **Rejected — bundle retrofit-in-place / wrapping the prototype in throwaway Vite+Vitest+Playwright:** builds
  infrastructure around the disposable reference, not the product. (Note: adding Playwright to *studio-suite* is
  warranted, real production infra — it belongs in the production repo, owned by dev, not bolted to the prototype.)
- **Rejected — handing the design lead the production repo to retrofit:** role-boundary error. Design specs the
  matrix; dev certifies the app against it.
- **Seed-not-dropin:** the bundle's `portal/*.jsx` and `showcase/*.jsx` are **re-implemented as real Vite/React
  components** in `apps/web` — not copied in. Same seed relationship the landing has to its retained `Landing.jsx`.

**Principle established:** *Design specs intent (the matrix / "what good looks like"); the dev/orchestrator side
certifies the shipped artifact against it (the gate); the bundle stays source-of-truth + intent-proof.* Each side
owns its half.

## 3. Decision 2 — Frozen-desktop vs §11 fluid: scope + authority
**Question (design lead):** Full fluid/intrinsic adherence (§3/§4: `auto-fit/minmax` primary, non-device
breakpoints) reverses the documented **frozen-desktop / "no auto-fit"** hard constraint and changes the desktop
layout. How far may I go? (Options offered: additive-only keep frozen desktop · full adherence permit desktop
change · hybrid per-surface · other.)

**The real collision (named):** Two ratified rules contradict. §11 demands intrinsic fluid layout; the design
system documents a **frozen-desktop / "no auto-fit"** hard constraint, and **additive-only / no-breaking-changes**
is a standing rule. Full intrinsic adherence **is** a breaking change to frozen-desktop at desktop widths — both
cannot be fully satisfied. This is **owner-gated**, not the design team's or CC's to resolve unilaterally.

**Resolution (ratified): Hybrid, evidence-triggered.**
- Additive-only alone can **under-deliver §11** (a frozen desktop with a dead-zone anywhere in the matrix leaves
  a gap §11 forbids). Full adherence **over-delivers into breakage** (blanket desktop reflow on surfaces
  deliberately frozen that already render correctly). Hybrid is the only honest fit.
- **The decision per surface is evidence-triggered, not taste:** the test is *"does the frozen desktop produce a
  dead-zone or failure anywhere in the §11 viewport matrix?"*
  - **Passes** the harness across the full range + both orientations, no dead-zone → **stays frozen** (zero
    regression; no reason to break a working surface).
  - **Fails** → that demonstrated failure is the **authorization** to move **that surface** to intrinsic.
- **Each desktop-affecting change is reported and signed off individually, before any code.**
- **Per-surface justification required:** for each surface kept frozen or moved, the lead states **why it is
  frozen**. If the constraint exists for a reason beyond "hand-tuned desktop" (e.g. print/export fidelity, a
  fixed-canvas dependency), that reason may make the surface **ineligible for intrinsic even with a dead-zone** —
  in which case the fix is a **different design, not auto-fit**. The owner approves against the **real reason**,
  not the symptom.

**Net answer:** *As far as the §11 matrix demonstrably requires on each surface, no further — additive/frozen
wherever it passes, intrinsic only where it provably fails, each break gated individually.*

**Status of downstream:** PENDING the design lead's **per-surface plan with justifications**; each frozen→intrinsic
break is approved one at a time. That plan is the **next real checkpoint before any responsive code.**

## 4. Consequences for the reset plan (feeds T1)
Beyond the three T1 decisions already queued (Option-1 topology, contracts/policy placement, responsive-gate wording):
1. **Responsive-gate wording — two-part + reconciliation clause.** The gate is: *the (extended) harness defines
   the viewport/orientation matrix (spec); the acceptance gate is a Playwright suite run against the production
   Vite build in CI.* PLUS a **frozen-desktop reconciliation clause**: the gate is satisfied by **passing the
   matrix**, NOT by mandating intrinsic layout everywhere — a frozen surface that passes is compliant; intrinsic
   is required only where frozen provably fails. Without this clause, §11 and the frozen-desktop constraint stay
   in open contradiction and CC hits the wall mid-build.
2. **Production responsive suite is a real T-task.** Stand up Playwright in studio-suite's CI (legitimate prod
   infra studio-suite lacks today) — slot into T5 (lands with the first responsive surface, the landing) or as a
   small dedicated CI task just ahead of it. Distinct from the rejected throwaway-around-the-prototype.
3. **Seed-not-dropin** for `portal/*.jsx` / `showcase/*.jsx` — re-implement as real Vite/React in `apps/web`;
   record in T1 so no one expects the prototype JSX to drop into the production tree as-is.
4. **Frozen-desktop / "no auto-fit" is now a named owner-gated decision surface** — not settled background. Record
   it in T1 as *under controlled, per-surface, evidence-triggered, justification-backed exception* (neither
   inviolable nor freely overridable).

## 5. The interdepartmental-collaboration precedent (generalised — reusable)
This exchange sets a standing precedent for how the orchestrator handles questions that cross a domain boundary.

**The orchestrator may call for / direct interdepartmental collaboration when:**
- a question touches a **domain owned by another team** (design intent, brand, legal, infra) that the build layer
  shouldn't decide unilaterally;
- a question reveals a **contradiction between ratified rules** (as in §3); or
- resolving it requires **authority the build layer does not have** (e.g. breaking a documented hard constraint).

**How it operates (relay-mediated — fidelity point):** The orchestrator has **no direct channel** to any
department. It *identifies* the cross-domain question, *drafts* the framing (the question + options + a reasoned
recommendation), and **the owner relays** it to the department lead and relays the reply back — exactly as the
owner is the sole relay to the machine. The orchestrator **directs** the collaboration; it does not conduct it.

**The role-split principle that should govern such collaborations:**
- the **domain owner specs intent** (e.g. design specs the responsive matrix / visual law);
- the **dev/orchestrator side certifies** the shipped artifact against that intent (the automated gate);
- the **owner gates** any change that breaks a ratified rule or documented constraint, **individually**.

**Framing discipline carried from the standing rules:** put cross-domain questions as **decisions with options +
the orchestrator's reasoned recommendation** (not open-ended asks); keep **domain-spec** calls with the domain
owner, **certification** on the dev side, and **breaking-change authority** owner-gated; make breaking changes
**evidence-triggered** (a demonstrated failure), not preference; and require the domain owner to **state the
reason** behind any constraint being kept or broken, so the owner approves against the real reason, not the symptom.

**Precedent value:** a future orchestrator session encountering a cross-domain or contradiction-of-rules question
should treat "draft the question for the owner to put to the relevant department lead" as a **sanctioned, expected
move** — not scope creep, and not something to absorb or guess at.

---
*DR-001. Prepared 2026-06-22T20-00-00. Commit to kingdom-docs project source under `docs/studio-suite/`
(or `docs/studio-suite/decisions/` if ADR-style separation is preferred). Pairs in spirit with the
2026-06-22T19-30-00 continuation baseline; both feed T1.*
