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


