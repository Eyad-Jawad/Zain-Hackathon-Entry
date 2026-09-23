# TOOD: Make an acquaintances table


from contextlib import asynccontextmanager

from zain_hackathon_entry.db import init_db, get_session

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()

    yield


app = FastAPI(lifespan=lifespan)

@app.get("/api/users")
def get_users():
    pass