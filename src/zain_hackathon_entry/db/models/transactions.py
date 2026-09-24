from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base

if TYPE_CHECKING:
    from .users import User


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(nullable=False)

    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    sender: Mapped["User"] = relationship(
        back_populates="sent_transactions",
        foreign_keys=[sender_id],
    )

    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    receiver: Mapped["User"] = relationship(
        back_populates="recieved_transactions",
        foreign_keys=[receiver_id],
    )

    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
