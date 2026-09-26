from heapq import nlargest

from rapidfuzz import fuzz, process
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from zain_hackathon_entry.schemas import AccessTokenResponse

from .models import (
    AccessToken,
    Acquaintance,
    PendingRequest,
    Transaction,
    User,
    UserRelationship,
)


async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))

    return list(result.scalars().all())


async def get_user_by_id(session: AsyncSession, id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == id))

    return result.scalar_one_or_none()


async def get_user_by_username(session: AsyncSession, name: str) -> User | None:
    result = await session.execute(select(User).where(User.username == name))

    return result.scalar_one_or_none()


async def get_user_by_card_token(session: AsyncSession, card_token: str) -> User | None:
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


async def add_transaction(
    session: AsyncSession, sender: User, receiver: User, amount: int
) -> Transaction:
    transaction = Transaction(sender=sender, receiver=receiver, amount=amount)

    session.add(transaction)
    await session.flush()

    return transaction


async def add_pending_transaction(
    sesison: AsyncSession, transaction: Transaction
) -> PendingRequest:
    pending_request = PendingRequest(user=transaction.sender, request_id=transaction.id)

    sesison.add(pending_request)
    await sesison.flush()

    return pending_request


async def get_pending_request(session: AsyncSession, id: int) -> PendingRequest | None:
    result = await session.execute(
        select(PendingRequest).where(PendingRequest.request_id == id)
    )

    return result.scalar_one_or_none()


async def delete_pending_transaction(
    session: AsyncSession, pending_transaction: PendingRequest
) -> None:
    await session.delete(pending_transaction)


async def get_transaction(session: AsyncSession, id: int) -> Transaction | None:
    result = await session.execute(select(Transaction).where(Transaction.id == id))

    return result.scalar_one_or_none()


async def get_user_transactions(
    session: AsyncSession, user_id: int
) -> list[Transaction]:
    result = await session.execute(
        select(Transaction).where(Transaction.sender_id == user_id)
    )

    return list(result.scalars().all())


async def transfer_balance(
    session: AsyncSession, sender: User, receiver: User, amount
) -> None:
    sender.balance -= amount
    receiver.balance += amount

    await session.flush()


async def delete_pending_reqest(
    session: AsyncSession, pending_request: PendingRequest
) -> None:
    await session.delete(pending_request)
    await session.flush()


async def get_acquaintance_by_id(
    session: AsyncSession, id: int, user_id: int
) -> Acquaintance | None:
    result = await session.execute(
        select(Acquaintance)
        .join(UserRelationship, UserRelationship.acquaintance_id == Acquaintance.id)
        .where(
            UserRelationship.user_id == user_id,
            Acquaintance.id == id,
        )
    )

    return result.scalar_one_or_none()


async def get_acquaintance_by_name(
    session: AsyncSession, name: str, user_id: int
) -> list[Acquaintance]:
    result = await session.execute(
        select(Acquaintance)
        .join(UserRelationship, UserRelationship.acquaintance_id == Acquaintance.id)
        .where(
            UserRelationship.user_id == user_id,
            Acquaintance.acquaintance_name == name,
        )
    )

    acquaintances = list(result.scalars().all())

    if len(acquaintances) != 0:
        return acquaintances

    acquaintances = await get_acquaintances(session, user_id)

    if len(acquaintances) == 0:
        return []

    fuzz_results = process.extract(
        query=name,
        choices=acquaintances,
        scorer=fuzz.ratio,
        processor=lambda a: a.acquaintance_name if isinstance(a, Acquaintance) else a,
    )

    return [
        a[0]
        for a in nlargest(
            5,
            fuzz_results,
            key=lambda a: a[1],
        )
    ]


async def get_acquaintances(session: AsyncSession, user_id: int) -> list[Acquaintance]:
    result = await session.execute(
        select(Acquaintance)
        .join(UserRelationship, UserRelationship.acquaintance_id == Acquaintance.id)
        .where(UserRelationship.user_id == user_id)
    )

    acquaintances = result.scalars().all()

    return list(acquaintances)


async def add_acquaintance(
    session: AsyncSession, user: User, acquaintance: User, name: str, notes: str
) -> Acquaintance:
    new_acquaintance = Acquaintance(
        id=acquaintance.id, acquaintance_name=name, notes_on_acquaintance=notes
    )
    session.add(new_acquaintance)
    await session.flush()

    relationship = UserRelationship(
        user_id=user.id,
        acquaintance_id=new_acquaintance.id,
    )

    session.add(relationship)
    await session.flush()

    return new_acquaintance
