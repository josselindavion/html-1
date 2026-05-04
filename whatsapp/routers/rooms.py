from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import Room, RoomCreate, Subscription, User

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


@router.post("/{room_id}/subscribe")
def subscribe(room_id: int, user_id: int, session: Session = Depends(get_session)):
    if not session.get(Room, room_id):
        raise HTTPException(status_code=404, detail="Salon introuvable")
    if not session.get(User, user_id):
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    existing = session.exec(
        select(Subscription).where(
            Subscription.user_id == user_id, Subscription.room_id == room_id
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Déjà abonné")
    session.add(Subscription(user_id=user_id, room_id=room_id))
    session.commit()
    return {"message": "Abonné avec succès"}


@router.delete("/{room_id}/subscribe")
def unsubscribe(room_id: int, user_id: int, session: Session = Depends(get_session)):
    sub = session.exec(
        select(Subscription).where(
            Subscription.user_id == user_id, Subscription.room_id == room_id
        )
    ).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Abonnement introuvable")
    session.delete(sub)
    session.commit()
    return {"message": "Désabonné avec succès"}
