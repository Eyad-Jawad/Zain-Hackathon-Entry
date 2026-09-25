from sqlalchemy.orm import Mapped, mapped_column

from .. import Base


class Acquaintance(Base):
    __tablename__ = "acquaintances"

    id: Mapped[int] = mapped_column(primary_key=True)

    acquaintance_name: Mapped[str | None]
    notes_on_acquaintance: Mapped[str | None]
