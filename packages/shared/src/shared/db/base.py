from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column

# Custom type annotation for timezone-aware datetime
# Usage: checked_at: Mapped[timestamp] = mapped_column(server_default=func.now())
timestamp = Annotated[datetime, mapped_column(DateTime(timezone=True))]


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy v2 models."""

    pass
