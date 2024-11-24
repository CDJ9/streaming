import os
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.models import Base, User
from app.dependencies import engine
from app.routers import auth, room, video_sync
from passlib.context import CryptContext
from app.schemas import UserCreate
from sqlalchemy.orm import Session


from fastapi import Depends
from app.dependencies import get_db


app = FastAPI()

# Mount the frontend directory as static files

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Allow requests from your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(room.router, prefix="/room", tags=["Room"])
app.include_router(video_sync.router, prefix="/video_sync", tags=["Video Sync"])

# Manage connections per room
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.active_connections:
            self.active_connections[room].remove(websocket)
            if not self.active_connections[room]:
                del self.active_connections[room]

    async def broadcast(self, room: str, message: str):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                await connection.send_text(message)

manager = ConnectionManager()

# WebSocket route for video control
@app.websocket("/ws/video_control/{room}/{username}")
async def video_control(websocket: WebSocket, room: str, username: str):
    await manager.connect(websocket, room)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(room, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
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


@app.post("/test-post")
def test_post():
    return {"message": "POST request successful"}


frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@app.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the username or email already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password
    hashed_password = get_password_hash(user.password)
    
    # Create a new user instance
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "username": new_user.username}