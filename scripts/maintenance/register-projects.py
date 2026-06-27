#!/usr/bin/env python
"""Register the tracked projects in the Kingdom control plane.

Derives a slug and name from each folder name (stripping the GitHub zip
'-main'/'-master' suffix and splitting camelCase for readable slugs), then
upserts each project. With --prune, any project whose slug is NOT in the
provided set is removed (cascading to its tasks/memories) so the control plane
tracks exactly the set you pass.

Usage:
  uv run python scripts/maintenance/register-projects.py <folder> [<folder> ...]
  uv run python scripts/maintenance/register-projects.py --prune <folder> ...
  uv run python scripts/maintenance/register-projects.py --dry-run --prune <folder> ...

Only the folder NAME is used (to derive slug/name); the path need not exist.
"""

from __future__ import annotations

import argparse
import asyncio
import re
from pathlib import Path

from sqlalchemy import select

from kingdom.db import session_scope
from kingdom.models import Project

SUFFIXES = ("-main", "-master")


def derive(folder: str) -> tuple[str, str]:
    """Return (slug, name) derived from a folder path's basename."""
    name = Path(folder).name
    for suffix in SUFFIXES:
        if name.lower().endswith(suffix):
            name = name[: -len(suffix)]
            break
    # Split camelCase boundaries so 'IlluminateMyGallery' -> readable slug.
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "-", name)
    slug = re.sub(r"[^a-z0-9]+", "-", spaced.lower()).strip("-")
    return slug, name


async def run(folders: list[str], prune: bool, dry_run: bool) -> None:
    specs = [derive(f) for f in folders]
    wanted = {slug for slug, _ in specs}

    print("Tracked set:")
    for slug, name in specs:
        print(f"  {slug:30} ({name})")
    print()

    async with session_scope() as session:
        for slug, name in specs:
            existing = (
                await session.execute(select(Project).where(Project.slug == slug))
            ).scalar_one_or_none()
            if existing is None:
                if not dry_run:
                    session.add(
                        Project(slug=slug, name=name, description="Tracked from remote main branch")
                    )
                print(f"  + add    {slug}")
            elif existing.name != name:
                if not dry_run:
                    existing.name = name
                print(f"  ~ update {slug} (name -> {name})")
            else:
                print(f"  = exists {slug}")

        if prune:
            all_projects = (await session.execute(select(Project))).scalars().all()
            for project in all_projects:
                if project.slug not in wanted:
                    if not dry_run:
                        await session.delete(project)
                    print(f"  - prune  {project.slug} (not in tracked set)")

        if dry_run:
            # Roll back so a dry run never commits.
            await session.rollback()

    print()
    print("DRY RUN — no changes written." if dry_run else "Done.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Register tracked Kingdom projects.")
    parser.add_argument("folders", nargs="+", help="project folder paths or names")
    parser.add_argument(
        "--prune", action="store_true", help="remove projects not in the provided set"
    )
    parser.add_argument("--dry-run", action="store_true", help="show changes without writing them")
    args = parser.parse_args()
    asyncio.run(run(args.folders, args.prune, args.dry_run))


if __name__ == "__main__":
    main()
