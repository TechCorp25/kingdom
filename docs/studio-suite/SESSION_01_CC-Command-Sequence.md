---
title: "SESSION_01 — Command Sequence (owner-run)"
project: "studio-suite (Kingdom workspace)"
prepared: "2026-06-15T12-30-00"
audience: "Owner — run these in the Kingdom terminal / Railway / EAS. This layer has no machine access."
rule: "Paste raw output back after each ★ step. ★ = irreversible / secret / owner-gated."
---

# Command Sequence — Session 01

Phased to interleave with the two CC build tasks. Run a phase, paste raw output back, wait for the
re-derivation before the next ★ step. SSH remotes only (HTTPS push is dead). Never `git add -A`.

---

## Phase 0a — repo genesis  (before any CC)

```bash
kstart                                            # postgres + ssh-add + status (source it)
ssh -T git@github.com                             # expect: Hi TechCorp25!

mkdir -p ~/kingdom/projects/studio-suite
cd ~/kingdom/projects/studio-suite                # LAUNCH EVERYTHING FROM HERE
git init -b main
```

Create the empty remote — **pick ONE**:

```bash
# A) GitHub CLI, if `gh` is installed & authed:
gh repo create techcorp-DevApps/studio-suite --private --description "studio-suite — studio management + client portal (web + Expo) " 

# B) No gh: create the empty repo at github.com (org techcorp-DevApps, name studio-suite, Private,
#    NO readme/gitignore/license — keep it empty), then just add the remote below.
```

```bash
git remote add origin git@github.com:techcorp-DevApps/studio-suite.git
git commit --allow-empty -m "Initial commit"      # seeds main so CC can branch + PR off it
git push -u origin main                            # ★ first push
git log --oneline -1                               # ← paste this back
```

Register as a kingdom tracked project (from `~/kingdom`):

```bash
cd ~/kingdom
uv run python scripts/maintenance/register-projects.py --dry-run studio-suite   # preview
uv run python scripts/maintenance/register-projects.py studio-suite             # apply
cd ~/kingdom/projects/studio-suite
```

> **Note on .gitignore:** intentionally not created here. CC's first sub-task in 01.0.0 writes
> `.gitignore` / `.gitattributes` / `.env.example` and stages them by explicit path, so the tree is
> protected from the first real PR onward. CC never `git add -A`, so the empty `main` is safe meanwhile.

---

## Phase 1 — CC task 01.0.0  (paste the prompt, then drive the gate loop)

```bash
cd ~/kingdom/projects/studio-suite
git pull --ff-only origin main
git log --oneline -3                               # confirm tip = the Initial commit SHA
claude                                             # confirm model = Opus 4.8 BEFORE pasting
```

In CC: open / paste `InstructionalPrompt_01.0.0.md` as the **first** message. Approve files
**option 1 (file-by-file)**. At every CC gate, run and paste back:

```bash
git diff --stat origin/main HEAD                   # ← the truth, not CC's checkboxes
git diff --name-only origin/main HEAD
git status --short
```

When 01.0.0 is reviewed GO, open the PR and squash-merge (★ two clicks: green button → **Confirm**),
**deleting the branch in the same step**. Then:

```bash
git checkout main && git pull --ff-only origin main
git log --oneline -3                               # ← paste: confirm the squash landed on main
```

---

## Phase 0b — Railway hookup  (after 01.0.0 is on main)

Do this in the Railway dashboard (UI), not the terminal:

1. New project → **Deploy from GitHub repo** → `techcorp-DevApps/studio-suite`.
2. Add service **backend** → settings → **Root Directory** `/backend`; build/start from `backend/railway.toml`.
3. Add service **web** → **Root Directory** `/web`; confirm build command keeps `npm ci --include=dev`
   and serves `npx serve -s build`.
4. ★ **Variables** (secrets — never in git): `MONGODB_URI`, `MONGODB_DB_NAME`,
   `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_ORIGINALS`,
   `R2_BUCKET_DERIVATIVES`, and the CORS origin/regex var the backend reads.
5. ★ Trigger the first **production** deploy from `main`. Paste the BUILD log back — confirm the web
   service installed dev deps and Vite ran (no `vite: not found`).
6. Open a throwaway PR on GitHub → confirm Railway creates a **preview deployment** → load it →
   confirm the preview frontend reaches the preview backend (no failing `OPTIONS` preflight).
7. Copy the two **service ids** and the two deploy URLs — paste back (they go into the baseline §1).

---

## Phase 2 — CC task 01.1.0  (mobile + EAS OTA)

```bash
cd ~/kingdom/projects/studio-suite
git pull --ff-only origin main
claude                                             # Opus 4.8
```

Paste `InstructionalPrompt_01.1.0.md` as message one. Same gate loop (raw diff back at each gate).
PR → squash-merge → delete branch → pull main.

---

## Phase 0c — EAS hookup + OTA proof  (after 01.1.0 is on main)

```bash
cd ~/kingdom/projects/studio-suite/mobile
npx eas-cli login                                  # if not already
eas init                                           # ★ creates remote EAS project — owner-gated
eas update:configure                               # wires EAS Update channels into the app
```

Then run a development build and prove OTA:

```bash
eas build --profile development --platform android # (and ios if dual-target)
# install the build on a device/emulator, open it once
eas update --branch development --message "OTA smoke test"   # ★ publish an update
# reopen the app → confirm it pulls the update over-the-air
eas project:info                                   # ← paste: project id + slug for the baseline
```

> EAS Build runs cloud-side, so the heavy lifting isn't on the Chromebook. The `.eas/workflows/*.yml`
> committed in 01.1.0 define the development / preview / production / hotfix pipelines; trigger them
> per the `expo-cicd-workflows` skill once the smoke test passes.

---

## Phase 3 — session close

```bash
cd ~/kingdom/projects/studio-suite
git status --short                                 # ← paste: confirm clean before the baseline commit
```

This layer produces `studio-suite-continuation-<ISO8601>.md`; you then:

```bash
mkdir -p ~/kingdom/docs/studio-suite
# drop the baseline file in, then commit it IN ISOLATION:
cd ~/kingdom
git add docs/studio-suite/studio-suite-continuation-<ISO8601>.md   # ONLY this file
git status                                          # ★ verify nothing else is staged
git commit -m "studio-suite: session-01 continuation baseline"
git push
```

Then `/clear` (never `/compact`).

---

*Owner-run sequence. Pair with `SESSION_01.md` (plan) and `SESSION_01_ToDo.md` (gates).*
