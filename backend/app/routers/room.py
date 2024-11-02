# app/routers/room.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db  # Ensure this is correctly imported

# Create the APIRouter object
router = APIRouter()

# Example endpoint for creating a room
@router.post("/create")
def create_room(room_name: str, user_name: str, db: Session = Depends(get_db)):
    # Logic for creating a room (placeholder logic)
    return {"room_name": room_name, "host": user_name}
