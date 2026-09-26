from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from zain_hackathon_entry.auth import get_current_user
from zain_hackathon_entry.db import get_session
from zain_hackathon_entry.db.models import User
from zain_hackathon_entry.db.quries import (
    add_acquaintance,
    add_pending_transaction,
    add_transaction,
    delete_pending_reqest,
    get_acquaintance_by_id,
    get_acquaintance_by_name,
    get_acquaintances,
    get_pending_request,
    delete_pending_transaction,
    get_transaction,
    get_user_by_id,
    get_user_by_username,
    transfer_balance,
)
from zain_hackathon_entry.error_strings import Errors
from zain_hackathon_entry.schemas import (
    AcquaintanceRequest,
    AcquaintanceResponse,
    RequestResponse,
    TransactionReqeust,
    TransactionResponse,
    UserResponse,
    UserOwnProfile,
)

router = APIRouter()


@router.post(
    "/api/transfer/make_request",
    response_model=RequestResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def make_request(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    transaction: TransactionReqeust,
):
    if user.id == transaction.receiver_id:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="You can't transfer to yourself.",
        )

    if user.balance < transaction.amount:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail={
                "error": Errors.SUM_IS_BIGGER_THAN_BALANCE,
                "data": {
                    "balance": user.balance,
                    "amount": transaction.amount,
                },
            },
        )

    receiver = await get_user_by_id(session, transaction.receiver_id)

    if receiver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": Errors.THERE_IS_NO_USER,
                "date": f"User with id {transaction.receiver_id} does not exist.",
            },
        )

    # If similar payment was made: make new error
    # If user not acquaintance: pend adding them

    new_transaction = await add_transaction(session, user, receiver, transaction.amount)

    await add_pending_transaction(session, new_transaction)

    return RequestResponse(
        message=Errors.CONFIRMATION_NEEDED,
        request=TransactionResponse.model_validate(new_transaction),
    )


@router.post(
    "/api/transfer/confirm_request/{id}",
    response_model=RequestResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def confirm_transfer_request(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    id: int,
):
    request = await get_pending_request(session, id)

    if request is None or request.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if datetime.now() - request.date > timedelta(days=1):
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail={
                "error": Errors.EXPIRED_REQUEST,
                "data": "Request was made more than a day ago.",
            },
        )

    transaction = await get_transaction(session, id)
    assert transaction, "Some error happened, please restart over"

    receiver = await get_user_by_id(session, transaction.receiver_id)

    if receiver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="receiver not found."
        )

    await transfer_balance(session, user, receiver, transaction.amount)

    await delete_pending_reqest(session, request)

    return RequestResponse(
        message="Transaction confirmed.",
        request=TransactionResponse.model_validate(transaction),
    )


@router.delete(
    "/api/transfer/confirm_request/{id}",
    status_code=status.HTTP_200_OK,
)
async def delete_pending_request(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    id: int,
):
    request = await get_pending_request(session, id)

    if request is None or request.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    await delete_pending_transaction(session, request)

    return {"request_deleted": True}


@router.get(
    "/api/users/me",
    response_model=UserOwnProfile,
    status_code=status.HTTP_200_OK,
)
async def api_get_user_by_id(
    user: Annotated[User, Depends(get_current_user)],
):
    return user


@router.get(
    "/api/users/id/{id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_user_by_id(
    session: Annotated[AsyncSession, Depends(get_session)],
    _user: Annotated[User, Depends(get_current_user)],
    id: int,
):
    user = await get_user_by_id(session, id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return user


@router.get(
    "/api/users/username/{username}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_user_by_username(
    session: Annotated[AsyncSession, Depends(get_session)],
    _user: Annotated[User, Depends(get_current_user)],
    username: str,
):
    user = await get_user_by_username(session, username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return user


@router.get(
    "/api/acquaintances/id/{id}",
    response_model=AcquaintanceResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_acquaintace_by_id(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    id: int,
):
    acquaintance = await get_acquaintance_by_id(session, id, user.id)

    if acquaintance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Acquaintance not found."
        )

    return acquaintance


@router.get(
    "/api/acquaintances/name/{name}",
    response_model=list[AcquaintanceResponse],
    status_code=status.HTTP_200_OK,
)
async def api_get_acquaintace_by_name(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    name: str,
):
    acquaintance = await get_acquaintance_by_name(session, name, user.id)

    if acquaintance is None or len(acquaintance) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Acquaintance not found."
        )

    return acquaintance


@router.get(
    "/api/acquaintances",
    response_model=list[AcquaintanceResponse],
    status_code=status.HTTP_200_OK,
)
async def api_get_acquaintaces(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
):
    acquaintances = await get_acquaintances(session, user.id)

    if acquaintances == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Acquaintances not found. Please add any.",
        )

    return acquaintances


@router.post(
    "/api/acquaintances",
    response_model=AcquaintanceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def api_add_acquaintace(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    request: AcquaintanceRequest,
):
    acquaintance = await get_user_by_username(session, request.username)

    if acquaintance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found, please check the username again.",
        )

    new_acquaintance = await add_acquaintance(
        session,
        user,
        acquaintance,
        request.acquaintance_name,
        request.notes_on_acquaintance,
    )

    return new_acquaintance
