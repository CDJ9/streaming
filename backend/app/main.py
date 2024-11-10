import os
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.models import Base
from app.dependencies import engine
from app.routers import auth, room, video_sync

app = FastAPI()

# Mount the frontend directory as static files

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(room.router, prefix="/room", tags=["Room"])
app.include_router(video_sync.router, prefix="/video_sync", tags=["Video Sync"])

# Connection manager to handle WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# WebSocket route for video control
@app.websocket("/ws/video_control/{username}")
async def video_control(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    try:
        if username.startswith("123"):
            await websocket.send_text("You are the host")
        else:
            await websocket.send_text("You are a visitor")

        # Listen for messages and broadcast if the user is the host
        while True:
            data = await websocket.receive_text()
            if username.startswith("123"):
                # Host sends message to all clients
                await manager.broadcast(data)
            else:
                await websocket.send_text("Visitors can't change the video state.")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print("WebSocket connection closed:", e)

# Serve the HTML frontend
@app.get("/", response_class=HTMLResponse)
def read_index():
    try:
        with open(os.path.join(frontend_path, "index.html"), "r") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="index.html not found", status_code=404)

@app.get("/routes")
def list_routes():
    return [{"path": route.path, "name": route.name} for route in app.router.routes]


@app.post("/test")
def test_endpoint():
    return {"message": "POST request successful!"}

frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
