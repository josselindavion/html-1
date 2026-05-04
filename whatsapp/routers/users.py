from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import User, UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=User, status_code=201)
def create_user(payload: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.name == payload.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ce nom d'utilisateur existe déjà")
    user = User(name=payload.name)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("", response_model=list[User])
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()
