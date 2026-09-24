from typing import TYPE_CHECKING

from .. import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .users import User

class Acquaintance(Base):
    __tablename__ = "acquaintances"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates="acquaintances")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    acquaintance_name: Mapped[str | None]
    acquaintance_card_number: Mapped[int]
    notes_on_acquaintance: Mapped[str | None]
