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