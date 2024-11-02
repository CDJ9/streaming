from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.models import Base
from app.dependencies import engine
from app.routers import auth, room, video_sync

app = FastAPI()

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(room.router, prefix="/room", tags=["Room"])
app.include_router(video_sync.router, prefix="/video_sync", tags=["Video Sync"])

# Serve the HTML frontend
@app.get("/", response_class=HTMLResponse)
def read_index():
    with open("../frontend/index.html") as f:
        return f.read()
