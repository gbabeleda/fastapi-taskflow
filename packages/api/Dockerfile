# syntax=docker/dockerfile:1
# Enable BuildKit features (cache mounts, bind mounts) for faster and cleaner builds

# Build Stage: Resolve dependencies and build wheels
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# uv configuration:
# - compile bytecode for faster startup
# - avoid hardlinks across layers
# - exclude development dependencies
# - rely on system python provided by base image
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install third-party deps using bind mounts — manifests are never written as a layer.
# This maximizes Docker layer cache reuse since dependency definitions
# change far less frequently than application code.
# All workspace pyproject.toml files must be bound so uv can resolve the full graph.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=packages/api/pyproject.toml,target=packages/api/pyproject.toml \
    --mount=type=bind,source=packages/shared/pyproject.toml,target=packages/shared/pyproject.toml \
    --mount=type=bind,source=packages/worker/pyproject.toml,target=packages/worker/pyproject.toml \
    uv sync --package api --locked --no-install-workspace

# Copy workspace source after dependencies to avoid cache invalidation
COPY packages/api/src    packages/api/src
COPY packages/shared/src packages/shared/src

# Build wheels for api and shared.
# shared must be built separately — it is a local workspace dep, not on PyPI,
# so the runtime image cannot resolve it without the wheel.
RUN uv build --wheel --package api    --out-dir /dist && \
    uv build --wheel --package shared --out-dir /dist


# Runtime Stage: Minimal production image
FROM python:3.13-slim-bookworm AS runtime

# Create non-root user for security
RUN groupadd --system --gid 999 appuser && \
    useradd --system --gid 999 --uid 999 --create-home appuser

WORKDIR /app

# Install only the pre-built wheels using system pip.
# --find-links /dist allows pip to resolve the shared wheel as a dep of api.
# This avoids shipping build tools and uv in the final image.
COPY --from=builder /dist /dist
RUN pip install --no-cache-dir --find-links /dist /dist/*.whl && rm -rf /dist

# alembic config and migrations — required by the migrator service in docker-compose
COPY packages/shared/pyproject.toml packages/shared/pyproject.toml
COPY packages/shared/alembic        packages/shared/alembic

# Drop privileges for runtime
USER appuser

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
