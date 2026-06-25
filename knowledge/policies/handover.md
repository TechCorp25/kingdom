# Policy — handover before compact (Req 6)

A high-detail handover/continuation file is produced at every clean task close **and
before any context compact**, so a fresh session resumes with absolute accuracy.

## The hard rule
Monitor the context window. Keep ~15–20% in reserve to write the handover in full. **A
compact that lands before the handover exists is a continuity failure** — the most
expensive kind, because it silently loses the very state needed to continue.

## Why this is policy, not just a hook
CC does not get a reliable token meter, and a `PreCompact` hook (if the CC version fires
one) runs *as* the harness decides to compact — too late to author a faithful summary.
So the dependable mechanism is **behavioural**: write the continuation file proactively
at clean boundaries, independent of compact timing. Treat rising context as the trigger,
not an external alarm.

## How
- Invoke the `handover` skill (`/handover`) — it defines the required sections, the
  existing file-naming pattern, and the git-truth-first method. Do not invent a new
  naming scheme; the series is `docs/<area>/kingdom-continuation-<ISO8601>.md`.
- Reconstruct git state by observation (never assert an unverified SHA).
- Pull forward still-open items from the prior continuation file; the new one supersedes
  it.
- Stage ONLY the handover file, commit it in isolation, *then* it is safe to `/clear` or
  allow a compact.

## Cadence
- Clean task close → checkpoint (Req 3) + handover.
- Context getting heavy mid-task → handover now, even mid-task, then continue or `/clear`.
- Owner asks → `/handover`.

## Token discipline (Req 1)
Dense, pointer-based, total-reconstructability-per-token. Reference paths and policy docs
rather than pasting large bodies.
