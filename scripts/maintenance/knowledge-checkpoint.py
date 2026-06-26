#!/usr/bin/env python
"""Autonomous knowledge checkpoint (Req 3).

Records a project's live state into ``knowledge/projects/<slug>.state.md`` at a
green-gated clean task close. Optionally runs the quality gates first and refuses
to write unless they all pass (unless ``--assume-green`` is given because the
caller already ran them).

Newest checkpoint is written first so a future session reads the current state in
the fewest tokens (Req 1).

This script will NEVER write under ``knowledge/global/`` — that tree is
owner-approval-gated (Req 4); propose changes via ``knowledge/global/_proposals/``.

Usage:
  uv run python scripts/maintenance/knowledge-checkpoint.py \
      --slug illuminate-my-gallery \
      --summary "Priority 3 R2 adapter landed; upload-intent endpoint next." \
      --gate "uv run ruff check ." --gate "uv run mypy" --gate "uv run pytest -q"

  # When you have already run the gates yourself:
  uv run python scripts/maintenance/knowledge-checkpoint.py \
      --slug kingdom --summary "..." --assume-green

  --repo PATH   repo whose branch+SHA is recorded in the entry (default: Kingdom root)
  --dry-run     print the entry that would be written; touch nothing
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

CHECKPOINT_MARKER = "<!-- CHECKPOINTS -->"
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


@dataclass(frozen=True)
class GateResult:
    """Outcome of a single gate command."""

    command: str
    passed: bool


def find_kingdom_root(start: Path) -> Path:
    """Locate the Kingdom root (the dir that owns ``knowledge/projects``).

    Honours ``$KINGDOM_ROOT`` first, then walks upward from ``start``.
    """
    env_root = os.environ.get("KINGDOM_ROOT")
    if env_root:
        return Path(env_root).resolve()
    for candidate in (start, *start.parents):
        if (candidate / "knowledge" / "projects").is_dir():
            return candidate.resolve()
    raise SystemExit(
        "could not locate Kingdom root (no knowledge/projects found upward "
        "and $KINGDOM_ROOT unset)"
    )


def git_ref(repo: Path) -> str:
    """Return ``<branch> @ <short-sha>`` for ``repo``, or a placeholder."""

    def run(args: list[str]) -> str | None:
        try:
            out = subprocess.run(
                ["git", "-C", str(repo), *args],
                capture_output=True,
                text=True,
                check=True,
            )
        except (OSError, subprocess.CalledProcessError):
            return None
        return out.stdout.strip()

    branch = run(["rev-parse", "--abbrev-ref", "HEAD"]) or "?"
    sha = run(["rev-parse", "--short", "HEAD"]) or "?"
    dirty = run(["status", "--porcelain"])
    suffix = " (dirty)" if dirty else ""
    return f"{branch} @ {sha}{suffix}"


def run_gates(gates: list[str], cwd: Path) -> list[GateResult]:
    """Run each gate command in ``cwd``; return results in order."""
    results: list[GateResult] = []
    for command in gates:
        print(f"  gate: {command}", file=sys.stderr)
        completed = subprocess.run(command, shell=True, cwd=str(cwd))
        results.append(GateResult(command=command, passed=completed.returncode == 0))
    return results


def render_entry(
    *,
    timestamp: str,
    ref: str,
    gate_results: list[GateResult],
    summary: str,
) -> str:
    """Render a single checkpoint block (newest-first ordering applied by caller)."""
    if gate_results:
        gates_line = ", ".join(
            f"{r.command} {'OK' if r.passed else 'FAIL'}" for r in gate_results
        )
    else:
        gates_line = "asserted green by caller (--assume-green)"
    return (
        f"## {timestamp} — {ref}\n"
        f"- gates: {gates_line}\n"
        f"- {summary.strip()}\n\n"
    )


def state_header(slug: str) -> str:
    """Header written once when the state file is first created."""
    return (
        f"# {slug} — live state (autonomous checkpoint log)\n\n"
        "> Maintained by `scripts/maintenance/knowledge-checkpoint.py` at each "
        "green-gated clean task close (Req 3).\n"
        "> Newest checkpoint first. Control-plane knowledge — not project "
        "business data.\n\n"
        f"{CHECKPOINT_MARKER}\n"
    )


def upsert_entry(state_file: Path, slug: str, entry: str) -> None:
    """Insert ``entry`` immediately after the marker (newest-first)."""
    if state_file.exists():
        text = state_file.read_text(encoding="utf-8")
        if CHECKPOINT_MARKER not in text:
            text = text.rstrip() + f"\n\n{CHECKPOINT_MARKER}\n"
        head, _, tail = text.partition(CHECKPOINT_MARKER)
        new_text = f"{head}{CHECKPOINT_MARKER}\n{entry}{tail.lstrip(chr(10))}"
    else:
        new_text = state_header(slug) + entry
    state_file.write_text(new_text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Autonomous knowledge checkpoint (Req 3).")
    parser.add_argument("--slug", required=True, help="project slug (a-z0-9-)")
    parser.add_argument("--summary", required=True, help="what closed / what is next")
    parser.add_argument(
        "--gate",
        action="append",
        default=[],
        metavar="CMD",
        help="quality-gate command to run (repeatable); all must pass",
    )
    parser.add_argument(
        "--assume-green",
        action="store_true",
        help="skip running gates; caller asserts they passed",
    )
    parser.add_argument(
        "--repo",
        default=None,
        help="repo whose branch+SHA to record (default: Kingdom root)",
    )
    parser.add_argument("--dry-run", action="store_true", help="print, write nothing")
    args = parser.parse_args()

    slug: str = args.slug
    if not SLUG_RE.match(slug):
        raise SystemExit(f"invalid slug {slug!r} (expected ^[a-z0-9][a-z0-9-]*$)")

    kingdom_root = find_kingdom_root(Path.cwd())
    projects_dir = kingdom_root / "knowledge" / "projects"
    state_file = (projects_dir / f"{slug}.state.md").resolve()

    # Hard guard: never escape knowledge/projects, never touch knowledge/global.
    if projects_dir.resolve() not in state_file.parents:
        raise SystemExit("refusing to write outside knowledge/projects/")

    repo = Path(args.repo).resolve() if args.repo else kingdom_root
    gate_results = (
        [] if args.assume_green else run_gates(list(args.gate), cwd=repo)
    )
    failed = [r.command for r in gate_results if not r.passed]
    if failed:
        print("\nNOT GREEN — checkpoint aborted, nothing written. Failing gates:")
        for command in failed:
            print(f"  ✗ {command}")
        return 1
    if not args.assume_green and not gate_results:
        print(
            "refusing to checkpoint with no gates and no --assume-green "
            "(pass --gate ... or --assume-green)",
            file=sys.stderr,
        )
        return 2

    timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = render_entry(
        timestamp=timestamp,
        ref=git_ref(repo),
        gate_results=gate_results,
        summary=args.summary,
    )

    if args.dry_run:
        print(f"--- DRY RUN: would prepend to {state_file} ---")
        print(entry, end="")
        return 0

    projects_dir.mkdir(parents=True, exist_ok=True)
    upsert_entry(state_file, slug, entry)
    print(f"checkpoint written: {state_file.relative_to(kingdom_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
