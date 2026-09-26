# TODO: Put utc back in auth token validation, and confirmation
# TODO: Document or make how ids are used cleaer
# TODO: Add more error strings
# TODO: Add checking similar paymet last day
# TODO: Add more error strings and things to handle
# TODO: Maybe bake the ai into the system not the user

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
