from typing import TYPE_CHECKING
from datetime import datetime, UTC

from .. import Base

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .users import User

class PendingRequest(Base):
    __tablename__ = "pending_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates="pending_requests")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    request: Mapped[str]
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
