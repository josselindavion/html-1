from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from database import get_session
from models import Room, Subscription, User

router = APIRouter(tags=["front"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse(url="/front/login")


@router.get("/front/login", response_class=HTMLResponse)
def login_page(request: Request, session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return templates.TemplateResponse("login.html", {"request": request, "users": users})


@router.get("/front/rooms", response_class=HTMLResponse)
def rooms_page(
    request: Request,
    user_id: Optional[int] = None,
    session: Session = Depends(get_session),
):
    if not user_id:
        return RedirectResponse(url="/front/login")
    user = session.get(User, user_id)
    if not user:
        return RedirectResponse(url="/front/login")

    rooms = session.exec(select(Room)).all()
    subs = session.exec(select(Subscription).where(Subscription.user_id == user_id)).all()
    subscribed_ids = {s.room_id for s in subs}

    return templates.TemplateResponse(
        "rooms.html",
        {"request": request, "user": user, "rooms": rooms, "subscribed_ids": subscribed_ids},
    )


@router.get("/front/rooms/{room_id}", response_class=HTMLResponse)
def chat_page(
    request: Request,
    room_id: int,
    user_id: Optional[int] = None,
    session: Session = Depends(get_session),
):
    if not user_id:
        return RedirectResponse(url="/front/login")
    user = session.get(User, user_id)
    room = session.get(Room, room_id)
    if not user or not room:
        return RedirectResponse(url="/front/login")

    return templates.TemplateResponse(
        "chat.html", {"request": request, "user": user, "room": room}
    )
