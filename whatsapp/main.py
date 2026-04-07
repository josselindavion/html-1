from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()

# On créé une classe pour gérer les connexions WebSocket et les messages
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Point d'entrée WebSocket - comme dans le cours
@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    await manager.broadcast(f"👋 {username} a rejoint le chat.")
    try:
        while True:
            # On attend qu'un message arrive - avant de le diffuser à tout le monde
            data = await websocket.receive_text()
            # On le diffuse à tout le monde
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        # Si l'utilisateur quitte la page ou se déconnecte / perd la connexion
        manager.disconnect(websocket)
        await manager.broadcast(f"🚪 {username} a quitté le chat.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)