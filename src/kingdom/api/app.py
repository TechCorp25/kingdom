"""FastAPI application factory and entry point."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from kingdom import __version__, services
from kingdom.config import get_settings
from kingdom.db import get_db, get_engine

DbSession = Annotated[AsyncSession, Depends(get_db)]


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    app = FastAPI(
        title="Kingdom API",
        version=__version__,
        summary="Control plane for AI-assisted software development",
    )

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        """Liveness + database connectivity check."""
        db_status = "ok"
        try:
            engine = get_engine()
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception:  # noqa: BLE001 - report any DB failure as degraded
            db_status = "unavailable"
        return {"status": "ok", "version": __version__, "database": db_status}

    @app.get("/projects", tags=["projects"])
    async def list_projects(session: DbSession) -> list[dict[str, object]]:
        """List all tracked projects."""
        projects = await services.list_projects(session)
        return [services.project_to_dict(p) for p in projects]

    @app.get("/projects/{slug}", tags=["projects"])
    async def get_project(slug: str, session: DbSession) -> dict[str, object]:
        """Fetch a single project by slug."""
        project = await services.get_project_by_slug(session, slug)
        if project is None:
            raise HTTPException(status_code=404, detail="project not found")
        return services.project_to_dict(project)

    return app


app = create_app()


def run() -> None:
    """Console entry point: serve the API with uvicorn."""
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "kingdom.api.app:app",
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    run()
