from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db_dir = Path(__file__).resolve().parent
db_path = db_dir / "app.db"
db_url = f"sqlite+aiosqlite:///{db_path}"

engine = create_async_engine(db_url)
SessionLocal = async_sessionmaker(bind=engine)


async def init_db():
    from . import models as models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        return engine


async def get_session() -> AsyncGenerator[AsyncSession]:
    try:
        session = SessionLocal()
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
