from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base

if TYPE_CHECKING:
    from .users import User


class Acquaintance(Base):
    __tablename__ = "acquaintances"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(
        back_populates="acquaintances",
        foreign_keys=[user_id],
    )

    acquaintance_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    acquaintance: Mapped["User"] = relationship(
        back_populates="acquaintanced_by",
        foreign_keys=[acquaintance_id],
    )

    acquaintance_name: Mapped[str | None]
    notes_on_acquaintance: Mapped[str | None]
