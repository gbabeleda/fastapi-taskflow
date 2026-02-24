"""
Main API v1 router.

This router aggregates all v1 endpoints. As the application grows,
sub-routers from different domains can be included here.

Example future structure:
    v1_router.include_router(users.router, prefix="/users", tags=["users"])
    v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
"""

from fastapi import APIRouter

v1_router = APIRouter()


@v1_router.get("/health")
def health_check() -> dict[str, str]:
    """
    Health check endpoint. Used to verify the API is running.
    """
    return {"status": "healthy"}
