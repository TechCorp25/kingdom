---
title: "Domain boundaries — what this layer governs, and what it must not do"
source: "§3 + §9 of the Kingdom orchestrator manual"
---

# What the Kingdom orchestrator governs (§3)

Distinguish **environment-level** concerns (this orchestrator's domain) from **project-level** product work
(a project orchestrator's domain). This layer owns:

- **The knowledge base** — `knowledge/global/`, `policies/`, `projects/`, `skills/`. Curation is **additive and
  owner-gated**. Global-knowledge promotion is a deliberate flow: stage proposals under
  `knowledge/global/_proposals/`, promote via explicit **`git mv`**, owner-approved — never write straight into
  `global/`. The `.claude/` hooks (`block-global-knowledge`, `block-global-bash`) enforce this; work with them.
- **Policies** — authoring/refining the `knowledge/policies/` set so it layers cleanly with CLAUDE.md and with
  per-project orchestrator prompts. When a policy changes, check it doesn't contradict a project orchestrator's
  standing rules; reconcile rather than run two rulebooks.
- **The `.claude/` automation** — hooks, skills, `settings.json`. Treat as infra: surface changes as decisions;
  never let CC silently rewrite a hook or settings file.
- **Environment hygiene & maintenance** — recurring audited passes (toolchain/version alignment, dependency
  drift, env/secret hygiene, config correctness). Run via `/automate-dev` with a green gate
  (`ruff`/`mypy --strict`/`pytest`) and a written checkpoint. Treat "grep-confirmed" as **not**
  "runtime-confirmed" (note it explicitly when a runtime check was skipped).
- **Cross-project governance** — the project registry (`register-projects.py`), the `docs/<slug>/` layout and
  retention rule, the `projects/` state files. The **boundary rule**: project repos are **separate** and
  **carved out of Kingdom auto-push** (`run-close.md`). This orchestrator governs the environment they live in;
  it does not reach into a project's application logic.
- **Dependency/Dependabot passes** — a deliberate own pass, queued separately, never folded into unrelated work.
- **Decision records & interdepartmental coordination** — capture environment/governance decisions as committed
  DR documents. When a question crosses a domain boundary (another team, a rule contradiction, or authority the
  build layer lacks), the orchestrator **drafts the framed question + a reasoned recommendation for the owner to
  relay** — it directs collaboration, it does not conduct it (there is no direct channel). Breaking changes to a
  documented constraint are **evidence-triggered and gated individually**. Keep a clean distinction of work
  types (governance vs implementation vs certification vs owner-gated authority); cross-lane work is permitted
  only when explicit, supervised, and recorded.

# Things NOT to do (§9, universal)

- Don't trust CC's prose over raw git/gate output. Re-derive.
- Don't assume `main` is current — pin bases to a SHA; `git log -- <path>` before assuming a file isn't committed.
- Don't commit directly to `main`; don't reuse a squash-merged branch; don't local-merge a non-ancestor.
- Don't `git add -A`; don't hand-edit JSON/TOML brace-by-brace; don't silently change infra/automation/hook files.
- Don't write into `knowledge/global/` directly — use `_proposals/` + owner-gated `git mv`.
- Don't treat a grep-confirmed fix as runtime-confirmed; don't treat a green gate as "renders/behaves correctly."
- Don't `/compact` a high-context session; don't push security/infra-critical work past ~70–80% context.
- Don't force-push. If `--ff-only` refuses, STOP and diagnose (check which branch you're on first).
- Don't reach into a project's application code — projects are separate, carved out of Kingdom auto-push.
- Don't end a session without the versioned continuation baseline committed in isolation.
