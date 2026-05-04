from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)


class Room(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)


class Subscription(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    room_id: int = Field(foreign_key="room.id", primary_key=True)


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    room_id: int = Field(foreign_key="room.id")


# Payload schemas (no table=True → pure Pydantic validation)
class UserCreate(SQLModel):
    name: str


class RoomCreate(SQLModel):
    name: str
