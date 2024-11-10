from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services.auth_service import create_user, authenticate_user, get_user_by_username
from app.schemas import UserCreate

router = APIRouter()

@router.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if the user already exists
    existing_user = get_user_by_username(db, username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Create the new user
    create_user(db, username, password, email)
    return {"message": "User registered successfully"}

@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": f"Welcome {username}!"}
