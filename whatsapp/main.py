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

#ROUTE HTTP CLASSIQUE (L'historique)
@app.get("/api/history/{room}")
def get_room_history(room: str, db: Session = Depends(get_db)):
    # On va chercher dans la BDD tous les messages de ce salon
    messages = db.query(Message).filter(Message.room == room).all()
    # On renvoie du JSON classique
    return [{"username": m.username, "content": m.content} for m in messages]


#ROUTE WEBSOCKET (Le direct)
@app.websocket("/ws/{room}/{username}")
async def chat_endpoint(websocket: WebSocket, room: str, username: str, db: Session = Depends(get_db)):
    # 1. L'utilisateur se connecte
    await manager.connect(websocket, room)
    
    try:
        # 2. On écoute en permanence (boucle infinie)
        while True:
            # On attend un texte du client
            texte_recu = await websocket.receive_text()
            
            # 3. On sauvegarde dans la base de données
            nouveau_message = Message(room=room, username=username, content=texte_recu)
            db.add(nouveau_message)
            db.commit() # On valide l'enregistrement
            
            # 4. On diffuse à tout le salon
            await manager.broadcast(f"<b>{username}</b>: {texte_recu}", room)
            
    except WebSocketDisconnect:
        # 5. Si le tuyau casse (l'utilisateur ferme l'onglet)
        manager.disconnect(websocket, room)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)