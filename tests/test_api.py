"""Tests for the FastAPI HTTP surface."""

from __future__ import annotations

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from kingdom.models import Project


async def test_health(client: AsyncClient) -> None:
    resp = await client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "version" in body


async def test_list_projects_endpoint(client: AsyncClient, session: AsyncSession) -> None:
    session.add(Project(slug="civicmaps", name="CivicMAPS"))
    await session.flush()
    resp = await client.get("/projects")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["slug"] == "civicmaps"


async def test_get_project_404(client: AsyncClient) -> None:
    resp = await client.get("/projects/missing")
    assert resp.status_code == 404
