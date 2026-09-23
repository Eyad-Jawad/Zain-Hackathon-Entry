from .. import Base

from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    card_number: Mapped[int] = mapped_column(unique=True, nullable=False, index=True)
