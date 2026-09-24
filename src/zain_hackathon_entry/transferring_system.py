from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from zain_hackathon_entry.auth import get_current_user
from zain_hackathon_entry.db import get_session
from zain_hackathon_entry.db.models import User
from zain_hackathon_entry.db.quries import (
    add_pending_transaction,
    add_transaction,
    delete_pending_reqest,
    get_pending_request,
    get_transaction,
    get_user_by_id,
    transfer_balance,
)
from zain_hackathon_entry.error_strings import Errors
from zain_hackathon_entry.schemas import TransactionReqeust, TransactionResponse

router = APIRouter()


@router.post(
    "/api/transfer/make_request",
    response_model=TransactionResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def make_request(
    session: Annotated[AsyncSession, get_session],
    user: Annotated[User, get_current_user],
    transaction: TransactionReqeust,
):
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

    reciever = await get_user_by_id(session, transaction.receiver_id)

    if reciever is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": Errors.THERE_IS_NO_USER,
                "date": f"User with id {transaction.receiver_id} does not exist.",
            },
        )

    # If similar payment was made: make new error
    # If user not acquaintance: pend adding them

    new_transaction = await add_transaction(session, user, reciever, transaction.amount)

    await add_pending_transaction(session, new_transaction)

    return {
        "message": Errors.CONFIRMATION_NEEDED,
        "pending_request": new_transaction,
    }


@router.post(
    "/api/transfer/confirm_request/{id}",
    response_model=TransactionResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def confirm_transfer_request(
    session: Annotated[AsyncSession, get_session],
    user: Annotated[User, get_current_user],
    id: int,
):
    request = await get_pending_request(session, id)

    if request is None or request.request_id != user.id:
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

    if transaction is None:
        await delete_pending_reqest(session, request)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found due to internal error, please restart over.",
        )

    reciever = await get_user_by_id(session, transaction.receiver_id)

    if reciever is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reciever not found."
        )

    await transfer_balance(session, user, reciever, transaction.amount)

    await delete_pending_reqest(session, request)

    return transaction
