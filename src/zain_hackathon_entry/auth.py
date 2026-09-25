from datetime import datetime
from typing import Annotated

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from zain_hackathon_entry.db import get_session
from zain_hackathon_entry.db.models import AccessToken, User
from zain_hackathon_entry.db.quries import (
    add_user,
    create_access_token,
    delete_user,
    get_token,
    get_user_by_card_token,
    get_user_by_name,
    revoke_access_token,
)
from zain_hackathon_entry.schemas import (
    AccessTokenResponse,
    DeleteAccountRequest,
    LogInRequest,
    SignUpRequest,
)

router = APIRouter()
ph = PasswordHasher()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/sign_up")


async def validate_and_get_token(session: AsyncSession, token: str) -> AccessToken:
    access_token = await get_token(session, token)

    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid access token."
        )

    if access_token.expiration_date < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired session. Please log in again.",
        )

    return access_token


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    access_token = await validate_and_get_token(session, token)

    await session.refresh(access_token, ["user"])

    return access_token.user


async def verify_unqiue_username(session: AsyncSession, username: str) -> None:
    user = await get_user_by_name(session, username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already used. Please use another one.",
        )


async def verify_unique_card_token(session: AsyncSession, card_token: str) -> None:
    user = await get_user_by_card_token(session, card_token)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Card number already used. Please try to log in.",
        )


@router.post(
    "/api/sign_up",
    response_model=AccessTokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up(
    creds: SignUpRequest, session: Annotated[AsyncSession, Depends(get_session)]
):
    await verify_unqiue_username(session, creds.username)
    await verify_unique_card_token(session, creds.card_token)

    """

    Some kind of card verfication using the pin code should go
    in here, but since it's outside the scope of this project
    as of now, we'll skip adding any boilprete.

    """

    password_hash = hash_password(creds.password)

    user = await add_user(session, creds.username, password_hash, creds.card_token)
    return await create_access_token(session, user)


@router.post(
    "/api/log_in",
    response_model=AccessTokenResponse,
    status_code=status.HTTP_200_OK,
)
async def log_in(
    creds: LogInRequest, session: Annotated[AsyncSession, Depends(get_session)]
):
    user = await get_user_by_name(session, creds.username)
    if user is None or not verify_password(creds.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid username or password. Please try again.",
        )

    return await create_access_token(session, user)


@router.delete("/api/log_out", status_code=status.HTTP_200_OK)
async def log_out(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    access_token = await validate_and_get_token(session, token)
    await revoke_access_token(session, access_token)

    return {"logged_out": True}


@router.delete("/api/delete_account", status_code=status.HTTP_200_OK)
async def delete_account(
    creds: DeleteAccountRequest, session: Annotated[AsyncSession, Depends(get_session)]
):
    user = await get_user_by_name(session, creds.username)
    if user is None or not verify_password(creds.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid username or password. Please try again.",
        )

    await delete_user(session, user)

    return {"account_deleted": True}


def hash_password(password: str):
    return ph.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        ph.verify(password_hash, password)
        return True

    except VerifyMismatchError:
        return False
