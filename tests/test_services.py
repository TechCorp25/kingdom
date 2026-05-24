"""Tests for the service layer (the logic shared by API and MCP)."""

from __future__ import annotations

from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from kingdom import services
from kingdom.models import Memory, Project


@pytest.fixture
def project_factory(session: AsyncSession):
    async def _make(slug: str = "civicmaps", name: str = "CivicMAPS") -> Project:
        project = Project(slug=slug, name=name)
        session.add(project)
        await session.flush()
        return project

    return _make


async def test_list_projects_empty(session: AsyncSession) -> None:
    assert await services.list_projects(session) == []


async def test_create_and_list_projects(session: AsyncSession, project_factory) -> None:
    await project_factory()
    projects = await services.list_projects(session)
    assert len(projects) == 1
    assert projects[0].slug == "civicmaps"


async def test_get_project_by_slug(session: AsyncSession, project_factory) -> None:
    await project_factory()
    found = await services.get_project_by_slug(session, "civicmaps")
    assert found is not None and found.name == "CivicMAPS"
    assert await services.get_project_by_slug(session, "missing") is None


async def test_create_task_under_project(session: AsyncSession, project_factory) -> None:
    await project_factory()
    task = await services.create_task(session, project_slug="civicmaps", title="Build MCP server")
    assert task is not None
    assert task.title == "Build MCP server"
    assert task.status == "open"


async def test_create_task_unknown_project(session: AsyncSession) -> None:
    assert await services.create_task(session, project_slug="nope", title="x") is None


async def test_search_memories(session: AsyncSession, project_factory) -> None:
    project = await project_factory()
    session.add(Memory(project_id=project.id, content="Railway deployment notes"))
    session.add(Memory(project_id=project.id, content="Patrol zone data"))
    await session.flush()
    hits = await services.search_memories(session, query="railway")
    assert len(hits) == 1
    assert "Railway" in hits[0].content


def test_list_artifacts(tmp_path: Path) -> None:
    (tmp_path / "reports").mkdir()
    (tmp_path / "reports" / "r1.md").write_text("hello")
    (tmp_path / "reports" / ".gitkeep").write_text("")
    items = services.list_artifacts(tmp_path)
    assert len(items) == 1
    assert items[0]["path"] == "reports/r1.md"


def test_list_artifacts_rejects_traversal(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        services.list_artifacts(tmp_path, subdir="../../etc")
