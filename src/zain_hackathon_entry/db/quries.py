from .models.users import User

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(
        select(User)
    )

    return list(result.scalars().all())

async def get_users_by_name(session: AsyncSession, name: str) -> list[User]:
    result = await session.execute(
        select(User).where(User.name == name)
    )

    return list(result.scalars().all())

async def get_users_by_card_number(session: AsyncSession, card_number: int) -> list[User]:
    result = await session.execute(
        select(User).where(User.card_number == card_number)
    )

    return list(result.scalars().all())
