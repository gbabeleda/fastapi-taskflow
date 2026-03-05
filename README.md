# fastapi-taskflow

fastapi-taskflow is a production-grade backend blueprint that extends the single-process FastAPI foundation into a distributed, worker-capable architecture.

## Repository Evolution

### Initial Setup — Workspace Scaffold

The workspace structure was established with three `uv init` calls: one
for the root, and one for each member. `api` and `worker` are separate
packages under `packages/` because they are separate processes with
distinct dependency trees.

Python version is pinned once at the root via `.python-version`. Members
use `--no-pin-python` — the root is the single source of truth for the
entire workspace.

```bash
uv init --package --python 3.13 --build-backend hatch --name fastapi-taskflow

cd packages/api
uv init --package --python 3.13 --build-backend hatch --name api --no-pin-python

cd ../worker
uv init --package --python 3.13 --build-backend hatch --name worker --no-pin-python
```

Each `uv init` inside `packages/` auto-registered the member in the root
`pyproject.toml` under `[tool.uv.workspace]`. A single `uv.lock` at the
root ensures consistent dependencies across the entire workspace.

### Add Shared Library

`shared` is an internal library consumed by both `api` and `worker`. It exists
because database models, session management, and Alembic migrations are shared
across both processes — putting them in `api` and importing from `worker` would
create an incorrect dependency direction.

`--lib` is used instead of `--package` because `shared` has no entrypoint —
it is never run directly, only imported.

```bash
mkdir -p packages/shared

cd packages/shared
uv init --lib --python 3.13 --build-backend hatch --name shared --no-pin-python

# Wire as a local workspace dependency in both members
uv add shared --package api
uv add shared --package worker
```

`[tool.uv.sources]` in each member's `pyproject.toml` tells uv to resolve
`shared` from the workspace rather than PyPI. Changes to `shared` are
immediately reflected in both consumers without reinstalling.

### Add Database layer

Dependencies are added to `shared` only — `api` and `worker` inherit them
transitively through the workspace dependency.

```bash
uv add alembic asyncpg psycopg2-binary pydantic "sqlalchemy[asyncio]" pydantic-settings --package shared
uv sync --all-packages
```

#### Alembic init (customized)

The `pyproject_async` template generates an async-ready `env.py` and, unlike
the default template, stores all Alembic config under `[tool.alembic]` in
`pyproject.toml` instead of a separate `alembic.ini` file.

```bash
cd packages/shared
uv run alembic init --template pyproject_async ./alembic
```

After init, `env.py` was customised from the generated scaffold:

1. **Deleted `alembic.ini`** — config lives in `packages/shared/pyproject.toml`
   under `[tool.alembic]`.

2. **Injected the database URL programmatically** — avoids hardcoding it in
   config and keeps secrets in `.env`:

   ```python
   config.set_main_option("sqlalchemy.url", shared_settings.APPLICATION_DATABASE_URL)
   ```

3. **Wired `target_metadata`** for autogenerate support:

   ```python
   from shared.db.base import Base
   target_metadata = Base.metadata
   ```

4. **Added a wildcard model import** so Alembic's autogenerate detects all
   models without manually listing each one:

   ```python
   from shared.db.models import *
   ```

5. **Commented out `fileConfig` logging** — the generated template wires up
   logging from the ini file, which no longer exists.

#### Ruff config for alembic

Two additions were needed in the root `pyproject.toml` to keep ruff happy:

```toml
# First-party so isort groups workspace packages correctly
[tool.ruff.lint.isort]
known-first-party = ["shared", "api", "worker"]

# env.py uses star imports for model discovery — expected, not a mistake
[tool.ruff.lint.per-file-ignores]
"packages/shared/alembic/env.py" = [
    "F403", # allow star imports for model discovery
    "F401", # allow unused imports (models needed for autogenerate)
]
```
