"""Kingdom MCP server (stdio transport).

Exposes the documented control-plane tools to MCP clients such as Claude Code:
list_projects, get_project, search_memories, create_task, list_artifacts.

Tools share the same service layer as the HTTP API, so behaviour is identical
across both surfaces.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from kingdom import services
from kingdom.config import get_settings
from kingdom.db import session_scope

mcp = FastMCP("kingdom")


@mcp.tool()
async def list_projects() -> list[dict[str, object]]:
    """List all tracked projects in the Kingdom control plane."""
    async with session_scope() as session:
        projects = await services.list_projects(session)
        return [services.project_to_dict(p) for p in projects]


@mcp.tool()
async def get_project(slug: str) -> dict[str, object]:
    """Fetch a single project by its slug.

    Returns the project, or an ``{"error": ...}`` object if not found.
    """
    async with session_scope() as session:
        project = await services.get_project_by_slug(session, slug)
        if project is None:
            return {"error": f"project not found: {slug}"}
        return services.project_to_dict(project)


@mcp.tool()
async def search_memories(
    query: str, project_slug: str | None = None, limit: int = 20
) -> list[dict[str, object]]:
    """Search memories by content substring, optionally scoped to a project."""
    async with session_scope() as session:
        memories = await services.search_memories(
            session, query=query, project_slug=project_slug, limit=limit
        )
        return [services.memory_to_dict(m) for m in memories]


@mcp.tool()
async def create_task(
    project_slug: str, title: str, description: str | None = None
) -> dict[str, object]:
    """Create a task under the named project.

    Returns the created task, or an ``{"error": ...}`` object if the project
    does not exist.
    """
    async with session_scope() as session:
        task = await services.create_task(
            session, project_slug=project_slug, title=title, description=description
        )
        if task is None:
            return {"error": f"project not found: {project_slug}"}
        return services.task_to_dict(task)


@mcp.tool()
def list_artifacts(subdir: str | None = None) -> list[dict[str, object]]:
    """List artifact files on disk, optionally within a subdirectory."""
    settings = get_settings()
    return services.list_artifacts(settings.artifacts_dir, subdir)


def main() -> None:
    """Console entry point: run the MCP server over stdio."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
