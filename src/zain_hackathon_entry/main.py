# TODO: Make an acquaintances table
# TODO: Make get_users_by_name use fuzzy search
# TODO: make the errors enum
# TODO: Make logging in logic
# TODO: Put utc back in auth token validation 

from typing import Annotated
from contextlib import asynccontextmanager

from zain_hackathon_entry.db import init_db, get_session
from zain_hackathon_entry.db.quries import (
    get_users,
    get_user_by_name,
    get_user_by_card_number,
    get_user_by_id,
)
from zain_hackathon_entry.error_strings import Errors
from zain_hackathon_entry import auth

from zain_hackathon_entry.schemas import UserRequest, UserResponse

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(_app: FastAPI):
    engine = await init_db()

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "WEBSITE GOES HERE LATER!!!!!!",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(auth.router, tags=["auth"])


# @app.post("/api/pay")
# async def payment_method(
#     request: Request, 
#     user: UserRequest, 
#     session: Annotated[AsyncSession, Depends(get_session)]
# ):
#     if user.id:
#         users = get_users_by_id(session, user.id)
#     elif user.card_number:
#         users = get_users_by_card_number(session, user.card_number)
#     else:
#         users = get_users_by_name(session, user.name)

#     if len(users) == 0 and user.card_number is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
#             "error": Errors.THERE_IS_NO_USER,
#             "data": "Ask the user for data about this person so we can add it to the database."
#         })
