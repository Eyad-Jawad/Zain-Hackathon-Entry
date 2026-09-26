from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .. import Base


class UserRelationship(Base):
    __tablename__ = "user_relationships"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    acquaintance_id: Mapped[int] = mapped_column(ForeignKey("acquaintances.id"))

    __table_args__ = (UniqueConstraint("user_id", "acquaintance_id"),)
