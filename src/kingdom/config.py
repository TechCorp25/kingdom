"""Application configuration loaded from environment / .env."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Repository root: src/kingdom/config.py -> parents[2] == project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Typed settings for the Kingdom control plane.

    Values are read from environment variables, falling back to a local
    ``.env`` file. Names are case-insensitive.
    """

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Core
    kingdom_root: Path = PROJECT_ROOT
    app_env: str = "development"
    log_level: str = "info"

    # Database (async driver for the app; Alembic reuses the async engine)
    database_url: str = Field(
        default="postgresql+asyncpg://kingdom:change_me@localhost:5432/kingdom",
    )

    # API
    api_host: str = "127.0.0.1"
    api_port: int = 8000

    # MCP
    mcp_host: str = "127.0.0.1"
    mcp_port: int = 8765

    # Worker / queue (optional)
    redis_url: str = "redis://localhost:6379/0"
    worker_concurrency: int = 2

    # Artifact storage
    artifacts_dir: Path = PROJECT_ROOT / "artifacts"

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
