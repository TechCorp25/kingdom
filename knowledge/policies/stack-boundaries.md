# Policy — stack & data boundaries

Kingdom tracks multiple projects with **different stacks**. Do not cross-pollinate them,
and do not mix control-plane data with project business data.

## Stacks are separate — use the right one per repo
| Project | Stack |
|---|---|
| **Kingdom** (this control plane) | Python 3.12 · uv · FastAPI · SQLAlchemy 2 async (asyncpg) · Alembic · Pydantic v2 · FastMCP · **PostgreSQL** |
| **IlluminateMyGallery** | FastAPI backend + Vite/React 19 + Tailwind/shadcn · **MongoDB Atlas** + **Cloudflare R2** + Worker CDN · Railway |
| **CivicMAPS** | Node/Express + **PostgreSQL** |
| **Le Répertoire** | **Flask** + **MongoDB/MongoEngine** |

So: Kingdom is **not** Flask and **not** Mongo. Flask/Mongo belongs to Le Répertoire;
Node/Express belongs to CivicMAPS. Never import a pattern from one project's stack into
another's.

## Data boundary
- Kingdom is the **control plane** (projects, tasks, runs, memories, artifacts). It is
  deliberately separate from the **business data** of the projects it tracks.
- Never store a tracked project's business data in Kingdom's Postgres, and never put
  Kingdom control-plane rows into a project's database.
- Tracked-project source lives under `projects/<slug>/` (gitignored, read by knowledge
  ingestion) — it is vendored working copy, not committed into Kingdom.

## Hierarchy of memory
Root `CLAUDE.md` rules apply everywhere under `~/kingdom`; a project's own
`projects/<slug>/CLAUDE.md` loads hierarchically when working in that subtree and refines
(never contradicts) the root contract.
