---
version: 2026-06-13T10-00-00
supersedes: kingdom-continuation-2026-06-10T13-00-00.md
project: IlluminateMyGallery (IMG) — Illuminate Studios
app_repo: techcorp-DevApps/IlluminateMyGallery
kingdom_repo: TechCorp25/kingdom
local_app_dir: ~/kingdom/projects/illuminate-my-gallery   # NOTE: actual on-disk path is *-gallery, not *-studio (see §Path note)
role: Claude = orchestrator/review layer above Claude Code (no machine access; owner relays terminal/Railway output)
---

# Kingdom continuation — IMG session close 2026-06-13

## 0. First actions for the next controller session
1. Read this file fully.
2. VERIFY git state before any branch work (SHAs below are "last observed", not assumed):
   - `cd ~/kingdom/projects/illuminate-my-gallery && git fetch && git log --oneline -5 origin/main`
   - `git branch -a | grep landing`
3. Then proceed with §3 Immediate next actions.

## 1. What this session accomplished
- Confirmed login WORKS (studio admin); earlier 401s were credential mismatches; `register→400` is by-design (no self-registration). Admin pages render correctly.
- Diagnosed the gallery upload 500: missing R2 env vars on backend (not a code bug). Confirmed the exact 7 var names from `task2-handoff-brief §9` (see §4).
- LANDING — corrected a scope miss: the design-system ships a CANONICAL landing component (`design-system/components/landing.jsx`) that IS the page; the first pass only conformed styling (tokens/classes) onto the old placeholder content. Rebuilt the landing BODY to the canonical (6 sections), structurally + content correct, on a pushed branch (NOT merged). See §2/§3.
- Established (from the owner's uploaded docs) that real studio pricing is a FIVE-category schedule, NOT the canonical's 3 wedding "collections" — so the canonical Investment section is structurally placeholder. Gating prompt prepared.
- Diagnosed the empty portfolio reel: ROOT CAUSE = no portfolio data (`/api/portfolio` yields `[]`); reel renders 6 grey `<Link>` tiles by design when empty. Surfaced the deeper gap: THERE IS NO PUBLIC PORTFOLIO IMAGE PIPELINE (see §5).

## 2. Git state (LAST OBSERVED — verify)
- `main` @ `cfc86ea` — includes the first landing styling-conformance work (squash-merged this session). VERIFY tip.
- Branch `design-system/landing-canonical-body` @ `46ffe62` — canonical landing BODY rebuild. Pushed. PR open/openable. **NOT merged.** merge-tree vs origin/main was CLEAN.
- Untracked in working tree: `.automate-dev/reports/2026-06-12T11-48-19Z-portfolio-pipeline-diagnosis.md` (portfolio diagnosis — keep, commit with portfolio work).
- Prior parked untracked: Mongo #15 review report + 2 IMG docs (still uncommitted); DB_NAME Railway stopgap (still present, redundant).

## 3. Immediate next actions (mostly self-contained prompts already delivered as files)
Run order on the EXISTING `design-system/landing-canonical-body` branch, THEN merge once it looks right:
1. **Investment gating** — prompt file `2026-06-12T10-00-00-investment-section-gate-wip-automate-dev-prompt.md`. Strips placeholder collection names/prices; replaces with honest "pricing on enquiry" interim, code-flagged WIP. (Owner confirmed: gate to work-in-progress, NOT a public "WIP" banner.)
2. **Type-scale + aesthetics polish** — prompt file `2026-06-12T10-30-00-landing-typescale-aesthetics-polish-automate-dev-prompt.md`. Fixes oversized text at mobile+desktop; ADDS the canonical's shadow/elevation/glow primitives to the DS layer (additive only — deliberate loosening of the "no new tokens" rule, because faithful reproduction needs them). Touches `Landing.jsx` + `index.css` (+ maybe `tailwind.config.js`), additive only.
3. Then **squash-merge** the landing PR (owner-gated). Reel stays empty until portfolio data exists — acceptable; code is correct.

Parallel / independent:
- **R2 env vars** (owner, Railway, backend svc `098b3c91…`): set the 7 vars in §4, redeploy, re-test upload → expect `upload-intent 200`. (Full image DELIVERY also needs the Cloudflare Worker live at `media.illuminatestudios.com.au` — still unconfirmed.)
- **Portfolio empty-data discriminator (owner, 1 min):** on the deployed landing, DevTools → Network → the `/api/portfolio` request:
  - fails / wrong host / never fires → frontend wiring: `VITE_BACKEND_URL` is build-time and has no value in `frontend/railway.toml`; both pages swallow fetch errors into `[]` (the PR #16 gotcha). Fix = set the build-time var.
  - returns `200 []` → backend has no rows: lifespan seed swallows exceptions, `seed_portfolio()` runs last; any earlier failure or DB-name mismatch leaves it empty. No `published` filter exists. Fix = seed/data.

## 4. R2 backend env vars (confirmed names — set on backend svc 098b3c91…)
```
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_ENDPOINT_URL=https://{account_id}.r2.cloudflarestorage.com
R2_BUCKET_ORIGINALS=illuminate-prod-originals
R2_BUCKET_DERIVATIVES=illuminate-prod-derivatives
CLOUDFLARE_WORKER_SHARED_SECRET=...   # must match the Worker's value
```
These serve client galleries/upload. Both buckets PRIVATE; no public bucket; delivery is Worker-gated (HMAC, 4h media token). This is NOT the public-portfolio path (see §5).

## 5. KEY FINDING — no public portfolio image pipeline (architecture decision required)
`/admin/portfolio` CRUD works but image fields are bare URL text inputs. R2 has no public bucket; every image route is auth-gated private-gallery only. The studio's own photos have NO route from disk to a public URL — the seed only works via external Unsplash/Pexels URLs. So the owner's requirement ("easily add/update portfolio albums with images via admin") is NOT met.
Two tracks:
- Track 1 (fast): make the reel show data — resolve §3 discriminator (build-time var OR seed/data).
- Track 2 (own session): build the public portfolio image pipeline. Claude Code's 5 options (no recommendation made): (a) harden external-URL model; (b) new PUBLIC R2 bucket; (c) authless backend proxy over private R2; (d) public prefix in the existing Worker; (e) Mongo-blob route. Orchestrator lean (to re-weigh): (b) or (d) keep the "everything via Cloudflare" posture; (c) reintroduces backend image-serving the architecture deliberately avoids. DECIDE before building.

## 6. Workstream queue (agreed + gated this session)
1. Landing: gating → polish → merge (§3).
2. Stage B — header/`Layout.jsx` → canonical Topnav/Footer. Shared by EVERY page incl. admin → own gated pass; gate = all existing pages + controls still work, zero admin regression. New nav items (Experience/Investment/Journal) imply pages that don't exist — follow-on, do not 404 silently.
3. Portfolio: Track 1 fix, then Track 2 pipeline (§5).
4. Workstream 1 — pricing as managed data: extend services/packages model to the real 5-category schema (category/package/price/coverage/deliverables/add-ons), seed once from the Package Schedule doc, admin-manage, wire landing Investment + booking live. PENDING DECISION: docs stay canonical source (re-import) vs admin becomes canonical after first seed.
5. Workstream 2 — contracts/consent/waivers (review-gated; legal stakes): 5 agreement templates + Package Schedule + Marketing/Portfolio Release; placeholder-fill per booking, deliver, sign; consent capture (esp. guardian/guest for childcare/school burst-access). Hooks existing `/api/contract-templates`. CAVEAT: studio's own Use Notes say these need Australian-solicitor review — build the mechanism, do NOT certify legal correctness.
6. Parked: Luma quality + safety hardening (own review-gated session, against the two Luma spec docs in project knowledge — functioning now, so hardening not fix; booking guardrails are security-adjacent → merge-readiness playbook + go/no-go). Dependabot (2 critical / 5 high). Commit the parked untracked reports; remove redundant DB_NAME stopgap.

## 7. Source-of-truth artifacts (owner-uploaded; in this project knowledge + local kingdom repo, UNPUSHED)
- Pricing: `06_..._Package_Schedule_and_Add_On_Terms` — 5 categories (Family/Anniversaries/Kids Birthdays/Events/Weddings), ~22 packages, add-ons, 10% retainer default, ACL-preserving.
- Contract pack: `01–05` per-category agreements, `00` Use Notes (incl. solicitor-review legal notice), `07` Optional Portfolio & Marketing Release (consent/waiver).
- SENSITIVITY: business-confidential; the Release governs personal/child consent. Decide deliberately where these live before committing (private repo ok, but treat as source-of-truth artifacts, not casual `git add`).

## 8. Key learnings added this session (append to standing rules)
- When a design-system folder ships a canonical page component, the conformance target is STRUCTURAL PARITY with that component — not token/class adoption. "Conform to the design system" ≠ "adopt its tokens."
- The "no new tokens / no inline styles" constraint is right for a styling-conformance pass but TOO STRICT for a faithful canonical rebuild — it silently drops legitimate canonical aesthetics (shadows/gradients). Allow ADDITIVE DS-primitive extensions (ported from spec values) when reproducing canonical depth.
- Green build ≠ renders; AND render-at-1280 ≠ renders responsively (oversized text only surfaced at real viewports). Verify mobile + desktop.
- A passing gate can still measure the wrong thing: set Phase-1 acceptance criteria from the right reference (the canonical component), or the loop faithfully achieves the wrong target.
- Public portfolio images and private client galleries are SEPARATE pipelines — never conflate; R2/Worker private path is not a public-image solution.

## 9. Standing rules (unchanged — see prior baselines)
File-based delivery only (mobile corrupts unicode). `/automate-dev` line 1 to activate the loop; its Python scripts are non-authoritative for JSX. Owner-gated merges; squash-merge + delete source branch same step; branch fresh from verified main; `--ff-only` pulls; never force-push (two-sided repo: CC + Codex). `cd` doesn't persist across CC bash — launch from project dir. git diff is truth, not CC checkboxes. Launch: `kstart` → `cd ~/kingdom/projects/illuminate-my-gallery` → `git pull --ff-only origin main` → `claude`. `/clear` not `/compact`.

## Path note
Owner referred to `illuminate-my-studio`; CC's resolved on-disk paths are all under `~/kingdom/projects/illuminate-my-gallery` and the repo is `IlluminateMyGallery`. Treating `illuminate-my-gallery` as the canonical local path. If two checkouts genuinely exist, reconcile in the next session.
