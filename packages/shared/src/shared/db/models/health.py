from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from shared.db.base import Base, timestamp


class HealthCheck(Base):
    """
    Minimal model for database health checks.

    Used to verify:
    - Database connectivity
    - Alembic migrations are applied
    - SQLAlchemy ORM can write/read data
    """

    __tablename__ = "health_check"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(primary_key=True)
    checked_at: Mapped[timestamp] = mapped_column(
        server_default=func.now(), comment="Timestamp of last health check (UTC)"
    )
