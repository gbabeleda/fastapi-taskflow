"""FastAPI application instance and configuration.

This module creates and configures the FastAPI application,
including all routers and middleware.
"""

from fastapi import FastAPI

from api.core.config import settings
from api.router.v1.router import v1_router

# Create FastAPI application instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
)

# Include API v1 router
app.include_router(v1_router, prefix=settings.API_V1_PREFIX)
