# backend/app/routers/video_sync.py (or backend/app/services/video_sync.py)
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()
host_username = None
connected_clients: List[WebSocket] = []

@router.websocket("/ws/video_control/{username}")
async def video_control(websocket: WebSocket, username: str):
    global host_username
    await websocket.accept()
    connected_clients.append(websocket)
    
    # Assign host role
    if username.startswith("123"):
        host_username = username
        await websocket.send_text("You are the host")
    else:
        await websocket.send_text("You are a visitor")

    try:
        # Listen for video control messages from the host
        while True:
            data = await websocket.receive_text()
            if username == host_username:
                # Broadcast video state to all connected clients
                for client in connected_clients:
                    if client != websocket:
                        await client.send_text(f"Host changed video state: {data}")
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        if username == host_username:
            host_username = None
