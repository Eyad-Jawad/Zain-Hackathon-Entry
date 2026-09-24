# TODO: Make get_users_by_name use fuzzy search
# TODO: make the errors enum
# TODO: Make logging in logic
# TODO: Put utc back in auth token validation, and confirmation

from contextlib import asynccontextmanager

from fastapi import FastAPI

from zain_hackathon_entry import auth, transferring_system
from zain_hackathon_entry.db import init_db


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
app.include_router(transferring_system.router, tags=["transfer"])
