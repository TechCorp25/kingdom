"""Core control-plane entities.

This is the initial vertical slice (Project, Task, Memory). The remaining
documented entities — repositories, agents, skills, tools, runs, run_events,
artifacts — follow the same pattern and are added in later phases.
"""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from kingdom.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Project(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """A tracked project (e.g. CivicMAPS)."""

    __tablename__ = "projects"

    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, default=None)
    status: Mapped[str] = mapped_column(String(32), default="active")

    tasks: Mapped[list[Task]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
    memories: Mapped[list[Memory]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )


class Task(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """A unit of work within a project."""

    __tablename__ = "tasks"

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        index=True,
    )
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str | None] = mapped_column(Text, default=None)
    status: Mapped[str] = mapped_column(String(32), default="open")

    project: Mapped[Project] = relationship(back_populates="tasks")


class Memory(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """A long-lived note or fact, optionally scoped to a project."""

    __tablename__ = "memories"

    project_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        default=None,
        index=True,
    )
    kind: Mapped[str] = mapped_column(String(32), default="note")
    content: Mapped[str] = mapped_column(Text)

    project: Mapped[Project | None] = relationship(back_populates="memories")
