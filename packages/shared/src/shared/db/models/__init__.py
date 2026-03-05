"""
Database models package.

All models must be imported here so Alembic can discover them for autogeneration.
"""

from .health import HealthCheck

__all__ = ["HealthCheck"]
