from typing import TYPE_CHECKING

from .. import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .pendings_requests import PendingRequest
    from .acquaintances import Acquaintance
    from .transactions import Transaction
    from .access_tokens import AccessToken

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str]
    tokens: Mapped[list["AccessToken"]] = relationship(
        back_populates="user", 
        cascade="all, delete"
    )

    card_number: Mapped[int] = mapped_column(unique=True, nullable=False, index=True)
    acquaintances: Mapped[list["Acquaintance"]] = relationship(
        back_populates="user", 
        cascade="all, delete"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="user", 
        cascade="all, delete"
    )
    pending_requests: Mapped[list["PendingRequest"]] = relationship(
        back_populates="user", 
        cascade="all, delete"
    )

