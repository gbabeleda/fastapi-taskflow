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
