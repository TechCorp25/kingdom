---
title: "studio-suite — Continuation Baseline (Source of Truth)"
project: "studio-suite (Kingdom workspace)"
version: "2026-06-22T19-30-00"
owner: "TechCorp (solo developer, Melbourne AU)"
supersedes: "studio-suite-continuation-2026-06-19T03-00-00.md"
status: "CLEAN PIVOT — 01.0.1b landing close-out ABANDONED (superseded). Next-gen design-system reset is the new line. T1 is the first task."
baseline_location: "~/kingdom/docs/studio-suite/"
note: "Secrets never live here — values are in gitignored .env / Railway Variables only."
---

# studio-suite — Continuation Baseline

Authoritative state as of 2026-06-22T19-30-00 (Melbourne). Where this conflicts with any older note or
the 2026-06-19 baseline, **this wins**. This is a **clean architectural-pivot boundary**: the 01.0.1b
pixel-fidelity close-out is deliberately abandoned (not failed — superseded by the next-gen design-system
that the design team delivered). No code work is mid-flight. The next session starts the **design-system
reset** at task **T1** (§5).

---

## 1. Identity & environment (unchanged)
- Owner: TechCorp, Melbourne AU. Machine: ChromeOS Crostini (Penguin), user `techcorp2024`.
- Workspace `~/kingdom` (native btrfs); never `/mnt/chromeos/*` (FUSE).
- GitHub org `techcorp-DevApps`; app repo `git@github.com:techcorp-DevApps/studio-suite.git`.
  Kingdom docs repo `git@github.com:TechCorp25/kingdom.git`. SSH key `~/.ssh/id_ed25519` (passphrase);
  SSH remotes only. `kstart` = postgres + ssh-add + status (NOT visible to non-interactive `bash`
  subprocesses — enter the SSH passphrase manually when running scripts, or `kstart` in the shell first).

## 2. Project facts (LOCKED — unchanged from prior baselines)
| Field | Value |
|---|---|
| Repo / branch | `techcorp-DevApps/studio-suite` · `main` |
| Dir | `~/kingdom/projects/studio-suite/` |
| Topology | Monorepo: `backend/` · `web/` · `mobile/` · `packages/tokens/` (`@is/tokens`) · `design-system/` (canonical) |
| Stack | Backend FastAPI + Motor; web Vite + React 19 + Tailwind + shadcn (publishes `web/build/`); mobile native Expo + RN (EAS), iOS + Android (**Architecture B** — native consumes `@is/tokens`); MongoDB Atlas; Cloudflare R2 private + Worker/CDN |
| Hosting | Railway (backend + web). Web service `a3b1e95d-d9ea-41b9-92c8-15c7f71c2837` → `studio-suite-preview.up.railway.app`. Mobile via EAS. |
| Package mgr | pnpm 10 workspace. `pnpm -F @is/tokens build`, `pnpm -F studio-suite-web build/dev` |
| CC model | Opus 4.8 (re-select if Fable 5 is default & unavailable) |

## 3. Git state (verified this session — re-derive at next start, never trust this verbatim)
- **`main` = `2014e2b`** "fix(tokens): correct light brand.gold to brass #a8884f (#5)". HEAD = origin/main, clean.
  Lineage: `2014e2b` → `0ded334` (tokens package #3) → `42b1a0b` (railway.toml).
- **`feature/landing-fidelity` = `0e834d5`** (local + origin) — PR #4, forked off `0ded334`. **RETAINED as the
  landing seed (§4). Do NOT delete.**
- **Codex** `origin/codex/set-up-automated-git-workflows-with-codex` = `979e1da` — deferred, do NOT merge.
- **Stale leftover** `fix/tokens-light-gold-brass` (local + origin) — squash-merged source of PR #5; content
  fully in `2014e2b`; non-ancestor "do not reuse" snare. OPTIONAL gated cleanup still pending (verified-safe
  delete script exists: empty diff vs main → `-D` + `push --delete`).
- **Kingdom docs** `git@github.com:TechCorp25/kingdom.git` = `ddf05c5` (the 2026-06-19T03-00-00 baseline commit).
  THIS baseline + paired handoff advance it next.

## 4. ★ THE PIVOT — why 01.0.1b is abandoned, and PR #4's fate
The design team delivered the **next-generation design-system** as a zip (`~/studio-suite/update-design-system.zip`,
unzipped read-only to scratch `~/ds-incoming-review/illuminate-design-system/`; **NOT in the repo**). It is the
ratified destination for tokens, the landing, responsive behaviour, and the portal surfaces. Characterisation
(read-only diffs this session) established:
- **Resolved brand-gold base is IDENTICAL** to current `main`: light `--brand-gold` = `#a8884f` (brass),
  dark = `#c9a96e` (champagne). The brass correction on `main` already agrees with the new system — no colour loss.
- The new `tokens.ts` is restructured (281→389 lines): **two-ramp gold** (`goldBrass`+`goldChampagne`, same
  resolved base), a `--gold-*/--ink-*/--bone-*` **scale-var system** with sage-inversion, and **gold gradients
  promoted into the token layer**. Light `goldHover` refined `#c9a96e`→`#b89868` (deliberate consistency fix).
- The fidelity target `landing.jsx` itself was revised (672→666 lines — a revision, not a rewrite).
- Bundle also carries `portal/` (client, admin, booking, pricing, profile, luma, app, data), `qa/` (incl.
  **responsive-harness.html** — the responsive design the parked 01.0.2 was waiting on), plus `contracts/`
  and `policy/` (placement question — §6).

**Consequence:** any further work on the *current* foundation is double-migration. The 01.0.1b polish-to-fidelity
pass targets a `landing.jsx`/`.btn` reference the new system already supersedes → abandoned. The pivot is *less*
total work than finishing then redoing.

**PR #4:** **close UNMERGED** (owner-gated, GitHub). No interim public landing is needed — it has no
functionality, would be a retired example only. **`feature/landing-fidelity` @ `0e834d5` is RETAINED** because
`web/src/pages/Landing.jsx` (+ `landing.css`) lives ONLY on that branch (never merged) and is the **seed** for
the new-gen landing build (T5). Delete the branch ONLY after T5 has consumed the seed.

## 5. The reset plan (decomposed — each its own gated task; this is the remaining-work ledger)
> One task per CC session, `/automate-dev` line one for build work, file approval option 1, files-not-paste,
> stage by explicit path, dual-repo verify before authoring. Each lands via its own branch → PR → squash.

- **T1 — Ratify & scope (docs/decision; this boundary partly does it).** Lock the architecture decisions (§ below),
  resolve the `contracts/`/`policy/` placement question (§6), and write the **responsive acceptance gate** concretely.
- **T2 — Stand up the next-gen design-system in the repo.** Place the bundle into the repo's `design-system/`
  structure; perform the **global IlluminateMyGallery/"Illuminate" → studio-suite rename** (legacy brand naming
  only — swap everywhere); triage out anything ruled out-of-scope in T1. Own branch/PR.
- **T3 — Re-sync `@is/tokens`** to the new contract: two-ramp gold, scale-vars emitted, **brand/semantic gold
  gradients emitted from tokens**. Keep the two byte-identical `tokens.ts` copies in lockstep if that pattern
  persists. Architecture-sensitive; verify the emitted CSS contract.
- **T4 — Rewire the web foundation** to consume the new vars (`index.css`/`main.jsx`/`tailwind.config.js`).
  Gradients consumed via **plain CSS** (`background-image: var(--gold-fill-grad)`), **never** Tailwind
  arbitrary-value `bg-[var(--…)]` (mis-parses a composite var — same failure mode as `shadow-[var(--x)]`).
- **T5 — Landing (absorbs old 01.0.1b + 01.0.2).** Build the landing **fluidly responsive** (§ responsive gate),
  faithful to the new `landing.jsx`, **seeded** from the retained `feature/landing-fidelity` `Landing.jsx`.
  Then retire `feature/landing-fidelity`.
- **T6 — Portal surfaces**, incrementally, each its own task (client, admin, booking, pricing, profile, luma,
  app, data).
- **Then native** (Expo/RN) consuming the re-synced `@is/tokens`.

### Ratified architecture (T1 locks these; confirmed with owner this session)
1. **Gradients-in-tokens — ADOPT, scoped.** Brand/semantic gold gradients (`gold-text`, `gold-fill`) are tokens;
   bespoke decorative gradients may remain web-local. Reverses the old "tokens colour-only, gradients web-local"
   rule deliberately. Justified: brass-flip propagation, per-theme correctness, web↔native parity (two consumers).
   Gradients are visually final (real-world tested) → no republish-churn cost.
2. **Two-ramp gold — ADOPT.** `goldBrass`+`goldChampagne`; resolved base identical to `main` → zero visual delta.
3. **Scale-var CSS system — ADOPT.** It is the contract the new `landing.jsx`/portal surfaces are authored against.
4. **Fluid responsive web — HARD completion gate (not "mobile responsive").** Vite web must render **seamlessly
   across the continuous viewport range AND both orientations** — tablets and small handsets incl. **iPhone 13
   mini (375pt portrait)** as the explicit small-end gate. Driven by intrinsic CSS (clamp fluid type/space,
   container queries, flexible grid/flex); breakpoints are refinements, not the primary mechanism. **No layout
   dead-zones.** Validated against the bundle's `qa/responsive-harness.html` across the range + both orientations —
   this is a load-bearing acceptance gate, not a desktop-match check. (Professional field-use product.)
5. **Shared-token contract → native (Architecture B retained).** Colour/spacing/type **scale** crosses to native
   via `@is/tokens`; fluid responsive **layout logic** is per-platform (web = CSS breakpoints/container queries;
   native = RN dimension-driven). At T2/T3 **confirm the responsive design is scale-driven (token-backed)** so
   native inherits design intent rather than the fluid behaviour being web-local-only.

## 6. Open questions / owner-owned decisions
- **`contracts/` + `policy/` placement** (NOT ownership — "Illuminate" is just legacy brand, all in-scope after
  rename). Do legal-contract PDFs and the Luma booking-AI policy belong *inside* `design-system/`, or are they
  product/content artifacts merely co-bundled? Resolve in T1.
- **Two-copy `tokens.ts` lockstep** — confirm whether the new system keeps the dual byte-identical copies or
  consolidates. Confirm at T3.

## 7. Parked (deliberate own passes — do not fold into reset tasks)
- Dependabot: 4 alerts (1 high) on studio-suite; 9 on kingdom-docs.
- Codex `979e1da` — do NOT merge.
- Live theme toggle — likely natural to the scale-var system now; revisit during/after T4.
- `ds-shots/` committed reference renders — would have caught the gold off-by-one; revisit post-landing.
- Stale `fix/tokens-light-gold-brass` cleanup (optional, verified-safe).

## 8. Verify-live (run at next session start; re-derive — do not trust §3 verbatim)
```bash
cd ~/kingdom/projects/studio-suite
git fetch origin && git checkout main && git pull --ff-only origin main
git log --oneline -3                 # EXPECT 2014e2b at tip
git rev-parse HEAD origin/main        # EXPECT equal
git branch -a                         # EXPECT main, feature/landing-fidelity (0e834d5, RETAINED),
                                      #        codex/...(979e1da); fix/tokens-light-gold-brass may still linger
git -C ~/kingdom log --oneline -1     # EXPECT this baseline's commit at tip
curl -s -o /dev/null -w "%{http_code}\n" https://studio-suite-preview.up.railway.app   # EXPECT 200
ls ~/ds-incoming-review/illuminate-design-system 2>/dev/null   # bundle scratch (re-unzip from ~/studio-suite/update-design-system.zip if gone)
```
STOP if `main` ≠ `2014e2b`, if `origin/main` moved unexpectedly (inspect `git show --stat`), or if
`feature/landing-fidelity` is missing (the seed).

## 9. Standing rules (carried forward — non-negotiable)
- **Re-derive state from raw output; never trust CC prose.** Verify every git/file/state claim against BOTH
  connected repos (search) AND raw owner output before asserting or writing it into any artifact. (Born from
  prior false-state errors.)
- Git diff is truth, not CC checkboxes. **Green build ≠ renders** — and now "renders" means **fluid across the
  viewport range + both orientations**, validated on the harness, not a desktop screenshot.
- `/automate-dev` line one of every build prompt; one task per prompt; per-sub-task gates; file approval option 1.
- Files-not-paste for everything CC-bound (mobile unicode corruption); diagnostics as `.sh`. Stage by explicit
  path, never `git add -A`. `/clear` not `/compact`. Security-critical work not past ~70–80% context.
- Tokens are the single colour source — no hardcoded gold in web. **Brand/semantic gradients now in tokens**
  (consumed via plain CSS, never Tailwind arbitrary-value vars).
- Every irreversible step owner-gated (remote, push, env/secrets, prod deploy, EAS, squash, PR close). Two-sided
  discipline: fetch + `git branch -a` every session, `--ff-only` only, never force-push, pin bases to a SHA.

## 10. Session-close protocol (when the next clean boundary lands)
Commit at the boundary first → produce `studio-suite-continuation-<ISO>.md` superseding THIS one (record new
SHAs, advance the ledger, carry §5/§9) → commit in isolation to `~/kingdom/docs/studio-suite/` (stage only that
file; `git status` to verify) → produce the paired handoff under `…/orchestrator/` → `/clear`. Filename
timestamp = real close time.

---
*Supersedes 2026-06-19T03-00-00. Commit in isolation to `~/kingdom/docs/studio-suite/`.*
*Paired handoff: orchestrator/2026-06-22T19-30-00-studio-suite-orchestrator-handoff.md*
