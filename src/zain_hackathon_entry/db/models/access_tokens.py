from typing import TYPE_CHECKING
from uuid import uuid4

from .. import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .users import User

class AccessToken(Base):
    __tablename__ = "access_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[User] = relationship(back_populates="user")
    user_id: Mapped[int] = mapped_column(ForeignKey("usres.id"))
    token: Mapped[str] = mapped_column(default=lambda: uuid4(), index=True)
