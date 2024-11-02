# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db  # Ensure correct import of get_db

router = APIRouter()  # This is the router object that needs to be defined

# Example endpoint for user signup
@router.post("/signup")
def signup(username: str, password: str, email: str, db: Session = Depends(get_db)):
    # Here, you would normally call a service to create the user
    return {"message": f"User {username} created successfully"}

# Example endpoint for user login
@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    # Example logic for login - you'd typically check the password here
    return {"message": f"Welcome {username}"}
