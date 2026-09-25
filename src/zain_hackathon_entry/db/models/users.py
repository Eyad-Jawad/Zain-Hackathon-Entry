from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base

if TYPE_CHECKING:
    from .access_tokens import AccessToken
    from .pendings_requests import PendingRequest
    from .transactions import Transaction


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str]
    tokens: Mapped[list["AccessToken"]] = relationship(
        back_populates="user", cascade="all, delete"
    )

    card_token: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    balance: Mapped[int] = mapped_column(default=100)

    sent_transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="sender",
        foreign_keys="Transaction.sender_id",
    )
    recieved_transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="receiver",
        foreign_keys="Transaction.receiver_id",
    )

    pending_requests: Mapped[list["PendingRequest"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
