"""
This file contains logic for managing user accounts.

- create_user(): Creates a new user and stores them in the database.
- get_user_by_username(): Retrieves a user by their username.

These functions are used by the authentication routes.
"""

from sqlalchemy.orm import Session
from app.models import User

def create_user(db: Session, username: str, password: str, email: str):
    """
    Create a new user and store them in the database.
    
    Args:
        db (Session): Database session.
        username (str): Username of the new user.
        password (str): Password (should be hashed in production).
        email (str): Email address of the user.

    Returns:
        User: The newly created user object.
    """
    user = User(username=username, password=password, email=email)
    db.add(user)  # Add user to the session
    db.commit()  # Commit the transaction
    db.refresh(user)  # Refresh to get the latest state from the DB
    return user

def get_user_by_username(db: Session, username: str):
    """
    Retrieve a user by their username from the database.

    Args:
        db (Session): Database session.
        username (str): Username to search for.

    Returns:
        User or None: The user object if found, else None.
    """
    return db.query(User).filter(User.username == username).first()
