---
title: "SESSION_01 ToDo — studio-suite"
project: "studio-suite (Kingdom workspace)"
prepared: "2026-06-15T12-30-00"
legend: "[O] owner-run · [CC] Claude Code · [ORCH] this layer · ★ = irreversible, owner-gated"
---

# SESSION_01 — ToDo

Ordered. Do not skip a gate. Tick as you go; the **committed git diff is the truth**, not these boxes.

## A — Phase-0 gate: ratify before anything runs
- [ ] [O] Confirm repo: `techcorp-DevApps/studio-suite`, branch `main`.
- [ ] [O] Ratify mobile platforms — **iOS + Android** (vs Android-only).
- [ ] [O] Ratify mobile location — **`~/kingdom/projects/studio-suite/mobile/`** (vs `~/app-work/`).
- [ ] [O] Acknowledge web↔native sharing will likely use the `use-dom` skill (decided for real in S02).

## B — Phase 0a: repo genesis  ★
- [ ] [O] `kstart` (sources postgres + ssh-add; expect `Hi TechCorp25!` on `ssh -T git@github.com`).
- [ ] [O] `mkdir -p ~/kingdom/projects/studio-suite && cd ~/kingdom/projects/studio-suite`.
- [ ] [O] `git init -b main`.
- [ ] [O] ★ Create the empty remote (`gh repo create …` **or** GitHub web), private.
- [ ] [O] ★ Add SSH remote + empty initial commit + push `main`.
- [ ] [O] Register studio-suite as a kingdom tracked project (`register-projects.py`).
- [ ] [ORCH] Confirm `git log --oneline` tip + remote from owner's pasted raw output.

## C — Phase 1: CC task 01.0.0 (backend + web + Railway CD + CI)
- [ ] [O] Launch `claude` **from the project dir**; confirm model = Opus 4.8.
- [ ] [O] Paste `InstructionalPrompt_01.0.0.md` as message one (file, not paste-of-paste — open the file in CC).
- [ ] [CC] `/automate-dev` foundation scaffold; **file approval option 1** at every gate.
- [ ] [O] At each CC gate, paste back CC's report **+** `git diff --stat origin/main HEAD` **+** `git diff --name-only`.
- [ ] [ORCH] Re-derive from raw diff vs the 01.0.0 completion gate; recommend; flag anything inconsistent.
- [ ] [O] Open PR; [ORCH] review branch against the gate (pinned to the branch SHA, not "main").
- [ ] [O] ★ Squash-merge to `main` (**two clicks**: green button → Confirm) **and delete the branch** in the same step.

## D — Phase 0b: Railway hookup  ★
- [ ] [O] Create Railway project; link the `studio-suite` repo.
- [ ] [O] Create **backend** service, root `/backend`; **web** service, root `/web` (publish `build/`).
- [ ] [O] Set build commands from the merged `railway.toml`s (web keeps `--include=dev`).
- [ ] [O] ★ Set env vars / secrets: `MONGODB_URI`, `MONGODB_DB_NAME`, R2 creds + bucket names, CORS regex. **Never commit these.**
- [ ] [O] ★ Trigger the first **production** deploy from `main`; paste the BUILD log back.
- [ ] [ORCH] Confirm the web build installed dev deps and Vite ran (watch for `vite: not found`).
- [ ] [O] Open a throwaway PR → confirm a **preview deployment** appears; load it.
- [ ] [O] Confirm preview frontend → preview backend works (no CORS/preflight failure on `OPTIONS`).
- [ ] [O] Record both Railway **service ids** + the two deploy URLs (go into §1 of the baseline).

## E — Phase 2: CC task 01.1.0 (mobile + EAS OTA)
- [ ] [O] Fresh `claude` session from the project dir; paste `InstructionalPrompt_01.1.0.md`.
- [ ] [CC] Read the `expo-*` skills first; scaffold the Expo app + `eas.json` + `.eas/workflows/*`.
- [ ] [O] Same gate loop: paste CC report + raw diff; [ORCH] re-derive + recommend.
- [ ] [O] ★ PR → squash-merge to `main` + delete branch.

## F — Phase 0c: EAS hookup + OTA proof  ★
- [ ] [O] ★ `eas init`; link the project (owner-gated — creates remote EAS project state).
- [ ] [O] Configure Update channels (development / preview / production).
- [ ] [O] Run a **development build**; install it on a device/emulator.
- [ ] [O] ★ Publish an **EAS Update**; confirm the running build pulls it **OTA**.
- [ ] [O] Record the EAS project id + channels (go into the baseline).

## G — Phase 3: session close (§7)  ★
- [ ] [O] Commit any verified work at the clean boundary first (nothing left uncommitted).
- [ ] [ORCH] Produce `studio-suite-continuation-<ISO8601>.md` (exact SHAs, open items, verify-live cmds, owner decisions, standing rules).
- [ ] [O] ★ Commit it **in isolation** to `~/kingdom/docs/studio-suite/` (stage ONLY that file; `git status` to verify); push.
- [ ] [ORCH] Produce paired `<ISO8601>-studio-suite-orchestrator-handoff.md`.
- [ ] [O] `/clear` (not `/compact`).
- [ ] [O] Update the kingdom continuation baseline's tracked-projects table to include studio-suite (next kingdom close).

---

**Stop-and-hand-off trigger:** if CC context passes ~70–80% before Section G — especially on
anything auth/security-adjacent — stop at the nearest clean boundary, commit, and produce a
**mid-task** handoff naming the single open thread. Do not `/compact` to push through.
