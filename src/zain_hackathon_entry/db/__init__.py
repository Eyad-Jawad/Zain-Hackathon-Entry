from collections.abc import AsyncGenerator
from pathlib import Path
from contextlib import asynccontextmanager

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine


class Base(DeclarativeBase):
    pass


db_dir = Path(__file__).resolve().parent()
db_path = db_dir / "app.db"
db_url = f"sqlite+aiosqlite://{db_path}"

engine = create_async_engine(db_url)
SessionLocal = async_sessionmaker(bind=engine)

async def init_db():
    from . import models as models

    async with engine.begin() as conn:
        conn.run_sync(Base.metadata.create_all())
        yield

    await engine.dispose()


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession]:
    try:
        session = SessionLocal()
        yield session
    finally:
        await session.commit()
        await session.close()
