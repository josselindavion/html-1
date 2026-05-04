import json
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from database import engine
from models import Message, User
from sqlmodel import Session

router = APIRouter()


class RoomManager:
    """Maintient la liste des connexions WebSocket actives par salon."""

    def __init__(self):
        self.connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int):
        await websocket.accept()
        self.connections.setdefault(room_id, []).append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: int):
        if room_id in self.connections:
            self.connections[room_id].remove(websocket)

    async def broadcast(self, room_id: int, data: dict):
        """Envoie un message JSON à tous les clients connectés dans le salon."""
        text = json.dumps(data)
        for ws in self.connections.get(room_id, []):
            await ws.send_text(text)


manager = RoomManager()


@router.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, user_id: int):
    # Vérification initiale : utilisateur et salon doivent exister
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            await websocket.close(code=4004)
            return

    await manager.connect(websocket, room_id)
    try:
        while True:
            text = await websocket.receive_text()
            # Nouvelle session par message pour éviter les conflits de transaction
            with Session(engine) as session:
                msg = Message(
                    content=text,
                    user_id=user_id,
                    room_id=room_id,
                    timestamp=datetime.utcnow(),
                )
                session.add(msg)
                session.commit()
                session.refresh(msg)
                username = session.get(User, user_id).name

            await manager.broadcast(room_id, {
                "id": msg.id,
                "content": msg.content,
                "username": username,
                "timestamp": msg.timestamp.isoformat(),
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
