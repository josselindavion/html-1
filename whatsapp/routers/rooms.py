from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import Room, RoomCreate

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("", response_model=Room, status_code=201)
def create_room(payload: RoomCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(Room).where(Room.name == payload.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ce salon existe déjà")
    room = Room(name=payload.name)
    session.add(room)
    session.commit()
    session.refresh(room)
    return room


@router.get("", response_model=list[Room])
def list_rooms(session: Session = Depends(get_session)):
    return session.exec(select(Room)).all()
