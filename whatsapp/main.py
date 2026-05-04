from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import create_db
from routers import users, rooms, ws, front


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


app = FastAPI(title="Mini WhatsApp", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(ws.router)
app.include_router(front.router)
