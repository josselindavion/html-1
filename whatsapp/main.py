from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from database import get_db, Message # On importe notre base de données
import uvicorn

app = FastAPI()

# On gère les websockets avec une classe pour organiser les connexions
class ConnectionManager:
    def __init__(self):
        # Un dictionnaire pour trier les gens par salon. 
        # Exemple : { "Mines": [websocket1, websocket2], "Famille": [websocket3] }
        self.rooms: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept() # On accepte la poignée de main WebSocket
        if room not in self.rooms:
            self.rooms[room] = []
        self.rooms[room].append(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        self.rooms[room].remove(websocket)

    async def broadcast(self, message: str, room: str):
        # On envoie le message UNIQUEMENT à la liste des gens de cette room
        if room in self.rooms:
            for connection in self.rooms[room]:
                await connection.send_text(message)

manager = ConnectionManager()