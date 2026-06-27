#!/usr/bin/env python3
"""Scaffold Kingdom-orchestrator artifacts as downloadable files.

This helper ONLY writes files. It has no git, no network, and no machine access — it is the
orchestrator-layer-safe way to produce the ISO-8601-stamped skeletons the owner then fills/commits.
It never reaches the repo or the machine; the owner remains the only relay.

Filename stamp uses the owner's compact UTC convention `YYYYMMDDTHHMMz`; the in-document `<ISO8601>`
placeholders are filled with the readable full UTC form (e.g. 2026-06-27T03:14Z). Pass --stamp to
override (e.g. to match an exact close time).

Usage:
  python scaffold_artifacts.py baseline   --out /mnt/user-data/outputs
  python scaffold_artifacts.py handoff    --out /mnt/user-data/outputs --mid-task
  python scaffold_artifacts.py dr         --out /mnt/user-data/outputs --title "adopt python 3.13"
  python scaffold_artifacts.py cc-task    --out /mnt/user-data/outputs --title "venv triple realign"
  python scaffold_artifacts.py all        --out /mnt/user-data/outputs
"""

from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# artifact key -> (template filename, output filename pattern using {stamp})
ARTIFACTS: dict[str, tuple[str, str]] = {
    "baseline": ("continuation-baseline.template.md", "kingdom-continuation-{stamp}.md"),
    "handoff": ("orchestrator-handoff.template.md", "{stamp}-kingdom-orchestrator-handoff.md"),
    "dr": ("decision-record.template.md", "DR-{stamp}.md"),
    "cc-task": ("cc-task-prompt.template.md", "{stamp}-cc-task.md"),
}


def _now_utc() -> _dt.datetime:
    return _dt.datetime.now(_dt.UTC)


def compact_stamp(now: _dt.datetime) -> str:
    """YYYYMMDDTHHMMz — the owner's filename convention."""
    return now.strftime("%Y%m%dT%H%Mz")


def iso_stamp(now: _dt.datetime) -> str:
    """Readable full UTC form for in-document fields, e.g. 2026-06-27T03:14Z."""
    return now.strftime("%Y-%m-%dT%H:%MZ")


def render(template_text: str, iso: str, title: str | None, mid_task: bool) -> str:
    out = template_text.replace("<ISO8601>", iso)
    if title:
        out = out.replace("<short title>", title)
    if mid_task:
        out = out.replace("<clean-boundary | MID-TASK>", "MID-TASK")
        out = out.replace("<clean-boundary>", "MID-TASK")
    return out


def emit(
    key: str,
    out_dir: Path,
    iso: str,
    stamp: str,
    title: str | None,
    mid_task: bool,
) -> Path:
    template_name, name_pattern = ARTIFACTS[key]
    template_path = ASSETS / template_name
    if not template_path.is_file():
        raise FileNotFoundError(f"template not found: {template_path}")
    text = render(template_path.read_text(encoding="utf-8"), iso, title, mid_task)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / name_pattern.format(stamp=stamp)
    out_path.write_text(text, encoding="utf-8")
    return out_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold Kingdom-orchestrator artifact skeletons (files only)."
    )
    parser.add_argument(
        "artifact", choices=[*ARTIFACTS.keys(), "all"], help="which artifact to scaffold"
    )
    parser.add_argument("--out", default="out", help="output directory (default: ./out)")
    parser.add_argument("--title", default=None, help="short title for dr / cc-task")
    parser.add_argument(
        "--stamp", default=None, help="override compact stamp (default: UTC now, YYYYMMDDTHHMMz)"
    )
    parser.add_argument("--mid-task", action="store_true", help="mark handoff as MID-TASK")
    args = parser.parse_args(argv)

    now = _now_utc()
    iso = iso_stamp(now)
    # Honour an explicit close-time stamp for the filename; the in-doc ISO text
    # stays the readable now()-derived form.
    stamp = args.stamp if args.stamp else compact_stamp(now)

    out_dir = Path(args.out)
    keys = list(ARTIFACTS.keys()) if args.artifact == "all" else [args.artifact]
    written: list[Path] = []
    for key in keys:
        path = emit(key, out_dir, iso, stamp, args.title, args.mid_task)
        written.append(path)
        print(f"wrote {path}")

    if not written:
        print("nothing written", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
