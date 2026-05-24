"""Service layer: business logic shared by the API and the MCP server.

Keeping logic here (rather than in route handlers or tool functions) means the
HTTP API and the MCP tools stay thin and behave identically.
"""

from __future__ import annotations

import uuid
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from kingdom.models import Memory, Project, Task


async def list_projects(session: AsyncSession) -> list[Project]:
    """Return all projects ordered by name."""
    result = await session.execute(select(Project).order_by(Project.name))
    return list(result.scalars().all())


async def get_project_by_slug(session: AsyncSession, slug: str) -> Project | None:
    """Return a single project by slug, or None."""
    result = await session.execute(select(Project).where(Project.slug == slug))
    return result.scalar_one_or_none()


async def create_task(
    session: AsyncSession,
    *,
    project_slug: str,
    title: str,
    description: str | None = None,
) -> Task | None:
    """Create a task under the named project.

    Returns the created Task, or None if the project does not exist.
    """
    project = await get_project_by_slug(session, project_slug)
    if project is None:
        return None
    task = Task(project_id=project.id, title=title, description=description)
    session.add(task)
    await session.flush()
    return task


async def search_memories(
    session: AsyncSession,
    *,
    query: str,
    project_slug: str | None = None,
    limit: int = 20,
) -> list[Memory]:
    """Case-insensitive substring search over memory content."""
    stmt = select(Memory).where(Memory.content.ilike(f"%{query}%"))
    if project_slug is not None:
        project = await get_project_by_slug(session, project_slug)
        if project is None:
            return []
        stmt = stmt.where(Memory.project_id == project.id)
    stmt = stmt.order_by(Memory.created_at.desc()).limit(limit)
    result = await session.execute(stmt)
    return list(result.scalars().all())


def list_artifacts(artifacts_dir: Path, subdir: str | None = None) -> list[dict[str, object]]:
    """List files under the artifacts directory (filesystem-backed).

    Path traversal outside ``artifacts_dir`` is rejected.
    """
    base = artifacts_dir.resolve()
    target = (base / subdir).resolve() if subdir else base
    if not (target == base or base in target.parents):
        raise ValueError("subdir escapes the artifacts directory")
    if not target.exists():
        return []
    items: list[dict[str, object]] = []
    for path in sorted(target.rglob("*")):
        if path.is_file() and path.name != ".gitkeep":
            items.append(
                {
                    "path": str(path.relative_to(base)),
                    "size_bytes": path.stat().st_size,
                }
            )
    return items


def project_to_dict(project: Project) -> dict[str, object]:
    """Serialize a Project for transport."""
    return {
        "id": str(project.id),
        "slug": project.slug,
        "name": project.name,
        "description": project.description,
        "status": project.status,
        "created_at": project.created_at.isoformat(),
    }


def task_to_dict(task: Task) -> dict[str, object]:
    """Serialize a Task for transport."""
    return {
        "id": str(task.id),
        "project_id": str(task.project_id),
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "created_at": task.created_at.isoformat(),
    }


def memory_to_dict(memory: Memory) -> dict[str, object]:
    """Serialize a Memory for transport."""
    return {
        "id": str(memory.id),
        "project_id": str(memory.project_id) if memory.project_id else None,
        "kind": memory.kind,
        "content": memory.content,
        "created_at": memory.created_at.isoformat(),
    }


def _coerce_uuid(value: str) -> uuid.UUID:
    """Parse a string into a UUID, raising ValueError on failure."""
    return uuid.UUID(value)
