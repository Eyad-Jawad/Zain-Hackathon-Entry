from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from zain_hackathon_entry.schemas import AccessTokenResponse

from .models import AccessToken, User


async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))

    return list(result.scalars().all())


async def get_user_by_id(session: AsyncSession, id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == id))

    return result.scalar_one_or_none()


async def get_user_by_name(session: AsyncSession, name: str) -> User | None:
    result = await session.execute(select(User).where(User.username == name))

    return result.scalar_one_or_none()


async def get_user_by_card_token(
    session: AsyncSession, card_token: str
) -> User | None:
    result = await session.execute(select(User).where(User.card_token == card_token))

    return result.scalar_one_or_none()


async def add_user(
    session: AsyncSession, username: str, password_hash: str, card_token: str
) -> User:
    user = User(
        username=username,
        password_hash=password_hash,
        card_token=card_token,
    )

    session.add(user)
    await session.flush()

    return user


async def create_access_token(session: AsyncSession, user: User) -> AccessTokenResponse:
    access_token = AccessToken(user=user)
    session.add(access_token)
    await session.flush()

    return AccessTokenResponse(
        access_token=access_token.token, exp=access_token.expiration_date
    )


async def get_token(session: AsyncSession, token: str) -> AccessToken | None:
    result = await session.execute(
        select(AccessToken).where(AccessToken.token == token)
    )

    return result.scalar_one_or_none()


async def revoke_access_token(session: AsyncSession, access_token: AccessToken) -> None:
    await session.delete(access_token)
    await session.flush()


async def delete_user(session: AsyncSession, user: User):
    await session.delete(user)
    await session.flush()
